P3 scaling probe and Gate 2 (ROADMAP-FINAL.md P3; decision D2).

    python 07_src/scripts/scaling_probe.py [--out results/scaling_probe] [--workers 2] [--sizes 8x3,12x4,16x5,20x6]

Sizes (jobs x machines) on the same 32-slot shift, gamma 19/14, W {0.40, 0.625} (below (M-1)/M for every size),
CV {0, 0.35}, 2 seeds, fresh base seed 20261121 (these instances are NOT reused by the main study). Budgets are the
Design defaults, identical to cal2 (stage 1: 60 det-s / 180 s wall; tie-breaks: 15 det-s / 60 s wall).

Per instance it runs the full main-study strategy set, so both proof rates and the cost of an M2 block are measured:
A, B, B_minpeak, the energy-peak front (top, P, capped solves), direct C at rho = 14 (cross-check of the front at
larger sizes), FCFS, energy-greedy, peak-capped greedy, and the safety guard at rho = 14 and the KERC-equivalent rho.

Gate 2 (approved D2): a size qualifies for a larger machine-count block only if >= 90 % of the REQUIRED front solves
are proven (top: EC stage; capped solves: EC stage or proven infeasible; P: min-peak stage, when solved). The share of
complete (exact) fronts is reported beside it. Nothing is dropped: every solve and status is in parts/*.json.
