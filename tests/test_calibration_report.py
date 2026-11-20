"""Tests for analysis/calibration_report.py (E1-E5): exact answers on synthetic frames, and the CLI on a real micro run.

The calibration design has 2 seeds per cell, so the module must stay DESCRIPTIVE: these tests also pin that no
interval / p-value / effect-size column appears in any output.
"""
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest

from analysis import calibration_report as cr
from analysis.tables import paired_table, rho_star_pair_table
from experiments.design import Design
from experiments.runner import run_experiment
from test_analysis import frame, synth

ROOT = Path(__file__).resolve().parents[1]
CAL_MICRO = Design(name="cal-micro", gammas=("19/14",), workloads=("0.40", "0.55"), cvs=("0", "0.35"),
                   rho_inr=("5", "50"), seeds_per_cell=2, n_jobs=4, n_machines=2, T=16, solver_time_limit_s=20,
                   solver_det_time_limit=8, tiebreak_time_limit_s=10, tiebreak_det_time_limit=4)
FORBIDDEN = ("ci_", "p_value", "pvalue", "stderr", "std_err", "effect_size", "cohen")


def inst(w, cv="0.35", seed=0, gamma="19/14", conflict=True, w_real=None, attempts=1, **over):
    """Synthetic instance. conflict=False => P cannot reduce the peak (C = B); conflict=True => C saves at both rho."""
    rows = synth(f"g{gamma[:2]}w{w}c{cv}s{seed}", cell=(gamma, w, cv), **over)
    for r in rows:
        r["seed_idx"], r["w_real"], r["gen_attempts"] = seed, (float(w) if w_real is None else w_real), attempts
        if not conflict:
            if r["strategy"] == "P":
                r["peak_w"] = 40_000
            if r["strategy"] == "C":
                r["ec_int"], r["peak_w"] = 1000, 40_000
    return rows


def build(*instances):
    df = frame(*instances)
    return cr.build_all(df, rho_paise_levels=[500, 1500])


# ------------------------------------------------------------------------------------------------ E1
def test_e1_counts_shares_and_undetermined_exclusion():
    res = build(inst("0.40", seed=0), inst("0.40", seed=1), inst("0.40", cv="0", seed=0),
                inst("0.40", cv="0", seed=1, P=("FEASIBLE", 1)),       # P stage 2 unproven -> undetermined
                inst("0.70", seed=0, conflict=False), inst("0.70", seed=1, conflict=False))
    e1 = res["e1_by_w"].set_index("w_target")
    a, b = e1.loc["0.40"], e1.loc["0.70"]
    assert (a.n_instances, a.n_conflict, a.n_no_conflict, a.n_undetermined) == (4, 3, 0, 1)
    assert a.share_conflict == pytest.approx(1.0)                       # undetermined is excluded from the denominator
    assert (b.n_conflict, b.n_no_conflict, b.share_conflict) == (0, 2, 0.0)
    assert list(res["e1_by_w"].w_target) == ["0.40", "0.70"]            # numeric W order
    assert {"w_real_mean", "w_real_min", "w_real_max"} <= set(res["e1_by_w"].columns)


def test_e1_all_undetermined_share_is_nan_not_zero():
    res = build(inst("0.40", seed=0, P=("UNKNOWN", 0)), inst("0.40", seed=1, P=("UNKNOWN", 0)))
    r = res["e1_by_w"].iloc[0]
    assert r.n_undetermined == 2 and pd.isna(r.share_conflict)


def test_missing_instance_rows_make_the_indicator_undetermined():
    rows = inst("0.40", seed=0)
    rows = [r for r in rows if r["strategy"] != "P"]                     # P never produced
    res = build(rows, inst("0.40", seed=1))
    e1 = res["e1_by_w"].iloc[0]
    assert (e1.n_conflict, e1.n_undetermined) == (1, 1)


# ------------------------------------------------------------------------------------------------ E2
def test_e2_replicate_categories():
    res = build(inst("0.40", cv="0", seed=0), inst("0.40", cv="0", seed=1),                           # both conflict
                inst("0.40", cv="0.35", seed=0, conflict=False), inst("0.40", cv="0.35", seed=1, conflict=False),
                inst("0.40", cv="0.75", seed=0), inst("0.40", cv="0.75", seed=1, conflict=False),       # disagree
                inst("0.55", cv="0", seed=0), inst("0.55", cv="0", seed=1, P=("FEASIBLE", 0)),          # undetermined
                inst("0.55", cv="0.35", seed=0))                                                         # incomplete
    c = res["e2_cells"].set_index(["w_target", "cv"]).category
    assert c[("0.40", "0")] == "both_conflict" and c[("0.40", "0.35")] == "both_none"
    assert c[("0.40", "0.75")] == "disagree" and c[("0.55", "0")] == "undetermined"
    assert c[("0.55", "0.35")] == "incomplete"
    ag = res["e2_agree"].set_index("w_target")
    assert ag.loc["0.40", "agreement_share"] == pytest.approx(2 / 3)
    assert ag.loc["ALL", "n_cells"] == 5 and ag.loc["ALL", "disagree"] == 1
    assert list(res["e2_agree"].w_target)[-1] == "ALL"                   # totals row last
    row = res["e2_cells"].set_index(["w_target", "cv"]).loc[("0.40", "0.75")]
    assert row.outcomes == "conflict|none" and "saving_pct_rho5_by_seed" in res["e2_cells"].columns


# ------------------------------------------------------------------------------------------------ E3
def test_e3_counts_and_conflict_restriction():
    res = build(inst("0.40", seed=0), inst("0.40", seed=1), inst("0.40", cv="0", seed=0, conflict=False),
                inst("0.40", cv="0", seed=1, C=("FEASIBLE", 0)))
    allrows = res["e3_by_rho"].set_index("rho_inr")
    r5 = allrows.loc[5.0]
    assert (r5.n_rows, r5.n_valid, r5.n_positive, r5.n_zero, r5.n_unproven, r5.n_missing) == (4, 3, 2, 1, 1, 0)
    assert r5.share_positive == pytest.approx(2 / 3) and r5.mean_saving_pct > 0
    conf = res["e3_conf_by_rho"].set_index("rho_inr").loc[5.0]            # restricted to conflict instances
    assert conf.n_rows == 3                                              # the unproven-C instance still has a conflict
    assert conf.n_valid == 2 and conf.n_positive == 2 and conf.share_positive == pytest.approx(1.0)
    assert not allrows.n_valid.eq(allrows.n_rows).all()                  # exclusions are visible, not silent


def test_subthreshold_criterion():
    mk = lambda lo, ref: pd.DataFrame({"rho_inr": [1.0, 5.0], "share_positive": [lo, ref]})
    assert cr.subthreshold_check(mk(0.2, 0.8))["captured"] is True
    assert cr.subthreshold_check(mk(0.6, 0.8))["captured"] is False
    assert cr.subthreshold_check(mk(0.55, 0.8))["captured"] is True       # boundary: exactly the 0.25 margin
    assert cr.subthreshold_check(mk(float("nan"), 0.8))["captured"] is None
    assert cr.subthreshold_check(pd.DataFrame({"rho_inr": [5.0], "share_positive": [1.0]}))["captured"] is None


def test_breakeven_summary_counts_upper_bounds_per_rho():
    res = build(inst("0.40", seed=0), inst("0.40", seed=1), inst("0.55", seed=0, conflict=False))
    be = res["be_inst"]
    assert len(be) == 2 and (be.w_target == "0.40").all()                # only conflict instances
    # ec_P - ec_B = 400 ; peak diff = 20_000 W -> rho*_ub = 400 / (6000 * 20000) INR/kW per synthetic units
    expected = 400 / (6000.0 * 20_000)
    assert be.rho_star_ub_B.iloc[0] == pytest.approx(expected)
    s = res["be_sum"].set_index("group")
    assert s.loc["ALL", "n"] == 2 and s.loc["ALL", "n_with_ub<=rho5"] == 2


# ------------------------------------------------------------------------------------------------ E4
def test_e4_accounting_counts_missing_unproven_and_unexpected():
    a, b = inst("0.40", seed=0), inst("0.40", seed=1, C=("FEASIBLE", 1))
    b = [r for r in b if not (r["strategy"] == "C" and r["rho_paise"] == 1500)]       # one C row never produced
    df = frame(a, b)
    ids = ["g19w0.40c0.35s0", "g19w0.40c0.35s1", "g19w0.40c0.35s2"]                    # third instance never ran
    status, proof, acc, excl = cr.e4_tables(df, paired_table(df), ids, [500, 1500])
    a_ = acc.iloc[0]
    assert (a_.expected_instances, a_.present_instances, a_.missing_instances) == (3, 2, 1)
    assert a_.expected_rows == 3 * (7 + 2) and a_.missing_rows == 3 * 9 - len(df) and a_.duplicate_rows == 0
    p5 = proof[(proof.w_target == "0.40") & (proof.rho_inr == 5.0)].iloc[0]
    assert (p5.rows, p5.fully_proven, p5.stage1_proven, p5.tiebreak_unproven, p5.stage1_unproven) == (2, 1, 2, 1, 0)
    p15 = proof[(proof.w_target == "0.40") & (proof.rho_inr == 15.0)].iloc[0]
    assert p15.rows == 1
    assert set(excl.flag) == {"saving_valid", "full_valid", "band_valid_Bmin", "band_valid_Bmax"}
    assert status.n.sum() == len(df)


def test_runtime_tables_cover_every_row():
    df = frame(inst("0.40", seed=0), inst("0.55", seed=0))
    by_s, by_c, per_inst = cr.runtime_tables(df)
    assert by_s["count"].sum() == len(df)
    assert per_inst.set_index("w_target").loc["ALL", "count"] == 2
    assert per_inst.set_index("w_target").loc["0.40", "sum"] == pytest.approx(9.0)      # 7 rho-free + 2 C rows, 1 s each


# ------------------------------------------------------------------------------------------------ workload / acceptance
def test_nominal_and_realised_workload_are_both_reported():
    res = build(inst("0.40", seed=0, w_real=0.4062), inst("0.40", seed=1, w_real=0.3875))
    acc = res["acceptance"].iloc[0]
    assert acc.w_target == "0.40" and acc.w_real_mean == pytest.approx((0.4062 + 0.3875) / 2)
    assert acc.w_real_min == pytest.approx(0.3875) and acc.w_real_max == pytest.approx(0.4062)
    assert acc.max_abs_w_diff == pytest.approx(0.0125) and acc.n_first_draw == 2 and acc.mean_attempts == 1.0
    assert {"w_target", "w_real"} <= set(res["inst"].columns) and "w_diff" in res["inst"].columns


def test_acceptance_attempts_are_reported():
    res = build(inst("0.70", seed=0, attempts=1), inst("0.70", seed=1, attempts=3))
    a = res["acceptance"].iloc[0]
    assert a.max_attempts == 3 and a.n_first_draw == 1 and a.draws_per_instance_accept_rate == pytest.approx(2 / 4)


# ------------------------------------------------------------------------------------------------ E5 and predictions
def test_transition_and_monotonicity():
    s = pd.Series({"0.40": 1.0, "0.475": 0.8, "0.55": 0.9, "0.625": 0.1, "0.70": 0.0})
    tr = cr.transition(s)
    assert tr["adjacent_increases"] == [(0.475, 0.55)] and not tr["monotone_non_increasing"]
    assert tr["highest_W_with_conflict"] == 0.625 and tr["lowest_W_with_zero_share"] == 0.7
    s2 = pd.Series({"0.40": 1.0, "0.55": 0.5, "0.70": 0.0})
    assert cr.transition(s2)["monotone_non_increasing"] is True
    assert cr.transition(pd.Series({"0.4": float("nan")}))["determined"] is False


def test_suggest_levels_rule_and_coincidence_note():
    s = pd.Series({"0.40": 1.0, "0.475": 1.0, "0.55": 0.5, "0.625": 0.25, "0.70": 0.0})
    lv = cr.suggest_levels(s)
    assert lv["picks"] == [0.475, 0.55, 0.625, 0.70] and lv["n_distinct"] == 4 and "distinct" in lv["note"]
    flat = pd.Series({"0.40": 1.0, "0.55": 0.0, "0.70": 0.0})
    lv2 = cr.suggest_levels(flat)
    assert lv2["n_distinct"] < 4 and "refine" in lv2["note"]
    assert cr.suggest_levels(pd.Series({"0.40": 0.0, "0.70": 0.0}))["levels"] == []


def test_predictions_a_b_c():
    held = build(*[inst("0.40", cv=cv, seed=s) for cv in ("0", "0.35") for s in (0, 1)],
                 *[inst("0.70", cv=cv, seed=s, conflict=False) for cv in ("0", "0.35") for s in (0, 1)])
    p = held["predictions"].set_index(held["predictions"].prediction.str[:3]).status
    assert p["(a)"] == "held"
    assert p["(b)"] == "not_held"                                         # CV>0 instances at W=0.40 do have conflict here
    inc = build(inst("0.40", seed=0, conflict=False), inst("0.40", seed=1, conflict=False),
                inst("0.70", seed=0), inst("0.70", seed=1))
    assert inc["predictions"].set_index(inc["predictions"].prediction.str[:3]).status["(a)"] == "not_held"
    no_cv = build(inst("0.40", cv="0", seed=0), inst("0.40", cv="0", seed=1))
    assert no_cv["predictions"].iloc[1].status == "undetermined"          # no CV>0 instance at all


# ------------------------------------------------------------------------------------------------ real pipeline + CLI
@pytest.fixture(scope="module")
def micro_results(tmp_path_factory):
    out = tmp_path_factory.mktemp("calmicro")
    run_experiment(CAL_MICRO, out, progress=lambda *_: None)
    return out


def test_cli_writes_all_outputs_without_any_interval_columns(micro_results, tmp_path):
    cmd = [sys.executable, str(ROOT / "07_src/analysis/calibration_report.py"), "--results", str(micro_results),
           "--out", str(tmp_path)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    for name in ("instance_table", "e1_conflict_by_W", "e2_replicate_cells", "e2_replicate_agreement_by_W", "e3_saving_by_W_rho",
                 "e3_saving_by_rho", "e3_breakeven_upper_bounds_summary", "e4_status_counts", "e4_C_proof_by_W_rho",
                 "e4_row_accounting", "runtime_by_strategy", "runtime_C_by_W_rho", "workload_nominal_vs_realised",
                 "e5_predictions"):
        assert (tmp_path / f"{name}.csv").exists(), name
    for fig in ("fig_e1_conflict_by_W", "fig_e2_replicate_agreement", "fig_e3_saving_by_rho", "fig_e4_C_proof_status_by_rho",
                "fig_runtime_C_by_rho", "fig_workload_nominal_vs_realised"):
        assert (tmp_path / f"{fig}.png").stat().st_size > 2000, fig
    for f in tmp_path.glob("*.csv"):
        cols = [c.lower() for c in pd.read_csv(f).columns]
        assert not any(c.startswith(FORBIDDEN) or any(k in c for k in FORBIDDEN[1:]) for c in cols), f.name
    assert "DESCRIPTIVE ONLY" in (tmp_path / "README.txt").read_text()
    j = json.loads((tmp_path / "e5_transition_and_levels.json").read_text())
    assert "not an estimate with uncertainty" in j["note"]
    acc = pd.read_csv(tmp_path / "e4_row_accounting.csv").iloc[0]
    assert acc.expected_instances == 8 == acc.present_instances and acc.missing_rows == 0 and acc.unexpected_rows == 0
    assert acc.expected_rows == 8 * (7 + 2)
    w = pd.read_csv(tmp_path / "workload_nominal_vs_realised.csv", dtype={"w_target": str})
    assert list(w.w_target) == ["0.40", "0.55"] and (w.n_instances == 4).all() and w.w_real_mean.notna().all()


def test_cli_refuses_missing_results_and_mixed_digest(micro_results, tmp_path):
    cmd = [sys.executable, str(ROOT / "07_src/analysis/calibration_report.py")]
    assert subprocess.run(cmd + ["--results", str(tmp_path / "none")], capture_output=True, text=True).returncode == 2
    bad = tmp_path / "bad"
    bad.mkdir()
    (bad / "results.csv").write_text((micro_results / "results.csv").read_text())
    m = json.loads((micro_results / "manifest.json").read_text())
    m["design_digest"] = "0" * 16
    (bad / "manifest.json").write_text(json.dumps(m))
    r = subprocess.run(cmd + ["--results", str(bad)], capture_output=True, text=True)
    assert r.returncode == 2 and "error" in r.stderr
