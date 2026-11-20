# SPEC-002 v2 — Proposal: second calibration pilot ("cal2-v1")

**Status: PROPOSAL for your approval. The calibration design is implemented as an inert configuration; it has NOT been run.
The 405-instance experiment has NOT been run. Everything quoted from the first pilot is PRELIMINARY (n = 1 per cell).**
Evidence base: `docs/handoff/PILOT-RESULTS.md`, `results/pilot27/results.csv` (unchanged, sha256 pinned in a test), and two new
analyses in `results/cal2_prep/` (`acceptance_study.py`, `estimate_runtime.py`, with their `.txt` outputs).

## 1. What the pilot left open, and what the new analyses add
| # | Pilot observation | Verified in CSV | Additional evidence from this step |
|---|---|---|---|
| 1 | Peak reduction possible in only 4/27 instances, all W = 0.40 | yes (3 at CV 0, 1 at CV 0.35 / γ 7/4) | see mechanism below |
| 2 | 18/18 instances at W = 0.70, 0.90: zero saving | yes (B peak = P peak in 18/18) | even *unfiltered* feasible instances at W = 0.90 leave only ≈3 % makespan slack (§4), so this null is structural, not a filter artefact |
| 3 | All 4 break-even upper bounds < ₹5 (0.00, 0.93, 3.50, 4.95) | yes | ρ = ₹5 is above every observed bound |
| 4 | Levels ₹5/14/50 miss the sub-threshold region | follows from 3 | — |
| 5 | C: 92.6 % stage-1 proven, 72.8 % fully proven | yes (75/81, 59/81) | difficulty rises with ρ (unproven 1/10/11 of 27 at ₹5/14/50), so adding ρ = ₹1, ₹2 should be cheap |
| 6 | Acceptance 8 % at W = 0.90 | yes (8.0 %) | reproduced independently: 8.6 % of 2000 draws (§4) |

**New finding — an interpretation problem with CV (needs your decision, §7-D2).** The generator draws processing times
independently of machine power. For CV > 0 the lowest-power machine is therefore also the minimum-energy machine for
97 % (CV 0.35) and 100 % (CV 0.75) of jobs, yet the fastest for only 36–40 % (chance ≈ 33 %). The energy-optimal schedule B then
concentrates work on the one machine that is simultaneously cheapest in energy *and* lowest in power, so energy and peak do not conflict.
This is consistent with the pilot (3 of the 4 informative instances have CV = 0; CV = 0.75: no peak reduction anywhere), but it is a
mechanism hypothesis, not a result. As generated, "CV" is not a clean heterogeneity factor; it creates a dominant machine.

## 2. Proposed calibration design `cal2-v1` (config `DESIGN_CAL2`, version `SPEC-002/v2-cal1`)
| Item | v1 full design | **cal2-v1 (proposed)** |
|---|---|---|
| γ (generation cell) | 1, 19/14, 7/4 | **same** (preserved) |
| CV (generation cell) | 0, 0.35, 0.75 | **same** (preserved) |
| W (generation cell) | 0.40, 0.70, 0.90 | **0.40, 0.475, 0.55, 0.625, 0.70** (equally spaced, 0.075; anchors 0.40 / 0.70 repeat the pilot's levels with new seeds; 0.90 dropped) |
| ρ (repeated measure, ₹/kW) | 5, 14, 50 | **1, 2, 5, 14, 50** (adds the sub-threshold region; keeps the three pilot points for continuity) |
| Seeds per cell | 15 | **2** (replication check, balanced) |
| Generation cells | 27 | **45** |
| Generated instances | 405 | **90** (18 per W level, 30 per γ, 30 per CV) |
| (instance, ρ) comparisons | 1215 | **450** (every ρ on the identical instance — pairing preserved) |
| Result rows / CP-SAT runs | 4050 / 3240 | **1080 / 900** |
| Instance size, tariff, power, solver limits | N 8, M 3, T 32 … | **identical** (so results are comparable to the pilot) |
| Base seed | 20261115 | 20261116 (independent draws; pilot instances are not reused) |

Implementation: `experiments/design.py` — `CalibrationDesign(Design)` (adds only a different `version` string), `DESIGN_CAL2`, registry
`DESIGNS`; CLI `--design cal2`. `DESIGN_FULL` and the pilot's digest are unchanged (pinned in `tests/test_calibration_design.py`:
full `c9af6944fe5da183`, pilot `37af47cf7472c2c4`). cal2 digest `99596784481ea861`. All validity/optimality filters, per-row digest
checks, missing/unproven counting and `--force` archiving apply unchanged; the report stays PRELIMINARY (`--validated` needs the exact full design).

### Why these levels (evidence, not preference)
* **W:** the pilot's slack of the minimum-makespan schedule (share of T) was 57 % at W = 0.40, 23 % at 0.70 and 3 % at 0.90, and peak
  reduction vanished between 0.40 and 0.70. Three interior levels resolve that interval; W = 0.90 is a boundary case already documented.
* **ρ:** four break-even upper bounds sit at 0–4.95 ₹/kW, so ρ = 1 and 2 are needed to see where C starts to differ from B; 5/14/50 are kept so the
  new run connects to the pilot and to the benchmark's ρ* = ₹12.70.
* **Seeds = 2:** the aim is calibration, not inference. Two seeds per cell show whether replicates agree on the key indicator; they do not
  support confidence intervals and are not used to claim effects. Raising to 3 seeds would cost +50 % (§5) and is not needed for the decision.
* **γ, CV kept:** as requested; with n = 6 per (W, CV) and 6 per (W, γ) they remain descriptive.

## 3. What the calibration will measure (fixed in advance)
Endpoints, all computed with the existing validity filters (B/C/P proof requirements, `saving_valid`, `full_valid`, `ρ*_ub` upper-bound labelling):
* **E1 conflict indicator** — share of instances with `state_B == ok` (peak reduction possible between B and P), by W (n = 18), by (W, CV) (n = 6), by (W, γ) (n = 6); exact binomial intervals shown only as descriptive.
* **E2 replicate agreement** — in how many of the 45 cells both seeds agree on E1.
* **E3 ρ-regime** — for conflict instances, the share with strictly positive saving at each of the 5 ρ levels and the distribution of `ρ*_ub`; "sub-threshold captured" if saving at ρ = 1 is positive in clearly fewer conflict instances than at ρ = 5.
* **E4 solver reliability** — stage-1 and full proof rates for C by (W, ρ); counts of missing/unproven rows.
* **E5 transition** — W where E1 falls from its W = 0.40 value to ≈ 0. Rule for the v2 full design: place its W levels at the observed high, ≈ 50 %, low and ≈ 0 points of E1, not at equal steps.
Pre-stated predictions (so they can be wrong): (a) E1 decreases with W; (b) under the current generator E1 ≈ 0 for CV > 0 at every W (dominance mechanism); (c) fewer conflict instances show saving at ρ = 1 than at ρ = 5.
**Not** concluded from cal2: any significance statement, γ/CV effect sizes, or anything about Model B (real ₹/kVA tariff).

## 4. Generator acceptance and SPT analysis (`results/cal2_prep/acceptance_study.py`; no experiment run)
Heuristic acceptance (FCFS or SPT meets D = T), 2000 raw draws per W:
| W | 0.55 | 0.60 | 0.65 | 0.70 | 0.75 | 0.80 | 0.85 | 0.90 | 0.95 |
|---|---|---|---|---|---|---|---|---|---|
| FCFS feasible | 1.000 | 1.000 | 0.998 | 0.958 | 0.815 | 0.558 | 0.275 | 0.079 | 0.009 |
| SPT feasible | 1.000 | 0.999 | 0.989 | 0.914 | 0.695 | 0.387 | 0.106 | 0.009 | 0.000 |
| **accepted (either)** | 1.000 | 1.000 | 1.000 | **0.992** | 0.921 | 0.701 | 0.346 | **0.086** | 0.009 |

Exact feasibility (does *any* schedule meet D? CP-SAT, 40 draws per W) versus the heuristic filter:
| W | exactly feasible | heuristic-accepted | feasible but rejected (of 40) | mean min-makespan of feasible (T = 32) |
|---|---|---|---|---|
| 0.70 | 1.00 | 1.00 | 0 | 24.2 |
| 0.80 | 1.00 | 0.75 | 10 | 27.7 |
| 0.85 | 1.00 | 0.40 | 24 | 29.5 |
| 0.90 | 0.95 | 0.15 | 32 | 31.1 |
| 0.95 | 0.43 | 0.03 | 16 | 31.8 |
* **Selection bias is real above W ≈ 0.75 and comes from the heuristic filter, not from feasibility:** at W = 0.90 it discards ≈ 85 % of the instances that are feasible. Pooled over W ≥ 0.80, accepted instances have shorter longest jobs (14.5 vs 15.7 slots) and more slack (min makespan 28.6 vs 30.4 of 32) than feasible-but-rejected ones. (Pilot W = 0.90 results are therefore for an easier-than-feasible subset.)
* **On the cal2 grid (W ≤ 0.70) the filter is practically inert, not absent:** expected rejection ≤ 0.8 % at W = 0.70 and ≈ 0 below; in the 90 cal2 instances 89 are first draws and exactly one (W = 0.70) needed a second draw (pinned in a test).
* **SPT infeasibility** is structural: SPT is a flow-time rule that postpones the longest jobs to the end, so deadline failures appear early. On feasible instances its makespan is 1.20× the optimum at W = 0.70 (FCFS 1.12×). SPT stays ≥ 91 % feasible up to W = 0.70 (pilot 7/9 at 0.70), so SPT/FCFS remain usable baselines on the cal2 grid; above W ≈ 0.75 only FCFS is meaningful.
* If W > 0.70 is ever studied, replace the heuristic filter by an exact-feasibility filter (accept iff strategy A finds a schedule within T; ≈ 1 s per draw, acceptance ≈ 95 % at W = 0.90 instead of 8.6 %). That is a generator-rule change needing its own version and is not part of cal2.
* The generator refactor used for this study (`draw_instance`, the raw draw) is behaviour-preserving: all 27 pilot instances regenerate identically (attempts, W, and B-strategy metrics match the stored results).

## 5. Expected solver workload and runtime (estimated before execution; `results/cal2_prep/runtime_estimate.txt`)
Basis: measured pilot solve times at W = 0.40 (57.0 s per instance) and W = 0.70 (87.0 s); interior W levels and ρ = 1, 2 are *unmeasured* and enter as scenarios.
| Scenario (ρ = 1, 2 cost \| interior W) | CPU-hours (95 % bootstrap over pilot instances) | wall-hours, 2 workers |
|---|---|---|
| easy \| linear interpolation | 1.88 (1.29–2.49) | 0.94 |
| **central** (= ρ = 5 cost) \| interpolation | **1.96 (1.30–2.58)** | **0.98** |
| central \| interior 1.5× harder than the harder anchor | 2.90 (1.94–3.91) | 1.45 |
| hard (= ρ = 14 cost) \| interior harder | 3.91 (2.68–5.49) | 1.95 |
* Expected: ≈ 1–2 h wall on 2 workers; ≈ 78 s CPU per instance. Hard cap from the applied deterministic limits: ≤ 914 s per instance = 11.4 h wall; the pilot's most expensive instance took 170 s, so the cap is not a realistic scenario.
* Solver limits are **unchanged** from the pilot (effective limits: deterministic 60 s stage 1, 15 s tie-break; the configured 180 s / 60 s wall limits are safety nets that did not bind). Expect unproven C rows mainly at ρ ≥ 14 (pilot: 21/54), few at ρ ≤ 5 (pilot: 1/27); all are counted, none removed.
* With 3 seeds per cell: +50 % (≈ 3 CPU-h central).

## 6. Comparison with the original design and deadline feasibility
| | v1 full | cal2 |
|---|---|---|
| Purpose | validated factorial | calibrate W transition and low-ρ region |
| Instances / rows | 405 / 4050 | 90 / 1080 |
| Signal (pilot evidence) | only in the W = 0.40 third of the grid (4 of its 9 instances) | W 0.40–0.70 resolved in 5 levels to locate the transition |
| ρ regime coverage | above all observed break-evens | spans sub-threshold to saturation |
| Generator filter effect | up to 92 % of draws rejected at W = 0.90 | ≈ 1 % of instances (1/90) |
| Est. runtime | 5.7 CPU-h (2.9 h wall) | 1.96 CPU-h (≈ 1 h wall), range 1.9–3.9 |
| Statistical use | inference (15 seeds) | descriptive (2 seeds) |

Schedule (today 15 Nov; demo 1 Dec; hard submission 7 Dec): cal2 run ≈ 1–2 h → calibration analysis and design freeze ≈ 1 day → v2 full run (indicatively 360 instances × 78 s ≈ 7.8 CPU-h ≈ 3.9 h wall on 2 workers, to be re-estimated after cal2) → analysis and report text. This leaves > 1 week of buffer before 1 Dec. The runner is resumable and deterministic; a process left running when a chat session ends is usually stopped, so launch on a machine that stays on, or re-issue the same command to resume.

## 7. Decisions needed from you
* **D1 — Approve `cal2-v1` as specified** (W 0.40/0.475/0.55/0.625/0.70; ρ 1/2/5/14/50; 2 seeds; γ and CV kept; limits unchanged)?
* **D2 — Speed–power coupling probe (not implemented).** Add an optional generator parameter κ: `p_jm ∝ (P_m/P̄)^(−κ)` (κ = 0 reproduces the current generator exactly; κ = 1 makes faster machines proportionally higher-power so energy per job is equal across machines and peak vs makespan genuinely conflict). Proposed as a separate small probe design `cal2b` (γ = 19/14, CV ∈ {0.35, 0.75}, W ∈ {0.40, 0.55, 0.70}, 2 seeds = 12 instances, ≈ 0.2 h) to test prediction (b). Needed if CV is to be a meaningful factor in the final report; otherwise the report must state that CV in this model means "one dominant low-power machine".
* **D3 — W = 0.90 dropped** from the main grid and reported only as pilot boundary evidence with its filter caveat (§4)?
* **D4 — Keep solver budgets identical to the pilot** (recommended: more time bought proofs, not better schedules; see PILOT-RESULTS §7)?

## 8. Implementation approach after approval
1. (done) Config + registry + tests; pilot untouched. 2. Run: `python 07_src/scripts/run_experiment.py --design cal2 --out results/cal2 --workers 2` then `python 07_src/analysis/report.py --results results/cal2`.
3. Add `07_src/analysis/calibration_report.py` for E1–E5 (reuses `paired_table` / `rho_star_pair_table`; counts missing/unproven) with tests. 4. If D2 approved: add κ to a `CouplingProbeDesign` (new field only on the new class; κ = 0 must reproduce `draw_instance` bit-for-bit, tested against the pilot) and run `cal2b`. 5. Freeze SPEC-002 v2 (W levels by rule E5, seed count from E2, ρ levels from E3) as a new versioned design; only then launch it.
