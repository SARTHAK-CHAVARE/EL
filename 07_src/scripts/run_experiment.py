"""Run or resume a factorial experiment (SPEC-002).

    python 07_src/scripts/run_experiment.py --design smoke --out results/smoke --workers 2
    python 07_src/scripts/run_experiment.py --design full  --out results/phase3_full --workers 4
    python 07_src/scripts/run_experiment.py --design cal2  --out results/cal2 --workers 2   (proposed calibration)

Re-running the same command resumes: finished instances are skipped.
"""
import argparse
import dataclasses
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from experiments.design import DESIGNS  # noqa: E402
from experiments.runner import RunnerError, aggregate, run_experiment  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--design", choices=sorted(DESIGNS), default="smoke")
    ap.add_argument("--out", required=True, type=Path, help="output directory (created if missing)")
    ap.add_argument("--workers", type=int, default=1, help="parallel processes (each solver uses 1 thread)")
    ap.add_argument("--seeds", type=int, default=None, help="override seeds per cell")
    ap.add_argument("--limit", type=int, default=None, help="only the first N tasks (for trials)")
    ap.add_argument("--force", action="store_true", help="overwrite manifest if the design changed")
    ap.add_argument("--aggregate-only", action="store_true", help="just rebuild results.csv from parts")
    a = ap.parse_args(argv)
    design = DESIGNS[a.design]
    if a.seeds is not None:
        design = dataclasses.replace(design, seeds_per_cell=a.seeds)
    try:
        if a.aggregate_only:
            print("wrote", aggregate(a.out))
            return 0
        counts = run_experiment(design, a.out, workers=a.workers, limit=a.limit, force=a.force)
    except RunnerError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"done: {counts}  ->  {a.out / 'results.csv'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
