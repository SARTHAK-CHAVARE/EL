"""Energy-cost / peak front (model/front.py): exhaustive-oracle agreement, benchmark, exactness labels, safety guard.

The oracle enumerates EVERY feasible schedule of small seeded instances, so the true nondominated (EC, peak) set, the
true C(rho), the true break-even and the true minimum TEC are known exactly.
"""
import dataclasses
from fractions import Fraction

import pytest

import model.front as front_mod
from benchmark_instance import benchmark_instance
from model import (Operation, SolveStatus, SolverConfig, Stage, best_for_rho, break_even, check_schedule,
                   ec_peak_front, filter_dominated, recommend, rho_intervals, run_lexicographic,
                   schedule_hint, solve_min_peak, solve_strategy_a, solve_strategy_b,
                   structural_peak_lower_bound, tec_lower_bound)
from model.front import BreakEven, Front, FrontPoint
from oracle import enumerate_schedules, random_instance, score

N_INSTANCES = 120
CFG = SolverConfig(num_workers=1, deterministic_time_limit=None, time_limit_s=60)


def _all_scores(inst):
    return [score(inst, s, 0) for s in enumerate_schedules(inst)]


def _oracle_front(scores):
    best_cmax = {}
    for sc in scores:
        k = (sc["pmax"], sc["ec"])
        best_cmax[k] = min(best_cmax.get(k, 10 ** 18), sc["cmax"])
    nd = [k for k in best_cmax if not any(o[0] <= k[0] and o[1] <= k[1] and o != k for o in best_cmax)]
    return sorted(((pk, ec, best_cmax[(pk, ec)]) for pk, ec in nd), key=lambda t: -t[0])


def _oracle_c(scores, rho):
    return min((sc["ec"] + 60 * rho * sc["pmax"], sc["cmax"]) for sc in scores)


def _oracle_break_even(scores, ref_ec, ref_peak):
    vals = [Fraction(max(0, sc["ec"] - ref_ec), 6000 * (ref_peak - sc["pmax"])) for sc in scores if sc["pmax"] < ref_peak]
    return min(vals) if vals else None


# ------------------------------------------------------------------------------------------------ oracle agreement
@pytest.mark.parametrize("seed", range(N_INSTANCES))
def test_front_matches_exhaustive_oracle(seed):
    inst = random_instance(seed)
    scores = _all_scores(inst)
    f = ec_peak_front(inst, CFG)
    if not scores:
        assert f.termination == "instance_infeasible" and f.points == [] and f.complete
        return
    assert f.complete, f.reason
    assert [(p.peak_w, p.ec_int, p.makespan) for p in f.points] == _oracle_front(scores)
    assert all(p.ec_proven for p in f.points) and f.dominated == []
    for p in f.points:
        assert check_schedule(inst, p.schedule) == []
    for rho in (0, 1, (seed * 137) % 4000, 5000, 20000):
        c = best_for_rho(f, rho)
        o_tec, o_mk = _oracle_c(scores, rho)
        assert c.ec_int + 60 * rho * c.peak_w == o_tec, f"seed {seed} rho {rho}: TEC"
        if rho > 0:
            assert c.makespan == o_mk, f"seed {seed} rho {rho}: makespan"
        else:   # documented rho = 0 case: front tie-break is restricted to min-peak energy optima
            assert c.makespan >= o_mk
            b_sched = solve_strategy_b(inst, CFG).schedule
            rec0 = recommend(inst, 0, f, {"B": b_sched})
            assert (rec0.metrics.tec_int, rec0.metrics.makespan) == (o_tec, o_mk)
        lb = tec_lower_bound(f, rho)
        assert lb == _oracle_c(scores, rho)[0]
        rec = recommend(inst, rho, f)
        assert rec.proven_optimal and rec.gap == 0 and rec.metrics.tec_int == lb
    b = solve_strategy_b(inst, CFG).metrics
    be = break_even(f, b.ec_int, b.peak_w)
    expect = _oracle_break_even(scores, b.ec_int, b.peak_w)
    if expect is None:
        assert be.kind == "no_peak_reduction" and be.rho_inr is None
    else:
        assert be.kind == "exact" and be.rho_inr == expect, f"seed {seed}: {be} vs {expect}"


def test_front_is_deterministic():
    inst = random_instance(7)
    a, b = ec_peak_front(inst, CFG), ec_peak_front(inst, CFG)
    assert [(p.peak_w, p.ec_int, p.makespan, p.schedule) for p in a.points] == \
           [(p.peak_w, p.ec_int, p.makespan, p.schedule) for p in b.points]


# ------------------------------------------------------------------------------------------------ benchmark
def test_benchmark_front_and_exact_break_even():
    inst = benchmark_instance()
    f = ec_peak_front(inst)
    assert f.complete and f.termination == "P_bound"
    assert [(p.peak_w, p.ec_int) for p in f.points] == [(37000, 785_60 * 60000), (27000, 912_60 * 60000)]
    b = solve_strategy_b(inst).metrics
    be = break_even(f, b.ec_int, b.peak_w, "B")
    assert be == BreakEven(Fraction(127, 10), "exact", "B", 27000) and be.is_exact
    assert rho_intervals(f) == [(Fraction(0), Fraction(127, 10)), (Fraction(127, 10), None)]
    assert best_for_rho(f, 1270).peak_w == 37000 and best_for_rho(f, 1271).peak_w == 27000


def test_reused_p_result_gives_same_front_and_is_not_counted():
    inst = benchmark_instance()
    p = solve_min_peak(inst)
    f1, f2 = ec_peak_front(inst), ec_peak_front(inst, p_result=p)
    assert [(q.peak_w, q.ec_int) for q in f1.points] == [(q.peak_w, q.ec_int) for q in f2.points]
    assert f2.n_solves == f1.n_solves - 1 and any(s.reused for s in f2.solves)


# ------------------------------------------------------------------------------------------------ exactness labels
def _degrade_caps(monkeypatch, *, drop_schedule=False):
    """Make every capped solve look unproven (FEASIBLE), or UNKNOWN without a schedule."""
    real = front_mod.run_lexicographic

    def fake(inst, strategy, stages, rho_paise=0, config=None, **kw):
        r = real(inst, strategy, stages, rho_paise, config, **kw)
        if not kw.get("extra_bounds"):
            return r
        if drop_schedule:
            return dataclasses.replace(r, status=SolveStatus.UNKNOWN, schedule=None, metrics=None,
                                       stage_statuses=["UNKNOWN"], stage_values=[], stage_bounds=[None])
        return dataclasses.replace(r, status=SolveStatus.FEASIBLE, proven_optimal=False,
                                   stage_statuses=["FEASIBLE"], stage_values=r.stage_values[:1],
                                   stage_bounds=[r.stage_bounds[0] - 1000.0])
    monkeypatch.setattr(front_mod, "run_lexicographic", fake)


def test_unproven_cap_solve_gives_upper_bound_not_exact(monkeypatch):
    _degrade_caps(monkeypatch)
    inst = benchmark_instance()
    f = ec_peak_front(inst)
    assert not f.complete and [p.peak_w for p in f.points] == [37000, 27000]
    assert not f.points[1].ec_proven
    b = solve_strategy_b(inst).metrics
    be = break_even(f, b.ec_int, b.peak_w)
    assert be.kind == "upper_bound" and be.rho_inr == Fraction(127, 10) and not be.is_exact
    rec = recommend(inst, 2000, f)
    assert not rec.proven_optimal and rec.gap is not None and rec.gap > 0      # weakened bound => positive gap
    assert rec.metrics.tec_int >= rec.tec_lower_bound


def test_capped_solve_without_schedule_is_undetermined(monkeypatch):
    _degrade_caps(monkeypatch, drop_schedule=True)
    inst = benchmark_instance()
    f = ec_peak_front(inst)
    assert f.termination == "unproven" and not f.complete and [p.peak_w for p in f.points] == [37000]
    b = solve_strategy_b(inst).metrics
    assert break_even(f, b.ec_int, b.peak_w).kind == "undetermined"
    lb = tec_lower_bound(f, 2000)                    # falls back to the top EC bound with the P peak bound
    assert lb is not None and lb <= recommend(inst, 2000, f).metrics.tec_int


def _pt(peak, ec, mk=5):
    return FrontPoint(peak, ec, mk, (), None, True, True, True, "cap", None)


def test_filter_dominated_drops_points_beaten_by_lower_peak():
    keep, drop = filter_dominated([_pt(50, 10), _pt(40, 10), _pt(30, 20), _pt(20, 25)])
    assert [(p.peak_w, p.ec_int) for p in keep] == [(40, 10), (30, 20), (20, 25)]
    assert [(p.peak_w, p.ec_int) for p in drop] == [(50, 10)]


def test_break_even_kinds_and_unsupported_points():
    f = Front([_pt(47000, 1000), _pt(32000, 1000 + 6000 * 15000 * 5), _pt(25000, 1000 + 6000 * 22000 * 20)],
              [], [], True, "P_bound", "", 0.0)
    be = break_even(f, 1000, 47000)
    assert be.kind == "exact" and be.rho_inr == 5 and be.via_peak_w == 32000
    assert break_even(f, 1000, 60000).rho_inr == 0                  # reference has a higher peak at the same EC
    assert break_even(f, 1000, 25000).kind == "no_peak_reduction"
    f.complete = False
    assert break_even(f, 1000, 47000).kind == "upper_bound"
    assert break_even(f, 1000, 25000).kind == "undetermined"
    # slopes: first->second 5 INR/kW, first->third 4 INR/kW, second->third 13/7 INR/kW => the middle point is
    # nondominated but NOT on the lower convex hull: optimal for no rho (unsupported)
    iv = rho_intervals(Front([_pt(47000, 0), _pt(32000, 6000 * 15000 * 5), _pt(25000, 6000 * 22000 * 4)],
                             [], [], True, "", "", 0.0))
    assert iv[0] == (0, 4) and iv[1] is None and iv[2] == (4, None)


def test_tec_lower_bound_requires_valid_regions():
    f = Front([_pt(10, 5)], [], [], True, "P_bound", "", 0.0, regions=[(5, 10), (8, 6)], lb_valid=True)
    assert tec_lower_bound(f, 0) == 5 and tec_lower_bound(f, 1) == min(5 + 600, 8 + 360)
    f.lb_valid = False
    assert tec_lower_bound(f, 1) is None


# ------------------------------------------------------------------------------------------------ safety guard
def test_guard_never_returns_worse_than_any_candidate():
    inst = benchmark_instance()
    a = solve_strategy_a(inst).schedule                 # makespan-optimal: expensive in energy
    b = solve_strategy_b(inst).schedule
    bad_front = Front([FrontPoint(37000, 0, 4, tuple(a), None, False, False, False, "cap", None)],
                      [], [], False, "unproven", "", 0.0)
    broken = [Operation(a[0].job_id, a[0].machine_id, a[0].start, a[0].end)]       # misses jobs => infeasible
    rec = recommend(inst, 500, bad_front, {"B": b, "broken": broken, "none": None})
    assert rec.choice == "B" and rec.metrics.tec_int == min(rec.candidate_tec.values())
    assert set(rec.rejected) == {"broken", "none"} and not rec.proven_optimal and rec.tec_lower_bound is None


# ------------------------------------------------------------------------------------------------ solver extensions
def test_extra_bounds_hint_and_stage_bounds():
    inst = benchmark_instance()
    st = [Stage("ec", "min"), Stage("pmax", "min"), Stage("cmax", "min")]
    r_inf = run_lexicographic(inst, "x", st, extra_bounds=[("pmax", "min", 26999)])
    assert r_inf.status == SolveStatus.INFEASIBLE and r_inf.stage_bounds == [None]
    p = solve_min_peak(inst)
    r1 = run_lexicographic(inst, "x", st, extra_bounds=[("pmax", "min", 30000)])
    r2 = run_lexicographic(inst, "x", st, extra_bounds=[("pmax", "min", 30000)], initial_hint=schedule_hint(p.schedule))
    assert r1.stage_values == r2.stage_values and r1.metrics.peak_w <= 30000
    assert len(r1.stage_bounds) == 3 and r1.stage_bounds[0] == r1.stage_values[0]
    assert r1.extra_bounds == [("pmax", "min", 30000)]
    with pytest.raises(ValueError):
        run_lexicographic(inst, "x", st, extra_bounds=[("pmax", "le", 1)])


# ------------------------------------------------------------------------------------------------ structural bound
@pytest.mark.parametrize("seed", range(N_INSTANCES))
def test_structural_peak_bound_never_exceeds_true_minimum_peak(seed):
    inst = random_instance(seed)
    peaks = [sc["pmax"] for sc in _all_scores(inst)]
    if peaks:
        assert structural_peak_lower_bound(inst) <= min(peaks)


def test_structural_bound_certifies_workload_theorem_on_cal2_instances():
    from experiments.design import DESIGN_CAL2, enumerate_tasks
    from experiments.generator import generate_instance
    for t in enumerate_tasks(DESIGN_CAL2):
        inst, meta = generate_instance(DESIGN_CAL2, t)
        max_peak = inst.base_w + sum(meta.machine_power_w)
        if meta.w_real > 2 / 3:
            assert structural_peak_lower_bound(inst) == max_peak, t.instance_id
        else:
            assert structural_peak_lower_bound(inst) < max_peak, t.instance_id


def test_front_terminates_by_structural_bound_without_p_solve():
    from experiments.design import DESIGN_CAL2, enumerate_tasks
    from experiments.generator import generate_instance
    from experiments.runner import _solver_config
    task = next(t for t in enumerate_tasks(DESIGN_CAL2) if t.instance_id == "g1w4c2s001")   # W = 0.70, CV = 0.75
    inst, _ = generate_instance(DESIGN_CAL2, task)
    f = ec_peak_front(inst, _solver_config(DESIGN_CAL2))
    assert f.complete and f.termination == "structural_bound" and len(f.points) == 1
    assert [s.label for s in f.solves] == ["top"]
    assert break_even(f, f.points[0].ec_int, f.points[0].peak_w).kind == "no_peak_reduction"
