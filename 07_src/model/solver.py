"""Two/three-stage lexicographic solves for Strategies A, B, C (SPEC-001 sections 5-7).

Every stage is a *fresh* CP-SAT model: the previous stages' optima are added as exact integer
bounds (``<=`` for minimised stages, ``>=`` for maximised stages) and the previous solution is
passed as a hint. No epsilon-weighted objectives are used.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Sequence, Tuple

from ortools.sat.python import cp_model

from .evaluate import Metrics, ScheduleError, evaluate_schedule
from .extraction import extract_schedule
from .formulation import InfeasibleInstance, build_formulation
from .instance import Instance, Operation
from .validation import InstanceError


class SolveStatus(str, Enum):
    OPTIMAL = "OPTIMAL"
    FEASIBLE = "FEASIBLE"
    INFEASIBLE = "INFEASIBLE"
    UNKNOWN = "UNKNOWN"
    MODEL_INVALID = "MODEL_INVALID"


class InternalConsistencyError(RuntimeError):
    """The solver's own objective values disagree with the independent evaluator (a bug)."""


@dataclass(frozen=True)
class SolverConfig:
    """Solver policy (SPEC-001 D7). Defaults favour reproducibility over speed."""
    time_limit_s: float = 120.0                 # wall-clock limit per stage
    deterministic_time_limit: Optional[float] = 30.0  # machine-load independent limit per stage
    num_workers: int = 1                        # 1 => reproducible; parallelise across processes
    random_seed: int = 0
    log_search: bool = False
    redundant_constraints: bool = True   # NoOverlap + Cumulative performance aids (SPEC-001 section 3)
    # Optional smaller budgets for the tie-break stages (stage >= 2). None => same as stage 1.
    # Rationale: proving the *compactness* tie-break (min C_max among cost-optimal schedules) can be much
    # harder than proving the cost optimum itself on low-workload instances (see SPEC-001 section 6).
    tiebreak_time_limit_s: Optional[float] = None
    tiebreak_deterministic_time_limit: Optional[float] = None


@dataclass(frozen=True)
class Stage:
    expr: str      # one of cmax | sum_c | pmax | ec | dc | tec
    sense: str     # "min" | "max"


@dataclass
class StrategyResult:
    strategy: str
    status: SolveStatus
    proven_optimal: bool            # True iff EVERY stage was proven optimal
    reason: str
    rho_paise: int
    schedule: Optional[List[Operation]]
    metrics: Optional[Metrics]
    stage_exprs: List[str] = field(default_factory=list)
    stage_statuses: List[str] = field(default_factory=list)
    stage_values: List[int] = field(default_factory=list)
    stage_times_s: List[float] = field(default_factory=list)
    wall_time_s: float = 0.0
    best_bound_last_stage: Optional[float] = None
    num_workers: int = 1
    random_seed: int = 0

    n_stages: int = 0                # number of stages defined for the strategy

    @property
    def proven_stages(self) -> int:
        """Number of LEADING stages proven OPTIMAL (stages after the first non-OPTIMAL one never run)."""
        n = 0
        for st in self.stage_statuses:
            if st != SolveStatus.OPTIMAL.value:
                break
            n += 1
        return n

    @property
    def primary_proven(self) -> bool:
        """Stage 1 (the strategy's primary objective) was proven optimal; later stages may not be.
        NOT the same as ``proven_optimal`` (= every stage proven). ``proven_optimal`` implies ``primary_proven``."""
        return self.proven_stages >= 1


_STATUS_MAP = {
    cp_model.OPTIMAL: SolveStatus.OPTIMAL,
    cp_model.FEASIBLE: SolveStatus.FEASIBLE,
    cp_model.INFEASIBLE: SolveStatus.INFEASIBLE,
    cp_model.MODEL_INVALID: SolveStatus.MODEL_INVALID,
    cp_model.UNKNOWN: SolveStatus.UNKNOWN,
}


def combine_status(stage_statuses: Sequence[SolveStatus], have_solution: bool) -> SolveStatus:
    """Strategy-level status from the per-stage statuses (SPEC-001 section 6).

    A FEASIBLE (non-proven) result is *never* promoted to OPTIMAL.
    """
    if not stage_statuses:
        return SolveStatus.UNKNOWN
    first = stage_statuses[0]
    if first in (SolveStatus.INFEASIBLE, SolveStatus.MODEL_INVALID):
        return first
    if not have_solution:
        return SolveStatus.UNKNOWN
    if all(s == SolveStatus.OPTIMAL for s in stage_statuses):
        return SolveStatus.OPTIMAL
    return SolveStatus.FEASIBLE


def _params(cfg: SolverConfig, stage_index: int = 0) -> cp_model.CpSolver:
    s = cp_model.CpSolver()
    tl, dl = cfg.time_limit_s, cfg.deterministic_time_limit
    if stage_index >= 1:
        if cfg.tiebreak_time_limit_s is not None:
            tl = cfg.tiebreak_time_limit_s
        if cfg.tiebreak_deterministic_time_limit is not None:
            dl = cfg.tiebreak_deterministic_time_limit
    s.parameters.max_time_in_seconds = tl
    if dl is not None:
        s.parameters.max_deterministic_time = dl
    s.parameters.num_workers = cfg.num_workers
    s.parameters.random_seed = cfg.random_seed
    s.parameters.log_search_progress = cfg.log_search
    return s


def run_lexicographic(inst: Instance, strategy: str, stages: Sequence[Stage], rho_paise: int = 0,
                      config: Optional[SolverConfig] = None) -> StrategyResult:
    """Solve ``stages`` in order over the shared feasible set and evaluate the result independently."""
    cfg = config or SolverConfig()
    t_start = time.perf_counter()
    res = StrategyResult(strategy=strategy, status=SolveStatus.UNKNOWN, proven_optimal=False, reason="",
                         rho_paise=rho_paise, schedule=None, metrics=None,
                         num_workers=cfg.num_workers, random_seed=cfg.random_seed,
                         n_stages=len(stages))
    statuses: List[SolveStatus] = []
    fixed: List[Tuple[str, str, int]] = []
    hint: Optional[Dict] = None
    last_x: Optional[Dict] = None
    last_vals: Optional[Dict[str, int]] = None

    for k, st in enumerate(stages):
        try:
            form = build_formulation(inst, rho_paise, redundant=cfg.redundant_constraints)
        except InfeasibleInstance as exc:
            res.status, res.reason = SolveStatus.INFEASIBLE, str(exc)
            res.wall_time_s = time.perf_counter() - t_start
            return res
        model = form.model
        for name, sense, val in fixed:
            model.add(form.exprs[name] <= val) if sense == "min" else model.add(form.exprs[name] >= val)
        if st.sense == "min":
            model.minimize(form.exprs[st.expr])
        else:
            model.maximize(form.exprs[st.expr])
        if hint is not None:
            for tr, var in form.x.items():
                model.add_hint(var, hint.get(tr, 0))
        solver = _params(cfg, k)
        t0 = time.perf_counter()
        code = solver.solve(model)
        dt = time.perf_counter() - t0
        status = _STATUS_MAP.get(code, SolveStatus.UNKNOWN)
        res.stage_exprs.append(f"{st.sense} {st.expr}")
        res.stage_statuses.append(status.value)
        res.stage_times_s.append(dt)
        if status in (SolveStatus.OPTIMAL, SolveStatus.FEASIBLE):
            xs = {tr: solver.value(v) for tr, v in form.x.items()}
            vals = {n: int(solver.value(e)) for n, e in form.exprs.items()}
            res.stage_values.append(vals[st.expr])
            res.best_bound_last_stage = solver.best_objective_bound
            hint, last_x, last_vals = xs, xs, vals          # preserve the best schedule found so far
            statuses.append(status)
            if status != SolveStatus.OPTIMAL:
                # The stage value is NOT proven, so it must not be frozen as a lexicographic bound and no later
                # stage may run: a later stage would optimise over a feasible set defined by an unproven value.
                res.reason = (f"stage {k + 1} ({st.sense} {st.expr}) ended with {status.value}; "
                              f"lexicographic hierarchy stopped, feasible schedule returned")
                break
            fixed.append((st.expr, st.sense, vals[st.expr]))  # exact bound: only OPTIMAL values are fixed
        else:
            statuses.append(status)
            if k == 0:
                res.reason = f"stage 1 ended with {status.value}"
                break
            if status == SolveStatus.INFEASIBLE:  # cannot happen: previous solution satisfies all fixed bounds
                raise InternalConsistencyError(
                    f"{strategy}: stage {k + 1} INFEASIBLE although stage {k}'s solution satisfies its bounds")
            res.reason = f"stage {k + 1} ended with {status.value}; returning stage {k} solution"
            break

    res.wall_time_s = time.perf_counter() - t_start
    res.status = combine_status(statuses, last_x is not None)
    res.proven_optimal = res.status == SolveStatus.OPTIMAL
    if last_x is not None:
        sched = extract_schedule(inst, last_x)
        try:
            m = evaluate_schedule(inst, sched, rho_paise, strict=True)
        except ScheduleError as exc:  # solver produced an infeasible schedule: a bug, never hide it
            raise InternalConsistencyError(f"{strategy}: solver schedule failed independent check: {exc}") from exc
        mism = [
            f"{n}: solver={last_vals[n]} evaluator={v}"
            for n, v in (("cmax", m.makespan), ("sum_c", m.sum_completion), ("pmax", m.peak_w),
                         ("ec", m.ec_int), ("dc", m.dc_int), ("tec", m.tec_int))
            if last_vals[n] != v
        ]
        if mism:
            raise InternalConsistencyError(f"{strategy}: solver/evaluator mismatch: " + "; ".join(mism))
        res.schedule, res.metrics = sched, m
    return res


# --- strategy definitions (SPEC-001 section 5) ---------------------------------------------

def solve_strategy_a(inst: Instance, config: Optional[SolverConfig] = None) -> StrategyResult:
    """A: min C_max, then min sum C_j. No energy/peak information is used."""
    return run_lexicographic(inst, "A", [Stage("cmax", "min"), Stage("sum_c", "min")], 0, config)


def solve_strategy_b(inst: Instance, config: Optional[SolverConfig] = None,
                     tie_break: str = "makespan") -> StrategyResult:
    """B: min EC, then min C_max (rho = 0).

    ``tie_break``: "makespan" (documented definition) | "min_peak" | "max_peak" (D4 robustness band,
    adds a third stage on P_max among EC- and makespan-optimal schedules).
    """
    stages = [Stage("ec", "min"), Stage("cmax", "min")]
    name = "B"
    if tie_break == "min_peak":
        stages.append(Stage("pmax", "min")); name = "B_minpeak"
    elif tie_break == "max_peak":
        stages.append(Stage("pmax", "max")); name = "B_maxpeak"
    elif tie_break != "makespan":
        raise ValueError(f"unknown tie_break {tie_break!r}")
    return run_lexicographic(inst, name, stages, 0, config)


def solve_strategy_c(inst: Instance, rho_paise: int, config: Optional[SolverConfig] = None) -> StrategyResult:
    """C: min TEC = EC + rho*Pmax, then min C_max."""
    return run_lexicographic(inst, "C", [Stage("tec", "min"), Stage("cmax", "min")], rho_paise, config)


def solve_min_peak(inst: Instance, config: Optional[SolverConfig] = None) -> StrategyResult:
    """P (analysis only): min P_max, then min EC, then min C_max (extreme point of the frontier)."""
    return run_lexicographic(inst, "P", [Stage("pmax", "min"), Stage("ec", "min"), Stage("cmax", "min")], 0, config)
