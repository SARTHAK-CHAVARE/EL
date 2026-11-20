"""Generate tables and figures from a results directory.

    python 07_src/analysis/report.py --results results/smoke [--out results/smoke/analysis] [--validated]

Every figure/table is stamped PRELIMINARY unless ``--validated`` is given *and* the run used the full
design; a smoke design can never be stamped validated.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from experiments.design import DESIGN_FULL  # noqa: E402
from analysis.tables import (MIN_SEEDS_FOR_INTERVALS, AnalysisError, coverage_table, load_results, paired_table,  # noqa: E402
                             rho_star_pair_table, runtime_table, status_table, summary_by)


def _stamp(fig, label: str) -> None:
    fig.text(0.99, 0.01, label, ha="right", va="bottom", fontsize=8, color="#b00020")


def fig_saving_vs_rho(t, out: Path, label: str, intervals: bool = True):
    s = summary_by(t, ["gamma", "rho_inr"], intervals=intervals)
    fig, ax = plt.subplots(figsize=(6.5, 4))
    for g, d in s.groupby("gamma"):
        d = d.sort_values("rho_inr")
        if "ci_lo" in d.columns:
            ax.errorbar(d.rho_inr, d["mean"], yerr=[d["mean"] - d.ci_lo, d.ci_hi - d["mean"]], marker="o", capsize=3,
                        label=f"gamma={g}")
        else:                                           # descriptive only: no interval is drawn
            ax.plot(d.rho_inr, d["mean"], marker="o", label=f"gamma={g}")
    ax.set(xlabel="demand-charge intensity rho (INR/kW per horizon)", ylabel="mean TEC saving of C vs B (%)",
           title="Cost saving of peak-aware (C) over energy-only (B)")
    ax.axhline(0, color="k", lw=0.5); ax.legend(); _stamp(fig, label)
    fig.tight_layout(); fig.savefig(out / "fig_saving_vs_rho.png", dpi=150); plt.close(fig)


def fig_tradeoff(t, out: Path, label: str):
    v = t[t.full_valid]
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    sc = ax.scatter(v.energy_increase_pct, v.peak_reduction_pct, c=v.rho_inr, cmap="viridis", s=14)
    fig.colorbar(sc, label="rho (INR/kW)")
    ax.set(xlabel="energy-cost increase of C vs B (%)", ylabel="peak reduction of C vs B (%)",
           title="Energy-cost vs peak trade-off (each point = instance x rho)")
    _stamp(fig, label); fig.tight_layout(); fig.savefig(out / "fig_tradeoff_energy_peak.png", dpi=150); plt.close(fig)
    v2 = t[t.full_valid]
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    ax.scatter(v2.makespan_penalty_pct, v2.saving_pct, c=v2.rho_inr, cmap="viridis", s=14)
    ax.set(xlabel="makespan penalty of C vs B (%)", ylabel="TEC saving (%)", title="Makespan penalty vs saving")
    _stamp(fig, label); fig.tight_layout(); fig.savefig(out / "fig_tradeoff_makespan_saving.png", dpi=150); plt.close(fig)


def fig_peaks(t, out: Path, label: str):
    v = t[t.rho_inr == t.rho_inr.min()]
    cols = {"A": "peak_w_A", "B": "peak_w_B", "C": "peak_w_C", "FCFS": "peak_w_FCFS", "SPT": "peak_w_SPT"}
    # same instances for every bar: B, C and A fully proven and both heuristics produced a schedule
    v = v[v.full_valid & (v.status_A == "OPTIMAL") & v.peak_w_FCFS.notna() & v.peak_w_SPT.notna()]
    means = {k: v[c].mean() / 1000 for k, c in cols.items()}
    fig, ax = plt.subplots(figsize=(5.5, 3.8))
    ax.bar(list(means), list(means.values()))
    ax.set(ylabel="mean peak demand (kW)",
           title=f"Peak demand by strategy (C at rho={t.rho_inr.min():g}; n={len(v)} instances)")
    _stamp(fig, label); fig.tight_layout(); fig.savefig(out / "fig_peak_by_strategy.png", dpi=150); plt.close(fig)


def fig_breakeven(rs, out: Path, label: str):
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    for w, d in rs.groupby("w_target"):
        vals = d["rho_star_ub_B"].dropna().sort_values()
        if len(vals):
            ax.step(vals, [(i + 1) / len(vals) for i in range(len(vals))], where="post", label=f"W={w}")
    ax.set(xlabel="rho*_ub (INR/kW), UPPER BOUND on the break-even rho", ylabel="ECDF over instances with a possible peak reduction",
           title="Break-even demand charge (upper bound)")
    ax.legend(); _stamp(fig, label); fig.tight_layout(rect=(0, 0.04, 1, 1)); fig.savefig(out / "fig_breakeven_ecdf.png", dpi=150); plt.close(fig)


def _phase_panel(ax, fig, t, r, index: str, ylabel: str):
    """One heat-map panel. Every cell prints 'mean over valid rows' AND 'n_valid/n_total' so that cells resting on few
    (or no) proven rows are visible; excluded (unproven/missing) rows are not drawn as zero."""
    d = t[t.rho_inr == r]
    g = d[d.saving_valid].pivot_table(index=index, columns="w_target", values="saving_pct", aggfunc="mean")
    nv = d[d.saving_valid].pivot_table(index=index, columns="w_target", values="saving_pct", aggfunc="count")
    nt = d.pivot_table(index=index, columns="w_target", values="saving_pct", aggfunc="size")
    g = g.reindex(index=nt.index, columns=nt.columns)
    nv = nv.reindex(index=nt.index, columns=nt.columns).fillna(0).astype(int)
    im = ax.imshow(g.values.astype(float), aspect="auto", cmap="YlGn", vmin=0)
    ax.set_xticks(range(len(g.columns)), g.columns); ax.set_yticks(range(len(g.index)), g.index)
    ax.set(title=f"rho={r:g}", xlabel="nominal workload W", ylabel=ylabel)
    for i in range(g.shape[0]):
        for j in range(g.shape[1]):
            v = g.values[i, j]
            txt = "n/a" if v != v else f"{v:.1f}"
            ax.text(j, i, f"{txt}\n{nv.values[i, j]}/{nt.values[i, j]}", ha="center", va="center", fontsize=7)
    fig.colorbar(im, ax=ax, label="mean saving over valid rows (%)")


def fig_phase_maps(t, out: Path, label: str):
    """Mean saving heat maps (one panel per rho), cells annotated with n_valid/n_total (valid = proven comparison)."""
    rhos = sorted(t.rho_inr.unique())
    for index, ylabel, name in (("gamma", "gamma (peak/off-peak)", "fig_phase_map_gamma_W.png"),
                                ("cv", "power CV", "fig_phase_map_cv_W.png")):
        fig, axes = plt.subplots(1, len(rhos), figsize=(4.2 * len(rhos), 3.9), squeeze=False)
        for ax, r in zip(axes[0], rhos):
            _phase_panel(ax, fig, t, r, index, ylabel)
        _stamp(fig, label); fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(out / name, dpi=150); plt.close(fig)


def fig_runtime(df, out: Path, label: str):
    order = [s for s in ("A", "B", "B_minpeak", "B_maxpeak", "P", "C") if s in set(df.strategy)]
    data = [df[df.strategy == s].wall_time_s.values for s in order]
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    ax.boxplot(data, tick_labels=order); ax.set_yscale("log")
    ax.set(ylabel="solve wall time per strategy run (s, log)", title="Solver runtime by strategy (1 worker)")
    _stamp(fig, label); fig.tight_layout(); fig.savefig(out / "fig_runtime.png", dpi=150); plt.close(fig)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--results", required=True, type=Path, help="directory containing results.csv + manifest.json")
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--validated", action="store_true", help="drop the PRELIMINARY stamp (full design only)")
    a = ap.parse_args(argv)
    csv_path = a.results / "results.csv"
    if not csv_path.exists():
        print(f"error: {csv_path} not found (run the experiment first, or --aggregate-only)", file=sys.stderr)
        return 2
    mpath = a.results / "manifest.json"
    manifest = json.loads(mpath.read_text()) if mpath.exists() else {}
    design_name = manifest.get("design", {}).get("name", "unknown")
    if a.validated and (design_name != "full" or manifest.get("design_digest") != DESIGN_FULL.digest()):
        print("error: --validated is only allowed for the unmodified full design (405 instances); "
              "pilots (--seeds/--limit overrides) and smoke runs stay PRELIMINARY", file=sys.stderr)
        return 2
    try:
        df = load_results(csv_path, expected_digest=manifest.get("design_digest"))
    except AnalysisError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    expected = None
    seeds_per_cell = int(manifest.get("design", {}).get("seeds_per_cell", 0))
    intervals = seeds_per_cell >= MIN_SEEDS_FOR_INTERVALS       # False => descriptive only, no CIs anywhere
    if manifest.get("design"):
        d = dict(manifest["design"])
        expected = (len(d["gammas"]) * len(d["workloads"]) * len(d["cvs"]) * d["seeds_per_cell"])
    cov = coverage_table(df, expected)
    if a.validated and int(cov.missing_instances.iloc[0]) > 0:
        print(f"error: --validated requires a complete run ({int(cov.missing_instances.iloc[0])} instances missing)",
              file=sys.stderr)
        return 2
    label = "VALIDATED" if a.validated else f"PRELIMINARY (design={design_name}) - not a validated finding"
    if not intervals:
        label += f"; {seeds_per_cell} seed(s) per cell: DESCRIPTIVE ONLY, no intervals"
    out = a.out or a.results / "analysis"
    out.mkdir(parents=True, exist_ok=True)
    t = paired_table(df)
    rs = rho_star_pair_table(df)
    t.to_csv(out / "paired_instances.csv", index=False)
    rs.to_csv(out / "rho_star_upper_bound.csv", index=False)
    cov.to_csv(out / "coverage.csv", index=False)
    kw = dict(intervals=intervals)
    summary_by(t, ["gamma", "w_target", "cv", "rho_inr"], **kw).to_csv(out / "summary_saving_by_cell.csv", index=False)
    summary_by(t, ["w_target", "rho_inr"], **kw).to_csv(out / "summary_saving_by_W_rho.csv", index=False)
    summary_by(t, ["rho_inr"], **kw).to_csv(out / "summary_saving_by_rho.csv", index=False)
    summary_by(t, ["rho_inr"], value="saving_pct_vs_Bmin", valid="band_valid_Bmin", **kw).to_csv(
        out / "summary_saving_vs_Bminpeak_by_rho.csv", index=False)
    summary_by(t, ["rho_inr"], value="saving_pct_vs_Bmax", valid="band_valid_Bmax", **kw).to_csv(
        out / "summary_saving_vs_Bmaxpeak_by_rho.csv", index=False)
    summary_by(t, ["rho_inr"], value="peak_reduction_pct", valid="full_valid", **kw).to_csv(
        out / "summary_peak_reduction_by_rho.csv", index=False)
    summary_by(t, ["rho_inr"], value="makespan_penalty_pct", valid="full_valid", **kw).to_csv(
        out / "summary_makespan_penalty_by_rho.csv", index=False)
    runtime_table(df).to_csv(out / "runtime_by_strategy.csv")
    status_table(df).to_csv(out / "status_counts.csv", index=False)
    if t.saving_valid.any():
        fig_saving_vs_rho(t, out, label, intervals); fig_phase_maps(t, out, label)
    if t.full_valid.any():
        fig_tradeoff(t, out, label); fig_peaks(t, out, label)
    if rs["rho_star_ub_B"].notna().any():
        fig_breakeven(rs, out, label)
    fig_runtime(df, out, label)
    (out / "README.txt").write_text(
        f"{label}\ninstances present/expected: {int(cov.present_instances.iloc[0])}/"
        f"{int(cov.expected_instances.iloc[0])}\nrows in paired table (instance x rho): {len(t)}  "
        f"saving_valid: {int(t.saving_valid.sum())}  full_valid: {int(t.full_valid.sum())}  "
        f"band_valid_Bmin: {int(t.band_valid_Bmin.sum())}  band_valid_Bmax: {int(t.band_valid_Bmax.sum())}\n"
        f"Excluded rows are counted in every summary_* table (n_missing / n_unproven / n_excluded).\n"
        + ("CIs: stratified cluster bootstrap (instances resampled within gamma x W x CV cells).\n" if intervals else
           f"NO intervals: {seeds_per_cell} seed(s) per cell is below {MIN_SEEDS_FOR_INTERVALS}; all numbers are descriptive.\n") +
        f"rho_star_ub_* is an UPPER BOUND on the smallest rho at which peak-aware C beats energy-only.\n")
    print(f"wrote analysis to {out}  [{label}]  saving_valid={int(t.saving_valid.sum())}/{len(t)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
