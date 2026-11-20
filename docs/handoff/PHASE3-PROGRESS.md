# Phase 3 progress report (2026-11-15)

| Item | State | Evidence |
|---|---|---|
| SPEC-001 solver spec | done | `docs/handoff/SPEC-001-solver.md` |
| CP-SAT engine (A, B, C, P; lexicographic; integer arithmetic) | **working implementation** | 341 tests pass |
| Benchmark reproduction (₹785.60, ₹912.60, 27 kW, ρ* ₹12.70) | reproduced (metrics) | `reproduce_benchmark.py`, 13/13 |
| Oracle cross-check | 720/720 agree (120 instances × 6 strategies; 180 are infeasible-instance agreements) | `run_oracle_report.py` |
| Experiment generator, FCFS/SPT, resumable runner | working, tested (determinism, resume, manifest guard) | `tests/test_experiments.py` |
| Analysis scripts | working on smoke data only | `tests/test_analysis.py` |
| SPEC-002 + docs | written | `docs/` |
| 27-instance pilot | **executed (PRELIMINARY)** | `docs/handoff/PILOT-RESULTS.md` |
| Calibration design cal2-v1 | **prepared, not run** — awaiting approval | `docs/handoff/SPEC-002-v2-proposal.md` |
| Full factorial (405 instances) | **not run** | on hold: grid mostly null at W >= 0.70 (pilot) |
| Results for the report | **none yet** (smoke output is pipeline validation only) | — |
| Hardware / serial executor | not started | no measurements exist |

## Known issues
1. Solve time on low-W/high-ρ instances: stage 1 15–25 s and the stage-2 compactness tie-break 70–115 s in single-worker
   probes (N=8, T=32, before budgets). Under the *smoke* budgets (30 s wall / 10 s deterministic) 3 of 12 optimisation
   rows ended FEASIBLE with **stage 1 itself unproven** (`proven_stages = 0`), so earlier wording that blamed only the
   tie-break stage was too optimistic. The pilot showed the *deterministic* limits (60/15 s) are the ones that bind, not the 180/60 s wall limits (PILOT-RESULTS §3, §7).
2. Smoke savings are mostly 0 at ρ=₹50 on the 2 valid instances — instance size/ρ levels may need tuning (U4).
3. SPT/FCFS fail the deadline on some instances (recorded as NO_SCHEDULE).
4. Generator acceptance filter biases high-W cells toward easier instances.

## Remaining for Phase 3
Approve and run cal2 → calibration analysis → freeze SPEC-002 v2 → full run → validated analysis → report figures/text; optional schedule export for the
testbed; hardware validation only if hardware is available.

## Next actions
1. Decide D1–D4 in `SPEC-002-v2-proposal.md`, then run the cal2 calibration (~1 h on 2 workers) and freeze the v2 design.
2. Launch the full factorial only after that, then regenerate the analysis with `--validated`.
3. Put benchmark reproduction, oracle agreement and the validated saving-vs-ρ figure into the report.
