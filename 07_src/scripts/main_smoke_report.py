"""P4 smoke report (SPEC-003 section 13): completeness, proofs, gaps, rules, runtime and the full-study projection.

    python 07_src/scripts/main_smoke_report.py [--smoke results/main_smoke]

Reads results/main_smoke/{m3,m4}/results.csv and smoke.log (block start/end times). Writes summary.json and CSVs to
results/main_smoke/report/. Smoke numbers are for planning only; they are not study results.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import statistics
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd  # noqa: E402

from experiments.design import DESIGN_MAIN_M3, DESIGN_MAIN_M3_SMOKE, DESIGN_MAIN_M4, DESIGN_MAIN_M4_SMOKE, enumerate_tasks  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
BLOCKS = {"m3": (DESIGN_MAIN_M3_SMOKE, DESIGN_MAIN_M3), "m4": (DESIGN_MAIN_M4_SMOKE, DESIGN_MAIN_M4)}
EXPECTED_ALWAYS = ("A", "B", "B_minpeak", "FRONT_top", "FRONT_PT", "C", "FCFS", "SPT", "EG", "BE_B", "BE_B_minpeak")
PER_RHO = ("C_front", "PCG", "GUARD")
WORKERS = 2


def block_times(log: Path) -> dict:
    t = {}
    for line in log.read_text().splitlines():
        m = re.match(r"\[smoke\] block (m\d) (start|end) (\S+)", line)
        if m:
            t.setdefault(m.group(1), {})[m.group(2)] = datetime.fromisoformat(m.group(3).replace("Z", "+00:00"))
    return {b: (v["end"] - v["start"]).total_seconds() for b, v in t.items() if "end" in v}


def boot_mean_ci(x, n_boot=4000, seed=7):
    rng = random.Random(seed)
    means = sorted(statistics.fmean(rng.choices(x, k=len(x))) for _ in range(n_boot))
    return means[int(0.05 * n_boot)], means[int(0.95 * n_boot) - 1]


def analyse_block(name: str, df: pd.DataFrame, smoke, main, wall_block: float) -> dict:
    exp_ids = {t.instance_id for t in enumerate_tasks(smoke)}
    got_ids = set(df.instance_id)
    rho_grid = sorted({int(r) for r in df[df.strategy == "C_front"].rho_paise})
    missing_rows = []
    for iid in sorted(got_ids):
        s = df[df.instance_id == iid]
        names = set(s.strategy)
        missing_rows += [f"{iid}:{x}" for x in EXPECTED_ALWAYS if x not in names]
        for x in PER_RHO:
            have = set(s[s.strategy == x].rho_paise.astype(int))
            missing_rows += [f"{iid}:{x}@{r}" for r in rho_grid if r not in have]
    inst = df.drop_duplicates("instance_id").set_index("instance_id")
    req = df[df.strategy.isin(["FRONT_top", "FRONT_cap", "P"])]
    top = df[df.strategy == "FRONT_top"].set_index("instance_id")
    cf = df[df.strategy == "C_front"]
    g = df[df.strategy == "GUARD"]
    c14 = df[df.strategy == "C"].set_index("instance_id")
    cf14 = cf[cf.rho_paise == int(round(float(main.cross_check_rho_inr) * 100))].set_index("instance_id")
    comparable = [i for i in got_ids if top.loc[i, "front_complete"] == 1 and c14.loc[i, "proven_stages"] >= 1]
    b = df[df.strategy == "B"].set_index("instance_id")
    guard_le_b = all(int(r.tec_int) <= int(b.loc[r.instance_id, "ec_int"]) + 60 * int(r.rho_paise) * int(b.loc[r.instance_id, "peak_w"])
                     for r in g.itertuples())
    cpu = inst.task_cpu_s.astype(float)
    wall_i = inst.task_wall_s.astype(float)

    def by(col):
        return {str(k): dict(n=int(len(v)), mean=round(float(v.mean()), 1), median=round(float(v.median()), 1),
                             max=round(float(v.max()), 1)) for k, v in cpu.groupby(inst[col])}
    scale = main.seeds_per_cell / smoke.seeds_per_cell               # every cell present in the smoke run
    n_main = len(enumerate_tasks(main))
    eff = (cpu.sum() / WORKERS) / wall_block if wall_block else None   # parallel efficiency observed
    lo, hi = boot_mean_ci(list(cpu))
    proj_cpu = cpu.sum() * scale
    proj = dict(main_instances=n_main, scale_factor=scale, cpu_h=proj_cpu / 3600,
                cpu_h_90ci=(lo * n_main / 3600, hi * n_main / 3600),
                wall_h=(proj_cpu / WORKERS) / (eff or 1) / 3600,
                wall_h_90ci=(lo * n_main / WORKERS / (eff or 1) / 3600, hi * n_main / WORKERS / (eff or 1) / 3600),
                worst_case_wall_h=(cpu.max() * n_main / WORKERS) / 3600,
                basis=f"smoke CPU per instance x {scale:g} (each cell present); wall = CPU / {WORKERS} workers / observed "
                      f"parallel efficiency; 90% interval = bootstrap of the mean over smoke instances")
    out = dict(
        block=name, design=smoke.name, digest=smoke.digest(), digests_in_results=sorted(df.design_digest.unique()),
        instances_expected=len(exp_ids), instances_present=len(got_ids), instances_missing=sorted(exp_ids - got_ids),
        rows=len(df), missing_rows=missing_rows, gen_attempts=inst.gen_attempts.astype(int).value_counts().to_dict(),
        w_real_by_w={k: (round(float(v.min()), 4), round(float(v.max()), 4)) for k, v in inst.w_real.astype(float).groupby(inst.w_target)},
        front_complete=int((top.front_complete == 1).sum()), front_terminations=top.front_termination.value_counts().to_dict(),
        front_points=top.front_n_points.astype(int).value_counts().sort_index().to_dict(),
        required_solves=int(len(req)), required_proven=int(req.required_proven.astype(int).sum()),
        incomplete_fronts=sorted(top[top.front_complete != 1].index),
        strategies_optimal={s: f"{int((df[df.strategy == s].status == 'OPTIMAL').sum())}/{int((df.strategy == s).sum())}"
                            for s in ("A", "B", "B_minpeak", "P", "C")},
        c14_stage1_proven=int((c14.proven_stages >= 1).sum()),
        c_front_optimal=f"{int((cf.status == 'OPTIMAL').sum())}/{len(cf)}",
        c_front_tec_exact=f"{int((cf.front_complete == 1).sum())}/{len(cf)}",
        cross_check_comparable=len(comparable),
        cross_check_equal=sum(int(cf14.loc[i, "tec_int"]) == int(c14.loc[i, "tec_int"]) for i in comparable),
        guard_le_B_all=guard_le_b, guard_optimal=f"{int((g.status == 'OPTIMAL').sum())}/{len(g)}",
        guard_gap_pct=dict(max=round(float(pd.to_numeric(g.gap, errors="coerce").max() * 100), 3),
                           n_positive=int((pd.to_numeric(g.gap, errors="coerce") > 0).sum())),
        guard_choice=g.choice.str.replace(r"\[.*", "", regex=True).value_counts().to_dict(),
        rules_ok={s: f"{int((df[df.strategy == s].status == 'HEURISTIC').sum())}/{int((df.strategy == s).sum())}"
                  for s in ("FCFS", "SPT", "EG", "PCG")},
        break_even_B=df[df.strategy == "BE_B"].break_even_kind.value_counts().to_dict(),
        cpu_s=dict(total=round(float(cpu.sum()), 1), mean=round(float(cpu.mean()), 1), median=round(float(cpu.median()), 1),
                   max=round(float(cpu.max()), 1)),
        task_wall_s_total=round(float(wall_i.sum()), 1), block_wall_s=wall_block,
        parallel_efficiency=None if eff is None else round(eff, 3),
        cpu_by_w=by("w_target"), cpu_by_cv=by("cv"), cpu_by_gamma=by("gamma"),
        projection=proj)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--smoke", type=Path, default=ROOT / "results/main_smoke")
    a = ap.parse_args(argv)
    times = block_times(a.smoke / "smoke.log")
    rep = {}
    for name, (smoke, main) in BLOCKS.items():
        df = pd.read_csv(a.smoke / name / "results.csv", dtype={"w_target": str, "cv": str, "gamma": str})
        rep[name] = analyse_block(name, df, smoke, main, times.get(name))
    tot = dict(cpu_h=sum(r["projection"]["cpu_h"] for r in rep.values()),
               wall_h=sum(r["projection"]["wall_h"] for r in rep.values()),
               wall_h_90ci=tuple(sum(r["projection"]["wall_h_90ci"][i] for r in rep.values()) for i in (0, 1)),
               worst_case_wall_h=sum(r["projection"]["worst_case_wall_h"] for r in rep.values()))
    rep["total_projection"] = tot
    out = a.smoke / "report"
    out.mkdir(exist_ok=True)
    (out / "summary.json").write_text(json.dumps(rep, indent=2, default=str))
    print(json.dumps(rep, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
