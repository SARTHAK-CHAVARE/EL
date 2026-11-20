import math
import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest

from analysis.tables import (AnalysisError, bootstrap_ci, coverage_table, load_results, paired_table,
                             rho_star_pair_table, status_table, stratified_cluster_bootstrap, summary_by)
from experiments.design import Design
from experiments.runner import run_experiment

ROOT = Path(__file__).resolve().parents[1]
MICRO = Design(name="micro", gammas=("19/14",), workloads=("0.40",), cvs=("0.35",), rho_inr=("5", "50"),
               seeds_per_cell=2, n_jobs=4, n_machines=2, T=16, solver_time_limit_s=20, solver_det_time_limit=8,
               tiebreak_time_limit_s=10, tiebreak_det_time_limit=4)

NSTAGES = {"A": 2, "B": 2, "B_minpeak": 3, "B_maxpeak": 3, "P": 3, "C": 2}


# ---------------------------------------------------------------- synthetic results (exact control of proofs)
def _row(iid, strat, rho, status, proven, ec, peak, mk=5, cell=("19/14", "0.40", "0.35"), digest="d1"):
    n = NSTAGES.get(strat, 0)
    return dict(design_digest=digest, instance_id=iid, gamma=cell[0], w_target=cell[1], w_real=0.4, cv=cell[2],
                seed_idx=int(iid[-1]), strategy=strat, rho_paise=rho, status=status, proven_optimal=int(status == "OPTIMAL"),
                primary_proven=int(proven >= 1), proven_stages=proven, n_stages=n, stage_statuses="", stage_values="",
                makespan=mk, sum_completion=10, peak_w=peak, energy_w_min=0, ec_int=ec, dc_int=0, tec_int=0,
                wall_time_s=1.0)


def synth(iid="i0", cell=("19/14", "0.40", "0.35"), rhos=(500, 1500), **over):
    """One instance. Defaults: everything proven. Override with e.g. Bmin=("FEASIBLE", 2) or C=(status, stages)."""
    spec = dict(A=("OPTIMAL", 2), B=("OPTIMAL", 2), B_minpeak=("OPTIMAL", 3), B_maxpeak=("OPTIMAL", 3),
                P=("OPTIMAL", 3), C=("OPTIMAL", 2))
    key = {"Bmin": "B_minpeak", "Bmax": "B_maxpeak"}
    spec.update({key.get(k, k): v for k, v in over.items()})
    ec = dict(A=900, B=1000, B_minpeak=1000, B_maxpeak=1000, P=1400, C=1100)
    pk = dict(A=40_000, B=40_000, B_minpeak=30_000, B_maxpeak=40_000, P=20_000, C=30_000)
    rows = []
    for s in ("A", "B", "B_minpeak", "B_maxpeak", "P"):
        rows.append(_row(iid, s, 0, spec[s][0], spec[s][1], ec[s], pk[s], cell=cell))
    for r in rhos:
        rows.append(_row(iid, "C", r, spec["C"][0], spec["C"][1], ec["C"], pk["C"], cell=cell))
    rows.append(_row(iid, "FCFS", 0, "HEURISTIC", 0, 1300, 45_000, cell=cell))
    rows.append(_row(iid, "SPT", 0, "NO_SCHEDULE", 0, None, None, cell=cell))
    return rows


def frame(*instances):
    return pd.DataFrame([r for inst in instances for r in inst])


# ---------------------------------------------------------------- issue 2: separate band validity
def test_band_flags_are_separate_for_minpeak_and_maxpeak():
    t = paired_table(frame(synth(Bmin=("FEASIBLE", 2))))           # B_minpeak tie-break stage 3 not run/proven
    assert not t.band_valid_Bmin.any() and t.band_valid_Bmax.all()
    assert t.saving_pct_vs_Bmin.isna().all() and t.tec_Bmin_valid.isna().all()
    assert t.saving_pct_vs_Bmax.notna().all()                       # unaffected by the other band strategy
    assert set(t.excl_reason_Bmin) == {"unproven"} and set(t.excl_reason_Bmax) == {"ok"}
    t = paired_table(frame(synth(Bmax=("UNKNOWN", 0))))
    assert t.band_valid_Bmin.all() and not t.band_valid_Bmax.any()
    assert t.saving_pct_vs_Bmax.isna().all() and t.saving_pct_vs_Bmin.notna().all()


def test_band_requires_all_three_stages_of_the_band_strategy():
    # stages 1-2 proven but stage 3 (peak tie-break) not -> status FEASIBLE with proven_stages == 2: still invalid
    t = paired_table(frame(synth(Bmax=("FEASIBLE", 2))))
    assert not t.band_valid_Bmax.any() and t.saving_pct_vs_Bmax.isna().all()


def test_band_requires_c_stage1():
    t = paired_table(frame(synth(C=("FEASIBLE", 0))))
    assert not t.band_valid_Bmin.any() and not t.band_valid_Bmax.any()
    assert t.saving_pct_vs_Bmin.isna().all()


def test_band_values_correct_when_valid():
    t = paired_table(frame(synth()))
    r = t[t.rho_paise == 500].iloc[0]
    tec_c = 1100 + 60 * 500 * 30_000
    tec_min = 1000 + 60 * 500 * 30_000
    tec_max = 1000 + 60 * 500 * 40_000
    assert r.saving_pct_vs_Bmin == pytest.approx(100 * (tec_min - tec_c) / tec_min)
    assert r.saving_pct_vs_Bmax == pytest.approx(100 * (tec_max - tec_c) / tec_max)


# ---------------------------------------------------------------- primary_proven vs proven_optimal
def test_saving_needs_b_fully_proven_but_only_c_stage1():
    t = paired_table(frame(synth(C=("FEASIBLE", 1))))              # C: cost proven, makespan tie-break not
    assert t.saving_valid.all() and t.saving_pct.notna().all()
    assert not t.full_valid.any()
    assert t.peak_reduction_pct.isna().all() and t.energy_increase_pct.isna().all() and t.makespan_penalty_pct.isna().all()
    t = paired_table(frame(synth(B=("FEASIBLE", 1))))              # B cost proven but B's peak is tie-break dependent
    assert not t.saving_valid.any() and t.saving_pct.isna().all()
    t = paired_table(frame(synth()))
    assert t.saving_valid.all() and t.full_valid.all() and t.peak_reduction_pct.notna().all()


# ---------------------------------------------------------------- missing / unproven are counted
def test_missing_and_unproven_rows_are_counted_not_dropped():
    good = synth("i0")
    unproven = synth("i1", C=("FEASIBLE", 0))
    partial = [r for r in synth("i2") if not (r["strategy"] == "C" and r["rho_paise"] == 1500)]   # rho=15 row missing
    t = paired_table(frame(good, unproven, partial))
    assert len(t) == 6                                              # 3 instances x 2 rho, none dropped
    s = summary_by(t, ["rho_inr"])
    r5, r15 = s[s.rho_inr == 5.0].iloc[0], s[s.rho_inr == 15.0].iloc[0]
    assert (r5.n_total, r5.n_valid, r5.n_excluded, r5.n_missing, r5.n_unproven) == (3, 2, 1, 0, 1)
    assert (r15.n_total, r15.n_valid, r15.n_excluded, r15.n_missing, r15.n_unproven) == (3, 1, 2, 1, 1)
    assert (s.n_valid + s.n_excluded == s.n_total).all()
    assert (s.n_excluded == s.n_missing + s.n_unproven).all()


def test_coverage_reports_missing_instances():
    c = coverage_table(frame(synth("i0"), synth("i1")), expected_instances=5)
    assert (int(c.present_instances.iloc[0]), int(c.missing_instances.iloc[0])) == (2, 3)


def test_status_table_lists_every_status_and_stage_count():
    st = status_table(frame(synth(), synth("i1", Bmin=("FEASIBLE", 1))))
    assert st.n.sum() == len(frame(synth(), synth("i1"))) and "proven_stages" in st.columns


# ---------------------------------------------------------------- break-even upper bound
def test_rho_star_is_named_and_computed_as_an_upper_bound():
    df = frame(synth())
    df.loc[(df.strategy == "P"), "ec_int"] = 1000 + 762_000_000       # DeltaEC = INR 127
    df.loc[(df.strategy == "B"), "peak_w"] = 30_000                    # DeltaPmax = 10 kW vs P at 20 kW
    df.loc[(df.strategy == "B_minpeak"), "peak_w"] = 30_000
    rs = rho_star_pair_table(df)
    assert "rho_star_ub_B" in rs.columns and not any(c.startswith("rho_star_pair") for c in rs.columns)
    assert rs.rho_star_ub_B.iloc[0] == pytest.approx(12.7) and rs.state_B.iloc[0] == "ok"


@pytest.mark.parametrize("over,state", [
    (dict(B=("FEASIBLE", 1)), "unproven"),
    (dict(P=("FEASIBLE", 1)), "unproven"),          # Pmax proven but EC(P) (stage 2) not -> not usable
])
def test_rho_star_requires_proven_inputs(over, state):
    rs = rho_star_pair_table(frame(synth(**over)))
    assert rs.state_B.iloc[0] == state and math.isnan(rs.rho_star_ub_B.iloc[0])


def test_rho_star_needs_only_two_proven_stages_of_p():
    rs = rho_star_pair_table(frame(synth(P=("FEASIBLE", 2))))     # Cmax tie-break of P irrelevant
    assert rs.state_B.iloc[0] == "ok"


def test_rho_star_missing_and_no_peak_reduction_states():
    df = frame(synth("i0"), synth("i1"))
    df = df[~((df.instance_id == "i1") & (df.strategy == "P"))]
    rs = rho_star_pair_table(df).set_index("instance_id")
    assert rs.loc["i1", "state_B"] == "missing"
    df2 = frame(synth())
    df2.loc[df2.strategy == "P", "peak_w"] = 40_000
    assert rho_star_pair_table(df2).state_B.iloc[0] == "no_peak_reduction_possible"


# ---------------------------------------------------------------- bootstrap scheme
def test_bootstrap_estimate_is_mean_of_cell_means_not_pooled_mean():
    rows = []
    for i in range(4):
        rows.append(dict(instance_id=f"a{i}", gamma="g", w_target="w1", cv="c", v=0.0))
    rows.append(dict(instance_id="b0", gamma="g", w_target="w2", cv="c", v=10.0))
    d = pd.DataFrame(rows)
    est, lo, hi, ncell = stratified_cluster_bootstrap(d, "v", n_boot=200)
    assert est == pytest.approx(5.0) and ncell == 2           # pooled mean would be 2.0
    assert lo <= est <= hi


def test_bootstrap_resamples_instances_not_rho_rows():
    """Two instances x 3 rho rows each (constant within instance): cluster resampling gives means in {0,5,10};
    an i.i.d. row bootstrap would give a 95% interval strictly inside (0,10)."""
    rows = [dict(instance_id=i, gamma="g", w_target="w", cv="c", v=val)
            for i, val in (("a", 0.0), ("b", 10.0)) for _ in range(3)]
    est, lo, hi, _ = stratified_cluster_bootstrap(pd.DataFrame(rows), "v", n_boot=2000)
    assert (lo, hi) == (0.0, 10.0) and est == pytest.approx(5.0)
    iid = bootstrap_ci([r["v"] for r in rows], n_boot=2000)
    assert iid[1] > 0.0                                       # shows the difference to the naive scheme


def test_bootstrap_is_stratified_within_cells():
    """Cells never mix: a cell with constant values contributes zero variance regardless of other cells."""
    rows = [dict(instance_id=f"x{i}", gamma="g", w_target="w1", cv="c", v=3.0) for i in range(5)]
    rows += [dict(instance_id=f"y{i}", gamma="g", w_target="w2", cv="c", v=7.0) for i in range(5)]
    est, lo, hi, _ = stratified_cluster_bootstrap(pd.DataFrame(rows), "v", n_boot=500)
    assert est == lo == hi == 5.0


def test_bootstrap_deterministic_empty_and_nan_handling():
    d = pd.DataFrame([dict(instance_id=f"i{k}", gamma="g", w_target="w", cv="c", v=float(k)) for k in range(6)])
    assert stratified_cluster_bootstrap(d, "v", seed_key="k") == stratified_cluster_bootstrap(d, "v", seed_key="k")
    assert all(math.isnan(x) for x in stratified_cluster_bootstrap(d.iloc[0:0], "v")[:3])
    a, b = bootstrap_ci([1.0, 2.0, 3.0, 4.0, 5.0]), bootstrap_ci([1.0, 2.0, 3.0, 4.0, 5.0])
    assert a == b and a[0] == 3.0


def test_summary_by_reports_cells_with_no_valid_instance():
    cell2 = ("1", "0.70", "0")
    t = paired_table(frame(synth("i0"), synth("i1", cell=cell2, C=("FEASIBLE", 0))))
    s = summary_by(t, ["rho_inr"])
    assert (s.n_cells == 2).all() and (s.n_cells_used == 1).all()


# ---------------------------------------------------------------- design identity in analysis input
def test_load_results_refuses_mixed_or_unexpected_digest(tmp_path):
    p = tmp_path / "results.csv"
    frame(synth("i0"), synth("i1")).to_csv(p, index=False)
    assert load_results(p, expected_digest="d1").design_digest.nunique() == 1
    with pytest.raises(AnalysisError):
        load_results(p, expected_digest="other")
    mixed = frame(synth("i0"), [dict(r, design_digest="d2") for r in synth("i1")])
    mixed.to_csv(p, index=False)
    with pytest.raises(AnalysisError) as e:
        load_results(p)
    assert "mixes designs" in str(e.value)


# ---------------------------------------------------------------- real pipeline end to end
@pytest.fixture(scope="module")
def results(tmp_path_factory):
    out = tmp_path_factory.mktemp("an")
    run_experiment(MICRO, out, progress=lambda *_: None)
    return out


def test_paired_table_identities_on_real_runs(results):
    t = paired_table(load_results(results / "results.csv"))
    assert len(t) == 2 * 2                                # instances x rho levels
    for _, r in t[t.saving_valid].iterrows():
        assert r.tec_C <= r.tec_B + 1e-9
        assert r.tec_C <= r.tec_A and r.saving_pct >= -1e-9
        assert math.isclose(r.saving_inr, (r.tec_B - r.tec_C) / 6_000_000)
    for _, r in t[t.band_valid_Bmin].iterrows():
        assert r.tec_C <= r.tec_Bmin
    for _, r in t[t.band_valid_Bmax].iterrows():
        assert r.tec_C <= r.tec_Bmax
    for _, r in t[t.full_valid].iterrows():
        assert r.ec_int_B <= r.ec_int_C and r.peak_w_P <= r.peak_w_C


def test_report_cli_outputs_and_guards(results, tmp_path):
    cmd = [sys.executable, str(ROOT / "07_src/analysis/report.py"), "--results", str(results), "--out", str(tmp_path)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    readme = (tmp_path / "README.txt").read_text()
    assert "PRELIMINARY" in readme and "UPPER BOUND" in readme
    assert "DESCRIPTIVE ONLY" in readme and "NO intervals" in readme and "stratified cluster bootstrap" not in readme
    ub = pd.read_csv(tmp_path / "rho_star_upper_bound.csv")
    assert any(c.startswith("rho_star_ub_") for c in ub.columns) and not (tmp_path / "rho_star_pair.csv").exists()
    cov = pd.read_csv(tmp_path / "coverage.csv")
    assert int(cov.missing_instances.iloc[0]) == 0
    for name in ("summary_saving_vs_Bminpeak_by_rho.csv", "summary_saving_vs_Bmaxpeak_by_rho.csv"):
        s = pd.read_csv(tmp_path / name)
        assert {"n_missing", "n_unproven", "n_excluded"} <= set(s.columns)
    r2 = subprocess.run(cmd + ["--validated"], capture_output=True, text=True)
    assert r2.returncode == 2 and "full design" in r2.stderr


def test_report_cli_rejects_digest_mismatch_and_missing_results(results, tmp_path):
    import json
    import shutil
    work = tmp_path / "w"
    shutil.copytree(results, work)
    mf = json.loads((work / "manifest.json").read_text())
    mf["design_digest"] = "0000000000000000"
    (work / "manifest.json").write_text(json.dumps(mf))
    r = subprocess.run([sys.executable, str(ROOT / "07_src/analysis/report.py"), "--results", str(work)],
                       capture_output=True, text=True)
    assert r.returncode == 2 and "digest" in r.stderr
    r = subprocess.run([sys.executable, str(ROOT / "07_src/analysis/report.py"), "--results", str(tmp_path / "nope")],
                       capture_output=True, text=True)
    assert r.returncode == 2 and "not found" in r.stderr


def test_validated_refused_for_modified_full_design_such_as_the_pilot(tmp_path):
    """A run named 'full' but with --seeds 1 (the 27-instance pilot) must never be stamped VALIDATED."""
    import dataclasses
    from experiments.design import DESIGN_FULL, Design
    from experiments.runner import run_experiment as run
    pilot = dataclasses.replace(MICRO, name="full")           # name 'full' but not the real full design
    out = tmp_path / "p"
    run(pilot, out, progress=lambda *_: None)
    r = subprocess.run([sys.executable, str(ROOT / "07_src/analysis/report.py"), "--results", str(out), "--validated"],
                       capture_output=True, text=True)
    assert r.returncode == 2 and "unmodified full design" in r.stderr
    assert pilot.digest() != DESIGN_FULL.digest()


# ---------------------------------------------------------------- small-n: no intervals; nominal + realised W
def test_summary_by_without_intervals_has_no_ci_columns_and_reports_w_real():
    t = paired_table(frame(synth("i0"), synth("i1", cell=("19/14", "0.55", "0.35"))))
    t.loc[t.instance_id == "i1", "w_real"] = 0.5625
    s = summary_by(t, ["w_target", "rho_inr"], intervals=False)
    assert not any(c.startswith("ci_") for c in s.columns) and "mean" in s.columns
    assert {"w_target", "w_real_mean", "w_real_min", "w_real_max"} <= set(s.columns)
    row = s[(s.w_target == "0.55") & (s.rho_inr == 5.0)].iloc[0]
    assert row.w_real_mean == pytest.approx(0.5625) and row.n_valid == 1
    assert "ci_lo" in summary_by(t, ["rho_inr"]).columns                     # default keeps the (>=10-seed) intervals


def test_report_suppresses_all_intervals_for_two_seed_design(results, tmp_path):
    import json
    cmd = [sys.executable, str(ROOT / "07_src/analysis/report.py"), "--results", str(results), "--out", str(tmp_path)]
    assert subprocess.run(cmd, capture_output=True, text=True).returncode == 0
    assert json.loads((results / "manifest.json").read_text())["design"]["seeds_per_cell"] == 2
    for f in tmp_path.glob("summary_*.csv"):
        cols = pd.read_csv(f).columns
        assert not any(c.startswith("ci_") for c in cols), f.name
    w = pd.read_csv(tmp_path / "summary_saving_by_W_rho.csv")
    assert {"w_target", "w_real_mean", "w_real_min", "w_real_max"} <= set(w.columns)
    assert "DESCRIPTIVE ONLY" in (tmp_path / "README.txt").read_text()
