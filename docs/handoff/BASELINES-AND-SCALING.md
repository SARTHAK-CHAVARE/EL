# P2 (honest baselines) and P3 (scaling probe, Gate 2)

_20 Nov 2026, branch `phase3-experiments`. Model V1.0 and all earlier results unchanged. Every number below comes from
`results/baselines_preview/` or `results/scaling_probe/`. All of it is **descriptive** (2 seeds per cell; 8 instances per size);
none of it is a validated finding._

## P2: energy-aware simple rules

### What was built
* **Energy-greedy (EG), `experiments/baselines.py`.**
  * Jobs are taken in decreasing minimum energy.
  * Each job goes to the feasible (machine, start) with the lowest energy cost for that job, priced with the evaluator's exact
    tariff accounting. Idle gaps are allowed.
  * It is deterministic. `None` only means the rule failed; it never claims the instance is infeasible.
* **Peak-capped greedy (PCG).**
  * The same rule under each power cap "base + maximum power of a subset of machines", including the uncapped case.
  * It keeps the cheapest result at the given ρ, so it is never worse than EG.
* **Tests (`tests/test_energy_rules.py`, 122):**
  * a hand-checked benchmark: EG gives exactly ₹785.60 at 37 kW (the energy optimum), and the rule fails under the 27 kW cap;
  * on 120 exhaustively enumerated instances the rules are feasible, respect their caps and never beat the true optimum;
  * determinism.

### Gate (all 90 cal2 instances, `results/baselines_preview/`)
**Cross-checks:**
* regenerated FCFS and SPT schedules equal the stored cal2 rows;
* no rule or B is ever below the exact optimum;
* 0 problems.

**Rule success:** EG and PCG succeeded on 90/90 instances and FCFS on 89/90. EG is energy-optimal on 16/90 instances (mean energy
gap to B 18.2 %, maximum 83.4 %).

**Decomposition at the KERC-equivalent ρ = 350/26 = ₹13.46/kW** (renegotiated contract demand). Each step is in points of FCFS
total cost:

| Subset | FCFS → EG | EG → B | B → C | Total vs FCFS | C vs B | C vs best rule (mean / median) | Best rule within 1 % of C |
|---|---|---|---|---|---|---|---|
| All 90 | 18.7 | 9.4 | 4.5 | 32.6 % | 5.8 % | 12.5 % / 9.1 % | 27 % |
| CV ≤ 0.35 (60) | 13.7 | 5.1 | 5.4 | 24.2 % | 6.4 % | 6.7 % / 3.6 % | 40 % |
| CV = 0.75, stress (30) | 28.5 | 17.7 | 2.9 | 49.1 % | 4.7 % | 24.2 % / 23.0 % | 0 % |
| Instances with a possible peak reduction (47) | 16.0 | 4.0 | 8.6 | 28.6 % | 11.2 % | 9.4 % / 3.7 % | 38 % |

**S3 rule (pre-stated):** "if the best rule is within 1 % of C on ≥ 90 % of instances at ρ_eq, exact optimisation adds little".
It is **not triggered**: 27 % overall and 40 % for CV ≤ 0.35.

**Reading:**
* Most of the gain over FCFS comes from energy-aware machine assignment.
* An exact solver adds a further 5–9 points over the simple rule (CV ≤ 0.35).
* Peak-awareness adds 5.4 points at ρ_eq (8.6 on instances where a peak reduction is possible).
* **Caveat:** these are cal2 instances with 2 seeds; a stronger rule (e.g. with local search) could narrow the gap. The main study
  will report this per cell.

## P3: scaling probe (`results/scaling_probe/`, 38 min wall)

**Setup:**
* 4 sizes on the same 32-slot shift: γ = 19/14, W {0.40, 0.625}, CV {0, 0.35}, 2 seeds = 8 instances per size;
* fresh seed 20261121 (not reused by the main study);
* cal2 budgets;
* full main-study strategy set: A, B, B_minpeak, front (including P), direct C at ρ = 14, FCFS, EG, PCG and the guard.

| Size (jobs × machines) | Required front solves proven | Complete fronts | Direct C@14 = front (where both proven) | Guard gap at ρ = 14 (max) | Solver time per instance (median / max) | **Gate 2** |
|---|---|---|---|---|---|---|
| 8 × 3 | 22/22 = **100 %** | 8/8 | 7/7 | 0 % | 23 s / 109 s | pass |
| 12 × 4 | 28/30 = **93.3 %** | 7/8 | 6/6 | 2.7 % | 46 s / 312 s | **pass (narrowly)** |
| 16 × 5 | 26/33 = 78.8 % | 6/8 | 4/4 | 5.4 % | 128 s / 387 s | fail |
| 20 × 6 | 27/45 = 60 % | 4/8 | 4/4 | 3.6 % | 196 s / 554 s | fail |

### Findings
* **Gate 2 decision (rule D2): the larger block is M₂ = 12 jobs × 4 machines.** It passes with 93.3 % against the 90 % threshold.
  **It is marginal:** with 8 instances, one more unproven solve would put it at 90 %. Its complete-front share is 7/8 (87.5 %).
* **Every unproven solve is at CV = 0.35.** All 16 CV = 0 instances have complete fronts at every size. The unproven solves are P (at
  16 × 5 and 20 × 6) and capped solves, where heterogeneous machines create many distinct peak levels. At 12 × 4 the single
  incomplete instance (`g0w1c1s000`, W 0.625, CV 0.35) has two capped solves FEASIBLE but not proven. Its break-even is therefore
  reported as an **upper bound**, and the guard's schedule is within 2.7 % of the proven lower bound.
* **The front holds up at larger sizes.** Where both are proven, front-derived C equals direct C at ρ = 14 in 21/21 instances.
  Direct C is often weaker: it is fully proven (cost and makespan) in only 11/32 instances and its cost stage in 22/32. Where direct C was unproven, the front found a
  cheaper schedule 4 times.
* **The guard always picks the front or direct C, never B or a rule.** Its schedule stays within 5.4 % of a proven lower bound at
  every size up to 20 × 6. As a **tool** the system remains usable at 20 × 6, with reported gaps; as an **exact study** it is
  limited to 12 × 4.
* **Cost estimate for the M₂ block:**
  * 60 instances (γ 19/14 × 3 W × CV {0, 0.35} × 10 seeds) ≈ 1.4 CPU-h ≈ 0.7 h wall on 2 workers;
  * basis: the mean probe time per 12 × 4 instance, 83 s;
  * the 12 × 4 time distribution is wide (25–312 s).

### Implications for P4 (SPEC-003)
* Include an M₂ = 12 × 4 block, with W levels below its threshold 3/4. Proposed: 0.40, 0.55, 0.70, to be fixed in SPEC-003 before
  any run.
* Expect some incomplete fronts at CV = 0.35. They will be counted and labelled `upper_bound` with explicit gaps, never reported
  as exact.
* 16 × 5 and 20 × 6 are **not** in the study. The report states the exact-solution limit (12 × 4 at these budgets) and the tool's
  gap behaviour up to 20 × 6.
