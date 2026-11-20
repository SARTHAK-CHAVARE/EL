# OVERNIGHT-STATUS

_Last updated: 2026-11-20 ~17:05 UTC (22:35 IST), after P2 and P3 (Gate 2). Branch `phase3-experiments`. GitHub had `fe530e0`
(pushed by you); newer commits are local until pushed (see "Open issues")._

## Plan and approvals
* The plan is `docs/handoff/ROADMAP-FINAL.md`.
* Approved on 20 Nov:
  * **D1:** front solver, with direct C at ρ = 14 kept as a cross-check and direct C kept as the fallback.
  * **D2:** a larger machine-count block only if ≥ 90 % of required front solves are proven.
  * **D3:** M = 3, W {0.40, 0.475, 0.55, 0.625}, 15 fresh seeds, all γ and CV levels, no B_maxpeak, W = 0.70 covered by the
    theorem; W = 0.25 only if runtime permits.
  * **D4:** CV = 0.75 is a stress test, separated from conclusions based on CV ≤ 0.35.
  * **D5:** no new procurement unless parts are available or guaranteed by 23 Nov evening.
  * **D6:** CLI first, then Streamlit.
  * **Git:** branch only, no force-push.

## Stage status
| Stage | Status | Evidence |
|---|---|---|
| P0: branch, pins, reproducibility | Done | Clean-env reproduction; pushed by you (`fe530e0`) |
| P1: front, guard, gaps, billing | Done; **Gate 1 passed** | `docs/handoff/FRONT-AND-BILLING.md`, `results/front_validation/` |
| P2: energy-greedy and peak-capped rules | **Done; gate met** | `docs/handoff/BASELINES-AND-SCALING.md` §P2, `results/baselines_preview/` |
| P3: scaling probe | **Done; Gate 2 → M₂ = 12 × 4 (narrow pass)** | `docs/handoff/BASELINES-AND-SCALING.md` §P3, `results/scaling_probe/` |
| P4: SPEC-003 freeze and smoke run | Next | — |
| P5 main run | **Not started** (only after P4 and your approval of the smoke estimate) | — |
| P6–P10 | Pending | — |

## Checks (actual results)
* `python -m pytest`: **739 passed** (617 + 122 rule tests).
* Benchmark reproduced.
* Model V1.0 formulation and `04_mathematical_model/verification/*`: zero diff.
* `results/pilot27`, `results/cal2` and `results/front_validation` unchanged.

## Key findings in this stage (descriptive)
* **Simple rules are not enough.** At ρ_eq = ₹13.46/kW the exact optimum beats the best simple rule by 6.7 % on average for
  CV ≤ 0.35 (12.5 % overall). The rule is within 1 % of the optimum in only 40 % / 27 % of instances, so S3's "little value" rule is
  **not** triggered.
* **Decomposition vs FCFS at ρ_eq (CV ≤ 0.35):** 13.7 points from energy-aware assignment, 5.1 from exact energy optimisation and
  5.4 from peak-awareness, 24.2 % in total.
* **Scaling.** Required front solves proven: 100 % (8 × 3), 93.3 % (12 × 4), 78.8 % (16 × 5), 60 % (20 × 6). All unproven solves are
  at CV = 0.35; CV = 0 fronts are complete at every size. Front = direct C in 21/21 comparable instances. The guard's schedule is
  within 5.4 % of a proven lower bound at every size.
* **M₂ block estimate:** 60 instances at 12 × 4 ≈ 1.4 CPU-h ≈ 0.7 h wall.

## Open issues
1. **Push:** this session still cannot push. The new commits are in `EL-phase3-p2p3.bundle` (incremental on `fe530e0`). In your EL
   folder: `git fetch <bundle> phase3-experiments && git merge --ff-only FETCH_HEAD && git push origin phase3-experiments`.
2. **Gate 2 is marginal** (12 × 4: 93.3 % from 8 instances; 7/8 complete fronts). I will include the block per D2, label incomplete
   fronts as upper bounds with gaps, and flag it in SPEC-003. Say so if you would rather drop the block.
3. **Hardware gate (D5):** answer needed by 23 Nov evening.

## Next task
P4:
* write `docs/handoff/SPEC-003-main-study.md` (M = 3 block per D3; M₂ = 12 × 4 block with W {0.40, 0.55, 0.70}; strategy set
  A, B, B_minpeak, front (incl. P), direct C@14, FCFS, SPT, EG, PCG; frozen analysis rules);
* implement the runner integration (front and rule columns, bounds and gaps), pin the new digest in tests, run a smoke run, and
  re-estimate runtime;
* then stop for your approval before P5.

## Commands
```
python -m pytest -q                                      # 739 tests
python 07_src/scripts/reproduce_benchmark.py             # benchmark
python 07_src/scripts/validate_front.py --workers 2      # Gate 1 (~5 min)
python 07_src/scripts/baseline_preview.py                # P2 preview (~1 s)
python 07_src/scripts/scaling_probe.py --workers 2       # P3 / Gate 2 (~40 min; resumable)
```
