"""FCFS and SPT dispatch baselines (SPEC-002 section 4).

Non-delay list scheduling on unrelated parallel machines, no gap filling: jobs are taken in priority
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
