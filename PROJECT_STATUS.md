# PROJECT STATUS

## Current Phase

MATHEMATICAL BENCHMARK INDEPENDENTLY VERIFIED → CP-SAT IMPLEMENTATION READY

## Current Authoritative Documents

1. `00_project_overview/energy_scheduling_project_master_context.md`
2. `05_planning/master_execution_plan.md`
3. `04_mathematical_model/formulation/mathematical_model_v1.md` (Updated: Sequential Lexicographic Optimization & Duration-Weighted Power)
4. `04_mathematical_model/derivation/assumptions.md`
5. `04_mathematical_model/derivation/literature_to_equation.md`
6. `04_mathematical_model/verification/model_v1_preimplementation_audit.md` (Prompt 2B Pre-Implementation Audit Report)
7. `04_mathematical_model/verification/test_instances/hand_calculations.md` (Rectified: Proven Global Optima & True Breakeven)
8. `04_mathematical_model/verification/verify_benchmark.py` (NEW: Prompt 2C Independent Reproducible Verifier Script)
9. `04_mathematical_model/verification/benchmark_verification_results.md` (NEW: Prompt 2C Benchmark Verification Results Report)
10. `04_mathematical_model/verification/final_code_audit.md` (NEW: Prompt 2D Code-Level Audit Report)
11. `03_tariff/tariff_reference.md`
12. `09_hardware/current_hardware_spec.md`

## Completed

- SDG 9 direction
- Rubric analysis
- Project selection
- Research-gap audit
- Research validation
- KERC tariff verification
- Master execution plan
- Repository organization
- PZEM → INA226 hardware correction
- Canonical master context V2
- Phase 1: Literature extraction and audit (15 candidate papers, 8 core foundational papers)
- Phase 1: Dual-pagination literature-to-model matrix (`literature_to_model_matrix.md`)
- Phase 1: Pre-modelling defect and claim audit (`literature_audit_before_model_v1.md`)
- Phase 2: Canonical Mathematical Model V1.0 (`mathematical_model_v1.md`)
- Phase 2: Complete assumptions taxonomy & scope limits (`assumptions.md`)
- Phase 2: Literature-to-equation traceability map (`literature_to_equation.md`)
- Phase 2: Hand-solved benchmark verification & breakeven analysis (`hand_calculations.md`)
- Phase 2B: Pre-implementation mathematical verification audit (`model_v1_preimplementation_audit.md`)
- Phase 2B: Rectification of benchmark optimality (Strategy A makespan 4h, Strategy B EC ₹785.60, contiguous Strategy C)
- Phase 2B: Rectification of breakeven demand rate ($\rho^* = 12.70\text{ ₹/kW}$, shifted from ₹5.00/kW)
- Phase 2B: Mathematical replacement of weighted $\epsilon$ objectives with Sequential Lexicographic Optimization
- Phase 2C: Independent reproducible benchmark verification (`verify_benchmark.py`) — 24/24 assertions passed (including explicit contiguity verification and full parameter checks)
- Phase 2C: Comprehensive verification results report (`benchmark_verification_results.md`) — Verdict: VERIFIED
- Phase 2D: Final code-level audit of verification artifacts (`final_code_audit.md`) — Verdict: PASSED (6/6 criteria passed, implementation authorized)

## Current Hardware

- Raspberry Pi 5
- ESP32
- INA226
- 12V DC machine-load emulators
- relay/MOSFET switching

## Superseded

- PZEM-004T was an earlier proposed measurement device for the DC testbed and has been superseded by INA226.
- Single-pass weighted $\epsilon$ objectives in Model V1.0 have been superseded by Sequential Lexicographic Optimization.
- Preliminary hand-solved numbers in `hand_calculations.md` (makespan 5h, EC ₹862.60, breakeven ₹5.00) have been superseded by verified global optima.

## Current Research Task

Phase 3: Computational Implementation — Google OR-Tools CP-SAT formulation, data structures, and baseline unit test verification matching the verified benchmark ground truth.

## Immediate Deliverables

- Python data structures for jobs, machines, tariffs (`07_src/model/instance.py`, `tariff.py`)
- Two-phase sequential lexicographic CP-SAT model implementation with native interval vars (`07_src/model/scheduler.py`)
- Automated unit test suite verifying exact match to rectified benchmark numbers (`tests/test_benchmark.py`)
- Baseline solver benchmarking on Raspberry Pi 5

## Do Not Start Yet

- large experiments
- full hardware integration
- dashboard
- rolling-horizon optimization
- machine learning
- NSGA-III