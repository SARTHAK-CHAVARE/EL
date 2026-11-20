"""Reproduce the benchmark metrics (INR 785.60 / 912.60 / 27 kW / rho* = INR 12.70 per kW) in one command.

    python 07_src/scripts/reproduce_benchmark.py

Solves the canonical 4-job / 2-machine / 5-slot instance with the CP-SAT engine (no hard-coded results in the
solver) and compares *metrics* with the documented values. Exit code 0 = all reproduced, 1 = mismatch.
"""
from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "07_src"))
sys.path.insert(0, str(ROOT / "tests"))

from benchmark_instance import EXPECTED, RHO_BENCH_PAISE, RHO_STAR_PAIR_INR, benchmark_instance  # noqa: E402
from model import (SolverConfig, evaluate_schedule, rho_star_pair, solve_strategy_a,  # noqa: E402
                   solve_strategy_b, solve_strategy_c)
from model.tariff import scaled_to_inr  # noqa: E402


def main() -> int:
    inst = benchmark_instance()
    cfg = SolverConfig(num_workers=1, deterministic_time_limit=None)
    res = dict(A=solve_strategy_a(inst, cfg), B=solve_strategy_b(inst, cfg),
               C=solve_strategy_c(inst, RHO_BENCH_PAISE, cfg))
    m = {k: evaluate_schedule(inst, r.schedule, RHO_BENCH_PAISE) for k, r in res.items()}
    checks = [(f"status {k}", r.status.value, "OPTIMAL") for k, r in res.items()]
    for k in "ABC":
        e = EXPECTED[k]
        checks.append((f"{k}: EC (INR)", str(scaled_to_inr(m[k].ec_int)), str(Fraction(e["ec"])).replace("/", "/")))
        checks.append((f"{k}: peak (kW)", str(Fraction(m[k].peak_w, 1000)), str(Fraction(e["peak_kw"]))))
        checks.append((f"{k}: TEC (INR)", str(scaled_to_inr(m[k].tec_int)), str(Fraction(e["tec"]))))
    checks.append(("rho*_pair B->C (INR/kW)", str(rho_star_pair(m["B"], m["C"])), str(Fraction(RHO_STAR_PAIR_INR))))
    ok = True
    for name, got, want in checks:
        good = got == want
        ok &= good
        print(f"[{'PASS' if good else 'FAIL'}] {name}: got {got}, expected {want}")
    print("BENCHMARK REPRODUCED" if ok else "BENCHMARK MISMATCH")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
