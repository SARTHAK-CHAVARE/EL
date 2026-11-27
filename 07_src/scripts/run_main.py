"""Run the SPEC-003 main study (M3, then M4) on any machine, with an environment record and a reproducibility check.

    python 07_src/scripts/run_main.py                 # workers: physical cores - 1 (estimated)
    python 07_src/scripts/run_main.py --workers 4

1. Appends this machine's environment (Python, OS, CPU, package versions, git commit, workers) to
   results/main_run/environment.json.
2. Reproducibility check: re-solves the 3 fastest smoke instances of each block and compares every result column except
   the timing columns with the committed smoke results (results/main_smoke). A mismatch stops the run before any main
   instance is solved; --accept-mismatch continues and records the mismatch.
3. Runs the SPEC-003 section 13 commands unchanged (run_experiment.py, main-m3 -> results/main_m3, main-m4 ->
   results/main_m4). All output is also appended to results/main_run/run_log.txt with UTC start/end per block.

Re-running the same command resumes: finished instances are skipped (the check is repeated; about 1-2 minutes).
"""
import argparse
import csv
import datetime as dt
import importlib.metadata as md
import json
import os
import platform
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "07_src"))

TIMING_COLUMNS = {"wall_time_s", "task_wall_s", "task_cpu_s"}
CHECK_IDS = {  # the 3 fastest smoke instances per block (by recorded wall time); see P4-SMOKE-RESULTS.md
    "main-m3-smoke": ("g0w0c0s000", "g0w3c0s000", "g0w2c0s000"),
    "main-m4-smoke": ("g0w2c0s001", "g0w2c0s000", "g0w0c0s000"),
}
SMOKE_DIRS = {"main-m3-smoke": "results/main_smoke/m3", "main-m4-smoke": "results/main_smoke/m4"}
BLOCKS = (("main-m3", "results/main_m3"), ("main-m4", "results/main_m4"))
RUN_DIR = ROOT / "results" / "main_run"


def utc() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def default_workers() -> int:
    return max(1, (os.cpu_count() or 2) // 2 - 1)


def _git(*args) -> str:
    try:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, timeout=30).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return "unavailable"


def environment(workers: int) -> dict:
    pkgs = sorted(f"{d.metadata['Name']}=={d.version}" for d in md.distributions() if d.metadata["Name"])
    return dict(
        recorded_utc=utc(), python=sys.version, executable=sys.executable, platform=platform.platform(),
        machine=platform.machine(), processor=platform.processor(), logical_cpus=os.cpu_count(), workers=workers,
        ortools=md.version("ortools"), git_commit=_git("rev-parse", "HEAD"),
        git_dirty_files=[ln for ln in _git("status", "--porcelain").splitlines() if ln and "results/main_" not in ln],
        packages=pkgs,
    )


def compare_rows(expected, got, ignore=TIMING_COLUMNS):
    """Differences between two row lists (list of dicts of strings), ignoring the given columns."""
    diffs = []
    if len(expected) != len(got):
        return [f"row count {len(got)} != expected {len(expected)}"]
    for i, (e, g) in enumerate(zip(expected, got)):
        for k in sorted(set(e) | set(g)):
            if k in ignore:
                continue
            if e.get(k, "") != g.get(k, ""):
                diffs.append(f"row {i} [{e.get('strategy', '')}] {k}: got {g.get(k, '')!r}, expected {e.get(k, '')!r}")
    return diffs


def _read(path: Path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def reproducibility_check(log) -> dict:
    from experiments.design import DESIGNS, enumerate_tasks
    from experiments.runner import _part_path, _write_part, columns_for, run_task

    report = {"checked_utc": utc(), "instances": {}, "passed": True}
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "parts").mkdir()
        for name, ids in CHECK_IDS.items():
            design = DESIGNS[name]
            tasks = {t.instance_id: t for t in enumerate_tasks(design)}
            for iid in ids:
                t0 = time.time()
                _write_part(Path(tmp), iid, run_task(design, tasks[iid]), columns_for(design))
                diffs = compare_rows(_read(_part_path(ROOT / SMOKE_DIRS[name], iid)), _read(_part_path(Path(tmp), iid)))
                ok = not diffs
                report["instances"][f"{name}/{iid}"] = {"match": ok, "diffs": diffs[:20], "wall_s": round(time.time() - t0, 1)}
                report["passed"] &= ok
                log(f"[check] {name}/{iid}: {'MATCH' if ok else 'MISMATCH'} ({time.time() - t0:.1f} s)")
                for d in diffs[:10]:
                    log(f"[check]   {d}")
    return report


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workers", type=int, default=default_workers())
    ap.add_argument("--accept-mismatch", action="store_true", help="continue even if the reproducibility check fails")
    ap.add_argument("--skip-check", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--limit", type=int, default=None, help=argparse.SUPPRESS)   # testing only
    a = ap.parse_args(argv)

    RUN_DIR.mkdir(parents=True, exist_ok=True)
    logf = open(RUN_DIR / "run_log.txt", "a", encoding="utf-8")

    def log(msg: str) -> None:
        print(msg, flush=True)
        logf.write(msg + "\n")
        logf.flush()

    env_path = RUN_DIR / "environment.json"
    record = json.loads(env_path.read_text(encoding="utf-8")) if env_path.exists() else {"invocations": []}
    inv = {"environment": environment(a.workers)}
    record["invocations"].append(inv)
    log(f"[main] {utc()} start; workers={a.workers}; python {platform.python_version()}; ortools "
        f"{inv['environment']['ortools']}; commit {inv['environment']['git_commit'][:7]}")

    def save():
        env_path.write_text(json.dumps(record, indent=2), encoding="utf-8")

    save()
    if not a.skip_check:
        inv["reproducibility_check"] = rep = reproducibility_check(log)
        save()
        if not rep["passed"]:
            log("[check] RESULT: MISMATCH with the smoke results produced on the reference machine.")
            if not a.accept_mismatch:
                log("[main] stopped before the main run. Send results/main_run/run_log.txt; do not rerun with "
                    "--accept-mismatch unless asked to.")
                save()
                return 3
            log("[main] --accept-mismatch given: continuing; the mismatch is recorded in environment.json.")
        else:
            log("[check] RESULT: all checked instances match the reference smoke results.")

    t_start = time.time()
    for design, out in BLOCKS:
        cmd = [sys.executable, str(ROOT / "07_src/scripts/run_experiment.py"), "--design", design, "--out", out,
               "--workers", str(a.workers)] + (["--limit", str(a.limit)] if a.limit else [])
        log(f"[main] block {design} start {utc()}")
        t0 = time.time()
        p = subprocess.Popen(cmd, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        for line in p.stdout:
            el = int(time.time() - t_start)
            log(f"{line.rstrip()}   [elapsed {el // 3600}:{el % 3600 // 60:02d}]")
        rc = p.wait()
        inv.setdefault("blocks", {})[design] = {"exit_code": rc, "wall_s": round(time.time() - t0), "end_utc": utc()}
        save()
        log(f"[main] block {design} end {utc()} exit={rc} wall={time.time() - t0:.0f} s")
        if rc != 0:
            log("[main] stopped: the block failed. Re-run the same command to resume, or send run_log.txt.")
            return rc
    log(f"[main] {utc()} finished both blocks in {(time.time() - t_start) / 3600:.2f} h.")
    log("[main] Next: git add results/main_m3 results/main_m4 results/main_run; git commit -m \"P5: main run\"; "
        "git push origin phase3-experiments")
    return 0


if __name__ == "__main__":
    sys.exit(main())
