# P1: Energy–peak front, safety guard, optimality gaps and monthly billing — implementation and Gate 1

_20 Nov 2026. Branch `phase3-experiments`. Model V1.0 (`07_src/model/formulation.py`) and
`04_mathematical_model/verification/*` are unchanged (zero diff). Raw results in `results/pilot27` and `results/cal2` are unchanged
(sha256 prefixes `516ee522cd874edf` / `857b9f1c1ef4b912`)._

## 1. What was built
| Piece | File | What it does |
|---|---|---|
| Solver extension | `07_src/model/solver.py` | Three optional arguments to `run_lexicographic`, with defaults identical to before. (1) `extra_bounds`: exact integer bounds in every stage (used for `pmax ≤ cap`). (2) `initial_hint`: warm start. (3) Per-stage `stage_bounds`: CP-SAT best bound, for gaps. |
| Front solver | `07_src/model/front.py` | ε-constraint over the peak. Solve min EC, then repeatedly min EC subject to peak ≤ (last peak − 1 W). The number of points is discovered by the loop; nothing is hard-coded. Termination is proven by P (min peak), by an infeasible cap, or by the **structural peak bound** (§3). |
| Derived quantities | `front.py` | `best_for_rho` (C at any ρ), `break_even` (labelled `exact` / `upper_bound` / `no_peak_reduction` / `undetermined`), `rho_intervals` (supported and unsupported points), `tec_lower_bound` (valid lower bound on min TEC from proven or CP-SAT bounds). |
| Safety guard | `front.recommend` | Re-evaluates every candidate (front points plus any extras such as B or simple rules) with the independent evaluator. Returns the cheapest feasible one, so TEC is never above any candidate's, including B's. Also returns the lower bound, the gap, and `proven_optimal` only when the front is complete and TEC equals the bound. |
| Monthly billing (Model B, post-hoc) | `07_src/model/billing.py` | Partial monthly bill = days × EC(shift) + ₹350/kVA × BD, with BD = max(MD, 0.90 × CD) and MD = peak/PF. Scenarios: `renegotiated` (CD = own MD) and `fixed` (CD = reference MD). Every result carries the `PARTIAL MONTHLY BILL ESTIMATE …` label listing what is excluded. ρ_eq = 350/(days × PF) applies to the renegotiated scenario only. |
| Validation | `07_src/scripts/validate_front.py` → `results/front_validation/` | Gate 1 against all 90 cal2 instances (regenerated and identity-checked; cal2 files only read). |

**Exact vs upper bound.**
* **Exact:** a break-even is `exact` only if the front is complete, meaning every EC stage was proven and termination was proven.
* **Upper bound:** a break-even computed from an incomplete front uses real schedules, so it is labelled `upper_bound` (the true
  value can only be lower).
* **cal2's columns:** `rho_star_ub_*` remain what they always were, upper bounds from the pair (B or B_minpeak) vs P.

**ρ = 0 limitation (documented, tested).** Total cost from the front is exact at every ρ, and makespan is exact for ρ > 0. At
ρ = 0 exactly, the true optimum may break the energy tie with a higher-peak, shorter-makespan schedule that is dominated on
(EC, peak). `recommend` with B as a candidate restores the exact answer. All study ρ levels are ≥ ₹1.

## 2. Tests (all pass: 617 in total, previously 359)
* **`tests/test_front.py`:**
  * **Exhaustive-oracle agreement on 120 seeded instances,** which include release times, due dates, job-dependent power and
    infeasible cases. The front's points (peak, EC, makespan) match the true nondominated set; C at 5 ρ values matches; the exact
    break-even vs B matches the oracle; the lower bound equals the true minimum TEC; the gap is 0.
  * **Structural bound:** never exceeds the true minimum peak on 120 enumerated instances, and equals the maximum peak on every
    cal2 instance with realised W > 2/3.
  * **Benchmark:** front {37, 27} kW and exact ρ* = ₹12.70.
  * **Exactness labels:** degraded solves are labelled `upper_bound` or `undetermined`, never `exact`.
  * **Safety guard:** chooses B over a bad front point and rejects an infeasible candidate.
  * **Solver extensions:** infeasible caps, hints that do not change the optimum, per-stage bounds.
* **`tests/test_billing.py`:** hand-checked examples, including the 47 → 32 kVA floor case, PF conversion, and input validation.

## 3. Gate 1 results (`results/front_validation/summary.json`)
| Criterion (ROADMAP §7.6) | Result |
|---|---|
| Regenerated instances identical to cal2 | 90/90 |
| Fronts complete (exact) | **90/90** |
| Front min EC = cal2 B EC (both proven) | 90/90; front top peak ≤ B peak in 90/90 |
| Front min-peak point = cal2 P (both proven) | 85/85 |
| Front-derived C vs direct C, **TEC** (C cost stage proven) | **432/432 equal** |
| Front-derived C vs direct C, **makespan** (C fully proven) | **381/381 equal** |
| Sign of saving vs B agrees with exact break-even | 432/432 |
| The 18 direct-C rows excluded as cost-unproven in cal2 | all 18 now proven optimal; their stored incumbents had exactly the optimal TEC |
| Exact break-even ≤ cal2 upper bound | 46/46 vs B (equal in 43; lower in 3: 0 vs 0.87, 3.15 vs 4.98, 10.80 vs 11.48), 45/45 vs B_minpeak |
| Solver time | front 467 s total vs 3227 s for direct C at 5 ρ (3861 s incl. P); median per instance 2.3 s vs 20.8 s (ratio 0.16); max 62 s |
| Abandon criterion (> 10 % cap solves unproven where direct C proven) | 1/40 = 2.5 %, not triggered |
| **Decision** | **PROCEED** (all criteria met; no problems logged) |

* **Points per front:** 1 point in 52 instances, 2 in 28, 3 in 8, 4 in 2.
* **Termination:** structural bound in 84 instances, P bound in 6.
* **Dominated points:** 0.

**Run history (nothing discarded).**
* The first run (`results/front_validation/run1_superseded_summary.json`) had 88/90 complete fronts. The two incomplete ones were
  W = 0.70 instances where proving "no schedule below 47 kW" timed out.
* The structural bound turns the workload theorem into a certificate: total minimum work beyond (k−1)·H forces k machines to run
  together. It was added, tested against the oracle, and the validation was re-run from scratch. Every number above is from the
  second run.

**What changes in the cal2 picture (descriptive, n = 2 per cell).**
* Every instance is now classified; none is undetermined.
* Instances with a possible peak reduction ("conflict") by W:

  | W | Conflict |
  |---|---|
  | 0.40 | 9/18 |
  | 0.475 | 11/18 |
  | 0.55 | 13/18 |
  | 0.625 | 14/18 |
  | 0.70 | 0/18 |

  That is 47 conflict and 43 none; cal2 reported 46 / 39 / 5 undetermined. The one newly resolved conflict is `g1w0c1s000`.
* Exact break-even vs B over the 47 conflict instances: median ₹2.28/kW, quartiles 0.56 and 5.08, maximum ₹10.80.
* Under the renegotiated-CD assumptions, ρ_eq = ₹13.46/kW at 26 days and ₹11.67/kW at 30 days (PF = 1). Both are above every
  exact break-even.

## 4. Correction of an earlier claim
CAL2-RESULTS §6 and §10.5, ROADMAP-FINAL §1.3 and OVERNIGHT-STATUS said that the 18 cost-unproven C incumbents were
"40–185 % worse than B". **That was my analysis error:** C's TEC at ρ (energy plus demand charge) was compared with B's TEC at
ρ = 0 (energy only). At the same ρ, 0 of the 18 is worse than B, and all 18 equal the exact optimum. The documents are corrected
in place, with "[Corrected 20 Nov 2026]" notes.

## 5. Billing on the benchmark (`tests/test_billing.py`, 26 days, PF = 1)
| Scenario | Energy-only B (785.60 ₹/shift, 37 kW) | Peak-aware C (912.60 ₹/shift, 27 kW) | Monthly saving of C |
|---|---|---|---|
| CD renegotiated (BD = MD) | ₹33,375.60 | ₹33,177.60 | **+₹198** |
| CD fixed at 37 kVA (BD floor 33.3 kVA) | ₹33,375.60 | ₹35,382.60 | **−₹2,007** |

All figures are partial bill estimates; the label lists the exclusions. With contract demand fixed at the old peak, peak-aware
scheduling *loses* money on the benchmark. The main study will report both scenarios.

## 6. Unresolved
* Push to GitHub is blocked (this session has no GitHub authorisation). The branch exists locally, and a git bundle is provided.
* The front is validated at 8 × 3 × 32 only. Larger sizes are P3's job (scaling probe).
* Runner integration (front columns, bound/gap, dropping B_maxpeak) is part of P4.
