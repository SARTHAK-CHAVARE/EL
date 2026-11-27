"""EL Tariff Opti command-line tool.

    python 07_src/app/cli.py solve --instance examples/benchmark.json [--rho 15 | --days 26 --pf 1] [--out out/]
    python 07_src/app/cli.py generate --size 8x3 --gamma 19/14 --w 0.55 --cv 0.35 --seed 0 --out my_shop.json

solve: one solve, then the recommended schedule at the chosen demand charge (default: the KERC-equivalent
INR 350/(days x PF) per kW per shift), the break-even, a comparison with simple rules, and PARTIAL monthly bills under
fixed and renegotiated contract demand. Writes schedule JSON files and PNG charts to --out.
"""
from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core import (analyse, bills, break_even_text, choose, comparison, front_table, kerc_rho_paise,  # noqa: E402
                      rho_paise_from_inr)
from app.io import instance_to_dict, load_instance, schedule_to_dict  # noqa: E402
from model import evaluate_schedule  # noqa: E402
from model.billing import BillingAssumptions, rho_equivalent_inr_per_kw  # noqa: E402


def _fmt_rows(rows):
    out = [f"{'approach':32s} {'energy':>9s} {'peak kW':>8s} {'demand':>9s} {'total':>10s} {'vs FCFS':>8s}  status"]
    for r in rows:
        if not r["feasible"]:
            out.append(f"{r['approach']:32s} {'-':>9s} {'-':>8s} {'-':>9s} {'-':>10s} {'-':>8s}  {r['note']}")
            continue
        sv = f"{r['saving_vs_fcfs_pct']:.1f}%" if "saving_vs_fcfs_pct" in r else "-"
        st = "proven optimal" if r["proven"] else r["note"]
        out.append(f"{r['approach']:32s} {r['energy_inr']:9.2f} {r['peak_kw']:8g} {r['demand_inr']:9.2f} "
                   f"{r['total_inr']:10.2f} {sv:>8s}  {st}")
    return "\n".join(out)


def cmd_solve(a) -> int:
    raw = json.loads(Path(a.instance).read_text(encoding="utf-8"))
    inst = load_instance(raw)
    start = raw.get("start_time")
    assumptions = BillingAssumptions(days_per_month=a.days, power_factor=Fraction(str(a.pf)))
    rho = rho_paise_from_inr(a.rho) if a.rho is not None else kerc_rho_paise(assumptions)
    print(f"Instance: {inst.name or a.instance}  ({len(inst.jobs)} jobs, {len(inst.machines)} machines, "
          f"{inst.T} slots of {inst.delta_t_min} min)")
    an = analyse(inst)
    print(f"Solved in {an.solve_time_s:.1f} s. Front: {len(an.front.points)} point(s), "
          f"{'complete (exact)' if an.front.complete else 'NOT complete (bounds shown)'}.")
    for n in an.notes:
        print("NOTE:", n)
    src = "given" if a.rho is not None else (f"KERC-equivalent 350/({a.days} x PF {a.pf}) = "
                                             f"{float(rho_equivalent_inr_per_kw(assumptions)):.2f}, rounded to paise")
    print(f"\nDemand charge rho = INR {rho / 100:.2f}/kW per shift ({src})")
    print(break_even_text(an))
    print("\nPareto front (energy cost vs peak):")
    for r in front_table(an):
        print(f"  peak {r['peak_kw']:g} kW  energy INR {r['energy_inr']:.2f}  makespan slot {r['makespan']}  "
              f"best for rho {r['best_for_rho_inr']}  {'proven' if r['proven'] else 'NOT proven'}")
    print("\nComparison at this demand charge (INR per shift):")
    print(_fmt_rows(comparison(an, rho)))
    rec = choose(an, rho)
    print(f"\nRecommended: {rec.choice}")
    print("\nPARTIAL monthly bill estimate vs the energy-only schedule "
          f"({a.days} shift-days, PF {a.pf}; demand charge INR 350/kVA, BD = max(MD, 0.90 CD)):")
    for name, cmp_ in bills(an, rec, assumptions).items():
        print(f"  CD {name:13s}: energy-only INR {float(cmp_.reference.total_inr):,.2f}  recommended INR "
              f"{float(cmp_.candidate.total_inr):,.2f}  saving INR {float(cmp_.saving_inr):,.2f}"
              + ("  (0.90 x CD floor binds)" if cmp_.candidate.floor_binding else ""))
    print("  " + cmp_.label)
    if a.out:
        out = Path(a.out)
        out.mkdir(parents=True, exist_ok=True)
        from app.plots import fig_cost_vs_rho, fig_front, fig_power, fig_schedule
        exports = {"recommended": (rec.schedule, rec.metrics), "energy_only": (an.b_schedule, an.b_metrics)}
        for name, (s, _) in exports.items():
            m = evaluate_schedule(inst, s, rho)
            (out / f"schedule_{name}.json").write_text(json.dumps(schedule_to_dict(inst, s, m, name, start, rho), indent=1))
        fig_schedule(inst, rec.schedule, "Recommended (peak-aware) schedule", start).savefig(out / "gantt_recommended.png", dpi=150)
        fig_schedule(inst, an.b_schedule, "Energy-only schedule", start, color="#eb6834").savefig(out / "gantt_energy_only.png", dpi=150)
        fig_power(inst, {"Recommended": rec.schedule, "Energy-only": an.b_schedule}, start).savefig(out / "power_profile.png", dpi=150)
        marks = {"break-even": float(an.break_even_b.rho_inr)} if an.break_even_b and an.break_even_b.rho_inr is not None else {}
        marks["chosen rho"] = rho / 100
        fig_cost_vs_rho(an.front.points, an.b_metrics.ec_int, an.b_metrics.peak_w,
                        max(30.0, rho / 100 * 1.5), marks).savefig(out / "cost_vs_rho.png", dpi=150)
        fig_front(an.front.points, rec.metrics.peak_w, (an.b_metrics.ec_int, an.b_metrics.peak_w)).savefig(out / "front.png", dpi=150)
        print(f"\nWrote schedules (JSON) and charts (PNG) to {out}")
    return 0


def cmd_generate(a) -> int:
    from app.core import generated_instance_dict
    dd = generated_instance_dict(a.size, a.gamma, a.w, a.cv, a.seed)
    Path(a.out).write_text(json.dumps(dd, indent=1))
    print(f"wrote {a.out}: {dd['name']}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("solve", help="solve an instance JSON")
    s.add_argument("--instance", required=True)
    s.add_argument("--rho", type=float, default=None, help="demand charge INR/kW per shift (default: KERC-equivalent)")
    s.add_argument("--days", type=int, default=26, help="shift-days per month (KERC-equivalent rho and bills)")
    s.add_argument("--pf", type=float, default=1.0, help="power factor (0-1]")
    s.add_argument("--out", default=None, help="directory for schedule JSON and PNG charts")
    g = sub.add_parser("generate", help="write a generated instance JSON (same generator as the study)")
    g.add_argument("--size", default="8x3")
    g.add_argument("--gamma", default="19/14")
    g.add_argument("--w", default="0.55")
    g.add_argument("--cv", default="0.35")
    g.add_argument("--seed", type=int, default=1)
    g.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    try:
        return cmd_solve(a) if a.cmd == "solve" else cmd_generate(a)
    except (ValueError, KeyError, FileNotFoundError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
