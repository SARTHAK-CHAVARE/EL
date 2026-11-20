"""Parametrised exhaustive enumerator (oracle) for small instances.

Independent of the solver *and* of ``model.evaluate``: schedules are enumerated by plain recursion over
(machine, start) choices and scored with its own integer arithmetic. The original
``04_mathematical_model/verification/verify_benchmark.py`` is hard-wired to one instance and is left
untouched; this is the generalised counterpart used for >=100 seeded random instances.
"""
from __future__ import annotations

import random
from typing import Dict, Iterator, List, Optional, Tuple

from model import Instance, Job, make_instance

Sched = Tuple[Tuple[str, int, int], ...]  # (job_id, machine, start) triples


def enumerate_schedules(inst: Instance) -> Iterator[Sched]:
    """Yield every feasible schedule as a tuple of (job, machine, start)."""
    jobs = list(inst.jobs)
    occupied: Dict[int, int] = {m: 0 for m in inst.machines}  # bitmask per machine (bit t = slot t)

    def rec(i: int, chosen: List[Tuple[str, int, int]]):
        if i == len(jobs):
            yield tuple(chosen)
            return
        j = jobs[i]
        last = inst.D if j.due is None else min(inst.D, j.due)
        for m, p in j.proc.items():
            mask_p = (1 << p) - 1
            for s in range(j.release, last - p + 2):
                mask = mask_p << s
                if occupied[m] & mask:
                    continue
                occupied[m] |= mask
                chosen.append((j.job_id, m, s))
                yield from rec(i + 1, chosen)
                chosen.pop()
                occupied[m] &= ~mask

    yield from rec(0, [])


def score(inst: Instance, sched: Sched, rho_paise: int) -> Dict[str, int]:
    """Independent integer scoring of one schedule."""
    jobs = {j.job_id: j for j in inst.jobs}
    prof = [inst.base_w] * (inst.T + 1)  # index 1..T
    comp = []
    for jid, m, s in sched:
        p = jobs[jid].proc[m]
        w = jobs[jid].power_w[m]
        for t in range(s, s + p):
            prof[t] += w
        comp.append(s + p - 1)
    peak = max(prof[1:])
    ec = sum(inst.tariff_paise[t - 1] * inst.delta_t_min * prof[t] for t in range(1, inst.T + 1))
    return dict(cmax=max(comp), sum_c=sum(comp), pmax=peak, ec=ec, dc=60 * rho_paise * peak,
                tec=ec + 60 * rho_paise * peak)


def lex_optimum(inst: Instance, keys: Tuple[Tuple[str, str], ...], rho_paise: int = 0
                ) -> Optional[Tuple[int, ...]]:
    """Lexicographic optimum value tuple over all feasible schedules (None if infeasible).

    ``keys`` = (("ec","min"),("cmax","min"),...). A 'max' key is compared on its negation.
    """
    best = None
    for sch in enumerate_schedules(inst):
        sc = score(inst, sch, rho_paise)
        tup = tuple(sc[k] if sense == "min" else -sc[k] for k, sense in keys)
        if best is None or tup < best:
            best = tup
    if best is None:
        return None
    return tuple(v if sense == "min" else -v for v, (_, sense) in zip(best, keys))


def random_instance(seed: int) -> Instance:
    """Seeded small instance: N<=4 jobs, M<=3 machines, T<=7 slots, optional release/due, job-dependent power."""
    rng = random.Random(seed)
    n = rng.randint(2, 4)
    m = rng.randint(1, 3)
    T = rng.randint(4, 7)
    D = rng.randint(max(3, T - 1), T)
    machines = list(range(1, m + 1))
    jobs, releases, dues = [], {}, {}
    for k in range(1, n + 1):
        jid = f"J{k}"
        elig = [mm for mm in machines if rng.random() < 0.8] or [rng.choice(machines)]
        proc = {mm: rng.randint(1, 3) for mm in elig}
        power = {mm: rng.choice([1, 2, 3, 5, 8, 10, 15]) for mm in elig}
        jobs.append((jid, proc, power))
        if rng.random() < 0.25:
            releases[jid] = rng.randint(1, 3)
        if rng.random() < 0.25:
            dues[jid] = rng.randint(2, D)
    tariff = [rng.choice(["5.60", "6.60", "7.60", "4.00", "9.00"]) for _ in range(T)]
    return make_instance(machines=machines, jobs=jobs, T=T, D=D, delta_t_min=rng.choice([15, 30, 60]),
                         base_kw=rng.choice(["0", "1", "2"]), tariff_inr_per_kwh=tariff,
                         releases=releases, dues=dues, name=f"rand-{seed}")
