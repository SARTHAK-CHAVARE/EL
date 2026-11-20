"""Regression tests for the correctness pass (issue 1 and the lexicographic-bound / flag-confusion checks)."""
import types

import pytest
from ortools.sat.python import cp_model

import model.solver as solver_mod
from benchmark_instance import RHO_BENCH_PAISE, benchmark_instance
from model import (SolveStatus, SolverConfig, check_schedule, solve_min_peak, solve_strategy_a, solve_strategy_b,
                   solve_strategy_c)
from oracle import random_instance

CFG = SolverConfig(num_workers=1, deterministic_time_limit=None)


class _Forced:
    """Delegates to a real CpSolver but reports FEASIBLE instead of OPTIMAL for selected stages (deterministic
    stand-in for a time-limit hit: the incumbent is genuinely optimal, but the *claim* is withheld)."""

    def __init__(self, real, force, log, k):
        self._real, self._force, self._log, self._k = real, force, log, k

    def solve(self, model):
        code = self._real.solve(model)
        self._log.append(self._k)
        return cp_model.FEASIBLE if (code == cp_model.OPTIMAL and self._k in self._force) else code

    def __getattr__(self, name):
        return getattr(self._real, name)


@pytest.fixture
def force_stages(monkeypatch):
    log = []

    def install(stages):
        real_params = solver_mod._params
        monkeypatch.setattr(solver_mod, "_params",
                            lambda cfg, k=0: _Forced(real_params(cfg, k), set(stages), log, k))
        return log
    return install


def test_stage2_not_optimal_stops_hierarchy_and_keeps_schedule(force_stages):
    inst = benchmark_instance()
    log = force_stages({1})                                   # stage 2 (index 1) reported FEASIBLE
    r = solve_strategy_b(inst, CFG, "min_peak")               # 3 stages defined: ec, cmax, pmax
    assert log == [0, 1]                                      # stage 3 was NEVER solved
    assert r.stage_statuses == ["OPTIMAL", "FEASIBLE"]
    assert len(r.stage_values) == 2 and r.n_stages == 3
    assert r.status == SolveStatus.FEASIBLE and not r.proven_optimal
    assert r.primary_proven and r.proven_stages == 1
    assert "stopped" in r.reason
    assert r.schedule is not None and check_schedule(inst, r.schedule) == []
    assert r.metrics.ec_int == r.stage_values[0]              # proven stage-1 bound still honoured


def test_stage1_not_optimal_runs_no_further_stage(force_stages):
    inst = benchmark_instance()
    log = force_stages({0})
    r = solve_strategy_c(inst, RHO_BENCH_PAISE, CFG)
    assert log == [0]
    assert r.status == SolveStatus.FEASIBLE and not r.proven_optimal and not r.primary_proven
    assert r.proven_stages == 0 and r.schedule is not None and check_schedule(inst, r.schedule) == []


def test_p_strategy_three_stage_stop_after_second(force_stages):
    log = force_stages({1})
    r = solve_min_peak(benchmark_instance(), CFG)
    assert log == [0, 1] and r.proven_stages == 1 and r.status == SolveStatus.FEASIBLE


def test_all_stages_optimal_flags_consistent():
    r = solve_strategy_b(benchmark_instance(), CFG, "max_peak")
    assert r.status == SolveStatus.OPTIMAL and r.proven_optimal and r.primary_proven
    assert r.proven_stages == r.n_stages == 3 and len(r.stage_values) == 3


def test_flags_cannot_be_confused_invariants():
    """proven_optimal  <=>  status OPTIMAL  <=>  proven_stages == n_stages;  proven_optimal => primary_proven."""
    for seed in range(15):
        inst = random_instance(seed)
        for r in (solve_strategy_a(inst, CFG), solve_strategy_b(inst, CFG, "min_peak"),
                  solve_strategy_c(inst, 1500, CFG), solve_min_peak(inst, CFG)):
            assert r.proven_optimal == (r.status == SolveStatus.OPTIMAL)
            if r.status != SolveStatus.INFEASIBLE:
                assert r.proven_optimal == (r.proven_stages == r.n_stages)
            if r.proven_optimal:
                assert r.primary_proven
            assert r.primary_proven == (r.proven_stages >= 1)


STAGE_EXPRS = {
    "A": ("makespan", "sum_completion"),
    "B": ("ec_int", "makespan"),
    "B_minpeak": ("ec_int", "makespan", "peak_w"),
    "B_maxpeak": ("ec_int", "makespan", "peak_w"),
    "P": ("peak_w", "ec_int", "makespan"),
    "C": ("tec_int", "makespan"),
}


@pytest.mark.parametrize("seed", range(30))
def test_every_stage_value_is_attained_by_the_returned_schedule(seed):
    """Lexicographic bounds are exact: each stage objective equals the stage value fixed for the later stages."""
    inst = random_instance(seed)
    results = [solve_strategy_a(inst, CFG), solve_strategy_b(inst, CFG), solve_strategy_b(inst, CFG, "min_peak"),
               solve_strategy_b(inst, CFG, "max_peak"), solve_min_peak(inst, CFG), solve_strategy_c(inst, 1500, CFG)]
    for r in results:
        if r.status != SolveStatus.OPTIMAL:
            continue
        got = tuple(getattr(r.metrics, a) for a in STAGE_EXPRS[r.strategy])
        assert got == tuple(r.stage_values), (r.strategy, got, r.stage_values)


def test_stage_senses_and_order_are_as_specified():
    inst = benchmark_instance()
    assert solve_strategy_b(inst, CFG, "max_peak").stage_exprs == ["min ec", "min cmax", "max pmax"]
    assert solve_strategy_b(inst, CFG, "min_peak").stage_exprs == ["min ec", "min cmax", "min pmax"]
    assert solve_min_peak(inst, CFG).stage_exprs == ["min pmax", "min ec", "min cmax"]
    assert solve_strategy_c(inst, 100, CFG).stage_exprs == ["min tec", "min cmax"]
    assert solve_strategy_a(inst, CFG).stage_exprs == ["min cmax", "min sum_c"]
