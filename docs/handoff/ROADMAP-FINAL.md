# EL – Tariff Opti: Engineering Roadmap to a Working, Defensible System (20 Nov → 7 Dec 2026)

_Written 20 Nov 2026 from the repository, the code, and the pilot27 / cal2 outputs. Every number below comes from a file in this repo
(source given). Unknowns are marked **UNKNOWN**. Nothing has been committed or pushed._

## 0. The answer in plain language

* **We already have a working model.** The "model" in this project is the optimisation model plus its solver: you give it jobs,
  machines and the KERC tariff, and it returns a provably optimal production schedule. It is implemented, tested (359 tests), checked
  against a brute-force oracle (720/720) and reproduces the hand-verified benchmark exactly. It is not a stub.
* **It should not become a machine-learning project.** There is nothing to learn: the tariff is published, the job list is an input,
  and we have no real plant data. An ML model would only learn our own random instance generator. The project's own master context
  says the same ("Do not describe the project as… an AI/deep-learning project"; ML is on the PROJECT_STATUS "Do Not Start Yet" list).
* **What is actually missing is not more mathematics.** It is (1) a tool a person can use, (2) the right comparisons to prove the
  optimiser is worth it, (3) a translation into a real monthly KERC bill, and (4) the main experiment. Physical validation is a
  conditional fifth item.
* **Three findings from our own data change the plan** (§1.4): savings against FCFS are mostly *not* due to peak-awareness; the
  W = 0.70 "collapse" is a mathematical certainty, not an experimental discovery; and with 3 machines the peak can only take 2–3
  values, which limits how far the results generalise.
* **First thing to build:** an energy-vs-peak "front" solver (§7.4). It gives the best schedule for *every* demand charge at once,
  the *exact* break-even (we currently only have an upper bound), and it is exactly what the demo needs.

---

## 1. Current state (evidence-based)

### 1.1 What exists and has been tested
| Component | Where | Evidence |
|---|---|---|
| Model V1.0: unrelated parallel machines, time-indexed CP-SAT, exact peak, sequential lexicographic objectives | `07_src/model/` | oracle 720/720 (`tests/run_oracle_report.py`), benchmark 13/13 (`07_src/scripts/reproduce_benchmark.py`: ₹785.60 / ₹912.60 / 27 kW / ρ* = ₹12.70), 359 tests |
| Strategies A (makespan), B (energy-only), B_minpeak, B_maxpeak, P (min-peak), C (EC + ρ·peak), FCFS, SPT | `model/solver.py`, `experiments/baselines.py` | as above |
| Instance generator (γ, W, CV), versioned designs, resumable runner with digests | `07_src/experiments/` | `tests/test_experiments.py`, `test_calibration_design.py` |
| Analysis: validity flags, break-even upper bound, stratified cluster bootstrap, calibration report | `07_src/analysis/` | `tests/test_analysis.py`, `test_calibration_report.py` |
| Pilot (27 instances) and calibration `cal2-v1` (90 instances, 1080 rows, 0 missing) | `results/pilot27`, `results/cal2` | `PILOT-RESULTS.md`, `CAL2-RESULTS.md` |

### 1.2 Researched or proposed, but **not implemented**
* ε-constraint / AUGMECON Pareto workflow: selected in `05_planning/master_execution_plan.md` Part 5, never coded.
* Model B (₹350/kVA/month on billing demand): documented in `03_tariff/tariff_reference.md`, not in any code.
* Experiments H (scalability), I and J (physical model fidelity and validation), and the Raspberry Pi edge run (RQ6, RQ7).
* Hardware: specified in `09_hardware/current_hardware_spec.md`, **not purchased** (per your earlier statement).
* The main factorial study: designed and calibrated, not run.

### 1.3 Missing for a usable system
* **No entry point for a user.** No command takes a new instance and returns a schedule. Only the benchmark script and the
  batch runner exist.
* **No schedule output a person or the ESP32 can use.** There is no Gantt chart, no power-vs-time plot and no schedule export.
* **No monthly-bill view.** Results exist only in normalised ρ (₹/kW per 8-hour shift).
* **No safety guard.** Nothing guarantees that a returned schedule is never more expensive than the energy-only schedule B when a solve is unproven. **[Corrected 20 Nov 2026]** This bullet originally claimed that the 18 cost-unproven C runs in cal2 returned schedules "40–185 % more expensive" than B. That was an analysis error: C's cost at ρ was compared with B's cost at ρ = 0. At the same ρ, none of them was worse than B, and the front later proved all 18 optimal (`docs/handoff/FRONT-AND-BILLING.md`). The guard is still required as a design property.
* **Reproducibility gaps.** The 141 Phase 3 files exist only as untracked files (and in your zip). `requirements.txt` has
  `ortools>=9.10` unpinned, while results were produced with 9.15.6755.
* **Documentation credibility.** README.md schedules hardware assembly for Jan 2027 and the final report for Feb 2027, both after the
  7 Dec deadline. It also describes the testbed in the present tense: "±0.1 %" accuracy, "100 Hz telemetry", and a 12 V supply in an
  enclosed chassis. None of this is built. An examiner who asks to see it will find a mismatch.

### 1.4 Weak assumptions and methodological problems found in our own data
1. **The central research question asks for something that is true by construction.** It asks when peak-aware scheduling gives a
   "statistically significant economic benefit" over energy-only scheduling. But B's schedule is a feasible solution of C's problem,
   so the optimal C cost can never be above B's. A significance test of "C better than B" is therefore meaningless. The defensible questions are **how much, how
   often (≥ 1 % saving), and under which conditions**: estimation, not testing.
2. **FCFS is a strawman baseline.** Moving from FCFS to the energy-only optimum B already cuts energy cost by 25.5 % on average even
   at γ = 1 (no time-of-day price difference at all). By CV, the same energy-cost saving averages 16.6 / 30.0 / 49.9 % (CV 0 / 0.35 / 0.75; cal2,
   computed from `results/cal2/results.csv`). That saving comes from *machine assignment* (FCFS picks the earliest-finishing
   machine, ignoring power), not from tariff or peak awareness. Against FCFS, C saves 32–36 % of total cost (mean, ρ = 1 → 50).
   The peak-aware step alone (C vs B) is worth only 0.2–13.3 % of B's cost over the same range. Headlining "30 % saving vs FCFS" would be misleading. We need an
   *energy-aware simple rule* as the honest "simple alternative".
3. **The W = 0.70 collapse is a theorem, not a finding.** If W > (M−1)/M, the work cannot fit on M−1 machines. Since
   W = Σ min p / (M·T), at some slot all M machines must run together, so the minimum possible peak equals the maximum peak and no
   conflict can exist. For M = 3 the threshold is 2/3. All 18 W = 0.70 instances have realised W between 0.677 and 0.708, above 2/3.
   Consequences:
   * the 4 "undetermined" W = 0.70 instances in cal2 are provably "no conflict";
   * the `cal3` refinement I proposed (W 0.65, 0.675) is largely unnecessary, because 0.675 is provably null (**I withdraw that
     recommendation**);
   * all cal2 conflict sits in one structural band, with W between 1/3 and 2/3.
4. **With 3 machines the peak is coarse.** Peak = 2 kW base + the powers of the machines running together, so only a few levels
   exist. Across all cal2 schedules only 47, 32 and 25.57 or 18.22 kW occur. FCFS always peaks at 47 kW (89/89). A "peak reduction"
   is essentially "never run all three machines together" (47 → 32 kW = −31.9 %, the median reduction at ρ = 14). Conclusions at
   M = 3 may not hold for larger shops; this is untested.
5. **CV = 0.75 creates an implausible machine.** Machine powers are 1.22 / 15 / 28.78 kW (≈ 24 : 1), with processing times drawn
   independently of power. So the 1.2 kW machine is on average as fast as the 28.8 kW one, and B concentrates work on it. CV = 0.35 gives
   8.57 / 15 / 21.43 kW. This is the deferred D2 issue in its most extreme form.
6. **The real tariff can wipe out much of the saving.** KERC bills demand on BD = max(MD, 0.90 × CD). Suppose contract demand stays
   at today's peak (CD = 47 kVA): cutting MD to 32 kVA lowers billed demand only to 42.3 kVA. That is 4.7 of the 15 kVA reduction
   (31 %) until the contract demand is renegotiated. Other unaddressed factors:
   * kW vs kVA needs a power-factor assumption;
   * the MD metering interval relative to our 15-minute slots is **UNKNOWN**;
   * ToD is optional below 500 kVA contract demand, while our instances peak around 47 kW;
   * whether a plant of this size is billed under HT-2(a) at all is **UNKNOWN** (to be checked in the tariff order).
7. **Exclusions are not random.** Unproven rows concentrate at ρ = 50 and CV = 0.35, so cell means at high ρ are biased (CAL2 §5).
8. **Design choices were tuned on cal2.** The main study must use fresh seeds and analysis rules frozen in advance. This is the
   optimisation analogue of not testing on your training data.
9. **Synthetic data only.** No real plant data exists in the repo. External validity rests on the generator, plus physical evidence
   if the rig is built.

### 1.5 Is the direction still right?
Yes for the core: exact optimisation of a published tariff, plus a controlled experiment, is the correct method for this problem.
Four corrections are needed:
* reframe the research question as estimation;
* add honest baselines;
* add a real-bill layer;
* turn the solver into a usable tool.

None of these requires redesigning the model. The model itself (V1.0) should **not** be touched again.

---

## 2. The actual objective

**System to build:** a decision-support scheduler for a small multi-machine shop under KERC HT-2(a). For a given set of jobs and
machines it must:
(a) return a feasible schedule that minimises total electricity cost for the user's demand-charge situation;
(b) show the full energy-vs-peak trade-off and the **exact** break-even demand charge;
(c) translate the result into a monthly KERC bill under stated assumptions (including the contract-demand floor);
(d) explain where peak-awareness pays, backed by a controlled experiment;
(e) conditionally, show that its power model predicts measured energy and peak on physical emulated loads.

**"Demonstrable", concretely:** someone outside the team loads an instance, presses Solve, and sees FCFS vs energy-only vs
peak-aware schedules (Gantt, power curve over the tariff bands, costs). They move a demand-charge slider or pick a KERC scenario,
see the schedule switch at the break-even point, and see the monthly bill. One command reproduces every reported number.

This maps onto the Phase III rubric (`01_rubric/030 EL Rubrics (1).pdf`):

| Rubric item | Marks | What scores it |
|---|---|---|
| Prototype demonstration (functionality, innovation, usability) | 30 | The tool above |
| Results & discussion | 20 | The main study, with honest decomposition and the structural explanation |
| Report | 20 | Report document |
| Poster / PPT | 10 | Poster and slides |
| Notable outcomes | 20 | Optional paper draft |

### Success criteria (pre-stated; the targets are ours, not measured yet)
| ID | Criterion | Target |
|---|---|---|
| F1 | Every schedule the tool returns passes the independent evaluator (`model/evaluate.check_schedule`) | 100 % |
| F2 | Returned TEC ≤ TEC of B and of every baseline (safety guarantee); optimality gap reported | 100 % |
| F3 | Front-derived C matches directly solved C in TEC and makespan, on every cal2 row where both are proven | 0 mismatches |
| F4 | Benchmark reproduced; front gives exact ρ* = ₹12.70 on the benchmark (its min-peak schedule is 27 kW = C's peak, so the front is {37, 27} kW) | exact |
| F5 | Laptop runtime of the product path on experiment-size instances | p95 ≤ 60 s (target; **UNKNOWN** until measured) |
| S1 | Main study: 0 missing; every unproven result counted; intervals only with ≥ 10 seeds per cell | as stated |
| S2 | Reported per cell: conflict share, exact break-even distribution, saving at the KERC-equivalent ρ under both contract-demand scenarios | as stated |
| S3 | Value of the optimiser over the best simple energy-aware rule at the KERC-equivalent ρ, per cell | reported whatever the sign |
| P1–P2 (conditional) | Measured vs predicted energy and peak per executed schedule | pre-register error targets (e.g. ≤ 5 %) before the first measurement |

---

## 3. Model development strategy

### 3.1 Which kind of model? (alternatives compared)
| Approach | Fits this problem? | Verdict |
|---|---|---|
| Exact time-indexed CP (CP-SAT), current | Yes: exact optima at 8 × 3 × 32, verified | **Retain** |
| ε-constraint over peak levels (the planned AUGMECON, reduced) | Yes: peak takes few discrete values, so the front has ≤ 3 interior points at M = 3 | **Implement** (§7.4) |
| MILP (HiGHS/Gurobi), same formulation | Same model, no shown advantage; licence or speed **UNKNOWN** | Avoid; switching costs time |
| Simple constructive rules (energy-greedy, peak-capped greedy) | Needed as honest baselines and as a fallback for large instances | **Implement** |
| Metaheuristics (GA, NSGA-II, SA) | No optimality guarantee; tuning burden; cannot beat an exact solver at this size | Avoid unless the scaling probe fails and CP-SAT with a time limit also fails |
| Reinforcement learning, GNN schedulers | Need large realistic training distributions; no guarantees; hard to validate | **Avoid** |
| Forecasting ML (load, price) | No forecasting target: tariff is fixed, jobs are given | **Avoid** |
| Learned predictor of "does peak-awareness pay?" | Would learn the generator; the main structure is already explained analytically (§1.4.3) | Optional, low value |

### 3.2 What "training, calibration, validation" mean here
* **Training:** none. Parameters come from the tariff order and, if the rig is built, from measured load powers.
* **Calibration:**
  * experimental design: done (pilot, cal2);
  * solver budgets: done (decision D4);
  * physical parameters: measure each load's steady-state power, which becomes P_m. This is the only real data path, and what H4
    in the master context asks for.
* **Validation:**
  * correctness: oracle on tiny instances, the benchmark, and the independent evaluator on every schedule;
  * cross-method consistency: front-derived C vs direct C;
  * generalisation: a fresh-seed confirmatory study with frozen analysis rules;
  * physical: measured vs predicted.
* **Leakage and overfitting analogues:**
  * design choices made by looking at cal2 must not be evaluated on cal2 instances;
  * do not pick W levels only where savings exist: report null regions;
  * never tune solver settings on the instances that are reported.

### 3.3 Inputs and outputs
* **Data:**
  * instance JSON: jobs, processing times per machine, release and deadline, machine powers, base load, 15-minute tariff vector;
  * sample instances: the benchmark plus generator instances;
  * no external dataset exists.
* **Features (analysis only):**
  * W, and the structural band ⌈W·M⌉ (the minimum number of machines that must at some point run together);
  * γ, CV, M;
  * slack (1 − makespan of A / T).
* **Compute:** 2-core laptop; cal2 averaged 52.8 CPU-s per instance across 12 strategy rows. Raspberry Pi runtime is **UNKNOWN**.
* **Outputs:**
  * schedule (job → machine, start, end) and per-slot power;
  * energy cost, peak, TEC(ρ) and the front table;
  * exact break-even ρ*;
  * monthly bill under scenarios;
  * comparison with baselines;
  * optimality status and gap.
* **How to read the result:** "At your effective demand charge ρ_eq, the peak-aware schedule saves ₹X per shift (₹Y per month if
  contract demand is lowered, ₹Y′ if not) by keeping peak at 32 instead of 47 kW, at an extra energy cost of ₹Z. Below
  ρ* = ₹…/kW, run the energy-only schedule."

### 3.4 Baselines, and how we show the optimiser is "meaningfully better"
1. FCFS and SPT (exist): a proxy for current practice. Report them, but never as the headline (§1.4.2).
2. A, makespan-optimal (exists): production first.
3. **Energy-greedy rule (new):** put each job on its minimum-energy machine, in the cheapest feasible window. A planner could do
   this in a spreadsheet.
4. **Peak-capped greedy (new):** the same rule with a cap on simultaneous power; try each achievable cap and keep the cheapest.
   This is the simplest possible peak-aware rule.
5. B / B_minpeak (exist): the exact energy-only optimum, the scientific counterfactual. B_minpeak is the conservative version.

Three distinct claims, kept separate:
* **value of peak-awareness:** C vs B_minpeak;
* **value of exact optimisation:** C vs the better of rules 3 and 4;
* **value vs current practice:** C vs FCFS, decomposed into FCFS → energy rule → B → C.

Each is a paired per-instance difference, reported as distributions, the share of instances with at least 1 % saving, and (with
≥ 10 seeds per cell) stratified-bootstrap intervals. Pre-stated rule: if the best simple rule is within 1 % TEC of C on ≥ 90 % of
instances at the KERC-equivalent ρ, we report that exact optimisation adds little at this scale, and the system's value then lies in
the break-even and bill analysis.

### 3.5 From research method to executable code
The pattern is unchanged: versioned design → digest → resumable runner → `results/<run>/results.csv` → analysis scripts → figures and
CSVs → handoff document, with tests pinning every digest. New pieces plug into the same pipeline (§5).

---

## 4. Research-to-implementation gap: every major component
| Component | Purpose | Necessary? | Code / status | Evidence needed | Verdict |
|---|---|---|---|---|---|
| Model V1.0 formulation | Feasible schedules, exact energy and peak | Yes | `model/formulation.py`, done | Done (oracle, benchmark) | **Retain unchanged** |
| Lexicographic stages and stop rule | Reproducible tie-breaks; no false optimality | Yes | `model/solver.py`, done | Done | Retain |
| ε-constraint / AUGMECON | Pareto structure (RQ1), exact break-even | Yes, reduced to energy vs peak | Missing | Front = direct C on cal2; benchmark ρ* | **Modify → implement** |
| Full 3-objective front (makespan, energy, peak) across the factorial | RQ1 in full | No: makespan acts mainly through the deadline; cost multiplies | Missing | n/a | Discard for the study; show on one demo instance at most |
| Model A (ρ per shift) | Sensitivity axis | Yes | Done | n/a | Retain |
| Model B (₹/kVA/month, BD floor, PF) | Real bill | Yes, for interpretation | Missing | Hand-checked arithmetic tests | **Implement post-hoc only**; not in the solver (`tariff_reference.md` keeps monthly aggregation outside the core model) |
| B_maxpeak | Worst-case energy-only peak | No: band non-zero in 4 of 75 proven pairs; B_minpeak + B_maxpeak use 14.2 % of solver time | Done | n/a | **Drop**; keep B_minpeak as the conservative baseline |
| C solved per ρ (5 solves, 68 % of solver time) | Savings at grid ρ | Superseded by the front | Done | n/a | Replace by the front; keep one direct C level (ρ = 14) as a cross-check |
| Break-even upper bound ρ*_ub | Decision metric | Yes, made exact via the front | Done | Front | **Modify** |
| W definition and generator | Workload factor | Yes | Done | Theorem (§1.4.3) documented | Retain; place W levels relative to k/M |
| CV levels {0, 0.35, 0.75} | Heterogeneity | Partly | Done | Report actual powers | Retain, with CV = 0.75 labelled a stress case (1.2 / 15 / 28.8 kW) |
| Heuristic acceptance filter | Feasibility | Harmless in range (89/90 first draws) | Done | Done | Retain, documented |
| Stratified cluster bootstrap | Uncertainty | Yes at ≥ 10 seeds | Done | Done | Retain |
| γ levels | ToD sensitivity (RQ3) | Yes | Done | Anchors | Retain; γ = 1 matches KERC Jul–Nov, 19/14 matches KERC Dec–Jun, 7/4 is synthetic |
| Scalability (Exp. H, RQ7) | Does it work beyond toy size? | Yes (laptop) | Missing | Scaling probe | **Implement** (probe); Raspberry Pi conditional |
| Physical validation (Exp. I/J, RQ6, H4) | Model fidelity | Conditional: core in the master context, but no hardware yet | Missing | Measured vs predicted | Conditional, gate by 23 Nov |
| κ speed–power coupling | Realistic CV | Optional | Missing | `cal2b` | Defer (your D2) |
| Monte Carlo, rolling horizon, dashboards beyond the demo, ML | — | No | — | — | **Discard** |

---

## 5. Execution roadmap

Dates assume decisions on 20–21 Nov. Gates are marked ⛔ (stop and decide). **E** = essential, **C** = conditional, **O** = optional.

### P0 — Freeze decisions, version control, purchasing (E) · 20–21 Nov
* **Tasks:**
  * decide D-1…D-6 (§7.2);
  * commit the 141 files to a branch, with your permission;
  * pin exact package versions;
  * hardware go/no-go: buy parts now or drop.
* **Files:** `requirements.txt` (pin `ortools==9.15.6755` plus the others), `docs/handoff/OVERNIGHT-STATUS.md`.
* **Done when:** decisions written down; branch pushed; `pip install -r requirements.txt && pytest` passes on your machine.

### P1 — Front solver, safety guard, gap recording, Model B bill (E) · 21–22 Nov
* **Method:**
  * solve B and P;
  * then iterate downward: solve "min EC s.t. peak ≤ (last peak − 1 W)", then minimise makespan, until reaching P's peak (the
    ε-constraint with integer step);
  * C(ρ) = the front point minimising EC + ρ·peak, with ties broken by makespan;
  * exact ρ* = min over front points of ΔEC / (6000·Δpeak) relative to B (integer units as in `rho_star_pair`);
  * warm-start each cap solve with the previous schedule (`model.add_hint` is already used between stages);
  * record `solver.best_objective_bound` (already computed in `StrategyResult.best_bound_last_stage`) to report an optimality gap;
  * product guard: return the cheapest *feasible* candidate among {front points, B, rules}, so returned TEC ≤ TEC(B) always.
* **Model B, post-hoc:**
  * monthly bill = D·EC_shift + 350·BD, with BD = max(MD/PF, 0.90·CD);
  * scenarios: contract demand renegotiated vs fixed at the old peak; PF ∈ {1, 0.9}; D ∈ {22, 26, 30} days;
  * ρ_eq = 350 / (D·PF) per shift, giving ₹13.46/kW at D = 26 and ₹11.67 at D = 30 (PF = 1). This assumes the same schedule every
    working day and that this shift sets the month's MD.
* **Files:**
  * new: `07_src/model/front.py`, `07_src/model/billing.py`;
  * modified: `model/solver.py` (optional initial hint), `model/__init__.py`;
  * tests: `tests/test_front.py`, `tests/test_billing.py`, plus a brute-force front in `tests/oracle.py`;
  * cross-check: `07_src/scripts/validate_front.py` → `results/front_validation/`.
* **Tests:**
  * oracle front on tiny instances;
  * benchmark ρ* = ₹12.70 exact;
  * front vs direct C on all 450 cal2 C rows (where both are proven: equal TEC and makespan);
  * billing hand examples, including the 47 → 32 kVA floor case.
* **Done when (⛔ Gate 1, rule in §7.6):** F3 and F4 pass; median front runtime per instance ≤ cal2 direct-C time for the same
  instance, or the cause is understood.

### P2 — Honest baselines (E) · 22 Nov
* **Tasks:** energy-greedy and peak-capped greedy rules, deterministic and tariff-aware.
* **Files:** `experiments/baselines.py`, `tests/test_baselines.py`.
* **Tests:** evaluator feasibility on all cal2 instances; never claims infeasibility; deterministic output; hand-checked on the
  benchmark.
* **Done when:** all cal2 instances are evaluated, and a decomposition table (FCFS → rule → B → C) is produced on cal2 as a
  descriptive preview.

### P3 — Scaling probe (E to run; C whether a second machine count enters the study) · 22 Nov
* **Tasks:**
  * sizes (jobs × machines): 8 × 3, 12 × 4, 16 × 5, 20 × 6, with W chosen in the band below (M−1)/M;
  * γ = 19/14, CV ∈ {0, 0.35}, 2 seeds each;
  * product path (B, P, front) with the existing budgets;
  * record proven share, gap and time.
* **Files:** `experiments/design.py` (`ScalingDesign`), `07_src/scripts/scaling_probe.py`, `results/scaling_probe/`.
* **Decision rule ⛔ Gate 2:** the largest size where ≥ 90 % of front solves are proven within budget becomes M₂ for the main
  study. If 12 × 4 fails: stay at M = 3, state the limit, and use rule + time-limited CP-SAT (with reported gap) beyond that size.

### P4 — Main-study specification and smoke run (E) · 23 Nov
* **Design (recommended):**
  * M = 3: γ {1, 19/14, 7/4} × W {0.40, 0.475, 0.55, 0.625} × CV {0, 0.35, 0.75 (stress)} × **15 fresh seeds** = 540 instances;
  * W = 0.70 replaced by the theorem plus cal2's 18 instances as illustration (it is provably null);
  * optionally W = 0.25 (below 1/3, where overlap of two machines is not forced) if budget allows;
  * plus, if Gate 2 passes, an M₂ block: γ = 19/14 × 3 W levels × CV {0, 0.35} × 10 seeds = 60 instances.
* **Strategy set:** A, B, B_minpeak, P, front, C@ρ = 14 (cross-check), FCFS, SPT, the two rules.
* **Analysis rules frozen in the spec:**
  * conflict labels evaluated on the whole curve, not the endpoints;
  * the theorem-based "no conflict" rule;
  * n_valid / n_total printed in every cell;
  * intervals only with ≥ 10 seeds per cell;
  * ρ grid {1, 2, 5, 14, 50} plus ρ_eq scenarios, evaluated from the front, so no extra solves.
* **Files:** `docs/handoff/SPEC-003-main-study.md`; `experiments/design.py` (`DESIGN_MAIN`, new version string and base seed);
  runner columns (front points, bound/gap, rules); tests pinning the digest; `results/main_smoke/`.
* **Gate ⛔ 4:** smoke-run runtime estimate (the cal2 estimate ran ~33 % high) plus your approval before the full run.

### P5 — Main run (E) · 23–24 Nov, overnight
* **Command:** `run_experiment.py --design main --out results/main --workers 2` (resumable).
* **Expected size:** about 540 × 50 CPU-s ≈ 7.5 CPU-h ≈ 3.8 h wall on 2 workers. This is projected from the cal2 mean; the front
  may be cheaper than the 5 direct C solves. Re-estimate in P4.
* **Done when:** 0 missing, single digest, aggregate written.

### P6 — Analysis and results (E) · 25–26 Nov
* **Outputs:**
  * conflict share by structural band, γ, CV and M;
  * exact break-even distribution;
  * savings at each ρ and at ρ_eq under both contract-demand scenarios (monthly ₹);
  * the decomposition FCFS → rule → B → C;
  * optimiser vs best rule (S3);
  * runtime and proven shares;
  * all intervals from the stratified bootstrap.
* **Files:** `analysis/report.py` (extend), `analysis/billing_report.py`, `docs/handoff/MAIN-RESULTS.md`.
* **Tests:** extend `tests/test_analysis.py` with exact answers on synthetic frames, including the theorem rule and billing.
* **Done when:** every number in MAIN-RESULTS.md traces to a CSV, and negative or null results are stated.

### P7 — Prototype tool (E) · 24–28 Nov, parallel with P5/P6
* **CLI:** `python -m app solve --instance examples/benchmark.json --kerc D=26,PF=1,cd=fixed` prints the schedule, front, ρ*,
  bill, baselines and gap, and writes the schedule JSON (also the ESP32 format) plus PNGs.
* **UI:** a thin Streamlit app over the same functions (justified by the 30-mark usability criterion; one new dependency). It offers:
  * an instance picker and editor;
  * Solve;
  * three Gantt charts with the power curve over the tariff bands;
  * a ρ / KERC-scenario slider driven by the precomputed front (instant, no re-solve);
  * the bill.
* **Files:** `07_src/app/{io.py, plots.py, cli.py, ui.py}`, `examples/*.json` (benchmark plus 3 generator instances),
  `tests/test_cli.py` (golden output on the benchmark), `tests/test_io.py` (schema round-trip).
* **Done when:** F1, F2 and F5 are met on the examples, and a non-team member can run the demo from the README.

### P8 — Physical validation rig (C, Gate 3 = parts in hand by 23 Nov evening) · 24–29 Nov
* **Minimal rig:**
  * ESP32 plus one INA226 on the common 12 V rail (measures the aggregate peak, which is what matters);
  * optionally one INA226 per load (calibrates each P_m);
  * 3 switched loads of different power;
  * serial link to the laptop (MQTT and the Raspberry Pi are not needed for validation).
* **Protocol:**
  * time-scaled slots (e.g. 15 min → 10 s) and power-scaled instance built from the *measured* load powers;
  * execute FCFS, B and C schedules, 3 repeats each;
  * measured peak = maximum slot-average power, matching the model's definition.
* **Metrics:** energy and peak errors vs prediction; timing jitter; inrush transients (which the model ignores) reported separately.
* **Files:** `09_hardware/firmware/esp32_scheduler/`, `07_src/testbed/{run_schedule.py, compare.py}`,
  `09_hardware/calibration/`, `results/physical/`.
* **Honest scope:** this validates power aggregation and schedule execution at 12 V / watt scale. It does not validate industrial
  savings.
* **If no-go:** state RQ6/H4 as not addressed and keep the demo software-only. Do **not** simulate "measurements".

### P9 — Demo freeze (E) · 28–30 Nov
* **Tasks:** correct README.md (timeline, hardware status, claims), demo script, rehearsal, poster and slide drafts.
* **Gate ⛔ 5 (29 Nov):** freeze; after this, only bug fixes.

### P10 — Report and submission (E) · 2–7 Dec
* **Tasks:** report, final poster and slides, reproducibility pack (one script regenerating every figure from `results/`),
  final test and benchmark run, tagged commit.
* **Optional (20-mark "notable outcomes"):** a workshop or conference paper draft built on the main study and the theorem.

### Avoid entirely
* ML, RL or forecasting;
* NSGA-II or other metaheuristics;
* Model B inside the solver;
* rolling-horizon scheduling;
* more reformulation of Model V1.0;
* dashboards beyond the demo UI;
* MQTT or Raspberry Pi integration before the serial rig works.

---

## 6. Risks and what could invalidate the results
| Risk | Effect | Mitigation | Fallback |
|---|---|---|---|
| Bug in the front or billing code | Wrong headline numbers | Oracle, benchmark ρ*, 450-row cross-check vs direct C, hand billing tests | Keep per-ρ direct C (current, validated) |
| Front cap solves often unproven | Exclusions return | Warm start, gap reporting, theorem rule | Per-ρ C with B-hint |
| Strawman comparison (FCFS) | Overstated value | Rules 3 and 4, decomposition, headline = C vs B_minpeak | — |
| Result is an artefact of M = 3 (coarse peak levels, threshold at 2/3) | Limited generality | M₂ block (Gate 2); state the structural explanation | Restrict claims to M = 3 explicitly |
| CV = 0.75 machine implausible | CV conclusions questioned | Report powers; label as stress case; base main conclusions on CV ≤ 0.35 | κ sensitivity if time allows |
| Billing realism (BD floor, PF, MD interval **UNKNOWN**, ToD optional below 500 kVA, consumer category for a ~50 kW plant **UNKNOWN**) | Real-₹ savings may be far smaller | Scenario bills, including the fixed-CD case; verify the MD interval and category in the tariff order PDF before the report | Present ρ results as sensitivity only |
| Design tuned on cal2 | Optimistic bias | Fresh seeds; analysis rules frozen in SPEC-003 | — |
| Compute overrun | Late results | Smoke estimate; resumable runner; drop ρ = 50 or the M₂ block first | 10 seeds instead of 15 |
| Hardware: procurement, inrush, timing | No physical evidence | Gate 3; minimal serial rig; slot averaging | Software-only demo, RQ6 stated as not addressed |
| Unpinned versions, untracked files | Non-reproducible | P0 | — |
| README overclaims | Credibility at evaluation | P9 correction | — |
| Deterministic, single-shift model (no breakdowns, no processing-time variance) | Real-plant transfer | State as scope limit | — |

**Results that would change the conclusions** (and must be reported if they occur):
* simple rules match the optimiser (S3);
* the fixed-contract-demand scenario erases most of the savings;
* front mismatches vs direct C;
* M₂ shows a different pattern than M = 3.

---

## 7. Immediate next steps

### 7.1 Recommended direction
Keep exact optimisation, but finish it as a product and a fair experiment, in this order:
1. the front solver, so one solve gives every ρ and the exact break-even;
2. honest baselines;
3. the real-bill layer;
4. the main study on fresh seeds;
5. the usable tool;
6. physical validation only if parts arrive by 23 Nov.

No machine learning.

### 7.2 Decisions needed from you (one line each is enough)
* **D-1:** adopt the front method in place of per-ρ C (recommended).
* **D-2:** include an M₂ block if the scaling probe passes (recommended).
* **D-3:** main study at M = 3, W {0.40, 0.475, 0.55, 0.625}, 15 fresh seeds, W = 0.70 covered by the theorem, B_maxpeak dropped
  (recommended); optional W = 0.25 (below 1/3).
* **D-4:** CV = 0.75 kept and labelled a stress case (recommended), or replaced.
* **D-5:** hardware go/no-go, with parts in hand by 23 Nov evening.
* **D-6:** Streamlit UI (recommended), or CLI plus static HTML only.
* **Also:** permission to commit the Phase 3 work to a branch (not `main`).

### 7.3 Steps in priority order
1. P0: decisions, branch commit, pinned versions, parts order.
2. **P1: front solver + safety guard + gap + billing** (first component).
3. P2: energy-greedy and peak-capped rules.
4. P3: scaling probe → Gate 2.
5. P4: SPEC-003 + smoke → Gate 4.
6. P5: main run.
7. P6: analysis.
8. P7: CLI + UI (in parallel).
9. P8: rig, if Gate 3 passes.
10. P9 → P10.

### 7.4 First component: the energy-vs-peak front (`07_src/model/front.py`)
Why it comes first:
* It is the core of the tool: one call answers every demand charge.
* It replaces the most expensive part of the experiment. Direct C used 3227 of 4750 solver seconds in cal2, while the front needs at
  most 0–3 extra solves beyond B and P: in cal2, of the 85 instances with a proven P, 64 have no achievable peak level strictly between P and B,
  5 have one, 10 have two and 6 have three.
* It upgrades the break-even from an upper bound to an exact value.
* It is the method already chosen in the master plan, so this is completion, not new research.
* It can be validated cheaply against 450 existing results.

### 7.5 Expected output
* **API:**
  * `ec_peak_front(inst) → [FrontPoint(peak_w, ec_int, makespan, schedule, status, bound)]`;
  * `best_for_rho(front, ρ)`, `exact_break_even(front)`, `tec_curve(front, ρ_range)`.
* **Validation report** in `results/front_validation/`:
  * rows compared;
  * exact TEC and makespan matches (expected: all), with any mismatches listed;
  * exact ρ* vs the cal2 upper bound per instance;
  * front time vs direct-C time per instance;
  * benchmark ρ* = ₹12.70.

### 7.6 Proceed, revise or abandon
* **Proceed** if:
  * 0 mismatches where both methods are proven;
  * benchmark ρ* is exact;
  * the oracle agrees;
  * median front time ≤ direct-C time for the same instance.
* **Revise** if:
  * mismatches trace to tie-break semantics (fix and document);
  * cap solves are slow on infeasible caps (skip caps below the structural lower bound, i.e. base plus the ⌈W·M⌉ lowest-power
    machines).
* **Abandon** (keep per-ρ direct C with a B-hint) if more than 10 % of cap solves stay unproven on instances where direct C was
  proven at every ρ. In that case the front would be less reliable than the method it replaces.
