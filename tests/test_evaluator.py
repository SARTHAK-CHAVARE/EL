from fractions import Fraction

import pytest

from model import Operation, ScheduleError, check_schedule, evaluate_schedule
from benchmark_instance import RHO_BENCH_PAISE, benchmark_instance

A = [Operation("J1", 1, 1, 2), Operation("J3", 1, 3, 4), Operation("J2", 2, 1, 2), Operation("J4", 2, 3, 4)]
B = [Operation("J1", 1, 1, 2), Operation("J2", 1, 3, 5), Operation("J4", 1, 6, 8), Operation("J3", 2, 1, 1)]
C = [Operation("J1", 1, 3, 4), Operation("J2", 1, 5, 7), Operation("J4", 2, 1, 2), Operation("J3", 2, 8, 8)]


@pytest.mark.parametrize("sched,cmax,sumc,ec,peak,tec", [
    (A, 4, 12, "1031.60", 37000, "1586.60"),
    (B, 8, 16, "785.60", 37000, "1340.60"),
    (C, 8, 21, "912.60", 27000, "1317.60"),
])
def test_hand_calculated_schedules(sched, cmax, sumc, ec, peak, tec):
    m = evaluate_schedule(benchmark_instance(), sched, RHO_BENCH_PAISE)
    assert (m.makespan, m.sum_completion, m.peak_w) == (cmax, sumc, peak)
    assert m.ec_inr == Fraction(ec) and m.tec_inr == Fraction(tec)


def test_peak_equals_max_of_profile():
    m = evaluate_schedule(benchmark_instance(), C, RHO_BENCH_PAISE)
    assert m.peak_w == max(m.power_profile_w) == 27000
    assert m.power_profile_w == (27000, 27000, 12000, 12000, 12000, 12000, 12000, 27000)


@pytest.mark.parametrize("sched,needle", [
    (A[:-1], "job J4 scheduled 0 times"),
    (A + [Operation("J4", 2, 5, 6)], "scheduled 2 times"),
    ([Operation("J1", 1, 1, 3)] + A[1:], "duration 3 != p=2"),
    ([Operation("J1", 1, 1, 2), Operation("J3", 1, 2, 3), Operation("J2", 2, 1, 2), Operation("J4", 2, 3, 4)], "overlap"),
    ([Operation("J1", 3, 1, 2)] + A[1:], "ineligible machine 3"),
    ([Operation("J1", 1, 7, 8)] + [Operation("J3", 1, 3, 4), Operation("J2", 2, 7, 8), Operation("J4", 2, 3, 4)][:0]
     + A[1:], None),
])
def test_violations_detected(sched, needle):
    v = check_schedule(benchmark_instance(), sched)
    if needle is None:
        assert v == []          # J1 at 7-8 is legal (no overlap), kept as a negative control
        return
    assert any(needle in s for s in v), v
    with pytest.raises(ScheduleError):
        evaluate_schedule(benchmark_instance(), sched)


def test_release_and_deadline_violations():
    from model import make_instance
    inst = make_instance(machines=[1], jobs=[("J", {1: 2}, {1: "1"})], T=6, D=5, delta_t_min=60, base_kw=0,
                         tariff_inr_per_kwh=["5"] * 6, releases={"J": 2}, dues={"J": 4})
    assert any("before release" in s for s in check_schedule(inst, [Operation("J", 1, 1, 2)]))
    assert any("after deadline" in s for s in check_schedule(inst, [Operation("J", 1, 4, 5)]))
    assert check_schedule(inst, [Operation("J", 1, 2, 3)]) == []
