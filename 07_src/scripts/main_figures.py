"""Figures for the report and slides, made only from results/main_analysis (07_src/scripts/main_report.py outputs).

    python 07_src/scripts/main_figures.py                      # M3 figures from results/main_analysis/m3
    python 07_src/scripts/main_figures.py --analysis DIR --block m3-smoke --out DIR   # (tests / development)

F1 saving of the peak-aware optimum over the energy-only optimum vs demand charge, one line per workload (95 % bootstrap band)
F2 exact break-even demand charge (ECDF) per workload, with the KERC-equivalent value
F3 where the saving vs FCFS comes from at the KERC-equivalent rho (complete chains only)
F4 partial monthly bill saving at the KERC-equivalent rho, contract demand renegotiated vs fixed
All figures use the exact set (complete fronts, proven B) of the CV <= 0.35 subset; n is printed on every figure.
Colours: workload = ordinal one-hue ramp (validated, dataviz validate_palette --ordinal); categories = validated categorical
slots (peak-aware blue, energy-only orange, as in the app).
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "07_src"))

W_RAMP = ["#86b6ef", "#3987e5", "#1c5cab", "#0d366b"]       # light -> dark = low -> high workload
BLUE, ORANGE, AQUA, GREY = "#2a78d6", "#eb6834", "#1baf7a", "#8a8984"
INK, INK2, GRID_C, SURFACE = "#1f1e1d", "#5f5e5a", "#e6e5e1", "#fcfcfb"
GRID_RHO = ["1", "2", "5", "14", "50"]


def _style(ax):
    ax.set_facecolor(SURFACE)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID_C)
    ax.tick_params(colors=INK2, labelsize=9)
    ax.grid(axis="y", color=GRID_C, lw=0.8)
    ax.set_axisbelow(True)


def _fig(w=7.2, h=4.0):
    fig, ax = plt.subplots(figsize=(w, h), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    _style(ax)
    return fig, ax


def _title(ax, title, sub):
    ax.set_title(title, loc="left", fontsize=11.5, color=INK, pad=22, fontweight="semibold")
    ax.text(0, 1.02, sub, transform=ax.transAxes, fontsize=8.5, color=INK2, va="bottom")


def f1_saving_vs_rho(sm, pr, rho_eq, out):
    t = sm[(sm.subset == "cv<=0.35") & (sm.grouping == "by_W") & (sm.estimand == "sav_B_pct") & sm.rho.isin(GRID_RHO)]
    fig, ax = _fig()
    ws = sorted(t.level.unique(), key=float)
    for i, w in enumerate(ws):
        g = t[t.level == w].assign(x=lambda d: d.rho.astype(float)).sort_values("x")
        c = W_RAMP[min(i, len(W_RAMP) - 1)]
        ax.fill_between(g.x, g.ci_lo, g.ci_hi, color=c, alpha=0.18, lw=0)
        ax.plot(g.x, g.mean_of_cell_means, color=c, lw=2, marker="o", ms=5, mec=SURFACE, mew=1.5, label=f"W = {w}")
    ax.axvline(rho_eq, color=INK2, lw=1, ls=(0, (4, 3)))
    ax.text(rho_eq, ax.get_ylim()[1], f" KERC-equivalent\n ₹{rho_eq:.2f}", fontsize=8, color=INK2, va="top")
    ax.set_xscale("log")
    ax.set_xticks([1, 2, 5, 14, 50], ["1", "2", "5", "14", "50"])
    ax.set_xlim(0.85, 60)
    ax.set_xlabel("Demand charge ρ (₹ per kW per shift, log scale)", fontsize=9, color=INK2)
    ax.set_ylabel("TEC saving vs energy-only optimum (%)", fontsize=9, color=INK2)
    n = int(t.n_valid.sum() / max(len(GRID_RHO), 1))
    _title(ax, "Saving of the peak-aware optimum over energy-only, by demand charge",
           f"8 × 3, CV ≤ 0.35; mean of cell means, 95 % bootstrap band; exact set, n = {n} instances")
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    fig.tight_layout()
    fig.savefig(out / "f1_saving_vs_rho.png")
    plt.close(fig)


def f2_break_even(it, rho_eq, out):
    d = it[it.cv.astype(str).isin(["0", "0.35"])]
    fig, ax = _fig()
    for i, (w, g) in enumerate(sorted(d.groupby("w_target"), key=lambda kv: float(kv[0]))):
        n = len(g)
        ex = sorted(g[g.be_B_kind == "exact"].be_B_inr.map(lambda s: float(Fraction(str(s)))))   # exact rationals, e.g. "127/10"
        none = int((g.be_B_kind == "no_peak_reduction").sum())
        other = n - len(ex) - none
        xs = [0] + ex + [60]
        ys = [0] + [(k + 1) / n for k in range(len(ex))] + [len(ex) / n]
        c = W_RAMP[min(i, len(W_RAMP) - 1)]
        ax.step(xs, [y * 100 for y in ys], where="post", color=c, lw=2,
                label=f"W = {w}: {len(ex)} exact, {none} no reduction" + (f", {other} other" if other else ""))
    ax.axvline(rho_eq, color=INK2, lw=1, ls=(0, (4, 3)))
    ax.text(rho_eq, 101, f" KERC ₹{rho_eq:.2f}", fontsize=8, color=INK2, va="bottom")
    ax.set_xlim(-0.5, 60)
    ax.set_ylim(0, 105)
    ax.set_xlabel("Break-even demand charge ρ* vs energy-only (₹ per kW per shift)", fontsize=9, color=INK2)
    ax.set_ylabel("Instances with ρ* ≤ x (%)", fontsize=9, color=INK2)
    _title(ax, "Exact break-even demand charge vs the KERC-equivalent value",
           "8 × 3, CV ≤ 0.35; ECDF over all instances; 'no reduction' instances never reach the curve")
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    fig.tight_layout()
    fig.savefig(out / "f2_break_even_ecdf.png")
    plt.close(fig)


def f3_decomposition(sm, out, rho="eq26"):
    t = sm[(sm.subset == "cv<=0.35") & (sm.grouping == "by_W") & (sm.rho == rho)]
    steps = [("step_fcfs_eg_pct", "FCFS → energy rule", AQUA), ("step_eg_b_pct", "energy rule → energy-only optimum", ORANGE),
             ("step_b_c_pct", "energy-only → peak-aware optimum", BLUE)]
    ws = sorted(t.level.unique(), key=float)
    fig, ax = _fig(h=3.4)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", color=GRID_C, lw=0.8)
    for yi, w in enumerate(ws):
        left = 0.0
        for est, lab, c in steps:
            v = float(t[(t.level == w) & (t.estimand == est)].mean_of_cell_means.iloc[0])
            ax.barh(yi, v, left=left, color=c, height=0.55, edgecolor=SURFACE, linewidth=2, label=lab if yi == 0 else None)
            left += v
        tot = float(t[(t.level == w) & (t.estimand == "total_fcfs_c_pct")].mean_of_cell_means.iloc[0])
        n = int(t[(t.level == w) & (t.estimand == "total_fcfs_c_pct")].n_valid.iloc[0])
        ax.text(left + 0.4, yi, f"{tot:.1f}%  (n={n})", va="center", fontsize=8, color=INK2)
    ax.set_yticks(range(len(ws)), [f"W = {w}" for w in ws])
    ax.invert_yaxis()
    ax.set_xlabel("Saving vs FCFS, in points of FCFS TEC (mean of cell means)", fontsize=9, color=INK2)
    _title(ax, "Where the saving vs FCFS comes from (KERC-equivalent ρ)",
           "8 × 3, CV ≤ 0.35; complete chains only (FCFS and energy rule succeeded, exact front)")
    ax.legend(frameon=False, fontsize=8, loc="lower center", bbox_to_anchor=(0.5, -0.42), ncol=3)
    fig.tight_layout()
    fig.savefig(out / "f3_decomposition.png")
    plt.close(fig)


def f4_bills(sm, out, rho="eq26"):
    t = sm[(sm.subset == "cv<=0.35") & (sm.grouping == "by_W") & (sm.rho == rho)]
    ws = sorted(t.level.unique(), key=float)
    fig, ax = _fig(h=3.6)
    for k, (est, lab, c) in enumerate([("bill_renegotiated_saving_inr", "contract demand renegotiated", BLUE),
                                       ("bill_fixed_saving_inr", "contract demand fixed", GREY)]):
        for i, w in enumerate(ws):
            r = t[(t.level == w) & (t.estimand == est)].iloc[0]
            x = i + (k - 0.5) * 0.36
            ax.bar(x, r.mean_of_cell_means, width=0.34, color=c, edgecolor=SURFACE, linewidth=2,
                   label=lab if i == 0 else None)
            ax.errorbar(x, r.mean_of_cell_means, yerr=[[r.mean_of_cell_means - r.ci_lo], [r.ci_hi - r.mean_of_cell_means]],
                        color=INK2, lw=1, capsize=2)
            v = r.mean_of_cell_means
            ax.text(x, max(r.ci_hi, 0), f"{'−' if v < 0 else ''}₹{abs(v):,.0f}", ha="center", va="bottom", fontsize=7.5,
                    color=INK2)
    ax.axhline(0, color=INK2, lw=0.8)
    ax.set_xticks(range(len(ws)), [f"W = {w}" for w in ws])
    ax.set_ylabel("Saving vs energy-only (₹ per month)", fontsize=9, color=INK2)
    _title(ax, "Partial monthly bill saving vs energy-only (KERC-equivalent ρ)",
           "PARTIAL MONTHLY BILL ESTIMATE: demand charge + scheduled energy; 26 days, PF 1; 95 % band")
    ax.legend(frameon=False, fontsize=8, loc="lower center", bbox_to_anchor=(0.5, -0.32), ncol=2)
    fig.tight_layout()
    fig.savefig(out / "f4_monthly_bill.png")
    plt.close(fig)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--analysis", type=Path, default=ROOT / "results/main_analysis")
    ap.add_argument("--block", default="m3")
    ap.add_argument("--out", type=Path, default=None)
    a = ap.parse_args(argv)
    src = a.analysis / a.block
    out = a.out or (a.analysis / "figures")
    out.mkdir(parents=True, exist_ok=True)
    sm = pd.read_csv(src / "summary_estimates.csv", dtype={"level": str, "rho": str})
    pr = pd.read_csv(src / "per_rho.csv", dtype={"w_target": str, "cv": str, "gamma": str, "rho": str})
    it = pd.read_csv(src / "instances.csv", dtype={"w_target": str, "cv": str, "gamma": str, "be_B_inr": str})
    rho_eq = float(pr[pr.rho == "eq26"].rho_inr.iloc[0])
    f1_saving_vs_rho(sm, pr, rho_eq, out)
    f2_break_even(it, rho_eq, out)
    f3_decomposition(sm, out)
    f4_bills(sm, out)
    print(f"wrote 4 figures to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
