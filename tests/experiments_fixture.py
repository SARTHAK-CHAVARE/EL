"""A mid-size instance (12 jobs, 3 machines, 32 slots) used to exercise limits and timing."""
import random

from model import make_instance


def mid_instance(seed: int = 1, n: int = 12, m: int = 3, T: int = 32):
    rng = random.Random(seed)
    machines = list(range(1, m + 1))
    jobs = [(f"J{k}", {mm: rng.randint(2, 8) for mm in machines},
             {mm: rng.choice([5, 10, 15, 20, 25]) for mm in machines}) for k in range(n)]
    tariff = [["5.60", "6.60", "7.60"][(t // 8) % 3] for t in range(T)]
    return make_instance(machines=machines, jobs=jobs, T=T, delta_t_min=15, base_kw=2,
                         tariff_inr_per_kwh=tariff, name="mid")
