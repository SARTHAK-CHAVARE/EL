# CAL2 RESULTS — calibration run `cal2-v1` (descriptive only)

> **Status: CALIBRATION, 2 seeds per generation cell. Everything below is descriptive: counts, shares, means over proven rows.
> There are no confidence intervals, tests or effect sizes, and none of it is a validated research finding.**
> Realised numbers come from `results/cal2/` (digest `99596784481ea861`, `results.csv` sha256 prefix `857b9f1c1ef4b912`).
> W always means the **nominal** workload level; realised `w_real` is given next to it. ρ is in INR/kW per horizon (Model A).

## 1. What was run
| | |
|---|---|
| Design | `cal2-v1` (`SPEC-002/v2-cal1`): γ {1, 19/14, 7/4} × W {0.40, 0.475, 0.55, 0.625, 0.70} × CV {0, 0.35, 0.75} × 2 seeds = **90 instances**; ρ {1, 2, 5, 14, 50} (paired: same instance at every ρ) |
| Command | `run_experiment.py --design cal2 --out results/cal2 --workers 2` (unchanged model, solver and limits: 60 s stage 1 / 15 s tie-break, deterministic) |
| Completeness | 90/90 instances, **1080/1080 rows, 0 missing, 0 duplicate, 0 unexpected**; one design digest in every row |
| Time | 05:24:19 → 06:04:38 UTC = **40.3 min wall**; solver time 4750 s = **1.32 CPU-h** (52.8 s/instance) vs estimate 1.96 CPU-h (range 1.30–2.58) and ≈ 0.98 h wall: the estimate was ~33 % high, actual sits at the bottom of its range |
| Not touched | model, solver, `DESIGN_FULL`, `results/pilot27`, `04_mathematical_model/verification/*` (verified before and after) |

Pre-flight: 359 tests, benchmark 13/13, oracle 720/720, digests and the pilot hash unchanged. Nothing committed.

## 2. Headline observations (all descriptive)
1. **A possible peak reduction ("conflict") exists in the middle of the W range, not at its ends as the pilot suggested.** Share of determined instances with conflict: 0.47 / 0.61 / 0.72 / 0.78 at W = 0.40 / 0.475 / 0.55 / 0.625, then **0 of 14 at W = 0.70** (4 further instances undetermined). It *rises* with W up to 0.625 and then collapses; the location of the collapse between 0.625 and 0.70 is not resolved. The pilot's grid (0.40, 0.70, 0.90) had no level in between, and it saw savings only at 0.40.
2. **Where conflict exists, saving depends strongly on ρ.** Among valid conflict instances: positive saving in 33 % at ρ = 1, 48 % at 2, 74 % at 5 and **100 % at 14 and 50**; mean saving 0.4 / 1.0 / 3.8 / 11.6 / 24.0 %. The sub-threshold region (ρ = 1, 2) is captured.
3. **Break-even upper bounds lie between INR 0 and 11.5** (median 2.3, quartiles 0.7 and 5.3) for all 46 conflict instances; ρ = 1, 2, 5, 14 span them, ρ = 50 lies above every one.
4. **CV is not a clean factor in this generator** (§8): CV = 0 gives conflict in 24/24 instances at W ≤ 0.625; CV = 0.75 gives 0/12 at W ≤ 0.475 but 7/12 at 0.55–0.625.
5. **Seeds agree for CV = 0 but not always for CV > 0:** the conflict indicator agrees across the two seeds in 15/15 CV = 0 cells and 19/25 CV > 0 cells.
6. **Solver difficulty concentrates at high ρ and at W = 0.40 / 0.70**; 18 of 450 C rows have an unproven cost stage (all excluded and counted).

## 3. E1 — conflict indicator by workload
Conflict = the energy-only optimum B can be beaten on peak (B peak > min-peak P); "none" = B already attains the minimum peak; "undetermined" = P (or B) not proven. Share is over determined instances.

| W (nominal) | `w_real` mean [min–max] | instances | conflict | none | undetermined | share |
|---|---|---|---|---|---|---|
| 0.40 | 0.396 [0.375–0.406] | 18 | 8 | 9 | 1 | 0.47 |
| 0.475 | 0.475 [0.458–0.490] | 18 | 11 | 7 | 0 | 0.61 |
| 0.55 | 0.545 [0.531–0.552] | 18 | 13 | 5 | 0 | 0.72 |
| 0.625 | 0.624 [0.615–0.635] | 18 | 14 | 4 | 0 | 0.78 |
| 0.70 | 0.697 [0.677–0.708] | 18 | 0 | 14 | 4 | 0.00 |

By CV (conflict / determined, W = 0.40 · 0.475 · 0.55 · 0.625 · 0.70): **CV 0:** 6/6 · 6/6 · 6/6 · 6/6 · 0/6. **CV 0.35:** 2/5 · 5/6 · 3/6 · 5/6 · 0/5. **CV 0.75:** 0/6 · 0/6 · 4/6 · 3/6 · 0/3.
By γ the share over W ≤ 0.625 is 0.33–0.67 (γ = 1), 0.40–0.83 (19/14) and 0.67–1.00 (7/4); at each W it is non-decreasing with γ (ties between 19/14 and 7/4 at 0.475 and 0.625; tables: `calibration/e1_*.csv`).
Mechanism for the collapse at 0.70 is not tested: in the pilot, too, B already had the minimum peak in 18/18 instances at W ≥ 0.70.
Figure: `calibration/fig_e1_conflict_by_W.png`.

## 4. E2 — replicate agreement (2 seeds per cell, 45 cells)
| W | both conflict | both none | seeds disagree | undetermined | agreement among determined |
|---|---|---|---|---|---|
| 0.40 | 4 | 4 | 0 | 1 | 8/8 |
| 0.475 | 5 | 3 | 1 | 0 | 8/9 |
| 0.55 | 6 | 2 | 1 | 0 | 8/9 |
| 0.625 | 5 | 0 | **4** | 0 | 5/9 |
| 0.70 | 0 | 5 | 0 | 4 | 5/5 |
| all | 20 | 14 | 6 | 5 | **34/40 (85 %)** |

All six disagreeing cells have CV > 0 (CV 0.35: 3 of 13 determined cells; CV 0.75: 3 of 12; CV 0: 0 of 15), and in them the two seeds have the *same* `w_real` in 5 of 6 cells, so the disagreement is instance-to-instance variation, not a workload difference. Saving magnitudes also vary: at ρ = 50, in 5 of the 23 cells with any saving one seed has zero saving and the other positive, and the largest within-cell gap is 42 pp. With n = 2 this shows that CV > 0 cells are noisy; it does not measure how noisy.

## 5. E3 — savings across all five ρ levels (C vs energy-only B)
Valid = B fully proven and C cost stage proven. Mean over valid rows; "positive" = strictly positive saving.

| ρ | conflict instances: valid / positive / mean % / max % | all 90 instances: valid / positive / mean % | excluded (unproven) |
|---|---|---|---|
| 1 | 46 / 15 / 0.36 / 1.9 | 90 / 15 / 0.18 | 0 |
| 2 | 46 / 22 / 1.00 / 3.8 | 90 / 23 / 0.54 | 0 |
| 5 | 46 / 34 / 3.76 / 10.3 | 90 / 35 / 2.01 | 0 |
| 14 | 45 / 45 / 11.63 / 24.7 | 87 / 45 / 6.02 | 3 |
| 50 | 41 / 41 / 24.00 / 44.4 | 75 / 41 / 13.12 | 15 |

Mean saving over valid rows by W at ρ = 14 / 50 (all instances): 0.40: 6.1 / 9.9; 0.475: 6.7 / 11.9; 0.55: 10.1 / 20.8; 0.625: 6.9 / 16.8; **0.70: 0 / 0**. At every ρ the W = 0.70 saving is exactly 0 in all valid rows. By γ (ρ = 50, mean over the 25 valid rows each): γ = 1 8.0 %, 19/14 14.4 %, 7/4 17.0 % (ρ = 14: 3.5 / 7.4 / 7.3 %).

**Break-even upper bounds** (46 conflict instances, `calibration/e3_breakeven_*.csv`): median 2.3, quartiles 0.7 / 5.3, max 11.5 INR/kW; instances with bound ≤ ρ: 15 (ρ=1), 22 (2), 34 (5), 46 (14), 46 (50). By W the medians are 1.8 / 2.4 / 1.7 / 4.8 (0.40 → 0.625). These are *upper bounds*; in this data they were also tight: for all 224 valid conflict rows saving is positive exactly when ρ exceeds the bound (157/157) and zero when it is below (67/67).

Consistency checks run on the outputs: in 187/187 valid rows of "no conflict" instances saving is exactly 0; the saving of a row recomputed from raw integers equals the table value; minimum saving over valid rows is 0 (C never worse than B).

**Read this together with the exclusions.** Excluded rows are the hard instances, and at ρ = 50 they concentrate in CV = 0.35 (14 of 30 rows) and W = 0.70 (7 of 18). In the ρ = 50 phase map the cell (CV 0.35, W 0.40) rests on 1 of 6 valid rows and (CV 0.35, W 0.70) on 0 of 6 (`analysis/fig_phase_map_cv_W.png` prints n_valid/n_total in every cell). The ρ = 50 means, and any CV comparison at ρ = 50, are therefore not comparable across cells.

## 6. E4 — solver status, missing results, runtime, generator
**Optimality (rows):** A 90/90, B 90/90, B_minpeak 90/90, B_maxpeak 75/90 (stage-3 tie-break unproven in 15), P 85/90 (**5 with cost stage unproven**), C 383/450 fully proven (85.1 %), 432/450 cost stage proven (96.0 %). FCFS feasible 89/90, SPT 90/90. **Missing: 0.**

**Strategy C by ρ** (rows: fully proven / cost proven only / cost unproven): ρ = 1: 90/0/0; 2: 90/0/0; 5: 87/3/0; 14: 65/22/3; 50: 51/24/15. By W (cost unproven of 90): 0.40: 6; 0.475: 3; 0.55: 0; 0.625: 1; 0.70: 8. Of the 18 cost-unproven rows, 17 are CV = 0.35. **[Corrected 20 Nov 2026]** An earlier version of this sentence said the 18 incumbents were "40–185 % worse than B". That was an analysis error: it compared C's cost at ρ (energy plus demand charge) with B's cost at ρ = 0 (energy only). At the same ρ, none of the 18 incumbents costs more than B, and the energy–peak front (`results/front_validation/`) proves 17 of them optimal. They were correctly excluded as unproven at the time, but they were not bad schedules.

**Exclusions by validity flag (450 paired rows):** saving 432 valid / 18 unproven / 0 missing; full (peak, energy, makespan) 383 / 67 / 0; vs B_minpeak 432 / 18 / 0; vs B_maxpeak 359 / 91 / 0. Of the 18 cost-unproven C rows, 8 belong to "no conflict" instances, where zero saving is implied without C (B is simultaneously energy-optimal and peak-optimal), 6 to conflict instances and 4 to undetermined ones. This inference was **not** applied to the cal2 tables.

**Runtime.** Mean CPU per instance by W (s): 75.4 / 38.7 / 29.2 / 36.9 / 83.6 (0.40 → 0.70); max instance 174 s. Strategy C is 68 % of solver time (ρ = 50: 36 %, ρ = 14: 20 %, ρ = 1 and 2 together: 6 %). Mean wall per C solve at ρ = 1 / 2 / 5 / 14 / 50: 1.2 / 1.9 / 3.2 / 10.4 / 19.2 s; longest 72.8 s.

**Generator acceptance.** 89/90 instances were accepted on the first draw; the single exception is `g1w4c1s000` (W = 0.70, 2 draws), as pinned by the pre-run test (generation is deterministic). The acceptance study (`results/cal2_prep`) gave 100 % up to W = 0.65 and 99.2 % at 0.70; observed first-draw acceptance: 72/72 for W ≤ 0.625, 17/18 at 0.70. The filter is practically inert in this design.

**Nominal vs realised W.** `w_real` is on a 1/96 grid; |w_real − W| ≤ 0.025 (max over all instances), mean offset −0.0025. Realised ranges of neighbouring levels do not overlap (table in §3, `calibration/workload_nominal_vs_realised.csv`, `fig_workload_nominal_vs_realised.png`).

## 7. Pre-stated predictions (written down before the run)
| | Prediction (SPEC-002-v2-proposal §3) | Outcome |
|---|---|---|
| (a) | conflict share decreases with W | **Not supported.** The share rises 0.47 → 0.78 over W = 0.40 → 0.625 (three of four steps increase) and is 0 at 0.70. The tool's label `held_non_monotone` only compares the first and last level and should not be quoted; this endpoint rule is a weakness to remove before the main study. |
| (b) | conflict ≈ 0 for CV > 0 at every W (dominance mechanism) | **Not supported as a general statement:** 22 conflict among 55 determined CV > 0 instances (share 0.40). It holds only for CV = 0.75 at W ≤ 0.475 (0/12); for CV = 0.35 conflict is present at every W ≤ 0.625 (2/5, 5/6, 3/6, 5/6). |
| (c) | fewer conflict instances show saving at ρ = 1 than at ρ = 5 | **Supported:** 15/46 at ρ = 1 vs 34/46 at ρ = 5 (criterion: ≥ 0.25 lower share; observed 0.33 vs 0.74). |

## 8. Implications of the independence assumption (D2 deferred)
Per your decision, the generator and the primary calibration were **not** changed: processing times are drawn independently of machine power, and CV only scales the spread of machine powers (κ-coupling is not implemented). Consequences that the final report must state:
* For CV > 0 one machine tends to be cheapest in energy *and* lowest in power (lowest-power machine is the min-energy machine for 97 % / 100 % of jobs at CV 0.35 / 0.75, the fastest for only 36–40 %; `SPEC-002-v2-proposal.md` §1). "CV" therefore means "one dominant low-power machine", not a speed–power trade-off.
* The cal2 data show that this does not remove conflict in general (22/55 at CV > 0), but conflict at CV = 0.75 appears only from W = 0.55; whether this is the dominance mechanism is **untested**.
* Conclusions about CV hold for this generator only. If real testbed machines trade speed for power, they may not transfer. A separate sensitivity experiment (`cal2b`, κ) remains an option if time permits; it is not needed to run the main study.

## 9. Boundary evidence at W = 0.90 (D3)
W = 0.90 is removed from the main experiment. Pilot27 results at W = 0.90 (9 instances, all zero saving, B peak = P peak) are kept as boundary evidence **with this caveat**: only 8.0 % of raw draws at W = 0.90 pass the FCFS-or-SPT acceptance filter (8.6 % in the independent study), while 95 % are exactly feasible; the filter rejects feasible instances preferentially (pooled over W ≥ 0.80, accepted instances have shorter longest jobs, 14.5 vs 15.7 slots, and smaller makespans, 28.6 vs 30.4 of T = 32). W = 0.90 results therefore describe a selected, atypical subpopulation near the feasibility edge, not the nominal workload population. The same filter is inert at W ≤ 0.65 and nearly so at 0.70 (§6), so cal2 results are not affected.

## 10. Recommendations for the final experiment (evidence-based; decisions are yours)
The 405-instance design (W 0.40 / 0.70 / 0.90) is superseded and has **not** been started.

1. **W levels: 0.40, 0.475, 0.55, 0.625, 0.70** (the cal2 grid). Each is generated reliably and solvable at the existing budgets for most rows (exclusions in §6), and the set covers the conflict plateau (0.40–0.625), the onset of conflict at CV = 0.75 (between 0.475 and 0.55) and the null region (0.70). A single gap remains: where the collapse lies between 0.625 and 0.70. If you want that location as a result, run a short refinement first (**`cal3`: W 0.65 and 0.675, same γ/CV/ρ, 2 seeds = 36 instances, ≈ 0.4–0.8 CPU-h ≈ 11–26 min wall**, projected from the cal2 means at 0.625 and 0.70) and then move one of the top two levels or add a sixth; otherwise it is not required. Realised W deviates from the nominal level by up to ±0.025, so main-grid levels closer than 0.05 can overlap in `w_real`; a sixth level between 0.625 and 0.70 cannot avoid this.
2. **ρ levels: keep 1, 2, 5, 14, 50.** 1–14 bracket every break-even bound; 50 only adds saving magnitude and costs 36 % of solver time and 15 of the 18 cost-unproven C rows. If runtime or exclusion bias becomes a concern, ρ = 50 is the level to drop or to treat separately; never compare CV cells at ρ = 50 without the n_valid/n_total counts.
3. **γ and CV: keep all three levels each** (conflict share is non-decreasing with γ and saving at ρ = 50 is larger for γ > 1; CV = 0 is the clean reference and CV > 0 the noisy part).
4. **Replications: 15 seeds per cell (675 instances for five W levels)** as the minimum I would defend, 20 if budget allows. Basis: our rule needs ≥ 10 per cell before any interval is shown; cal2 shows seed disagreement in 6 of 25 determined CV > 0 cells and none for CV = 0; and within-cell saving gaps up to 42 pp. cal2 **cannot size** the replication count statistically; 15 is a judgement, and if budget binds, spend replications on CV > 0 rather than on extra W levels. Projected cost (cal2 CPU means by W; high variance, estimator was ~33 % high last time): 15 seeds ≈ 9.9 CPU-h ≈ 5.0 h wall on 2 workers; 10 seeds ≈ 6.6 CPU-h ≈ 3.3 h; 20 seeds ≈ 13.2 CPU-h ≈ 6.7 h; a sixth level adds 1.4–3.1 CPU-h at 15 seeds. This fits before 1 December.
5. **Solver budgets (D4): keep.** **[Corrected 20 Nov 2026]** This item originally said unproven C incumbents were "far worse than B". That was the analysis error described in §6. The front solver now proves most of these rows without extra budget (see `docs/handoff/FRONT-AND-BILLING.md`).
6. **Fix the analysis rules before the main run:** (i) conflict indicator and prediction labels evaluated on the full curve, not endpoints; (ii) decide whether to apply the dominance rule (zero saving at every ρ when B attains the minimum peak, 8 of the 18 unproven rows here); (iii) report n_valid/n_total in every cell; (iv) intervals only with ≥ 10 seeds per cell.

## 11. Limitations
Two seeds per cell; one instance size (8 jobs × 3 machines × T = 32); P unproven in 5 instances makes the conflict indicator undetermined for them; exclusion of unproven rows is non-random (§5); B_maxpeak is unproven in 15 instances (band comparisons rest on 359 rows); Model B (real ₹/kVA/month) is not in the solver; no hardware involved; the W-collapse location and the CV mechanism are open.

## 12. Files
`results/cal2/results.csv`, `manifest.json`, `parts/`; standard analysis `results/cal2/analysis/` (tables, 8 figures, `README.txt`); calibration analysis `results/cal2/calibration/` (E1–E5 CSVs, `e5_transition_and_levels.json`, 7 figures, `README.txt`); code `07_src/analysis/calibration_report.py`, tests `tests/test_calibration_report.py`; run log `results/cal2.log`, `results/cal2.start`.

## Addendum (20 Nov 2026)
§10.1's optional `cal3` refinement (W 0.65, 0.675) is withdrawn. If W > (M−1)/M, all M machines must run together at some slot,
so no conflict is possible. For M = 3 this means W > 2/3, which covers every W = 0.70 instance here (realised W 0.677–0.708) and
W = 0.675. The four "undetermined" W = 0.70 instances are therefore provably "no conflict". The results above are unchanged. See
`docs/handoff/ROADMAP-FINAL.md` §1.4.
