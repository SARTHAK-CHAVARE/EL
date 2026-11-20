"""Canonical 4-job / 2-machine benchmark (hand_calculations.md section 2, verify_benchmark.py).

The numbers here are *test data* describing the documented benchmark; the solver itself contains
no benchmark values.
"""
from model import make_instance, inr_to_paise

RHO_BENCH_INR = 15
RHO_BENCH_PAISE = inr_to_paise(RHO_BENCH_INR)

TARIFF = [5.60, 5.60, 7.60, 7.60, 7.60, 6.60, 6.60, 6.60]  # illustrative block sequence (ISS-08)


def benchmark_instance():
    p = {"J1": {1: 2, 2: 2}, "J2": {1: 3, 2: 2}, "J3": {1: 2, 2: 1}, "J4": {1: 3, 2: 2}}
    power = {1: "10", 2: "25"}
    return make_instance(
        machines=[1, 2],
        jobs=[(jid, proc, power) for jid, proc in p.items()],
        T=8, D=8, delta_t_min=60, base_kw="2",
        tariff_inr_per_kwh=[str(c) for c in TARIFF],
        name="canonical-benchmark",
    )

# Expected values from verify_benchmark.py / hand_calculations.md (INR, kW)
EXPECTED = {
    "A": dict(makespan=4, sum_c=12, ec="1031.60", peak_kw=37, tec="1586.60"),
    "B": dict(makespan=8, ec="785.60", peak_kw=37, tec="1340.60"),
    "C": dict(ec="912.60", peak_kw=27, tec="1317.60"),
}
RHO_STAR_PAIR_INR = "12.70"
