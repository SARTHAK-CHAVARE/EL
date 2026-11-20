"""Time-indexed CP-SAT formulation of Model V1.0 (SPEC-001 sections 2-5).

``build_formulation`` returns a fresh model plus named linear expressions that stages of a
lexicographic strategy can minimise / constrain. All coefficients are Python ints.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from ortools.sat.python import cp_model

from .instance import Instance
from .tariff import MINUTES_PER_HOUR
from .validation import InstanceError, OVERFLOW_LIMIT, tec_upper_bound, validate_instance

Triple = Tuple[str, int, int]  # (job_id, machine_id, start_slot)


class InfeasibleInstance(Exception):
    """Raised when some job has no valid (machine, start) placement at all."""


def placements(inst: Instance) -> List[Triple]:
    """All valid (job, machine, start) triples: release/deadline/horizon respected (Eqs. 3, 4, 8)."""
    out: List[Triple] = []
    for j in inst.jobs:
        last = inst.job_deadline(j)
        for m, p in j.proc.items():
            for t in range(j.release, last - p + 2):  # t + p - 1 <= last
                out.append((j.job_id, m, t))
    return out


@dataclass
class Formulation:
    model: cp_model.CpModel
    x: Dict[Triple, cp_model.IntVar]
    exprs: Dict[str, object]          # name -> linear expression / IntVar
    rho_paise: int
    meta: Dict[str, int] = field(default_factory=dict)


def build_formulation(inst: Instance, rho_paise: int = 0, redundant: bool = True) -> Formulation:
    """Build the shared feasible set (Eqs. 1-14) and the objective expressions.

    Exposed expressions: ``cmax``, ``sum_c``, ``pmax``, ``ec``, ``dc``, ``tec``.
    """
    if not isinstance(rho_paise, int) or isinstance(rho_paise, bool) or rho_paise < 0:
        raise InstanceError([f"rho_paise must be a non-negative int (got {rho_paise!r})"])
    validate_instance(inst, rho_paise)

    trips = placements(inst)
    have = defaultdict(int)
    for jid, _, _ in trips:
        have[jid] += 1
    missing = [j.job_id for j in inst.jobs if have[j.job_id] == 0]
    if missing:
        raise InfeasibleInstance(
            f"no valid (machine, start) placement within release/deadline for job(s): {', '.join(missing)}"
        )

    jobs = {j.job_id: j for j in inst.jobs}
    model = cp_model.CpModel()
    x = {tr: model.new_bool_var(f"x[{tr[0]},{tr[1]},{tr[2]}]") for tr in trips}

    # (1)-(2) exactly one start per job
    by_job: Dict[str, List[Triple]] = defaultdict(list)
    for tr in x:
        by_job[tr[0]].append(tr)
    for jid, keys_j in by_job.items():
        model.add_exactly_one([x[tr] for tr in keys_j])

    # coverage of every (machine, slot) and per-slot power terms  (Eqs. 5, 6, 11)
    cover: Dict[Tuple[int, int], List[cp_model.IntVar]] = defaultdict(list)
    slot_terms: Dict[int, List[Tuple[cp_model.IntVar, int]]] = defaultdict(list)
    ec_coef: Dict[Triple, int] = defaultdict(int)
    w_slot = {t: inst.tariff_paise[t - 1] * inst.delta_t_min for t in range(1, inst.T + 1)}
    for tr, v in x.items():
        jid, m, s = tr
        job = jobs[jid]
        p, pw = job.proc[m], job.power_w[m]
        for t in range(s, s + p):
            cover[(m, t)].append(v)
            slot_terms[t].append((v, pw))
            ec_coef[tr] += w_slot[t] * pw
    for vs in cover.values():                       # (6) machine non-overlap
        if len(vs) > 1:
            model.add_at_most_one(vs)

    max_machine_w = {m: 0 for m in inst.machines}
    for j in inst.jobs:
        for m, w in j.power_w.items():
            max_machine_w[m] = max(max_machine_w[m], w)
    p_ub = inst.base_w + sum(max_machine_w.values())

    # (11) slot power and (14) exact peak
    pt_vars = []
    for t in range(1, inst.T + 1):
        terms = slot_terms.get(t)
        if not terms:
            continue
        pv = model.new_int_var(inst.base_w, p_ub, f"P[{t}]")
        model.add(pv == inst.base_w + cp_model.LinearExpr.weighted_sum(
            [v for v, _ in terms], [w for _, w in terms]))
        pt_vars.append(pv)
    pmax = model.new_int_var(inst.base_w, p_ub, "Pmax")
    model.add_max_equality(pmax, pt_vars + [inst.base_w])

    # (7), (9), (10) completion times and makespan
    cj_vars = []
    cmax_lo = 1
    for j in inst.jobs:
        last = inst.job_deadline(j)
        lo = j.release + min(j.proc.values()) - 1
        cmax_lo = max(cmax_lo, lo)
        cj = model.new_int_var(lo, last, f"C[{j.job_id}]")
        keys_j = by_job[j.job_id]
        model.add(cj == cp_model.LinearExpr.weighted_sum(
            [x[tr] for tr in keys_j], [tr[2] + j.proc[tr[1]] - 1 for tr in keys_j]))
        cj_vars.append(cj)
    cmax = model.new_int_var(cmax_lo, inst.D, "Cmax")
    model.add_max_equality(cmax, cj_vars)

    # Optional redundant interval constraints (SPEC-001 section 3): per-machine NoOverlap and a cumulative
    # constraint "total job power <= Pmax - base". They are *implied* by Eqs. (6),(11),(14) and change no
    # feasible schedule or objective value; they only strengthen propagation (lower bounds on C_max
    # under a peak cap), which makes the lexicographic tie-break stages provable much faster.
    if redundant:
        ivs_by_machine: Dict[int, list] = defaultdict(list)
        all_ivs, demands = [], []
        for jid, keys_j in by_job.items():
            job = jobs[jid]
            for m in job.proc:
                kk = [tr for tr in keys_j if tr[1] == m]
                if not kk:
                    continue
                z = model.new_bool_var(f"z[{jid},{m}]")
                model.add(z == sum(x[tr] for tr in kk))
                lo, hi = min(tr[2] for tr in kk), max(tr[2] for tr in kk)
                st = model.new_int_var(lo, hi, f"s[{jid},{m}]")
                model.add(st == cp_model.LinearExpr.weighted_sum([x[tr] for tr in kk], [tr[2] for tr in kk])
                          ).only_enforce_if(z)
                iv = model.new_optional_fixed_size_interval_var(st, job.proc[m], z, f"iv[{jid},{m}]")
                ivs_by_machine[m].append(iv)
                all_ivs.append(iv)
                demands.append(job.power_w[m])
        for ivs in ivs_by_machine.values():
            if len(ivs) > 1:
                model.add_no_overlap(ivs)
        if all_ivs:
            model.add_cumulative(all_ivs, demands, pmax - inst.base_w)

    # objective expressions (SPEC-001 section 4)
    ec_const = sum(w_slot[t] for t in range(1, inst.T + 1)) * inst.base_w
    keys = list(ec_coef)
    ec = cp_model.LinearExpr.weighted_sum([x[k] for k in keys], [ec_coef[k] for k in keys]) + ec_const
    dc = MINUTES_PER_HOUR * rho_paise * pmax
    tec = ec + dc
    sum_c = cp_model.LinearExpr.sum(cj_vars)

    return Formulation(
        model=model, x=x,
        exprs={"cmax": cmax, "sum_c": sum_c, "pmax": pmax, "ec": ec, "dc": dc, "tec": tec},
        rho_paise=rho_paise,
        meta={"n_x": len(x), "tec_upper_bound": tec_upper_bound(inst, rho_paise), "limit": OVERFLOW_LIMIT},
    )
