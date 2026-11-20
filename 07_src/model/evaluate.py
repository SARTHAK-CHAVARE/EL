"""Independent schedule checker and metric evaluator (SPEC-001 section 7).

This module deliberately imports nothing from the CP-SAT formulation or the solver: it recomputes
every reported metric from a plain list of :class:`Operation` using integer arithmetic, so a bug in
the model cannot silently contaminate the results.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, List, Sequence, Tuple

from .instance import Instance, Operation
from .tariff import MINUTES_PER_HOUR, scaled_to_inr


class ScheduleError(ValueError):
    """The schedule violates the constraints of the problem."""

    def __init__(self, violations):
        self.violations = list(violations)
        super().__init__("infeasible schedule:\n  - " + "\n  - ".join(self.violations))


@dataclass(frozen=True)
class Metrics:
    makespan: int                       # C_max (slot)
    sum_completion: int                 # sum_j C_j
    completion: Dict[str, int]          # C_j per job
    power_profile_w: Tuple[int, ...]    # P_t, t = 1..T
    peak_w: int                         # P_max (L = 1)
    energy_w_min: int                   # sum_t P_t * dt_min   (W*min)
    ec_int: int                         # energy cost, units of 1/6e6 INR
    dc_int: int                         # demand charge, same units
    tec_int: int                        # EC_int + DC_int
    rho_paise: int

    # exact rupee views ---------------------------------------------------------------
    @property
    def ec_inr(self) -> Fraction:
        return scaled_to_inr(self.ec_int)

    @property
    def dc_inr(self) -> Fraction:
        return scaled_to_inr(self.dc_int)

    @property
    def tec_inr(self) -> Fraction:
        return scaled_to_inr(self.tec_int)

    @property
    def energy_kwh(self) -> Fraction:
        return Fraction(self.energy_w_min, 1000 * MINUTES_PER_HOUR)

    @property
    def peak_kw(self) -> Fraction:
        return Fraction(self.peak_w, 1000)


def check_schedule(inst: Instance, schedule: Sequence[Operation]) -> List[str]:
    """Return a list of violated constraints (empty list = feasible). 1-based slots."""
    v: List[str] = []
    jobs = {j.job_id: j for j in inst.jobs}
    seen: Dict[str, int] = {}
    occupancy: Dict[Tuple[int, int], str] = {}
    for op in schedule:
        seen[op.job_id] = seen.get(op.job_id, 0) + 1
        job = jobs.get(op.job_id)
        if job is None:
            v.append(f"unknown job {op.job_id}")
            continue
        if op.machine_id not in job.proc:
            v.append(f"{op.job_id} assigned to ineligible machine {op.machine_id}")
            continue
        p = job.proc[op.machine_id]
        if op.end - op.start + 1 != p:
            v.append(f"{op.job_id}: duration {op.end - op.start + 1} != p={p} on machine {op.machine_id}")
        if op.start < job.release:
            v.append(f"{op.job_id}: starts at {op.start} before release {job.release}")
        last_allowed = inst.job_deadline(job)
        if op.end > last_allowed:
            v.append(f"{op.job_id}: ends at {op.end} after deadline/due {last_allowed}")
        if op.start < 1 or op.end > inst.T:
            v.append(f"{op.job_id}: outside horizon [1,{inst.T}]")
        for t in range(op.start, op.end + 1):
            other = occupancy.get((op.machine_id, t))
            if other is not None and other != op.job_id:
                v.append(f"machine {op.machine_id} overlap at slot {t}: {other} and {op.job_id}")
            occupancy[(op.machine_id, t)] = op.job_id
    for jid in jobs:
        if seen.get(jid, 0) != 1:
            v.append(f"job {jid} scheduled {seen.get(jid, 0)} times (expected exactly 1)")
    return v


def evaluate_schedule(inst: Instance, schedule: Sequence[Operation], rho_paise: int = 0,
                      strict: bool = True) -> Metrics:
    """Recompute all metrics from ``schedule``.

    With ``strict=True`` (default) a constraint violation raises :class:`ScheduleError`.
    """
    if strict:
        viol = check_schedule(inst, schedule)
        if viol:
            raise ScheduleError(viol)
    jobs = {j.job_id: j for j in inst.jobs}
    profile = [inst.base_w] * inst.T
    completion: Dict[str, int] = {}
    for op in schedule:
        power = jobs[op.job_id].power_w[op.machine_id]
        for t in range(op.start, op.end + 1):
            profile[t - 1] += power
        completion[op.job_id] = op.end
    peak = max(profile)
    energy_w_min = sum(profile) * inst.delta_t_min
    ec_int = sum(inst.tariff_paise[t] * inst.delta_t_min * profile[t] for t in range(inst.T))
    dc_int = MINUTES_PER_HOUR * rho_paise * peak
    return Metrics(
        makespan=max(completion.values()),
        sum_completion=sum(completion.values()),
        completion=completion,
        power_profile_w=tuple(profile),
        peak_w=peak,
        energy_w_min=energy_w_min,
        ec_int=ec_int,
        dc_int=dc_int,
        tec_int=ec_int + dc_int,
        rho_paise=rho_paise,
    )


def rho_star_pair(m_low_energy: Metrics, m_low_peak: Metrics):
    """Break-even rho (INR/kW) between two *fixed* schedules (SPEC-001 D8).

    rho* = (EC_peak_aware - EC_energy_only) / (Pmax_energy_only - Pmax_peak_aware).
    Returns an exact :class:`Fraction`, or ``None`` if the second schedule has no lower peak
    (then no positive rho makes it preferable). NOTE: this is only an *upper bound* on the true
    switching rho when intermediate efficient schedules exist.
    """
    d_ec = m_low_peak.ec_int - m_low_energy.ec_int
    d_p = m_low_energy.peak_w - m_low_peak.peak_w
    if d_p <= 0:
        return None
    if d_ec <= 0:
        return Fraction(0)
    # rho[INR/kW] = (d_ec/6e6 INR) / (d_p/1000 kW) = d_ec / (6000 * d_p)
    return Fraction(d_ec, 6000 * d_p)
