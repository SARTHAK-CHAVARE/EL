"""Schedule extraction from CP-SAT variable values (SPEC-001 section 7)."""
from __future__ import annotations

from typing import List, Mapping, Tuple

from .instance import Instance, Operation

Triple = Tuple[str, int, int]


def extract_schedule(inst: Instance, x_values: Mapping[Triple, int]) -> List[Operation]:
    """Turn solved ``x[j,m,t]`` values into Operations sorted by (machine, start)."""
    jobs = {j.job_id: j for j in inst.jobs}
    ops = []
    for (jid, m, s), val in x_values.items():
        if val:
            p = jobs[jid].proc[m]
            ops.append(Operation(jid, m, s, s + p - 1))
    ops.sort(key=lambda o: (o.machine_id, o.start, o.job_id))
    return ops
