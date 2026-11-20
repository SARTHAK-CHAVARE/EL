# PILOT-RESULTS — 27-instance pilot of the SPEC-002 full design (one seed per cell)

**Status: PRELIMINARY. This is a pilot with n = 1 instance per generation cell. Nothing here is a validated research finding.**
Confidence intervals in the pilot outputs are degenerate (one instance per cell → no within-cell resampling variance) and must not be quoted.
All numbers come from `results/pilot27/results.csv` and the scripts listed in §9; nothing was edited by hand.

## 1. Configuration (unchanged `DESIGN_FULL`, only `--seeds 1`)
| Item | Value |
|---|---|
| Command | `python 07_src/scripts/run_experiment.py --design full --seeds 1 --out results/pilot27 --workers 2` |
| Design digest | `37af47cf7472c2c4` (design `full`, `SPEC-002/v1`, seeds_per_cell = 1) |
| Cells / instances | γ {1, 19/14, 7/4} × W {0.40, 0.70, 0.90} × CV {0, 0.35, 0.75} = 27 cells, 27 instances (seed index 0) |
| Instance size | N = 8 jobs, M = 3 machines, T = 32 slots × 15 min, base load 2 kW, mean machine power 15 kW |
| ρ (repeated measure) | ₹5, ₹14, ₹50 per kW per horizon, strategy C solved at all three on every instance |
| Rows | 27 × (A, B, B_minpeak, B_maxpeak, P, C×3, FCFS, SPT) = 270 rows; 81 (instance, ρ) comparisons |
| Solver | OR-Tools CP-SAT 9.15, 1 worker per solve, redundant NoOverlap/Cumulative on; 2 instances in parallel |
| Configured limits | stage 1: 180 s wall / 60 s deterministic; tie-break stages: 60 s wall / 15 s deterministic |
| Machine | 2 cores, 8 GB (shared sandbox) |
| Run time | 04:01 → ≈04:12 UTC (≈ 11.6 min wall); Σ solver wall time 1371 s = 50.8 s per instance |
| Pre-flight | pytest 333 passed; benchmark reproduced (13/13); oracle 720/720 (100 %); working tree = only new untracked files; verifier untouched |

## 2. Execution result
27/27 instances completed, 0 missing, 0 crashes, 0 generator failures, digest check clean, no `InternalConsistencyError`
(every returned schedule passed the independent evaluator). Coverage: 27 present / 27 expected.

## 3. Optimality (rows; OPTIMAL = every lexicographic stage proven)
| Strategy | Rows | OPTIMAL | Stage 1 proven | Max wall (s) |
|---|---|---|---|---|
| A | 27 | 27 (100 %) | 27 | 3.0 |
| B | 27 | 27 (100 %) | 27 | 1.1 |
| B_minpeak | 27 | 27 (100 %) | 27 | 2.3 |
| B_maxpeak | 27 | 25 (92.6 %) | 27 | 25.2 |
| P | 27 | 27 (100 %) | 27 | 48.1 |
| **C** | 81 | **59 (72.8 %)** | **75 (92.6 %)** | 67.8 |

**Stage-wise completion for C** (the only strategy with real trouble): 59 rows fully proven; 16 rows stage 1 proven but the
makespan tie-break (stage 2) not; 6 rows stage 1 itself unproven. B_maxpeak: 2 rows with stages 1–2 proven, stage 3 (max peak) not.
Unproven by ρ: ₹5: 1 of 27, ₹14: 10 of 27, ₹50: 11 of 27 — difficulty rises steeply with ρ.
Heuristics: no solver involved.

**What the time limits really were.** The largest single solve took 67.8 s. Rows with an unproven stage 1 stop at 55–68 s total, and rows with an unproven tie-break total 14–68 s (stage-1 time plus ≈15 s; per-stage times are not stored in the CSV): the **deterministic** limits (60 s / 15 s) bind, the configured 180 s / 60 s wall limits never
did in the pilot. The "180 s / 60 s" wording in the design therefore overstates the budget actually applied.

## 4. Runtime (s per strategy run, 1 worker)
| Strategy | n | mean | median | p95 | max |
|---|---|---|---|---|---|
| A | 27 | 1.4 | 1.2 | 2.7 | 3.0 |
| B | 27 | 0.7 | 0.7 | 1.0 | 1.1 |
| B_minpeak | 27 | 1.1 | 0.9 | 2.1 | 2.3 |
| B_maxpeak | 27 | 3.9 | 1.0 | 20.5 | 25.2 |
| P | 27 | 7.3 | 1.3 | 41.0 | 48.1 |
| C | 81 | 12.2 | 1.8 | 60.9 | 67.8 |

Per instance (all strategies): mean 50.8 s, median 24.2 s, sd 53.1 s, max 170.5 s (heavy-tailed).

**By factor (C and P).** By W (mean s / unproven C rows of 27): 0.40 → 14.3 / 8; **0.70 → 21.0 / 14**; 0.90 → 1.1 / 0. By CV: 0 → 3.9 / 5;
**0.35 → 23.6 / 12**; 0.75 → 8.9 / 5. By γ: 12.4 / 7 (γ=1), 14.3 / 9 (19/14), 9.8 / 6 (7/4) — no clear γ effect. By ρ: 2.5 / 1, 12.3 / 10, 21.7 / 11 (₹5/14/50).
With one instance per cell these are single draws; the CV = 0.35 column in particular is 9 instances and may reflect instance luck.

## 5. Savings, trade-offs, robustness (all PRELIMINARY, descriptive)
**Saving of C over B (TEC, %), mean over valid rows:** ₹5: 0.59 (27/27 valid), ₹14: 1.89 (26/27), ₹50: 2.87 (22/27).
Pooled means hide that the effect is concentrated: **only 4 of 27 instances show any possible peak reduction, all at W = 0.40**
(CV 0: γ = 1, 19/14, 7/4; CV 0.35: γ = 7/4). Among W = 0.40 instances the mean saving is 1.8 / 6.1 / 10.5 % at ₹5 / 14 / 50.
**All 18 instances with W = 0.70 or 0.90 show exactly 0 % saving at every ρ**: the energy-optimal schedule B already has the
minimum possible peak (B peak = P peak in 18/18). The minimum feasible makespan of A leaves slack of 56.6 % of T at W = 0.40, 23.3 % at 0.70 and 2.8 % at 0.90.
Mean saving by γ (₹5 / 14 / 50): γ=1: 0.6 / 1.3 / 2.7; 19/14: 0.2 / 1.2 / 3.0; 7/4: 0.9 / 3.1 / 3.0 (driven by the same 4 instances). CV 0.75: zero everywhere.

**The four informative instances** (saving %, ₹5 / 14 / 50): g0w0c0 (γ=1) 5.6 / 12.0 / 21.8; g1w0c0 (19/14) 1.8 / 9.4 / 20.7; g2w0c0 (7/4) 0.1 / 8.7 / 20.7;
g2w0c1 (7/4, CV 0.35) 8.3 / 19.0 / — (₹50 row unproven). Peak reduction when it exists: 31.9 % (47 → 32 kW) or 45.6 % (47 → 25.6 kW);
energy-cost increase 0–8.2 %; makespan penalty 0 or 33.3 % (the γ=1 instance).
Trade-off summary on fully-proven rows (n = 26 / 17 / 16 at ₹5/14/50): mean peak reduction 5.4 / 4.6 / 6.0 %, mean energy increase 0.6 / 0.1 / 0.8 %,
mean makespan penalty 1.3 / 2.0 / 2.1 %; medians are 0 (most instances cannot be improved). Only 59/81 rows are fully proven, so these are biased to easier rows.

**B_minpeak / B_maxpeak robustness band.** Peak spread between B_maxpeak and B_minpeak is **0 kW in all 25 instances where both are proven**
(and B, B_minpeak, B_maxpeak peaks coincide in all 27). The band therefore has zero width in this pilot. Savings vs B_minpeak / B / B_maxpeak: 0.59 / 0.59 / 0.63 (₹5),
1.89 / 1.89 / 2.04 (₹14), 2.87 / 2.87 / 3.01 (₹50) — differences come only from which rows are valid, not from tie-break ambiguity.

**Break-even ρ\*_ub (upper bound).** Defined for the 4 instances with possible peak reduction: 0.00, 0.93, 3.50, 4.95 ₹/kW (all < ₹5); 23 instances: "no peak reduction possible".
These are upper bounds on the smallest ρ at which C beats the energy-only schedule; the lowest ρ level (₹5) is above all of them, so the pilot never sees the below-threshold regime.

## 6. Heuristics, exclusions, generator
**FCFS / SPT feasibility** (deadline met): FCFS 25/27 (92.6 %), SPT 17/27 (63.0 %). By W (0.40 / 0.70 / 0.90): FCFS 100 / 89 / 89 %; SPT 100 / 78 / **11 %**. SPT is nearly useless as a baseline at W = 0.90.
**Missing / excluded** (never dropped silently): missing 0. Unproven → excluded: saving_valid 6 of 81 rows, full_valid 22 of 81, band_valid_Bmin 6, band_valid_Bmax 11.
**Generator acceptance** (FCFS-or-SPT feasibility filter): W = 0.40 and 0.70: 100 % (1.0 attempts); **W = 0.90: 8.0 % (12.4 attempts mean, max 26)**. Realised W (time-based formula): 0.39–0.42, 0.69–0.72, 0.90–0.92.
Selection bias: at W = 0.90 only instances that a dispatch rule can fit within the horizon are kept; these instances have 2.8 % makespan slack, i.e. they sit at the feasibility edge.
How much this shapes the W = 0.90 results cannot be quantified from accepted instances alone.

## 7. Budget diagnostic (separate from the pilot dataset)
`results/pilot27/budget_diagnostic.py` re-solved 6 stage-1-unproven and 3 tie-break-unproven C rows with larger limits (stage 1: 180 s det / 180 s wall; tie-break: 60 s / 60 s). Factor levels untouched.
| Pilot row | Pilot (60 s/15 s det) | Larger limits |
|---|---|---|
| g1w0c1 ρ₹14, g1w1c1 ρ₹50, g2w0c1 ρ₹50 | stage 1 unproven | stage 1 **proven** after 54 / 83 / 161 s, **same value as the pilot incumbent**; tie-break still unproven at 60 s |
| g0w0c1 ρ₹50, g1w0c1 ρ₹50, g2w1c1 ρ₹50 | stage 1 unproven | still unproven after 145 / 152 / 180 s, incumbent value unchanged |
| g0w1c1 ρ₹14 | tie-break unproven | tie-break **proven** (27.5 s) |
| g1w0c0 ρ₹14, g2w1c0 ρ₹50 | tie-break unproven | still unproven after 57 / 52 s (stage 1 took < 1 s) |
Reading: in all 6 stage-1 cases the incumbent cost found within the pilot budget was never improved by 2–3× more time (3 of 6 were then proven optimal); more time buys *proof*, not better schedules.
The makespan tie-break is the expensive part: stage 1 can finish in < 1 s while proving min C_max among cost-optimal schedules does not finish in 60 s.

## 8. Evidence-based recommendations
1. **Time budgets.** The configured 180 s / 60 s wall limits are not what is applied; the deterministic 60 s / 15 s limits are. Either state the effective limits in SPEC-002 or set them deliberately. Raising the stage-1 limit to 180 s would
   convert about half of the 6 stage-1-unproven rows to proven (+~100 s each; extrapolated +46 s per instance) without changing any value; I recommend **not** raising it and instead keeping the 6/81 (7.4 %) unproven-stage-1 rows excluded and counted.
   Makespan/peak/energy comparisons are available for only 59/81 rows (73 %), biased to easier rows; if those comparisons matter for the report, the tie-break stage budget (or a tighter tie-break formulation) is the lever. No change made.
2. **Instance size N = 8, M = 3, T = 32.** Solvable (all A/B/P/B_minpeak 100 % optimal; C 92.6 % stage 1). It is large enough to be non-trivial at W ≤ 0.70 and small enough to run. But at W = 0.70/0.90 the deadline leaves no flexibility (see §5), so size alone is not the problem — the W levels are.
3. **W levels.** 2 of 3 W levels (18 of 27 instances) gave identical energy-optimal and min-peak schedules and exactly 0 saving at all ρ; the transition lies between W = 0.40 and 0.70, which the grid does not resolve. W = 0.90 is also the cheapest to solve (1.1 s) but the most expensive to *generate* (8 % acceptance) and has 11 % SPT feasibility.
   "No savings at high utilisation" is itself a legitimate finding, but running 405 instances with two-thirds of the grid at a known null would spend compute on little information. I recommend a decision on W levels (e.g. replacing 0.90 and adding a level between 0.40 and 0.70, or lowering all levels) **before** the full run. Not changed here.
4. **ρ levels.** ρ separates the effect where it exists (W = 0.40: 1.8 → 6.1 → 10.5 %), so ₹5/14/50 do carry information; but all four observed break-even upper bounds are below ₹5, so there is no sub-threshold level. Consider adding a level around ₹1–2 if the break-even regime matters for the report. ρ = ₹50 is also the most expensive level (11/27 unproven).
5. **B_maxpeak.** Zero tie-break spread in 25/25 proven cases and the second-most unproven strategy; its only value so far is the (so far zero-width) robustness band. Candidate to keep only on a subset, but retained pending the second-pilot decision.
6. **SPT baseline** is infeasible for 89 % of W = 0.90 instances; baseline comparisons at high W rest on FCFS only.
7. **High-workload difficulty.** Solver difficulty is **not** monotone in W: W = 0.70 is hardest (mean C 21.0 s, 14/27 unproven), W = 0.90 is easiest (1.1 s, 0/27) because the deadline nearly forces the schedule. "High workload is disproportionately difficult" holds for 0.70 vs 0.40, not for 0.90.

## 9. Full-experiment feasibility and go/no-go
**Time.** At the limits actually applied: 405 × 50.8 s = 5.7 core-hours ≈ **2.9 h wall on 2 workers** (bootstrap 95 % interval of the pilot mean 32–71 s per instance → 1.8–4.0 h; heavy-tailed, n = 27). If the stage-1 limit were raised to 180 s: ≈ 10.9 core-hours ≈ 5.4 h on 2 workers (extrapolation).
The deadline (demo 1 Dec, submission 7 Dec) leaves ample room for either. The run is resumable and deterministic, but a process left running when a session ends is usually stopped, so it should be run on a machine that stays on, or in resumed chunks.

**Recommendation.**
* **Infrastructure: GO.** The pipeline ran end to end without failure; validity filtering, exclusion counting and digest protection behaved as specified.
* **Full 405-instance run as currently specified: HOLD — decision needed from you, then GO.** It is technically achievable (~3 h), but the pilot shows the current W/ρ grid will mostly document a null region and misses the break-even regime. Options:
  (A) launch as specified — cheap, yields a valid map including the "no savings at W ≥ 0.70" boundary, thin signal (informative cells ≈ one third, only W = 0.40 so far);
  (B, my recommendation) first run a second, ≈15-instance pilot of a *revised* grid (more W levels between 0.20 and 0.70, one lower ρ), report it as a design-calibration step, then fix SPEC-002 and launch. This needs a small CLI/design variant that does not exist yet and was not implemented here.
* The pilot sample (n = 1 per cell) cannot support claims about γ or CV effects; ignore the pilot's γ/CV patterns.

## 10. Where things are
| What | Location |
|---|---|
| Raw results (270 rows) / manifest | `results/pilot27/results.csv`, `results/pilot27/manifest.json`, `parts/` |
| Analysis tables | `results/pilot27/analysis/*.csv`, `README.txt` (stamped PRELIMINARY) |
| Detailed text summary (all numbers above) | `results/pilot27/analysis/pilot_summary.txt`, `pilot_extra.txt`; script `results/pilot27/pilot_summary.py` |
| Figures | `results/pilot27/analysis/fig_saving_vs_rho.png`, `fig_phase_map_gamma_W.png`, `fig_phase_map_cv_W.png`, `fig_tradeoff_energy_peak.png`, `fig_tradeoff_makespan_saving.png`, `fig_peak_by_strategy.png`, `fig_breakeven_ecdf.png`, `fig_runtime.png` |
| Budget diagnostic | `results/pilot27/budget_diagnostic.py`, `results/pilot27/diagnostics/budget_diagnostic.csv` |
| Run log | `results/pilot27.log` |
Figures show one instance per cell; their error bars are degenerate and the "saving vs ρ" curve pools only a few non-zero instances.

## 11. Limitations of this pilot
n = 1 per cell (no inference); a single machine, 2 workers sharing cores (wall times are indicative); deterministic-limit stops depend on solver internals; savings are Model A (normalised ρ), not the real KERC ₹/kVA tariff;
excluded rows (22 of 81 for makespan/peak comparisons) bias those summaries toward easier instances; no hardware data of any kind is involved.
