# OVERNIGHT-STATUS

_Last updated: 2026-11-27 (IST evening), after P7 (prototype: CLI + Streamlit) and the README correction. Branch
`phase3-experiments`. GitHub has `5d363fa`; newer commits are local until pushed (bundle provided)._

## Stage status
| Stage | Status | Evidence |
|---|---|---|
| P0: branch, pins, reproducibility | Done | Clean-env reproduction |
| P1: front, guard, gaps, billing | Done; Gate 1 passed | `FRONT-AND-BILLING.md`, `results/front_validation/` |
| P2: energy-greedy and peak-capped rules | Done | `BASELINES-AND-SCALING.md` §P2 (denominators corrected: 89 FCFS chains) |
| P3: scaling probe | Done; Gate 2 → M₂ = 12 × 4 (narrow) | `BASELINES-AND-SCALING.md` §P3 |
| P4: SPEC-003 and smoke run | Done: GO recommended, **awaiting your approval** | `SPEC-003-main-study.md`, `P4-SMOKE-RESULTS.md`, `results/main_smoke/` |
| P5: main run (540 + 60) | **Not started** (Gate 4: your approval) | — |
| P6: analysis, MAIN-RESULTS | Pending (needs P5) | — |
| P7: prototype (CLI, then Streamlit) | **Done** | `07_src/app/`, `examples/`, `tests/test_app.py` |
| README correction | **Done** | `README.md` |
| P8–P10: demo script, slides/poster, report, final package | Pending | — |

## P7 in brief
* **Shared functions** (`07_src/app/core.py`, `io.py`, `plots.py`): the CLI and the web app call the same code. It reuses the
  existing solver, front, break-even, guard and billing modules; Model V1.0 is unchanged.
* **Instances:** editable JSON (machines, jobs, tariff per slot, base load, start time). Five examples in `examples/`:
  * `benchmark.json`: the verified 4-slot benchmark;
  * `shop_8x3_kerc.json`: the main demo;
  * `shop_8x3_three_options.json`: a front with three options;
  * `shop_8x3_no_reduction.json`: no peak reduction is possible (the workload theorem case);
  * `shop_12x4.json`: the larger shop.

  `07_src/scripts/make_examples.py` regenerates the four `shop_*` files from the smoke designs.
* **CLI** (`python 07_src/app/cli.py`):
  * `solve` prints the trade-off front, the break-even with its label, a comparison table (FCFS, energy rule, peak-capped
    rule, energy-only optimum, recommended) and both partial-bill scenarios;
  * `solve` writes schedule JSON files, Gantt charts, the power profile, cost vs ρ and the front chart;
  * `generate` creates new instances.
* **Streamlit** (`streamlit run 07_src/app/ui.py`):
  * instance from an example, the generator or an upload;
  * demand charge as the KERC equivalent or a slider, plus days, PF and the contract-demand scenario;
  * tabs: schedules, power over the shift with tariff bands, trade-off, comparison, monthly bill and export.

  Every bill figure is labelled PARTIAL MONTHLY BILL ESTIMATE.
* **README:**
  * Python 3.13;
  * hardware testbed marked "designed, not built"; H3 marked "not tested";
  * tariff peak surcharge corrected to +₹1.00 (per `03_tariff/tariff_reference.md`);
  * the unsupported "15-minute integration" claim replaced with "interval not verified" (the order's only 15-minute
    reference is about data updates);
  * roadmap table set to the Dec 2026 deadlines;
  * prototype run commands added.
* **Requirements:** `streamlit==1.67.0` pinned. The lock gained only new packages; no existing version changed.

## Actual results (CLI, this run)
| Example | Break-even ρ | Recommended peak | Partial monthly saving vs energy-only (26 days, PF 1) | Run time |
|---|---|---|---|---|
| `benchmark.json` | ₹12.70/kW (exact) | 27 kW | renegotiated CD ₹198.00; fixed CD −₹2,007.00 | 1.6 s |
| `shop_8x3_kerc.json` | ₹6.00/kW (exact) | 32 kW (proven optimal) | renegotiated ₹2,910.00; fixed −₹695.00 (0.90 × CD floor binds) | 4.7 s |
| `shop_12x4.json` | ₹2.00/kW (exact) | 32 kW (proven optimal) | renegotiated ₹7,672.50; fixed −₹657.50 (floor binds) | 9.5 s |

In the fixed-CD scenario the bill rises: the demand-charge floor (90 % of the old contract demand) means a lower peak saves
nothing while energy still costs more. The app states this; it is a finding, not a bug.

## Checks (actual)
* **760 tests passed:** 752 earlier, plus 8 new app tests covering:
  * benchmark golden values;
  * bills;
  * guard ≤ B;
  * a CLI subprocess run;
  * a headless Streamlit AppTest.
* Benchmark reproduced.
* Model V1.0, `04_mathematical_model/` and the verification scripts: zero diff.
* No result file modified.
* Charts checked visually on the benchmark, 8 × 3 and 12 × 4 examples.

## Open issues
1. **Push:** the commits after `5d363fa` are in `EL-phase3-p7.bundle`, which supersedes `EL-phase3-p4.bundle`. In your EL folder:
   `git fetch <bundle> phase3-experiments && git merge --ff-only FETCH_HEAD && git push origin phase3-experiments`.
2. **Gate 4 (your decision):** approve the main run (about 2.8 h wall) and say who runs it.
3. **D5:** no components were confirmed by 23 Nov. Under D5 the demo is software-only unless you say otherwise.

## Next task
P8: demo script and slides, using the prototype and the examples above. Then P5/P6 once the main run is approved.
