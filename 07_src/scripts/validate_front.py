"""Gate 1 (ROADMAP-FINAL.md P1 / section 7.6): validate the energy-peak front against every applicable cal2 result.

    python 07_src/scripts/validate_front.py [--cal2 results/cal2] [--out results/front_validation] [--workers 2]

Regenerates each cal2 instance (deterministic generator, checked against the stored w_real and attempts), computes the
front with the cal2 solver budgets, and compares it with the stored direct solves. Nothing in results/cal2 is modified.
Resumable: instances with an existing parts/<id>.json are not re-solved.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from fractions import Fraction
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd  # noqa: E402

from analysis.tables import rho_star_pair_table  # noqa: E402
from experiments.design import DESIGN_CAL2, enumerate_tasks  # noqa: E402
from experiments.generator import generate_instance  # noqa: E402
from experiments.runner import _solver_config  # noqa: E402
from model import best_for_rho, break_even, ec_peak_front, rho_intervals, tec_lower_bound  # noqa: E402
from model.front import tec_int  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
RHO_PAISE = [100, 200, 500, 1400, 5000]


def _fs(x):
    return None if x is None else str(x)


def solve_one(args):
    task, refs, out = args
    path = out / "parts" / f"{task.instance_id}.json"
    if path.exists():
        return task.instance_id
    inst, meta = generate_instance(DESIGN_CAL2, task)
    f = ec_peak_front(inst, _solver_config(DESIGN_CAL2))
    iv = rho_intervals(f)
    rec = dict(
        instance_id=task.instance_id, w_real=meta.w_real, attempts=meta.attempts, complete=f.complete,
        termination=f.termination, reason=f.reason, n_solves=f.n_solves, wall_time_s=f.wall_time_s,
        solve_time_s=sum(sum(s.result.stage_times_s) for s in f.solves if not s.reused),
        lb_valid=f.lb_valid, n_dominated=len(f.dominated),
        solves=[dict(label=s.label, cap_w=s.cap_w, status=s.result.status.value,
                     stage_statuses=s.result.stage_statuses, time_s=sum(s.result.stage_times_s)) for s in f.solves],
        points=[dict(peak_w=p.peak_w, ec_int=p.ec_int, makespan=p.makespan, ec_proven=p.ec_proven,
                     peak_proven=p.peak_proven, makespan_proven=p.makespan_proven, source=p.source, cap_w=p.cap_w,
                     rho_interval=None if v is None else [_fs(v[0]), _fs(v[1])]) for p, v in zip(f.points, iv)],
    )
    for ref in ("B", "B_minpeak"):
        if refs.get(ref) is not None:
            ec, pk = refs[ref]
            be = break_even(f, ec, pk, ref)
            rec[f"be_{ref}"] = dict(rho_inr=_fs(be.rho_inr), kind=be.kind, via_peak_w=be.via_peak_w)
    rows = []
    for r in RHO_PAISE:
        c = best_for_rho(f, r)
        rows.append(dict(rho_paise=r, peak_w=c.peak_w if c else None, ec_int=c.ec_int if c else None,
                         makespan=c.makespan if c else None, makespan_proven=c.makespan_proven if c else None,
                         tec_int=tec_int(c.ec_int, c.peak_w, r) if c else None, tec_lb=tec_lower_bound(f, r)))
    rec["rho_rows"] = rows
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(rec, indent=1))
    tmp.replace(path)
    return task.instance_id


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cal2", type=Path, default=ROOT / "results/cal2")
    ap.add_argument("--out", type=Path, default=ROOT / "results/front_validation")
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--limit", type=int, default=None, help="solve only the first N instances (smoke test)")
    a = ap.parse_args(argv)
    df = pd.read_csv(a.cal2 / "results.csv", dtype={"w_target": str, "cv": str, "gamma": str})
    (a.out / "parts").mkdir(parents=True, exist_ok=True)
    tasks = enumerate_tasks(DESIGN_CAL2)
    by = {s: df[df.strategy == s].set_index("instance_id") for s in ("B", "B_minpeak", "P")}
    refs = {}
    for t in tasks:
        refs[t.instance_id] = {s: ((int(by[s].loc[t.instance_id, "ec_int"]), int(by[s].loc[t.instance_id, "peak_w"]))
                                   if by[s].loc[t.instance_id, "status"] in ("OPTIMAL", "FEASIBLE") else None)
                               for s in ("B", "B_minpeak")}
    todo = [(t, refs[t.instance_id], a.out) for t in tasks][: a.limit]
    with Pool(a.workers) as pool:
        for i, iid in enumerate(pool.imap_unordered(solve_one, todo), 1):
            print(f"[front] {i}/{len(todo)} {iid}", flush=True)
    return aggregate(df, a.out)


# =============================================================================================== aggregation
def aggregate(df: pd.DataFrame, out: Path) -> int:
    recs = [json.loads(p.read_text()) for p in sorted((out / "parts").glob("*.json"))]
    inst = df.drop_duplicates("instance_id").set_index("instance_id")
    S = {s: df[df.strategy == s].set_index("instance_id") for s in ("B", "B_minpeak", "P")}
    rs = rho_star_pair_table(df).set_index("instance_id")
    irows, rrows, problems = [], [], []
    for r in recs:
        iid = r["instance_id"]
        b, bm, p = S["B"].loc[iid], S["B_minpeak"].loc[iid], S["P"].loc[iid]
        pts = r["points"]
        top, bot = pts[0], pts[-1]
        same_inst = abs(r["w_real"] - inst.loc[iid, "w_real"]) < 1e-9 and r["attempts"] == inst.loc[iid, "gen_attempts"]
        if not same_inst:
            problems.append(f"{iid}: regenerated instance differs from cal2 (w_real/attempts)")
        c5 = df[(df.instance_id == iid) & (df.strategy == "C")]
        caps = [s for s in r["solves"] if s["label"] == "cap"]
        rec = dict(instance_id=iid, w_target=inst.loc[iid, "w_target"], w_real=r["w_real"], cv=inst.loc[iid, "cv"],
                   gamma=inst.loc[iid, "gamma"], same_instance=same_inst, complete=r["complete"],
                   termination=r["termination"], n_points=len(pts), n_dominated=r["n_dominated"],
                   n_solves=r["n_solves"], n_cap_solves=len(caps),
                   n_cap_unproven=sum(1 for s in caps if s["status"] not in ("OPTIMAL", "INFEASIBLE")),
                   front_time_s=r["solve_time_s"], direct_c5_time_s=float(c5.wall_time_s.sum()),
                   direct_p_time_s=float(p.wall_time_s), c5_all_proven=bool((c5.proven_stages >= 1).all()))
        # (1) top point vs energy-only B / B_minpeak (both proven)
        if b.status == "OPTIMAL" and top["ec_proven"]:
            rec["top_ec_eq_B"] = top["ec_int"] == int(b.ec_int)
            if not rec["top_ec_eq_B"]:
                problems.append(f"{iid}: front min EC {top['ec_int']} != cal2 B {int(b.ec_int)}")
        rec["top_peak_le_B"] = top["peak_w"] <= int(b.peak_w)
        rec["top_peak_le_Bmin"] = top["peak_w"] <= int(bm.peak_w) if bm.status in ("OPTIMAL", "FEASIBLE") else None
        if rec.get("top_ec_eq_B") and not rec["top_peak_le_B"]:
            problems.append(f"{iid}: front top peak above B's at equal EC")
        # (2) min-peak point vs cal2 P
        if r["complete"] and p.status == "OPTIMAL":
            rec["bottom_eq_P"] = (bot["peak_w"], bot["ec_int"]) == (int(p.peak_w), int(p.ec_int))
            if not rec["bottom_eq_P"]:
                problems.append(f"{iid}: min-peak point {bot['peak_w']},{bot['ec_int']} != cal2 P")
        # (3) break-even: exact vs cal2 upper bound
        for ref, col, stc in (("B", "rho_star_ub_B", "state_B"), ("B_minpeak", "rho_star_ub_Bminpeak", "state_Bminpeak")):
            be = r.get(f"be_{ref}")
            key = "B" if ref == "B" else "Bmin"
            rec[f"be_{key}_kind"] = be["kind"] if be else None
            rec[f"be_{key}_inr"] = float(Fraction(be["rho_inr"])) if be and be["rho_inr"] is not None else None
            rec[f"ub_{key}_state"] = rs.loc[iid, stc]
            ub = rs.loc[iid, col]
            rec[f"ub_{key}_inr"] = None if pd.isna(ub) else float(ub)
            if be and be["rho_inr"] is not None and rec[f"ub_{key}_inr"] is not None:
                ex = Fraction(be["rho_inr"])
                rec[f"be_{key}_le_ub"] = float(ex) <= rec[f"ub_{key}_inr"] + 1e-12
                rec[f"be_{key}_eq_ub"] = abs(float(ex) - rec[f"ub_{key}_inr"]) < 1e-9
                if not rec[f"be_{key}_le_ub"]:
                    problems.append(f"{iid}: exact break-even vs {ref} {float(ex)} above upper bound {rec[f'ub_{key}_inr']}")
        # (4) theorem: W > (M-1)/M => no peak reduction below B
        rec["theorem_applies"] = r["w_real"] > 2 / 3
        if rec["theorem_applies"] and any(q["peak_w"] < int(b.peak_w) for q in pts):
            problems.append(f"{iid}: theorem violated: front has a point below B's peak at w_real {r['w_real']}")
        irows.append(rec)
        # (5) C(rho) vs direct C
        cdir = c5.set_index("rho_paise")
        for row in r["rho_rows"]:
            rp = row["rho_paise"]
            d = cdir.loc[rp]
            rr = dict(instance_id=iid, w_target=rec["w_target"], cv=rec["cv"], gamma=rec["gamma"], rho_inr=rp / 100,
                      front_complete=r["complete"], front_tec=row["tec_int"], front_peak=row["peak_w"],
                      front_makespan=row["makespan"], front_makespan_proven=row["makespan_proven"],
                      front_tec_lb=row["tec_lb"], direct_status=d.status, direct_proven_stages=int(d.proven_stages),
                      direct_tec=int(d.tec_int) if pd.notna(d.tec_int) else None,
                      direct_makespan=int(d.makespan) if pd.notna(d.makespan) else None)
            if r["complete"] and d.proven_stages >= 1:
                rr["tec_match"] = row["tec_int"] == rr["direct_tec"]
                if not rr["tec_match"]:
                    problems.append(f"{iid} rho {rp/100}: TEC front {row['tec_int']} != direct {rr['direct_tec']}")
            if r["complete"] and d.status == "OPTIMAL" and row["makespan_proven"]:
                rr["makespan_match"] = row["makespan"] == rr["direct_makespan"]
                if not rr["makespan_match"]:
                    problems.append(f"{iid} rho {rp/100}: makespan front {row['makespan']} != direct {rr['direct_makespan']}")
            if d.proven_stages < 1 and rr["direct_tec"] is not None:
                rr["front_vs_unproven_direct_pct"] = (rr["direct_tec"] - row["tec_int"]) / rr["direct_tec"] * 100
            if row["tec_lb"] is not None and row["tec_int"]:
                rr["gap_pct"] = (row["tec_int"] - row["tec_lb"]) / row["tec_int"] * 100
            # (6) saving sign vs exact break-even (against B)
            be = r.get("be_B")
            if be and be["kind"] in ("exact", "no_peak_reduction") and b.status == "OPTIMAL" and d.proven_stages >= 1:
                saving = int(b.ec_int) + 60 * rp * int(b.peak_w) - rr["direct_tec"]
                predicted = be["rho_inr"] is not None and Fraction(rp, 100) > Fraction(be["rho_inr"])
                rr["sign_consistent"] = (saving > 0) == predicted
                if not rr["sign_consistent"]:
                    problems.append(f"{iid} rho {rp/100}: saving {saving} inconsistent with exact break-even {be['rho_inr']}")
            rrows.append(rr)
    it, rt = pd.DataFrame(irows), pd.DataFrame(rrows)
    it.to_csv(out / "instances.csv", index=False)
    rt.to_csv(out / "rho_rows.csv", index=False)

    def cnt(series):
        s = series.dropna()
        return dict(n=int(len(s)), true=int(s.astype(bool).sum()))
    ratio = (it.front_time_s / it.direct_c5_time_s).replace([float("inf")], float("nan")).dropna()
    abandon_base = it[it.c5_all_proven]
    cap_total = int(abandon_base.n_cap_solves.sum())
    cap_unproven = int(abandon_base.n_cap_unproven.sum())
    summary = dict(
        instances=len(it), same_instance=cnt(it.same_instance), complete=cnt(it.complete),
        termination=it.termination.value_counts().to_dict(), n_points=it.n_points.value_counts().sort_index().to_dict(),
        n_dominated_total=int(it.n_dominated.sum()),
        top_ec_eq_B=cnt(it.get("top_ec_eq_B", pd.Series(dtype=object))), top_peak_le_B=cnt(it.top_peak_le_B),
        bottom_eq_P=cnt(it.get("bottom_eq_P", pd.Series(dtype=object))),
        tec_match=cnt(rt.get("tec_match", pd.Series(dtype=object))),
        makespan_match=cnt(rt.get("makespan_match", pd.Series(dtype=object))),
        sign_consistent=cnt(rt.get("sign_consistent", pd.Series(dtype=object))),
        be_B_kind=it.be_B_kind.value_counts(dropna=False).to_dict(),
        be_B_le_ub=cnt(it.get("be_B_le_ub", pd.Series(dtype=object))), be_B_eq_ub=cnt(it.get("be_B_eq_ub", pd.Series(dtype=object))),
        be_Bmin_le_ub=cnt(it.get("be_Bmin_le_ub", pd.Series(dtype=object))),
        be_Bmin_eq_ub=cnt(it.get("be_Bmin_eq_ub", pd.Series(dtype=object))),
        theorem_instances=int(it.theorem_applies.sum()),
        unproven_direct_rows=int((rt.direct_proven_stages < 1).sum()),
        unproven_direct_rows_improved_by_front=int((rt.get("front_vs_unproven_direct_pct", pd.Series(dtype=float)) > 0).sum()),
        front_time_s=dict(total=float(it.front_time_s.sum()), median=float(it.front_time_s.median()),
                          max=float(it.front_time_s.max())),
        direct_c5_time_s=dict(total=float(it.direct_c5_time_s.sum()), median=float(it.direct_c5_time_s.median())),
        direct_c5_plus_p_time_s=float((it.direct_c5_time_s + it.direct_p_time_s).sum()),
        median_ratio_front_over_c5=float(statistics.median(ratio)) if len(ratio) else None,
        abandon_check=dict(cap_solves_on_instances_with_all_direct_C_proven=cap_total, unproven=cap_unproven,
                           share=(cap_unproven / cap_total) if cap_total else 0.0),
        problems=problems,
    )
    gate = dict(
        zero_tec_mismatch=summary["tec_match"]["n"] == summary["tec_match"]["true"],
        zero_makespan_mismatch=summary["makespan_match"]["n"] == summary["makespan_match"]["true"],
        no_problems=not problems,
        median_front_time_le_direct=summary["median_ratio_front_over_c5"] is not None and summary["median_ratio_front_over_c5"] <= 1,
        abandon_triggered=summary["abandon_check"]["share"] > 0.10,
    )
    gate["proceed"] = all(gate[k] for k in ("zero_tec_mismatch", "zero_makespan_mismatch", "no_problems",
                                            "median_front_time_le_direct")) and not gate["abandon_triggered"]
    summary["gate1"] = gate
    (out / "summary.json").write_text(json.dumps(summary, indent=2, default=str))
    (out / "README.txt").write_text(
        "Gate 1 validation of the energy-peak front (model/front.py) against results/cal2 (unchanged).\n"
        "instances.csv: one row per cal2 instance; rho_rows.csv: front-derived C vs direct C at the 5 cal2 rho levels;\n"
        "summary.json: counts and the gate decision (ROADMAP-FINAL.md section 7.6). Break-even values labelled 'exact'\n"
        "come from a complete front; cal2's rho_star_ub columns are UPPER BOUNDS (pair B or B_minpeak vs P).\n")
    print(json.dumps({k: summary[k] for k in ("instances", "complete", "tec_match", "makespan_match", "sign_consistent",
                                              "be_B_kind", "median_ratio_front_over_c5", "gate1")}, indent=1, default=str))
    print(f"problems: {len(problems)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
