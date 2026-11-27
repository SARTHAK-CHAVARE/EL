"""Prototype (07_src/app): shared engine, file formats, CLI and Streamlit UI.

Golden values are the hand-verified benchmark (04_mathematical_model/verification/test_instances/hand_calculations.md).
"""
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import pytest

from app.core import (analyse, best_for_bill, bills, choose, comparison, front_table, generated_instance_dict,
                      kerc_rho_paise, rho_paise_from_inr)
from app.io import instance_to_dict, load_instance, power_profile_w, schedule_to_dict, slot_label
from benchmark_instance import benchmark_instance
from model import check_schedule, evaluate_schedule
from model.billing import BillingAssumptions

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = sorted((ROOT / "examples").glob("*.json"))


@pytest.fixture(scope="module")
def bench():
    return analyse(benchmark_instance())


def test_instance_json_round_trip_is_exact():
    inst = benchmark_instance()
    back = load_instance(json.loads(json.dumps(instance_to_dict(inst))))
    assert (back.jobs, back.tariff_paise, back.base_w, back.T, back.D, back.delta_t_min) == \
        (inst.jobs, inst.tariff_paise, inst.base_w, inst.T, inst.D, inst.delta_t_min)
    with pytest.raises(ValueError):
        load_instance({**instance_to_dict(inst), "tariff_inr_per_kwh": [5.6]})
    assert slot_label(5, 15, "16:00") == "17:00" and slot_label(3, 60, None) == "slot 3"


def test_examples_load_and_are_valid():
    assert {p.stem for p in EXAMPLES} >= {"benchmark", "shop_8x3_kerc", "shop_12x4"}
    for p in EXAMPLES:
        inst = load_instance(p)
        assert len(inst.tariff_paise) == inst.T


def test_benchmark_golden_values(bench):
    assert bench.front.complete and bench.break_even_b.kind == "exact"
    assert bench.break_even_b.rho_inr == Fraction(127, 10)
    rec = choose(bench, 1500)
    assert rec.proven_optimal and rec.metrics.peak_w == 27000 and rec.metrics.tec_int == 131760 * 60000
    assert choose(bench, 1270).metrics.peak_w == 37000                      # at the break-even: tie -> energy-only
    rows = {r["approach"].split(" (")[0]: r for r in comparison(bench, 1500)}
    assert rows["Energy-only optimum"]["total_inr"] == pytest.approx(1340.60) and rows["Energy-only optimum"]["proven"]
    assert rows["Recommended"]["total_inr"] == pytest.approx(1317.60)
    assert [r["peak_kw"] for r in front_table(bench)] == [37, 27]


def test_benchmark_bills_and_scenario_choice(bench):
    a = BillingAssumptions(26)
    assert kerc_rho_paise(a) == 1346 and rho_paise_from_inr("13.46") == 1346
    rec = choose(bench, kerc_rho_paise(a))
    b = bills(bench, rec, a)
    assert b["renegotiated"].saving_inr == 198 and b["fixed"].saving_inr == -2007
    name_f, _, bill_f = best_for_bill(bench, a, "fixed")
    name_r, _, bill_r = best_for_bill(bench, a, "renegotiated")
    assert bill_f.total_inr == Fraction("33375.6") and name_f in ("front[peak=37000W]", "Energy-only (B)")
    assert bill_r.total_inr == Fraction("33177.6") and "peak=27000" in name_r


def test_schedule_export(bench):
    rec = choose(bench, 1500)
    d = schedule_to_dict(bench.inst, rec.schedule, rec.metrics, "recommended", None, 1500)
    assert d["metrics"]["peak_kw"] == 27 and d["metrics"]["tec_inr"] == 1317.6
    assert len(d["operations"]) == 4 and max(d["power_profile_kw"]) == 27
    assert power_profile_w(bench.inst, rec.schedule) == [w * 1000 for w in d["power_profile_kw"]]


def test_generated_instance_and_guard_never_worse_than_energy_only():
    inst = load_instance(generated_instance_dict("8x3", "19/14", "0.55", "0.35", 3))
    a = analyse(inst)
    for rho in (100, 1346, 5000):
        rec = choose(a, rho)
        assert check_schedule(inst, rec.schedule) == []
        assert rec.metrics.tec_int <= evaluate_schedule(inst, a.b_schedule, rho).tec_int


def test_cli_solve_and_generate(tmp_path):
    cli = [sys.executable, str(ROOT / "07_src/app/cli.py")]
    r = subprocess.run(cli + ["solve", "--instance", str(ROOT / "examples/benchmark.json"), "--rho", "15",
                              "--out", str(tmp_path)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert "INR 12.70/kW per shift (exact)" in r.stdout and "saving INR 198.00" in r.stdout
    assert "PARTIAL MONTHLY BILL ESTIMATE" in r.stdout
    for f in ("schedule_recommended.json", "schedule_energy_only.json", "gantt_recommended.png", "power_profile.png",
              "cost_vs_rho.png", "front.png"):
        assert (tmp_path / f).stat().st_size > 500, f
    g = subprocess.run(cli + ["generate", "--out", str(tmp_path / "g.json")], capture_output=True, text=True)
    assert g.returncode == 0 and load_instance(tmp_path / "g.json").T == 32
    bad = subprocess.run(cli + ["solve", "--instance", str(tmp_path / "missing.json")], capture_output=True, text=True)
    assert bad.returncode == 2 and "error" in bad.stderr


def test_streamlit_app_runs_headless():
    st_testing = pytest.importorskip("streamlit.testing.v1")
    at = st_testing.AppTest.from_file(str(ROOT / "07_src/app/ui.py"), default_timeout=180).run()
    assert not at.exception
    labels = {m.label: m.value for m in at.metric}
    assert labels["Peak demand"] == "27 kW" and labels["Break-even demand charge"] == "INR 12.70/kW"
    at.sidebar.radio[2].set_value("fixed").run()
    assert not at.exception and any(m.label == "Best monthly saving, CD fixed" for m in at.metric)
