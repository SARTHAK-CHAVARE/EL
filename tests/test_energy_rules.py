"""Energy-aware baseline rules (experiments/baselines.py, ROADMAP-FINAL P2): hand-checked benchmark, exhaustive-oracle
properties on 120 seeded instances, determinism, cap semantics."""
import pytest

from benchmark_instance import benchmark_instance
from experiments.baselines import (cap_levels, energy_greedy_schedule, peak_capped_candidates,
                                   peak_capped_greedy_schedule)
from model import check_schedule, evaluate_schedule
from oracle import enumerate_schedules, random_instance, score

N_INSTANCES = 120


def test_benchmark_by_hand():
    """Hand calculation (tariff 5.60,5.60,7.60,7.60,7.60,6.60,6.60,6.60 INR/kWh; 1 h slots; M1 10 kW, M2 25 kW):
    order J2, J4 (30 kWh), J1, J3 (20 kWh). J2 -> M1 1-3 (INR 188), J4 -> M1 6-8 (198), J1 -> M1 4-5 (152),
    J3 -> M2 slot 1 (140). Jobs 678 + base 107.60 = INR 785.60 (= the energy optimum), peak 2+10+25 = 37 kW."""
    inst = benchmark_instance()
    s = energy_greedy_schedule(inst)
    assert [(o.job_id, o.machine_id, o.start, o.end) for o in s] == \
        [("J2", 1, 1, 3), ("J1", 1, 4, 5), ("J4", 1, 6, 8), ("J3", 2, 1, 1)]
    m = evaluate_schedule(inst, s, 0)
    assert m.ec_int == 78560 * 60000 and m.peak_w == 37000
    # caps: 2+10+25, 2+25, 2+10 kW. Under 27 kW, J3 (25 kW) cannot run beside M1, which is full: the rule fails.
    assert cap_levels(inst) == [37000, 27000, 12000]
    assert energy_greedy_schedule(inst, 27000) is None and energy_greedy_schedule(inst, 12000) is None
    assert [c for c, _ in peak_capped_candidates(inst)] == [None]
    # so at the benchmark rho (INR 15/kW) the rule's TEC is B's INR 1340.60, above the optimum's INR 1317.60
    assert evaluate_schedule(inst, peak_capped_greedy_schedule(inst, 1500), 1500).tec_int == 134060 * 60000


@pytest.mark.parametrize("seed", range(N_INSTANCES))
def test_rules_are_feasible_respect_caps_and_never_beat_the_oracle(seed):
    inst = random_instance(seed)
    scores = [score(inst, s, 0) for s in enumerate_schedules(inst)]
    eg = energy_greedy_schedule(inst)
    if not scores:
        assert eg is None and peak_capped_candidates(inst) == []
        return
    if eg is not None:
        assert check_schedule(inst, eg) == []
        assert evaluate_schedule(inst, eg, 0).ec_int >= min(sc["ec"] for sc in scores)
    for cap, sched in peak_capped_candidates(inst):
        assert check_schedule(inst, sched) == []
        if cap is not None:
            assert evaluate_schedule(inst, sched, 0).peak_w <= cap
    for rho in (0, 500, 5000):
        pc = peak_capped_greedy_schedule(inst, rho)
        if pc is None:
            assert eg is None or peak_capped_candidates(inst) == []
            continue
        tec_pc = evaluate_schedule(inst, pc, rho).tec_int
        assert tec_pc >= min(sc["ec"] + 60 * rho * sc["pmax"] for sc in scores)      # optimum is a lower bound
        if eg is not None:
            assert tec_pc <= evaluate_schedule(inst, eg, rho).tec_int                # includes the uncapped rule


def test_rules_are_deterministic_and_cap_below_base_fails():
    inst = random_instance(11)
    assert energy_greedy_schedule(inst) == energy_greedy_schedule(inst)
    assert peak_capped_candidates(inst) == peak_capped_candidates(inst)
    assert energy_greedy_schedule(inst, inst.base_w - 1) is None
