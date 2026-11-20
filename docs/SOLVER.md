# CP-SAT solver — installation, usage, testing

Spec: `docs/handoff/SPEC-001-solver.md` (model), `docs/handoff/SPEC-002-experiments.md` (experiments).

## Install
```
python -m venv .venv && .venv/bin/pip install -r requirements.txt     # ortools, pytest, pandas, matplotlib
```
Tested on Python 3.13 with ortools 9.15. All commands run from any directory (paths are relative to the repo).

## Layout (`07_src/`)
| Module | Role |
|---|---|
| `model/tariff.py` | exact unit conversions, scaling (W, paise, minutes), KERC ToD clock |
| `model/instance.py`, `validation.py` | frozen data model; validation with all problems listed; overflow guard 10^17 |
| `model/formulation.py` | time-indexed CP-SAT model (x[j,m,t], exact peak by `AddMaxEquality`, redundant NoOverlap/Cumulative) |
| `model/solver.py` | lexicographic stages, strategies A/B/C/P, status policy, time budgets |
| `model/extraction.py`, `evaluate.py` | schedule extraction; **independent** metric recomputation (no solver imports) |
| `experiments/` | generator, FCFS/SPT, resumable runner |
| `analysis/` | tables (bootstrap CI, ρ*_pair, validity filters) and figures |

## Use
```python
from model import make_instance, SolverConfig, solve_strategy_c
res = solve_strategy_c(inst, 1500, SolverConfig(num_workers=1))   # res.status, res.schedule, res.metrics
```
`res.status` is OPTIMAL only if every lexicographic stage is proven; otherwise FEASIBLE/UNKNOWN/INFEASIBLE.
The hierarchy stops at the first stage that is not OPTIMAL (later stages do not run; the best schedule is kept,
status FEASIBLE). `res.proven_stages` / `res.n_stages` say how far the proof got; `res.primary_proven` (stage 1 only)
is weaker than `res.proven_optimal` (all stages) and must not be used in their place.
The solver re-evaluates its own schedule with the independent evaluator and raises `InternalConsistencyError`
on any mismatch.

## Reproduce the benchmark (one command)
```
python 07_src/scripts/reproduce_benchmark.py        # exit 0 + "BENCHMARK REPRODUCED"
```
Compares metrics (₹785.60, ₹912.60, 27 kW, ρ* = ₹12.70/kW and the A/B/C values), not schedules.

## Test
```
python -m pytest                                    # 341 tests
python tests/run_oracle_report.py 120               # oracle agreement report (JSON)
```
## Experiments
```
python 07_src/scripts/run_experiment.py --design smoke --out results/smoke --workers 2
python 07_src/analysis/report.py --results results/smoke
```
The 27-instance pilot is done (`docs/handoff/PILOT-RESULTS.md`). Do not run `--design full` (405 instances) until the v2 calibration decisions in `docs/handoff/SPEC-002-v2-proposal.md` are taken; `--design cal2` is the prepared calibration design (not yet run).

## Known limitations
* Time-indexed model: size grows with N·M·T; large instances (N>12, T>48) not benchmarked.
* Tie-break stages (min Cmax among cost-optimal schedules) can be much harder than the cost optimum. Such rows end
  as FEASIBLE; which analyses may still use them is defined per quantity in SPEC-002 §6 (e.g. TEC of C needs only
  stage 1, but every B-based comparison needs B fully OPTIMAL).
* Peak window L = 1 only; Model B (real kVA tariff) not implemented in the solver; ρ is Model A.
* No hardware measurements exist; nothing here is physically validated.
