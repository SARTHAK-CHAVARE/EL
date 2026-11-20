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

from model import (SolveStatus, SolverConfig, best_for_rho, break_even, ec_peak_front, evaluate_schedule, inr_to_paise,
                   recommend, solve_min_peak, solve_strategy_a, solve_strategy_b, solve_strategy_c,
                   structural_peak_lower_bound, tec_lower_bound)

from .baselines import energy_greedy_schedule, fcfs_schedule, peak_capped_candidates, spt_schedule
from .design import MAIN_VERSION, Design, MainDesign, Task, enumerate_tasks
from .generator import generate_instance

COLUMNS = [
    "design_version", "design_digest", "instance_id", "gamma", "w_target", "w_real", "cv", "seed_idx",
    "gen_attempts", "n_jobs", "n_machines", "T", "delta_t_min", "tariff_off_paise", "tariff_normal_paise",
    "tariff_peak_paise", "strategy", "rho_paise", "status", "proven_optimal", "primary_proven", "proven_stages", "n_stages",
    "stage_statuses",
    "stage_values", "makespan", "sum_completion", "peak_w", "energy_w_min", "ec_int", "dc_int", "tec_int",
    "wall_time_s", "num_workers", "random_seed",
]
#: SPEC-003 rows carry these additional columns (old designs keep exactly COLUMNS).
COLUMNS_MAIN = COLUMNS + [
    "task_wall_s", "task_cpu_s", "front_label", "cap_w", "front_point_idx", "front_complete", "front_termination",
    "front_n_points", "front_n_solves", "required_proven", "ec_proven", "peak_proven", "makespan_proven",
    "structural_peak_lb_w", "tec_lower_bound", "gap", "choice", "rule_cap_w",
    "break_even_inr", "break_even_kind", "break_even_ref",
]
#: columns that legitimately differ between identical runs (machine speed); excluded when checking determinism
NONDETERMINISTIC_COLUMNS = ("wall_time_s", "task_wall_s", "task_cpu_s")


def columns_for(design_or_version) -> List[str]:
    v = design_or_version if isinstance(design_or_version, str) else design_or_version.version
    return COLUMNS_MAIN if v == MAIN_VERSION else COLUMNS


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
    if isinstance(design, MainDesign):
        return run_task_main(design, task)
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


def derived_c_status(front_complete: bool, makespan_proven: bool) -> tuple:
    """(status, proven_stages) of C(rho) read off the front, with the direct-C semantics (stage 1 TEC, stage 2 C_max):
    TEC is proven only if the front is complete; OPTIMAL needs the makespan tie-break proven as well."""
    stages = (1 if front_complete else 0) + (1 if front_complete and makespan_proven else 0)
    return ("OPTIMAL" if stages == 2 else "FEASIBLE"), stages


def _required_proven(label: str, res) -> bool:
    if label == "cap":
        return res.proven_stages >= 1 or res.status == SolveStatus.INFEASIBLE
    return res.proven_stages >= 1        # top: EC stage; P: min-peak stage


def run_task_main(design: MainDesign, task: Task) -> List[Dict]:
    """SPEC-003 protocol (docs/handoff/SPEC-003-main-study.md section 5). Every solve and every derived quantity is
    a row; nothing is dropped. Statuses: solver rows keep CP-SAT's status; derived rows are OPTIMAL only when proven."""
    w0, c0 = time.perf_counter(), time.process_time()
    inst, meta = generate_instance(design, task)
    cfg = _solver_config(design)
    base = dict(
        design_version=design.version, design_digest=design.digest(), instance_id=meta.instance_id,
        gamma=meta.gamma, w_target=meta.w_target, w_real=meta.w_real, cv=meta.cv, seed_idx=meta.seed_idx,
        gen_attempts=meta.attempts, n_jobs=len(inst.jobs), n_machines=len(inst.machines), T=inst.T,
        delta_t_min=inst.delta_t_min, tariff_off_paise=meta.off_paise, tariff_normal_paise=meta.normal_paise,
        tariff_peak_paise=meta.peak_paise, structural_peak_lb_w=structural_peak_lower_bound(inst))
    rows: List[Dict] = []
    a, b = solve_strategy_a(inst, cfg), solve_strategy_b(inst, cfg)
    bmin = solve_strategy_b(inst, cfg, "min_peak")
    for res in (a, b, bmin):
        rows.append(_row(base, res.strategy, 0, res.status.value, res.proven_optimal, res))
    front = ec_peak_front(inst, cfg)
    fx = dict(front_complete=int(front.complete), front_termination=front.termination,
              front_n_points=len(front.points), front_n_solves=front.n_solves)
    for s in front.solves:
        r = _row(base, "P" if s.label == "P" else f"FRONT_{s.label}", 0, s.result.status.value,
                 s.result.proven_optimal, s.result)
        r.update(fx, front_label=s.label, cap_w="" if s.cap_w is None else s.cap_w,
                 required_proven=int(_required_proven(s.label, s.result)))
        rows.append(r)
    for i, p in enumerate(front.points):
        r = _row(base, "FRONT_PT", 0, "POINT", bool(front.complete and p.ec_proven), metrics=p.metrics)
        r.update(fx, front_label=p.source, front_point_idx=i, cap_w="" if p.cap_w is None else p.cap_w,
                 ec_proven=int(p.ec_proven), peak_proven=int(p.peak_proven), makespan_proven=int(p.makespan_proven))
        rows.append(r)
    rho_x = inr_to_paise(design.cross_check_rho_inr)
    c_direct = solve_strategy_c(inst, rho_x, cfg)
    rows.append(_row(base, "C", rho_x, c_direct.status.value, c_direct.proven_optimal, c_direct))
    rule_scheds = {}
    for name, fn in (("FCFS", fcfs_schedule), ("SPT", spt_schedule), ("EG", energy_greedy_schedule)):
        t0 = time.perf_counter()
        sched = fn(inst)
        wall = time.perf_counter() - t0
        rule_scheds[name] = sched
        rows.append(_row(base, name, 0, "NO_SCHEDULE", False, wall=wall) if sched is None else
                    _row(base, name, 0, "HEURISTIC", False, metrics=evaluate_schedule(inst, sched, 0), wall=wall))
    t0 = time.perf_counter()
    pcg_cands = [(cap, sched, evaluate_schedule(inst, sched, 0)) for cap, sched in peak_capped_candidates(inst)]
    pcg_wall = time.perf_counter() - t0
    for rho_inr in design.rho_inr:
        rho = inr_to_paise(rho_inr)
        lb = tec_lower_bound(front, rho)
        pt = best_for_rho(front, rho)
        if pt is None:
            r = _row(base, "C_front", rho, "NO_SCHEDULE", False)
        else:
            st, stages = derived_c_status(front.complete, pt.makespan_proven)
            r = _row(base, "C_front", rho, st, st == "OPTIMAL", metrics=evaluate_schedule(inst, pt.schedule, rho))
            r.update(proven_stages=stages, n_stages=2, primary_proven=int(front.complete),
                     front_point_idx=front.points.index(pt),
                     gap="" if lb is None else repr(float((r["tec_int"] - lb) / r["tec_int"])))
        r.update(fx, tec_lower_bound="" if lb is None else lb)
        rows.append(r)
        pcg = None
        if pcg_cands:
            pcg = min(enumerate(pcg_cands),
                      key=lambda kv: (kv[1][2].ec_int + 60 * rho * kv[1][2].peak_w, kv[1][2].makespan, kv[0]))[1]
        if pcg is None:
            rows.append(_row(base, "PCG", rho, "NO_SCHEDULE", False, wall=pcg_wall))
        else:
            r = _row(base, "PCG", rho, "HEURISTIC", False, metrics=evaluate_schedule(inst, pcg[1], rho), wall=pcg_wall)
            r["rule_cap_w"] = "" if pcg[0] is None else pcg[0]
            rows.append(r)
        cands = {"B": b.schedule, "B_minpeak": bmin.schedule, "A": a.schedule, "EG": rule_scheds["EG"],
                 "PCG": None if pcg is None else pcg[1], "FCFS": rule_scheds["FCFS"], "SPT": rule_scheds["SPT"],
                 "C": c_direct.schedule if rho == rho_x else None}
        try:
            g = recommend(inst, rho, front, cands)
            r = _row(base, "GUARD", rho, "OPTIMAL" if g.proven_optimal else "FEASIBLE", g.proven_optimal,
                     metrics=g.metrics)
            r.update(choice=g.choice, tec_lower_bound="" if g.tec_lower_bound is None else g.tec_lower_bound,
                     gap="" if g.gap is None else repr(float(g.gap)))
        except ValueError:
            r = _row(base, "GUARD", rho, "NO_SCHEDULE", False)
        r.update(fx)
        rows.append(r)
    for ref_name, ref in (("B", b), ("B_minpeak", bmin)):
        if ref.metrics is None:
            r = _row(base, f"BE_{ref_name}", 0, "UNDETERMINED", False)
            r.update(break_even_kind="undetermined", break_even_ref=ref_name)
        else:
            be = break_even(front, ref.metrics.ec_int, ref.metrics.peak_w, ref_name)
            r = _row(base, f"BE_{ref_name}", 0, be.kind.upper(), be.is_exact)
            r.update(break_even_inr="" if be.rho_inr is None else str(be.rho_inr), break_even_kind=be.kind,
                     break_even_ref=ref_name, peak_w="" if be.via_peak_w is None else be.via_peak_w)
        r.update(fx)
        rows.append(r)
    task_wall, task_cpu = round(time.perf_counter() - w0, 4), round(time.process_time() - c0, 4)
    for r in rows:
        r.update(task_wall_s=task_wall, task_cpu_s=task_cpu)
    return rows


# --- atomic part files ---------------------------------------------------------------------------

def _part_path(out: Path, instance_id: str) -> Path:
    return out / "parts" / f"{instance_id}.csv"


def _write_part(out: Path, instance_id: str, rows: Sequence[Dict], columns: Sequence[str] = COLUMNS) -> None:
    final = _part_path(out, instance_id)
    tmp = final.with_name(f".{final.name}.tmp.{os.getpid()}")
    with open(tmp, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(columns), restval="")
        w.writeheader()
        w.writerows(rows)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, final)


def _worker(args):
    design, task, out = args
    rows = run_task(design, task)
    _write_part(Path(out), task.instance_id, rows, columns_for(design))
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
            _write_part(out, t.instance_id, run_task(design, t), columns_for(design))
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
    manifest = json.loads(mf.read_text())
    digest = manifest["design_digest"]
    columns = columns_for(manifest.get("design_version", ""))
    bad = _foreign_parts(out, digest)
    if bad:
        raise RunnerError(f"{len(bad)} part file(s) in {out / 'parts'} do not belong to design {digest} "
                          f"(e.g. {bad[0].name}); refusing to aggregate mixed designs")
    rows = []
    for p in sorted((out / "parts").glob("*.csv")):
        with open(p, newline="") as fh:
            rows.extend(csv.DictReader(fh))
    def _int(v):
        return int(v) if v not in (None, "") else -1
    rows.sort(key=lambda r: (r["instance_id"], r["strategy"], int(r["rho_paise"]), _int(r.get("front_point_idx")),
                             -_int(r.get("cap_w"))))
    dest = out / "results.csv"
    tmp = dest.with_suffix(".csv.tmp")
    with open(tmp, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=columns, restval="")
        w.writeheader()
        w.writerows(rows)
    os.replace(tmp, dest)
    return dest
