"""Runtime estimate for DESIGN_CAL2 from the measured pilot27 solve times (nothing is executed).
Unknowns the pilot cannot supply are handled as explicit scenarios:
  * interior W levels (0.475, 0.55, 0.625): pilot has only W=0.40 and W=0.70 -> linear interpolation (central) or
    1.5x the larger anchor (hard-interior scenario; pilot showed difficulty is NOT monotone in W)
  * rho = 1, 2: not measured -> cost of the measured rho = 5 rows (central), 0.5x that (easy), rho = 14 cost (hard)
Output: results/cal2_prep/runtime_estimate.txt
"""
import random, sys
from pathlib import Path
import pandas as pd
root = Path(__file__).resolve().parent
sys.path.insert(0, str(root.parents[1] / "07_src"))
from experiments.design import DESIGN_CAL2, DESIGN_FULL, enumerate_tasks
df = pd.read_csv(root.parent / "pilot27" / "results.csv", dtype={"w_target": str, "cv": str, "gamma": str})
nonC = df[~df.strategy.isin(["C"])].groupby("instance_id").wall_time_s.sum()
C = df[df.strategy == "C"].pivot_table(index="instance_id", columns="rho_paise", values="wall_time_s", aggfunc="sum")
w = df.drop_duplicates("instance_id").set_index("instance_id").w_target
anch = {a: [i for i in w.index if w[i] == a] for a in ("0.40", "0.70")}
def inst_cost(i, rho1, rho2, mode):
    c5, c14, c50 = C.loc[i, 500], C.loc[i, 1400], C.loc[i, 5000]
    r12 = {"central": 2 * c5, "easy": 2 * 0.5 * c5, "hard": 2 * c14}[mode]
    return nonC[i] + c5 + c14 + c50 + r12
n_per_w = 3 * 3 * DESIGN_CAL2.seeds_per_cell          # gamma x CV x seeds = 18 instances per W level
Wlev = {w_: float(__import__("fractions").Fraction(w_)) for w_ in DESIGN_CAL2.workloads}
def total(m40, m70, interior_mode):
    t = 0.0
    for w_, x in Wlev.items():
        if w_ == "0.40": t += n_per_w * m40
        elif w_ == "0.70": t += n_per_w * m70
        else:
            lin = m40 + (m70 - m40) * (x - 0.40) / 0.30
            t += n_per_w * (lin if interior_mode == "interp" else 1.5 * max(m40, m70))
    return t
L = [f"DESIGN_CAL2: {len(enumerate_tasks(DESIGN_CAL2))} instances, rho levels {DESIGN_CAL2.rho_inr}, "
     f"12 result rows per instance (5 rho-independent solves + 5 C solves + FCFS + SPT) = {12*len(enumerate_tasks(DESIGN_CAL2))} rows, "
     f"{10*len(enumerate_tasks(DESIGN_CAL2))} CP-SAT runs",
     "pilot anchors (mean CPU s per instance incl. rho=5/14/50 only): " + ", ".join(
         f"W={a}: {sum(nonC[i]+C.loc[i,500]+C.loc[i,1400]+C.loc[i,5000] for i in ids)/len(ids):.1f}" for a, ids in anch.items()), ""]
rows = []
rng = random.Random(7)
for rho_mode in ("easy", "central", "hard"):
    for interior in ("interp", "hard-interior"):
        m = {a: sum(inst_cost(i, 0, 0, rho_mode) for i in ids) / len(ids) for a, ids in anch.items()}
        pt = total(m["0.40"], m["0.70"], "interp" if interior == "interp" else "hard")
        bs = []
        for _ in range(3000):
            mm = {a: sum(inst_cost(rng.choice(ids), 0, 0, rho_mode) for _ in ids) / len(ids) for a, ids in anch.items()}
            bs.append(total(mm["0.40"], mm["0.70"], "interp" if interior == "interp" else "hard"))
        bs.sort()
        rows.append((rho_mode, interior, pt, bs[75], bs[2925]))
L.append("scenario (rho=1,2 cost | interior W)   CPU-h (point; 95% bootstrap over pilot instances)   wall-h @2 workers   wall-h @1 worker")
for r in rows:
    L.append(f"{r[0]:>7s} | {r[1]:<13s}  {r[2]/3600:5.2f}  ({r[3]/3600:4.2f} - {r[4]/3600:4.2f})   {r[2]/7200:5.2f}   {r[2]/3600:5.2f}")
# hard upper bound from the solver limits actually applied (deterministic 60 s stage 1, 15 s tie-break; ~10% wall overhead)
d = DESIGN_CAL2
stage1, tb = 1.15 * d.solver_det_time_limit, 1.15 * d.tiebreak_det_time_limit
solves = {"A": (1, 1), "B": (1, 1), "B_minpeak": (1, 2), "B_maxpeak": (1, 2), "P": (1, 2)}
cap = sum(s1 * stage1 + n_tb * tb for s1, n_tb in solves.values()) + 5 * (stage1 + tb)
L += ["", f"hard cap from applied deterministic limits: <= {cap:.0f} s per instance -> {cap*90/3600:.1f} CPU-h = {cap*90/7200:.1f} h wall @2 workers (never approached in the pilot: max instance 170 s)"]
L += ["", "for comparison (same method, v1 full design with measured pilot cost 50.8 s/instance): 405 instances = "
      f"{405*50.8/3600:.1f} CPU-h = {405*50.8/7200:.1f} h wall @2 workers"]
(root / "runtime_estimate.txt").write_text("\n".join(L) + "\n"); print("\n".join(L))
