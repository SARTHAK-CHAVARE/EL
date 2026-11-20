"""SPEC-003 designs and runner protocol (experiments/design.py MainDesign, runner.run_task_main)."""
import csv
import itertools
from dataclasses import replace
from fractions import Fraction

import pytest

from experiments.design import (DESIGN_CAL2, DESIGN_FULL, DESIGN_MAIN_M3, DESIGN_MAIN_M3_SMOKE, DESIGN_MAIN_M4,
                                DESIGN_MAIN_M4_SMOKE, DESIGNS, MAIN_VERSION, MainDesign, enumerate_tasks)
from experiments.runner import (COLUMNS, COLUMNS_MAIN, RunnerError, aggregate, derived_c_status, run_experiment)

PINNED = {"main-m3-v1": "56e0f2f2f3455ffd", "main-m4-v1": "e5bfe31d5230171c",
          "main-m3-smoke": "8788174bf9477c21", "main-m4-smoke": "c4002ac66cfdb832"}


def test_digests_pinned_and_old_designs_unchanged():
    for d in (DESIGN_MAIN_M3, DESIGN_MAIN_M4, DESIGN_MAIN_M3_SMOKE, DESIGN_MAIN_M4_SMOKE):
        assert d.version == MAIN_VERSION and d.digest() == PINNED[d.name]
    assert DESIGN_FULL.digest() == "c9af6944fe5da183" and DESIGN_CAL2.digest() == "99596784481ea861"
    assert replace(DESIGN_FULL, seeds_per_cell=1).digest() == "37af47cf7472c2c4"            # pilot27
    assert {k: DESIGNS[k].name for k in ("main-m3", "main-m4", "main-m3-smoke", "main-m4-smoke")} == \
        {"main-m3": "main-m3-v1", "main-m4": "main-m4-v1", "main-m3-smoke": "main-m3-smoke", "main-m4-smoke": "main-m4-smoke"}


def test_factor_levels_and_sizes_match_the_approved_spec():
    m3, m4 = DESIGN_MAIN_M3, DESIGN_MAIN_M4
    assert (m3.gammas, m3.workloads, m3.cvs, m3.seeds_per_cell, m3.n_jobs, m3.n_machines) == \
        (("1", "19/14", "7/4"), ("0.40", "0.475", "0.55", "0.625"), ("0", "0.35", "0.75"), 15, 8, 3)
    assert (m4.gammas, m4.workloads, m4.cvs, m4.seeds_per_cell, m4.n_jobs, m4.n_machines) == \
        (("19/14",), ("0.40", "0.55", "0.70"), ("0", "0.35"), 10, 12, 4)
    assert len(enumerate_tasks(m3)) == 540 and len(enumerate_tasks(m4)) == 60
    assert m3.rho_inr == m4.rho_inr == ("1", "2", "5", "14", "50") and m3.cross_check_rho_inr == "14"
    # every W level lies strictly below the structural threshold (M-1)/M of its block
    for d in (m3, m4):
        assert all(Fraction(w) < Fraction(d.n_machines - 1, d.n_machines) for w in d.workloads)


def test_smoke_covers_every_cell_and_never_shares_seeds_with_the_main_run():
    for smoke, main in ((DESIGN_MAIN_M3_SMOKE, DESIGN_MAIN_M3), (DESIGN_MAIN_M4_SMOKE, DESIGN_MAIN_M4)):
        cells = {(t.gamma_idx, t.w_idx, t.cv_idx) for t in enumerate_tasks(smoke)}
        assert cells == set(itertools.product(range(len(main.gammas)), range(len(main.workloads)), range(len(main.cvs))))
        assert smoke.name != main.name and smoke.base_seed != main.base_seed
        assert (smoke.solver_det_time_limit, smoke.tiebreak_det_time_limit) == (main.solver_det_time_limit,
                                                                                 main.tiebreak_det_time_limit)
    seeds = {DESIGN_FULL.base_seed, DESIGN_CAL2.base_seed, 20261121, DESIGN_MAIN_M3.base_seed, DESIGN_MAIN_M3_SMOKE.base_seed}
    assert len(seeds) == 5                                    # pilot, cal2, probe, main, smoke: all distinct


def test_derived_c_status_never_claims_unproven_optimality():
    assert derived_c_status(True, True) == ("OPTIMAL", 2)
    assert derived_c_status(True, False) == ("FEASIBLE", 1)
    assert derived_c_status(False, True) == ("FEASIBLE", 0)
    assert derived_c_status(False, False) == ("FEASIBLE", 0)


MICRO = MainDesign(name="main-micro", gammas=("19/14",), workloads=("0.40",), cvs=("0", "0.35"),
                   rho_inr=("1", "14"), seeds_per_cell=1, n_jobs=4, n_machines=2, T=16,
                   solver_time_limit_s=20.0, solver_det_time_limit=8.0, tiebreak_time_limit_s=10.0,
                   tiebreak_det_time_limit=4.0)


@pytest.fixture(scope="module")
def micro_run(tmp_path_factory):
    out = tmp_path_factory.mktemp("main_micro")
    counts = run_experiment(MICRO, out, workers=1, progress=lambda *_: None)
    with open(out / "results.csv", newline="") as fh:
        rows = list(csv.DictReader(fh))
    return out, counts, rows


def test_micro_run_rows_strategies_and_columns(micro_run):
    out, counts, rows = micro_run
    assert counts == dict(total=2, skipped=0, ran=2)
    assert list(rows[0].keys()) == COLUMNS_MAIN and COLUMNS_MAIN[:len(COLUMNS)] == COLUMNS
    for iid in {r["instance_id"] for r in rows}:
        rs = [r for r in rows if r["instance_id"] == iid]
        strat = [r["strategy"] for r in rs]
        assert "B_maxpeak" not in strat
        for s in ("A", "B", "B_minpeak", "FRONT_top", "FRONT_PT", "C", "FCFS", "SPT", "EG", "BE_B", "BE_B_minpeak"):
            assert s in strat, s
        top = next(r for r in rs if r["strategy"] == "FRONT_top")
        # P is solved unless the energy optimum already sits on the structural peak bound (one-point front)
        assert ("P" in strat) == (top["front_termination"] != "structural_bound" or int(top["front_n_solves"]) > 1)
        for s in ("C_front", "PCG", "GUARD"):
            assert sorted(int(r["rho_paise"]) for r in rs if r["strategy"] == s) == [100, 1400]
        assert [int(r["rho_paise"]) for r in rs if r["strategy"] == "C"] == [1400]   # direct C only at the cross-check
        assert len({r["task_wall_s"] for r in rs}) == 1 and float(rs[0]["task_cpu_s"]) > 0


def test_micro_run_derived_values_are_consistent(micro_run):
    _, _, rows = micro_run
    for iid in {r["instance_id"] for r in rows}:
        rs = {(r["strategy"], int(r["rho_paise"])): r for r in rows if r["instance_id"] == iid}
        cf, cd = rs[("C_front", 1400)], rs[("C", 1400)]
        if cf["front_complete"] == "1" and int(cd["proven_stages"]) >= 1:
            assert cf["tec_int"] == cd["tec_int"]                              # front == direct C at rho 14
        for rho in (100, 1400):
            g, b = rs[("GUARD", rho)], rs[("B", 0)]
            b_tec = int(b["ec_int"]) + 60 * rho * int(b["peak_w"])
            assert int(g["tec_int"]) <= b_tec and int(g["tec_int"]) <= int(rs[("PCG", rho)]["tec_int"])
            if g["status"] == "OPTIMAL":
                assert int(g["tec_lower_bound"]) == int(g["tec_int"]) and float(g["gap"]) == 0.0
            c = rs[("C_front", rho)]
            if c["status"] == "OPTIMAL":
                assert c["front_complete"] == "1" and c["proven_stages"] == "2"
        assert rs[("BE_B", 0)]["break_even_kind"] in ("exact", "no_peak_reduction", "upper_bound", "undetermined")


def test_micro_run_is_resumable_and_refuses_other_designs(micro_run):
    out, _, rows = micro_run
    before = (out / "results.csv").read_text()
    again = run_experiment(MICRO, out, workers=1, progress=lambda *_: None)
    assert again == dict(total=2, skipped=2, ran=0)
    aggregate(out)
    assert (out / "results.csv").read_text() == before                         # deterministic aggregation
    with pytest.raises(RunnerError):
        run_experiment(replace(MICRO, seeds_per_cell=2), out, workers=1, progress=lambda *_: None)
