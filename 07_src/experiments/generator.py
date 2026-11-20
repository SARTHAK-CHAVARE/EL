"""Seeded instance generator (SPEC-002 section 3).

Deterministic: identical (design, task) always yields the identical instance (the RNG is seeded from a
string, which Python hashes deterministically with SHA-512 independent of PYTHONHASHSEED).
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, Tuple

from model import Instance, Job, inr_to_paise, kw_to_w
from model.tariff import tou_vector_paise

from .baselines import fcfs_schedule, spt_schedule
from .design import Design, Task, frac


class GeneratorError(RuntimeError):
    pass


@dataclass(frozen=True)
class InstanceMeta:
    instance_id: str
    gamma: str
    w_target: str
    cv: str
    seed_idx: int
    w_real: float
    attempts: int
    off_paise: int
    normal_paise: int
    peak_paise: int
    machine_power_w: Tuple[int, ...]


def _round_half_up(x: Fraction) -> int:
    return int(math.floor(x + Fraction(1, 2)))


def tariff_levels_paise(gamma: Fraction, normal_inr: str) -> Tuple[int, int, int]:
    """(off, normal, peak) in paise/kWh. Normal is fixed; normal = mean(off, peak); peak = gamma*off.

    gamma = 19/14 reproduces the KERC HT-2(a) values 5.60 / 6.60 / 7.60 exactly.
    """
    normal = Fraction(inr_to_paise(normal_inr))
    off = 2 * normal / (1 + gamma)
    peak = gamma * off
    return _round_half_up(off), int(normal), _round_half_up(peak)


def machine_powers_w(n_machines: int, mean_kw: str, cv: Fraction) -> Tuple[int, ...]:
    """Equally spaced machine powers with mean ``mean_kw`` and (population) coefficient of variation ``cv``.

    standardised offsets a_m (mean 0, population SD 1); P_m = mean * (1 + cv * a_m); floor 0.5 kW.
    """
    mean_w = kw_to_w(mean_kw)
    if n_machines == 1 or cv == 0:
        return tuple([mean_w] * n_machines)
    raw = [i - (n_machines - 1) / 2 for i in range(n_machines)]
    sd = math.sqrt(sum(r * r for r in raw) / n_machines)
    return tuple(max(500, int(round(mean_w * (1 + float(cv) * r / sd)))) for r in raw)


def workload_w(inst: Instance) -> Fraction:
    """THE workload definition (SPEC-002 section 2), exact:

        W = ( sum_j  min_m p_jm ) / ( M * T )

    i.e. the fraction of the machines' time capacity needed if every job ran on its fastest machine. It is a
    time-based utilisation lower bound. It deliberately does NOT involve machine powers, so that W (how busy the
    shop is) and CV (how different the machines' powers are) stay separate factors. Generator metadata
    (``InstanceMeta.w_real``) and the tests both use this function.
    """
    return Fraction(sum(min(j.proc.values()) for j in inst.jobs), len(inst.machines) * inst.T)


def draw_instance(design: Design, task: Task, attempt: int) -> Instance:
    """One raw random draw (attempt number ``attempt``) for ``task`` -- NO acceptance filter applied.

    ``generate_instance`` loops over attempts and keeps the first draw accepted by the heuristic filter; this
    function exposes the unfiltered draw so that the filter's selection effect can be studied
    (``results/cal2_prep/acceptance_study.py``). The random stream is exactly the one used by ``generate_instance``.
    """
    gamma = frac(design.gammas[task.gamma_idx])
    w_target = frac(design.workloads[task.w_idx])
    cv = frac(design.cvs[task.cv_idx])
    off, normal, peak = tariff_levels_paise(gamma, design.normal_inr)
    tariff = tou_vector_paise(design.shift_start_hour, design.delta_t_min, design.T, off, normal, peak)
    powers = machine_powers_w(design.n_machines, design.mean_power_kw, cv)
    machines = tuple(range(1, design.n_machines + 1))
    base_w = kw_to_w(design.base_kw)
    lo, hi = float(frac(design.proc_noise[0])), float(frac(design.proc_noise[1]))
    n, M, D = design.n_jobs, design.n_machines, design.T
    rng = random.Random(f"{design.base_seed}|{design.name}|{task.instance_id}|{attempt}")
    w = [0.5 + rng.random() for _ in range(n)]                       # relative job sizes
    u = [[lo + (hi - lo) * rng.random() for _ in range(M)] for _ in range(n)]  # machine multipliers
    min_u = [min(w[j] * u[j][m] for m in range(M)) for j in range(n)]
    k = float(w_target) * M * D / sum(min_u)
    jobs = []
    for j in range(n):
        proc = {m + 1: max(1, min(D, int(round(k * w[j] * u[j][m])))) for m in range(M)}
        jobs.append(Job(f"J{j + 1}", proc, {m: powers[m - 1] for m in proc}))
    return Instance(machines=machines, jobs=tuple(jobs), T=design.T, D=design.T,
                    delta_t_min=design.delta_t_min, base_w=base_w, tariff_paise=tariff, name=task.instance_id)


def generate_instance(design: Design, task: Task) -> Tuple[Instance, InstanceMeta]:
    off, normal, peak = tariff_levels_paise(frac(design.gammas[task.gamma_idx]), design.normal_inr)
    powers = machine_powers_w(design.n_machines, design.mean_power_kw, frac(design.cvs[task.cv_idx]))

    for attempt in range(1, design.max_attempts + 1):
        inst = draw_instance(design, task, attempt)
        # accept only instances for which a dispatch heuristic finds a feasible schedule (documented bias)
        if fcfs_schedule(inst) is not None or spt_schedule(inst) is not None:
            w_real = float(workload_w(inst))
            return inst, InstanceMeta(task.instance_id, design.gammas[task.gamma_idx],
                                      design.workloads[task.w_idx], design.cvs[task.cv_idx], task.seed_idx,
                                      round(w_real, 6), attempt, off, normal, peak, powers)
    raise GeneratorError(
        f"could not generate a feasible instance for {task.instance_id} in {design.max_attempts} attempts "
        f"(W target {design.workloads[task.w_idx]}); lower the workload level or raise max_attempts")
