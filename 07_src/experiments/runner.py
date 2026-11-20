"""Resumable, parallel-safe experiment runner (SPEC-002 section 5).

* One *task* = one generated instance; all strategies (A, B, B_minpeak, B_maxpeak, P, C at every rho,
  FCFS, SPT) are solved on it, which gives paired comparisons.
* Each finished task is written atomically to ``<out>/parts/<instance_id>.csv`` (temp file +
  ``os.replace``). A task is "done" iff its part file exists, so an interrupted run resumes without
  duplicating or losing work and parallel workers never touch the same file.
* ``aggregate`` merges the parts into one deterministic, sorted ``results.csv``.
* Design identity: every row carries ``design_digest``. A part file counts as done only if its digest equals the
  current design's; ``aggregate`` refuses to merge parts whose digest differs from the manifest. ``--force`` on a
  changed design never reuses old files: they are moved (not deleted) to ``<out>/superseded/<old digest>/`` and the
  run starts empty. Results of different designs therefore cannot be mixed.
"""
from __future__ import annotations

import csv
import dataclasses
import json
import multiprocessing as mp
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Optional, Sequence

from model import (SolverConfig, evaluate_schedule, inr_to_paise, solve_min_peak, solve_strategy_a,
                   solve_strategy_b, solve_strategy_c)

from .baselines import fcfs_schedule, spt_schedule
from .design import Design, Task, enumerate_tasks
from .generator import generate_instance

COLUMNS = [
    "design_version", "design_digest", "instance_id", "gamma", "w_target", "w_real", "cv", "seed_idx",
    "gen_attempts", "n_jobs", "n_machines", "T", "delta_t_min", "tariff_off_paise", "tariff_normal_paise",
    "tariff_peak_paise", "strategy", "rho_paise", "status", "proven_optimal", "primary_proven", "proven_stages", "n_stages",
    "stage_statuses",
    "stage_values", "makespan", "sum_completion", "peak_w", "energy_w_min", "ec_int", "dc_int", "tec_int",
    "wall_time_s", "num_workers", "random_seed",
]
#: columns that legitimately differ between identical runs (machine speed); excluded when checking determinism
NONDETERMINISTIC_COLUMNS = ("wall_time_s",)


class RunnerError(RuntimeError):
    pass


def _solver_config(design: Design) -> SolverConfig:
    return SolverConfig(time_limit_s=design.solver_time_limit_s,
                        deterministic_time_limit=design.solver_det_time_limit, num_workers=1, random_seed=0,
                        tiebreak_time_limit_s=design.tiebreak_time_limit_s,
                        tiebreak_deterministic_time_limit=design.tiebreak_det_time_limit)


def _row(base: Dict, strategy: str, rho_paise: int, status: str, proven: bool, res=None, metrics=None,
         wall: float = 0.0) -> Dict:
    r = dict(base, strategy=strategy, rho_paise=rho_paise, status=status, proven_optimal=int(proven),
             primary_proven=int(res.primary_proven) if res is not None else 0,
             proven_stages=res.proven_stages if res is not None else 0,
             n_stages=res.n_stages if res is not None else 0,
             stage_statuses="", stage_values="", makespan="", sum_completion="", peak_w="", energy_w_min="",
             ec_int="", dc_int="", tec_int="", wall_time_s=round(wall, 4), num_workers=1, random_seed=0)
    if res is not None:
        r["stage_statuses"] = "|".join(res.stage_statuses)
        r["stage_values"] = "|".join(str(v) for v in res.stage_values)
        r["wall_time_s"] = round(res.wall_time_s, 4)
        r["num_workers"], r["random_seed"] = res.num_workers, res.random_seed
        metrics = res.metrics
    if metrics is not None:
        r.update(makespan=metrics.makespan, sum_completion=metrics.sum_completion, peak_w=metrics.peak_w,
                 energy_w_min=metrics.energy_w_min, ec_int=metrics.ec_int, dc_int=metrics.dc_int,
                 tec_int=metrics.tec_int)
    return r


def run_task(design: Design, task: Task) -> List[Dict]:
    """Solve every strategy on one generated instance and return result rows."""
    inst, meta = generate_instance(design, task)
    cfg = _solver_config(design)
    base = dict(
        design_version=design.version, design_digest=design.digest(), instance_id=meta.instance_id,
        gamma=meta.gamma, w_target=meta.w_target, w_real=meta.w_real, cv=meta.cv, seed_idx=meta.seed_idx,
        gen_attempts=meta.attempts, n_jobs=len(inst.jobs), n_machines=len(inst.machines), T=inst.T,
        delta_t_min=inst.delta_t_min, tariff_off_paise=meta.off_paise, tariff_normal_paise=meta.normal_paise,
        tariff_peak_paise=meta.peak_paise)
    rows = []
    for res in (solve_strategy_a(inst, cfg), solve_strategy_b(inst, cfg),
                solve_strategy_b(inst, cfg, "min_peak"), solve_strategy_b(inst, cfg, "max_peak"),
                solve_min_peak(inst, cfg)):
        rows.append(_row(base, res.strategy, 0, res.status.value, res.proven_optimal, res))
    for rho_inr in design.rho_inr:
        rho = inr_to_paise(rho_inr)
        res = solve_strategy_c(inst, rho, cfg)
        rows.append(_row(base, "C", rho, res.status.value, res.proven_optimal, res))
    for name, fn in (("FCFS", fcfs_schedule), ("SPT", spt_schedule)):
        t0 = time.perf_counter()
        sched = fn(inst)
        wall = time.perf_counter() - t0
        if sched is None:
            rows.append(_row(base, name, 0, "NO_SCHEDULE", False, wall=wall))
        else:
            rows.append(_row(base, name, 0, "HEURISTIC", False, metrics=evaluate_schedule(inst, sched, 0),
                             wall=wall))
    return rows


# --- atomic part files ---------------------------------------------------------------------------

def _part_path(out: Path, instance_id: str) -> Path:
    return out / "parts" / f"{instance_id}.csv"


def _write_part(out: Path, instance_id: str, rows: Sequence[Dict]) -> None:
    final = _part_path(out, instance_id)
    tmp = final.with_name(f".{final.name}.tmp.{os.getpid()}")
    with open(tmp, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, final)


def _worker(args):
    design, task, out = args
    rows = run_task(design, task)
    _write_part(Path(out), task.instance_id, rows)
    return task.instance_id, len(rows)


def _part_digest(path: Path) -> Optional[str]:
    """design_digest recorded in a part file (None if unreadable / missing column)."""
    try:
        with open(path, newline="") as fh:
            first = next(csv.DictReader(fh), None)
    except (OSError, csv.Error):
        return None
    return None if first is None else first.get("design_digest")


def done_ids(out: Path, digest: Optional[str] = None) -> set:
    """Instance ids with a finished part file. With ``digest`` only parts of that design count."""
    d = Path(out) / "parts"
    if not d.exists():
        return set()
    return {p.stem for p in d.glob("*.csv") if digest is None or _part_digest(p) == digest}


def _foreign_parts(out: Path, digest: str) -> List[Path]:
    d = Path(out) / "parts"
    return sorted(p for p in d.glob("*.csv") if _part_digest(p) != digest) if d.exists() else []


def _archive_previous(out: Path, old_digest: str) -> Path:
    """Move parts/, results.csv and manifest.json of a previous design out of the way (nothing is deleted)."""
    dest = out / "superseded" / str(old_digest)
    n = 1
    while dest.exists():
        dest = out / "superseded" / f"{old_digest}.{n}"
        n += 1
    dest.mkdir(parents=True)
    for name in ("parts", "results.csv", "manifest.json"):
        if (out / name).exists():
            os.replace(out / name, dest / name)
    (out / "parts").mkdir(exist_ok=True)
    return dest


def _check_manifest(out: Path, design: Design, force: bool) -> None:
    """Guarantee that ``out`` only ever holds results of ``design`` (see module docstring)."""
    mf = out / "manifest.json"
    cur = dict(design_version=design.version, design_digest=design.digest(), design=dataclasses.asdict(design))
    digest = cur["design_digest"]
    old_digest = json.loads(mf.read_text()).get("design_digest") if mf.exists() else None
    foreign = _foreign_parts(out, digest)
    if old_digest not in (None, digest) or foreign:
        what = (f"manifest digest {old_digest}" if old_digest not in (None, digest)
                else f"{len(foreign)} part file(s) of another/unknown design (manifest missing or inconsistent)")
        if not force:
            raise RunnerError(
                f"{out} holds results from a different design ({what}; current digest {digest}). "
                f"Use a new --out directory, or --force to archive the old results to {out / 'superseded'} "
                f"and start this design from scratch (old files are never reused).")
        dest = _archive_previous(out, old_digest or "unknown")
        print(f"[runner] --force: previous results archived to {dest}", file=sys.stderr)
    mf.write_text(json.dumps(cur, indent=2, sort_keys=True))


def run_experiment(design: Design, out: Path, workers: int = 1, limit: Optional[int] = None,
                   force: bool = False, progress=print) -> Dict[str, int]:
    """Run (or resume) the experiment. Returns counts {total, skipped, ran}."""
    out = Path(out)
    (out / "parts").mkdir(parents=True, exist_ok=True)
    _check_manifest(out, design, force)
    for stale in (out / "parts").glob(".*.tmp.*"):      # leftovers of a killed run
        stale.unlink()
    tasks = enumerate_tasks(design)
    if limit is not None:
        tasks = tasks[:limit]
    done = done_ids(out, design.digest())
    todo = [t for t in tasks if t.instance_id not in done]
    counts = dict(total=len(tasks), skipped=len(tasks) - len(todo), ran=0)
    progress(f"[runner] design={design.name} digest={design.digest()} tasks={len(tasks)} "
             f"already_done={counts['skipped']} to_run={len(todo)} workers={workers}")
    if workers <= 1:
        for t in todo:
            _write_part(out, t.instance_id, run_task(design, t))
            counts["ran"] += 1
            progress(f"[runner] {counts['skipped'] + counts['ran']}/{len(tasks)} {t.instance_id}")
    else:
        ctx = mp.get_context("spawn")
        with ProcessPoolExecutor(max_workers=workers, mp_context=ctx) as ex:
            futs = {ex.submit(_worker, (design, t, str(out))): t for t in todo}
            try:
                for f in as_completed(futs):
                    iid, _ = f.result()
                    counts["ran"] += 1
                    progress(f"[runner] {counts['skipped'] + counts['ran']}/{len(tasks)} {iid}")
            except BaseException:
                for f in futs:
                    f.cancel()
                raise
    aggregate(out)
    return counts


def aggregate(out: Path) -> Path:
    """Merge part files into ``results.csv`` sorted by (instance_id, strategy, rho_paise).

    Refuses (RunnerError) if the manifest is missing or any part belongs to a different design digest."""
    out = Path(out)
    mf = out / "manifest.json"
    if not mf.exists():
        raise RunnerError(f"{mf} not found: cannot verify which design the parts belong to")
    digest = json.loads(mf.read_text())["design_digest"]
    bad = _foreign_parts(out, digest)
    if bad:
        raise RunnerError(f"{len(bad)} part file(s) in {out / 'parts'} do not belong to design {digest} "
                          f"(e.g. {bad[0].name}); refusing to aggregate mixed designs")
    rows = []
    for p in sorted((out / "parts").glob("*.csv")):
        with open(p, newline="") as fh:
            rows.extend(csv.DictReader(fh))
    rows.sort(key=lambda r: (r["instance_id"], r["strategy"], int(r["rho_paise"])))
    dest = out / "results.csv"
    tmp = dest.with_suffix(".csv.tmp")
    with open(tmp, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    os.replace(tmp, dest)
    return dest
