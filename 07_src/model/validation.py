"""Instance validation (SPEC-001 sections 4 and 7).

``validate_instance`` raises :class:`InstanceError` listing *all* problems found, so users can fix
an input file in one pass. A semantically infeasible instance (a job that cannot be placed
anywhere) is *not* an input error: it is reported by the solver as INFEASIBLE.
"""
from __future__ import annotations

from .instance import Instance
from .tariff import MINUTES_PER_HOUR

#: Safe upper bound on any integer objective value (CP-SAT works in int64).
OVERFLOW_LIMIT: int = 10 ** 17


class InstanceError(ValueError):
    """Malformed instance. ``problems`` holds every individual problem."""

    def __init__(self, problems):
        self.problems = list(problems)
        super().__init__("invalid instance:\n  - " + "\n  - ".join(self.problems))


def _is_int(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def tec_upper_bound(inst: Instance, rho_paise: int = 0) -> int:
    """Upper bound on TEC_int: highest tariff on every slot at max power, plus DC at max peak."""
    max_machine_w = {m: 0 for m in inst.machines}
    for j in inst.jobs:
        for m, p in j.power_w.items():
            if m in max_machine_w:
                max_machine_w[m] = max(max_machine_w[m], p)
    p_ub = inst.base_w + sum(max_machine_w.values())
    c_max = max(inst.tariff_paise) if inst.tariff_paise else 0
    ec_ub = inst.T * c_max * inst.delta_t_min * p_ub
    dc_ub = MINUTES_PER_HOUR * rho_paise * p_ub
    return ec_ub + dc_ub


def validate_instance(inst: Instance, rho_paise: int = 0) -> None:
    errs = []
    if not inst.machines:
        errs.append("no machines")
    if len(set(inst.machines)) != len(inst.machines):
        errs.append("duplicate machine ids")
    for m in inst.machines:
        if not _is_int(m):
            errs.append(f"machine id {m!r} is not an int")
    for name in ("T", "D", "delta_t_min", "base_w"):
        if not _is_int(getattr(inst, name)):
            errs.append(f"{name} must be an int (got {getattr(inst, name)!r}); floats are not allowed in the engine")
    if errs:
        raise InstanceError(errs)  # later checks assume ints
    if inst.T < 1:
        errs.append("T must be >= 1")
    if not (1 <= inst.D <= inst.T):
        errs.append(f"deadline D={inst.D} must satisfy 1 <= D <= T={inst.T}")
    if inst.delta_t_min < 1:
        errs.append("delta_t_min must be >= 1 minute")
    if inst.base_w < 0:
        errs.append("base_w must be >= 0")
    if len(inst.tariff_paise) != inst.T:
        errs.append(f"tariff has {len(inst.tariff_paise)} entries but T={inst.T}")
    for i, c in enumerate(inst.tariff_paise, start=1):
        if not _is_int(c) or c < 0:
            errs.append(f"tariff slot {i}: {c!r} must be a non-negative int (paise/kWh)")
    if not inst.jobs:
        errs.append("no jobs")
    ids = [j.job_id for j in inst.jobs]
    if len(set(ids)) != len(ids):
        errs.append("duplicate job ids")
    mset = set(inst.machines)
    for j in inst.jobs:
        tag = f"job {j.job_id}"
        if not j.proc:
            errs.append(f"{tag}: no eligible machine")
        if set(j.proc) != set(j.power_w):
            errs.append(f"{tag}: proc and power_w must define the same machines")
        for m, p in j.proc.items():
            if m not in mset:
                errs.append(f"{tag}: unknown machine {m}")
            if not _is_int(p) or p < 1:
                errs.append(f"{tag}: processing time on machine {m} must be an int >= 1 (got {p!r})")
        for m, w in j.power_w.items():
            if not _is_int(w) or w < 0:
                errs.append(f"{tag}: power on machine {m} must be an int >= 0 W (got {w!r})")
        if not _is_int(j.release) or j.release < 1:
            errs.append(f"{tag}: release must be an int >= 1 (got {j.release!r})")
        if j.due is not None and (not _is_int(j.due) or j.due < 1):
            errs.append(f"{tag}: due must be an int >= 1 (got {j.due!r})")
    if errs:
        raise InstanceError(errs)
    bound = tec_upper_bound(inst, rho_paise)
    if bound > OVERFLOW_LIMIT:
        raise InstanceError([
            f"objective upper bound {bound} exceeds the int64 safety limit {OVERFLOW_LIMIT}; "
            "reduce T, power or tariff magnitudes"
        ])
