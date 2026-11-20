"""Benchmark reproduction (SPEC-001 section 8). Metrics are tested, never specific schedules."""
import sys
from fractions import Fraction
from pathlib import Path

import pytest

from model import (SolveStatus, SolverConfig, evaluate_schedule, rho_star_pair, solve_min_peak,
                   solve_strategy_a, solve_strategy_b, solve_strategy_c)
from benchmark_instance import EXPECTED, RHO_BENCH_PAISE, RHO_STAR_PAIR_INR, benchmark_instance

CFG = SolverConfig(num_workers=1, deterministic_time_limit=None)
VERIFIER_DIR = Path(__file__).resolve().parents[1] / "04_mathematical_model" / "verification"


@pytest.fixture(scope="module")
def inst():
    return benchmark_instance()


@pytest.fixture(scope="module")
def res(inst):
    return dict(A=solve_strategy_a(inst, CFG), B=solve_strategy_b(inst, CFG),
                C=solve_strategy_c(inst, RHO_BENCH_PAISE, CFG), P=solve_min_peak(inst, CFG))


def _at_rho(inst, r):
    return evaluate_schedule(inst, r.schedule, RHO_BENCH_PAISE)


def test_all_proven_optimal(res):
    for r in res.values():
        assert r.status == SolveStatus.OPTIMAL and r.proven_optimal


def test_strategy_a(inst, res):
    m, e = _at_rho(inst, res["A"]), EXPECTED["A"]
    assert m.makespan == e["makespan"] and m.sum_completion == e["sum_c"]
    assert m.ec_inr == Fraction(e["ec"]) and m.peak_kw == e["peak_kw"] and m.tec_inr == Fraction(e["tec"])


def test_strategy_b(inst, res):
    m, e = _at_rho(inst, res["B"]), EXPECTED["B"]
    assert m.makespan == e["makespan"] and m.ec_inr == Fraction(e["ec"])
    assert m.peak_kw == e["peak_kw"] and m.tec_inr == Fraction(e["tec"])
    assert res["B"].stage_values == [4_713_600_000, 8]


def test_strategy_c(inst, res):
    m, e = _at_rho(inst, res["C"]), EXPECTED["C"]
    assert m.tec_inr == Fraction(e["tec"]) and m.ec_inr == Fraction(e["ec"]) and m.peak_kw == e["peak_kw"]
    assert res["C"].stage_values == [7_905_600_000, 8]


def test_rho_star_pair_is_12_70(inst, res):
    mb, mc = _at_rho(inst, res["B"]), _at_rho(inst, res["C"])
    assert rho_star_pair(mb, mc) == Fraction(RHO_STAR_PAIR_INR)


def test_min_peak_extreme_point_confirms_rho_star(inst, res):
    mp = _at_rho(inst, res["P"])
    assert (mp.peak_kw, mp.ec_inr) == (27, Fraction("912.60"))
    assert rho_star_pair(_at_rho(inst, res["B"]), mp) == Fraction("12.70")


def test_b_tiebreak_band_collapses_on_benchmark(inst):
    lo = solve_strategy_b(inst, CFG, "min_peak").metrics
    hi = solve_strategy_b(inst, CFG, "max_peak").metrics
    assert lo.peak_w == hi.peak_w == 37000 and lo.ec_inr == hi.ec_inr == Fraction("785.60")


def test_c_at_rho_zero_agrees_with_b(inst, res):
    c0 = solve_strategy_c(inst, 0, CFG)
    assert c0.stage_values == res["B"].stage_values
    assert (c0.metrics.makespan, c0.metrics.ec_int) == (res["B"].metrics.makespan, res["B"].metrics.ec_int)


# --- cross-check against the *unmodified* exhaustive verifier -----------------------------------
@pytest.fixture(scope="module")
def verifier():
    sys.dont_write_bytecode = True            # never create __pycache__ in the verification folder
    sys.path.insert(0, str(VERIFIER_DIR))
    try:
        import verify_benchmark as vb
    finally:
        sys.path.remove(str(VERIFIER_DIR))
    metrics = [vb.evaluate_schedule(s) for s in vb.enumerate_all_feasible_schedules()]
    return vb, metrics


def test_verifier_enumerates_7530(verifier):
    assert len(verifier[1]) == 7530


@pytest.mark.parametrize("rho_inr", [0, 5, 10, 12, 14, 15, 20, 30])
def test_solver_tec_equals_enumerated_global_min(inst, verifier, rho_inr):
    vb, metrics = verifier
    r = solve_strategy_c(inst, rho_inr * 100, CFG)
    glob = min(m.energy_cost_inr + rho_inr * m.peak_demand_kw for m in metrics)
    assert abs(float(r.metrics.tec_inr) - glob) < 1e-6


@pytest.mark.parametrize("name", ["A", "B", "C"])
def test_solver_schedule_is_in_verifier_optimal_set(inst, res, verifier, name):
    vb, metrics = verifier
    out = {"A": vb.solve_strategy_a, "B": vb.solve_strategy_b, "C": vb.solve_strategy_c}[name](metrics)
    allowed = {frozenset((o.job_id, o.machine_id, o.start_slot, o.end_slot) for o in m.schedule)
               for m in out["all_optima"]}
    mine = frozenset((o.job_id, o.machine_id, o.start, o.end) for o in res[name].schedule)
    assert mine in allowed
    assert len(out["all_optima"]) == {"A": 4, "B": 12, "C": 6}[name]
