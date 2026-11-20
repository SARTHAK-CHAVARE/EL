# SPEC-003 — Main study (pre-registered; frozen before any main-study run)

_Version `SPEC-003/v1`, 20 Nov 2026, branch `phase3-experiments`._

**Design digests, pinned in `tests/test_main_design.py`:**

| Design | Digest | Instances |
|---|---|---|
| `main-m3-v1` | `56e0f2f2f3455ffd` | 540 |
| `main-m4-v1` | `e5bfe31d5230171c` | 60 |
| `main-m3-smoke` | `8788174bf9477c21` | 36 |
| `main-m4-smoke` | `c4002ac66cfdb832` | 12 |

**Freeze rule:**
* No factor level, budget, strategy or analysis rule below may change after the smoke run is approved.
* A change requires a new version string, which gives a new digest and a new output directory. The runner refuses to mix digests.
* Analysis choices not written here are labelled "post hoc" wherever they are reported.

## 1. Questions (estimation, not significance testing)
Peak-aware C can never cost more than the energy-only optimum B (B is feasible for C's problem), so "is C better than B?" is not
tested. The study **estimates**:

* **Q1:** how often a peak reduction is possible ("conflict"), by W, γ, CV and M;
* **Q2:** the distribution of the **exact** break-even demand charge;
* **Q3:** the saving of C over B (and B_minpeak) at ρ ∈ {1, 2, 5, 14, 50} ₹/kW per shift and at the KERC-equivalent ρ_eq, plus the
  partial monthly bill under fixed and renegotiated contract demand;
* **Q4:** the value of exact optimisation over the best simple rule (EG / PCG);
* **Q5:** the decomposition of the saving vs FCFS (FCFS → EG → B → C);
* **Q6:** computation: proof rates, optimality gaps, runtime.

## 2. Designs and why these levels
### Primary block M3: `main-m3-v1`, 540 instances
**Fixed settings (same as pilot / cal2):**
* 8 jobs × 3 machines;
* T = 32 slots of 15 min (16:00–24:00: normal 16–18, peak 18–22, off-peak 22–24);
* mean machine power 15 kW, base load 2 kW;
* processing-time multipliers U(0.7, 1.3).

| Factor | Levels | Reason |
|---|---|---|
| W (nominal) | 0.40, 0.475, 0.55, 0.625 | All lie inside the only band where a peak reduction is possible for M = 3: above 1/3 (two machines must overlap) and below 2/3 (§3). cal2: 9–14 of 18 instances per level had a possible reduction. W ≥ 2/3 is provably null and is **covered by the theorem, not run**; the evidence is cal2's 18/18 W = 0.70 instances. W = 0.25 is not in this spec; it can only be added later as a separate, labelled supplementary design. |
| γ (peak/off-peak) | 1, 19/14, 7/4 | 1 = KERC Jul–Nov (no ToD adjustment). 19/14 = KERC Dec–Jun (₹7.60 / ₹5.60). 7/4 = synthetic stress. |
| CV of machine power | 0, 0.35, 0.75 | 0 = identical machines (15/15/15 kW). 0.35 = moderate (8.57/15/21.43 kW). **0.75 = stress test** (1.22/15/28.78 kW, ≈ 24 : 1, processing times independent of power). Per D4, CV = 0.75 is reported separately and is never pooled into conclusions drawn from CV ≤ 0.35. |
| Seeds per cell | 15 | Intervals need ≥ 10 seeds per cell (§9). cal2 showed seed disagreement in CV > 0 cells. |

### Conditional block M4: `main-m4-v1`, 60 instances (Gate 2: 12 × 4)
| Factor | Levels | Reason |
|---|---|---|
| Size | 12 jobs × 4 machines, same shift and powers | Largest size passing Gate 2 (93.3 % of required front solves proven; narrow pass) |
| γ | 19/14 | The KERC Dec–Jun ratio, which keeps the block small |
| W | 0.40, 0.55, 0.70 | All below the M = 4 threshold 3/4. 0.70 is **above** the M = 3 threshold, which tests that the null region moves with M as the theorem predicts. 0.40 and 0.55 match M3 levels. |
| CV | 0, 0.35 | CV = 0.75 is excluded: at larger sizes even CV = 0.35 produced all of P3's unproven solves |
| Seeds per cell | 10 | Minimum for intervals |

### Common settings
* **ρ grid:** {1, 2, 5, 14, 50} ₹/kW per shift, plus ρ_eq = 350/(D·PF) for D ∈ {22, 26, 30} and PF ∈ {1, 0.9}. All are evaluated
  from the front with no extra solves.
* **Budgets (as in cal2):** stage 1 60 deterministic s (180 s wall cap); tie-break stages 15 deterministic s (60 s wall cap); 1
  CP-SAT worker; random seed 0.
* **Seeds:** main base seed 20261123 and smoke 20261122, both distinct from pilot (20261115), cal2 (20261116) and probe
  (20261121). No instance used to choose this design is reused in it.

## 3. Structural workload theorem (implemented: `model.front.structural_peak_lower_bound`; tested against the exhaustive oracle)
**Setup.**
* All operations lie in a window of H slots; job j occupies at least min_m p_jm of them.
* So the machines are busy for at least W_min = Σ_j min_m p_jm machine-slots.

**Theorem.**
* If at most k − 1 machines were busy in every slot, only (k − 1)·H machine-slots would exist.
* Hence with **k = ⌈W_min / H⌉**, some slot has at least k busy machines.
* Each busy machine m draws at least min_j power_jm, so **peak ≥ base + (sum of the k smallest per-machine minimum powers)**.

**Corollary.** With W = W_min / (M·H): if **W > (M−1)/M**, then k = M. Every schedule then has the maximum peak, no peak
reduction is possible, and C = B at every ρ.

| Block | Threshold (M−1)/M | Nominal W → forced overlap k = ⌈W·M⌉ | Consequence |
|---|---|---|---|
| M3 | 2/3 | 0.40 → 2; 0.475 → 2; 0.55 → 2; 0.625 → 2; (0.70 → 3) | All run levels allow a reduction; W ≥ 2/3 provably none |
| M4 | 3/4 | 0.40 → 2; 0.55 → 3; 0.70 → 3 | All run levels below 3/4 |

k is computed from realised work, so realised W is reported for every instance. The bound also certifies termination of the
front (P3: it terminated 84 of 90 cal2 fronts).

## 4. Strategy protocol (`runner.run_task_main`; every row stored, nothing dropped)
| Row `strategy` | ρ | What |
|---|---|---|
| A | 0 | min makespan, then min Σ completion |
| B | 0 | min EC, then min makespan: the energy-only counterfactual |
| B_minpeak | 0 | min EC, min makespan, min peak: the conservative energy-only reference. **No B_maxpeak.** |
| FRONT_top / FRONT_cap / P | 0 | Every ε-constraint solve (top; caps at 1 W below the last peak; P only when needed). Columns: `cap_w`, `required_proven`. |
| FRONT_PT | 0 | Every nondominated point: peak, EC, makespan, `ec_proven`, `peak_proven`, `makespan_proven` |
| C | 14 only | Direct C solve: the independent cross-check of the front (D1) |
| C_front | each grid ρ | C read off the front. TEC exact iff the front is complete; status OPTIMAL only if the front is complete **and** the makespan tie-break is proven; else FEASIBLE. Columns: `tec_lower_bound`, `gap`. |
| FCFS, SPT, EG | 0 | Rules; NO_SCHEDULE if a rule fails (never "infeasible") |
| PCG | each grid ρ | Peak-capped greedy, best cap at that ρ (`rule_cap_w`) |
| GUARD | each grid ρ | Cheapest independently re-evaluated feasible schedule among front points, B, B_minpeak, A, EG, PCG, FCFS, SPT (and direct C at 14). OPTIMAL only if the front is complete and TEC = lower bound. Columns: `choice`, `gap`. |
| BE_B, BE_B_minpeak | 0 | Break-even vs B and vs B_minpeak (§5) |

Every row carries `design_digest`, realised W, generation attempts, the structural bound, and task wall and CPU time.

## 5. Break-even: exact values vs upper bounds
* **Definition.** ρ*(ref) = the smallest ρ at which some schedule has lower TEC than a fixed reference schedule (B or B_minpeak):
  ρ* = min over front points p with peak_p < peak_ref of max(0, EC_p − EC_ref) / (peak_ref − peak_p), in exact rational ₹/kW.
* **Labels:**

  | Label | Meaning |
  |---|---|
  | `exact` | Front complete |
  | `upper_bound` | Front incomplete; computed from real schedules, so the true ρ* can only be lower |
  | `no_peak_reduction` | Complete front, no point below the reference peak |
  | `undetermined` | Incomplete front, no such point |

* **Reporting.** Exact values and upper bounds are **never pooled**. Distributions are reported over `exact` plus
  `no_peak_reduction` instances, with the count and values of `upper_bound` instances listed beside them.
* cal2's `rho_star_ub_*` columns remain labelled upper bounds and are not mixed with SPEC-003 values.

## 6. Dominance rules (pre-registered; every use counted and labelled "by dominance")
1. **C ≤ B by construction.** Saving < 0 can only indicate a bug, and the run stops if it occurs.
2. **No-reduction instances.** If the front is complete with no point below B's peak (`no_peak_reduction`), or the top peak equals
   the structural bound, then the saving of C over B is exactly 0 at every ρ, whatever the status of any direct solve.
3. **Theorem.** Realised W > (M−1)/M implies rule 2. No such instance is planned; one arising from rounding would be reported.
4. **Guard.** The guard's TEC is ≤ every candidate's (re-evaluated). Any violation stops the run.
5. **No other inference.** An unproven value is never replaced by an implied value except via rules 2 and 3.

## 7. Front completeness and optimality gaps
* **Per instance:** front complete (yes/no), termination reason, number of solves, required-solve proof share, number of points.
* **Per (instance, ρ):** C_front status, TEC lower bound LB (a valid bound over all schedules; §P1) and gap = (TEC_guard − LB)/TEC_guard.
* **Primary estimates use the exact set** (complete fronts). As a pre-registered sensitivity analysis, all instances are reported
  with:
  * the achieved saving of the guard schedule, a lower bound on the optimal saving;
  * the bound-based upper bound (B − LB)/B.

  If the two analyses differ materially (any cell mean differs by > 1 percentage point), this is stated.
* **Proof shares are reported by block × W × CV.** If fewer than 90 % of M4 fronts are complete (Gate 2 was marginal), M4 results
  are reported as bounds and the statement "M4 exact results" is not made.

## 8. Rule-versus-optimiser comparisons
* **Rules:**
  * EG: each job, largest first, in its cheapest feasible window;
  * PCG: EG under each machine-subset power cap, best at the given ρ.
* **Value of exact optimisation** = (best rule − C) / best rule, with best rule = min(EG, PCG).
* **S3 (pre-stated):** if the best rule is within 1 % of C on ≥ 90 % of instances at ρ_eq (D = 26, PF = 1), the report states
  that exact optimisation adds little at this scale.
* **Decomposition vs FCFS:** FCFS → EG → B → C, in points of FCFS TEC, on **complete chains only** (FCFS and EG both succeeded).
  The number of complete chains is always stated.

## 9. Paired methodology and statistics
* **Pairing.** Every strategy and every ρ are evaluated on the same instance. ρ is a within-instance factor; all comparisons are
  per-instance differences.
* **Estimand.**
  * For a group of cells: the unweighted mean of cell means (each γ × W × CV cell weighs equally).
  * Also reported: medians, quartiles, and the share of instances with saving ≥ 1 %.
* **Intervals.**
  * Method: stratified cluster bootstrap (`analysis.tables.stratified_cluster_bootstrap`). Instances are resampled with
    replacement within their generation cell; 2000 replicates; 95 % percentile intervals; fixed bootstrap seed.
  * Intervals are produced **only where every contributing cell has ≥ 10 seeds** (`MIN_SEEDS_FOR_INTERVALS`); both blocks qualify.
  * Otherwise the output is labelled descriptive.
* **No significance tests:** no p-values, and none for C vs B (true by construction). Intervals describe sampling uncertainty over
  generator instances only. Generalisation beyond the generator is not claimed.
* **Blocks are analysed separately and never pooled.**
  * M3 answers Q1–Q6 for 8 × 3.
  * M4 is a generality check (different M, W levels and threshold). It is compared with M3 only at the shared settings (γ 19/14;
    W 0.40 and 0.55; CV 0 and 0.35), as a side-by-side description.
  * CV = 0.75 is reported separately within M3 (D4).

## 10. Exclusions and missing results (all counted, none silent)
* **Expected rows per instance:**
  * A, B, B_minpeak, FCFS, SPT, EG, BE_B, BE_B_minpeak;
  * FRONT_top plus every FRONT_cap / P solve and every FRONT_PT point;
  * C@14;
  * C_front, PCG and GUARD × 5 ρ.
* **Missing instances.** The aggregator works from the expected task list. A missing instance is reported per cell; the main run is
  "complete" only with 0 missing.
* **Reasons per estimand** (each with a count): `missing`, `unproven` (front incomplete or a required stage unproven),
  `no_schedule` (rule failed), `by_dominance` (§6).
* **Generation.** Attempts per instance are reported; the acceptance filter is inert in this W range (cal2: 89/90 first draws).
* **Guarantees.** A FEASIBLE result is never reported as OPTIMAL, and an unproven result is never silently replaced or dropped.

## 11. Billing outputs (Model B, post-hoc; `model/billing.py`)
* Partial monthly bill: D · EC_shift + ₹350/kVA · BD, with BD = max(MD/PF, 0.90 · CD).
* Scenarios:
  * renegotiated (CD = own MD);
  * fixed (CD = the energy-only schedule's MD).
* D ∈ {22, 26, 30}; PF ∈ {1, 0.9}.
* Every value carries the "PARTIAL MONTHLY BILL ESTIMATE" label and its list of exclusions. Both scenarios are always shown
  together.

## 12. What would change the conclusions (to be reported if observed)
* Best rule within 1 % of C on ≥ 90 % of instances (S3).
* Fixed-contract-demand bills erase most of the savings.
* Front ≠ direct C at ρ = 14 where both are proven (stop and investigate).
* M4 shows a different pattern than M3 at the shared settings.
* Exact-set and all-instance estimates diverge (§7).

## 13. Execution, runtime and stop rules
* **Commands** (separate directories; resumable; digests checked):
  ```
  python 07_src/scripts/run_experiment.py --design main-m3 --out results/main_m3 --workers 2
  python 07_src/scripts/run_experiment.py --design main-m4 --out results/main_m4 --workers 2
  ```
* **Runtime.** Projected from the smoke run (`docs/handoff/P4-SMOKE-RESULTS.md`). If the run exceeds 1.5× the projection, it is
  paused and reported. It is never shortened by changing the design.
* **Gate 4.** No main run before you approve the smoke results.
