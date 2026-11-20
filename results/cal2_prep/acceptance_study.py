"""Generator acceptance / selection-bias study (analysis of the generator only; no experiment is run).

Part 1  heuristic acceptance vs W (FCFS, SPT, either) from N raw draws per W level. Heuristics ignore tariff and
        power, so one (gamma, CV) setting is enough.
Part 2  at higher W: exact feasibility (does ANY schedule meet D = T?  strategy A, CP-SAT) versus the heuristic
        filter, and how the accepted instances differ from all feasible ones.
Usage: python results/cal2_prep/acceptance_study.py   -> acceptance_part1.csv, acceptance_part2.csv, acceptance_summary.txt
"""
import csv, dataclasses, multiprocessing as mp, statistics as st, sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
root = Path(__file__).resolve().parent
sys.path.insert(0, str(root.parents[1] / "07_src"))
from experiments.baselines import fcfs_schedule, spt_schedule
from experiments.design import DESIGN_FULL, enumerate_tasks
from experiments.generator import draw_instance, workload_w
from model import SolveStatus, SolverConfig, evaluate_schedule, solve_strategy_a

W_GRID_1 = ["0.30", "0.40", "0.50", "0.55", "0.60", "0.65", "0.70", "0.75", "0.80", "0.85", "0.90", "0.95"]
N1 = 2000                                   # raw draws per W for part 1
W_GRID_2 = ["0.70", "0.80", "0.85", "0.90", "0.95"]
N2 = 40                                     # exact-feasibility draws per W for part 2


def _design(w):
    return dataclasses.replace(DESIGN_FULL, name="acceptance-study", workloads=(w,), gammas=("19/14",), cvs=("0.35",),
                               seeds_per_cell=1)


def part1(w):
    d = _design(w); t = enumerate_tasks(d)[0]; rows = []
    for a in range(1, N1 + 1):
        inst = draw_instance(d, t, a)
        rows.append((fcfs_schedule(inst) is not None, spt_schedule(inst) is not None))
    n = len(rows)
    return dict(W=w, draws=n, fcfs=sum(r[0] for r in rows) / n, spt=sum(r[1] for r in rows) / n,
                either=sum(r[0] or r[1] for r in rows) / n, both=sum(r[0] and r[1] for r in rows) / n,
                only_fcfs=sum(r[0] and not r[1] for r in rows) / n, only_spt=sum(r[1] and not r[0] for r in rows) / n)


def part2_one(args):
    w, a = args
    d = _design(w); t = enumerate_tasks(d)[0]; inst = draw_instance(d, t, a)
    f, s = fcfs_schedule(inst), spt_schedule(inst)
    res = solve_strategy_a(inst, SolverConfig(time_limit_s=30, deterministic_time_limit=10, num_workers=1))
    longest = max(min(j.proc.values()) for j in inst.jobs)
    out = dict(W=w, attempt=a, w_real=round(float(workload_w(inst)), 4), longest_min_p=longest,
               fcfs_ok=int(f is not None), spt_ok=int(s is not None), heur_ok=int(f is not None or s is not None),
               exact_status=res.status.value, exact_feasible=int(res.status in (SolveStatus.OPTIMAL, SolveStatus.FEASIBLE)),
               exact_proven=int(res.status in (SolveStatus.OPTIMAL, SolveStatus.INFEASIBLE)),
               A_makespan=res.metrics.makespan if res.metrics else "",
               fcfs_makespan=evaluate_schedule(inst, f, 0).makespan if f else "",
               spt_makespan=evaluate_schedule(inst, s, 0).makespan if s else "")
    return out


if __name__ == "__main__":
    ctx = mp.get_context("spawn")
    with ProcessPoolExecutor(2, mp_context=ctx) as ex:
        p1 = list(ex.map(part1, W_GRID_1))
        p2 = list(ex.map(part2_one, [(w, a) for w in W_GRID_2 for a in range(1, N2 + 1)], chunksize=4))
    for name, rows in (("acceptance_part1.csv", p1), ("acceptance_part2.csv", p2)):
        with open(root / name, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    L = ["## Part 1: heuristic acceptance by W (%d raw draws per W; fractions)" % N1,
         "W      FCFS   SPT    either both   only_FCFS only_SPT"]
    for r in p1:
        L.append(f"{r['W']:>5} {r['fcfs']:6.3f} {r['spt']:6.3f} {r['either']:6.3f} {r['both']:6.3f} {r['only_fcfs']:9.3f} {r['only_spt']:8.3f}")
    L += ["", "## Part 2: exact feasibility (A, CP-SAT) vs heuristic filter (%d draws per W)" % N2,
          "W     exact_feasible heuristic_accept  feasible_but_rejected  unproven  mean_A_makespan(feas)  mean_FCFS/A  mean_SPT/A"]
    for w in W_GRID_2:
        g = [r for r in p2 if r["W"] == w]; fe = [r for r in g if r["exact_feasible"]]
        rej = [r for r in fe if not r["heur_ok"]]
        fa = [r["fcfs_makespan"] / r["A_makespan"] for r in fe if r["fcfs_makespan"] != ""]
        sa = [r["spt_makespan"] / r["A_makespan"] for r in fe if r["spt_makespan"] != ""]
        L.append(f"{w:>5} {len(fe)/len(g):14.3f} {sum(r['heur_ok'] for r in g)/len(g):16.3f} {len(rej):20d} "
                 f"{sum(1-r['exact_proven'] for r in g):9d} {st.mean(r['A_makespan'] for r in fe) if fe else float('nan'):20.2f} "
                 f"{st.mean(fa) if fa else float('nan'):12.3f} {st.mean(sa) if sa else float('nan'):11.3f}")
    L += ["", "## Part 2b: accepted vs feasible-but-rejected (pooled over W>=0.80): longest job (slots) and A makespan"]
    pool = [r for r in p2 if r["exact_feasible"] and float(r["W"]) >= 0.8]
    for lab, sel in (("heuristic-accepted", [r for r in pool if r["heur_ok"]]), ("feasible-but-rejected", [r for r in pool if not r["heur_ok"]])):
        if sel:
            L.append(f"{lab:22s} n={len(sel):3d} longest_min_p mean={st.mean(r['longest_min_p'] for r in sel):5.2f} "
                     f"A_makespan mean={st.mean(r['A_makespan'] for r in sel):5.2f} (T=32)")
    (root / "acceptance_summary.txt").write_text("\n".join(L) + "\n"); print("\n".join(L))
