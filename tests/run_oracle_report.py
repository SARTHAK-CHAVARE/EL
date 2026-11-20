"""Run the CP-SAT vs oracle comparison and print/write a JSON agreement report.

    python tests/run_oracle_report.py [N] [out.json]
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "07_src"))
sys.path.insert(0, str(ROOT / "tests"))

from model import (SolveStatus, SolverConfig, check_schedule, solve_min_peak, solve_strategy_a,  # noqa: E402
                   solve_strategy_b, solve_strategy_c)
from oracle import enumerate_schedules, lex_optimum, random_instance, score  # noqa: E402

CFG = SolverConfig(num_workers=1, deterministic_time_limit=None, time_limit_s=60)


def main(n=120, out=None):
    rows, total, agree, infeasible, discrepancies = 0, 0, 0, 0, []
    n_sched = []
    for seed in range(n):
        inst = random_instance(seed)
        rho = (seed * 137) % 4000
        n_sched.append(sum(1 for _ in enumerate_schedules(inst)))
        checks = [
            ("A", lambda: solve_strategy_a(inst, CFG), (("cmax", "min"), ("sum_c", "min")), 0),
            ("B", lambda: solve_strategy_b(inst, CFG), (("ec", "min"), ("cmax", "min")), 0),
            ("B_minpeak", lambda: solve_strategy_b(inst, CFG, "min_peak"),
             (("ec", "min"), ("cmax", "min"), ("pmax", "min")), 0),
            ("B_maxpeak", lambda: solve_strategy_b(inst, CFG, "max_peak"),
             (("ec", "min"), ("cmax", "min"), ("pmax", "max")), 0),
            ("C", lambda: solve_strategy_c(inst, rho, CFG), (("tec", "min"), ("cmax", "min")), rho),
            ("P", lambda: solve_min_peak(inst, CFG), (("pmax", "min"), ("ec", "min"), ("cmax", "min")), 0),
        ]
        for name, run, keys, r in checks:
            total += 1
            opt = lex_optimum(inst, keys, r)
            res = run()
            if opt is None:
                infeasible += 1
                ok = res.status == SolveStatus.INFEASIBLE
            else:
                ok = False
                if res.status == SolveStatus.OPTIMAL and check_schedule(inst, res.schedule) == []:
                    sc = score(inst, tuple((o.job_id, o.machine_id, o.start) for o in res.schedule), r)
                    ok = tuple(sc[k] for k, _ in keys) == opt
            if ok:
                agree += 1
            else:
                discrepancies.append(dict(seed=seed, strategy=name, status=res.status.value))
    report = dict(instances=n, comparisons=total, agree=agree, agreement_pct=100.0 * agree / total,
                  infeasible_comparisons=infeasible, discrepancies=discrepancies,
                  schedules_per_instance=dict(min=min(n_sched), max=max(n_sched),
                                              mean=sum(n_sched) / len(n_sched)))
    print(json.dumps(report, indent=2))
    if out:
        Path(out).write_text(json.dumps(report, indent=2))
    return 0 if not discrepancies else 1


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    sys.exit(main(n, sys.argv[2] if len(sys.argv) > 2 else None))
