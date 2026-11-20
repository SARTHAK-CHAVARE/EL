import csv
import dataclasses
import shutil
from pathlib import Path

import pytest

from experiments.baselines import fcfs_schedule, spt_schedule
from experiments.design import DESIGN_FULL, Design, enumerate_tasks, frac
from experiments.generator import (GeneratorError, generate_instance, machine_powers_w, tariff_levels_paise)
from experiments.runner import COLUMNS, NONDETERMINISTIC_COLUMNS, RunnerError, aggregate, done_ids, run_experiment
from model import (SolveStatus, SolverConfig, check_schedule, evaluate_schedule, solve_strategy_a,
                   solve_strategy_b, solve_strategy_c, validate_instance)
from benchmark_instance import benchmark_instance
from oracle import random_instance

MICRO = Design(name="micro", gammas=("19/14",), workloads=("0.40",), cvs=("0.35",), rho_inr=("5", "50"),
               seeds_per_cell=2, n_jobs=4, n_machines=2, T=16, solver_time_limit_s=20, solver_det_time_limit=8,
               tiebreak_time_limit_s=10, tiebreak_det_time_limit=4)


# ------------------------------------------------------------------ baselines
def test_fcfs_spt_hand_simulation_on_benchmark():
    inst = benchmark_instance()
    f, s = fcfs_schedule(inst), spt_schedule(inst)
    assert [(o.job_id, o.machine_id, o.start, o.end) for o in f] == [
        ("J1", 1, 1, 2), ("J4", 1, 3, 5), ("J2", 2, 1, 2), ("J3", 2, 3, 3)]
    assert [(o.job_id, o.machine_id, o.start, o.end) for o in s] == [
        ("J1", 1, 1, 2), ("J4", 1, 3, 5), ("J3", 2, 1, 1), ("J2", 2, 2, 3)]
    for sched in (f, s):
        assert check_schedule(inst, sched) == []
        assert evaluate_schedule(inst, sched, 0).makespan == 5


def test_baseline_fails_gracefully_when_deadline_too_tight():
    inst = dataclasses.replace(benchmark_instance(), D=3)
    assert fcfs_schedule(inst) is None and spt_schedule(inst) is None


@pytest.mark.parametrize("seed", range(25))
def test_baselines_never_beat_optimal_strategies(seed):
    inst = random_instance(seed)
    cfg = SolverConfig(num_workers=1, deterministic_time_limit=None)
    rho = 1500
    a, b, c = solve_strategy_a(inst, cfg), solve_strategy_b(inst, cfg), solve_strategy_c(inst, rho, cfg)
    for fn in (fcfs_schedule, spt_schedule):
        sched = fn(inst)
        if sched is None:
            continue
        assert a.status == SolveStatus.OPTIMAL            # a feasible schedule exists
        assert check_schedule(inst, sched) == []
        m = evaluate_schedule(inst, sched, rho)
        assert m.makespan >= a.metrics.makespan
        assert m.ec_int >= b.metrics.ec_int
        assert m.tec_int >= c.metrics.tec_int


# ------------------------------------------------------------------ generator
def test_kerc_tariff_levels_reproduced_exactly():
    assert tariff_levels_paise(frac("19/14"), "6.60") == (560, 660, 760)
    assert tariff_levels_paise(frac("1"), "6.60") == (660, 660, 660)
    off, normal, peak = tariff_levels_paise(frac("7/4"), "6.60")
    assert (off, normal, peak) == (480, 660, 840) and peak / off == 1.75


def test_machine_powers_mean_and_cv():
    assert machine_powers_w(3, "15", frac("0")) == (15000,) * 3
    p = machine_powers_w(3, "15", frac("0.35"))
    mean = sum(p) / 3
    sd = (sum((x - mean) ** 2 for x in p) / 3) ** 0.5
    assert abs(mean - 15000) < 2 and abs(sd / mean - 0.35) < 0.001


def test_generator_deterministic_valid_and_close_to_target_workload():
    for task in enumerate_tasks(DESIGN_FULL)[::37]:
        i1, m1 = generate_instance(DESIGN_FULL, task)
        i2, m2 = generate_instance(DESIGN_FULL, task)
        assert i1 == i2 and m1 == m2
        validate_instance(i1)
        assert abs(m1.w_real - float(frac(m1.w_target))) < 0.1
        assert len(i1.tariff_paise) == 32 and set(i1.tariff_paise) <= {m1.off_paise, m1.normal_paise, m1.peak_paise}
        assert fcfs_schedule(i1) is not None or spt_schedule(i1) is not None


def test_generator_seeds_differ_and_infeasible_target_raises():
    t = enumerate_tasks(MICRO)
    assert generate_instance(MICRO, t[0])[0] != generate_instance(MICRO, t[1])[0]
    impossible = dataclasses.replace(MICRO, workloads=("3.00",), max_attempts=5)
    with pytest.raises(GeneratorError) as e:
        generate_instance(impossible, enumerate_tasks(impossible)[0])
    assert "could not generate" in str(e.value)


def test_full_design_size():
    assert len(enumerate_tasks(DESIGN_FULL)) == 3 * 3 * 3 * 15


# ------------------------------------------------------------------ runner
def _load(out):
    with open(Path(out) / "results.csv", newline="") as fh:
        return list(csv.DictReader(fh))


def _stable(rows):
    return [{k: v for k, v in r.items() if k not in NONDETERMINISTIC_COLUMNS} for r in rows]


@pytest.fixture(scope="module")
def run_a(tmp_path_factory):
    out = tmp_path_factory.mktemp("run_a")
    counts = run_experiment(MICRO, out, workers=1, progress=lambda *_: None)
    return out, counts


def test_runner_outputs_structure(run_a):
    out, counts = run_a
    assert counts == dict(total=2, skipped=0, ran=2)
    rows = _load(out)
    assert list(rows[0].keys()) == COLUMNS
    strategies = {r["strategy"] for r in rows}
    assert strategies == {"A", "B", "B_minpeak", "B_maxpeak", "P", "C", "FCFS", "SPT"}
    assert len(rows) == 2 * (5 + 2 + 2)                 # per instance: 5 solves + C at 2 rho + 2 heuristics
    for r in rows:
        if r["strategy"] in ("A", "B", "C", "P") and r["status"] == "OPTIMAL":
            assert r["proven_optimal"] == "1" and r["primary_proven"] == "1"
        if r["status"] != "OPTIMAL" and r["strategy"] not in ("FCFS", "SPT"):
            assert r["proven_optimal"] == "0"
    # peak recorded for every solved row, tec = ec + 60*rho*peak
    for r in rows:
        if r["ec_int"]:
            assert int(r["tec_int"]) == int(r["ec_int"]) + 60 * int(r["rho_paise"]) * int(r["peak_w"])


def test_resume_skips_done_and_does_not_duplicate(run_a, tmp_path):
    out, _ = run_a
    work = tmp_path / "copy"
    shutil.copytree(out, work)
    before = _stable(_load(work))
    counts = run_experiment(MICRO, work, progress=lambda *_: None)
    assert counts == dict(total=2, skipped=2, ran=0)
    assert _stable(_load(work)) == before
    # simulate an interruption: one instance missing + a stale temp file from a killed worker
    victim = sorted(done_ids(work))[0]
    (work / "parts" / f"{victim}.csv").unlink()
    (work / "parts" / f".{victim}.csv.tmp.123").write_text("garbage")
    counts = run_experiment(MICRO, work, progress=lambda *_: None)
    assert counts == dict(total=2, skipped=1, ran=1)
    assert not list((work / "parts").glob(".*.tmp.*"))
    assert _stable(_load(work)) == before                # identical after resume (deterministic)


def test_deterministic_across_independent_runs_and_worker_counts(run_a, tmp_path):
    out, _ = run_a
    other = tmp_path / "parallel"
    run_experiment(MICRO, other, workers=2, progress=lambda *_: None)
    assert _stable(_load(other)) == _stable(_load(out))


def test_manifest_mismatch_is_refused_with_clear_message(run_a):
    out, _ = run_a
    changed = dataclasses.replace(MICRO, seeds_per_cell=3)
    with pytest.raises(RunnerError) as e:
        run_experiment(changed, out, progress=lambda *_: None)
    assert "different design" in str(e.value)
