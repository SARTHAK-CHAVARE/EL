"""P3 scaling probe and Gate 2 (ROADMAP-FINAL.md P3; decision D2).

    python 07_src/scripts/scaling_probe.py [--out results/scaling_probe] [--workers 2] [--sizes 8x3,12x4,16x5,20x6]

Sizes (jobs x machines) on the same 32-slot shift, gamma 19/14, W {0.40, 0.625} (below (M-1)/M for every size),
CV {0, 0.35}, 2 seeds, fresh base seed 20261121 (these instances are NOT reused by the main study). Budgets are the
Design defaults, identical to cal2 (stage 1: 60 det-s / 180 s wall; tie-breaks: 15 det-s / 60 s wall).

Per instance it runs the full main-study strategy set, so both proof rates and the cost of an M2 block are measured:
A, B, B_minpeak, the energy-peak front (top, P, capped solves), direct C at rho = 14 (cross-check of the front at
larger sizes), FCFS, energy-greedy, peak-capped greedy, and the safety guard at rho = 14 ONLY. (The guard evaluates
schedules at integer paise; the KERC-equivalent rho, 350/26 INR/kW, is fractional and is NOT evaluated by this probe.)

Result identity: every part file stores ``digest`` = hash(probe protocol, size design digest, solver config). An
existing part is reused only if its digest equals the current one; otherwise the run stops (StaleProbeResult) instead
of reusing it. Parts written before digests existed (commit 5d363fa) are accepted only through the "legacy" entry of
``manifest.json``, which records the digest of the code that produced them; any later change to the design or budgets
changes the current digest and those parts are then rejected too.

Completeness: ``aggregate`` enumerates every expected instance of every size. Missing or unreadable parts are listed
per size; such a size gets gate2_pass = None ("incomplete") and can never be selected as M2.

Gate 2 (approved D2): a size qualifies for a larger machine-count block only if >= 90 % of the REQUIRED front solves
are proven (top: EC stage; capped solves: EC stage or proven infeasible; P: min-peak stage, when solved). The share of
complete (exact) fronts is reported beside it. Nothing is dropped: every solve and status is in parts/*.json.
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import statistics
import sys
import time
from fractions import Fraction
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from experiments.baselines import (energy_greedy_schedule, fcfs_schedule, peak_capped_greedy_schedule)  # noqa: E402
from experiments.design import Design, enumerate_tasks  # noqa: E402
from experiments.generator import generate_instance  # noqa: E402
from experiments.runner import _solver_config  # noqa: E402
from model import (SolveStatus, break_even, ec_peak_front, recommend, solve_strategy_a, solve_strategy_b,  # noqa: E402
                   solve_strategy_c, structural_peak_lower_bound)

ROOT = Path(__file__).resolve().parents[2]
BASE_SEED = 20261121
GATE_SHARE = 0.90
PROTOCOL = "P3/v1"


class StaleProbeResult(RuntimeError):
    pass


def probe_design(n: int, m: int) -> Design:
    return Design(name=f"probe-{n}x{m}", gammas=("19/14",), workloads=("0.40", "0.625"), cvs=("0", "0.35"),
                  rho_inr=("14",), seeds_per_cell=2, n_jobs=n, n_machines=m, base_seed=BASE_SEED)


def probe_digest(n: int, m: int) -> str:
    """Identity of a probe size: protocol, the size's design digest and the solver configuration."""
    d = probe_design(n, m)
    payload = dict(protocol=PROTOCOL, design_digest=d.digest(), solver=dataclasses.asdict(_solver_config(d)))
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()[:16]


def _load_manifest(out: Path) -> dict:
    mf = out / "manifest.json"
    return json.loads(mf.read_text()) if mf.exists() else {}


def part_digest(rec: dict, size: str, manifest: dict):
    """Digest of a part: its own field, or (pre-digest parts only) the manifest's legacy entry for its size."""
    if "digest" in rec:
        return rec["digest"]
    return manifest.get("legacy", {}).get("digest_by_size", {}).get(size)


def _check_existing(path: Path, n: int, m: int, out: Path) -> bool:
    """True if a valid part for the CURRENT digest exists; raises StaleProbeResult for a stale one."""
    if not path.exists():
        return False
    rec = json.loads(path.read_text())
    got, want = part_digest(rec, f"{n}x{m}", _load_manifest(out)), probe_digest(n, m)
    if got != want:
        raise StaleProbeResult(f"{path.name}: part digest {got} != current {want}; use a new --out directory")
    return True


def _res(r, rho_paise=0):
    m = r.metrics
    return dict(status=r.status.value, stage_statuses=r.stage_statuses, proven_stages=r.proven_stages,
                n_stages=r.n_stages, time_s=sum(r.stage_times_s),
                ec_int=m.ec_int if m else None, peak_w=m.peak_w if m else None, makespan=m.makespan if m else None,
                tec_int=(m.ec_int + 60 * rho_paise * m.peak_w) if m else None)


def run_one(args):
    n, m, task, out = args
    path = out / "parts" / f"{n}x{m}_{task.instance_id}.json"
    if _check_existing(path, n, m, out):
        return path.name
    d = probe_design(n, m)
    cfg = _solver_config(d)
    t0 = time.perf_counter()
    inst, meta = generate_instance(d, task)
    rec = dict(digest=probe_digest(n, m), size=f"{n}x{m}", n_jobs=n, n_machines=m, instance_id=task.instance_id, w_target=meta.w_target,
               w_real=meta.w_real, cv=meta.cv, gamma=meta.gamma, seed_idx=meta.seed_idx, attempts=meta.attempts,
               structural_peak_lb_w=structural_peak_lower_bound(inst), max_peak_w=inst.base_w + sum(meta.machine_power_w))
    a = solve_strategy_a(inst, cfg)
    b = solve_strategy_b(inst, cfg)
    bmin = solve_strategy_b(inst, cfg, tie_break="min_peak")
    f = ec_peak_front(inst, cfg)
    c14 = solve_strategy_c(inst, 1400, cfg)
    rec.update(A=_res(a), B=_res(b), B_minpeak=_res(bmin), C14=_res(c14, 1400))
    req = []
    for s in f.solves:
        r = s.result
        if s.label == "top":
            ok = r.proven_stages >= 1
        elif s.label == "cap":
            ok = r.proven_stages >= 1 or r.status == SolveStatus.INFEASIBLE
        else:   # P: its min-peak value certifies termination
            ok = r.proven_stages >= 1
        req.append(dict(label=s.label, cap_w=s.cap_w, status=r.status.value, stage_statuses=r.stage_statuses,
                        time_s=sum(r.stage_times_s), required_proven=ok))
    rec["front"] = dict(complete=f.complete, termination=f.termination, reason=f.reason, n_points=len(f.points),
                        n_solves=f.n_solves, time_s=sum(x["time_s"] for x in req), solves=req,
                        points=[dict(peak_w=p.peak_w, ec_int=p.ec_int, makespan=p.makespan, ec_proven=p.ec_proven)
                                for p in f.points])
    if b.metrics:
        be = break_even(f, b.metrics.ec_int, b.metrics.peak_w, "B")
        rec["break_even_B"] = dict(rho_inr=None if be.rho_inr is None else str(be.rho_inr), kind=be.kind)
    # cross-check: front-derived C at rho 14 vs direct C
    if f.points and c14.metrics:
        fc = min(p.ec_int + 60 * 1400 * p.peak_w for p in f.points)
        rec["c14_check"] = dict(front_tec=fc, direct_tec=rec["C14"]["tec_int"],
                                comparable=f.complete and c14.proven_stages >= 1,
                                equal=fc == rec["C14"]["tec_int"],
                                front_better=fc < rec["C14"]["tec_int"])
    fc_s, eg = fcfs_schedule(inst), energy_greedy_schedule(inst)
    rec["rules"] = dict(fcfs_ok=fc_s is not None, eg_ok=eg is not None)
    guard = {}
    for label, rho in (("14", 1400),):            # rho = 14 only (see module docstring)
        cands = {"B": b.schedule, "B_minpeak": bmin.schedule, "C14": c14.schedule if rho == 1400 else None,
                 "FCFS": fc_s, "EG": eg, "PCG": peak_capped_greedy_schedule(inst, rho)}
        if f.points or any(v is not None for v in cands.values()):
            g = recommend(inst, rho, f, cands)
            guard[label] = dict(choice=g.choice, tec_int=g.metrics.tec_int, lb=g.tec_lower_bound,
                                gap_pct=None if g.gap is None else float(g.gap * 100), proven=g.proven_optimal,
                                candidate_tec=g.candidate_tec)
    rec["guard"] = guard
    rec["total_solver_time_s"] = sum(rec[k]["time_s"] for k in ("A", "B", "B_minpeak", "C14")) + rec["front"]["time_s"]
    rec["wall_s"] = time.perf_counter() - t0
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(rec, indent=1, default=str))
    tmp.replace(path)
    return path.name


def aggregate(out: Path, sizes=None) -> dict:
    """Summarise every expected instance of ``sizes`` (default: the sizes recorded in the manifest, else those found).

    Never drops anything silently: missing / unreadable parts are listed per size, a size with any missing part gets
    gate2_pass = None, and a part whose digest does not match the current probe digest raises StaleProbeResult."""
    manifest = _load_manifest(out)
    if sizes is None:
        sizes = manifest.get("sizes") or sorted({p.name.split("_")[0] for p in (out / "parts").glob("*.json")})
    sizes = sorted(sizes, key=lambda s: tuple(int(x) for x in s.split("x")))
    recs, missing = [], {}
    for s in sizes:
        n, m = (int(x) for x in s.split("x"))
        want = probe_digest(n, m)
        missing[s] = []
        for t in enumerate_tasks(probe_design(n, m)):
            p = out / "parts" / f"{s}_{t.instance_id}.json"
            try:
                rec = json.loads(p.read_text())
            except (OSError, ValueError):
                missing[s].append(t.instance_id)
                continue
            got = part_digest(rec, s, manifest)
            if got != want:
                raise StaleProbeResult(f"{p.name}: digest {got} != current {want}; refusing to aggregate")
            recs.append(rec)
    summ = {}
    for s in sizes:
        rs = [r for r in recs if r["size"] == s]
        if not rs:
            summ[s] = dict(instances=0, expected=len(missing[s]), missing=missing[s], gate2_pass=None)
            continue
        req = [x for r in rs for x in r["front"]["solves"]]
        share = sum(x["required_proven"] for x in req) / len(req) if req else 0.0
        checks = [r["c14_check"] for r in rs if "c14_check" in r]
        comp = [c for c in checks if c["comparable"]]
        t = [r["total_solver_time_s"] for r in rs]
        ft = [r["front"]["time_s"] for r in rs]
        gaps = [r["guard"]["14"]["gap_pct"] for r in rs if "14" in r["guard"] and r["guard"]["14"]["gap_pct"] is not None]
        summ[s] = dict(
            instances=len(rs), expected=len(rs) + len(missing[s]), missing=missing[s], required_front_solves=len(req), required_proven_share=share,
            complete_fronts=sum(r["front"]["complete"] for r in rs),
            terminations={k: sum(r["front"]["termination"] == k for r in rs) for k in
                          sorted({r["front"]["termination"] for r in rs})},
            front_points={k: sum(r["front"]["n_points"] == k for r in rs) for k in sorted({r["front"]["n_points"] for r in rs})},
            strategy_proven={k: sum(r[k]["status"] == "OPTIMAL" for r in rs) for k in ("A", "B", "B_minpeak", "C14")},
            strategy_stage1_proven={k: sum(r[k]["proven_stages"] >= 1 for r in rs) for k in ("A", "B", "B_minpeak", "C14")},
            c14_comparable=len(comp), c14_equal=sum(c["equal"] for c in comp),
            c14_front_better_where_direct_unproven=sum(c["front_better"] for c in checks if not c["comparable"]),
            conflict=sum(1 for r in rs if r.get("break_even_B", {}).get("kind") == "exact"),
            break_even_kinds={k: sum(r.get("break_even_B", {}).get("kind") == k for r in rs)
                              for k in ("exact", "upper_bound", "no_peak_reduction", "undetermined")},
            guard14_proven=sum(1 for r in rs if r["guard"].get("14", {}).get("proven")),
            guard14_choice={k: sum(1 for r in rs if r["guard"].get("14", {}).get("choice", "").startswith(k))
                            for k in ("front", "B", "C14", "EG", "PCG", "FCFS")},
            guard14_gap_pct_max=max(gaps) if gaps else None,
            fcfs_ok=sum(r["rules"]["fcfs_ok"] for r in rs), eg_ok=sum(r["rules"]["eg_ok"] for r in rs),
            solver_time_s=dict(median=statistics.median(t), max=max(t), sum=sum(t)),
            front_time_s=dict(median=statistics.median(ft), max=max(ft)),
            gate2_pass=(share >= GATE_SHARE) if not missing[s] else None)
    # M2: the largest size above 8x3 that passes, provided every smaller size passes too
    m2 = None
    for s in sizes:
        if summ[s]["gate2_pass"] is not True:          # failed OR incomplete: stop
            break
        if s != "8x3":
            m2 = s
    est = None
    if m2:
        per = summ[m2]["solver_time_s"]["sum"] / summ[m2]["instances"]
        est = dict(size=m2, instances=60, cpu_h=60 * per / 3600, wall_h_2_workers=60 * per / 3600 / 2,
                   basis="mean probe solver time per instance at that size (gamma 19/14, W 0.40/0.625)")
    result = dict(sizes=summ, gate_share=GATE_SHARE, m2=m2, m2_block_estimate=est,
                  note="Probe instances: gamma 19/14, W {0.40, 0.625}, CV {0, 0.35}, 2 seeds; descriptive only.")
    (out / "summary.json").write_text(json.dumps(result, indent=2, default=str))
    (out / "README.txt").write_text(__doc__)
    return result


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=ROOT / "results/scaling_probe")
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--sizes", default="8x3,12x4,16x5,20x6")
    ap.add_argument("--aggregate-only", action="store_true")
    a = ap.parse_args(argv)
    (a.out / "parts").mkdir(parents=True, exist_ok=True)
    sizes = a.sizes.split(",")
    mf = a.out / "manifest.json"
    man = _load_manifest(a.out)
    man.update(protocol=PROTOCOL, sizes=sizes,
               digest_by_size={s: probe_digest(*(int(x) for x in s.split("x"))) for s in sizes})
    mf.write_text(json.dumps(man, indent=2, sort_keys=True))
    if not a.aggregate_only:
        todo = []
        for s in a.sizes.split(","):
            n, m = (int(x) for x in s.split("x"))
            todo += [(n, m, t, a.out) for t in enumerate_tasks(probe_design(n, m))]
        with Pool(a.workers) as pool:
            for i, name in enumerate(pool.imap(run_one, todo), 1):
                print(f"[probe] {i}/{len(todo)} {name}", flush=True)
    res = aggregate(a.out, sizes)
    print(json.dumps(res, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
