"""Dispatch baselines: FCFS and SPT (SPEC-002 section 4) and the energy-aware rules (ROADMAP-FINAL P2).

FCFS / SPT: non-delay list scheduling on unrelated parallel machines, no gap filling: jobs are taken in priority
order and each is placed on the eligible machine where it would *complete earliest* (ties: lower machine
id). Both rules are blind to tariff and power. They return ``None`` when a job would finish after its
deadline (the heuristic fails; this does not prove the instance infeasible).
"""
from __future__ import annotations

from typing import Callable, List, Optional

from model import Instance, Job, Operation


def _dispatch(inst: Instance, order: List[Job]) -> Optional[List[Operation]]:
    free = {m: 1 for m in inst.machines}            # first free slot on each machine (1-based)
    ops: List[Operation] = []
    for job in order:
        best = None
        for m in sorted(job.proc):
            start = max(free[m], job.release)
            end = start + job.proc[m] - 1
            if best is None or end < best[0]:
                best = (end, m, start)
        end, m, start = best
        if end > inst.job_deadline(job):
            return None
        free[m] = end + 1
        ops.append(Operation(job.job_id, m, start, end))
    ops.sort(key=lambda o: (o.machine_id, o.start, o.job_id))
    return ops


def fcfs_schedule(inst: Instance) -> Optional[List[Operation]]:
    """First-come-first-served: by release time, then input order."""
    order = sorted(enumerate(inst.jobs), key=lambda iv: (iv[1].release, iv[0]))
    return _dispatch(inst, [j for _, j in order])


def spt_schedule(inst: Instance) -> Optional[List[Operation]]:
    """Shortest processing time first: by min_m p_jm, then input order."""
    order = sorted(enumerate(inst.jobs), key=lambda iv: (min(iv[1].proc.values()), iv[1].release, iv[0]))
    return _dispatch(inst, [j for _, j in order])


# ============================================================================ energy-aware rules (ROADMAP-FINAL P2)
# Honest "simple alternatives" a planner could apply without an optimiser. Both use the evaluator's exact energy
# accounting (sum over slots of price x slot length x power). They are deterministic and never claim that an
# instance is infeasible: ``None`` only means the rule failed to place every job.

def _job_order_by_energy(inst: Instance) -> List[Job]:
    """Largest minimum job energy first (min_m p_jm * power_jm); ties: release, input order."""
    keyed = sorted(enumerate(inst.jobs),
                   key=lambda iv: (-min(iv[1].proc[m] * iv[1].power_w[m] for m in iv[1].proc), iv[1].release, iv[0]))
    return [j for _, j in keyed]


def energy_greedy_schedule(inst: Instance, cap_w: Optional[int] = None) -> Optional[List[Operation]]:
    """Energy-greedy rule: jobs in decreasing minimum energy; each job goes to the feasible (machine, start) with the
    lowest energy cost FOR THAT JOB (ties: earlier start, then lower machine id). Idle gaps are allowed.

    Feasible = eligible machine idle over the whole window, release <= start, end <= the job's deadline, and, if
    ``cap_w`` is given, base load + running power <= cap_w in every slot of the window (peak-capped variant).
    """
    T = inst.T
    prefix = [0] * (T + 1)                                   # prefix[t] = sum of tariff over slots 1..t
    for t in range(1, T + 1):
        prefix[t] = prefix[t - 1] + inst.tariff_paise[t - 1]
    busy = {m: [False] * (T + 2) for m in inst.machines}
    load = [inst.base_w] * (T + 2)
    if cap_w is not None and inst.base_w > cap_w:
        return None
    ops: List[Operation] = []
    for job in _job_order_by_energy(inst):
        best = None
        last_end = inst.job_deadline(job)
        for m in sorted(job.proc):
            p, pw = job.proc[m], job.power_w[m]
            for s in range(job.release, last_end - p + 2):
                e = s + p - 1
                if any(busy[m][t] for t in range(s, e + 1)):
                    continue
                if cap_w is not None and any(load[t] + pw > cap_w for t in range(s, e + 1)):
                    continue
                cost = (prefix[e] - prefix[s - 1]) * inst.delta_t_min * pw
                key = (cost, s, m)
                if best is None or key < best[0]:
                    best = (key, m, s, e, pw)
        if best is None:
            return None
        _, m, s, e, pw = best
        for t in range(s, e + 1):
            busy[m][t] = True
            load[t] += pw
        ops.append(Operation(job.job_id, m, s, e))
    ops.sort(key=lambda o: (o.machine_id, o.start, o.job_id))
    return ops


def cap_levels(inst: Instance) -> List[int]:
    """Candidate power caps for the peak-capped rule: base load + the sum of the maximum job power of every non-empty
    subset of machines ("never run more than these machines together"), distinct, in decreasing order."""
    mx = []
    for m in inst.machines:
        powers = [j.power_w[m] for j in inst.jobs if m in j.proc]
        if powers:
            mx.append(max(powers))
    sums = {0}
    for v in mx:
        sums |= {s + v for s in sums}
    return sorted((inst.base_w + s for s in sums if s > 0), reverse=True)


def peak_capped_candidates(inst: Instance) -> List[tuple]:
    """(cap_w or None, schedule) for the uncapped energy-greedy rule and every cap level where the rule succeeds.
    Identical schedules are kept once (first, i.e. loosest, cap)."""
    out, seen = [], set()
    for cap in [None] + cap_levels(inst):
        sched = energy_greedy_schedule(inst, cap)
        if sched is None:
            continue
        key = tuple(sched)
        if key in seen:
            continue
        seen.add(key)
        out.append((cap, sched))
    return out


def peak_capped_greedy_schedule(inst: Instance, rho_paise: int) -> Optional[List[Operation]]:
    """Peak-capped greedy: run the energy-greedy rule under every cap level and keep the schedule with the lowest
    TEC at ``rho_paise`` (ties: lower makespan, then looser cap). Includes the uncapped rule, so its TEC is never above
    the energy-greedy rule's."""
    from model import evaluate_schedule
    best = None
    for order, (cap, sched) in enumerate(peak_capped_candidates(inst)):
        m = evaluate_schedule(inst, sched, rho_paise, strict=True)
        key = (m.tec_int, m.makespan, order)
        if best is None or key < best[0]:
            best = (key, sched)
    return None if best is None else best[1]
