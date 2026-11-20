"""Second calibration design (cal2-v1): separate, versioned, paired in rho; v1 designs and the pilot untouched."""
import csv
import dataclasses
import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

import pytest

from experiments.design import (CALIBRATION_VERSION, DESIGN_CAL2, DESIGN_FULL, DESIGN_SMOKE, DESIGN_VERSION, DESIGNS,
                                CalibrationDesign, enumerate_tasks, frac)
from experiments.generator import draw_instance, generate_instance, workload_w
from experiments.runner import run_experiment

ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "results" / "pilot27"
FULL_DIGEST = "c9af6944fe5da183"          # DESIGN_FULL, recorded 2026-11-15 before the calibration work
PILOT_DIGEST = "37af47cf7472c2c4"         # DESIGN_FULL with seeds_per_cell=1 (the executed 27-instance pilot)
PILOT_RESULTS_SHA256 = "516ee522cd874edf"  # first 16 hex of results/pilot27/results.csv as archived


# ---------------------------------------------------------------- v1 designs and the pilot are untouched
def test_v1_digests_are_pinned():
    assert DESIGN_FULL.digest() == FULL_DIGEST and DESIGN_FULL.version == DESIGN_VERSION == "SPEC-002/v1"
    assert dataclasses.replace(DESIGN_FULL, seeds_per_cell=1).digest() == PILOT_DIGEST
    assert DESIGN_FULL.workloads == ("0.40", "0.70", "0.90") and DESIGN_FULL.rho_inr == ("5", "14", "50")
    assert DESIGN_FULL.seeds_per_cell == 15 and len(enumerate_tasks(DESIGN_FULL)) == 405


@pytest.mark.skipif(not PILOT.exists(), reason="pilot outputs not present in this checkout")
def test_pilot_outputs_preserved_and_still_regenerable():
    assert json.loads((PILOT / "manifest.json").read_text())["design_digest"] == PILOT_DIGEST
    assert hashlib.sha256((PILOT / "results.csv").read_bytes()).hexdigest().startswith(PILOT_RESULTS_SHA256)
    with open(PILOT / "results.csv", newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 270 and {r["design_digest"] for r in rows} == {PILOT_DIGEST}
    meta = {r["instance_id"]: r for r in rows}
    d1 = dataclasses.replace(DESIGN_FULL, seeds_per_cell=1)
    for task in enumerate_tasks(d1)[::3]:                        # generator refactor must not change any instance
        _, m = generate_instance(d1, task)
        assert m.attempts == int(meta[task.instance_id]["gen_attempts"])
        assert m.w_real == pytest.approx(float(meta[task.instance_id]["w_real"]), abs=1e-9)


# ---------------------------------------------------------------- the calibration design
def test_cal2_is_separate_and_versioned():
    d = DESIGN_CAL2
    assert isinstance(d, CalibrationDesign) and d.name == "cal2-v1" and d.version == CALIBRATION_VERSION
    assert CALIBRATION_VERSION != DESIGN_VERSION
    assert d.digest() not in (FULL_DIGEST, PILOT_DIGEST, DESIGN_SMOKE.digest())
    assert d.base_seed != DESIGN_FULL.base_seed                   # independent draws, not a re-use of pilot instances
    # the registry may grow (SPEC-003 designs were added on 20 Nov); the original entries must stay exactly as they were
    assert {k: DESIGNS[k] for k in ("smoke", "full", "cal2")} == {"smoke": DESIGN_SMOKE, "full": DESIGN_FULL,
                                                                    "cal2": DESIGN_CAL2}
    # same instance size / tariff / power / budgets as v1 => comparable with the pilot
    for f in ("n_jobs", "n_machines", "T", "delta_t_min", "base_kw", "mean_power_kw", "shift_start_hour", "normal_inr",
              "proc_noise", "solver_time_limit_s", "solver_det_time_limit", "tiebreak_time_limit_s",
              "tiebreak_det_time_limit", "gammas", "cvs"):
        assert getattr(d, f) == getattr(DESIGN_FULL, f), f


def test_cal2_levels_counts_and_balance():
    d = DESIGN_CAL2
    assert d.workloads == ("0.40", "0.475", "0.55", "0.625", "0.70")
    assert d.rho_inr == ("1", "2", "5", "14", "50") and d.seeds_per_cell == 2
    ws = [frac(w) for w in d.workloads]
    assert ws[0] == Fraction(2, 5) and ws[-1] == Fraction(7, 10)
    assert {ws[i + 1] - ws[i] for i in range(4)} == {Fraction(3, 40)}      # equally spaced, anchors 0.40 / 0.70
    tasks = enumerate_tasks(d)
    assert len(tasks) == 5 * 3 * 3 * 2 == 90 and len({t.instance_id for t in tasks}) == 90
    cells = Counter((t.gamma_idx, t.w_idx, t.cv_idx) for t in tasks)
    assert len(cells) == 45 and set(cells.values()) == {2}                 # balanced: 2 seeds in every cell


def test_cal2_generation_filter_is_practically_inert_and_deterministic():
    """The heuristic acceptance filter is practically inert on the cal2 grid (W <= 0.70) but NOT absent: 89 of 90
    instances are the first draw; exactly one (W = 0.70) needed a second draw. Pinned so a change is noticed."""
    attempts = Counter()
    for t in enumerate_tasks(DESIGN_CAL2):
        inst, meta = generate_instance(DESIGN_CAL2, t)
        attempts[meta.attempts] += 1
        if meta.attempts > 1:
            assert meta.w_target == "0.70"
        assert inst == draw_instance(DESIGN_CAL2, t, meta.attempts)
        assert abs(meta.w_real - float(frac(meta.w_target))) <= 0.06
        assert meta.w_real == round(float(workload_w(inst)), 6)
    assert attempts == Counter({1: 89, 2: 1})
    t = enumerate_tasks(DESIGN_CAL2)[7]
    assert generate_instance(DESIGN_CAL2, t) == generate_instance(DESIGN_CAL2, t)


def test_draw_instance_is_the_stream_used_by_generate_instance():
    d = dataclasses.replace(DESIGN_FULL, seeds_per_cell=1)
    for t in enumerate_tasks(d)[::5]:
        inst, meta = generate_instance(d, t)
        assert inst == draw_instance(d, t, meta.attempts)                  # the accepted draw is exactly attempt k


# ---------------------------------------------------------------- paired rho + versions in a tiny run
MICRO = CalibrationDesign(name="cal-micro", gammas=("19/14",), workloads=("0.40",), cvs=("0.35",),
                          rho_inr=("1", "2", "5"), seeds_per_cell=2, n_jobs=4, n_machines=2, T=16,
                          solver_time_limit_s=20, solver_det_time_limit=8, tiebreak_time_limit_s=10,
                          tiebreak_det_time_limit=4)


def test_micro_calibration_run_keeps_rho_paired_and_versioned(tmp_path):
    run_experiment(MICRO, tmp_path, progress=lambda *_: None)
    with open(tmp_path / "results.csv", newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert {r["design_version"] for r in rows} == {CALIBRATION_VERSION}
    assert json.loads((tmp_path / "manifest.json").read_text())["design_version"] == CALIBRATION_VERSION
    by_inst = {}
    for r in rows:
        if r["strategy"] == "C":
            by_inst.setdefault(r["instance_id"], []).append(int(r["rho_paise"]))
    assert len(by_inst) == 2 and all(sorted(v) == [100, 200, 500] for v in by_inst.values())  # every rho on every instance
    for iid in by_inst:                       # rho-independent strategies are solved exactly once per instance
        assert sum(r["strategy"] == "A" and r["instance_id"] == iid for r in rows) == 1


def test_cli_accepts_cal2_but_nothing_is_run_by_tests():
    import subprocess, sys
    out = subprocess.run([sys.executable, str(ROOT / "07_src/scripts/run_experiment.py"), "--help"],
                         capture_output=True, text=True)
    assert out.returncode == 0 and "cal2" in out.stdout
