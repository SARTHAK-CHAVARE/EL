import dataclasses

import pytest

from model import (InfeasibleInstance, Instance, SolveStatus, SolverConfig, build_formulation, check_schedule,
                   combine_status, make_instance, solve_strategy_a, solve_strategy_b, solve_strategy_c)
from model.solver import InternalConsistencyError
from benchmark_instance import benchmark_instance
from oracle import random_instance

CFG = SolverConfig(num_workers=1, deterministic_time_limit=None)


def _one_machine(jobs, T, D=None, **kw):
    return make_instance(machines=[1], jobs=jobs, T=T, D=D, delta_t_min=60, base_kw=kw.pop("base_kw", 0),
                         tariff_inr_per_kwh=kw.pop("tariff", ["5"] * T), **kw)


def test_infeasible_job_too_long():
    inst = _one_machine([("J", {1: 5}, {1: "1"})], T=6, D=3)
    for fn in (solve_strategy_a, solve_strategy_b, lambda i, c: solve_strategy_c(i, 100, c)):
        r = fn(inst, CFG)
        assert r.status == SolveStatus.INFEASIBLE and not r.proven_optimal
        assert r.schedule is None and "no valid" in r.reason


def test_infeasible_capacity():
    inst = _one_machine([(f"J{k}", {1: 3}, {1: "1"}) for k in range(3)], T=6, D=6)   # 9 slots of work in 6
    r = solve_strategy_a(inst, CFG)
    assert r.status == SolveStatus.INFEASIBLE and r.schedule is None
    with pytest.raises(InfeasibleInstance):
        build_formulation(_one_machine([("J", {1: 5}, {1: "1"})], T=6, D=3))


def test_release_and_due_respected_by_solver():
    inst = _one_machine([("J1", {1: 2}, {1: "1"}), ("J2", {1: 2}, {1: "1"})], T=8,
                        releases={"J1": 3, "J2": 5}, dues={"J1": 6, "J2": 8})
    r = solve_strategy_a(inst, CFG)
    assert r.status == SolveStatus.OPTIMAL and check_schedule(inst, r.schedule) == []
    ops = {o.job_id: o for o in r.schedule}
    assert ops["J1"].start >= 3 and ops["J1"].end <= 6 and ops["J2"].start >= 5


def test_single_job_single_machine_cheapest_slots_and_base_beyond_deadline():
    # 2 slots of work, D=4 < T=6; base load 1 kW is billed over all T=6 slots
    inst = _one_machine([("J", {1: 2}, {1: "10"})], T=6, D=4, base_kw=1,
                        tariff=["9", "9", "5", "5", "7", "7"])
    r = solve_strategy_b(inst, CFG)
    assert r.status == SolveStatus.OPTIMAL
    assert (r.schedule[0].start, r.schedule[0].end) == (3, 4)
    # EC = 10kW*(5+5) + base 1kW*(9+9+5+5+7+7) = 100 + 42 = 142 INR
    assert r.metrics.ec_inr == 142


def test_zero_power_machine_and_flat_tariff_ties_are_fine():
    inst = make_instance(machines=[1, 2], jobs=[("J1", {1: 1, 2: 1}, {1: "0", 2: "5"}),
                                                ("J2", {1: 1, 2: 1}, {1: "0", 2: "5"})],
                         T=3, delta_t_min=60, base_kw=0, tariff_inr_per_kwh=["6", "6", "6"])
    r = solve_strategy_b(inst, CFG)
    assert r.status == SolveStatus.OPTIMAL and r.metrics.ec_int == 0 and r.metrics.peak_w == 0


def test_job_with_single_eligible_machine():
    inst = make_instance(machines=[1, 2], jobs=[("J1", {2: 2}, {2: "4"}), ("J2", {1: 1, 2: 1}, {1: "1", 2: "1"})],
                         T=4, delta_t_min=60, base_kw=0, tariff_inr_per_kwh=["5"] * 4)
    r = solve_strategy_a(inst, CFG)
    assert {o.job_id: o.machine_id for o in r.schedule}["J1"] == 2


def test_multiple_optima_same_metrics_across_seeds():
    inst = benchmark_instance()
    vals = set()
    scheds = set()
    for seed in range(6):
        r = solve_strategy_a(inst, SolverConfig(num_workers=1, deterministic_time_limit=None, random_seed=seed))
        vals.add((r.metrics.makespan, r.metrics.sum_completion, r.metrics.ec_int, r.metrics.peak_w))
        scheds.add(tuple((o.job_id, o.machine_id, o.start) for o in r.schedule))
    assert len(vals) == 1                      # all optima share the metrics
    assert len(scheds) >= 1                    # schedule itself may legitimately differ


def test_deterministic_under_fixed_seed():
    inst = random_instance(7)
    a = solve_strategy_c(inst, 1500, CFG)
    b = solve_strategy_c(inst, 1500, CFG)
    assert a.schedule == b.schedule and a.stage_values == b.stage_values


def test_peak_equals_actual_max_from_raw_schedule():
    for seed in range(20):
        inst = random_instance(seed)
        r = solve_strategy_c(inst, 2000, CFG)
        if r.schedule is None:
            continue
        jobs = {j.job_id: j for j in inst.jobs}
        prof = [inst.base_w] * inst.T
        for o in r.schedule:
            for t in range(o.start, o.end + 1):
                prof[t - 1] += jobs[o.job_id].power_w[o.machine_id]
        assert r.metrics.peak_w == max(prof)


def test_every_job_exactly_once_and_durations():
    inst = random_instance(3)
    r = solve_strategy_a(inst, CFG)
    if r.schedule:
        assert sorted(o.job_id for o in r.schedule) == sorted(j.job_id for j in inst.jobs)
        jobs = {j.job_id: j for j in inst.jobs}
        for o in r.schedule:
            assert o.end - o.start + 1 == jobs[o.job_id].proc[o.machine_id]
            assert r.metrics.completion[o.job_id] == o.end


def test_combine_status_never_promotes_feasible():
    S = SolveStatus
    assert combine_status([S.OPTIMAL, S.OPTIMAL], True) == S.OPTIMAL
    assert combine_status([S.OPTIMAL, S.FEASIBLE], True) == S.FEASIBLE
    assert combine_status([S.FEASIBLE, S.OPTIMAL], True) == S.FEASIBLE
    assert combine_status([S.OPTIMAL, S.UNKNOWN], True) == S.FEASIBLE
    assert combine_status([S.UNKNOWN], False) == S.UNKNOWN
    assert combine_status([S.INFEASIBLE], False) == S.INFEASIBLE
    assert combine_status([S.MODEL_INVALID], False) == S.MODEL_INVALID
    assert combine_status([], False) == S.UNKNOWN


def test_timeout_is_reported_not_faked():
    # a mid-size instance with an absurdly small deterministic budget
    from experiments_fixture import mid_instance
    inst = mid_instance()
    r = solve_strategy_c(inst, 1500, SolverConfig(num_workers=1, time_limit_s=5, deterministic_time_limit=0.0005))
    assert r.proven_optimal == (r.status == SolveStatus.OPTIMAL)
    if r.status != SolveStatus.OPTIMAL:
        assert r.status in (SolveStatus.FEASIBLE, SolveStatus.UNKNOWN)
        if r.schedule is not None:
            assert check_schedule(inst, r.schedule) == []
    if r.status == SolveStatus.UNKNOWN:
        assert r.schedule is None and r.metrics is None


def test_x_variables_only_for_valid_placements():
    inst = _one_machine([("J", {1: 3}, {1: "1"})], T=8, D=6, releases={"J": 2}, dues={"J": 5})
    f = build_formulation(inst)
    assert sorted(t for (_, _, t) in f.x) == [2, 3]      # starts 2..(5-3+1)=3


@pytest.mark.parametrize("seed", range(40))
def test_redundant_constraints_do_not_change_optima(seed):
    """Compare only the lexicographic objectives of each strategy (other metrics are free ties)."""
    from oracle import random_instance
    inst = random_instance(seed)
    on = SolverConfig(num_workers=1, deterministic_time_limit=None, redundant_constraints=True)
    off = SolverConfig(num_workers=1, deterministic_time_limit=None, redundant_constraints=False)
    keys = {"A": lambda m: (m.makespan, m.sum_completion),
            "B": lambda m: (m.ec_int, m.makespan),
            "C": lambda m: (m.tec_int, m.makespan)}
    for name, fn, args in (("A", solve_strategy_a, ()), ("B", solve_strategy_b, ()),
                           ("C", solve_strategy_c, (1500,))):
        r1, r0 = fn(inst, *args, on), fn(inst, *args, off)
        assert r1.status == r0.status
        if r1.metrics is not None:
            assert keys[name](r1.metrics) == keys[name](r0.metrics)
