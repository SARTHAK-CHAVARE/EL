"""P6 analysis (07_src/scripts/main_report.py) run end to end on the committed smoke results (36 + 12 instances)."""
import json
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "07_src" / "scripts"))
sys.path.insert(0, str(ROOT / "07_src"))

import main_report  # noqa: E402


@pytest.fixture(scope="module")
def out(tmp_path_factory):
    o = tmp_path_factory.mktemp("main_analysis")
    rc = main_report.main(["--blocks", "m3-smoke", "m4-smoke", "--n-boot", "20", "--out", str(o)])
    return o, rc


def test_recomputed_values_match_stored_rows(out):
    o, rc = out
    s = json.loads((o / "summary.json").read_text(encoding="utf-8"))
    assert s["problems"] == [] and rc == 0          # C, guard, PCG, rules and the rho-14 cross-check all agree


def test_counts_and_incomplete_front_handling(out):
    o, _ = out
    b = json.loads((o / "summary.json").read_text(encoding="utf-8"))["blocks"]
    assert (b["m3-smoke"]["front_complete"], b["m4-smoke"]["front_complete"]) == (36, 11)     # as P4-SMOKE-RESULTS
    assert b["m4-smoke"]["instances_missing"] == [] and not b["m4-smoke"]["intervals_valid"]
    pr = pd.read_csv(o / "m4-smoke" / "per_rho.csv")
    inc = pr[~pr.front_complete]
    assert len(inc) and not inc.sav_B_valid.any() and (inc.sav_B_reason == "unproven").all()
    assert inc.ach_B_valid.all()                     # the sensitivity analysis keeps them, as achieved savings


def test_identities_and_signs(out):
    o, _ = out
    for blk in ("m3-smoke", "m4-smoke"):
        pr = pd.read_csv(o / blk / "per_rho.csv")
        v = pr[pr.sav_B_valid]
        assert (v.sav_B_pct >= 0).all() and (pr.opt_value_pct.dropna() >= -1e-12).all()
        assert (v.ach_B_pct - v.sav_B_pct).abs().max() < 1e-9       # complete front: guard = exact optimum
        eq = v[v.rho.str.startswith("eq")]                         # renegotiated bill = D x TEC(rho_eq)
        assert (eq.bill_renegotiated_saving_pct - eq.sav_B_pct).abs().max() < 1e-9
        ch = v[v.chain_valid]
        steps = ch.step_fcfs_eg_pct + ch.step_eg_b_pct + ch.step_b_c_pct
        assert (steps - ch.total_fcfs_c_pct).abs().max() < 1e-9


def test_missing_instances_are_counted_not_dropped(tmp_path):
    src = ROOT / "results/main_smoke/m4"
    d = tmp_path / "main_smoke" / "m4"
    d.mkdir(parents=True)
    (d / "manifest.json").write_text((src / "manifest.json").read_text(encoding="utf-8"), encoding="utf-8")
    df = pd.read_csv(src / "results.csv", dtype=str, keep_default_na=False)
    df[df.instance_id != "g0w0c0s000"].to_csv(d / "results.csv", index=False)
    main_report.main(["--blocks", "m4-smoke", "--n-boot", "5", "--results", str(tmp_path), "--out", str(tmp_path / "o")])
    b = json.loads((tmp_path / "o" / "summary.json").read_text(encoding="utf-8"))["blocks"]["m4-smoke"]
    assert b["instances_missing"] == ["g0w0c0s000"]
    pr = pd.read_csv(tmp_path / "o" / "m4-smoke" / "per_rho.csv")
    assert (pr[pr.instance_id == "g0w0c0s000"].sav_B_reason == "missing").all()


def test_figures_render_from_analysis_outputs(out, tmp_path):
    import main_figures
    o, _ = out
    assert main_figures.main(["--analysis", str(o), "--block", "m3-smoke", "--out", str(tmp_path)]) == 0
    assert sorted(p.name for p in tmp_path.glob("*.png")) == [
        "f1_saving_vs_rho.png", "f2_break_even_ecdf.png", "f3_decomposition.png", "f4_monthly_bill.png"]
