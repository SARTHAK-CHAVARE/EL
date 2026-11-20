"""Regression tests: workload definition (issue 3) and runner design-identity / --force behaviour (issue 4)."""
import csv
import dataclasses
import json
import re
import shutil
import types
from fractions import Fraction
from pathlib import Path

import pytest

from experiments.design import DESIGN_FULL, DESIGN_VERSION, Design, enumerate_tasks
from experiments.generator import generate_instance, workload_w
from experiments.runner import (COLUMNS, RunnerError, _row, aggregate, done_ids, run_experiment)
from model import Instance, Job

ROOT = Path(__file__).resolve().parents[1]
MICRO = Design(name="micro", gammas=("19/14",), workloads=("0.40",), cvs=("0.35",), rho_inr=("5", "50"),
               seeds_per_cell=2, n_jobs=4, n_machines=2, T=16, solver_time_limit_s=20, solver_det_time_limit=8,
               tiebreak_time_limit_s=10, tiebreak_det_time_limit=4)
MICRO_B = dataclasses.replace(MICRO, seeds_per_cell=3)          # a different design (different digest)
quiet = dict(progress=lambda *_: None)


# ------------------------------------------------------------------------------- W definition
def _inst(proc_list, powers, M=2, T=10):
    jobs = tuple(Job(f"J{i}", p, {m: powers[m - 1] for m in p}) for i, p in enumerate(proc_list))
    return Instance(machines=tuple(range(1, M + 1)), jobs=jobs, T=T, D=T, delta_t_min=15, base_w=0,
                    tariff_paise=(500,) * T, name="w")


def test_workload_w_hand_computed_exact_and_power_independent():
    inst = _inst([{1: 2, 2: 3}, {1: 4, 2: 1}, {1: 5, 2: 5}], powers=(10_000, 20_000))
    assert workload_w(inst) == Fraction(2 + 1 + 5, 2 * 10)               # sum_j min_m p_jm / (M*T) = 8/20
    other = _inst([{1: 2, 2: 3}, {1: 4, 2: 1}, {1: 5, 2: 5}], powers=(1_000, 90_000))
    assert workload_w(other) == workload_w(inst)                          # machine powers do not enter W


def test_meta_and_formula_agree_for_sampled_full_design_cells():
    for task in enumerate_tasks(DESIGN_FULL)[::23]:
        inst, meta = generate_instance(DESIGN_FULL, task)
        by_hand = Fraction(sum(min(j.proc.values()) for j in inst.jobs), len(inst.machines) * inst.T)
        assert meta.w_real == round(float(by_hand), 6) == round(float(workload_w(inst)), 6)
        # integer rounding of <= n/2 slots can move W by at most n/(2*M*T)
        assert abs(meta.w_real - float(Fraction(meta.w_target))) <= len(inst.jobs) / (2 * len(inst.machines) * inst.T) + 0.02


def test_spec002_states_the_implemented_definition_only():
    text = (ROOT / "docs/handoff/SPEC-002-experiments.md").read_text()
    assert "Σ_j min_m p_jm / (M·T)" in text
    assert not re.search(r"min_m\(p_jm\s*·\s*P_jm\)", text), "energy-weighted W formula must not appear in SPEC-002"
    design_src = (ROOT / "07_src/experiments/design.py").read_text()
    assert "sum_j min_m p_jm / (M*D)" in design_src


# ------------------------------------------------------------------------------- design identity
def test_digest_changes_with_every_design_field_and_version():
    base = MICRO.digest()
    for change in (dict(seeds_per_cell=3), dict(solver_time_limit_s=21.0), dict(tiebreak_det_time_limit=5.0),
                   dict(rho_inr=("5", "51")), dict(base_seed=1), dict(name="other")):
        assert dataclasses.replace(MICRO, **change).digest() != base, change
    assert DESIGN_VERSION in json.dumps({"_design_version": DESIGN_VERSION})


@pytest.fixture(scope="module")
def run_a(tmp_path_factory):
    out = tmp_path_factory.mktemp("force_a")
    run_experiment(MICRO, out, **quiet)
    return out


def _rows(path):
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def test_changed_design_without_force_is_refused_and_leaves_files_untouched(run_a, tmp_path):
    work = tmp_path / "w"
    shutil.copytree(run_a, work)
    before = sorted(p.name for p in work.rglob("*"))
    with pytest.raises(RunnerError) as e:
        run_experiment(MICRO_B, work, **quiet)
    assert "different design" in str(e.value) and "--force" in str(e.value)
    assert sorted(p.name for p in work.rglob("*")) == before


def test_force_archives_old_results_and_never_reuses_them(run_a, tmp_path):
    work = tmp_path / "w"
    shutil.copytree(run_a, work)
    old_digest = MICRO.digest()
    old_parts = {p.name: p.read_bytes() for p in (work / "parts").glob("*.csv")}
    counts = run_experiment(MICRO_B, work, force=True, **quiet)
    assert counts == dict(total=3, skipped=0, ran=3)                      # nothing reused although ids overlap
    arch = work / "superseded" / old_digest
    assert {p.name: p.read_bytes() for p in (arch / "parts").glob("*.csv")} == old_parts   # kept, not deleted
    assert (arch / "manifest.json").exists() and (arch / "results.csv").exists()
    rows = _rows(work / "results.csv")
    assert {r["design_digest"] for r in rows} == {MICRO_B.digest()}
    assert json.loads((work / "manifest.json").read_text())["design_digest"] == MICRO_B.digest()
    assert {r["instance_id"] for r in rows} == {t.instance_id for t in enumerate_tasks(MICRO_B)}
    assert all(_rows(p)[0]["design_digest"] == MICRO_B.digest() for p in (work / "parts").glob("*.csv"))


def test_force_with_identical_design_does_not_discard_work(run_a, tmp_path):
    work = tmp_path / "w"
    shutil.copytree(run_a, work)
    counts = run_experiment(MICRO, work, force=True, **quiet)
    assert counts == dict(total=2, skipped=2, ran=0) and not (work / "superseded").exists()


def test_hand_edited_manifest_cannot_launder_old_parts(run_a, tmp_path):
    """Old parts + manifest edited to the new digest (the silent-reuse scenario) -> still refused."""
    work = tmp_path / "w"
    shutil.copytree(run_a, work)
    mf = json.loads((work / "manifest.json").read_text())
    mf["design_digest"] = MICRO_B.digest()
    (work / "manifest.json").write_text(json.dumps(mf))
    with pytest.raises(RunnerError) as e:
        run_experiment(MICRO_B, work, **quiet)
    assert "part file" in str(e.value)
    counts = run_experiment(MICRO_B, work, force=True, **quiet)           # force archives them
    assert counts["ran"] == 3 and counts["skipped"] == 0
    assert {r["design_digest"] for r in _rows(work / "results.csv")} == {MICRO_B.digest()}


def test_missing_manifest_with_existing_parts_is_refused(run_a, tmp_path):
    work = tmp_path / "w"
    shutil.copytree(run_a, work)
    (work / "manifest.json").unlink()
    (work / "results.csv").unlink()
    # same design but no manifest: parts carry the right digest -> accepted and resumed
    assert run_experiment(MICRO, work, **quiet) == dict(total=2, skipped=2, ran=0)
    # parts of a different design without manifest -> refused
    (work / "manifest.json").unlink()
    with pytest.raises(RunnerError):
        run_experiment(MICRO_B, work, **quiet)


def test_done_ids_only_counts_parts_of_the_requested_digest(run_a):
    assert done_ids(run_a) == done_ids(run_a, MICRO.digest()) and len(done_ids(run_a)) == 2
    assert done_ids(run_a, MICRO_B.digest()) == set()


def test_aggregate_refuses_mixed_designs_and_missing_manifest(run_a, tmp_path):
    work = tmp_path / "w"
    shutil.copytree(run_a, work)
    victim = sorted((work / "parts").glob("*.csv"))[0]
    rows = _rows(victim)
    for r in rows:
        r["design_digest"] = "deadbeefdeadbeef"
    with open(victim, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    with pytest.raises(RunnerError) as e:
        aggregate(work)
    assert "mixed designs" in str(e.value)
    (work / "manifest.json").unlink()
    with pytest.raises(RunnerError):
        aggregate(work)


def test_part_without_digest_column_is_treated_as_foreign(run_a, tmp_path):
    work = tmp_path / "w"
    shutil.copytree(run_a, work)
    victim = sorted((work / "parts").glob("*.csv"))[0]
    victim.write_text("instance_id,strategy\nx,A\n")                       # legacy / unknown format
    assert victim.stem not in done_ids(work, MICRO.digest())
    with pytest.raises(RunnerError):
        run_experiment(MICRO, work, **quiet)


# ------------------------------------------------------------------------------- flags in CSV rows
def test_row_keeps_primary_proven_and_proven_optimal_apart():
    res = types.SimpleNamespace(primary_proven=True, proven_stages=1, n_stages=3,
                                stage_statuses=["OPTIMAL", "FEASIBLE"], stage_values=[5, 7], wall_time_s=1.0,
                                num_workers=1, random_seed=0, metrics=None)
    row = _row({}, "B_minpeak", 0, "FEASIBLE", False, res)
    assert (row["proven_optimal"], row["primary_proven"], row["proven_stages"], row["n_stages"]) == (0, 1, 1, 3)
    assert row["stage_statuses"] == "OPTIMAL|FEASIBLE"
