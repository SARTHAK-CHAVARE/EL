"""Budget diagnostic (NOT part of the pilot dataset): re-solve selected unproven pilot rows with larger limits.
Design factor levels are untouched; only solver limits differ. Output: diagnostics/budget_diagnostic.csv"""
import csv, dataclasses, sys, time
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp
from pathlib import Path
root = Path(__file__).resolve().parent
sys.path.insert(0, str(root.parents[1] / "07_src"))

# (instance_id, rho_paise, reason) taken from the pilot's unproven list
ROWS = [("g0w0c1s000", 5000, "stage1"), ("g1w0c1s000", 1400, "stage1"), ("g1w0c1s000", 5000, "stage1"),
        ("g1w1c1s000", 5000, "stage1"), ("g2w0c1s000", 5000, "stage1"), ("g2w1c1s000", 5000, "stage1"),
        ("g0w1c1s000", 1400, "tiebreak"), ("g1w0c0s000", 1400, "tiebreak"), ("g2w1c0s000", 5000, "tiebreak")]

def work(args):
    iid, rho, why = args
    from experiments.design import DESIGN_FULL, enumerate_tasks
    from experiments.generator import generate_instance
    from model import SolverConfig, solve_strategy_c
    design = dataclasses.replace(DESIGN_FULL, seeds_per_cell=1)
    task = [t for t in enumerate_tasks(design) if t.instance_id == iid][0]
    inst, _ = generate_instance(design, task)
    cfg = SolverConfig(time_limit_s=180, deterministic_time_limit=180, num_workers=1, random_seed=0,
                       tiebreak_time_limit_s=60, tiebreak_deterministic_time_limit=60)
    t0 = time.perf_counter(); r = solve_strategy_c(inst, rho, cfg)
    return dict(instance_id=iid, rho_paise=rho, pilot_reason=why, status=r.status.value,
                stage_statuses="|".join(r.stage_statuses), stage_values="|".join(map(str, r.stage_values)),
                stage_times_s="|".join(f"{x:.1f}" for x in r.stage_times_s), wall_s=round(time.perf_counter() - t0, 1))

if __name__ == "__main__":
    out = root / "diagnostics" / "budget_diagnostic.csv"
    with ProcessPoolExecutor(2, mp_context=mp.get_context("spawn")) as ex, open(out, "w", newline="") as fh:
        w = None
        for row in ex.map(work, ROWS):
            if w is None:
                w = csv.DictWriter(fh, fieldnames=list(row)); w.writeheader()
            w.writerow(row); fh.flush(); print(row, flush=True)
