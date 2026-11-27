"""P6: analysis of the SPEC-003 main study, following docs/handoff/SPEC-003-main-study.md sections 1 and 5-12.

    python 07_src/scripts/main_report.py                       # both blocks, 2000 bootstrap replicates
    python 07_src/scripts/main_report.py --n-boot 200 --blocks m3   # quick look

Inputs: results/main_m3 and results/main_m4 (results.csv + manifest.json; digests checked against the frozen designs).
Outputs: results/main_analysis/<block>/*.csv and results/main_analysis/summary.json, plus a README.txt with the labels.

How the numbers are made (no new CP-SAT solves):
* Grid rho {1, 2, 5, 14, 50}: C, the guard and PCG are recomputed from the stored rows and checked against the stored
  C_front / GUARD / PCG rows (any difference is listed under "problems").
* rho_eq = 350/(D.PF), D in {22, 26, 30}, PF in {1, 0.9}: C is read off the front (exact iff the front is complete); the
  guard is the cheapest of the same candidates the runner uses (direct C is a candidate only at its own rho = 14);
  PCG is re-evaluated from the regenerated rule schedules (deterministic heuristics; FCFS/SPT/EG regeneration is checked
  against the stored rows). For incomplete fronts no lower bound is available at rho_eq, so the bound-based upper bound
  of the saving is reported at the grid rho only.
* Exact values are never pooled with bounds. Exclusions are counted by reason (missing / unproven / no_schedule).
* Intervals: analysis.tables.stratified_cluster_bootstrap (instances resampled within gamma x W x CV cells, statistic =
  unweighted mean of cell means, 95 % percentile). No significance tests.
* Bills are PARTIAL MONTHLY BILL ESTIMATES (model/billing.py): demand charge + energy of the scheduled shift only.
"""
from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "07_src"))

import pandas as pd  # noqa: E402

from analysis.tables import MIN_SEEDS_FOR_INTERVALS, SCALE, stratified_cluster_bootstrap  # noqa: E402
from experiments.baselines import (energy_greedy_schedule, fcfs_schedule, peak_capped_candidates,  # noqa: E402
                                   spt_schedule)
from experiments.design import DESIGNS, enumerate_tasks  # noqa: E402
from experiments.generator import generate_instance  # noqa: E402
from model import evaluate_schedule  # noqa: E402
from model.billing import PARTIAL_BILL_LABEL, BillingAssumptions, compare_bills, rho_equivalent_inr_per_kw  # noqa: E402

BLOCKS = {"m3": ("main-m3", "main_m3"), "m4": ("main-m4", "main_m4"),
          "m3-smoke": ("main-m3-smoke", "main_smoke/m3"), "m4-smoke": ("main-m4-smoke", "main_smoke/m4")}  # smoke: tests
STRATA = ["gamma", "w_target", "cv"]
GRID = {r: Fraction(r) for r in ("1", "2", "5", "14", "50")}
EQ_SETTINGS = [(d, pf) for d in (22, 26, 30) for pf in (Fraction(1), Fraction(9, 10))]


def eq_label(d: int, pf: Fraction) -> str:
    return f"eq{d}" if pf == 1 else f"eq{d}_pf{float(pf):g}"


EQ = {eq_label(d, pf): (d, pf, rho_equivalent_inr_per_kw(BillingAssumptions(days_per_month=d, power_factor=pf)))
      for d, pf in EQ_SETTINGS}
RHOS = {**GRID, **{k: v[2] for k, v in EQ.items()}}
HEADLINE_RHO = "eq26"


def tec(ec_int: int, peak_w: int, rho: Fraction) -> Fraction:
    """Shift TEC in INR: energy + rho [INR/kW] x peak [kW] (same as tec_int / SCALE)."""
    return Fraction(ec_int, SCALE) + rho * Fraction(peak_w, 1000)


def pct(num, den):
    return None if num is None or den in (None, 0) else float(Fraction(num) / Fraction(den) * 100)


def _int(x):
    return None if x in ("", None) or (isinstance(x, float) and x != x) else int(float(x))


class Problems(list):
    def add(self, msg: str) -> None:
        self.append(msg)


# --------------------------------------------------------------------------- per-instance extraction
def extract(g: pd.DataFrame, iid: str, problems: Problems) -> dict:
    def one(s):
        r = g[g.strategy == s]
        if len(r) != 1:
            problems.add(f"{iid}: expected one {s} row, found {len(r)}")
            return None
        return r.iloc[0]

    def ep(r):                                          # (ec_int, peak_w) of a row that has a schedule
        return None if r is None or r.ec_int == "" else (int(r.ec_int), int(r.peak_w))

    top, b, bmin, a, c14 = one("FRONT_top"), one("B"), one("B_minpeak"), one("A"), one("C")
    rules = {s: one(s) for s in ("FCFS", "SPT", "EG")}
    pts = [(int(r.ec_int), int(r.peak_w)) for r in g[g.strategy == "FRONT_PT"].itertuples()]
    req = g[g.strategy.isin(["FRONT_top", "FRONT_cap", "P"])]
    first = g.iloc[0]
    rec = dict(
        instance_id=iid, gamma=first.gamma, w_target=first.w_target, cv=first.cv, seed_idx=int(first.seed_idx),
        w_real=float(first.w_real), gen_attempts=int(first.gen_attempts),
        structural_peak_lb_w=_int(first.structural_peak_lb_w),
        front_complete=top is not None and top.front_complete == "1",
        front_termination=None if top is None else top.front_termination,
        front_n_points=len(pts), front_n_solves=len(req),
        required_solves=len(req), required_proven=int((req.required_proven == "1").sum()),
        top_proven=top is not None and top.status == "OPTIMAL", top_peak_w=None if top is None else _int(top.peak_w),
        b_ok=b is not None and b.status == "OPTIMAL", bmin_ok=bmin is not None and bmin.status == "OPTIMAL",
        a_ok=a is not None and a.status == "OPTIMAL",
        c14_proven=c14 is not None and c14.status == "OPTIMAL",
        c14_primary_proven=c14 is not None and c14.primary_proven == "1",
        task_cpu_s=float(first.task_cpu_s), task_wall_s=float(first.task_wall_s),
    )
    rec["pts"] = pts
    rec["B"], rec["Bmin"], rec["A"], rec["C14"] = ep(b), ep(bmin), ep(a), ep(c14)
    for s, r in rules.items():
        rec[s] = ep(r) if r is not None and r.status == "HEURISTIC" else None
    for ref in ("B", "B_minpeak"):
        r = one(f"BE_{ref}")
        rec[f"be_{ref}_kind"] = None if r is None else r.break_even_kind
        rec[f"be_{ref}_inr"] = None if r is None or r.break_even_inr == "" else Fraction(r.break_even_inr)
    if rec["B"]:
        bpk = rec["B"][1]
        found_lower = any(pk < bpk for _, pk in pts)
        rec["reduction_vs_B"] = found_lower if rec["front_complete"] else (True if found_lower else None)
        if rec["front_complete"] and rec["b_ok"] and pts:      # complete front: its min-EC points carry the proven min peak
            ec_min = min(e for e, _ in pts)
            if ec_min != rec["B"][0]:
                problems.add(f"{iid}: front min EC {ec_min} != proven B EC {rec['B'][0]}")
            rec["free_reduction_vs_B"] = min(pk for e, pk in pts if e == ec_min) < bpk
        else:
            rec["free_reduction_vs_B"] = (rec["top_peak_w"] < bpk) if rec["top_proven"] and rec["b_ok"] else None
    else:
        rec["reduction_vs_B"] = rec["free_reduction_vs_B"] = None
    rec["tradeoff"] = (len(pts) >= 2) if rec["front_complete"] else (True if len(pts) >= 2 else None)
    stored = {}
    for s in ("C_front", "GUARD", "PCG"):
        for r in g[g.strategy == s].itertuples():
            stored[(s, int(r.rho_paise))] = r
    rec["stored"] = stored
    sc14 = stored.get(("C_front", 1400))
    rec["cross_comparable"] = bool(rec["front_complete"] and rec["c14_primary_proven"] and sc14 is not None
                                   and sc14.tec_int != "" and c14 is not None and c14.tec_int != "")
    rec["cross_equal"] = rec["cross_comparable"] and int(sc14.tec_int) == int(c14.tec_int)
    if rec["cross_comparable"] and not rec["cross_equal"]:
        problems.add(f"{iid}: front C at rho 14 != proven direct C (stop and investigate, section 12)")
    return rec


def regenerate_rules(design, task, rec: dict, problems: Problems) -> list:
    """Regenerate the deterministic rule schedules; check FCFS/SPT/EG against the stored rows; return PCG candidates."""
    inst, _ = generate_instance(design, task)
    for name, fn in (("FCFS", fcfs_schedule), ("SPT", spt_schedule), ("EG", energy_greedy_schedule)):
        s = fn(inst)
        got = None if s is None else (lambda m: (m.ec_int, m.peak_w))(evaluate_schedule(inst, s, 0, strict=True))
        if got != rec[name]:
            problems.add(f"{rec['instance_id']}: regenerated {name} {got} != stored {rec[name]}")
    cands = []
    for _cap, s in peak_capped_candidates(inst):
        m = evaluate_schedule(inst, s, 0, strict=True)
        cands.append((m.ec_int, m.peak_w))
    return cands


# --------------------------------------------------------------------------- per (instance, rho)
def per_rho_rows(rec: dict, pcg: list, problems: Problems) -> list:
    iid, pts, complete = rec["instance_id"], rec["pts"], rec["front_complete"]
    out = []
    for label, rho in RHOS.items():
        grid = label in GRID
        rho_paise = int(rho * 100) if grid else None
        r = dict(instance_id=iid, gamma=rec["gamma"], w_target=rec["w_target"], cv=rec["cv"], rho=label,
                 rho_inr=float(rho), grid=grid, front_complete=complete)
        c_best = min(pts, key=lambda p: (tec(p[0], p[1], rho), -p[1])) if pts else None   # tie: higher peak
        c_val = None if c_best is None else tec(*c_best, rho)
        cands = list(pts) + [x for x in (rec["B"], rec["Bmin"], rec["A"], rec["EG"], rec["FCFS"], rec["SPT"]) if x]
        if rho == 14 and rec["C14"]:
            cands.append(rec["C14"])
        pcg_val = min((tec(e, p, rho) for e, p in pcg), default=None)
        guard_val = min([tec(e, p, rho) for e, p in cands] + ([pcg_val] if pcg_val is not None else []), default=None)
        lb = None
        if grid:
            st = rec["stored"]
            sc, sg, sp = st.get(("C_front", rho_paise)), st.get(("GUARD", rho_paise)), st.get(("PCG", rho_paise))
            if sc is not None and sc.tec_int != "" and c_val is not None and Fraction(int(sc.tec_int), SCALE) != c_val:
                problems.add(f"{iid} rho {label}: recomputed C {float(c_val)} != stored C_front {int(sc.tec_int) / SCALE}")
            if sg is not None and sg.tec_int != "" and guard_val is not None and Fraction(int(sg.tec_int), SCALE) != guard_val:
                problems.add(f"{iid} rho {label}: recomputed guard {float(guard_val)} != stored {int(sg.tec_int) / SCALE}")
            if sp is not None and sp.status == "HEURISTIC" and Fraction(int(sp.tec_int), SCALE) != pcg_val:
                problems.add(f"{iid} rho {label}: regenerated PCG {pcg_val} != stored {int(sp.tec_int) / SCALE}")
            if sg is not None and sg.tec_lower_bound != "":
                lb = Fraction(int(sg.tec_lower_bound), SCALE)
            r["guard_status"] = None if sg is None else sg.status
            r["guard_gap"] = None if sg is None or sg.gap == "" else float(sg.gap)
            r["c_front_status"] = None if sc is None else sc.status
        elif complete:
            lb = c_val
        if complete and guard_val is not None and c_val is not None and guard_val < c_val:
            problems.add(f"{iid} rho {label}: a candidate ({float(guard_val)}) beats the exact optimum ({float(c_val)})")
        tb = None if rec["B"] is None else tec(*rec["B"], rho)
        tbm = None if rec["Bmin"] is None else tec(*rec["Bmin"], rho)
        best_rule = min([x for x in ((tec(*rec["EG"], rho) if rec["EG"] else None), pcg_val) if x is not None], default=None)
        r.update(tec_b=None if tb is None else float(tb), tec_c=None if c_val is None else float(c_val),
                 tec_guard=None if guard_val is None else float(guard_val), tec_lb=None if lb is None else float(lb),
                 tec_best_rule=None if best_rule is None else float(best_rule),
                 c_peak_kw=None if c_best is None else c_best[1] / 1000)
        # Q3: saving of C over B / B_minpeak (exact set) and the all-instance sensitivity (achieved, bound-based UB)
        r["sav_B_valid"] = complete and rec["b_ok"]
        r["sav_B_pct"] = pct(tb - c_val, tb) if r["sav_B_valid"] else None
        r["sav_B_reason"] = "" if r["sav_B_valid"] else "unproven"
        r["sav_Bmin_valid"] = complete and rec["bmin_ok"]
        r["sav_Bmin_pct"] = pct(tbm - c_val, tbm) if r["sav_Bmin_valid"] else None
        r["sav_Bmin_reason"] = "" if r["sav_Bmin_valid"] else "unproven"
        r["ach_B_valid"] = tb is not None and guard_val is not None
        r["ach_B_pct"] = pct(tb - guard_val, tb) if r["ach_B_valid"] else None
        r["ach_B_reason"] = "" if r["ach_B_valid"] else "no_schedule"
        r["ub_B_valid"] = tb is not None and lb is not None
        r["ub_B_pct"] = pct(tb - lb, tb) if r["ub_B_valid"] else None
        r["ub_B_reason"] = "" if r["ub_B_valid"] else "unproven"
        for k in ("sav_B_pct", "sav_Bmin_pct", "ach_B_pct"):
            if r[k] is not None and r[k] < 0:
                problems.add(f"{iid} rho {label}: negative {k} = {r[k]} (C <= B by construction; bug)")
        # Q4: value of exact optimisation over the best rule
        r["opt_valid"] = complete and best_rule is not None
        r["opt_value_pct"] = pct(best_rule - c_val, best_rule) if r["opt_valid"] else None
        r["opt_reason"] = "" if r["opt_valid"] else ("unproven" if not complete else "no_schedule")
        if r["opt_value_pct"] is not None and r["opt_value_pct"] < 0:
            problems.add(f"{iid} rho {label}: a rule beats the exact optimum (opt_value {r['opt_value_pct']})")
        # Q5: decomposition FCFS -> EG -> B -> C in points of FCFS TEC (complete chains only)
        chain = complete and rec["b_ok"] and rec["FCFS"] is not None and rec["EG"] is not None
        r["chain_valid"] = chain
        r["chain_reason"] = "" if chain else ("unproven" if not (complete and rec["b_ok"]) else "no_schedule")
        if chain:
            tf, te = tec(*rec["FCFS"], rho), tec(*rec["EG"], rho)
            r.update(step_fcfs_eg_pct=pct(tf - te, tf), step_eg_b_pct=pct(te - tb, tf), step_b_c_pct=pct(tb - c_val, tf),
                     total_fcfs_c_pct=pct(tf - c_val, tf))
        # Q3 bills (rho_eq only)
        if label in EQ and r["sav_B_valid"]:
            d, pf, _ = EQ[label]
            cmp = compare_bills(c_best[0], c_best[1], rec["B"][0], rec["B"][1],
                                BillingAssumptions(days_per_month=d, power_factor=pf))
            for sc in ("renegotiated", "fixed"):
                x = cmp[sc]
                r[f"bill_{sc}_ref_inr"] = float(x.reference.total_inr)
                r[f"bill_{sc}_saving_inr"] = float(x.saving_inr)
                r[f"bill_{sc}_saving_pct"] = pct(x.saving_inr, x.reference.total_inr)
            r["bill_fixed_floor_binding"] = cmp["fixed"].candidate.floor_binding
        r["bill_valid"] = label in EQ and r["sav_B_valid"]
        r["bill_reason"] = "" if r["bill_valid"] else "unproven"
        out.append(r)
    return out


# --------------------------------------------------------------------------- summaries
def subsets(block: str, t: pd.DataFrame):
    if block.startswith("m3"):
        main = t[t.cv.isin(["0", "0.35"])]
        yield "cv<=0.35", main, [("all", []), ("by_W", ["w_target"]), ("by_gamma", ["gamma"]), ("by_CV", ["cv"])]
        yield "cv=0.75", t[t.cv == "0.75"], [("all", []), ("by_W", ["w_target"]), ("by_gamma", ["gamma"])]
    else:
        yield "all", t, [("all", []), ("by_W", ["w_target"]), ("by_CV", ["cv"])]


def summarise(t: pd.DataFrame, value: str, valid: str, reason: str, groups, n_boot: int, seed: str) -> list:
    out = []
    for gname, by in groups:
        parts = [((), t)] if not by else [((k if isinstance(k, tuple) else (k,)), g) for k, g in t.groupby(by)]
        for key, g in parts:
            gv = g[g[valid] & g[value].notna()]
            rec = dict(grouping=gname, level="|".join(map(str, key)) or "all", n_total=len(g), n_valid=len(gv))
            for why, n in g.loc[~g[valid], reason].value_counts().items():
                rec[f"n_{why}"] = int(n)
            if len(gv):
                est, lo, hi, ncell = stratified_cluster_bootstrap(gv, value, STRATA, n_boot=n_boot,
                                                                  seed_key=f"{seed}|{gname}|{key}|{value}")
                v = gv[value]
                rec.update(mean_of_cell_means=est, ci_lo=lo, ci_hi=hi, n_cells=ncell, median=float(v.median()),
                           q1=float(v.quantile(.25)), q3=float(v.quantile(.75)), min=float(v.min()), max=float(v.max()),
                           share_ge_1pct=float((v >= 1).mean()), share_gt_0=float((v > 1e-12).mean()))
            out.append(rec)
    return out


def analyse_block(block: str, n_boot: int, problems: Problems, results: Path, out_root: Path) -> dict:
    dname, rdir = BLOCKS[block]
    design = DESIGNS[dname]
    rdir = results / rdir
    man = json.loads((rdir / "manifest.json").read_text(encoding="utf-8"))
    if man["design_digest"] != design.digest():
        raise SystemExit(f"{rdir}: manifest digest {man['design_digest']} != frozen design {design.digest()}")
    df = pd.read_csv(rdir / "results.csv", dtype=str, keep_default_na=False)
    if set(df.design_digest) != {design.digest()}:
        raise SystemExit(f"{rdir}: results mix digests {sorted(set(df.design_digest))}")
    tasks = {t.instance_id: t for t in enumerate_tasks(design)}
    present = set(df.instance_id)
    missing = sorted(set(tasks) - present)
    insts, rows = [], []
    for iid, g in df.groupby("instance_id", sort=True):
        rec = extract(g, iid, problems)
        pcg = regenerate_rules(design, tasks[iid], rec, problems)
        rows += per_rho_rows(rec, pcg, problems)
        insts.append({k: v for k, v in rec.items() if k not in ("pts", "stored")} | dict(n_pcg_candidates=len(pcg)))
    for iid in missing:                                   # counted, never silent
        t = tasks[iid]
        lv = dict(instance_id=iid, gamma=design.gammas[t.gamma_idx], w_target=design.workloads[t.w_idx],
                  cv=design.cvs[t.cv_idx])
        insts.append(lv | dict(missing=True))
        for label, rho in RHOS.items():
            rows.append(lv | dict(rho=label, rho_inr=float(rho), grid=label in GRID, **{
                f"{k}_valid": False for k in ("sav_B", "sav_Bmin", "ach_B", "ub_B", "opt", "chain", "bill")}, **{
                f"{k}_reason": "missing" for k in ("sav_B", "sav_Bmin", "ach_B", "ub_B", "opt", "chain", "bill")}))
    it, pr = pd.DataFrame(insts), pd.DataFrame(rows)
    out = out_root / block
    out.mkdir(parents=True, exist_ok=True)
    it.to_csv(out / "instances.csv", index=False)
    pr.to_csv(out / "per_rho.csv", index=False)

    # ---- Q3/Q4/Q5 summaries (intervals: both blocks have >= MIN_SEEDS_FOR_INTERVALS seeds per cell)
    if design.seeds_per_cell < MIN_SEEDS_FOR_INTERVALS:          # smoke designs (tests only): no intervals claimed
        n_boot = max(n_boot, 1)
    estimands = [("sav_B_pct", "sav_B_valid", "sav_B_reason"), ("sav_Bmin_pct", "sav_Bmin_valid", "sav_Bmin_reason"),
                 ("opt_value_pct", "opt_valid", "opt_reason"), ("ach_B_pct", "ach_B_valid", "ach_B_reason"),
                 ("ub_B_pct", "ub_B_valid", "ub_B_reason"), ("step_fcfs_eg_pct", "chain_valid", "chain_reason"),
                 ("step_eg_b_pct", "chain_valid", "chain_reason"), ("step_b_c_pct", "chain_valid", "chain_reason"),
                 ("total_fcfs_c_pct", "chain_valid", "chain_reason"),
                 ("bill_renegotiated_saving_pct", "bill_valid", "bill_reason"),
                 ("bill_fixed_saving_pct", "bill_valid", "bill_reason"),
                 ("bill_renegotiated_saving_inr", "bill_valid", "bill_reason"),
                 ("bill_fixed_saving_inr", "bill_valid", "bill_reason")]
    summ = []
    for sname, sub, groups in subsets(block, pr):
        for label in RHOS:
            t = sub[sub.rho == label]
            for value, valid, reason in estimands:
                if value not in t or (value.startswith("bill_") and label not in EQ):
                    continue
                if value == "ub_B_pct" and label not in GRID:
                    continue
                for rec in summarise(t, value, valid, reason, groups, n_boot, f"{block}|{sname}|{label}"):
                    summ.append(dict(subset=sname, rho=label, estimand=value) | rec)
    sm = pd.DataFrame(summ)
    sm.to_csv(out / "summary_estimates.csv", index=False)

    # ---- Q1 conflict and Q2 break-even
    q1, q2 = [], []
    live = it[~it.get("missing", pd.Series(False, index=it.index)).fillna(False).astype(bool)]
    for sname, sub, groups in subsets(block, live):
        for gname, by in groups:
            parts = [((), sub)] if not by else [((k if isinstance(k, tuple) else (k,)), g) for k, g in sub.groupby(by)]
            for key, g in parts:
                lvl = "|".join(map(str, key)) or "all"
                known = g.reduction_vs_B.dropna()
                tk = g.tradeoff.dropna()
                fr = g.free_reduction_vs_B.dropna()
                q1.append(dict(subset=sname, grouping=gname, level=lvl, n=len(g),
                               reduction_vs_B_share=float(known.astype(bool).mean()) if len(known) else None,
                               reduction_undetermined=int(g.reduction_vs_B.isna().sum()),
                               costly_tradeoff_share=float(tk.astype(bool).mean()) if len(tk) else None,
                               tradeoff_undetermined=int(g.tradeoff.isna().sum()),
                               free_reduction_share=float(fr.astype(bool).mean()) if len(fr) else None,
                               free_reduction_undetermined=int(g.free_reduction_vs_B.isna().sum())))
                for ref in ("B", "B_minpeak"):
                    kinds = g[f"be_{ref}_kind"].value_counts().to_dict()
                    ex = g[g[f"be_{ref}_kind"] == "exact"][f"be_{ref}_inr"].map(float)
                    ub = g[g[f"be_{ref}_kind"] == "upper_bound"][f"be_{ref}_inr"].map(float)
                    rho_eq = float(EQ[HEADLINE_RHO][2])
                    q2.append(dict(subset=sname, grouping=gname, level=lvl, reference=ref, n=len(g),
                                   **{f"n_{k}": int(v) for k, v in kinds.items()},
                                   exact_median=float(ex.median()) if len(ex) else None,
                                   exact_q1=float(ex.quantile(.25)) if len(ex) else None,
                                   exact_q3=float(ex.quantile(.75)) if len(ex) else None,
                                   exact_min=float(ex.min()) if len(ex) else None,
                                   exact_max=float(ex.max()) if len(ex) else None,
                                   exact_share_zero=float((ex == 0).mean()) if len(ex) else None,
                                   share_pays_at_eq26=(float((ex < rho_eq).sum() / (len(ex) + kinds.get("no_peak_reduction", 0)))
                                                       if len(ex) + kinds.get("no_peak_reduction", 0) else None),
                                   upper_bound_values=";".join(f"{v:.4g}" for v in sorted(ub))))
    pd.DataFrame(q1).to_csv(out / "q1_conflict.csv", index=False)
    pd.DataFrame(q2).to_csv(out / "q2_break_even.csv", index=False)

    # ---- Q6 computation, by W x CV
    q6 = []
    for key, g in live.groupby(["w_target", "cv"]):
        q6.append(dict(w_target=key[0], cv=key[1], n=len(g), front_complete=int(g.front_complete.sum()),
                       required_proven=f"{int(g.required_proven.sum())}/{int(g.required_solves.sum())}",
                       A_optimal=int(g.a_ok.sum()), B_optimal=int(g.b_ok.sum()), Bmin_optimal=int(g.bmin_ok.sum()),
                       C14_optimal=int(g.c14_proven.sum()), C14_primary_proven=int(g.c14_primary_proven.sum()),
                       cpu_s_mean=float(g.task_cpu_s.mean()), cpu_s_median=float(g.task_cpu_s.median()),
                       cpu_s_max=float(g.task_cpu_s.max())))
    pd.DataFrame(q6).to_csv(out / "q6_computation.csv", index=False)
    grid_rows = pr[pr.grid == True]  # noqa: E712
    gaps = pd.to_numeric(grid_rows.get("guard_gap"), errors="coerce")

    # ---- cross-check (front vs direct C at 14) and exact-vs-all divergence (section 7)
    div = []
    for label in RHOS:
        t = pr[pr.rho == label]
        for key, g in t.groupby(STRATA):
            a = g[g.sav_B_valid].sav_B_pct.mean()
            b = g[g.ach_B_valid].ach_B_pct.mean()
            u = g[g.ub_B_valid].ub_B_pct.mean() if label in GRID else float("nan")
            div.append(dict(rho=label, gamma=key[0], w_target=key[1], cv=key[2], exact_mean=a, achieved_all_mean=b,
                            ub_all_mean=u, max_abs_diff=max(abs(a - b) if a == a and b == b else 0,
                                                            abs(a - u) if a == a and u == u else 0)))
    dv = pd.DataFrame(div)
    dv.to_csv(out / "exact_vs_all.csv", index=False)

    n = len(live)
    head = sm[(sm.rho == HEADLINE_RHO) & (sm.grouping == "all")]
    s3 = {}
    for sname, sub, _ in subsets(block, pr):
        t = sub[(sub.rho == HEADLINE_RHO) & sub.opt_valid]
        s3[sname] = dict(n=len(t), share_best_rule_within_1pct=float((t.opt_value_pct < 1).mean()) if len(t) else None)
    return dict(
        block=block, design=dname, digest=design.digest(), instances_expected=len(tasks), instances_present=len(present),
        instances_missing=missing, front_complete=int(live.front_complete.sum()), front_complete_share=float(live.front_complete.mean()),
        intervals_valid=design.seeds_per_cell >= MIN_SEEDS_FOR_INTERVALS,
        m4_exact_claim_allowed=not block.startswith("m4") or float(live.front_complete.mean()) >= 0.90,
        statuses=dict(A=int(live.a_ok.sum()), B=int(live.b_ok.sum()), B_minpeak=int(live.bmin_ok.sum()),
                      C14=int(live.c14_proven.sum()), C14_primary=int(live.c14_primary_proven.sum()), n=n),
        guard_optimal_grid=f"{int((grid_rows.get('guard_status') == 'OPTIMAL').sum())}/{len(grid_rows)}",
        guard_gap_max_pct=None if gaps is None or gaps.isna().all() else float(gaps.max() * 100),
        guard_gap_positive=int((gaps > 0).sum()) if gaps is not None else 0,
        cross_check=dict(comparable=int(live.cross_comparable.sum()), equal=int(live.cross_equal.sum())),
        exact_vs_all_max_cell_diff_pp=float(dv.max_abs_diff.max()) if len(dv) else None,
        s3_at_eq26=s3, rho_eq_inr={k: str(v[2]) for k, v in EQ.items()},
        cpu_s=dict(total=float(live.task_cpu_s.sum()), mean=float(live.task_cpu_s.mean()),
                   median=float(live.task_cpu_s.median()), max=float(live.task_cpu_s.max())),
        headline_eq26={f"{r.subset}:{r.estimand}": dict(mean=r.get("mean_of_cell_means"), ci=[r.get("ci_lo"), r.get("ci_hi")],
                                                        n_valid=r.n_valid, n_total=r.n_total)
                       for _, r in head.iterrows()},
    )


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--blocks", nargs="+", default=["m3", "m4"], choices=sorted(BLOCKS))
    ap.add_argument("--n-boot", type=int, default=2000)
    ap.add_argument("--results", type=Path, default=ROOT / "results")
    ap.add_argument("--out", type=Path, default=ROOT / "results/main_analysis")
    a = ap.parse_args(argv)
    problems = Problems()
    res = {b: analyse_block(b, a.n_boot, problems, a.results, a.out) for b in a.blocks}
    if {"m3", "m4"} <= set(a.blocks):                      # section 9: side by side at the shared settings only
        rows = []
        for b in ("m3", "m4"):
            pr = pd.read_csv(a.out / b / "per_rho.csv", dtype={"gamma": str, "w_target": str, "cv": str})
            t = pr[(pr.gamma == "19/14") & pr.w_target.isin(["0.40", "0.55"]) & pr.cv.isin(["0", "0.35"])
                   & pr.rho.isin(["14", HEADLINE_RHO])]
            for key, g in t.groupby(["rho", "w_target", "cv"]):
                v = g[g.sav_B_valid == True].sav_B_pct  # noqa: E712
                rows.append(dict(block=b, rho=key[0], w_target=key[1], cv=key[2], n=len(g), n_valid=len(v),
                                 sav_B_mean=float(v.mean()) if len(v) else None,
                                 sav_B_median=float(v.median()) if len(v) else None,
                                 share_gt_0=float((v > 1e-12).mean()) if len(v) else None))
        pd.DataFrame(rows).to_csv(a.out / "m3_vs_m4_shared.csv", index=False)
    summary = dict(blocks=res, problems=problems, n_boot=a.n_boot, bill_label=PARTIAL_BILL_LABEL)
    out = a.out
    (out / "summary.json").write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    (out / "README.txt").write_text(
        "SPEC-003 main study analysis (07_src/scripts/main_report.py). Exact values and bounds are never pooled;\n"
        "exclusions are counted by reason. Intervals: stratified cluster bootstrap, 95 % percentile, descriptive of\n"
        "generator sampling only; no significance tests. Bills: " + PARTIAL_BILL_LABEL + " (demand charge + energy of\n"
        "the scheduled shift only; both contract-demand scenarios shown). Blocks M3 and M4 are never pooled.\n",
        encoding="utf-8")
    print(json.dumps({b: dict(front_complete=r["front_complete"], instances=r["instances_present"],
                              missing=len(r["instances_missing"]), cross_check=r["cross_check"],
                              s3=r["s3_at_eq26"]) for b, r in res.items()}, indent=1))
    print(f"problems: {len(problems)}")
    for p in problems[:30]:
        print("  " + p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
