"""EL Tariff Opti - Streamlit prototype.

    streamlit run 07_src/app/ui.py

A thin layer over app.core (the same engine as the CLI): one exact solve per instance, then every demand charge and
billing scenario is read off the energy-peak front instantly.
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

from app.core import (analyse, best_for_bill, bills, break_even_text, choose, comparison, front_table,  # noqa: E402
                      generated_instance_dict, kerc_rho_paise, rho_paise_from_inr)
from app.io import load_instance, schedule_to_dict  # noqa: E402
from app.plots import ORANGE, GREY, fig_cost_vs_rho, fig_front, fig_power, fig_schedule  # noqa: E402
from model import evaluate_schedule  # noqa: E402
from model.billing import PARTIAL_BILL_LABEL, BillingAssumptions, rho_equivalent_inr_per_kw  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = sorted((ROOT / "examples").glob("*.json"))

st.set_page_config(page_title="EL Tariff Opti", layout="wide")


@st.cache_resource(show_spinner=False, max_entries=16)
def _analyse(instance_json: str):
    return analyse(load_instance(json.loads(instance_json)))


def _show(fig):
    st.pyplot(fig, width="stretch")
    plt.close(fig)


# ------------------------------------------------------------------------------------------------ sidebar
with st.sidebar:
    st.header("1 · Shop and shift")
    source = st.radio("Instance", ["Example", "Generate", "Upload JSON"], horizontal=True)
    raw = None
    if source == "Example":
        names = {json.loads(p.read_text(encoding="utf-8")).get("name", p.stem): p for p in EXAMPLES}
        default = next((i for i, p in enumerate(names.values()) if p.stem == "benchmark"), 0)
        pick = st.selectbox("Example", list(names), index=default)
        raw = json.loads(names[pick].read_text(encoding="utf-8"))
    elif source == "Generate":
        c1, c2 = st.columns(2)
        size = c1.selectbox("Size (jobs x machines)", ["8x3", "12x4"])
        gamma = c2.selectbox("Peak/off-peak price ratio", ["19/14", "1", "7/4"],
                             help="19/14 = KERC Dec-Jun (7.60/5.60); 1 = KERC Jul-Nov; 7/4 = steep stress case")
        w = c1.selectbox("Workload W", ["0.40", "0.475", "0.55", "0.625", "0.70"], index=2)
        cv = c2.selectbox("Machine power spread (CV)", ["0", "0.35"], index=1)
        seed = st.number_input("Seed", min_value=0, max_value=10_000, value=1, step=1)
        raw = generated_instance_dict(size, gamma, w, cv, int(seed))
    else:
        up = st.file_uploader("Instance JSON", type="json")
        if up is not None:
            raw = json.loads(up.read())
        st.caption("Format: see examples/*.json (slot_minutes, horizon_slots, base_load_kw, "
                   "tariff_inr_per_kwh, machines, jobs with proc_slots and power_kw).")

    st.header("2 · Tariff and billing")
    days = st.slider("Shift-days per month", 20, 31, 26)
    pf = st.slider("Power factor", 0.80, 1.00, 1.00, 0.01)
    assumptions = BillingAssumptions(days_per_month=days, power_factor=Fraction(str(pf)))
    rho_eq = float(rho_equivalent_inr_per_kw(assumptions))
    mode = st.radio("Demand charge used for scheduling",
                    [f"KERC-equivalent (INR {rho_eq:.2f}/kW per shift)", "Custom"])
    rho_paise = (kerc_rho_paise(assumptions) if mode.startswith("KERC") else
                 rho_paise_from_inr(st.slider("INR per kW per shift", 0.0, 60.0, 15.0, 0.5)))
    st.caption("KERC HT-2(a): INR 350 per kVA per month on billing demand BD = max(MD, 0.90 x contract demand). "
               "Equivalent per shift = 350 / (days x PF), assuming the same schedule every day.")
    scenario = st.radio("Contract demand", ["renegotiated", "fixed"],
                        format_func=lambda s: "Renegotiated to the new peak" if s == "renegotiated"
                        else "Fixed at today's (energy-only) peak")

# ------------------------------------------------------------------------------------------------ main
st.title("EL Tariff Opti: peak-aware production scheduling")
st.caption("Exact CP-SAT optimisation under the KERC HT-2(a) tariff. One solve gives every schedule on the "
           "energy-cost / peak-demand trade-off; the demand charge then picks the best one.")
if raw is None:
    st.info("Upload an instance JSON or choose an example to begin.")
    st.stop()
try:
    inst = load_instance(raw)
except (ValueError, KeyError) as exc:
    st.error(f"Invalid instance: {exc}")
    st.stop()
start = raw.get("start_time")
st.markdown(f"**{inst.name}**  \n{len(inst.jobs)} jobs · {len(inst.machines)} machines · {inst.T} slots of "
            f"{inst.delta_t_min} min · base load {inst.base_w / 1000:g} kW")
with st.spinner("Solving (exact)…"):
    a = _analyse(json.dumps(raw, sort_keys=True))
for n in a.notes:
    st.warning(n)
rec = choose(a, rho_paise)
b_tec = (a.b_metrics.ec_int + 60 * rho_paise * a.b_metrics.peak_w) / 6e6
r_tec = rec.metrics.tec_int / 6e6
cmp_ = bills(a, rec, assumptions)[scenario]
best_name, best_sched, best_bill = best_for_bill(a, assumptions, scenario)
ref_bill = cmp_.reference.total_inr
k1, k2, k3, k4 = st.columns(4)
k1.metric("Peak demand", f"{rec.metrics.peak_w / 1000:g} kW",
          f"{(rec.metrics.peak_w - a.b_metrics.peak_w) / 1000:+g} kW vs energy-only", delta_color="inverse")
k2.metric("Cost of the shift", f"INR {r_tec:,.2f}", f"{r_tec - b_tec:+,.2f} vs energy-only", delta_color="inverse")
k3.metric(f"Best monthly saving, CD {scenario}", f"INR {float(ref_bill - best_bill.total_inr):,.0f}",
          help="Cheapest schedule for this contract-demand scenario vs the energy-only schedule. " + PARTIAL_BILL_LABEL)
be = a.break_even_b
k4.metric("Break-even demand charge",
          "none" if be is None or be.rho_inr is None else f"INR {float(be.rho_inr):.2f}/kW",
          None if be is None else ("exact" if be.kind in ("exact", "no_peak_reduction") else "upper bound"),
          delta_color="off")
st.write(break_even_text(a))
status = ("**proven optimal**" if rec.proven_optimal else
          f"not proven optimal (gap ≤ {float(rec.gap) * 100:.2f} %)" if rec.gap is not None else "not proven")
st.write(f"Recommended at INR {rho_paise / 100:.2f}/kW per shift: `{rec.choice}`, {status}. "
         f"Solved in {a.solve_time_s:.1f} s.")
st.write(f"Cheapest schedule for the monthly bill with contract demand **{scenario}**: `{best_name}` "
         f"(partial bill INR {float(best_bill.total_inr):,.0f} vs INR {float(ref_bill):,.0f} for energy-only).")

t1, t2, t3, t4, t5 = st.tabs(["Schedules", "Power over the shift", "Trade-off", "Comparison", "Monthly bill"])
with t1:
    _show(fig_schedule(inst, rec.schedule, "Recommended (peak-aware) schedule", start))
    _show(fig_schedule(inst, a.b_schedule, "Energy-only schedule (ignores the demand charge)", start, color=ORANGE))
    if a.rules["FCFS"] is not None:
        _show(fig_schedule(inst, a.rules["FCFS"], "FCFS (first come, first served)", start, color=GREY))
with t2:
    sched = {"Recommended": rec.schedule, "Energy-only": a.b_schedule}
    if a.rules["FCFS"] is not None and st.checkbox("Show FCFS too"):
        sched["FCFS"] = a.rules["FCFS"]
    _show(fig_power(inst, sched, start))
with t3:
    c1, c2 = st.columns([3, 2])
    marks = {}
    if be is not None and be.rho_inr is not None:
        marks["break-even"] = float(be.rho_inr)
    marks["chosen"] = rho_paise / 100
    with c1:
        _show(fig_cost_vs_rho(a.front.points, a.b_metrics.ec_int, a.b_metrics.peak_w,
                              max(30.0, rho_paise / 100 * 1.5), marks))
    with c2:
        _show(fig_front(a.front.points, rec.metrics.peak_w if rec.choice.startswith("front") else None,
                        (a.b_metrics.ec_int, a.b_metrics.peak_w)))
    st.dataframe(pd.DataFrame(front_table(a)).rename(columns={
        "peak_kw": "peak (kW)", "energy_inr": "energy cost (INR)", "makespan": "last slot",
        "proven": "proven", "best_for_rho_inr": "best for demand charge (INR/kW)"}), hide_index=True)
with t4:
    rows = comparison(a, rho_paise)
    df = pd.DataFrame(rows)
    show = df[[c for c in ("approach", "energy_inr", "peak_kw", "demand_inr", "total_inr", "saving_vs_fcfs_pct",
                           "makespan", "proven", "note") if c in df.columns]]
    st.dataframe(show.rename(columns={"energy_inr": "energy (INR)", "peak_kw": "peak (kW)",
                                      "demand_inr": "demand charge (INR)", "total_inr": "total (INR)",
                                      "saving_vs_fcfs_pct": "saving vs FCFS (%)", "makespan": "last slot"}),
                 hide_index=True)
    st.caption("All costs per shift at the chosen demand charge. 'proven' = proven optimal by CP-SAT.")
with t5:
    out = []
    for scen, c in bills(a, rec, assumptions).items():
        bn, _, bb = best_for_bill(a, assumptions, scen)
        out.append({"contract demand": scen, "energy-only bill (INR)": float(c.reference.total_inr),
                    "recommended bill (INR)": float(c.candidate.total_inr), "saving (INR)": float(c.saving_inr),
                    "0.90 x CD floor binds": c.candidate.floor_binding,
                    "best schedule for this scenario": bn, "its bill (INR)": float(bb.total_inr)})
    st.dataframe(pd.DataFrame(out), hide_index=True)
    st.info(PARTIAL_BILL_LABEL)
    st.caption("With contract demand fixed at today's peak, a peak cut below 0.90 x CD earns nothing, so the "
               "energy-only schedule can be the better choice until the contract demand is renegotiated.")

with st.expander("Export"):
    m = evaluate_schedule(inst, rec.schedule, rho_paise)
    st.download_button("Recommended schedule (JSON)",
                       json.dumps(schedule_to_dict(inst, rec.schedule, m, "recommended", start, rho_paise), indent=1),
                       file_name="schedule_recommended.json", mime="application/json")
    st.download_button("Instance (JSON)", json.dumps(raw, indent=1), file_name="instance.json",
                       mime="application/json")
