# MAIN-RESULTS: SPEC-003 main study

_Status 28 Nov 2026: complete._
* **M3 (8 jobs × 3 machines, 540 instances):** complete and analysed.
* **M4 (12 × 4, 60 instances):** complete and analysed. Its run was interrupted once by this session's 2-hour background
  limit and resumed; finished instances were kept and the re-aggregated M3 data stayed byte-identical.

Sources:
* `results/main_m3/` (raw rows, manifest, digest `56e0f2f2f3455ffd`) and `results/main_m4/` (digest `e5bfe31d5230171c`);
* `results/main_analysis/{m3,m4}/` (tables), `results/main_analysis/m3_vs_m4_shared.csv`,
  `results/main_analysis/figures/` (F1–F4, M3);
* `results/main_run/` (environment record, run log, reproducibility check).

Analysis by `07_src/scripts/main_report.py --n-boot 2000`, figures by `07_src/scripts/main_figures.py`.

Reading rules (SPEC-003 §5, §7, §9):
* "Mean" = unweighted mean of γ × W × CV cell means.
* Brackets = 95 % stratified cluster-bootstrap interval (2000 replicates); it describes generator sampling only. There
  are no significance tests.
* Exact values and bounds are never pooled.
* CV = 0.75 is reported separately (D4).
* ρ_eq = 350/(D·PF) ₹ per kW per shift, e.g. ₹13.46 at D = 26, PF = 1. The headline setting is D = 26, PF = 1.
* Bills are **PARTIAL MONTHLY BILL ESTIMATES**: KERC HT-2(a) demand charge plus energy of the scheduled shift only.

## 0. Integrity of the M3 data
| Check | Result |
|---|---|
| Instances | 540/540, 0 missing; one design digest throughout |
| Platform | Linux, Python 3.13.18, OR-Tools 9.15.6755, 2 workers. The pre-run check re-solved 6 smoke instances: 6/6 identical. |
| Fronts complete (exact) | 539/540. Exception: `g2w3c2s010` (γ 7/4, W 0.625, CV 0.75), labelled upper bound and excluded from exact estimates. |
| Proven optimal | A 540, B 539, B_minpeak 531, direct C at ρ = 14 (primary stage) 532 of 540; every unproven one is counted |
| Front vs direct C at ρ = 14 (both proven) | 531/531 equal TEC (§12 trigger: none) |
| Recomputed C, guard, PCG at every grid ρ vs stored rows; regenerated FCFS/SPT/EG | 0 differences |
| C ≤ B, guard ≤ every candidate, no rule below the optimum | No violation |
| Exact-set vs all-instance estimates (§7) | Largest cell difference 0.57 points (< 1 point threshold) |
| Runtime | 11,016 CPU-s in total; per instance: median 10.3 s, p95 72.7 s, max 169 s. M3 block wall time: 1.58 h on 2 workers for the 525 instances after the resume (the first 15 ran before it). |

## 1. Q1: how often can the peak be reduced? (`q1_conflict.csv`)
| Subset | Peak below energy-only's possible | Costly trade-off (≥ 2 front points) | "Free" reduction (lower peak at equal energy cost) |
|---|---|---|---|
| CV ≤ 0.35 (n = 360) | **78.9 %** | 62.5 % | 18.1 % |
| CV = 0.75 (n = 180) | 28.3 % | 24.4 % | 4.5 % (1 undetermined) |

By workload, CV ≤ 0.35 (W 0.40 / 0.475 / 0.55 / 0.625):

| Measure | W 0.40 | W 0.475 | W 0.55 | W 0.625 |
|---|---|---|---|---|
| Peak reduction possible | 62 % | 83 % | 82 % | 88 % |
| Costly trade-off | 47 % | 67 % | 67 % | 70 % |

* By peak/off-peak price ratio γ (1 / 19/14 / 7/4), reduction is possible in 61 / 83 / 93 %.
* At γ = 1 (flat energy price) the reductions are mostly "free" (53 % of instances, out of the 61 % that can reduce),
  because timing does not change energy cost.
* By CV: CV 0 gives 98 %; CV 0.35 gives 59 %.

## 2. Q2: exact break-even demand charge vs energy-only (`q2_break_even.csv`, F2)
**CV ≤ 0.35:**
* 284 exact values and 76 "no peak reduction" (proven); 0 upper bounds.
* Exact ρ*: median **₹3.18**/kW per shift, IQR 0.46–5.75, maximum 13.68; 23 % are exactly 0.
* Peak-aware scheduling pays at KERC rates (ρ* < ₹13.46) in **79 %** of instances, which is almost every instance where a
  reduction exists.

**CV = 0.75:** 50 exact (median ₹1.10), 129 no reduction, 1 upper bound (₹16.88, the incomplete front; listed, not pooled).

## 3. Q3: saving of the peak-aware optimum C over energy-only B (`summary_estimates.csv`, F1)
**CV ≤ 0.35, n = 360, exact set.** TEC saving vs B by demand charge:

| ρ (₹/kW per shift) | 1 | 2 | 5 | 14 | 50 | ρ_eq (D 26, PF 1) |
|---|---|---|---|---|---|---|
| Mean saving | 0.25 % | 0.60 % | 2.11 % | 7.44 % | 17.00 % | **7.17 % [6.75, 7.60]** |

At ρ_eq:
* The median saving is 7.33 %; 78 % of instances save at least 1 %.
* Against the conservative reference B_minpeak the saving is 6.80 % [6.40, 7.21] (n = 359). "Free" reductions therefore
  explain little of the saving.
* By workload at ρ_eq (W 0.40 / 0.475 / 0.55 / 0.625): 7.32 / 8.61 / 7.17 / 5.56 %.
* By γ: 6.10 / 8.00 / 7.41 %. By CV: 7.49 % (CV 0) and 6.85 % (CV 0.35).

**CV = 0.75** at ρ_eq: 4.31 % [3.18, 5.51]. The median is 0: only 25 % of these instances save anything.

**Partial monthly bill at ρ_eq** (CV ≤ 0.35, n = 360; F4):

| D, PF | Renegotiated contract demand | Fixed contract demand |
|---|---|---|
| 26, 1 | **₹3,345 per month [3,158, 3,541]** (7.17 %) | **₹127 per month [74, 184]** (0.32 %) |
| 22, 1 | ₹3,524 | ₹297 |
| 30, 1 | ₹3,169 | −₹33 |
| 26, 0.9 | ₹3,846 | ₹267 |

With a **fixed contract demand, most of the saving disappears** (a §12 item, observed):
* The 0.90 × CD floor binds in every one of the 283 instances that save money.
* In 119 of those 283 the fixed-demand bill is no lower, or is higher.
* By workload, the fixed-demand saving falls from ₹427 per month (W 0.40) to −₹146 (W 0.625).

## 4. Q4: value of exact optimisation over the best simple rule (EG / PCG)
* At ρ_eq, CV ≤ 0.35: the best rule costs **6.89 % [6.45, 7.34]** more than the optimum (median 2.99 %).
* It depends strongly on job-power variability:

  | CV | Mean gap | Instances with gap ≥ 1 % |
  |---|---|---|
  | 0 | 0.93 % | 34 % |
  | 0.35 | 12.85 % | 98 % |
  | 0.75 | 21.38 % | — |

* By workload: 4.54 % (W 0.40) rising to 9.70 % (W 0.625).
* **S3 not triggered.** The best rule is within 1 % of the optimum on 33.6 % of CV ≤ 0.35 instances (and 1.1 % of
  CV = 0.75), against a 90 % threshold. Exact optimisation therefore adds value at this scale, except roughly when job
  powers are identical (CV 0).

## 5. Q5: where the saving vs FCFS comes from, at ρ_eq (complete chains only, F3)
**CV ≤ 0.35, 360 complete chains.** Total saving vs FCFS: **25.69 % [25.34, 26.03]** of FCFS TEC. It splits into:

| Step | Points of FCFS TEC |
|---|---|
| FCFS → energy rule | 14.57 |
| Energy rule → energy-only optimum | 5.12 |
| Energy-only → peak-aware optimum | 6.00 |

* By workload the total falls from 29.4 % (W 0.40) to 21.5 % (W 0.625).
* CV = 0.75 (178 chains): total 53.71 %, made up of 36.15 + 14.85 + 2.72 points. Most of that comes from moving energy
  in time, and little from the peak.

## 6. What would change the conclusions (SPEC-003 §12)
| Item | Observed? |
|---|---|
| Best rule within 1 % of C on ≥ 90 % (S3) | No (33.6 %) |
| Fixed-contract-demand bills erase most of the savings | **Yes:** ₹127 vs ₹3,345 per month; negative at high workload. Reported as a main finding. |
| Front ≠ direct C at ρ = 14 where both proven | No (531/531) |
| M3: exact-set and all-instance estimates diverge (> 1 point) | No (max 0.57) |
| M4 pattern differs from M3 at shared settings | **Yes, in the workload trend** (§7 below) |
| M4: exact-set vs all-instance (> 1 point) | **Yes, one cell** (W 0.70, CV 0.35; up to 2.42 points); stated in §7 |

## 7. M4: 12 jobs × 4 machines (generality check; never pooled with M3)
**Design and integrity:**
* γ 19/14 (KERC), W ∈ {0.40, 0.55, 0.70}, CV ∈ {0, 0.35}, 10 seeds per cell: 60 instances, 0 missing.
* **Fronts complete: 55/60 (91.7 %).** This is at or above the 90 % pre-registered bar, so exact M4 statements are allowed.
  The 5 incomplete fronts are all in the cell W 0.70, CV 0.35.
* Proven: B 60/60, B_minpeak 56/60.
* Front vs direct C at ρ = 14 (both proven): 44/44 equal.
* Recomputed values vs stored rows: 0 differences.
* CPU per instance: median 32 s, p95 247 s, max 464 s.

**Results at ρ_eq (D 26, PF 1):**

| Question | Result |
|---|---|
| Peak reduction possible | 95 % of instances; costly trade-off 95 % |
| Exact break-even | 52 exact, median ₹2.87/kW per shift (IQR 1.35–5.31, max 6.00). 5 upper bounds (2.59–7.00; listed, not pooled); 3 no-reduction. Pays at KERC rates in 57 of 60 (95 %): all 52 exact values and all 5 upper bounds are below ₹13.46. |
| Saving vs energy-only B (exact set, n = 55) | **9.29 % [8.24, 10.24]**. By W 0.40 / 0.55 / 0.70: 15.19 / 7.26 / 5.42 %. By CV 0 / 0.35: 7.34 / 11.24 %. Against B_minpeak: 8.82 %. |
| Partial monthly bill (n = 55) | Renegotiated contract demand **₹5,491 per month [4,906, 6,060]**; fixed **₹242 [93, 389]**. At W 0.40 the fixed-demand saving is −₹355. |
| Value of exact optimisation | 8.03 % [7.05, 9.04] over the best rule: CV 0 gives 1.05 %, CV 0.35 gives 15.01 %. S3 not triggered (best rule within 1 % on 30.9 %). |
| FCFS → C | 26.02 % of FCFS TEC (55 complete chains) |

**Exact set vs all instances (§7): a material difference, stated.**
* In the cell W 0.70, CV 0.35 the exact-set mean saving uses only 5 of 10 instances: 6.94 % at ρ_eq.
* The achieved saving over all 10 (a lower bound on the optimal saving) is 5.66 %, a difference of 1.28 points. At ρ = 50
  the difference reaches 2.42 points.
* At ρ = 14 the cell's true mean lies between 5.92 % (achieved) and 7.50 % (bound-based upper limit).
* The exact-set value for that cell is therefore likely **optimistic**. The block-level estimate at ρ_eq with all 60
  instances, as achieved savings, is 9.08 % [8.05, 10.01], against 9.29 % for the exact set.

**M4 vs M3 at the shared settings** (γ 19/14, W 0.40 and 0.55, CV 0 and 0.35; descriptive; `m3_vs_m4_shared.csv`):

| Block | W 0.40 | W 0.55 |
|---|---|---|
| M3 | 8.06 % | 8.38 % |
| M4 | **15.19 %** | 7.26 % |

* M3's saving is flat across the two workloads; M4's is twice as high at the low workload.
* By cell at ρ_eq:
  * W 0.40, CV 0: M3 9.92 %, M4 13.24 %;
  * W 0.40, CV 0.35: M3 6.20 %, M4 17.15 %;
  * W 0.55, CV 0: M3 6.83 %, M4 4.89 %;
  * W 0.55, CV 0.35: M3 9.92 %, M4 9.64 %.
* So the **pattern differs** (a §12 item). With four machines at low workload there are more ways to avoid running machines
  together. This explanation is plausible but **not tested**.
* With 10–15 instances per cell this is a descriptive contrast, not an estimate of a size effect. The direction of the
  main findings is the same in both blocks:
  * reductions are common and cheap;
  * savings hinge on renegotiating contract demand;
  * rules suffice mainly at CV 0.

## 8. Plain-language summary
* For an 8-job, 3-machine shift under KERC prices, a lower peak than the energy-only schedule is possible in about 4 of
  5 instances, unless job powers vary a lot.
* In nearly all of those, cutting the peak already pays at the KERC demand charge. The exact break-even is typically
  ₹3 per kW per shift, a quarter of KERC's ₹13.46.
* The shift cost falls by about 7 %, worth roughly ₹3,300 per month on the partial bill, **but only if the plant
  renegotiates its contract demand**. With a fixed contract, KERC's 90 % billing floor removes most of the saving, and at
  high workload it can turn into a loss.
* Simple energy-aware rules capture most of the benefit only when all jobs draw the same power. Otherwise the exact
  optimiser is on average 13 % (CV 0.35) to 21 % (CV 0.75) cheaper.
* The larger shop (12 jobs × 4 machines) shows the same picture, with bigger savings at low workload: 9.3 % of shift
  cost, about ₹5,500 per month if contract demand is renegotiated, and about ₹240 if it is not.

## 9. Limits
* Synthetic instances from the documented generator; no plant data; no physical measurement (hardware not built).
* Bills are partial and assume the same schedule every shift-day.
* Results are for 8 × 3 and 12 × 4, 32 slots of 15 minutes, and the 1-CP-SAT-worker budgets of SPEC-003. At 12 × 4 the
  hardest cell (W 0.70, CV 0.35) already leaves half the fronts incomplete, so larger shops will need bounds, not exact
  fronts.
* Proof status can depend on platform: a Windows run of the same smoke instances found equally optimal but different
  schedules and lost one proof. All results here come from one Linux machine.
