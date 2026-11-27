"""Charts for the prototype (matplotlib; shared by the CLI and the Streamlit app).

Colour roles (validated categorical palette, dataviz skill): recommended = blue #2a78d6, energy-only = orange #eb6834,
FCFS = muted grey. Tariff periods are a neutral background shade (darker = more expensive), never a series colour.
"""
from __future__ import annotations

from fractions import Fraction
from typing import Dict, Optional, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

from model import Instance, Operation  # noqa: E402

from .io import power_profile_w, slot_label  # noqa: E402

BLUE, ORANGE, GREY = "#2a78d6", "#eb6834", "#8a8984"
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e6e5e1"
BAND_SHADES = ["#f7f6f3", "#ecebe6", "#dcdbd4", "#cbcac2"]       # cheapest -> most expensive
SERIES = {"Recommended": BLUE, "Energy-only": ORANGE, "FCFS": GREY}


def _style(ax):
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.set_axisbelow(True)


def _tariff_bands(ax, inst: Instance, legend: bool = True):
    levels = sorted(set(inst.tariff_paise))
    shade = {lv: BAND_SHADES[min(i, len(BAND_SHADES) - 1)] for i, lv in enumerate(levels)}
    t = 1
    while t <= inst.T:
        lv = inst.tariff_paise[t - 1]
        u = t
        while u + 1 <= inst.T and inst.tariff_paise[u] == lv:
            u += 1
        ax.axvspan(t - 0.5, u + 0.5, color=shade[lv], zorder=0, lw=0)
        t = u + 1
    if legend:
        return [Patch(facecolor=shade[lv], edgecolor="#b9b8b1", label=f"tariff INR {lv / 100:.2f}/kWh") for lv in levels]
    return []


def _xticks(ax, inst: Instance, start_time: Optional[str]):
    step = max(1, inst.T // 8)
    ticks = list(range(1, inst.T + 1, step))
    ax.set_xticks(ticks, [slot_label(t, inst.delta_t_min, start_time) for t in ticks])
    ax.set_xlim(0.5, inst.T + 0.5)


def fig_schedule(inst: Instance, ops: Sequence[Operation], title: str, start_time: Optional[str] = None,
                 color: str = BLUE):
    fig, ax = plt.subplots(figsize=(9, 0.55 * len(inst.machines) + 1.6))
    _style(ax)
    handles = _tariff_bands(ax, inst)
    machines = list(inst.machines)
    for o in ops:
        y = machines.index(o.machine_id)
        ax.barh(y, o.end - o.start + 1, left=o.start - 0.5, height=0.6, color=color, edgecolor="#fcfcfb", lw=2, zorder=3)
        ax.text((o.start + o.end) / 2, y, o.job_id, ha="center", va="center", color="white", fontsize=8, zorder=4,
                fontweight="bold")
    ax.set_yticks(range(len(machines)), [f"Machine {m}" for m in machines])
    ax.invert_yaxis()
    _xticks(ax, inst, start_time)
    ax.set_title(title, fontsize=10, color=INK, loc="left")
    ax.legend(handles=handles, frameon=False, fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.18),
              ncol=len(handles))
    fig.tight_layout()
    return fig


def fig_power(inst: Instance, schedules: Dict[str, Sequence[Operation]], start_time: Optional[str] = None,
              title: str = "Facility power over the shift"):
    """Step lines of total power (base load included) for up to 3 schedules, peaks labelled."""
    fig, ax = plt.subplots(figsize=(9, 3.4))
    _style(ax)
    ax.grid(axis="y", color=GRID, lw=0.8)
    handles = _tariff_bands(ax, inst)
    xs = list(range(1, inst.T + 1))
    for name, ops in schedules.items():
        p = [w / 1000 for w in power_profile_w(inst, ops)]
        col = SERIES.get(name.split(" ")[0], BLUE)
        ax.step([x - 0.5 for x in xs] + [inst.T + 0.5], p + [p[-1]], where="post", color=col, lw=2, zorder=3,
                label=f"{name} (peak {max(p):g} kW)")
        k = p.index(max(p)) + 1
        ax.annotate(f"{max(p):g} kW", (k, max(p)), textcoords="offset points", xytext=(0, 4), ha="center",
                    fontsize=8, color=INK, zorder=5)
    ax.set_ylabel("kW", color=MUTED, fontsize=8)
    ax.set_ylim(0, None)
    _xticks(ax, inst, start_time)
    ax.set_title(title, fontsize=10, color=INK, loc="left")
    lines = ax.get_legend_handles_labels()[0]
    ax.legend(handles=lines + handles, frameon=False, fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.12),
              ncol=min(4, len(lines) + len(handles)))
    fig.tight_layout()
    return fig


def fig_cost_vs_rho(points, b_ec_int: int, b_peak_w: int, rho_max_inr: float = 30.0,
                    marks: Optional[Dict[str, float]] = None):
    """Shift cost vs demand charge: energy-only schedule (line) vs peak-aware optimum (lower envelope of the front)."""
    fig, ax = plt.subplots(figsize=(7.5, 3.6))
    _style(ax)
    ax.grid(color=GRID, lw=0.8)
    rs = [rho_max_inr * i / 200 for i in range(201)]
    b = [b_ec_int / 6e6 + r * b_peak_w / 1000 for r in rs]
    c = [min(p.ec_int / 6e6 + r * p.peak_w / 1000 for p in points) for r in rs]
    ax.plot(rs, b, color=ORANGE, lw=2, label="Energy-only schedule")
    ax.plot(rs, c, color=BLUE, lw=2, label="Peak-aware optimum")
    for name, r in (marks or {}).items():
        ax.axvline(r, color=MUTED, lw=1, ls="--")
        ax.text(r, ax.get_ylim()[1], f" {name}", rotation=90, va="top", ha="right", fontsize=7, color=MUTED)
    ax.set(xlabel="demand charge (INR/kW per shift)", ylabel="cost of the shift (INR)")
    ax.xaxis.label.set_color(MUTED); ax.yaxis.label.set_color(MUTED)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax.set_title("Where peak-awareness starts to pay", fontsize=10, color=INK, loc="left")
    fig.tight_layout()
    return fig


def fig_front(points, chosen_peak_w: Optional[int] = None, b_point=None):
    fig, ax = plt.subplots(figsize=(5.5, 3.6))
    _style(ax)
    ax.grid(color=GRID, lw=0.8)
    xs = [p.peak_w / 1000 for p in points]
    ys = [p.ec_int / 6e6 for p in points]
    ax.plot(xs, ys, color=BLUE, lw=1.5, marker="o", ms=8, mec="#fcfcfb", mew=2, zorder=3, label="Pareto front")
    if b_point is not None:
        ax.scatter([b_point[1] / 1000], [b_point[0] / 6e6], s=70, color=ORANGE, edgecolor="#fcfcfb", lw=2, zorder=4,
                   label="Energy-only schedule")
    if chosen_peak_w is not None:
        p = next(q for q in points if q.peak_w == chosen_peak_w)
        ax.scatter([p.peak_w / 1000], [p.ec_int / 6e6], s=220, facecolor="none", edgecolor=INK, lw=1.5, zorder=5,
                   label="Recommended")
    ax.set(xlabel="peak demand (kW)", ylabel="energy cost of the shift (INR)")
    ax.xaxis.label.set_color(MUTED); ax.yaxis.label.set_color(MUTED)
    ax.legend(frameon=False, fontsize=8)
    ax.set_title("Energy cost vs peak (every nondominated schedule)", fontsize=10, color=INK, loc="left")
    fig.tight_layout()
    return fig
