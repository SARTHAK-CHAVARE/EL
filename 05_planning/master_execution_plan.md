# MASTER EXECUTION PLAN
## Peak-Aware Energy-Cost Production Scheduling Under Industrial Tariff Structures

> **Version:** 1.0 — 2026-10-02  
> **Status:** PLANNING → Awaiting team review  
> **Corrections applied:** PZEM→INA226, tariff verification, demand-charge modelling, AUGMECON caveats, CP-SAT terminology, arbitrary thresholds removed.

---

# PART 1 — PROJECT FREEZE

## Final project title

**Peak-Aware Energy-Cost Production Scheduling for Small Manufacturing Systems Under Industrial Tariff Structures: A Multi-Objective Optimization Study with Physical Validation**

## Problem statement

Small manufacturing units operate under industrial electricity tariffs comprising (a) time-differentiated energy charges and (b) demand charges based on recorded peak power. Current production scheduling in these settings ignores electricity costs entirely. Energy-cost-only scheduling can reduce energy charges but may inadvertently increase peak demand, raising the total bill through demand charges. No systematic study characterises under what tariff and workload conditions peak-demand-aware scheduling provides economically meaningful benefit over energy-cost-only scheduling.

## Research question

> Under what combinations of demand-charge intensity, time-of-use tariff differential, workload intensity, and machine power heterogeneity does peak-aware multi-objective production scheduling provide a statistically significant economic benefit over energy-cost-only scheduling?

## Hypotheses

**H1 (Primary):** Peak-aware scheduling (minimising makespan + energy cost + peak demand) produces schedules with a lower simulated total electricity bill than energy-cost-only scheduling (minimising makespan + energy cost) when demand-charge intensity exceeds a threshold value. The threshold and magnitude of benefit are unknown prior to experimentation.

**H2:** The economic benefit of peak-aware scheduling increases with: (a) demand-charge rate, (b) time-of-use price differential, (c) workload intensity (ratio of total processing time to available time), and (d) machine power heterogeneity.

**H3:** Energy-cost-only scheduling does not significantly increase peak demand relative to makespan-only scheduling in all workload conditions; there exist workload conditions where it does and conditions where it does not.

**H4:** A deterministic scheduling model using measured machine power profiles (idle, processing, startup) predicts total energy consumption within an experimentally-determined error bound when validated against physical testbed measurements.

## Objectives

1. Formulate a tri-objective production scheduling model (makespan, energy cost, peak demand) using constraint programming.
2. Implement the model using OR-Tools CP-SAT and solve via ε-constraint method (AUGMECON variant).
3. Implement appropriate baseline scheduling methods (FCFS, SPT, makespan-only, energy-only).
4. Design and execute a systematic sensitivity study over demand-charge rate, ToU differential, workload intensity, and power heterogeneity.
5. Build a programmable machine-load emulation testbed and validate predicted vs. measured energy/peak.
6. Deploy the optimization workflow on a Raspberry Pi 5 and benchmark solver performance.
7. Report findings with statistical analysis, including identification of conditions under which peak-awareness is and is not beneficial.

## Scope

### In scope (CORE)

- Static/open-loop scheduling (schedule computed once, then executed)
- Deterministic processing times
- Synthetic workload instances parameterised for sensitivity analysis
- OR-Tools CP-SAT as primary solver
- ε-constraint (AUGMECON-style) multi-objective method
- Sensitivity analysis over 4 factors
- Physical testbed with 3–4 DC loads, INA226 power measurement, ESP32 control
- Raspberry Pi 5 as edge optimization platform
- Comparison against FCFS, SPT, makespan-only, and energy-cost-only baselines

### In scope (STRETCH — only after CORE is complete)

- Uncertainty analysis (Monte Carlo perturbation of processing times)
- NSGA-III for larger instances
- Rolling-horizon / adaptive rescheduling

### Out of scope

- Real factory deployment
- AC mains measurement or mains-voltage switching
- Machine learning / deep learning
- Blockchain, computer vision, chatbot / voice interface
- Real-time dynamic job arrival
- Multi-factory or supply-chain scheduling

## Expected contribution (taxonomy)

| # | Contribution | Classification |
|---|---|---|
| 1 | Tri-objective formulation (makespan + energy cost + peak demand) for production scheduling | `ENGINEERING INTEGRATION` — combines known components. The formulation uses established techniques. |
| 2 | Systematic sensitivity study: under what tariff/workload conditions does peak-awareness matter? | `EMPIRICAL CONTRIBUTION` — produces new experimental data. Not algorithmic novelty. |
| 3 | Comparison of scheduling strategies across multiple baselines | `EMPIRICAL CONTRIBUTION` — standard experimental methodology. |
| 4 | Physical validation of predicted vs. measured energy/peak on testbed | `PHYSICAL VALIDATION CONTRIBUTION` — rare in scheduling literature. |
| 5 | Deployment and benchmarking on Raspberry Pi edge platform | `ENGINEERING INTEGRATION` — demonstrates feasibility. Not a research contribution per se. |

## Assumptions

1. Processing times are deterministic (known and fixed for each instance).
2. All jobs and their operations are known at scheduling time (no dynamic arrivals).
3. Machine power draw is approximately constant during processing (verified via measurement).
4. Tariff parameters are modelled after verified Indian industrial tariff structure but parameterised for sensitivity analysis.
5. The physical testbed emulates machine behavior; it does not replicate a real factory.
6. No machine breakdowns occur during schedule execution.

## Limitations

1. Testbed scale (3–4 loads) limits physical validation to small instances.
2. Deterministic model does not capture real-world processing time variability.
3. Results are specific to the parameterised tariff structure; generalisation requires additional study.
4. DC loads do not fully represent industrial AC machinery (no power factor effects).
5. Edge solver performance is hardware-dependent.

## Terminology

| Term | Definition |
|---|---|
| Makespan ($C_{\max}$) | Completion time of the last operation across all jobs |
| Energy cost | Total (power × duration × time-slot price) for all machine activity |
| Peak demand ($P^{\text{peak}}$) | Maximum total instantaneous power across all machines over all time slots |
| Total bill | Energy cost + demand charge component (peak demand × demand-charge rate, scaled to billing period) |
| Demand charge | Fixed cost per unit of peak demand per billing period (₹/kVA/month in real tariffs) |
| ToU / ToD | Time-of-Use / Time-of-Day: time-varying electricity price |
| Pareto-efficient | A solution where no objective can be improved without worsening another |
| CP-SAT | Google OR-Tools Constraint Programming with SAT solver — a constraint programming solver, NOT a MILP solver |
| AUGMECON | Augmented ε-constraint method for multi-objective optimization |
| Machine-load emulation testbed | Physical system with controllable electrical loads representing machines |

---

# PART 2 — LITERATURE AND RESEARCH FOUNDATION

## 2.1 Topics to search

| # | Topic | Purpose |
|---|---|---|
| 1 | Energy-aware manufacturing/job-shop scheduling | Core domain |
| 2 | Multi-objective production scheduling (makespan + energy) | Baseline formulations |
| 3 | Peak demand / demand-charge-aware scheduling | Gap verification |
| 4 | Time-of-use electricity scheduling in manufacturing | Tariff-aware precedents |
| 5 | ε-constraint / AUGMECON method | Solution methodology |
| 6 | Constraint programming for scheduling (CP-SAT) | Solver methodology |
| 7 | Robust / stochastic scheduling (energy-aware) | Context (stretch) |
| 8 | Physical validation of scheduling models | Gap verification |
| 9 | Edge computing for manufacturing optimization | RPi context |
| 10 | Indian industrial tariff structure | Tariff parameterisation |
| 11 | MSME / small-manufacturer energy management | Application context |

## 2.2 Search query templates

```
"energy-aware" AND "job shop scheduling" AND ("multi-objective" OR "Pareto")
"peak demand" AND "production scheduling" AND "optimization"
"time-of-use" AND "manufacturing scheduling" AND ("MILP" OR "constraint programming")
"demand charge" AND ("scheduling" OR "peak shaving") AND "manufacturing"
"augmented epsilon-constraint" AND "scheduling"
"CP-SAT" AND "scheduling" AND "energy"
"robust scheduling" AND "processing time uncertainty" AND "energy"
"physical validation" AND "scheduling" AND "energy consumption"
"Raspberry Pi" AND "optimization" AND ("scheduling" OR "edge")
"Indian industrial tariff" AND ("ToD" OR "time-of-day" OR "demand charge")
```

## 2.3 Databases

1. **Google Scholar** — primary
2. **IEEE Xplore** — via Scholar links
3. **ScienceDirect** — EJOR, Computers & Industrial Engineering
4. **SpringerLink** — OR Spectrum, JMSY
5. **MDPI** — open access (Sustainability, Algorithms, Energies)
6. **arXiv** — preprints

## 2.4 Paper collection targets

| Category | Target | Purpose |
|---|---|---|
| Foundational (pre-2020) | 3–5 | Mouzon 2007, Gahm 2016 survey, AUGMECON (Mavrotas 2009) |
| Recent scheduling (2020–2026) | 8–12 | Current state of energy scheduling |
| Peak demand / demand charge | 3–5 | Verify gap claim |
| Physical validation | 2–3 | Confirm rarity |
| Methodology (ε-constraint, CP) | 2–3 | Solution method references |
| Tariff / policy | 2–3 | KERC orders, national ToD rules |
| **Total** | **20–30** | Sufficient for undergraduate project |

## 2.5 Literature review spreadsheet columns

```
ID | Authors | Year | Title | Venue | Model_Type | Objectives | Machines |
Uncertainty | Physical_Validation | Tariff_Type | Peak_Demand_Addressed |
Solution_Method | Instance_Size | Key_Finding | Limitation | Relevance_to_Us |
PDF_Available | Notes
```

## 2.6 Claims requiring primary/official sources

| Claim | Required source |
|---|---|
| Indian industrial tariffs include demand charges on peak kVA | KERC tariff order (official PDF) |
| ToD is mandatory for ≥10 kW consumers | MoP Electricity (Rights of Consumers) Amendment Rules, 2023 |
| Peak hours are 6–9 AM, 6–10 PM in Karnataka | KERC tariff order |
| ToD incentive/penalty is ±20% | KERC regulation or national rule |
| Demand charges are ~₹365/kVA for HT-2a | Latest KERC tariff order |

---

# PART 3 — TARIFF RESEARCH

## 3.1 Verified tariff structure (Karnataka / BESCOM / KERC)

> [!IMPORTANT]
> The values below are sourced from web-accessible summaries of KERC tariff orders (FY 2025-26, March 2026 revision). **BEFORE USING IN THE FINAL REPORT**, download and verify against the official KERC tariff order PDF from kerc.karnataka.gov.in or bescom.karnataka.gov.in.

### Consumer categories relevant to MSMEs

| Category | Description | Metering | Demand basis |
|---|---|---|---|
| **LT-5** | LT Industrial (Motive Power) | LT metering | Sanctioned load in **kW**; fixed charge per kW |
| **HT-2(a)** | HT Industrial | HT metering (≥11 kV supply) | Billing demand in **kVA** |

**For our model, HT-2(a) is the more appropriate reference** because it has explicit demand charges in ₹/kVA billed on recorded peak demand, directly analogous to our peak-demand objective. LT-5 uses fixed charges per kW of sanctioned load, not recorded peak.

### HT-2(a) tariff components (approximate FY 2025-26)

| Component | Value | Unit | Notes | Verification status |
|---|---|---|---|---|
| Demand charge | ~₹365 | per kVA per month | Billed on max of (recorded MD, ~75% of sanctioned demand) | `REQUIRES OFFICIAL PDF VERIFICATION` |
| Energy charge | ~₹6.60 | per kWh | May vary by slab | `REQUIRES VERIFICATION` |
| ToD peak surcharge | +20% | of energy charge | During peak hours | `CONSISTENT WITH NATIONAL RULE` |
| ToD off-peak rebate | −20% | of energy charge | During off-peak hours | `CONSISTENT WITH NATIONAL RULE` |
| Peak hours | 06:00–09:00, 18:00–22:00 | | 7 hours total | `REPORTED CONSISTENTLY` |
| Off-peak hours | 22:00–06:00 | | 8 hours total | `REPORTED CONSISTENTLY` |
| Normal hours | 09:00–18:00 | | 9 hours total | `INFERRED` |
| Electricity tax | 9% | of total | Additional surcharge | `REPORTED` |
| FPPCA | Variable | per kWh | Monthly fuel adjustment | `VARIABLE` |
| Power factor penalty | Surcharge if PF < 0.90 | | Additional | `REPORTED` |
| Billing period | 1 month | | | `STANDARD` |
| MD measurement | 15-min or 30-min sliding window | kVA | Highest average kVA in any window | `REPORTED` |

### How tariff maps to mathematical model

**Energy charge:**

$$\text{EnergyCost} = \sum_{t \in \mathcal{T}} \left( \sum_{m \in \mathcal{M}} P_m(t) \cdot \Delta \right) \cdot \pi_t$$

where $\pi_t$ is the ToD-adjusted price:

$$\pi_t = \begin{cases} \pi_{\text{base}} \times 1.20 & \text{if } t \in \text{Peak hours} \\ \pi_{\text{base}} \times 0.80 & \text{if } t \in \text{Off-peak hours} \\ \pi_{\text{base}} & \text{if } t \in \text{Normal hours} \end{cases}$$

**Demand charge:**

$$\text{DemandCharge} = \rho \cdot P^{\text{peak}}$$

where $\rho$ is in ₹/kW/scheduling-horizon (see §3.2).

**Total bill:**

$$\text{TotalBill} = \text{EnergyCost} + \text{DemandCharge}$$

## 3.2 Demand-charge scaling for experiments

> [!WARNING]
> Real demand charges are ₹/kVA/**month**. Our scheduling horizon is hours, not months. We cannot claim "this 8-hour experiment saves ₹X per month."

**Approach:**

1. Define a per-experiment demand-charge parameter $\rho$ with units ₹/kW (not ₹/kVA/month).
2. Sweep $\rho$ across a range including the monthly-equivalent rate and fractions of it.
3. Report: "For a demand-charge parameter of $\rho$ ₹/kW applied to the scheduling horizon, the peak-aware schedule reduces total cost by Y% vs energy-only."
4. Map to real tariff in discussion: "If the scheduling horizon covers the month's expected peak period, then $\rho = 365$ ₹/kVA (the HT-2a rate). If the schedule covers one of $N$ identical shifts, a conservative estimate is $\rho = 365/N$."

This parameterises $\rho$ and reports sensitivity rather than claiming specific monthly savings.

## 3.3 Power factor

Our DC testbed has PF = 1.0 (DC loads are purely resistive/motor). In the model we use kW directly. In real industrial settings, low PF increases kVA demand. This is a documented limitation.

---

# PART 4 — MATHEMATICAL FORMULATION

## 4.1 Modelling approach: CP-SAT with interval variables

> [!IMPORTANT]
> **Correction from previous report.** The previous report described a time-indexed MILP with binary variables $x_{omt}$. OR-Tools CP-SAT performs much better with **interval variables** and built-in scheduling constraints (`AddNoOverlap`). We reformulate using CP-SAT's native constructs.

### Sets

| Symbol | Definition |
|---|---|
| $\mathcal{J} = \{1, \ldots, n\}$ | Jobs |
| $\mathcal{O}_j = \{(j,1), \ldots, (j,n_j)\}$ | Ordered operations of job $j$ |
| $\mathcal{M} = \{1, \ldots, m\}$ | Machines |
| $\mathcal{T}_{\text{slots}}$ | Set of discrete time-slot boundaries (for energy/peak accounting) |
| $\mathcal{M}_o \subseteq \mathcal{M}$ | Eligible machines for operation $o$ |

### Parameters

| Symbol | Definition | Unit | Source |
|---|---|---|---|
| $p_o$ | Processing time of operation $o$ | integer time units | Model input |
| $P^{\text{proc}}_m$ | Power draw of machine $m$ when processing | W | Measured (INA226) |
| $P^{\text{idle}}_m$ | Power draw of machine $m$ when idle | W | Measured |
| $E^{\text{start}}_m$ | Startup energy of machine $m$ | Wh | Measured |
| $\pi_t$ | Electricity price in time slot $t$ | ₹/kWh | Tariff model |
| $\rho$ | Demand-charge parameter | ₹/kW | Parameterised |
| $d_j$ | Deadline for job $j$ | time units | Optional |
| $H$ | Scheduling horizon | time units | Derived |

### Decision variables (CP-SAT interval formulation)

For each operation $o$ (with duration $p_o$):

| Variable | CP-SAT type | Meaning |
|---|---|---|
| $\text{start}_o$ | `NewIntVar(0, H)` | Start time of operation $o$ |
| $\text{end}_o$ | `NewIntVar(0, H)` | End time of operation $o$ |
| $\text{interval}_o$ | `NewIntervalVar(start, p_o, end)` | Interval representation |

For flexible job-shop (operation assignable to multiple machines):

| Variable | CP-SAT type | Meaning |
|---|---|---|
| $\text{mchoice}_{o,m}$ | `NewBoolVar()` | 1 if $o$ assigned to machine $m$ |
| $\text{opt\_interval}_{o,m}$ | `NewOptionalIntervalVar(...)` | Optional interval per candidate |

For time-slot accounting:

| Variable | CP-SAT type | Meaning |
|---|---|---|
| $\text{load}_{m,t}$ | `NewBoolVar()` | 1 if machine $m$ is processing during slot $t$ |
| $\text{slot\_power}_t$ | `NewIntVar(0, ...)` | Total power in slot $t$ (watts, integer) |
| $P^{\text{peak}}$ | `NewIntVar(0, ...)` | Maximum of all $\text{slot\_power}_t$ |

### Objective functions

**F1 — Makespan:**
$$\min\ C_{\max} = \max_{j} \text{end}_{(j, n_j)}$$

CP-SAT: `model.AddMaxEquality(makespan, [end_vars of last operations])`

**F2 — Energy cost:**

$$\text{EnergyCost} = \sum_{t} \text{slot\_power}_t \cdot \Delta \cdot \pi_t \cdot 10^{-3}$$

Since CP-SAT works with integers, multiply all costs by a scaling factor (e.g., 1000) to avoid floating-point.

**F3 — Peak demand:**
$$\min\ P^{\text{peak}} = \max_{t} \text{slot\_power}_t$$

CP-SAT: `model.AddMaxEquality(peak_power, slot_power_vars)`

### Constraints

**C1 — Precedence:** Operations within a job must execute in order.
```python
for j in jobs:
    for k in range(len(j.operations) - 1):
        model.Add(start[j,k+1] >= end[j,k])
```
*Each operation starts after its predecessor finishes.*

**C2 — Machine non-overlap:** At most one operation on each machine at any time.
```python
for m in machines:
    model.AddNoOverlap(intervals_on_machine[m])
```
*No two operations on the same machine can overlap.*

**C3 — Assignment (flexible job-shop):** Each operation assigned to exactly one eligible machine.
```python
for o in operations:
    model.AddExactlyOne(mchoice[o, m] for m in eligible[o])
```

**C4 — Time-slot power accounting:** For each slot $t$ and machine $m$, determine if $m$ is processing.

This requires channelling constraints between interval variables and boolean slot variables. For each operation $o$ on machine $m$, if $o$'s interval overlaps slot $t$:

```python
# For each slot t (covering [t*delta, (t+1)*delta)):
# load[m,t] = 1 iff some operation on m overlaps slot t
# This uses reification and interval overlap logic
```

**Implementation note:** This is the most complex part. Two approaches:
1. **Element-based:** For each slot, check if start ≤ t*delta and end > t*delta.
2. **Cumulative-based:** Use `AddCumulative` with capacity 1 per machine and energy demands linked to intervals.

Start with approach 1 for clarity; optimise if slow.

**C5 — Slot power summation:**
```python
for t in slots:
    model.Add(slot_power[t] == sum(load[m,t] * P_proc[m] for m in machines))
```
*Total power in slot $t$ equals sum of processing power of all active machines.*

**C6 — Peak demand:**
```python
for t in slots:
    model.Add(peak_power >= slot_power[t])
```
*Peak power must be at least as large as power in any slot.*

**C7 — Makespan:**
```python
for j in jobs:
    model.Add(makespan >= end[j, last_op[j]])
```

**C8 — Deadline (optional):**
```python
for j in jobs:
    if deadline[j] is not None:
        model.Add(end[j, last_op[j]] <= deadline[j])
```

### Model hierarchy

| Model | Objectives | Constraints | Purpose |
|---|---|---|---|
| M0: Makespan-only | min $C_{\max}$ | C1, C2, C3, C7 | Baseline |
| M1: Energy-only | min EnergyCost | C1, C2, C3, C4, C5, C7 | Baseline |
| M2: Bi-objective | min {$C_{\max}$, EnergyCost} via ε-constraint | C1–C5, C7 | Comparison |
| **M3: Tri-objective** | **min {$C_{\max}$, EnergyCost, $P^{\text{peak}}$}** | **C1–C7** | **Proposed** |

### Assumptions stated honestly

| Assumption | Realistic? | If violated | Mitigation |
|---|---|---|---|
| Deterministic processing times | No (±10-30% in reality) | Schedule may miss deadlines | Document; stretch: uncertainty study |
| Constant $P^{\text{proc}}_m$ during processing | Approximately yes for steady-state loads | Energy estimate error | Use measured average; report error |
| No machine breakdowns | Unrealistic long-term | Schedule becomes infeasible | Excluded; acknowledge |
| Jobs known in advance | Yes for batch production | N/A | Appropriate for MSME batch |
| Piecewise-constant tariff | Yes — Indian ToD tariffs are block rates | N/A | Matches real structure |
| PF = 1 (DC testbed) | No (real machines have PF < 1) | kW ≠ kVA | Document as limitation |

---

# PART 5 — OPTIMIZATION METHOD

## 5.1 Method comparison

| Method | Multi-obj? | Non-convex Pareto? | Guarantees | Solves needed | Feasibility |
|---|---|---|---|---|---|
| Weighted sum | Yes | **No** — misses non-convex regions | Optimal per weight | 1 per weight combo | Easy |
| ε-constraint | Yes | **Yes** | Optimal per ε (if solver proves optimal) | 1 per ε | Easy |
| AUGMECON | Yes | **Yes** | Pareto-efficient (not weakly dominated) if solver optimal | k² for 3-obj | Moderate |
| NSGA-II/III | Yes | Yes | No optimality guarantee | Population × generations | Moderate |
| CP-SAT direct | Single | N/A | Proves optimality or reports gap | 1 | Easy |

## 5.2 Selected: ε-constraint via CP-SAT (AUGMECON-style)

### What AUGMECON guarantees (precisely)

> [!WARNING]
> AUGMECON guarantees that every returned solution is **Pareto-efficient** (not weakly dominated) — **IF the underlying solver finds the true global optimum for each sub-problem.** If the solver returns sub-optimal solutions (e.g., due to time limits), the guarantees weaken: solutions are feasible and high-quality but not provably Pareto-efficient. Always report solver status and optimality gap.

### ε-constraint workflow (pseudocode)

```
INPUT: instance I, grid sizes k1, k2
OUTPUT: Pareto-efficient solution set S

# Step 1: Find anchor points
C_max_min = solve(min C_max, subject to C1-C3,C7)
EC_min    = solve(min EnergyCost, subject to C1-C5,C7)
PP_min    = solve(min P_peak, subject to C1-C7)

C_max_max = max(C_max across individual optima)
EC_max    = max(EC across individual optima)
PP_max    = max(PP across individual optima)

# Ranges
r1 = C_max_max - C_max_min   # makespan range
r2 = PP_max - PP_min          # peak power range

# Step 2: ε-grid over makespan and peak power
S = empty set
for i = 0 to k1:
    eps_cmax = C_max_min + i * r1 / k1
    for j = 0 to k2:
        eps_pp = PP_min + j * r2 / k2

        # Step 3: Sub-problem (AUGMECON formulation)
        # Primary: min EnergyCost - delta*(s1/r1 + s2/r2)
        # Subject to:
        #   C_max <= eps_cmax + s1   (s1 >= 0, surplus variable)
        #   P_peak <= eps_pp + s2    (s2 >= 0, surplus variable)
        #   all scheduling constraints C1-C7
        # delta = small (e.g., 1e-3 * EC_range)

        result = solve_augmecon_subproblem(eps_cmax, eps_pp)
        if result.status in [OPTIMAL, FEASIBLE]:
            S.add(result.solution)

# Step 4: Filter dominated solutions
S = remove_dominated(S)

RETURN S
```

### Key implementation details

- **Grid size:** Start with k1 = k2 = 10 (100 sub-problems). Increase if Pareto surface is sparse.
- **Solver time limit per sub-problem:** Do NOT pre-specify. Start with pilot runs on 2–3 instances to determine typical solve time. Set limit to 2× median solve time.
- **Objective scaling for AUGMECON:** Surplus variables $s_1$, $s_2$ are scaled by objective ranges $r_1$, $r_2$.
- **Integer scaling:** CP-SAT uses integers. Multiply energy cost by 1000 to preserve 3 decimal places.
- **Infeasibility:** If sub-problem infeasible (ε too tight), skip. Record as infeasible cell.
- **Solver seed:** `solver.parameters.random_seed = 42` for reproducibility.

---

# PART 6 — SOFTWARE ARCHITECTURE

## 6.1 Folder structure

```
energy_scheduling/
├── README.md
├── requirements.txt
├── config/
│   ├── default_config.yaml
│   └── tariff_profiles/
│       ├── bescom_ht2a.yaml
│       └── parametric.yaml
├── data/
│   ├── instances/
│   │   ├── small/                 # 5x3
│   │   ├── medium/                # 8x4
│   │   └── large/                 # 10x5, 15x6
│   └── measured/
│       ├── machine_profiles.csv
│       └── calibration_logs/
├── src/
│   ├── __init__.py
│   ├── model/
│   │   ├── __init__.py
│   │   ├── instance.py            # Data classes
│   │   ├── tariff.py              # Tariff model
│   │   └── solution.py            # Schedule solution
│   ├── solver/
│   │   ├── __init__.py
│   │   ├── cpsat_model.py         # CP-SAT model builder
│   │   ├── epsilon_constraint.py  # AUGMECON loop
│   │   └── baselines.py           # FCFS, SPT dispatchers
│   ├── evaluation/
│   │   ├── __init__.py
│   │   ├── metrics.py             # Cost, peak, makespan, bill
│   │   ├── pareto.py              # Dominance, hypervolume
│   │   └── statistics.py          # Wilcoxon, Friedman
│   ├── generators/
│   │   ├── __init__.py
│   │   └── instance_generator.py
│   └── visualization/
│       ├── __init__.py
│       ├── gantt.py
│       ├── pareto_plot.py
│       ├── sensitivity_plot.py
│       └── power_trace.py
├── experiments/
│   ├── exp_a_baseline.py
│   ├── exp_b_biobj_pareto.py
│   ├── exp_c_triobj_vs_biobj.py
│   ├── exp_d_demand_charge.py
│   ├── exp_e_tod_sensitivity.py
│   ├── exp_f_workload.py
│   ├── exp_g_heterogeneity.py
│   ├── exp_h_scalability.py
│   ├── exp_i_model_fidelity.py
│   ├── exp_j_physical.py
│   └── run_all.py
├── hardware/
│   ├── esp32/
│   │   └── firmware.ino
│   ├── calibration/
│   │   └── calibrate.py
│   └── testbed_controller.py
├── deployment/
│   ├── rpi_setup.sh
│   └── benchmark.py
├── results/
│   ├── raw/
│   ├── processed/
│   └── plots/
└── tests/
    ├── test_model.py
    ├── test_solver.py
    ├── test_baselines.py
    └── test_metrics.py
```

## 6.2 Key data class: `src/model/instance.py`

```python
from dataclasses import dataclass, field

@dataclass
class Operation:
    job_id: int
    op_index: int
    eligible_machines: list[int]
    processing_time: int  # integer time units

@dataclass
class Machine:
    machine_id: int
    power_processing_w: float
    power_idle_w: float
    startup_energy_wh: float

@dataclass
class TariffSlot:
    slot_index: int
    price_per_kwh: float  # ₹/kWh, ToD-adjusted

@dataclass
class Instance:
    name: str
    jobs: list[list[Operation]]
    machines: list[Machine]
    tariff_slots: list[TariffSlot]
    demand_charge_rate: float  # rho, ₹/kW
    time_slot_width_hours: float
    horizon: int
    deadlines: dict[int, int] | None = None
    seed: int = 0
```

## 6.3 Input/output CSV formats

**Instance CSV:** See Part 7 for specification.

**Results CSV columns:**
```
experiment_id, instance_name, method, makespan, energy_cost, peak_power_w,
total_bill, solve_time_s, solver_status, optimality_gap, seed, timestamp
```

---

# PART 7 — DATA MODEL

## 7.1 Instance parameters

| Parameter | Small | Medium | Large |
|---|---|---|---|
| Jobs ($n$) | 5 | 8 | 10–15 |
| Machines ($m$) | 3 | 4 | 5–6 |
| Ops per job | 2–3 | 2–4 | 3–5 |
| Processing times | U(1, 6) | U(1, 8) | U(1, 10) |
| Machine eligibility | 1–2 per op | 1–3 | 1–3 |
| Power (processing, W) | Depends on heterogeneity level | | |
| Time slot width | 1 unit (maps to 15 min in model, 15 sec in testbed) | | |
| Horizon | 48 slots | 64 slots | 96 slots |

## 7.2 Power heterogeneity levels

| Level | $P^{\text{proc}}$ range (W) | Meaning |
|---|---|---|
| Low | U(100, 150) | All machines similar |
| Medium | U(50, 250) | Moderate spread |
| High | U(30, 400) | One machine 13× another |

## 7.3 Workload intensity

$$\lambda = \frac{\sum_o p_o}{m \times H}$$

| Level | $\lambda$ | Meaning |
|---|---|---|
| Light | 0.3 | Plenty of slack |
| Moderate | 0.5 | Some scheduling freedom |
| Heavy | 0.7 | Tight |
| Very heavy | 0.9 | Very little room |

Adjust processing times or horizon to achieve target $\lambda$.

## 7.4 Reproducibility

- 20 instances per (size, heterogeneity, intensity) combination
- Seeds: 1000, 1001, ..., 1019
- All instances saved as CSV with full metadata
- Generator script is deterministic given seed

---

# PART 8 — BASELINES

| ID | Method | Algorithm | Objective optimised | Implementation |
|---|---|---|---|---|
| B0 | FCFS | Schedule operations in job order. Assign to first available eligible machine. | None (arrival order) | Greedy dispatcher |
| B1 | SPT | Sort all operations by shortest processing time. Assign to earliest-available eligible machine. | Heuristic: reduce flow time | Greedy dispatcher |
| B2 | Makespan-only | CP-SAT: min $C_{\max}$ subject to C1, C2, C3, C7. | min makespan | CP-SAT |
| B3 | Energy-only | CP-SAT: min EnergyCost subject to C1–C5, C7. | min energy cost | CP-SAT |
| P1 | Bi-objective | ε-constraint: min {$C_{\max}$, EnergyCost}. | Pareto front (2D) | ε-constraint |
| P2 | Tri-objective | ε-constraint: min {$C_{\max}$, EnergyCost, $P^{\text{peak}}$}. | Pareto surface (3D) | AUGMECON |

**Essential:** B0, B1, B2, B3, P1, P2.

---

# PART 9 — EXPERIMENTAL DESIGN

## Experiment A — Baseline comparison (CORE)

- **RQ:** How do FCFS, SPT, makespan-only, energy-only compare on all metrics?
- **IV:** Scheduling method (B0, B1, B2, B3)
- **DV:** Makespan, energy cost, peak power, total bill
- **Controlled:** 20 medium instances (8×4), BESCOM reference tariff, $\rho$ = reference
- **Statistical test:** Friedman test + post-hoc Nemenyi
- **Plots:** Box plots per metric per method

## Experiment B — Bi-objective Pareto front (CORE)

- **RQ:** What is the shape of the makespan–energy-cost Pareto front?
- **IV:** ε (makespan bound)
- **DV:** Energy cost, peak power (observed), total bill
- **Instances:** 10 medium
- **Key analysis:** Does peak power change as you move along the front? If yes → coupled. If no → independent.

## Experiment C — Tri-obj vs bi-obj (CORE)

- **RQ:** Does adding peak demand as a 3rd objective produce different Pareto-efficient schedules?
- **IV:** Model (P1 vs P2)
- **DV:** Total bill (Common Evaluation Space — see Part 10)
- **Instances:** 20 medium
- **Test:** Wilcoxon signed-rank on best-bill from each Pareto set

## Experiment D — Demand-charge sensitivity (CORE)

- **RQ:** How does benefit of peak-awareness change with $\rho$?
- **IV:** $\rho \in \{0, 25, 50, 100, 150, 200, 300, 400, 500\}$ ₹/kW
- **DV:** Total bill difference (P1 best-bill vs P2 best-bill)
- **Instances:** 10 medium
- **Plots:** Savings vs $\rho$ curve
- **Expected:** Benefit increases with $\rho$; at $\rho = 0$, no difference

## Experiment E — ToD sensitivity (CORE)

- **RQ:** How does peak/off-peak price ratio affect benefit?
- **IV:** Peak multiplier ∈ {1.0, 1.05, 1.10, 1.15, 1.20, 1.30, 1.50, 2.0}
- **DV:** Energy cost savings, total bill savings
- **Instances:** 10 medium
- **Plots:** Savings vs multiplier

## Experiment F — Workload intensity (CORE)

- **RQ:** Does utilisation affect peak-aware scheduling benefit?
- **IV:** $\lambda \in \{0.3, 0.5, 0.7, 0.9\}$
- **DV:** Peak power, total bill
- **Instances:** 10 per level
- **Hypothesis:** Higher $\lambda$ → more machine overlap → higher peak → more benefit

## Experiment G — Machine power heterogeneity (CORE)

- **RQ:** Does heterogeneity in power draw affect benefit?
- **IV:** Heterogeneity level: low, medium, high
- **DV:** Peak power variance, total bill
- **Instances:** 10 per level

## Experiment H — Scalability (CORE: laptop; STRETCH: RPi)

- **RQ:** At what size does CP-SAT fail to find good solutions within time limits?
- **IV:** Size: 5×3, 8×4, 10×5, 12×5, 15×6
- **DV:** Solve time, optimality gap, Pareto points
- **Platform:** Laptop AND RPi 5

## Experiment I — Model fidelity (CORE — physical)

- **RQ:** How accurately does the model predict energy and peak?
- **IV:** Schedule variant (FCFS, optimised)
- **DV:** Prediction error (energy, peak)
- **Procedure:** 5 schedules × 3 repetitions on testbed
- **Metrics:** MAE, RMSE, relative error
- **Acceptance:** Error characterised relative to measurement uncertainty (see Part 15)

## Experiment J — Physical validation (CORE — physical)

- **RQ:** Does the optimised schedule produce lower measured cost/peak than FCFS on the testbed?
- **IV:** Schedule: FCFS vs optimised
- **DV:** Measured energy, measured peak, execution time
- **Repetitions:** 3 per schedule

---

# PART 10 — PARETO ANALYSIS

## 10.1 The comparison problem

Comparing a 2-objective Pareto front (P1) against a 3-objective Pareto surface (P2) using raw hypervolume is invalid — they live in different objective spaces.

## 10.2 Solution: Common Evaluation Space

Both P1 and P2 produce *schedules*. Every schedule has values for ALL three objectives (makespan, energy cost, peak power) even if peak was not optimised by P1.

1. Evaluate ALL P1 and P2 solutions on the SAME 3 metrics.
2. Compute total bill: $\text{Bill} = \text{EC} + \rho \cdot P^{\text{peak}}$.
3. For each instance, compare best-bill from P1 vs best-bill from P2.
4. Hypervolume in 3D: compute HV for P1 solutions (in 3D) vs P2 solutions (in 3D) using same reference point.

## 10.3 Metrics

| Metric | Use |
|---|---|
| Best-bill | Primary comparison |
| Hypervolume (3D, normalised) | Pareto approximation quality |
| Spacing | Distribution |
| Number of Pareto points | Coverage |

## 10.4 Normalisation

Each objective normalised to [0, 1] using global min/max across ALL solutions (P1 ∪ P2) per instance. Reference point: (1.1, 1.1, 1.1).

---

# PART 11 — SENSITIVITY / PHASE-MAP STUDY

## 11.1 Factor grid

| Factor | Symbol | Levels |
|---|---|---|
| Demand-charge rate | $\rho$ | {0, 50, 100, 200, 365, 500} ₹/kW |
| ToD multiplier | $\alpha$ | {1.0, 1.1, 1.2, 1.3, 1.5} |
| Workload intensity | $\lambda$ | {0.3, 0.5, 0.7, 0.9} |
| Power heterogeneity | $\sigma$ | {low, medium, high} |

Full factorial: 6 × 5 × 4 × 3 = 360 cells, 5 instances each → 1,800 runs per model.

If too many: use a reduced design (fix $\lambda$ = 0.7, $\sigma$ = medium, sweep $\rho$ × $\alpha$ first → 30 cells × 5 = 150 runs. Expand later.).

## 11.2 Metric per cell

$$\Delta\text{Bill}(\%) = \frac{\text{BestBill}_{P1} - \text{BestBill}_{P2}}{\text{BestBill}_{P1}} \times 100$$

## 11.3 Visualisation

- 2D heatmap of $\Delta\text{Bill}(\%)$ vs ($\rho$, $\alpha$) at fixed ($\lambda$, $\sigma$)
- Contour line where $\Delta\text{Bill} = 0$ — "phase boundary"
- Slice plots for each factor

## 11.4 Evidence criteria

- **For H1:** A region where $\Delta\text{Bill} > 0$ consistently AND a region where ≈ 0, with clear boundary.
- **Against H1:** $\Delta\text{Bill} ≈ 0$ everywhere (peak-awareness never helps) — valid negative result.
- **Trivial support:** Benefit only at extreme unrealistic parameters.

---

# PART 12 — HARDWARE ARCHITECTURE

## 12.1 Measurement correction

> [!IMPORTANT]
> **PZEM-004T is an AC measurement device. It cannot measure DC power.** Our testbed uses 12V DC loads. We use **INA226** modules (I²C, 16-bit, DC) instead.

### Component table

| Component | Purpose | Interface | Notes |
|---|---|---|---|
| **INA226** (×3) | DC V/I/P measurement per load | I²C to ESP32 | 16-bit, ~±0.1%, 0–36V, up to 3.2A |
| **ESP32-WROOM-32** | Controller + I²C + relay + WiFi | GPIO, I²C, WiFi | |
| **4-channel relay module** | Load switching | GPIO | 5V coil, switches 12V |
| **12V DC loads** | Machine emulators | Relay-switched | |
| **12V 10A SMPS** | Power for loads | Mains (enclosed unit) | **Students do NOT open** |
| **Raspberry Pi 5** (borrowed) | Optimization server | WiFi | |

### Block diagram

```
┌─────────────── 12V DC Supply (enclosed) ──────────────────┐
│                                                            │
├──→ Relay 1 ──→ INA226(0x40) ──→ Load 1 (Motor, ~24W) ──→ GND
├──→ Relay 2 ──→ INA226(0x41) ──→ Load 2 (Heater, ~40W) ──→ GND
├──→ Relay 3 ──→ INA226(0x44) ──→ Load 3 (LED, ~12W) ──→ GND
│
│   ┌──────────┐  I²C (SDA/SCL)  ┌──────────────────────────┐
│   │  ESP32   │◄───────────────►│ INA226 × 3 (shared bus)  │
│   │          │  GPIO           └──────────────────────────┘
│   │          │──────────────────→ Relay Module (4ch)
│   │          │  WiFi/MQTT
│   │          │◄──────────────────────► Raspberry Pi 5
│   └──────────┘
```

### I²C addresses

- INA226 #1: A0=GND, A1=GND → 0x40
- INA226 #2: A0=VS, A1=GND → 0x41
- INA226 #3: A0=GND, A1=VS → 0x44

### Safety

- ALL loads are 12V DC. No mains on breadboard.
- 12V supply is enclosed commercial unit — not opened or modified.
- Max total current ~8A, within 10A supply rating.
- Relay module provides galvanic isolation (ESP32 3.3V ↔ load 12V).

## 12.2 BOM

| Component | Qty | ₹/unit | Total ₹ |
|---|---|---|---|
| ESP32-WROOM-32 DevKit | 1 | 500 | 500 |
| INA226 breakout | 3 | 180 | 540 |
| 4-channel relay module | 1 | 200 | 200 |
| DC motor (775, 12V) | 1 | 250 | 250 |
| Ceramic heater (12V, 40W) | 1 | 100 | 100 |
| LED strip (12V, 1m) | 1 | 150 | 150 |
| 12V 10A SMPS | 1 | 350 | 350 |
| Breadboard + wires | 1 | 200 | 200 |
| **Total** | | | **₹2,290** |
| Raspberry Pi 5 (borrowed) | 1 | — | 0 |

---

# PART 13 — PHYSICAL TESTBED

## 13.1 Load-to-machine mapping

| Load | Machine | Expected P_proc | Notes |
|---|---|---|---|
| DC Motor (775) | M1 | ~24W | Motor-type process |
| Ceramic heater (12V) | M2 | ~40W | Thermal process |
| LED strip (12V) | M3 | ~12W | Light-duty process |

## 13.2 Operation mapping

One "processing operation" = relay ON for $p_o$ time units. Time unit = 15 seconds (physical demo).

## 13.3 What it proves / does not prove

| Can demonstrate | Cannot demonstrate |
|---|---|
| Energy model predicts measured energy within quantified error | Works on real industrial machines |
| Optimised schedule physically executes correctly | Monthly demand charge savings |
| Peak power matches prediction | Scales to factory size |
| Observable difference between FCFS and optimised | System works unsupervised |

---

# PART 14 — CALIBRATION PROTOCOL

For each load:

**Step 1: Steady-state power.** Turn ON. Wait 5s. Sample INA226 at 10 Hz for 60s. Record mean(P), std(P).

**Step 2: Idle power.** If modelled: apply idle config. Sample 60s. Record.

**Step 3: Startup energy.** Record OFF→ON transient. Integrate power until stable (within 5%). Repeat 5×. Report mean, variance.

**Step 4: Repeat** on 3 occasions. Report overall mean, std, CoV.

**Output:** `data/measured/machine_profiles.csv`:
```csv
machine_id,P_proc_mean_W,P_proc_std_W,P_idle_mean_W,P_idle_std_W,E_start_mean_Wh,E_start_std_Wh,n_trials,date
```

---

# PART 15 — SIMULATION ↔ HARDWARE VALIDATION

## Metrics

| Metric | Formula |
|---|---|
| Energy relative error | $\|E_{\text{pred}} - E_{\text{meas}}\| / E_{\text{meas}}$ |
| Peak relative error | $\|P^{\text{peak}}_{\text{pred}} - P^{\text{peak}}_{\text{meas}}\| / P^{\text{peak}}_{\text{meas}}$ |
| Power trace MAE | $\frac{1}{T}\sum_t \|P_{\text{pred}}(t) - P_{\text{meas}}(t)\|$ |
| Power trace RMSE | $\sqrt{\frac{1}{T}\sum_t (P_{\text{pred}}(t) - P_{\text{meas}}(t))^2}$ |

## Acceptance

Do NOT pre-specify thresholds. Instead:
1. Calibration uncertainty (Part 14) sets the measurement floor.
2. If calibration shows ±5% power variability → prediction error <10% is reasonable.
3. Report BOTH the error AND the measurement uncertainty.

---

# PART 16 — RASPBERRY PI DEPLOYMENT

## Software

```bash
# Raspberry Pi OS Lite 64-bit (Bookworm)
sudo apt update && sudo apt install -y python3-pip python3-venv mosquitto
python3 -m venv ~/env && source ~/env/bin/activate
pip install ortools numpy pandas paho-mqtt pyyaml matplotlib
```

## Benchmark

Solve same instances on laptop and RPi 5. Report speedup ratio = time(RPi)/time(laptop).

This is an **engineering/deployment evaluation**, not research novelty.

---

# PART 17 — END-TO-END WORKFLOW

```
1. Generate instance → CSV
2. Load instance + tariff config → Instance object
3. Run baselines (B0–B3) → schedules + metrics → CSV
4. Run bi-objective ε-constraint (P1) → Pareto front → CSV
5. Run tri-objective AUGMECON (P2) → Pareto surface → CSV
6. Evaluate ALL solutions in Common 3D Space → total bill → CSV
7. [Physical] Select FCFS + optimised schedule
8. [Physical] RPi → MQTT → ESP32 → execute → INA226 → measure
9. [Physical] Compare predicted vs measured → validation metrics
10. Aggregate across instances → statistical tests → plots
11. Generate sensitivity heatmaps → phase maps
```

---

# PART 18 — FAILURE MODES

| # | Symptom | Cause | Fix | Fallback |
|---|---|---|---|---|
| 1 | CP-SAT INFEASIBLE | ε too tight | Skip cell; expected near Pareto boundary | Normal |
| 2 | CP-SAT timeout | Instance too large | Increase time limit; reduce size | Report gap |
| 3 | Few Pareto points | Grid too coarse; objectives not conflicting | Finer grid; verify formulation | Report sparse front |
| 4 | All methods same bill | $\rho$ too low; tariff flat | Valid result | Report "no benefit" |
| 5 | INA226 reads 0 | Wiring error; wrong address | I²C scan; check wiring | Swap module |
| 6 | Relay won't switch | GPIO issue; needs 5V logic | Level shifter or transistor | MOSFET switch |
| 7 | MQTT drops | WiFi; Mosquitto down | Check service; serial fallback | Direct serial |
| 8 | Measured ≫ predicted | Load draws more than calibrated | Recalibrate | Update model |
| 9 | Measured ≪ predicted | Load partial; relay intermittent | Check connections | Replace load |
| 10 | RPi too slow | ARM limitations | Reduce instance size | Report as limit |
| 11 | Timing drift | ESP32 millis() drift | Hardware timer; NTP sync | Document error |
| 12 | Supply overloaded | All loads simultaneous | Check total; stagger | Higher-rated supply |
| 13 | Wrong constraints | Bug in CP-SAT model | Verify on 2×2 by hand | Test suite |
| 14 | Trivial instances | Too much slack | Check $\lambda$; adjust | Regenerate |

---

# PART 19 — REPRODUCIBILITY

## Git structure

```
energy-scheduling/
├── .gitignore          # __pycache__, .env, results/raw/
├── README.md           # Setup, run, reproduce
├── requirements.txt    # Pinned versions
├── config/             # Committed
├── data/instances/     # Committed (generated, deterministic)
├── data/measured/      # Committed (calibration data)
├── src/                # Committed
├── experiments/        # Committed
├── hardware/           # Committed
├── tests/              # Committed
├── results/            # .gitignore (use releases for data)
└── docs/               # Committed
```

## Checklist

- [ ] `requirements.txt` with pinned versions
- [ ] Random seeds in instance files
- [ ] CP-SAT seed: `solver.parameters.random_seed = 42`
- [ ] All instances committed
- [ ] README: clone → install → run
- [ ] Hardware BOM, wiring, firmware committed
- [ ] Calibration data committed
- [ ] Raw results as CSV with experiment ID + timestamp

---

# PART 20 — PROJECT TIMELINE

## 20.1 One-week emergency plan

| Day | Task | Output |
|---|---|---|
| 1 | Install OR-Tools. Implement data classes. Build 3 test instances by hand. | Python env; 3 CSVs |
| 2 | Implement M0 (makespan-only CP-SAT). Verify on 2×2 by hand. | Working solver |
| 3 | Add energy cost (M1). Add FCFS/SPT. First comparison table. | B0, B1, M0, M1 |
| 4 | Implement ε-constraint for bi-obj (P1). Generate Pareto front. | 2D Pareto plot |
| 5 | Add peak demand (M3). Tri-objective loop (P2). | 3D Pareto points |
| 6 | Instance generator. 20 medium instances. Run Exp A. | Baseline results |
| 7 | Run Exp C (P1 vs P2). First sensitivity (Exp D, 3 values of $\rho$). | Core results draft |

## 20.2 Four-week realistic plan

| Week | Focus | Deliverables |
|---|---|---|
| 1 | Software: M0–M3, B0–B3, P1, P2, instance generator, tests | Working system. Verified on small instances. |
| 2 | Experiments A–E. Statistical analysis. Plots. | Results CSVs. Preliminary analysis. |
| 3 | Hardware: order → assemble → calibrate → validate model. | Testbed. Calibration data. Exp I, J. |
| 4 | Experiments F–G. Phase-map. RPi deploy + benchmark. Report. | Complete results. Heatmaps. Draft report. |

## 20.3 Eight-week complete plan

| Week | Focus | Deliverables |
|---|---|---|
| 1 | Literature review. Tariff verification. KERC PDF. | Lit spreadsheet. Tariff doc. |
| 2 | Core software. Instance generator. Unit tests. | Working M0–M3, baselines, 60 instances. |
| 3 | ε-constraint. Pareto code. Visualisation. | P1, P2. Pareto plots. |
| 4 | Experiments A–C. | Baseline comparison. Bi vs tri. |
| 5 | Experiments D–G. Phase-map. | Sensitivity plots. Heatmaps. |
| 6 | Hardware: order, assemble, calibrate. | Testbed. Calibration log. |
| 7 | Physical validation (Exp I, J). RPi deploy + benchmark. | Validation. RPi results. |
| 8 | Report. Poster. Final polish. | Complete deliverables. |

### Critical path

```
Tariff verify (W1) → Formulation (W1) → CP-SAT (W2) → ε-constraint (W3)
→ Experiments A–C (W4) → Sensitivity (W5) → Report (W8)

[Parallel:] Hardware order (W2) → Assemble (W6) → Calibrate (W6) → Validate (W7)
```

---

# PART 21 — DEFINITION OF DONE

- [ ] Tariff verified against official KERC PDF (downloaded, cited)
- [ ] Formulation documented, all symbols defined, verified by hand on 2×2
- [ ] CP-SAT solves M0, M1, M2, M3 correctly
- [ ] ε-constraint produces Pareto front (2D) and surface (3D)
- [ ] Baselines (FCFS, SPT, makespan-only, energy-only) correct
- [ ] Instance generator creates reproducible instances
- [ ] Experiment A complete with statistical test
- [ ] Experiment C complete with Common Evaluation Space
- [ ] Experiment D complete with savings-vs-ρ plot
- [ ] Experiment E complete
- [ ] Experiment F complete
- [ ] Phase-map produced (at least ρ × α heatmap)
- [ ] Physical testbed assembled and powered
- [ ] Calibration complete with uncertainty
- [ ] Experiment I: prediction error reported with uncertainty
- [ ] Experiment J: FCFS vs optimised on testbed
- [ ] RPi deployment working
- [ ] RPi benchmark reported
- [ ] All results saved as CSV
- [ ] All plots generated
- [ ] Limitations documented honestly
- [ ] Novelty claims match Part 1 taxonomy
- [ ] Code committed with README + requirements.txt
- [ ] Report complete

---

# PART 22 — START HERE

The first 10 concrete actions to begin immediately.

---

### Action 1: Install OR-Tools and verify

**Task:** Install Python dependencies.

```bash
pip install ortools numpy pandas pyyaml matplotlib scipy
python -c "from ortools.sat.python import cp_model; print('CP-SAT OK')"
```

**Output:** No errors. CP-SAT imports.
**Done when:** Import succeeds.

---

### Action 2: Create project directory structure

**Task:** Create folders from Part 6.1. Initialise Git.

```bash
mkdir -p energy_scheduling/{config/tariff_profiles,data/{instances/{small,medium,large},measured/calibration_logs},src/{model,solver,evaluation,generators,visualization},experiments,hardware/{esp32,calibration},deployment,results/{raw,processed,plots},tests,docs}
cd energy_scheduling && git init
```

**Output:** Full directory tree. `.git/` exists.
**Done when:** `find . -type d` shows all directories.

---

### Action 3: Implement Instance data model

**Task:** Create `src/model/instance.py` with dataclasses from Part 6.2. Create `src/model/tariff.py` with `build_tariff_slots()`.

**Output:** Two .py files that import without error.
**Done when:** `python -c "from src.model.instance import Instance"` works.

---

### Action 4: Build a 2×2 test instance by hand

**Task:** Create `data/instances/small/test_2x2.csv`: 2 jobs, 2 machines, 2 operations per job. Compute optimal makespan on paper. Draw the Gantt chart.

**Output:** CSV file + hand-computed answer written in `docs/verification_notes.md`.
**Done when:** You can explain the optimal makespan and why.

---

### Action 5: Implement makespan-only CP-SAT model (M0)

**Task:** Create `src/solver/cpsat_model.py`. Implement interval variables, precedence, NoOverlap, makespan objective. Solve `test_2x2`.

**Output:** Solver returns makespan matching hand calculation.
**Done when:** Optimal makespan matches paper answer.

---

### Action 6: Implement FCFS and SPT baselines

**Task:** Create `src/solver/baselines.py`. Implement FCFS and SPT dispatchers. Run on `test_2x2`.

**Output:** Valid schedules (no overlap, precedence respected).
**Done when:** Both schedules are valid. SPT makespan ≤ FCFS (usually).

---

### Action 7: Add energy-cost accounting

**Task:** Extend `cpsat_model.py`: time-slot-to-operation mapping, tariff prices, energy cost computation. Create 2-slot tariff (cheap=5, expensive=8 ₹/kWh). Verify by hand.

**Output:** Energy cost for a schedule, matching hand calculation.
**Done when:** Computed cost = manual Σ(P × duration × price) calculation.

---

### Action 8: Add peak-demand constraint and objective

**Task:** Add $P^{\text{peak}}$ variable, slot_power variables, constraint C6. Solve `test_2x2` with `min P_peak`. Check peak = max simultaneous power.

**Output:** $P^{\text{peak}}$ matches manual Gantt inspection.
**Done when:** Peak equals max sum of concurrent machine powers.

---

### Action 9: Implement ε-constraint loop (2-objective)

**Task:** Create `src/solver/epsilon_constraint.py`. Implement Part 5.2 workflow for 2 objectives (makespan, energy cost). Run on 3×2 instance with k=5.

**Output:** 5 Pareto-efficient solutions. 2D scatter plot.
**Done when:** All solutions non-dominated. Plot shows expected tradeoff.

---

### Action 10: Download and verify KERC tariff order

**Task:** Visit kerc.karnataka.gov.in or bescom.karnataka.gov.in. Download latest tariff order PDF. Find HT-2(a) section. Record: demand charge (₹/kVA), energy charge (₹/kWh), ToD multipliers, peak hours, MD measurement.

**Output:** `docs/tariff_reference.md` with values and page-number citations.
**Done when:** Document has demand charge, energy charge, ToD multipliers, peak hours — all with PDF page references.
