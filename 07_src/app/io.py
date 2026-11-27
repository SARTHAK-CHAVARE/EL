"""Instance and schedule files for the prototype (human-editable JSON, engineering units).

Instance JSON:
{
  "name": "my shop",
  "slot_minutes": 15, "horizon_slots": 32, "deadline_slot": 32,       # deadline optional (default = horizon)
  "start_time": "16:00",                                              # optional, only for labels
  "base_load_kw": 2,
  "tariff_inr_per_kwh": [6.6, 6.6, ...],                              # one value per slot
  "machines": [1, 2, 3],
  "jobs": [{"id": "J1", "proc_slots": {"1": 4, "2": 5}, "power_kw": {"1": 15, "2": 9}, "release": 1, "due": null}]
}
Numbers are converted exactly (via their decimal text), so 7.60 means exactly INR 7.60.
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Union

from model import Instance, Metrics, Operation, make_instance

PathOrDict = Union[str, Path, dict]


def _num(x) -> str:
    """Exact decimal text for make_instance (avoids binary float artefacts)."""
    if isinstance(x, bool):
        raise ValueError("boolean is not a number")
    return str(x)


def instance_from_dict(d: dict) -> Instance:
    req = ("slot_minutes", "horizon_slots", "base_load_kw", "tariff_inr_per_kwh", "machines", "jobs")
    miss = [k for k in req if k not in d]
    if miss:
        raise ValueError(f"instance file is missing: {', '.join(miss)}")
    T = int(d["horizon_slots"])
    if len(d["tariff_inr_per_kwh"]) != T:
        raise ValueError(f"tariff has {len(d['tariff_inr_per_kwh'])} values, horizon_slots is {T}")
    jobs, rel, due = [], {}, {}
    for j in d["jobs"]:
        jid = str(j["id"])
        proc = {int(m): int(p) for m, p in j["proc_slots"].items()}
        power = {int(m): _num(p) for m, p in j["power_kw"].items()}
        if set(proc) != set(power):
            raise ValueError(f"job {jid}: proc_slots and power_kw must list the same machines")
        jobs.append((jid, proc, power))
        if j.get("release") not in (None, 1):
            rel[jid] = int(j["release"])
        if j.get("due") is not None:
            due[jid] = int(j["due"])
    return make_instance(machines=[int(m) for m in d["machines"]], jobs=jobs, T=T,
                         D=int(d.get("deadline_slot") or T), delta_t_min=int(d["slot_minutes"]),
                         base_kw=_num(d["base_load_kw"]), tariff_inr_per_kwh=[_num(c) for c in d["tariff_inr_per_kwh"]],
                         releases=rel, dues=due, name=str(d.get("name", "")))


def load_instance(src: PathOrDict) -> Instance:
    d = src if isinstance(src, dict) else json.loads(Path(src).read_text(encoding="utf-8"))
    return instance_from_dict(d)


def _dec(frac: Fraction) -> Union[int, float, str]:
    """Exact JSON number when the value is a finite decimal with <= 6 places, else a fraction string."""
    if frac.denominator == 1:
        return int(frac)
    for places in range(1, 7):
        v = frac * 10 ** places
        if v.denominator == 1:
            return float(f"{int(v) / 10 ** places:.{places}f}")
    return str(frac)


def instance_to_dict(inst: Instance, start_time: Optional[str] = None) -> dict:
    d = dict(name=inst.name, slot_minutes=inst.delta_t_min, horizon_slots=inst.T, deadline_slot=inst.D,
             base_load_kw=_dec(Fraction(inst.base_w, 1000)),
             tariff_inr_per_kwh=[_dec(Fraction(c, 100)) for c in inst.tariff_paise],
             machines=list(inst.machines),
             jobs=[dict(id=j.job_id, proc_slots={str(m): p for m, p in j.proc.items()},
                        power_kw={str(m): _dec(Fraction(w, 1000)) for m, w in j.power_w.items()},
                        release=j.release, due=j.due) for j in inst.jobs])
    if start_time:
        d["start_time"] = start_time
    return d


def slot_label(slot: int, delta_t_min: int, start_time: Optional[str]) -> str:
    """Clock time at the START of a 1-based slot, or 'slot n' without a start time."""
    if not start_time:
        return f"slot {slot}"
    h, m = (int(x) for x in start_time.split(":"))
    total = h * 60 + m + (slot - 1) * delta_t_min
    return f"{(total // 60) % 24:02d}:{total % 60:02d}"


def power_profile_w(inst: Instance, ops: Sequence[Operation]) -> List[int]:
    """Total facility power per slot (W), base load included."""
    jobs = {j.job_id: j for j in inst.jobs}
    p = [inst.base_w] * inst.T
    for o in ops:
        for t in range(o.start, o.end + 1):
            p[t - 1] += jobs[o.job_id].power_w[o.machine_id]
    return p


def schedule_to_dict(inst: Instance, ops: Sequence[Operation], metrics: Metrics, label: str,
                     start_time: Optional[str] = None, rho_paise: int = 0) -> dict:
    """Schedule export (also the format a controller such as the ESP32 would consume: one switch window per job)."""
    end_label = lambda s: slot_label(s + 1, inst.delta_t_min, start_time)          # noqa: E731
    return dict(
        label=label, instance=inst.name, slot_minutes=inst.delta_t_min, start_time=start_time,
        operations=[dict(job=o.job_id, machine=o.machine_id, start_slot=o.start, end_slot=o.end,
                         start=slot_label(o.start, inst.delta_t_min, start_time), end=end_label(o.end))
                    for o in sorted(ops, key=lambda o: (o.start, o.machine_id, o.job_id))],
        power_profile_kw=[_dec(Fraction(w, 1000)) for w in power_profile_w(inst, ops)],
        metrics=dict(energy_cost_inr=_dec(Fraction(metrics.ec_int, 6_000_000)), peak_kw=_dec(Fraction(metrics.peak_w, 1000)),
                     makespan_slot=metrics.makespan, rho_inr_per_kw=_dec(Fraction(rho_paise, 100)),
                     tec_inr=_dec(Fraction(metrics.ec_int + 60 * rho_paise * metrics.peak_w, 6_000_000))))
