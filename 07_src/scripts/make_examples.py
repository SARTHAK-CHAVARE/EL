"""Regenerate the demo instances in examples/ from the frozen P4 smoke designs (deterministic generator).

    python 07_src/scripts/make_examples.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.io import instance_to_dict  # noqa: E402
from experiments.design import DESIGN_MAIN_M3_SMOKE, DESIGN_MAIN_M4_SMOKE, enumerate_tasks  # noqa: E402
from experiments.generator import generate_instance  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
PICKS = [  # (file, design, instance id, description) - chosen from results/main_smoke as quick, illustrative cases
    ("shop_8x3_kerc.json", DESIGN_MAIN_M3_SMOKE, "g1w3c0s000",
     "8 jobs x 3 identical 15 kW machines, KERC Dec-Jun prices (7.60/6.60/5.60), workload 0.625"),
    ("shop_8x3_three_options.json", DESIGN_MAIN_M3_SMOKE, "g2w1c1s000",
     "8 jobs x 3 machines (8.6/15/21.4 kW), steep peak prices (gamma 7/4), workload 0.475: three trade-off options"),
    ("shop_8x3_no_reduction.json", DESIGN_MAIN_M3_SMOKE, None,
     "8 jobs x 3 machines where no peak reduction is possible (energy-only is already optimal)"),
    ("shop_12x4.json", DESIGN_MAIN_M4_SMOKE, "g0w0c0s000",
     "12 jobs x 4 identical 15 kW machines, KERC Dec-Jun prices, workload 0.40"),
]


def main() -> int:
    import pandas as pd
    out = ROOT / "examples"
    out.mkdir(exist_ok=True)
    for fname, design, iid, desc in PICKS:
        if iid is None:   # fastest smoke instance with a proven 'no peak reduction'
            df = pd.read_csv(ROOT / "results/main_smoke/m3/results.csv")
            be = df[(df.strategy == "BE_B") & (df.break_even_kind == "no_peak_reduction")]
            iid = be.sort_values("task_cpu_s").instance_id.iloc[0]
        task = next(t for t in enumerate_tasks(design) if t.instance_id == iid)
        inst, meta = generate_instance(design, task)
        d = instance_to_dict(inst, start_time="16:00")
        d["name"] = f"{desc} [{design.name} {iid}, realised W {meta.w_real:.3f}]"
        (out / fname).write_text(json.dumps(d, indent=1))
        print("wrote", fname, iid)
    return 0


if __name__ == "__main__":
    sys.exit(main())
