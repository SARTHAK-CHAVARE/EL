"""Scaling-probe bookkeeping (scripts/scaling_probe.py): stale-result protection and complete accounting.

No solving: synthetic part files exercise the digest checks and the aggregation of incomplete sizes.
"""
import json

import pytest

from experiments.design import enumerate_tasks
from scripts import scaling_probe as sp


def _rec(size, iid, digest=True, proven=True):
    n, m = (int(x) for x in size.split("x"))
    r = dict(size=size, instance_id=iid,
             front=dict(complete=proven, termination="structural_bound", n_points=2, time_s=1.0,
                        solves=[dict(label="top", required_proven=True), dict(label="cap", required_proven=proven)]),
             A=dict(status="OPTIMAL", proven_stages=2, time_s=1.0), B=dict(status="OPTIMAL", proven_stages=2, time_s=1.0),
             B_minpeak=dict(status="OPTIMAL", proven_stages=3, time_s=1.0),
             C14=dict(status="OPTIMAL", proven_stages=2, time_s=1.0),
             c14_check=dict(comparable=True, equal=True, front_better=False),
             break_even_B=dict(kind="exact"), guard={"14": dict(choice="front[peak=1W]", gap_pct=0.0, proven=True)},
             rules=dict(fcfs_ok=True, eg_ok=True), total_solver_time_s=5.0)
    if digest:
        r["digest"] = sp.probe_digest(n, m)
    return r


def _write_all(out, size="8x3", skip=(), **kw):
    n, m = (int(x) for x in size.split("x"))
    (out / "parts").mkdir(parents=True, exist_ok=True)
    ids = [t.instance_id for t in enumerate_tasks(sp.probe_design(n, m))]
    for iid in ids:
        if iid not in skip:
            (out / "parts" / f"{size}_{iid}.json").write_text(json.dumps(_rec(size, iid, **kw)))
    return ids


def test_complete_size_passes_and_selects_nothing_for_8x3_only(tmp_path):
    _write_all(tmp_path)
    res = sp.aggregate(tmp_path, ["8x3"])
    s = res["sizes"]["8x3"]
    assert s["instances"] == s["expected"] == 8 and s["missing"] == [] and s["gate2_pass"] is True
    assert res["m2"] is None                       # 8x3 is the baseline size, never M2


def test_missing_part_is_listed_and_blocks_the_gate(tmp_path):
    ids = _write_all(tmp_path, "8x3")
    _write_all(tmp_path, "12x4", skip={"g0w1c1s001"})
    (tmp_path / "parts" / f"8x3_{ids[0]}.json").write_text("{ truncated")      # unreadable counts as missing
    res = sp.aggregate(tmp_path, ["8x3", "12x4"])
    assert res["sizes"]["8x3"]["missing"] == [ids[0]] and res["sizes"]["8x3"]["gate2_pass"] is None
    assert res["sizes"]["12x4"]["missing"] == ["g0w1c1s001"] and res["sizes"]["12x4"]["gate2_pass"] is None
    assert res["m2"] is None                       # an incomplete size can never be selected


def test_stale_digest_is_refused_in_aggregation_and_resume(tmp_path):
    ids = _write_all(tmp_path)
    p = tmp_path / "parts" / f"8x3_{ids[0]}.json"
    rec = json.loads(p.read_text())
    rec["digest"] = "0" * 16
    p.write_text(json.dumps(rec))
    with pytest.raises(sp.StaleProbeResult):
        sp.aggregate(tmp_path, ["8x3"])
    with pytest.raises(sp.StaleProbeResult):
        sp._check_existing(p, 8, 3, tmp_path)
    assert sp._check_existing(tmp_path / "parts" / f"8x3_{ids[1]}.json", 8, 3, tmp_path) is True
    assert sp._check_existing(tmp_path / "parts" / "8x3_nope.json", 8, 3, tmp_path) is False


def test_legacy_parts_need_a_matching_manifest_entry(tmp_path):
    _write_all(tmp_path, digest=False)
    with pytest.raises(sp.StaleProbeResult):                     # no manifest: digest unknown
        sp.aggregate(tmp_path, ["8x3"])
    (tmp_path / "manifest.json").write_text(json.dumps({"legacy": {"digest_by_size": {"8x3": "f" * 16}}}))
    with pytest.raises(sp.StaleProbeResult):                     # manifest from other code
        sp.aggregate(tmp_path, ["8x3"])
    (tmp_path / "manifest.json").write_text(json.dumps({"legacy": {"digest_by_size": {"8x3": sp.probe_digest(8, 3)}}}))
    assert sp.aggregate(tmp_path, ["8x3"])["sizes"]["8x3"]["gate2_pass"] is True


def test_gate_uses_required_solves_and_stops_at_first_failing_size(tmp_path):
    _write_all(tmp_path, "8x3")
    _write_all(tmp_path, "12x4", proven=False)                   # 50 % of required solves proven
    _write_all(tmp_path, "16x5")
    res = sp.aggregate(tmp_path, ["8x3", "12x4", "16x5"])
    assert res["sizes"]["12x4"]["required_proven_share"] == 0.5 and res["sizes"]["12x4"]["gate2_pass"] is False
    assert res["sizes"]["16x5"]["gate2_pass"] is True and res["m2"] is None     # no skipping over a failed size


def test_real_probe_results_are_consistent():
    from pathlib import Path
    out = Path(__file__).resolve().parents[1] / "results" / "scaling_probe"
    res = sp.aggregate(out, ["8x3", "12x4", "16x5", "20x6"])
    assert all(v["missing"] == [] for v in res["sizes"].values()) and res["m2"] == "12x4"
