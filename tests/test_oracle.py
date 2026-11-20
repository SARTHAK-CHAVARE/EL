"""Oracle validation: CP-SAT vs exhaustive enumeration on >=100 seeded random small instances."""
import pytest

from model import (SolveStatus, SolverConfig, check_schedule, solve_min_peak, solve_strategy_a,
                   solve_strategy_b, solve_strategy_c)
from oracle import lex_optimum, random_instance, score

N_INSTANCES = 120
CFG = SolverConfig(num_workers=1, deterministic_time_limit=None, time_limit_s=60)




@pytest.mark.parametrize("seed", range(N_INSTANCES))
def test_cpsat_matches_oracle(seed):
    inst = random_instance(seed)
    rho = (seed * 137) % 4000          # paise/kW, 0..40 INR/kW (includes 0)
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
        oracle_opt = lex_optimum(inst, keys, r)
        res = run()
        if oracle_opt is None:
            assert res.status == SolveStatus.INFEASIBLE, f"{name} seed {seed}: oracle infeasible, solver {res.status}"
            continue
        assert res.status == SolveStatus.OPTIMAL and res.proven_optimal, f"{name} seed {seed}: {res.status} {res.reason}"
        assert check_schedule(inst, res.schedule) == [], f"{name} seed {seed}: infeasible schedule"
        sc = score(inst, tuple((o.job_id, o.machine_id, o.start) for o in res.schedule), r)
        got = tuple(sc[k] for k, _ in keys)
        assert got == oracle_opt, f"{name} seed {seed}: solver {got} != oracle {oracle_opt}"
