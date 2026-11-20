# P4 smoke results and GO/NO-GO for the main study

_20 Nov 2026. Branch `phase3-experiments`. Smoke designs `main-m3-smoke` (`8788174bf9477c21`, 36 instances: every
γ × W × CV cell once) and `main-m4-smoke` (`c4002ac66cfdb832`, 12 instances: W 0.40 / 0.55 / 0.70 × CV 0 / 0.35 × 2 seeds).
Same protocol, budgets and code as the main designs; separate base seed (20261122). These are **planning numbers, not study
results**. Raw output: `results/main_smoke/{m3,m4}/`; report: `results/main_smoke/report/summary.json`
(`07_src/scripts/main_smoke_report.py`)._

## 1. Recommendation: **GO**
Run M3 (540) then M4 (60), sequentially on 2 workers. **Projected wall time 2.8 h** (90 % interval 1.7–4.0 h): M3 1.9 h, then M4
0.9 h. Conditions:
* **M4 incomplete fronts.** About 1 in 12 M4 instances is expected to have an incomplete front (all at CV 0.35). Under SPEC-003
  §7 these are reported as bounds with gaps. If fewer than 90 % of M4 fronts are complete, M4 is reported as bounds only.
* **Pause rule.** The run is paused and reported if it exceeds 1.5 × the projection (4.2 h).
* **Session limit.** A run started by me must be watched in one working session (background jobs stop when a reply ends). It is
  resumable, so an interruption loses at most the instances in progress. Alternatively you can run it on your machine with the two
  commands in SPEC-003 §13.

## 2. Completeness and correctness
| Check | M3 smoke | M4 smoke |
|---|---|---|
| Instances present / expected (missing) | 36/36 (0) | 12/12 (0) |
| Rows; expected rows missing | 996; **0** | 362; **0** |
| Single design digest in results | yes | yes |
| Generation | 36/36 first draw; realised W within −0.004 / +0.017 of nominal | 12/12 first draw; within −0.013 / +0.006 |
| Front complete (exact) | **36/36** | **11/12** |
| Required front solves proven | 76/76 = 100 % | 38/42 = 90.5 % |
| Front terminations | structural bound 32, P bound 4 | structural bound 12 |
| Direct C@14 = front C@14 (both proven) | **34/34** | **8/8** |
| Guard TEC ≤ B at every ρ | yes (180/180) | yes (60/60) |
| Guard proven optimal (gap 0) | 180/180 | 55/60; the 5 others are the incomplete instance, gap 1.6–3.7 % |
| Break-even vs B | exact 24, no reduction 12 | exact 9, no reduction 2, **upper bound 1** |
| Rules succeeded (FCFS / SPT / EG / PCG) | 36 / 36 / 36 / 180 of 180 | 12 / 12 / 12 / 60 of 60 |

**Solver statuses (every non-OPTIMAL row counted):**
* **M3:** 18 of 220 solver rows are FEASIBLE: direct C 9, B_minpeak 3, FRONT_top 2, FRONT_cap 2, B 1, P 1. Every FRONT row still
  has its *required* stage proven; the unproven stages are tie-breaks. C_front is OPTIMAL in 171 of 180 rows; the other 9 have exact
  TEC with an unproven makespan tie-break.
* **M4:**
  * 21 of 90 solver rows are FEASIBLE: direct C 9, FRONT_cap 7, P 2, B 1, B_minpeak 1, FRONT_top 1.
  * Direct C is fully proven in only 3/12 instances (9/12 on its cost stage). The front is the more reliable method at this size.
  * C_front: 54 of 60 rows OPTIMAL. Of the other 6, 5 are from the incomplete instance and 1 has an unproven makespan tie-break.

**The one incomplete front.** `g0w2c1s001` (M4, W 0.70, CV 0.35, realised W 0.6875):
* 3 of its 4 capped solves are FEASIBLE but unproven at 60 deterministic seconds;
* its break-even vs B is labelled **upper bound** (₹376067/110220 ≈ ₹3.41/kW);
* the guard's schedule is within 1.6–3.7 % of a proven lower bound;
* it is the most expensive smoke instance (348 CPU-s).

## 3. Runtime
| | M3 smoke (36) | M4 smoke (12) |
|---|---|---|
| Block wall time | 446.7 s (7.4 min) | 666.2 s (11.1 min) |
| CPU per instance: mean / median / max | 24.4 / 11.7 / 159.0 s | 81.7 / 30.1 / 348.3 s |
| Parallel efficiency (CPU / 2 / wall) | 0.985 | 0.736 (12 tasks of very unequal length) |

**Mean CPU seconds per instance by W × CV:**

| M3 | CV 0 | CV 0.35 | CV 0.75 |
|---|---|---|---|
| W 0.40 | 10.3 | 41.0 | 14.0 |
| W 0.475 | 9.5 | 29.0 | 25.7 |
| W 0.55 | 8.3 | 9.1 | 13.9 |
| W 0.625 | 6.1 | 92.8 | 33.5 |

| M4 | CV 0 | CV 0.35 |
|---|---|---|
| W 0.40 | 26.6 | 76.4 |
| W 0.55 | 30.1 | 119.8 |
| W 0.70 | 17.2 | 220.3 |

M3 rows are one instance per cell and M4 rows two, so single values are noisy. The pattern matches P3: **CV 0.35 drives the cost**,
especially at high W. CV 0 is cheap at every W. By γ (M3), mean CPU is 25.3 s (γ 1), 34.2 s (19/14) and 13.9 s (7/4).

### Projection for the full study
**Method:**
* Every cell appears in the smoke run, so total CPU = smoke CPU × (main seeds / smoke seeds): × 15 for M3, × 5 for M4.
* Wall time = CPU / 2 workers / observed parallel efficiency.
* 90 % interval: bootstrap of the mean CPU per instance over smoke instances.

| Block | CPU-h (90 % interval) | Wall h on 2 workers (90 % interval) |
|---|---|---|
| M3, 540 instances | 3.67 (2.45–5.08) | **1.86** (1.25–2.58) |
| M4, 60 instances | 1.36 (0.73–2.17) | **0.93** (0.49–1.47) |
| **Total** | **5.03** | **2.79** (1.74–4.05) |

**Notes:**
* The M4 wall estimate uses the smoke's poor efficiency (0.736). With 60 tasks it should balance better (≈ 0.7 h at 0.98), so 0.93 h
  is conservative.
* It agrees with P3's independent estimate for 60 instances at 12 × 4 (0.7 h).
* A theoretical worst case, where every instance is as slow as the slowest smoke instance, is 14.8 h. That is not expected; it only
  bounds the risk.
* For comparison, the cal2 estimate was 33 % too high.

## 4. Acceptance checks
| Check | Result |
|---|---|
| Model V1.0 unchanged | `formulation.py` and `04_mathematical_model/` zero diff since P3 (and since Phase 3 began) |
| Benchmark | BENCHMARK REPRODUCED |
| Tests | 752 passed |
| Design digests pinned | `tests/test_main_design.py` (main and smoke designs); old digests (full, pilot, cal2) still pinned |
| Resumable output | Runner part files plus digest check, tested end to end (re-run skips everything; a different design is refused) |
| No old data overwritten | `git diff -- results` empty (pilot27 `516ee522…`, cal2 `857b9f1c…`, front_validation, baselines_preview, scaling_probe unchanged); smoke output in a new directory |
| All unproven results counted | Every solve and derived row is stored with its status; counts in §2 and `summary.json` |

## 5. Commands for the main run (after your approval)
```
python 07_src/scripts/run_experiment.py --design main-m3 --out results/main_m3 --workers 2
python 07_src/scripts/run_experiment.py --design main-m4 --out results/main_m4 --workers 2
```
