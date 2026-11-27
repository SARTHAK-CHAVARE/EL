"""Wrapper for the main run on another machine (07_src/scripts/run_main.py): comparison logic and records."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "07_src" / "scripts"))
sys.path.insert(0, str(ROOT / "07_src"))

import run_main  # noqa: E402
from experiments.design import DESIGNS, enumerate_tasks  # noqa: E402


def test_compare_ignores_timing_only():
    e = [{"strategy": "B", "ec_int": "10", "wall_time_s": "1.0", "task_cpu_s": "2"}]
    g = [{"strategy": "B", "ec_int": "10", "wall_time_s": "9.9", "task_cpu_s": "7"}]
    assert run_main.compare_rows(e, g) == []


def test_compare_detects_value_status_and_row_count_changes():
    e = [{"strategy": "C", "status": "OPTIMAL", "tec_int": "5"}]
    assert run_main.compare_rows(e, [{"strategy": "C", "status": "FEASIBLE", "tec_int": "5"}])
    assert run_main.compare_rows(e, [{"strategy": "C", "status": "OPTIMAL", "tec_int": "6"}])
    assert run_main.compare_rows(e, e + e) == ["row count 2 != expected 1"]


def test_check_instances_exist_in_smoke_designs_and_committed_results():
    for name, ids in run_main.CHECK_IDS.items():
        known = {t.instance_id for t in enumerate_tasks(DESIGNS[name])}
        for iid in ids:
            assert iid in known
            assert (ROOT / run_main.SMOKE_DIRS[name] / "parts" / f"{iid}.csv").exists()


def test_blocks_are_the_spec003_commands():
    assert run_main.BLOCKS == (("main-m3", "results/main_m3"), ("main-m4", "results/main_m4"))
    assert DESIGNS["main-m3"].digest() == "56e0f2f2f3455ffd"
    assert DESIGNS["main-m4"].digest() == "e5bfe31d5230171c"


def test_environment_record_is_json_and_has_versions():
    env = run_main.environment(3)
    json.dumps(env)
    assert env["workers"] == 3 and env["ortools"] == "9.15.6755" and env["packages"]
