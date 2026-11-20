"""Energy-cost vs peak front (epsilon-constraint over P_max) and everything derived from it.

Method (master_execution_plan.md Part 5, epsilon-constraint; ROADMAP-FINAL.md P1). Model V1.0 is used unchanged;
the only addition is the exact integer bound ``pmax <= cap`` passed to ``run_lexicographic`` as an extra bound.

    top      : min EC, then min P_max, then min C_max                     (no cap)
    P        : min P_max, then min EC, then min C_max                     (minimum-peak extreme, certifies termination)
    repeat   : cap := (peak of the last point found) - 1 W
               min EC, then min P_max, then min C_max  subject to P_max <= cap
    until    : cap < proven minimum peak (from P or the structural bound below), or a capped solve is proven INFEASIBLE.

Structural peak bound (a proof, no solve): all operations lie in the window [min release, max deadline] of H slots
and job j occupies at least min_m p_jm slots, so the machines are busy for at least  W_min = sum_j min_m p_jm
machine-slots. If at most k-1 machines were busy in every slot, at most (k-1)*H machine-slots would be available;
hence with k = ceil(W_min / H) some slot has at least k busy machines, and every busy machine m draws at least
min_j power_jm. So   peak >= base + (sum of the k smallest per-machine minimum powers).
For W > (M-1)/M this equals the maximum possible peak: no peak reduction exists (ROADMAP-FINAL.md 1.4.3).

The number of points is discovered by the loop; nothing is assumed about how many exist. Each step lowers the peak by
at least 1 W, so the loop terminates. P's schedule satisfies every cap >= its peak and is passed as a hint, so every
such capped solve starts from a feasible schedule.

Why this gives the exact front when every EC stage is proven: point k = (e_k, q_k) with e_k = min EC over schedules
with peak <= c_k. The next solve proves e_{k+1} = min EC over peak <= q_k - 1. If e_{k+1} > e_k no schedule with peak
< q_k reaches e_k (point k is nondominated); if e_{k+1} = e_k, point k is dominated and dropped. So only the EC stage
of each solve and the termination need proofs; an unproven P_max tie-break stage cannot make the front wrong.

Everything derived (C at any rho, break-even, TEC lower bound) is labelled EXACT only if ``Front.complete``.
Otherwise the front's points are still real, independently evaluated schedules, so a break-even computed from them is
an UPPER BOUND on the true one (a better schedule may have been missed), never a guess.

Units: ec_int in 1/6e6 INR; peak in W; rho in paise/kW; TEC_int = ec_int + 60 * rho_paise * peak_w.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Dict, List, Mapping, Optional, Sequence, Tuple

from .evaluate import Metrics, ScheduleError, evaluate_schedule
from .instance import Instance, Operation
from .solver import (SolveStatus, SolverConfig, Stage, StrategyResult, run_lexicographic, solve_min_peak)

FRONT_STAGES = (Stage("ec", "min"), Stage("pmax", "min"), Stage("cmax", "min"))
_OPT = SolveStatus.OPTIMAL.value


def tec_int(ec_int: int, peak_w: int, rho_paise: int) -> int:
    return ec_int + 60 * rho_paise * peak_w


def ratio_inr_per_kw(d_ec_int: int, d_peak_w: int) -> Fraction:
    """(d_ec/6e6 INR) / (d_peak/1000 kW), exact."""
    return Fraction(d_ec_int, 6000 * d_peak_w)


def schedule_hint(schedule: Sequence[Operation]) -> Dict[Tuple[str, int, int], int]:
    """x[j,m,t] hint from a schedule (all other placements default to 0)."""
    return {(o.job_id, o.machine_id, o.start): 1 for o in schedule}


# ============================================================================================ data
@dataclass(frozen=True)
class FrontSolve:
    label: str                 # "top" | "P" | "cap"
    cap_w: Optional[int]       # None for top and P
    result: StrategyResult
    reused: bool = False       # P result supplied by the caller (its time is not part of this front's wall time)


@dataclass(frozen=True)
class FrontPoint:
    peak_w: int
    ec_int: int
    makespan: int
    schedule: Tuple[Operation, ...]
    metrics: Metrics
    ec_proven: bool            # EC is the proven minimum over all schedules with peak <= cap_w
    peak_proven: bool          # P_max tie-break stage proven (not needed for front exactness, see module doc)
    makespan_proven: bool      # C_max tie-break stage proven (needed for the makespan of a derived C)
    source: str                # "top" | "cap" | "P"
    cap_w: Optional[int]


@dataclass
class Front:
    points: List[FrontPoint]           # nondominated, peak strictly decreasing, EC strictly increasing
    solves: List[FrontSolve]
    dominated: List[FrontPoint]        # found but dominated (possible only after an unproven P_max stage)
    complete: bool                     # True => points are EXACTLY the nondominated (EC, peak) set
    termination: str   # P_bound | structural_bound | infeasible_cap | unproven | instance_infeasible | no_solution
    reason: str
    wall_time_s: float
    regions: List[Tuple[int, int]] = field(default_factory=list)  # (EC lower bound, peak lower bound), see below
    lb_valid: bool = False             # regions cover every feasible schedule

    @property
    def n_solves(self) -> int:
        return sum(1 for s in self.solves if not s.reused)

    @property
    def min_ec_point(self) -> Optional[FrontPoint]:
        return self.points[0] if self.points else None

    @property
    def min_peak_point(self) -> Optional[FrontPoint]:
        return self.points[-1] if self.points else None


# ============================================================================================ construction
def _point(res: StrategyResult, source: str, cap: Optional[int]) -> FrontPoint:
    m = res.metrics
    st = res.stage_statuses
    if source == "P":    # stages (pmax, ec, cmax): EC proven means stage 2 proven (stage 1 implicit)
        ec_p, pk_p, mk_p = res.proven_stages >= 2, res.proven_stages >= 1, res.proven_stages >= 3
    else:                # stages (ec, pmax, cmax)
        ec_p, pk_p, mk_p = res.proven_stages >= 1, res.proven_stages >= 2, res.proven_stages >= 3
    return FrontPoint(peak_w=m.peak_w, ec_int=m.ec_int, makespan=m.makespan, schedule=tuple(res.schedule),
                      metrics=m, ec_proven=ec_p, peak_proven=pk_p, makespan_proven=mk_p, source=source, cap_w=cap)


def _ec_lower_bound(res: StrategyResult, ec_stage_index: int) -> Optional[int]:
    """Valid integer lower bound on the EC stage: the proven value if OPTIMAL, else floor(CP-SAT bound)."""
    if len(res.stage_statuses) <= ec_stage_index:
        return None
    if res.stage_statuses[ec_stage_index] == _OPT:
        return int(res.stage_values[ec_stage_index])
    b = res.stage_bounds[ec_stage_index] if len(res.stage_bounds) > ec_stage_index else None
    return None if b is None or math.isinf(b) or math.isnan(b) else int(math.floor(b))


def structural_peak_lower_bound(inst: Instance) -> int:
    """Proven lower bound on the peak of EVERY feasible schedule (see module docstring)."""
    work = sum(min(j.proc.values()) for j in inst.jobs)
    lo = min(j.release for j in inst.jobs)
    hi = max(inst.job_deadline(j) for j in inst.jobs)
    horizon = hi - lo + 1
    if work <= 0 or horizon <= 0:
        return inst.base_w
    k = -(-work // horizon)                                   # ceil(work / horizon)
    machine_min = sorted(min(j.power_w[m] for j in inst.jobs if m in j.proc)
                         for m in inst.machines if any(m in j.proc for j in inst.jobs))
    return inst.base_w + sum(machine_min[:k])


def filter_dominated(found: Sequence[FrontPoint]) -> Tuple[List[FrontPoint], List[FrontPoint]]:
    """Split points found in strictly decreasing peak order into (nondominated, dominated)."""
    keep, drop = [], []
    for i, p in enumerate(found):
        if any(q.ec_int <= p.ec_int and q.peak_w <= p.peak_w and (q.ec_int, q.peak_w) != (p.ec_int, p.peak_w)
               for q in found[i + 1:]):
            drop.append(p)
        else:
            keep.append(p)
    return keep, drop


def ec_peak_front(inst: Instance, config: Optional[SolverConfig] = None,
                  p_result: Optional[StrategyResult] = None) -> Front:
    """Discover the energy-cost / peak front of ``inst`` (see module docstring).

    ``p_result``: an already computed ``solve_min_peak`` result for this instance and config (optional reuse).
    Regions (for ``tec_lower_bound``): every feasible schedule lies in some region (e_lb, q_lb) meaning
    EC >= e_lb and peak >= q_lb.
    """
    cfg = config or SolverConfig()
    t0 = time.perf_counter()
    s_lb = structural_peak_lower_bound(inst)
    solves: List[FrontSolve] = []
    found: List[FrontPoint] = []
    regions: List[Tuple[int, int]] = []

    top = run_lexicographic(inst, "FRONT_top", FRONT_STAGES, 0, cfg)
    solves.append(FrontSolve("top", None, top))
    if top.status == SolveStatus.INFEASIBLE:
        return Front([], solves, [], True, "instance_infeasible", top.reason, time.perf_counter() - t0, [], True)
    if top.schedule is None:
        return Front([], solves, [], False, "no_solution", f"top solve: {top.reason}", time.perf_counter() - t0)
    found.append(_point(top, "top", None))
    top_ec_lb = _ec_lower_bound(top, 0)
    if top_ec_lb is not None:
        regions.append((top_ec_lb, found[-1].peak_w))
    if found[-1].peak_w < s_lb:   # impossible: the bound is a proof
        raise RuntimeError(f"structural peak bound {s_lb} W exceeds a feasible peak {found[-1].peak_w} W")
    if found[-1].peak_w == s_lb:  # the energy optimum already has the provably minimal peak: one-point front
        return Front(points=found, solves=solves, dominated=[], complete=top.proven_stages >= 1,
                     termination="structural_bound",
                     reason=f"energy-optimal peak {s_lb} W equals the structural lower bound (no reduction possible)",
                     wall_time_s=time.perf_counter() - t0, regions=regions, lb_valid=top_ec_lb is not None)

    if p_result is None:
        bottom = solve_min_peak(inst, cfg)
        solves.append(FrontSolve("P", None, bottom))
    else:
        bottom = p_result
        solves.append(FrontSolve("P", None, bottom, reused=True))
    pmin = bottom.stage_values[0] if bottom.proven_stages >= 1 else None
    pmin_lb = s_lb
    if bottom.stage_bounds and bottom.stage_bounds[0] is not None and not math.isinf(bottom.stage_bounds[0]):
        pmin_lb = max(s_lb, int(math.ceil(bottom.stage_bounds[0] - 1e-9)))
    if pmin is not None:
        pmin_lb = pmin
    p_hint = schedule_hint(bottom.schedule) if bottom.schedule else None
    p_peak = bottom.metrics.peak_w if bottom.metrics else None

    termination, reason = "", ""
    lb_valid = top_ec_lb is not None
    cap = found[-1].peak_w - 1
    while True:
        if cap < s_lb:
            termination, reason = "structural_bound", f"cap {cap} W below the structural peak bound {s_lb} W"
            break
        if pmin is not None and cap < pmin:
            termination, reason = "P_bound", f"cap {cap} W below the proven minimum peak {pmin} W"
            break
        if pmin is not None and cap == pmin and bottom.proven_stages >= 2:
            pt = _point(bottom, "P", cap)
            found.append(pt)
            regions.append((int(bottom.stage_values[1]), pmin))
            termination, reason = "P_bound", "reached the proven minimum-peak point (taken from P)"
            break
        hint = p_hint if (p_peak is not None and p_peak <= cap) else None
        r = run_lexicographic(inst, "FRONT_cap", FRONT_STAGES, 0, cfg, extra_bounds=[("pmax", "min", cap)],
                              initial_hint=hint)
        solves.append(FrontSolve("cap", cap, r))
        if r.status == SolveStatus.INFEASIBLE:
            termination, reason = "infeasible_cap", f"no schedule with peak <= {cap} W (proven)"
            break
        lb = _ec_lower_bound(r, 0)
        if r.schedule is None:
            termination = "unproven"
            reason = f"capped solve at {cap} W ended {r.status.value} without a schedule; front below is unknown"
            fallback = lb if lb is not None else top_ec_lb
            if fallback is None:
                lb_valid = False
            else:
                regions.append((fallback, pmin_lb))
            break
        pt = _point(r, "cap", cap)
        found.append(pt)
        if lb is None:
            lb_valid = False
        else:
            regions.append((lb, pt.peak_w))
        cap = pt.peak_w - 1

    keep, drop = filter_dominated(found)
    complete = (top.proven_stages >= 1
                and all(s.result.proven_stages >= 1 for s in solves if s.label == "cap"
                        and s.result.status != SolveStatus.INFEASIBLE)
                and ((termination == "P_bound" and pmin is not None)
                     or termination in ("infeasible_cap", "structural_bound")))
    if not complete and not reason:
        reason = "an EC stage or the termination is unproven"
    return Front(points=keep, solves=solves, dominated=drop, complete=complete, termination=termination,
                 reason=reason, wall_time_s=time.perf_counter() - t0, regions=regions, lb_valid=lb_valid)


# ============================================================================================ derived quantities
def best_for_rho(front: Front, rho_paise: int) -> Optional[FrontPoint]:
    """C(rho) from the front: min TEC, ties broken by min makespan (the direct-C lexicographic order).

    TEC is exact for every rho >= 0 when the front is complete. The makespan equals direct C's for every rho > 0. At
    rho = 0 exactly, direct C may break the EC tie with a schedule of HIGHER peak and shorter makespan, which is
    dominated on (EC, peak) and therefore not on the front; then this point's makespan can be larger. ``recommend``
    with the energy-only schedule B as a candidate resolves that case (equal TEC, lower makespan wins)."""
    if not front.points:
        return None
    return min(front.points, key=lambda p: (tec_int(p.ec_int, p.peak_w, rho_paise), p.makespan))


def rho_intervals(front: Front) -> List[Optional[Tuple[Fraction, Optional[Fraction]]]]:
    """Per point: the rho range [lo, hi] (INR/kW) on which it minimises TEC (None = never: unsupported point).

    hi None means unbounded. Endpoints are ties with a neighbouring point."""
    out = []
    pts = front.points
    for i, p in enumerate(pts):
        lo, hi = Fraction(0), None
        ok = True
        for j, q in enumerate(pts):
            if j == i:
                continue
            if q.peak_w > p.peak_w:          # q: higher peak, lower EC -> p needs rho >= ...
                r = ratio_inr_per_kw(p.ec_int - q.ec_int, q.peak_w - p.peak_w)
                lo = max(lo, r)
            else:                            # q: lower peak, higher EC -> p needs rho <= ...
                r = ratio_inr_per_kw(q.ec_int - p.ec_int, p.peak_w - q.peak_w)
                hi = r if hi is None else min(hi, r)
        if hi is not None and lo > hi:
            ok = False
        out.append((lo, hi) if ok else None)
    return out


@dataclass(frozen=True)
class BreakEven:
    rho_inr: Optional[Fraction]   # smallest rho at which some schedule has lower TEC than the reference
    kind: str                     # exact | upper_bound | no_peak_reduction | undetermined
    reference: str
    via_peak_w: Optional[int] = None

    @property
    def is_exact(self) -> bool:
        return self.kind in ("exact", "no_peak_reduction")


def break_even(front: Front, ref_ec_int: int, ref_peak_w: int, reference: str = "B") -> BreakEven:
    """Break-even demand charge of the peak-aware optimum against a FIXED reference schedule (EC, peak).

    For rho above the value, some schedule is strictly cheaper than the reference; at the value, a tie.
    kind = exact if the front is complete; upper_bound if computed from an incomplete front (real schedules, so
    the true value can only be lower); no_peak_reduction if the complete front has no point below the reference
    peak; undetermined if the front is incomplete and has no such point.
    """
    cands = [p for p in front.points if p.peak_w < ref_peak_w]
    if not cands:
        return BreakEven(None, "no_peak_reduction" if front.complete else "undetermined", reference)
    best = min(cands, key=lambda p: (ratio_inr_per_kw(max(0, p.ec_int - ref_ec_int), ref_peak_w - p.peak_w),
                                     -p.peak_w))
    val = ratio_inr_per_kw(max(0, best.ec_int - ref_ec_int), ref_peak_w - best.peak_w)
    return BreakEven(val, "exact" if front.complete else "upper_bound", reference, best.peak_w)


def tec_lower_bound(front: Front, rho_paise: int) -> Optional[int]:
    """Valid lower bound on min TEC(rho) over ALL feasible schedules (None if the regions are not valid)."""
    if not front.lb_valid or not front.regions:
        return None
    return min(tec_int(e, q, rho_paise) for e, q in front.regions)


# ============================================================================================ safety guard
@dataclass(frozen=True)
class Recommendation:
    rho_paise: int
    choice: str
    schedule: Tuple[Operation, ...]
    metrics: Metrics
    tec_lower_bound: Optional[int]
    gap: Optional[Fraction]               # (TEC - LB) / TEC, None if no valid bound
    proven_optimal: bool                  # complete front and TEC equals the lower bound
    candidate_tec: Dict[str, int]
    rejected: Dict[str, str]


def recommend(inst: Instance, rho_paise: int, front: Front,
              extra_candidates: Optional[Mapping[str, Optional[Sequence[Operation]]]] = None) -> Recommendation:
    """Product guard: return the cheapest independently re-evaluated feasible schedule among the front points and
    ``extra_candidates`` (e.g. B, energy rules, FCFS). The returned TEC is therefore never above any candidate's,
    in particular never above B's, even when solves were unproven. Ties: lower makespan, then front points first."""
    cands: List[Tuple[str, Sequence[Operation]]] = [
        (f"front[peak={p.peak_w}W]", p.schedule) for p in front.points]
    for name, sched in (extra_candidates or {}).items():
        cands.append((name, sched))
    tecs: Dict[str, int] = {}
    rejected: Dict[str, str] = {}
    best = None
    for order, (name, sched) in enumerate(cands):
        if sched is None:
            rejected[name] = "no schedule"
            continue
        try:
            m = evaluate_schedule(inst, sched, rho_paise, strict=True)
        except ScheduleError as exc:
            rejected[name] = f"infeasible: {exc.violations[:2]}"
            continue
        tecs[name] = m.tec_int
        key = (m.tec_int, m.makespan, order)
        if best is None or key < best[0]:
            best = (key, name, tuple(sched), m)
    if best is None:
        raise ValueError("no feasible candidate schedule")
    _, name, sched, m = best
    lb = tec_lower_bound(front, rho_paise)
    if lb is not None and m.tec_int < lb:   # a feasible schedule below a "valid" lower bound would be a bug
        raise RuntimeError(f"TEC lower bound {lb} exceeds the feasible TEC {m.tec_int} of {name!r}")
    gap = None if lb is None else Fraction(m.tec_int - lb, m.tec_int) if m.tec_int else Fraction(0)
    proven = bool(front.complete and lb is not None and m.tec_int == lb)
    return Recommendation(rho_paise, name, sched, m, lb, gap, proven, tecs, rejected)
