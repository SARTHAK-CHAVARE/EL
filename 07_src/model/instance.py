"""Data models for the scheduling problem (SPEC-001 sections 1-2).

Everything numeric inside an :class:`Instance` is an ``int`` (watts, paise/kWh, minutes, 1-based
slots). Use :func:`make_instance` to build one from kW / rupee inputs with exact conversion.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Mapping, NamedTuple, Optional, Sequence, Tuple

from .tariff import Number, inr_to_paise, kw_to_w


class Operation(NamedTuple):
    """One scheduled operation. Slots are 1-based and inclusive: end = start + p - 1."""
    job_id: str
    machine_id: int
    start: int
    end: int


@dataclass(frozen=True)
class Job:
    """A job with machine-dependent processing time (slots) and power (watts).

    ``proc`` keys define the eligible machine set M_j; ``power_w`` must have the same keys.
    ``due=None`` means the global deadline D.
    """
    job_id: str
    proc: Mapping[int, int]
    power_w: Mapping[int, int]
    release: int = 1
    due: Optional[int] = None


@dataclass(frozen=True)
class Instance:
    machines: Tuple[int, ...]
    jobs: Tuple[Job, ...]
    T: int                       # number of slots in the horizon
    D: int                       # global deadline slot (D <= T)
    delta_t_min: int             # slot length in minutes
    base_w: int                  # constant facility load, W
    tariff_paise: Tuple[int, ...]  # C~_t, paise/kWh, length T (index 0 = slot 1)
    name: str = ""

    def job_deadline(self, job: Job) -> int:
        """Effective last slot for ``job``: min(D, due)."""
        return self.D if job.due is None else min(self.D, job.due)

    def tariff_at(self, t: int) -> int:
        """Tariff (paise/kWh) for 1-based slot t."""
        return self.tariff_paise[t - 1]


def make_instance(
    *,
    machines: Iterable[int],
    jobs: Iterable[Tuple[str, Mapping[int, int], Mapping[int, Number]]],
    T: int,
    delta_t_min: int,
    base_kw: Number,
    tariff_inr_per_kwh: Sequence[Number],
    D: Optional[int] = None,
    releases: Optional[Mapping[str, int]] = None,
    dues: Optional[Mapping[str, int]] = None,
    name: str = "",
) -> Instance:
    """Build an :class:`Instance` from engineering units with exact conversion.

    ``jobs`` items are ``(job_id, {machine: p_slots}, {machine: power_kW})``.
    """
    releases = releases or {}
    dues = dues or {}
    job_objs = []
    for job_id, proc, power_kw in jobs:
        job_objs.append(Job(
            job_id=job_id,
            proc=dict(proc),
            power_w={m: kw_to_w(p) for m, p in power_kw.items()},
            release=releases.get(job_id, 1),
            due=dues.get(job_id),
        ))
    return Instance(
        machines=tuple(machines),
        jobs=tuple(job_objs),
        T=T,
        D=T if D is None else D,
        delta_t_min=delta_t_min,
        base_w=kw_to_w(base_kw),
        tariff_paise=tuple(inr_to_paise(c) for c in tariff_inr_per_kwh),
        name=name,
    )


def machine_ids(instance: Instance) -> Dict[int, int]:
    """Map machine id -> position (helper for callers that need dense indices)."""
    return {m: i for i, m in enumerate(instance.machines)}
