"""Calibration analysis E1-E5 for the cal2 design (docs/handoff/SPEC-002-v2-proposal.md section 3).

    python 07_src/analysis/calibration_report.py --results results/cal2 [--out results/cal2/calibration]

STRICTLY DESCRIPTIVE. A calibration run has 2 seeds per generation cell, which supports counts and shares but no
intervals, tests or effect sizes: this module therefore emits none (no CI columns, no p-values), and every output is
stamped so. Everything reuses the validity rules of ``analysis.tables`` (B/C/P proof requirements; missing and
unproven results are counted, never dropped). Nominal workload (``w_target``) and realised workload (``w_real``) are
reported side by side in every workload table.

Pre-stated criteria (fixed before cal2 was run):
* conflict indicator: ``state_B == ok`` (a peak reduction between the energy-only schedule B and the min-peak
  extreme P exists). ``no_peak_reduction_possible`` = no conflict. ``unproven``/``missing`` = undetermined (counted).
* E3 sub-threshold regime "captured": the share of conflict instances with a strictly positive saving at the lowest
  rho is at least SUBTHRESHOLD_MARGIN (0.25) below that share at rho = INR 5.
* Prediction (a): conflict share at the highest W <= at the lowest W, with 0 adjacent increases -> "held";
  <= with increases -> "held_non_monotone"; otherwise "not_held".
* Prediction (b): pooled conflict share among CV > 0 instances <= PRED_B_MAX_SHARE (0.10) -> "held".
* Prediction (c): sub-threshold criterion above.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from analysis.tables import (INSTANCE_COLS, AnalysisError, load_results, paired_table,  # noqa: E402
                             rho_star_pair_table)

SUBTHRESHOLD_MARGIN = 0.25
PRED_B_MAX_SHARE = 0.10
RHO_REFERENCE_INR = 5.0
RHO_FREE_STRATEGIES = ("A", "B", "B_minpeak", "B_maxpeak", "P", "FCFS", "SPT")
STAMP = "CALIBRATION - n=2 per cell, DESCRIPTIVE ONLY (no intervals/tests); not a validated finding"


# =============================================================================== tables
def instance_table(df: pd.DataFrame, t: pd.DataFrame, rs: pd.DataFrame) -> pd.DataFrame:
    """One row per instance: nominal W, realised W, conflict indicator, saving at every rho."""
    cols = INSTANCE_COLS + (["gen_attempts"] if "gen_attempts" in df.columns else [])
    inst = df.drop_duplicates("instance_id")[cols].copy()
    st = rs.set_index("instance_id")[["state_B", "state_Bminpeak", "rho_star_ub_B", "rho_star_ub_Bminpeak"]]
    inst = inst.merge(st, left_on="instance_id", right_index=True, how="left")
    inst["state_B"] = inst["state_B"].fillna("missing")
    inst["conflict"] = inst.state_B.map(lambda s: "conflict" if s == "ok" else
                                        "none" if s == "no_peak_reduction_possible" else "undetermined")
    inst["w_diff"] = inst.w_real - inst.w_target.astype(float)
    for r, g in t.groupby("rho_inr"):
        g = g.set_index("instance_id")
        inst[f"saving_pct_rho{r:g}"] = inst.instance_id.map(g.saving_pct)
        inst[f"saving_valid_rho{r:g}"] = inst.instance_id.map(g.saving_valid).fillna(False).astype(bool)
    return inst


def _w_cols(g: pd.DataFrame) -> Dict[str, float]:
    return dict(w_real_mean=float(g.w_real.mean()), w_real_min=float(g.w_real.min()), w_real_max=float(g.w_real.max()))


def e1_conflict(inst: pd.DataFrame, by: Sequence[str]) -> pd.DataFrame:
    """Counts and share of instances with a possible peak reduction. Share is over determined instances only."""
    rows = []
    for key, g in inst.groupby(list(by)):
        key = key if isinstance(key, tuple) else (key,)
        k, n0, nu = (int((g.conflict == c).sum()) for c in ("conflict", "none", "undetermined"))
        rows.append(dict(zip(by, key), n_instances=len(g), n_conflict=k, n_no_conflict=n0, n_undetermined=nu,
                         share_conflict=(k / (k + n0)) if (k + n0) else float("nan"),
                         **(_w_cols(g) if "w_target" in by else {})))
    out = pd.DataFrame(rows)
    return out.sort_values(list(by), key=lambda c: c.astype(float) if c.name == "w_target" else c).reset_index(drop=True)


def e2_replicates(inst: pd.DataFrame) -> pd.DataFrame:
    """Per generation cell: do the two seeds agree on the conflict indicator?"""
    rows = []
    for (g_, w_, c_), g in inst.groupby(["gamma", "w_target", "cv"]):
        g = g.sort_values("seed_idx")
        lab = list(g.conflict)
        if len(lab) < 2:
            cat = "incomplete"
        elif "undetermined" in lab:
            cat = "undetermined"
        elif len(set(lab)) == 1:
            cat = "both_conflict" if lab[0] == "conflict" else "both_none"
        else:
            cat = "disagree"
        rec = dict(gamma=g_, w_target=w_, cv=c_, n_seeds=len(g), category=cat, outcomes="|".join(lab),
                   w_real_seeds="|".join(f"{x:.4f}" for x in g.w_real))
        for col in [c for c in g.columns if c.startswith("saving_pct_rho")]:
            rec[col + "_by_seed"] = "|".join("" if pd.isna(v) else f"{v:.2f}" for v in g[col])
        rows.append(rec)
    return pd.DataFrame(rows).sort_values(["w_target", "gamma", "cv"], key=lambda c: c.astype(float) if c.name == "w_target" else c).reset_index(drop=True)


def e2_agreement_by_w(cells: pd.DataFrame) -> pd.DataFrame:
    cats = ["both_conflict", "both_none", "disagree", "undetermined", "incomplete"]
    rows = []
    for w_, g in cells.groupby("w_target"):
        cnt = {c: int((g.category == c).sum()) for c in cats}
        det = cnt["both_conflict"] + cnt["both_none"] + cnt["disagree"]
        rows.append(dict(w_target=w_, n_cells=len(g), **cnt, n_determined_cells=det,
                         agreement_share=((cnt["both_conflict"] + cnt["both_none"]) / det) if det else float("nan")))
    tot = {c: int((cells.category == c).sum()) for c in cats}
    det = tot["both_conflict"] + tot["both_none"] + tot["disagree"]
    rows.append(dict(w_target="ALL", n_cells=len(cells), **tot, n_determined_cells=det,
                     agreement_share=((tot["both_conflict"] + tot["both_none"]) / det) if det else float("nan")))
    out = pd.DataFrame(rows)
    return out.sort_values("w_target", key=lambda c: c.map(lambda x: 9.0 if x == "ALL" else float(x))).reset_index(drop=True)


def e3_saving(t: pd.DataFrame, by: Sequence[str], conflict_ids: Optional[set] = None) -> pd.DataFrame:
    """Descriptive saving of C vs B: counts of valid / positive / zero rows and the mean over valid rows."""
    d = t if conflict_ids is None else t[t.instance_id.isin(conflict_ids)]
    cols = list(by) + ["n_rows", "n_valid", "n_positive", "n_zero", "n_missing", "n_unproven", "share_positive",
                       "mean_saving_pct", "max_saving_pct"] + (["w_real_mean", "w_real_min", "w_real_max"] if "w_target" in by else [])
    if d.empty:
        return pd.DataFrame(columns=cols)
    rows = []
    for key, g in d.groupby(list(by)):
        key = key if isinstance(key, tuple) else (key,)
        v = g[g.saving_valid]
        pos = int((v.saving_pct > 0).sum())
        rows.append(dict(zip(by, key), n_rows=len(g), n_valid=len(v), n_positive=pos,
                         n_zero=int((v.saving_pct == 0).sum()), n_missing=int((g.excl_reason_saving == "missing").sum()),
                         n_unproven=int((g.excl_reason_saving == "unproven").sum()),
                         share_positive=(pos / len(v)) if len(v) else float("nan"),
                         mean_saving_pct=float(v.saving_pct.mean()) if len(v) else float("nan"),
                         max_saving_pct=float(v.saving_pct.max()) if len(v) else float("nan"),
                         **(_w_cols(g.drop_duplicates("instance_id")) if "w_target" in by else {})))
    return pd.DataFrame(rows).sort_values(list(by), key=lambda c: c.astype(float) if c.name in ("w_target", "cv") else c).reset_index(drop=True)


def subthreshold_check(conflict_by_rho: pd.DataFrame) -> Dict[str, object]:
    if conflict_by_rho.empty:
        return dict(captured=None, reason="no instance with a determinable peak-reduction conflict")
    d = conflict_by_rho.set_index("rho_inr")
    lo, ref = float(d.index.min()), RHO_REFERENCE_INR
    if ref not in d.index or lo == ref:
        return dict(captured=None, reason="reference or lowest rho level missing", lowest_rho=lo)
    s_lo, s_ref = d.loc[lo, "share_positive"], d.loc[ref, "share_positive"]
    if pd.isna(s_lo) or pd.isna(s_ref):
        return dict(captured=None, reason="share undefined (no valid conflict rows)", lowest_rho=lo)
    return dict(captured=bool(s_lo <= s_ref - SUBTHRESHOLD_MARGIN), lowest_rho=lo, reference_rho=ref,
                share_positive_lowest=float(s_lo), share_positive_reference=float(s_ref), margin=SUBTHRESHOLD_MARGIN)


def breakeven_tables(inst: pd.DataFrame, rho_levels: Sequence[float]):
    """rho*_ub (UPPER BOUND on the smallest rho at which C beats energy-only) for conflict instances."""
    c = inst[inst.conflict == "conflict"][["instance_id", "gamma", "w_target", "w_real", "cv", "seed_idx",
                                           "rho_star_ub_B", "rho_star_ub_Bminpeak"]].copy()
    def summ(g, label):
        v = g.rho_star_ub_B.dropna().values
        rec = dict(group=label, n=len(v))
        if len(v):
            rec.update(min=v.min(), q25=np.percentile(v, 25), median=np.median(v), q75=np.percentile(v, 75), max=v.max())
            for r in rho_levels:
                rec[f"n_with_ub<=rho{r:g}"] = int((v <= r).sum())
        return rec
    rows = [summ(c, "ALL")] + [summ(g, f"W={w}") for w, g in c.groupby("w_target")]
    return c, pd.DataFrame(rows)


def e4_tables(df: pd.DataFrame, t: pd.DataFrame, expected_ids: Sequence[str], rho_paise_levels: Sequence[int]):
    status = df.groupby(["strategy", "status", "proven_stages", "n_stages"], dropna=False).size().rename("n").reset_index()
    c = df[df.strategy == "C"].copy()
    c["rho_inr"] = c.rho_paise / 100.0
    c["stage1_proven"] = c.proven_stages >= 1
    c["fully_proven"] = c.status == "OPTIMAL"
    proof = (c.groupby(["w_target", "rho_inr"]).agg(rows=("status", "size"), fully_proven=("fully_proven", "sum"),
             stage1_proven=("stage1_proven", "sum"), feasible_only=("status", lambda s: int((s == "FEASIBLE").sum())),
             unknown=("status", lambda s: int((s == "UNKNOWN").sum())), mean_wall_s=("wall_time_s", "mean"),
             max_wall_s=("wall_time_s", "max")).reset_index())
    proof["stage1_unproven"] = proof.rows - proof.stage1_proven
    proof["tiebreak_unproven"] = proof.stage1_proven - proof.fully_proven
    proof = proof.sort_values(["w_target", "rho_inr"], key=lambda s: s.astype(float)).reset_index(drop=True)
    exp_rows = {(i, s, 0) for i in expected_ids for s in RHO_FREE_STRATEGIES}
    exp_rows |= {(i, "C", int(r)) for i in expected_ids for r in rho_paise_levels}
    got = set(zip(df.instance_id, df.strategy, df.rho_paise.astype(int)))
    acc = dict(expected_instances=len(set(expected_ids)), present_instances=df.instance_id.nunique(),
               missing_instances=len(set(expected_ids) - set(df.instance_id)), expected_rows=len(exp_rows),
               present_rows=len(got & exp_rows), missing_rows=len(exp_rows - got), unexpected_rows=len(got - exp_rows),
               duplicate_rows=int(len(df) - len(got)))
    excl = []
    for flag, rc in (("saving_valid", "excl_reason_saving"), ("full_valid", "excl_reason_full"),
                     ("band_valid_Bmin", "excl_reason_Bmin"), ("band_valid_Bmax", "excl_reason_Bmax")):
        excl.append(dict(flag=flag, n_rows=len(t), n_valid=int(t[flag].sum()), n_missing=int((t[rc] == "missing").sum()),
                         n_unproven=int((t[rc] == "unproven").sum())))
    return status, proof, pd.DataFrame([acc]), pd.DataFrame(excl)


def runtime_tables(df: pd.DataFrame):
    by_s = df.groupby("strategy").wall_time_s.describe(percentiles=[.5, .95])[["count", "mean", "50%", "95%", "max"]]
    c = df[df.strategy == "C"].copy()
    c["rho_inr"] = c.rho_paise / 100.0
    c_by = c.groupby(["w_target", "rho_inr"]).wall_time_s.agg(["count", "mean", "median", "max"]).reset_index()
    tot = df.groupby("instance_id").agg(w_target=("w_target", "first"), cpu_s=("wall_time_s", "sum"))
    per_w = tot.groupby("w_target").cpu_s.agg(["count", "mean", "median", "max", "sum"]).reset_index()
    allrow = pd.DataFrame([dict(w_target="ALL", count=len(tot), mean=tot.cpu_s.mean(), median=tot.cpu_s.median(),
                                max=tot.cpu_s.max(), sum=tot.cpu_s.sum())])
    return by_s, c_by, pd.concat([per_w, allrow], ignore_index=True)


def acceptance_table(inst: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for w_, g in inst.groupby("w_target"):
        rec = dict(w_target=w_, n_instances=len(g), **_w_cols(g), max_abs_w_diff=float(g.w_diff.abs().max()),
                   mean_w_diff=float(g.w_diff.mean()))
        if "gen_attempts" in g.columns:
            rec.update(mean_attempts=float(g.gen_attempts.mean()), n_first_draw=int((g.gen_attempts == 1).sum()),
                       max_attempts=int(g.gen_attempts.max()),
                       draws_per_instance_accept_rate=float(len(g) / g.gen_attempts.sum()))
        rows.append(rec)
    return pd.DataFrame(rows).sort_values("w_target", key=lambda c: c.astype(float)).reset_index(drop=True)


# =============================================================================== E5 and predictions
def transition(share_by_w: pd.Series) -> Dict[str, object]:
    """Descriptive reading of the conflict-share curve (index = nominal W as str, values in [0,1] or NaN)."""
    s = share_by_w.dropna()
    s.index = s.index.astype(float)
    s = s.sort_index()
    if s.empty:
        return dict(determined=False)
    inc = [(float(a), float(b)) for a, b, x, y in zip(s.index[:-1], s.index[1:], s.values[:-1], s.values[1:]) if y > x]
    pos = s[s > 0]
    zero = s[s == 0]
    return dict(determined=True, shares={f"{k:g}": float(v) for k, v in s.items()}, adjacent_increases=inc,
                monotone_non_increasing=not inc, highest_W_with_conflict=float(pos.index.max()) if len(pos) else None,
                lowest_W_with_zero_share=float(zero.index.min()) if len(zero) else None,
                max_share=float(s.max()))


def suggest_levels(share_by_w: pd.Series, targets=(1.0, 0.5, 0.25, 0.0)) -> Dict[str, object]:
    """Rule E5: observed W nearest to the high / 50 % / 25 % / zero points of the curve (levels may coincide).
    Guidance only: with 5 W levels and 2 seeds the curve is coarse; coincident targets mean 'refine between'."""
    s = share_by_w.dropna().copy()
    s.index = s.index.astype(float)
    s = s.sort_index()
    if s.empty or s.max() == 0:
        return dict(levels=[], note="no conflict observed at any W")
    smax = s.max()
    picks = []
    for k, tg in enumerate(targets):
        want = tg * smax
        d = (s - want).abs()
        best = d[d == d.min()].index
        picks.append(float(best.max() if k == 0 else best.min()))   # edge of the plateau / edge of the null region
    levels = list(dict.fromkeys(picks))
    return dict(levels=levels, targets_share=[round(tg * smax, 4) for tg in targets], picks=picks,
                n_distinct=len(levels), note=("targets coincide on the coarse grid: refine between the neighbouring "
                                              "levels" if len(levels) < len(targets) else "all targets distinct"))


def predictions(by_w: pd.DataFrame, inst: pd.DataFrame, sub: Dict[str, object]) -> pd.DataFrame:
    s = by_w.set_index("w_target").share_conflict
    tr = transition(s)
    rows = []
    if tr.get("determined"):
        shares = list(tr["shares"].values())
        if shares[-1] <= shares[0]:
            a = "held" if not tr["adjacent_increases"] else "held_non_monotone"
        else:
            a = "not_held"
        rows.append(dict(prediction="(a) conflict share decreases with W", status=a,
                         observed=f"shares by W {tr['shares']}; adjacent increases {tr['adjacent_increases']}"))
    else:
        rows.append(dict(prediction="(a) conflict share decreases with W", status="undetermined", observed="no data"))
    cvp = inst[inst.cv.astype(float) > 0]
    k, n0 = int((cvp.conflict == "conflict").sum()), int((cvp.conflict == "none").sum())
    share = k / (k + n0) if (k + n0) else float("nan")
    rows.append(dict(prediction=f"(b) conflict share among CV>0 <= {PRED_B_MAX_SHARE}",
                     status=("undetermined" if np.isnan(share) else "held" if share <= PRED_B_MAX_SHARE else "not_held"),
                     observed=f"{k} conflict of {k + n0} determined CV>0 instances (share {share:.3f})"))
    cap = sub.get("captured")
    rows.append(dict(prediction=f"(c) share with saving at lowest rho >= {SUBTHRESHOLD_MARGIN} below share at rho=5",
                     status="undetermined" if cap is None else "held" if cap else "not_held", observed=json.dumps(sub)))
    return pd.DataFrame(rows)


# =============================================================================== figures
C1, C2, C3 = "#2a78d6", "#eb6834", "#1baf7a"           # validated categorical slots 1-3 (light surface)
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e6e5e1"


def _style(ax):
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)
    ax.tick_params(colors=MUTED)


def _stamp(fig):
    fig.text(0.99, 0.005, STAMP, ha="right", va="bottom", fontsize=7, color="#b00020")


def fig_e1(by_w, by_wcv, out: Path):
    fig, ax = plt.subplots(figsize=(7.6, 4.6)); _style(ax)
    x = by_w.w_target.astype(float)
    for col, mk, (cv, g) in zip((C1, C2, C3), ("s", "^", "D"), by_wcv.groupby("cv")):
        g = g.sort_values("w_target", key=lambda s: s.astype(float))
        ax.plot(g.w_target.astype(float), g.share_conflict, color=col, lw=1.6, marker=mk, ms=6, label=f"CV = {cv}  (n=6 per W)")
    ax.plot(x, by_w.share_conflict, color=INK, lw=2.6, marker="o", ms=8, zorder=4, label="all CV  (k/n under each W)")
    ax.set(ylim=(-0.05, 1.08), xlim=(x.min() - 0.02, x.max() + 0.02),
           xlabel="nominal workload W   (second line: instances with possible peak reduction k / determined n, all CV)",
           ylabel="share of instances with possible peak reduction",
           title="E1: conflict indicator by nominal workload (18 instances per W)")
    ax.set_xticks(list(x), [f"{w}\n{r.n_conflict}/{r.n_conflict + r.n_no_conflict}" for w, r in zip(by_w.w_target, by_w.itertuples())])
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    _stamp(fig); fig.tight_layout(); fig.savefig(out / "fig_e1_conflict_by_W.png", dpi=150); plt.close(fig)


def fig_e2(agree, out: Path):
    a = agree[agree.w_target != "ALL"]
    fig, ax = plt.subplots(figsize=(7.2, 4.6)); _style(ax)
    layers = (("both_conflict", C1, "both seeds: conflict"), ("both_none", "#c9c8c2", "both seeds: none"),
              ("disagree", C2, "seeds disagree"), ("undetermined", "#ffffff", "undetermined (unproven)"))
    bottom = np.zeros(len(a))
    for key, col, lab in layers:
        v = a[key].values.astype(float)
        ax.bar(a.w_target.astype(str), v, bottom=bottom, color=col, edgecolor=(MUTED if key == "undetermined" else "#fcfcfb"),
               linewidth=[(1 if key == "undetermined" else 2) if h > 0 else 0 for h in v], label=lab, hatch="//" if key == "undetermined" else None, width=0.62)
        for i, (b, h) in enumerate(zip(bottom, v)):
            if h > 0:
                ax.text(i, b + h / 2, f"{int(h)}", ha="center", va="center", fontsize=8,
                        color="white" if key in ("both_conflict", "disagree") else INK)
        bottom += v
    ax.set(xlabel="nominal workload W", ylabel="generation cells (of 9 per W)",
           title="E2: replicate agreement on the conflict indicator (2 seeds per cell)")
    ax.legend(frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=4, columnspacing=2.2, handlelength=1.6)
    _stamp(fig)
    fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(out / "fig_e2_replicate_agreement.png", dpi=150); plt.close(fig)


def fig_e3(sav_w_rho, conflict_by_rho, out: Path):
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 4.5)); [_style(a) for a in (a1, a2)]
    ramp = ["#9ecae1", "#6baed6", "#4292c6", "#2171b5", "#08306b"]
    rhos = sorted(sav_w_rho.rho_inr.unique())
    for col, (w_, g) in zip(ramp, sav_w_rho.groupby("w_target", sort=False)):
        g = g.sort_values("rho_inr")
        a1.plot(g.rho_inr, g.mean_saving_pct, color=col, lw=2, marker="o", ms=6, label=f"W = {w_}")
    a1.set(xscale="log", xlabel="rho (INR/kW per horizon, log scale)", ylabel="mean saving of C vs B over valid rows (%)",
           title="E3: saving by rho and nominal W (all valid instances)")
    a1.set_xticks(rhos, [f"{r:g}" for r in rhos]); a1.minorticks_off()
    a1.legend(frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=5, columnspacing=1.0, handlelength=1.4)
    g = conflict_by_rho.sort_values("rho_inr") if not conflict_by_rho.empty else conflict_by_rho
    a2.bar(g.rho_inr.map(lambda r: f"{r:g}"), g.share_positive.fillna(0) if len(g) else [], color=C1, edgecolor="#fcfcfb", linewidth=2, width=0.6)
    for i, r in enumerate(g.itertuples()):
        a2.text(i, (0 if pd.isna(r.share_positive) else r.share_positive) + 0.02, f"{r.n_positive}/{r.n_valid}",
                ha="center", fontsize=8, color=INK)
    a2.set(ylim=(0, 1.12), xlabel="rho (INR/kW)", ylabel="share with strictly positive saving",
           title="E3: instances with a possible peak reduction (k/n valid)")
    _stamp(fig); fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(out / "fig_e3_saving_by_rho.png", dpi=150); plt.close(fig)


def fig_breakeven(be, rho_levels, out: Path, all_ws=None):
    if be.empty or be.rho_star_ub_B.notna().sum() == 0:
        return
    fig, ax = plt.subplots(figsize=(7.2, 4.2)); _style(ax)
    ws = sorted(set(be.w_target.unique()) | set(all_ws or []), key=float)
    rng = np.random.default_rng(3)
    for i, w_ in enumerate(ws):
        v = be[be.w_target == w_].rho_star_ub_B.dropna().values
        if not len(v):
            ax.text(i, 0.0, "no instance with a\npossible peak reduction", ha="center", va="bottom", fontsize=8, color=MUTED)
        ax.scatter(np.full(len(v), i) + rng.uniform(-0.12, 0.12, len(v)), v, s=36, color=C1, edgecolor="#fcfcfb", lw=1.5, zorder=3)
    for r in rho_levels:
        ax.axhline(r, color="#b0afa8", lw=0.8, ls="--"); ax.text(len(ws) - 0.45, r, f"rho={r:g}", fontsize=7, color=MUTED, va="bottom")
    ax.set_yscale("symlog", linthresh=1.0); ax.set_xticks(range(len(ws)), ws)
    ticks = [0.0] + [float(r) for r in rho_levels]
    ax.set_yticks(ticks, [f"{t:g}" for t in ticks]); ax.minorticks_off()
    ax.set(xlabel="nominal workload W", ylabel="rho*_ub (INR/kW)  [UPPER BOUND on break-even]", xlim=(-0.5, len(ws) - 0.3),
           title="E3: break-even upper bounds of instances with a possible peak reduction")
    _stamp(fig); fig.tight_layout(); fig.savefig(out / "fig_e3_breakeven_upper_bounds.png", dpi=150); plt.close(fig)


def fig_e4(proof, out: Path):
    g = proof.groupby("rho_inr")[["fully_proven", "tiebreak_unproven", "stage1_unproven"]].sum().reset_index()
    fig, ax = plt.subplots(figsize=(7.2, 4.6)); _style(ax)
    bottom = np.zeros(len(g))
    for key, col, lab in (("fully_proven", C1, "fully proven"), ("tiebreak_unproven", "#9ecae1", "cost proven, makespan tie-break not"),
                          ("stage1_unproven", C2, "cost (stage 1) unproven")):
        v = g[key].values.astype(float)
        ax.bar(g.rho_inr.map(lambda r: f"{r:g}"), v, bottom=bottom, color=col, edgecolor="#fcfcfb", linewidth=2, label=lab, width=0.62)
        for i, (b, h) in enumerate(zip(bottom, v)):
            if h > 0:
                ax.text(i, b + h / 2, f"{int(h)}", ha="center", va="center", fontsize=8, color="white" if col in (C1, C2) else INK)
        bottom += v
    ax.set(xlabel="rho (INR/kW)", ylabel="strategy-C rows",
           title=f"E4: proof status of strategy C by rho ({int(g[['fully_proven', 'tiebreak_unproven', 'stage1_unproven']].sum(axis=1).max())} instances)")
    ax.legend(frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=3, columnspacing=1.2, handlelength=1.4)
    _stamp(fig); fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(out / "fig_e4_C_proof_status_by_rho.png", dpi=150); plt.close(fig)


def fig_runtime(df, out: Path):
    c = df[df.strategy == "C"].copy(); c["rho_inr"] = c.rho_paise / 100.0
    rhos = sorted(c.rho_inr.unique())
    fig, ax = plt.subplots(figsize=(7.2, 4.0)); _style(ax)
    ax.boxplot([c[c.rho_inr == r].wall_time_s.clip(lower=0.05).values for r in rhos], tick_labels=[f"{r:g}" for r in rhos],
               boxprops=dict(color=C1), medianprops=dict(color=C2, lw=2), whiskerprops=dict(color=MUTED), capprops=dict(color=MUTED),
               flierprops=dict(marker="o", ms=4, markerfacecolor=MUTED, markeredgecolor="none"))
    ax.set(yscale="log", xlabel="rho (INR/kW)", ylabel="wall time per C solve (s, log)", title="Runtime of strategy C solves by rho (wall time per solve)")
    _stamp(fig); fig.tight_layout(); fig.savefig(out / "fig_runtime_C_by_rho.png", dpi=150); plt.close(fig)


def fig_workload(inst, out: Path):
    fig, ax = plt.subplots(figsize=(5.6, 4.6)); _style(ax)
    rng = np.random.default_rng(5)
    x = inst.w_target.astype(float).values
    ax.scatter(x + rng.uniform(-0.006, 0.006, len(x)), inst.w_real.values, s=22, color=C1, edgecolor="#fcfcfb", lw=1, zorder=3)
    lim = (x.min() - 0.03, x.max() + 0.03)
    ax.plot(lim, lim, color=MUTED, lw=1, ls="--"); ax.set(xlim=lim, ylim=lim, xlabel="nominal W", ylabel="realised w_real",
                                                          title="Nominal vs realised workload (dashed: identity)")
    _stamp(fig); fig.tight_layout(); fig.savefig(out / "fig_workload_nominal_vs_realised.png", dpi=150); plt.close(fig)


# =============================================================================== main
def build_all(df: pd.DataFrame, expected_ids: Optional[Sequence[str]] = None, rho_paise_levels: Optional[Sequence[int]] = None
              ) -> Dict[str, object]:
    t, rs = paired_table(df), rho_star_pair_table(df)
    inst = instance_table(df, t, rs)
    ids = list(expected_ids) if expected_ids is not None else list(inst.instance_id)
    rhos = list(rho_paise_levels) if rho_paise_levels is not None else sorted(int(r) for r in df[df.strategy == "C"].rho_paise.unique())
    by_w = e1_conflict(inst, ["w_target"])
    cells = e2_replicates(inst)
    conflict_ids = set(inst[inst.conflict == "conflict"].instance_id)
    conf_by_rho = e3_saving(t, ["rho_inr"], conflict_ids)
    sub = subthreshold_check(conf_by_rho)
    be_inst, be_sum = breakeven_tables(inst, [r / 100.0 for r in rhos])
    status, proof, acc, excl = e4_tables(df, t, ids, rhos)
    rt_s, rt_c, rt_i = runtime_tables(df)
    share = by_w.set_index("w_target").share_conflict
    return dict(t=t, rs=rs, inst=inst, e1_by_w=by_w, e1_by_w_cv=e1_conflict(inst, ["w_target", "cv"]),
                e1_by_w_gamma=e1_conflict(inst, ["w_target", "gamma"]), e2_cells=cells, e2_agree=e2_agreement_by_w(cells),
                e3_by_w_rho=e3_saving(t, ["w_target", "rho_inr"]), e3_by_rho=e3_saving(t, ["rho_inr"]),
                e3_conf_by_rho=conf_by_rho, e3_by_cv_rho=e3_saving(t, ["cv", "rho_inr"]),
                e3_by_gamma_rho=e3_saving(t, ["gamma", "rho_inr"]), e3_conf_by_w_rho=e3_saving(t, ["w_target", "rho_inr"], conflict_ids),
                subthreshold=sub, be_inst=be_inst, be_sum=be_sum, e4_status=status, e4_proof=proof, e4_accounting=acc,
                e4_excluded=excl, rt_strategy=rt_s, rt_c=rt_c, rt_instance=rt_i, acceptance=acceptance_table(inst),
                transition=transition(share), levels=suggest_levels(share), predictions=predictions(by_w, inst, sub),
                rho_levels=[r / 100.0 for r in rhos])


def write_outputs(res: Dict[str, object], df: pd.DataFrame, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    csvs = {"instance_table": "inst", "e1_conflict_by_W": "e1_by_w", "e1_conflict_by_W_CV": "e1_by_w_cv",
            "e1_conflict_by_W_gamma": "e1_by_w_gamma", "e2_replicate_cells": "e2_cells", "e2_replicate_agreement_by_W": "e2_agree",
            "e3_saving_by_W_rho": "e3_by_w_rho", "e3_saving_by_rho": "e3_by_rho",
            "e3_saving_conflict_instances_by_rho": "e3_conf_by_rho", "e3_saving_conflict_instances_by_W_rho": "e3_conf_by_w_rho",
            "e3_saving_by_CV_rho": "e3_by_cv_rho", "e3_saving_by_gamma_rho": "e3_by_gamma_rho",
            "e3_breakeven_upper_bounds_instances": "be_inst", "e3_breakeven_upper_bounds_summary": "be_sum",
            "e4_status_counts": "e4_status", "e4_C_proof_by_W_rho": "e4_proof", "e4_row_accounting": "e4_accounting",
            "e4_excluded_by_validity_flag": "e4_excluded", "runtime_by_strategy": "rt_strategy", "runtime_C_by_W_rho": "rt_c",
            "runtime_instance_cpu_by_W": "rt_instance", "generator_acceptance_and_workload_by_W": "acceptance",
            "e5_predictions": "predictions"}
    for name, key in csvs.items():
        res[key].to_csv(out / f"{name}.csv", index=key in ("rt_strategy",))
    res["acceptance"].to_csv(out / "workload_nominal_vs_realised.csv", index=False)
    (out / "e5_transition_and_levels.json").write_text(json.dumps(dict(
        transition=res["transition"], suggested_levels=res["levels"], subthreshold=res["subthreshold"],
        note="descriptive guidance from a coarse 5-level, 2-seed calibration; not an estimate with uncertainty"), indent=2, default=float))
    fig_e1(res["e1_by_w"], res["e1_by_w_cv"], out); fig_e2(res["e2_agree"], out)
    fig_e3(res["e3_by_w_rho"], res["e3_conf_by_rho"], out); fig_breakeven(res["be_inst"], res["rho_levels"], out, list(res["e1_by_w"].w_target))
    fig_e4(res["e4_proof"], out); fig_runtime(df, out); fig_workload(res["inst"], out)
    (out / "README.txt").write_text(
        STAMP + "\n\nAll numbers are counts, shares or means over a small design (2 seeds per generation cell). No confidence intervals, "
        "significance tests or effect sizes are produced. rho*_ub columns are UPPER BOUNDS on the smallest rho at which "
        "peak-aware C beats energy-only. Nominal W (w_target) and realised workload (w_real) are reported side by side. "
        "Excluded rows are counted (n_missing / n_unproven).\n")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--results", required=True, type=Path)
    ap.add_argument("--out", type=Path, default=None)
    a = ap.parse_args(argv)
    csv_path, mpath = a.results / "results.csv", a.results / "manifest.json"
    if not csv_path.exists() or not mpath.exists():
        print(f"error: {csv_path} or {mpath} not found (run the experiment first)", file=sys.stderr)
        return 2
    manifest = json.loads(mpath.read_text())
    try:
        df = load_results(csv_path, expected_digest=manifest.get("design_digest"))
    except AnalysisError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    from experiments.design import Design, enumerate_tasks
    from model import inr_to_paise
    d = {k: (tuple(v) if isinstance(v, list) else v) for k, v in manifest["design"].items()}
    design = Design(**d)
    ids = [t.instance_id for t in enumerate_tasks(design)]
    res = build_all(df, ids, [inr_to_paise(r) for r in design.rho_inr])
    out = a.out or a.results / "calibration"
    write_outputs(res, df, out)
    print(f"wrote calibration analysis to {out}  [{STAMP}]")
    print(res["e1_by_w"][["w_target", "w_real_mean", "n_instances", "n_conflict", "n_no_conflict", "n_undetermined", "share_conflict"]].to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
