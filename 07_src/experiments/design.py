"""Experimental design (SPEC-002): factor levels, profiles and task enumeration.

``DESIGN_FULL`` is the proposed factorial; ``DESIGN_SMOKE`` is a tiny design used only to validate the
pipeline. The design is hashed into the run manifest so that a resumed run can never silently mix
results from different designs.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, replace
from fractions import Fraction
from typing import List, Tuple

DESIGN_VERSION = "SPEC-002/v1"


@dataclass(frozen=True)
class Design:
    name: str = "full"
    # factors ---------------------------------------------------------------------------------
    gammas: Tuple[str, ...] = ("1", "19/14", "7/4")       # peak/off-peak tariff ratio (exact fractions)
    workloads: Tuple[str, ...] = ("0.40", "0.70", "0.90")  # W = sum_j min_m p_jm / (M*D)
    cvs: Tuple[str, ...] = ("0", "0.35", "0.75")           # coefficient of variation of machine powers
    rho_inr: Tuple[str, ...] = ("5", "14", "50")           # INR/kW per scheduling horizon (evaluated, not generated)
    seeds_per_cell: int = 15
    # profile (SPEC-001 D6 "experiment") ---------------------------------------------------------
    n_jobs: int = 8
    n_machines: int = 3
    T: int = 32
    delta_t_min: int = 15
    base_kw: str = "2"
    mean_power_kw: str = "15"
    shift_start_hour: int = 16          # 16:00-24:00: contains normal, peak and off-peak tiers
    normal_inr: str = "6.60"            # KERC HT-2(a) base energy charge (tariff_reference.md)
    proc_noise: Tuple[str, str] = ("0.7", "1.3")  # multiplier range u_jm on machine-independent size
    base_seed: int = 20261115
    max_attempts: int = 200
    solver_time_limit_s: float = 180.0        # stage 1 (primary objective), wall clock
    solver_det_time_limit: float = 60.0       # stage 1, machine-load independent
    tiebreak_time_limit_s: float = 60.0       # stages >= 2 (compactness / peak tie-breaks)
    tiebreak_det_time_limit: float = 15.0

    @property
    def version(self) -> str:
        """Design-family version string (hashed into the digest, stored in manifest and result rows)."""
        return DESIGN_VERSION

    def digest(self) -> str:
        """Identity of the design (all fields + design version). Any change gives a different digest."""
        payload = dict(asdict(self), _design_version=self.version)
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:16]


@dataclass(frozen=True)
class Task:
    instance_id: str
    gamma_idx: int
    w_idx: int
    cv_idx: int
    seed_idx: int


def enumerate_tasks(design: Design) -> List[Task]:
    tasks = []
    for gi in range(len(design.gammas)):
        for wi in range(len(design.workloads)):
            for ci in range(len(design.cvs)):
                for s in range(design.seeds_per_cell):
                    tasks.append(Task(f"g{gi}w{wi}c{ci}s{s:03d}", gi, wi, ci, s))
    return tasks


def frac(s: str) -> Fraction:
    return Fraction(s)


DESIGN_FULL = Design()


@dataclass(frozen=True)
class CalibrationDesign(Design):
    """Calibration designs (SPEC-002 v2 proposal). Same fields as ``Design``; only the version string differs, so the
    digest of every calibration design is distinct from every v1 design and ``DESIGN_FULL`` is left untouched."""

    @property
    def version(self) -> str:
        return CALIBRATION_VERSION


CALIBRATION_VERSION = "SPEC-002/v2-cal1"

#: Second calibration pilot (PROPOSED, not yet executed): workload transition region + low-rho region.
#: Same instance size, tariff, power and solver budgets as the v1 pilot, so results are comparable.
#: 5 W x 3 gamma x 3 CV = 45 generation cells x 2 seeds = 90 instances, each evaluated at 5 rho (paired).
DESIGN_CAL2 = CalibrationDesign(
    name="cal2-v1",
    workloads=("0.40", "0.475", "0.55", "0.625", "0.70"),
    rho_inr=("1", "2", "5", "14", "50"),
    seeds_per_cell=2,
    base_seed=20261116,
)

#: Tiny design for validating the pipeline. Its output is NOT a research result.
DESIGN_SMOKE = Design(name="smoke", gammas=("19/14",), workloads=("0.40", "0.90"), cvs=("0.35",),
                      rho_inr=("5", "50"), seeds_per_cell=2, n_jobs=6, solver_time_limit_s=30.0,
                      solver_det_time_limit=10.0, tiebreak_time_limit_s=10.0, tiebreak_det_time_limit=4.0)


# ================================================================================ SPEC-003 main study
MAIN_VERSION = "SPEC-003/v1"


@dataclass(frozen=True)
class MainDesign(Design):
    """SPEC-003 main-study designs (docs/handoff/SPEC-003-main-study.md).

    Strategy protocol (runner.run_task_main): A, B, B_minpeak, the energy-peak front (top, P, capped solves),
    direct C at ``cross_check_rho_inr`` only, FCFS, SPT, energy-greedy (EG), peak-capped greedy (PCG) and the guard.
    ``rho_inr`` are EVALUATED from the front (no solve per rho). No B_maxpeak. The extra fields and the version make
    every MainDesign digest distinct from all SPEC-002 designs, whose digests are unchanged.
    """
    cross_check_rho_inr: str = "14"
    block: str = "M3"

    @property
    def version(self) -> str:
        return MAIN_VERSION


RHO_GRID_MAIN = ("1", "2", "5", "14", "50")
#: Primary block: 3 gamma x 4 W x 3 CV = 36 cells x 15 seeds = 540 instances (fresh base seed).
DESIGN_MAIN_M3 = MainDesign(name="main-m3-v1", block="M3", workloads=("0.40", "0.475", "0.55", "0.625"),
                            rho_inr=RHO_GRID_MAIN, seeds_per_cell=15, base_seed=20261123)
#: Conditional block (Gate 2: M2 = 12 x 4): 1 gamma x 3 W x 2 CV = 6 cells x 10 seeds = 60 instances.
DESIGN_MAIN_M4 = MainDesign(name="main-m4-v1", block="M4", gammas=("19/14",), workloads=("0.40", "0.55", "0.70"),
                            cvs=("0", "0.35"), rho_inr=RHO_GRID_MAIN, seeds_per_cell=10, n_jobs=12, n_machines=4,
                            base_seed=20261123)
#: P4 smoke runs: same protocol and budgets, every cell, separate names and base seed (never reused by the main run).
DESIGN_MAIN_M3_SMOKE = replace(DESIGN_MAIN_M3, name="main-m3-smoke", seeds_per_cell=1, base_seed=20261122)
DESIGN_MAIN_M4_SMOKE = replace(DESIGN_MAIN_M4, name="main-m4-smoke", seeds_per_cell=2, base_seed=20261122)

#: name -> design, used by the CLI. Adding a design here never changes another design's digest.
DESIGNS = {"smoke": DESIGN_SMOKE, "full": DESIGN_FULL, "cal2": DESIGN_CAL2,
           "main-m3": DESIGN_MAIN_M3, "main-m4": DESIGN_MAIN_M4,
           "main-m3-smoke": DESIGN_MAIN_M3_SMOKE, "main-m4-smoke": DESIGN_MAIN_M4_SMOKE}
