"""P2 gate (ROADMAP-FINAL.md P2): energy-aware rules on all cal2 instances and the savings decomposition.

    python 07_src/scripts/baseline_preview.py [--out results/baselines_preview]

DESCRIPTIVE ONLY (cal2 has 2 seeds per cell). Inputs, all read-only:
  * results/cal2/results.csv               energy-only optimum B (ec_int, peak_w), stored FCFS rows (cross-check)
  * results/front_validation/parts/*.json  exact energy-peak fronts (C at any rho)
  * regenerated cal2 instances             FCFS, SPT, energy-greedy (EG) and peak-capped greedy (PCG) schedules
Every rule schedule is re-evaluated by the independent evaluator. Rule failures are counted, never dropped silently.

Chain (all as % of FCFS TEC):  FCFS -> EG (energy-aware rule) -> B (exact energy optimum) -> C (exact peak-aware optimum).
Separate claims: value of exact optimisation = (best rule - C) / best rule, best rule = min(EG, PCG);
value of peak-awareness = (B - C) / B.  Pre-stated S3 rule: if the best rule is within 1 % of C on >= 90 % of instances
at the KERC-equivalent rho, report that exact optimisation adds little at this scale.
"""
from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd  # noqa: E402

from experiments.baselines import (energy_greedy_schedule, fcfs_schedule, peak_capped_candidates,  # noqa: E402
                                   spt_schedule)
from experiments.design import DESIGN_CAL2, enumerate_tasks  # noqa: E402
from experiments.generator import generate_instance  # noqa: E402
from model import evaluate_schedule  # noqa: E402
from model.billing import BillingAssumptions, rho_equivalent_inr_per_kw  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
RHOS = {f"{r:g}": Fraction(r) for r in (1, 2, 5, 14, 50)}
RHOS["eq26"] = rho_equivalent_inr_per_kw(BillingAssumptions(26))
RHOS["eq30"] = rho_equivalent_inr_per_kw(BillingAssumptions(30))
INR = 6_000_000


def tec_inr(ec_int: int, peak_w: int, rho_inr: Fraction) -> Fraction:
    """EC + rho * peak in INR (rho in INR/kW): ec_int / 6e6 + rho * peak_w / 1000."""
    return Fraction(ec_int, INR) + rho_inr * Fraction(peak_w, 1000)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cal2", type=Path, default=ROOT / "results/cal2")
    ap.add_argument("--fronts", type=Path, default=ROOT / "results/front_validation/parts")
    ap.add_argument("--out", type=Path, default=ROOT / "results/baselines_preview")
    a = ap.parse_args(argv)
    df = pd.read_csv(a.cal2 / "results.csv", dtype={"w_target": str, "cv": str, "gamma": str})
    S = {s: df[df.strategy == s].set_index("instance_id") for s in ("B", "FCFS", "SPT")}
    rows, inst_rows, problems = [], [], []
    for task in enumerate_tasks(DESIGN_CAL2):
        iid = task.instance_id
        inst, meta = generate_instance(DESIGN_CAL2, task)
        front = json.loads((a.fronts / f"{iid}.json").read_text())
        if not front["complete"]:
            problems.append(f"{iid}: front not complete")
        pts = [(p["ec_int"], p["peak_w"]) for p in front["points"]]
        b = S["B"].loc[iid]
        if b.status != "OPTIMAL":
            problems.append(f"{iid}: B not optimal")
        b_ec, b_pk = int(b.ec_int), int(b.peak_w)
        sched = {"FCFS": fcfs_schedule(inst), "SPT": spt_schedule(inst), "EG": energy_greedy_schedule(inst)}
        met = {k: (evaluate_schedule(inst, s, 0, strict=True) if s is not None else None) for k, s in sched.items()}
        for k in ("FCFS", "SPT"):                                       # regenerated rule == stored cal2 row
            st = S[k].loc[iid]
            stored = None if st.status != "HEURISTIC" else (int(st.ec_int), int(st.peak_w))
            got = None if met[k] is None else (met[k].ec_int, met[k].peak_w)
            if stored != got:
                problems.append(f"{iid}: regenerated {k} {got} != stored {stored}")
        pcg = [(evaluate_schedule(inst, s, 0, strict=True), cap) for cap, s in peak_capped_candidates(inst)]
        eg = met["EG"]
        inst_rows.append(dict(instance_id=iid, gamma=meta.gamma, w_target=meta.w_target, w_real=meta.w_real, cv=meta.cv,
                              fcfs_ok=met["FCFS"] is not None, eg_ok=eg is not None, n_pcg_candidates=len(pcg),
                              eg_energy_gap_pct=(float(Fraction(eg.ec_int - b_ec, b_ec) * 100) if eg else None),
                              eg_peak_kw=eg.peak_w / 1000 if eg else None, b_peak_kw=b_pk / 1000,
                              front_points=len(pts), conflict=any(pk < b_pk for _, pk in pts)))
        for name, rho in RHOS.items():
            c = min(tec_inr(e, p, rho) for e, p in pts)
            bt = tec_inr(b_ec, b_pk, rho)
            ft = tec_inr(met["FCFS"].ec_int, met["FCFS"].peak_w, rho) if met["FCFS"] else None
            st_ = tec_inr(met["SPT"].ec_int, met["SPT"].peak_w, rho) if met["SPT"] else None
            et = tec_inr(eg.ec_int, eg.peak_w, rho) if eg else None
            pt = min((tec_inr(m.ec_int, m.peak_w, rho) for m, _ in pcg), default=None)
            best_rule = min([x for x in (et, pt) if x is not None], default=None)
            for label, val in (("EG", et), ("PCG", pt), ("B", bt)):
                if val is not None and val < c:
                    problems.append(f"{iid} rho {name}: {label} TEC {float(val)} below the exact optimum {float(c)}")
            r = dict(instance_id=iid, gamma=meta.gamma, w_target=meta.w_target, cv=meta.cv, rho=name,
                     rho_inr=float(rho), tec_fcfs=_f(ft), tec_spt=_f(st_), tec_eg=_f(et), tec_pcg=_f(pt),
                     tec_b=float(bt), tec_c=float(c))
            r["chain_complete"] = bool(ft and et)          # the FCFS -> EG -> B -> C chain needs FCFS and EG
            if r["chain_complete"]:
                r.update(step_fcfs_to_eg_pct=_pct(ft - et, ft), step_eg_to_b_pct=_pct(et - bt, ft),
                         step_b_to_c_pct=_pct(bt - c, ft), total_fcfs_to_c_pct=_pct(ft - c, ft))
            r.update(peak_aware_vs_b_pct=_pct(bt - c, bt),
                     pcg_vs_eg_pct=_pct(et - pt, et) if (et and pt) else None,
                     opt_vs_best_rule_pct=_pct(best_rule - c, best_rule) if best_rule else None)
            r["best_rule_within_1pct"] = None if r["opt_vs_best_rule_pct"] is None else r["opt_vs_best_rule_pct"] < 1.0
            rows.append(r)
    out = a.out
    out.mkdir(parents=True, exist_ok=True)
    it, rt = pd.DataFrame(inst_rows), pd.DataFrame(rows)
    it.to_csv(out / "instances.csv", index=False)
    rt.to_csv(out / "per_instance_rho.csv", index=False)

    def summ(d):
        g = d.groupby("rho", sort=False)
        s = g.agg(n=("instance_id", "size"), n_fcfs=("tec_fcfs", "count"), n_eg=("tec_eg", "count"),
                  n_pcg=("tec_pcg", "count"), n_chain=("chain_complete", "sum"),
                  n_c_vs_b=("peak_aware_vs_b_pct", "count"), n_c_vs_rule=("opt_vs_best_rule_pct", "count"),
                  fcfs_to_eg_mean=("step_fcfs_to_eg_pct", "mean"), eg_to_b_mean=("step_eg_to_b_pct", "mean"),
                  b_to_c_mean=("step_b_to_c_pct", "mean"), fcfs_to_c_mean=("total_fcfs_to_c_pct", "mean"),
                  peak_aware_vs_b_mean=("peak_aware_vs_b_pct", "mean"), pcg_vs_eg_mean=("pcg_vs_eg_pct", "mean"),
                  opt_vs_rule_mean=("opt_vs_best_rule_pct", "mean"), opt_vs_rule_median=("opt_vs_best_rule_pct", "median"),
                  opt_vs_rule_max=("opt_vs_best_rule_pct", "max"),
                  share_rule_within_1pct=("best_rule_within_1pct", "mean"))
        return s.reset_index()
    parts = []
    for label, d in (("all", rt), ("cv<=0.35", rt[rt.cv.isin(["0", "0.35"])]), ("cv=0.75 (stress)", rt[rt.cv == "0.75"]),
                     ("conflict instances", rt[rt.instance_id.isin(it[it.conflict].instance_id)])):
        s = summ(d)
        s.insert(0, "subset", label)
        parts.append(s)
    summary = pd.concat(parts, ignore_index=True)
    summary.to_csv(out / "summary.csv", index=False)
    s3 = {}
    for label in ("all", "cv<=0.35"):
        row = summary[(summary.subset == label) & (summary.rho == "eq26")].iloc[0]
        s3[label] = dict(share_best_rule_within_1pct=float(row.share_rule_within_1pct),
                         triggers_little_value_rule=bool(row.share_rule_within_1pct >= 0.90))
    meta = dict(instances=len(it), fcfs_feasible=int(it.fcfs_ok.sum()), eg_feasible=int(it.eg_ok.sum()),
                eg_energy_optimal=int((it.eg_energy_gap_pct == 0).sum()),
                eg_energy_gap_pct=dict(mean=float(it.eg_energy_gap_pct.mean()), max=float(it.eg_energy_gap_pct.max())),
                conflict_instances=int(it.conflict.sum()),
                rho_eq_inr={"eq26": str(RHOS["eq26"]), "eq30": str(RHOS["eq30"])}, s3_at_rho_eq26=s3, problems=problems)
    (out / "summary.json").write_text(json.dumps(meta, indent=2, default=str))
    (out / "README.txt").write_text(
        "P2 preview on cal2 instances: DESCRIPTIVE ONLY (2 seeds per cell); not a validated finding.\n"
        "Steps are % of FCFS TEC: FCFS -> EG (energy-greedy rule) -> B (exact energy optimum) -> C (exact peak-aware).\n"
        "The chain columns are averaged over n_chain instances (FCFS and EG both succeeded); C-vs-B over n_c_vs_b and\n"
        "C-vs-best-rule over n_c_vs_rule. In cal2 FCFS failed on 1 instance, so n_chain = 89 of 90 (59 of 60 for CV<=0.35).\n"
        "opt_vs_best_rule_pct = (min(EG, PCG) - C) / min(EG, PCG) * 100. rho 'eq26'/'eq30' = 350/(days x PF), PF 1,\n"
        "renegotiated-contract-demand equivalent (model/billing.py). Rule failures are counted in n_eg / n_pcg.\n")
    pd.set_option("display.width", 250)
    print(summary.round(2).to_string(index=False))
    print(json.dumps(meta, indent=1, default=str))
    return 0 if not problems else 1


def _f(x):
    return None if x is None else float(x)


def _pct(num, den):
    return float(Fraction(num) / Fraction(den) * 100)


if __name__ == "__main__":
    sys.exit(main())
