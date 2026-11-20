# OVERNIGHT-STATUS

_Last updated: 2026-11-15 06:15 UTC, after the calibration run `cal2-v1` and its analysis. Nothing has been committed or pushed._

> **20 Nov 2026:** the forward plan is now `docs/handoff/ROADMAP-FINAL.md`; its decisions D-1…D-6 replace the "Open for you" list below.

## Current state in one paragraph
Solver, evaluator, oracle, generator, runner and analysis are implemented and tested. The 27-instance pilot (`results/pilot27`) and the
approved calibration run **`cal2-v1` (`results/cal2`, 90 instances, 1080 rows, 0 missing) have been executed and analysed**. Everything
from cal2 is descriptive (2 seeds per cell): no intervals, no tests, not a validated finding. The 405-instance experiment and any
main-study run have **not** been started. Next step is yours: choose the main-study design (see `CAL2-RESULTS.md` §10).

## What cal2 showed (descriptive; details and caveats in `docs/handoff/CAL2-RESULTS.md`)
* Conflict (a possible peak reduction) is present for W = 0.40–0.625 (share of determined instances 0.47 / 0.61 / 0.72 / 0.78) and absent at W = 0.70 (0/14 determined, 4 undetermined). It rises, then collapses; pre-stated prediction (a) "decreases with W" is not supported, (b) "no conflict at CV > 0" is not supported (22/55), (c) "saving rarer at ρ = 1 than at ρ = 5" is supported (15/46 vs 34/46).
* Among valid conflict instances saving is positive in 33 / 48 / 74 / 100 / 100 % at ρ = 1 / 2 / 5 / 14 / 50 (mean 0.4 / 1.0 / 3.8 / 11.6 / 24.0 %). Break-even upper bounds: all 46 between 0 and 11.5 INR/kW, median 2.3.
* Seeds agree on conflict in 15/15 CV = 0 cells and 19/25 CV > 0 cells. Solver: A/B/B_minpeak 100 % optimal, B_maxpeak 83 %, P 94 %, C 85 % fully and 96 % cost-stage proven; 0 missing rows; 18 C rows excluded as cost-unproven (17 at CV = 0.35; incumbents 40–185 % worse than B).
* Cost: 40.3 min wall, 1.32 CPU-h (pre-run estimate 1.96 CPU-h, ~33 % high). Generator: 89/90 first-draw acceptances; realised W within 0.025 of nominal.

## Decisions as given (cal2) and what is open now
D1 approved and executed. D2 deferred (no κ coupling; independence assumption retained and its implications documented in `CAL2-RESULTS.md` §8). D3 applied (W = 0.90 not in the main experiment; pilot results kept as boundary evidence with the generator-selection bias stated, §9). D4 kept (budgets unchanged; all unproven results counted).
**Open for you:** (1) main-study W levels (recommended: cal2 grid 0.40 / 0.475 / 0.55 / 0.625 / 0.70) and whether to run the optional `cal3` refinement (W 0.65, 0.675; 36 instances, ≈ 11–26 min wall) to locate the collapse; (2) replications (recommended 15 per cell = 675 instances ≈ 5 h wall; 20 per cell ≈ 6.7 h); (3) keep or drop ρ = 50 (36 % of solver time, 15 of 18 cost-unproven rows); (4) optional solver hint (B's schedule as start for C; needs oracle/benchmark/test re-run); (5) optional κ sensitivity experiment; (6) analysis rules to fix before the main run (CM §10.6).

## Changes in this step
`analysis/tables.py` (`MIN_SEEDS_FOR_INTERVALS = 10`; `summary_by(..., intervals=...)` emits no CI columns when unsupported; nominal `w_target` + realised `w_real` mean/min/max in workload summaries), `analysis/report.py` (descriptive-only mode below 10 seeds per cell; phase maps print n_valid/n_total per cell; ECDF layout fix; "nominal workload W" labels; new `summary_saving_by_W_rho.csv`), **new** `analysis/calibration_report.py` (E1–E5, counts/shares only, 7 figures), tests `tests/test_calibration_report.py` (16) and 2 new in `tests/test_analysis.py`. Not touched: model, solver, evaluator, generator, runner, `DESIGN_FULL`, `results/pilot27`, `04_mathematical_model/verification/*`.

## Checks (actual results, final)
* `python -m pytest`: **359 passed**. Benchmark: **BENCHMARK REPRODUCED** (13/13). Oracle (run before cal2; model/solver unchanged since): **720/720 agree**.
* Digests: DESIGN_FULL `c9af6944fe5da183`, pilot `37af47cf7472c2c4`, cal2 `99596784481ea861` (as pinned). `results/pilot27/results.csv` sha256 prefix `516ee522cd874edf` unchanged; `results/cal2/results.csv` prefix `857b9f1c1ef4b912`.
* No file under `07_src/model`, `07_src/experiments`, `07_src/scripts` or `04_mathematical_model` is newer than the cal2 launch; `git status`: only new untracked files, no tracked file modified.
* Output consistency checks on cal2 (CM §5): 187/187 valid rows of "no conflict" instances have exactly zero saving; saving positive in 157/157 valid conflict rows with ρ above the break-even bound and zero in 67/67 below it; minimum saving 0.

## Not done
Main-study experiment (any size); `cal3`; κ sensitivity (`cal2b`); solver hint; dominance-rule inference in the analysis (proposed, not applied); Model B in the solver; hardware work.

## Commands
Re-run the analyses on the existing results (no solver): 
```
python 07_src/analysis/report.py --results results/cal2
python 07_src/analysis/calibration_report.py --results results/cal2
```
The cal2 run itself is complete; `--force` would archive it to `results/cal2/superseded/<digest>/` and rerun.
