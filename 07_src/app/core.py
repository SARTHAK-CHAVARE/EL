"""Shared engine of the prototype (used by the CLI and the Streamlit app). No new modelling: it calls the validated
solver (Model V1.0), the energy-peak front, the safety guard, the simple rules and the partial billing layer.

    a = analyse(inst)                       # solves once: energy-only B + the front (+ rules)
    c = choose(a, rho_paise)                # recommended schedule at any demand charge (no new solve)
    rows = comparison(a, rho_paise)         # FCFS / energy rule / peak-capped rule / energy-only / recommended
    bills = bills(a, c, BillingAssumptions(days_per_month=26))
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Dict, List, Optional, Sequence, Tuple

from experiments.baselines import energy_greedy_schedule, fcfs_schedule, peak_capped_candidates
from model import (BreakEven, Front, Instance, Metrics, Operation, Recommendation, SolverConfig, break_even,
                   ec_peak_front, evaluate_schedule, recommend, rho_intervals, solve_strategy_b)
from model.billing import BillComparison, BillingAssumptions, compare_bills, rho_equivalent_inr_per_kw

INR = 6_000_000
DEFAULT_CONFIG = SolverConfig(time_limit_s=180.0, deterministic_time_limit=60.0, num_workers=1, random_seed=0,
                              tiebreak_time_limit_s=60.0, tiebreak_deterministic_time_limit=15.0)


@dataclass
class Analysis:
    inst: Instance
    b_schedule: Optional[Tuple[Operation, ...]]
    b_metrics: Optional[Metrics]
    b_status: str
    front: Front
    break_even_b: Optional[BreakEven]
    rules: Dict[str, Optional[Tuple[Operation, ...]]]
    pcg_candidates: List[Tuple[Optional[int], Tuple[Operation, ...], Metrics]]
    solve_time_s: float
    notes: List[str] = field(default_factory=list)


def analyse(inst: Instance, config: Optional[SolverConfig] = None) -> Analysis:
    """Solve once. Everything at any demand charge is then read off the front (no further solves)."""
    cfg = config or DEFAULT_CONFIG
    t0 = time.perf_counter()
    b = solve_strategy_b(inst, cfg)
    front = ec_peak_front(inst, cfg)
    be = break_even(front, b.metrics.ec_int, b.metrics.peak_w, "B") if b.metrics else None
    rules = {"FCFS": fcfs_schedule(inst), "Energy rule": energy_greedy_schedule(inst)}
    rules = {k: (tuple(v) if v is not None else None) for k, v in rules.items()}
    pcg = [(cap, tuple(s), evaluate_schedule(inst, s, 0)) for cap, s in peak_capped_candidates(inst)]
    notes = []
    if not front.complete:
        notes.append(f"Front not proven complete ({front.reason}); break-even is an UPPER BOUND and a gap is shown.")
    if b.status.value != "OPTIMAL":
        notes.append(f"Energy-only reference B is {b.status.value} (not proven optimal).")
    return Analysis(inst, tuple(b.schedule) if b.schedule else None, b.metrics, b.status.value, front, be, rules, pcg,
                    time.perf_counter() - t0, notes)


def rho_paise_from_inr(rho_inr) -> int:
    """Demand charge in INR/kW per shift -> integer paise (the schedulers work in whole paise)."""
    return int(round(Fraction(str(rho_inr)) * 100))


def choose(a: Analysis, rho_paise: int) -> Recommendation:
    """Recommended schedule at ``rho_paise``: the guard over the front, B and the simple rules (never worse than any)."""
    cands = {"Energy-only (B)": a.b_schedule, **a.rules}
    if a.pcg_candidates:
        best = min(a.pcg_candidates, key=lambda c: (c[2].ec_int + 60 * rho_paise * c[2].peak_w, c[2].makespan))
        cands["Peak-capped rule"] = best[1]
    return recommend(a.inst, rho_paise, a.front, cands)


def tec_inr(m: Metrics, rho_paise: int) -> Fraction:
    return Fraction(m.ec_int + 60 * rho_paise * m.peak_w, INR)


def comparison(a: Analysis, rho_paise: int) -> List[dict]:
    """One row per approach at this demand charge (INR per shift). 'proven' is True only for proven optima."""
    rec = choose(a, rho_paise)
    rows = []

    def add(name, sched, proven, note=""):
        if sched is None:
            rows.append(dict(approach=name, feasible=False, note=note or "rule could not place every job"))
            return
        m = evaluate_schedule(a.inst, sched, rho_paise, strict=True)
        rows.append(dict(approach=name, feasible=True, energy_inr=float(Fraction(m.ec_int, INR)),
                         peak_kw=m.peak_w / 1000, demand_inr=float(Fraction(60 * rho_paise * m.peak_w, INR)),
                         total_inr=float(tec_inr(m, rho_paise)), makespan=m.makespan, proven=proven, note=note))
    add("FCFS (current practice proxy)", a.rules["FCFS"], False)
    add("Energy rule (greedy)", a.rules["Energy rule"], False)
    best_pcg = None
    if a.pcg_candidates:
        best_pcg = min(a.pcg_candidates, key=lambda c: (c[2].ec_int + 60 * rho_paise * c[2].peak_w, c[2].makespan))
    add("Peak-capped rule (greedy)", best_pcg[1] if best_pcg else None, False)
    add("Energy-only optimum (B)", a.b_schedule, a.b_status == "OPTIMAL", "ignores the demand charge")
    gap = "" if rec.gap is None else f"gap {float(rec.gap) * 100:.2f} %"
    add("Recommended (peak-aware)", rec.schedule, rec.proven_optimal,
        "proven optimal" if rec.proven_optimal else (gap or "not proven"))
    base = next((r for r in rows if r["approach"].startswith("FCFS") and r["feasible"]), None)
    for r in rows:
        if r["feasible"] and base:
            r["saving_vs_fcfs_pct"] = (base["total_inr"] - r["total_inr"]) / base["total_inr"] * 100
    return rows


def front_table(a: Analysis) -> List[dict]:
    iv = rho_intervals(a.front)
    out = []
    for p, v in zip(a.front.points, iv):
        out.append(dict(peak_kw=p.peak_w / 1000, energy_inr=float(Fraction(p.ec_int, INR)), makespan=p.makespan,
                        proven=bool(a.front.complete and p.ec_proven),
                        best_for_rho_inr=("never (unsupported)" if v is None else
                                          f"{float(v[0]):.2f} - {'inf' if v[1] is None else f'{float(v[1]):.2f}'}")))
    return out


def bills(a: Analysis, rec: Recommendation, assumptions: BillingAssumptions) -> Dict[str, BillComparison]:
    """Partial monthly bills of the recommended schedule vs the energy-only schedule B, both CD scenarios."""
    m = rec.metrics
    return compare_bills(m.ec_int, m.peak_w, a.b_metrics.ec_int, a.b_metrics.peak_w, assumptions)


def kerc_rho_paise(assumptions: BillingAssumptions) -> int:
    return rho_paise_from_inr(rho_equivalent_inr_per_kw(assumptions))


def break_even_text(a: Analysis) -> str:
    be = a.break_even_b
    if be is None:
        return "Break-even: not available (no energy-only reference)."
    if be.kind == "no_peak_reduction":
        return "No peak reduction is possible (proven): the energy-only schedule is optimal at every demand charge."
    if be.kind == "undetermined":
        return "Break-even undetermined: the front could not be proven within the time limits."
    label = "exact" if be.kind == "exact" else "UPPER BOUND (front not proven complete)"
    return (f"Break-even demand charge: INR {float(be.rho_inr):.2f}/kW per shift ({label}). Above it, cutting the peak "
            f"to {be.via_peak_w / 1000:g} kW beats the energy-only schedule; below it, run energy-only.")


def best_for_bill(a: Analysis, assumptions: BillingAssumptions, scenario: str):
    """Cheapest candidate (front points, energy-only B, simple rules) for the PARTIAL monthly bill under one contract-
    demand scenario. Under 'fixed', CD = the energy-only schedule's MD for every candidate, so a peak cut below
    0.90 x CD earns nothing: the answer can differ from the rho-based choice. Returns (name, schedule, bill)."""
    from model.billing import md_kva, partial_monthly_bill
    cands = [(f"front[peak={p.peak_w}W]", p.schedule) for p in a.front.points]
    cands += [("Energy-only (B)", a.b_schedule)] + [(k, v) for k, v in a.rules.items()]
    cands += [(f"Peak-capped rule[cap={cap}]", s) for cap, s, _ in a.pcg_candidates]
    cd = md_kva(a.b_metrics.peak_w, assumptions) if scenario == "fixed" else None
    best = None
    for order, (name, s) in enumerate(cands):
        if s is None:
            continue
        m = evaluate_schedule(a.inst, s, 0, strict=True)
        bill = partial_monthly_bill(m.ec_int, m.peak_w, assumptions, scenario, cd)
        key = (bill.total_inr, m.makespan, order)
        if best is None or key < best[0]:
            best = (key, name, tuple(s), bill)
    return best[1], best[2], best[3]


def generated_instance_dict(size: str = "8x3", gamma: str = "19/14", w: str = "0.55", cv: str = "0.35",
                            seed: int = 1) -> dict:
    """Instance JSON from the study's generator (same code as the experiments; shift 16:00-24:00, 15-min slots)."""
    from app.io import instance_to_dict
    from experiments.design import Design, Task
    from experiments.generator import generate_instance
    n, m = (int(x) for x in size.split("x"))
    d = Design(name="app", gammas=(gamma,), workloads=(w,), cvs=(cv,), rho_inr=("14",), seeds_per_cell=1,
               n_jobs=n, n_machines=m, base_seed=int(seed))
    inst, meta = generate_instance(d, Task("app", 0, 0, 0, 0))
    dd = instance_to_dict(inst, start_time="16:00")
    dd["name"] = f"generated {size}, gamma {gamma}, W {w}, CV {cv}, seed {seed} (realised W {meta.w_real:.3f})"
    return dd
