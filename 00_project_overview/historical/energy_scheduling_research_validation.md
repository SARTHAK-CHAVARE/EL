> [!WARNING]
> # HISTORICAL / REFERENCE DOCUMENT
>
> This file records an earlier project state.
>
> It may contain the superseded PZEM-004T hardware design and earlier
> tariff/model assumptions.
>
> It must NOT be treated as the current technical specification.
>
> Current specifications:
> - `00_project_overview/energy_scheduling_project_master_context.md`
> - `05_planning/master_execution_plan.md`
> - `09_hardware/current_hardware_spec.md`
> - `03_tariff/tariff_reference.md`

# Energy Scheduling — Mathematical Research & Engineering Depth Validation

> **Date:** 2026-10-02
> **Posture:** Hostile evaluator. No manufactured novelty. No unsupported percentages.

---

## 1. Audit of the Existing Idea

**Source:** [sdg9_project_audit.md](file:///c:/Project/EL/sdg9_project_audit.md), §6.2, §10.2

### Current formulation

`[ESTABLISHED]` Bi-objective MILP: min{C_max, EnergyCost} with machine-state energy (processing/idle/startup), Indian ToU tariffs, MSME batch production.

### Mathematical model

`[ESTABLISHED]` Standard job-shop MILP with precedence, no-overlap, machine-state variables. ε-constraint for Pareto + NSGA-II for scale.

### Proposed hardware

`[PROPOSED]` PZEM-004T power meter for machine energy profiling. Optional—not load-bearing for core research.

### Optimizer

`[ESTABLISHED]` PuLP / Gurobi (academic). Standard MILP solvers.

### Baseline

`[ESTABLISHED]` FCFS, SPT, energy-unaware MILP.

### Innovation claim

`[OVERCLAIMED]` Prior audit classified this as "contextual novelty (E) and experimental novelty (D)." The formulation is textbook. The Indian-tariff parameterisation is the only differentiator.

### Prototype

`[PROPOSED]` Software-only Gantt + cost dashboard. Prior audit flagged this as "less visually dramatic" and potentially weak on Phase III Innovation/Usability (30 marks).

### Weaknesses (from prior audit)

1. **No mathematical contribution.** The formulation is literally Mouzon (2007) + Gahm (2016) with different parameters.
2. **Software-only prototype** risks scoring poorly on Innovation criterion.
3. **Novelty claim is indefensible** as algorithmic or mathematical contribution.
4. **No uncertainty handling.** Deterministic model only.
5. **No physical validation.** Synthetic instances only.

### Feasibility concerns

- Energy savings may be marginal if tariff differential is small.
- Evaluator sees "applying existing technique with different data."

### Relevant rubric requirements

- **Phase III Prototype (30/200):** Functionality, Innovation, Usability — the highest-weight single criterion.
- **Phase III Results (20/200):** Requires thorough analysis and logical interpretation — needs statistical validation, not single-run.
- **Phase II Tools (20/200):** "Cutting-edge, highly appropriate" tools — standard PuLP/MILP may not score here.

---

## 2. Core Question Answer

> **Can energy-aware manufacturing scheduling become a mathematically rigorous, experimentally falsifiable engineering project with a compelling working prototype?**

| Dimension | Current State | Verdict |
|---|---|---|
| Mathematical research depth | **Zero.** Formulation is textbook MILP from 2007–2016 literature. | ❌ Insufficient |
| Physical engineering depth | **Minimal.** PZEM-004T is optional; core is software-only. | ⚠️ Weak |
| Experimental depth | **Reasonable.** Synthetic instances + statistical comparison is standard OR practice. | ✅ Adequate |
| Prototype quality | **Weak.** Gantt chart + dashboard is standard; no physical demonstration. | ⚠️ Weak |
| SDG 9 relevance | **Strong.** Indian MSMEs + ToU tariffs + SDG 9.4. | ✅ Strong |

**Assessment:** The project as originally proposed is a software optimization demo with Indian parameters. It needs a genuine mathematical research layer and a physical engineering layer. Both are achievable. **MODIFY, then GO.**

---

## 3. Prior-Art / State-of-the-Art

| Work | Model | Objectives | Uncertainty | Physical validation | Main limitation |
|---|---|---|---|---|---|
| Mouzon et al. (2007, IIE) | Single-machine ON/OFF | Energy | None | None | Single machine; no ToU |
| Gahm et al. (2016, EJOR) | Survey: 100+ papers | Various | Rarely addressed | Rarely | Pre-2016 snapshot |
| State-dependent MILP (MDPI 2023–24) | Job-shop + machine states | Makespan + Energy | None | None (synthetic) | Western tariffs; no peak demand |
| Period-indexed MILP (SciTePress 2024) | ToU-aware MILP | Energy cost | None | None | Computational only |
| Multi-obj green scheduling (MDPI 2023) | Bi-objective FJSP | Makespan + Energy | None | None (NSGA-II) | No real data validation |
| AUGMECON ε-constraint (2022–24) | Multi-obj MILP | Cost + Emissions + Peak | None | Mixed | No uncertainty; no MSME |
| DRL + rolling horizon (MDPI 2024) | Dynamic scheduling | Makespan + Energy | Machine breakdown | Digital twin | Complex; no student feasibility |
| Robust FJSP (Atlantis Press 2024) | Robust MILP | Makespan robustness | Processing time | None | No energy awareness |
| Co-scheduling with DDU (arXiv 2024) | Energy + production | Cost | Decision-dependent | Simulation | Advanced; limited applicability |
| MPC-based scheduling (arXiv 2024) | Receding horizon | Energy cost | Price volatility | Simulation | Requires real-time solver |

### What is already solved

`[ESTABLISHED]` The following are standard, well-studied, and have extensive published solutions:

- Bi-objective makespan + energy MILP: **Solved since 2007.**
- Machine-state energy models (idle/processing/startup): **Standard since 2016.**
- ε-constraint and NSGA-II for Pareto front: **Textbook methodology.**
- ToU-aware scheduling: **Standard in OR literature.**
- Multi-objective green scheduling: **Hundreds of papers.**

### What is less studied

`[OBSERVED GAP]` These gaps are genuine but narrow:

1. **Peak demand as an explicit objective** (not just total energy): Most papers minimise total energy cost, ignoring demand charges. Indian tariffs include demand charges based on 15-minute peak kVA.
2. **Uncertainty-aware energy scheduling with physical validation**: Most robust/stochastic models are purely computational; very few validate with measured machine power.
3. **Tri-objective scheduling (makespan + energy cost + peak demand)**: The three-objective version is genuinely less explored than bi-objective.
4. **Rolling-horizon rescheduling with measured energy feedback**: Closed-loop scheduling where measured power feeds back into re-optimisation is rare in student-feasible implementations.

### Honesty check

`[ESTABLISHED]` None of these gaps constitute major algorithmic breakthroughs. They are **extensions and combinations** of existing techniques applied to a specific, practical context. This is honest and defensible for an undergraduate project, but must not be sold as "novel algorithm."

---

## 4. Mathematical Research Gap Analysis

| Research direction | Baseline | Proposed change | Why it matters | How to test | Difficulty |
|---|---|---|---|---|---|
| **A. Tri-objective: Makespan + Cost + Peak** | Bi-objective (makespan + energy cost) | Add peak demand as third objective; use AUGMECON for 3D Pareto | Indian industrial tariffs charge for peak kVA separately. Ignoring peak can make "optimal" schedules expensive in practice. | Generate Pareto surfaces; compare 2-obj vs 3-obj on total bill (energy + demand charge). | Medium |
| **B. Processing time uncertainty** | Deterministic MILP | Scenario-based robust MILP: solve over K scenarios of processing time drawn from measured distributions | Real processing times vary ±10–30%. Deterministic schedule may violate deadlines. | Compare expected cost + deadline violations under Monte Carlo perturbation. | Medium-High |
| **C. Rolling-horizon rescheduling** | Single-shot optimize-then-execute | Measure → optimise → execute → detect deviation → re-optimise | Single-shot schedules break when disruptions occur. Rolling-horizon adapts. | Compare schedule stability and realised cost between single-shot and rolling-horizon under simulated disruptions. | High |
| **D. Peak-demand-aware scheduling** | Minimise total energy cost only | Add peak power constraint or objective: min max_t Σ_m P_m(t) | Demand charges can be 30%+ of Indian industrial bills. Shaving peak saves money even if total kWh stays the same. | Measure difference in peak demand and demand charge between cost-only and peak-aware schedules. | Medium |
| **E. Measured vs constant energy models** | Constant P_proc per machine | Measure real power profiles (variable power during processing); use measured profiles in MILP | Constant-power assumption may misestimate energy by 15–40%. If the model is wrong, the schedule is wrong. | Compare schedules from constant vs measured models; validate with PZEM-004T. | Low-Medium |
| **F. Scalability analysis** | Small instances (5×3) | Systematic scaling: 5×3 → 10×5 → 20×8 → 50×10 | Must know where MILP becomes intractable and heuristic is needed. | Plot solver time, gap, and solution quality vs instance size. | Low |

### Strongest defensible research direction

**Direction D+A combined: Tri-objective scheduling with peak demand awareness.**

Justification:

1. `[ESTABLISHED]` Indian industrial tariffs (as of April 2024) include mandatory ToD pricing AND demand charges based on 15-minute peak kVA. This is a documented structural feature, not an assumption.
2. `[OBSERVED GAP]` Most energy-aware scheduling papers minimise total energy cost (kWh × price), ignoring demand charges. This means the "optimal" schedule can actually increase the total electricity bill if it creates power spikes.
3. `[INFERENCE]` Adding peak demand as a third objective changes the Pareto front structure in a non-trivial way — there are genuine trade-offs between spreading work (to reduce peak) and concentrating work in cheap periods (to reduce energy cost).
4. `[HYPOTHESIS]` A peak-demand-aware schedule will reduce the total electricity bill (energy charge + demand charge) compared to a cost-only schedule, even if total kWh is slightly higher.

This is **not** a new algorithm. It is an **extended formulation** with a mathematically defensible reason (demand charge structure) and a testable hypothesis (total-bill reduction). This is honest.

### Directions to deprioritise

- **B (Uncertainty):** Genuine research, but adds significant complexity. Risk of intractability. Reserve for Level 3/4.
- **C (Rolling-horizon):** Genuine research question, but requires real-time implementation. Too complex for minimum viable.
- **E (Measured profiles):** Important for engineering depth but not mathematically novel. Use as hardware integration layer.
- **F (Scalability):** Standard experiment, not research contribution. Include as supporting experiment.

---

## 5. Mathematical Formulation

### Sets

- $\mathcal{J} = \{1, \ldots, n\}$: set of jobs
- $\mathcal{O}_i$: set of operations for job $i$
- $\mathcal{M}$: set of machines
- $\mathcal{T} = \{1, \ldots, T\}$: set of discrete time slots (e.g., 15-minute intervals)
- $\mathcal{M}_o \subseteq \mathcal{M}$: set of machines eligible for operation $o$

### Parameters

- $p_o$: processing time of operation $o$ (time slots)
- $P^{proc}_m$: processing power of machine $m$ (kW) — **measured via PZEM-004T**
- $P^{idle}_m$: idle power of machine $m$ (kW) — **measured**
- $E^{start}_m$: startup energy of machine $m$ (kWh) — **measured**
- $\text{tariff}(t)$: energy price in time slot $t$ (₹/kWh) — **from state SERC tariff order**
- $D^{charge}$: demand charge rate (₹/kVA/month) — **from state SERC tariff order**
- $\Delta t$: time slot duration (hours)
- $d_i$: deadline for job $i$ (optional)
- $\text{prec}(o', o)$: 1 if operation $o'$ must precede $o$

### Decision variables

- $x_{omt} \in \{0, 1\}$: operation $o$ starts on machine $m$ at time $t$
- $y_{mt} \in \{0, 1\}$: machine $m$ is processing during time slot $t$
- $w_{mt} \in \{0, 1\}$: machine $m$ is idle (on but not processing) during time slot $t$
- $z_{mt} \in \{0, 1\}$: machine $m$ has a startup event at time slot $t$
- $C_{max} \in \mathbb{R}^+$: makespan
- $P^{peak} \in \mathbb{R}^+$: peak total power across all time slots

### Why each variable exists

| Variable | Purpose | Without it |
|---|---|---|
| $x_{omt}$ | Assigns each operation to a machine and start time | Cannot construct a schedule |
| $y_{mt}$ | Tracks whether machine is actively processing | Cannot compute processing energy |
| $w_{mt}$ | Distinguishes idle from off | Cannot model idle energy (real machines draw power when on but not processing) |
| $z_{mt}$ | Detects startup transitions | Cannot model startup energy cost |
| $C_{max}$ | Makespan objective | Cannot optimise production time |
| $P^{peak}$ | Peak power variable | Cannot optimise demand charge |

### Objective functions

**Objective 1 — Makespan:**
$$\min C_{max} = \max_{i \in \mathcal{J}} \left( \max_{o \in \mathcal{O}_i} \sum_{m,t} x_{omt} \cdot (t + p_o) \right) \cdot \Delta t$$

**Objective 2 — Energy cost:**
$$\min \text{EnergyCost} = \sum_{t \in \mathcal{T}} \sum_{m \in \mathcal{M}} \left[ P^{proc}_m \cdot y_{mt} + P^{idle}_m \cdot w_{mt} + \frac{E^{start}_m}{\Delta t} \cdot z_{mt} \right] \cdot \text{tariff}(t) \cdot \Delta t$$

**Objective 3 — Peak demand (our proposed extension):**
$$\min P^{peak}$$

where $P^{peak}$ is constrained by:
$$P^{peak} \geq \sum_{m \in \mathcal{M}} \left[ P^{proc}_m \cdot y_{mt} + P^{idle}_m \cdot w_{mt} + \frac{E^{start}_m}{\Delta t} \cdot z_{mt} \right] \quad \forall t \in \mathcal{T}$$

**Total electricity bill (for comparison, not optimisation):**
$$\text{TotalBill} = \text{EnergyCost} + D^{charge} \cdot P^{peak}$$

### Constraints

**C1 — Assignment:** Each operation assigned to exactly one machine and start time:
$$\sum_{m \in \mathcal{M}_o} \sum_{t \in \mathcal{T}} x_{omt} = 1 \quad \forall o$$

**C2 — Precedence:** If $\text{prec}(o', o) = 1$:
$$\sum_{m,t} x_{o'mt} \cdot (t + p_{o'}) \leq \sum_{m,t} x_{omt} \cdot t$$

**C3 — No overlap:** At most one operation on each machine at any time:
$$\sum_{o : m \in \mathcal{M}_o} \sum_{\tau = t - p_o + 1}^{t} x_{om\tau} \leq 1 \quad \forall m, t$$

**C4 — Machine state logic:**
$$y_{mt} + w_{mt} \leq 1 \quad \forall m, t$$

$y_{mt} = 1$ if and only if some operation is being processed on machine $m$ at time $t$:
$$y_{mt} = \sum_{o : m \in \mathcal{M}_o} \sum_{\tau = \max(1, t - p_o + 1)}^{t} x_{om\tau} \quad \forall m, t$$

**C5 — Startup detection:**
$$z_{mt} \geq (y_{mt} + w_{mt}) - (y_{m,t-1} + w_{m,t-1}) \quad \forall m, t > 1$$

**C6 — Makespan:**
$$C_{max} \geq \sum_{m,t} x_{omt} \cdot (t + p_o) \cdot \Delta t \quad \forall o \text{ that is the last operation of some job}$$

**C7 — Deadline (optional):**
$$\sum_{m,t} x_{omt} \cdot (t + p_o) \cdot \Delta t \leq d_i \quad \forall i, o = \text{last}(i)$$

**C8 — Peak demand:**
$$P^{peak} \geq \sum_{m \in \mathcal{M}} \left[ P^{proc}_m \cdot y_{mt} + P^{idle}_m \cdot w_{mt} + \frac{E^{start}_m}{\Delta t} \cdot z_{mt} \right] \quad \forall t$$

### Multi-objective solution method

**AUGMECON (Augmented ε-constraint):**

1. Optimise each objective individually to find anchor points.
2. Choose one primary objective (e.g., EnergyCost).
3. Treat others as constraints with systematically varied ε values.
4. Generate Pareto-efficient solution set.

For the 3-objective case, this produces a **Pareto surface** (not just a front), which is visualisable as a 3D scatter plot.

### Assumptions (stated honestly)

| Assumption | Realistic? | Consequence if violated |
|---|---|---|
| Processing times are deterministic | **No** — real times vary ±10–30% | Schedule may violate deadlines; addressed by uncertainty experiments |
| Machine power is constant during processing | **Roughly yes** for most MSME machines (motors, CNC at steady state) | If violated, measured profiles provide correction |
| No machine breakdowns | **Unrealistic** for long horizons | Rolling-horizon would address; excluded from minimum viable |
| Jobs are known in advance | **Roughly yes** for batch MSME production | Dynamic arrival excluded from minimum viable |
| Linear ToU tariff | **Yes** — Indian tariffs are piecewise-constant per time block | Directly matches real tariff structure |
| Demand charge based on peak kW | **Yes** — standard Indian industrial tariff structure | Directly matches real billing |

### What mathematical contribution is actually ours

`[PROPOSED]` **The extension from bi-objective to tri-objective (adding peak demand), motivated by the specific structure of Indian industrial tariffs where demand charges are a documented significant cost component.**

This is:
- NOT a new algorithm ← `[ESTABLISHED]` AUGMECON, MILP, and NSGA-II are all standard
- NOT a new model structure ← `[ESTABLISHED]` machine-state MILP exists
- An **extended formulation** with a **specific practical motivation** (demand charges) and **testable consequences** (different Pareto structure, different total bill)
- Honest for an undergraduate project

### Computational complexity

`[ESTABLISHED]` Job-shop scheduling is NP-hard. The tri-objective extension does not change the complexity class but increases the number of MILP solves required (grid over 2 ε dimensions → O(k²) solves for k grid points per dimension). For small instances (≤10 jobs × 5 machines), exact solution via Gurobi is feasible. For larger instances, NSGA-III (3-objective extension of NSGA-II) is the standard metaheuristic.

### Solvability within student resources

- **Gurobi Academic License:** Free. Handles 10×5 instances in seconds to minutes.
- **PuLP with CBC:** Free, open-source. Slower but adequate for small instances.
- **NSGA-III via pymoo:** Free Python library. Handles larger instances.
- **Estimated computation:** 3-objective AUGMECON with 10×10 ε-grid = 100 MILP solves. At ~10 seconds each = ~17 minutes total. Feasible on a laptop.

---

## 6. Mathematical Experiments

### Experiment 1 — Model comparison (ablation)

**Question:** Does adding peak demand as an objective change the optimal schedule?

| Condition | Objectives | Method |
|---|---|---|
| A (baseline heuristic) | None (FCFS) | Dispatch rule |
| B (baseline heuristic) | None (SPT) | Dispatch rule |
| C (single-obj) | min Makespan | MILP |
| D (bi-objective) | min {Makespan, EnergyCost} | AUGMECON |
| E (tri-objective) | min {Makespan, EnergyCost, PeakDemand} | AUGMECON |

**Measures:** Makespan, energy cost (₹), peak demand (kW), total bill (₹), solver time (s), optimality gap (%).

**Instances:** 20 random instances per size category: 5×3, 8×4, 10×5.

**Statistical test:** Wilcoxon signed-rank test on total bill, D vs E.

**Falsifiability:** If E does not reduce total bill compared to D on ≥60% of instances, the peak-demand extension provides no benefit. This would be a valid negative result.

### Experiment 2 — Sensitivity to tariff structure

**Question:** Under what tariff conditions does peak-demand-aware scheduling matter?

**Design:** Vary demand charge rate from ₹0 to ₹500/kVA/month in 10 steps. For each, run bi-objective (D) and tri-objective (E). Plot total bill difference vs demand charge rate.

**Expected outcome:** `[HYPOTHESIS]` Benefit of peak-demand awareness increases with demand charge rate. There exists a threshold below which it provides negligible benefit. Finding this threshold is a research contribution.

### Experiment 3 — Sensitivity to tariff differential

**Question:** Does the peak/off-peak price ratio affect whether energy-aware scheduling is worthwhile?

**Design:** Vary peak/off-peak ratio from 1.0 (flat tariff) to 2.0 (steep differential). Fix demand charge at Karnataka BESCOM rate. Compare FCFS vs tri-objective on total bill.

**Expected outcome:** `[HYPOTHESIS]` Benefit increases with price differential. At ratio ≈ 1.0, benefit approaches zero.

### Experiment 4 — Scalability

**Question:** At what problem size does exact MILP become intractable?

**Design:** Increase from 5×3 to 50×10. Measure solver time, optimality gap (1% threshold), and memory. Compare MILP (Gurobi) vs NSGA-III (pymoo).

**Measures:** Wall-clock time, optimality gap, hypervolume indicator, number of Pareto-efficient solutions found.

### Experiment 5 — Energy model realism (ablation)

**Question:** Does using measured power profiles instead of constant power change the optimal schedule?

**Design:** 
- F1: Constant P_proc (literature default)
- F2: Measured P_proc + P_idle (from PZEM-004T)
- F3: F2 + measured startup energy

Run tri-objective MILP on same instances with each energy model. Compare resulting schedules and costs.

**Falsifiability:** If F1, F2, F3 produce identical schedules on >80% of instances, the energy model refinement is unnecessary.

### Experiment 6 — Uncertainty (stretch goal)

**Question:** Does a deterministic schedule remain good when processing times are perturbed?

**Design:** Generate 100 perturbation scenarios (processing times drawn from N(p_o, 0.15·p_o)). Evaluate the deterministic schedule under each scenario. Measure deadline violations, realised cost, and peak demand.

**Falsifiability:** If the deterministic schedule violates deadlines in <5% of scenarios, robustness extensions are unnecessary for this problem scale.

---

## 7. Physical Engineering Layer

### Minimum testbed

| Component | Technical purpose | Required? |
|---|---|---|
| PZEM-004T energy meter | Measures real V, I, P, E of physical loads — provides measured P_proc, P_idle, E_start | **Yes** — transforms project from simulation to measurement |
| ESP32 microcontroller | Reads PZEM-004T via UART; transmits data to optimizer; controls relays | **Yes** — provides edge computing and I/O |
| 4-channel relay module | Switches physical loads on/off per schedule — demonstrates schedule execution | **Yes** — closes the loop from optimizer to physical world |
| 3 small loads (motor, heater, lamp) | Represent 3 "machines" with different power profiles | **Yes** — minimum for scheduling (need >1 machine) |
| Dashboard (laptop/tablet) | Displays schedule, real-time power, cost accumulation | **Yes** — evaluator needs to see the system working |

### What each component demonstrates

1. **PZEM-004T → ESP32:** Real power measurement feeds the energy model. This is NOT simulated data.
2. **ESP32 → Relay → Loads:** Schedule execution. The optimizer's output physically turns machines on/off at the right times.
3. **Loads → PZEM-004T:** Closed loop. Measured power validates that the executed schedule matches the prediction.
4. **Dashboard:** Visualises the Gantt chart, power timeline, cost accumulation, and comparison between baseline and optimised schedules in real time.

### BOM

| Component | Qty | Unit Cost (₹) | Total (₹) |
|---|---|---|---|
| ESP32-WROOM-32 | 1 | 500 | 500 |
| PZEM-004T (with CT) | 1 | 500 | 500 |
| 4-channel relay module (5V) | 1 | 200 | 200 |
| Small DC motor (775) | 1 | 250 | 250 |
| Heating element (small) | 1 | 100 | 100 |
| LED lamp/load | 1 | 50 | 50 |
| Breadboard + wires | 1 | 200 | 200 |
| **Total** | | | **₹1,800** |

---

## 8. Real Data vs Simulation

### REAL (measured from physical testbed)

- Machine power profiles: P_proc, P_idle for each load — **via PZEM-004T**
- Startup energy: E_start for each load — **via PZEM-004T**
- Schedule execution: actual ON/OFF times — **via relay + timestamp logging**
- Realised energy consumption — **via PZEM-004T integration over time**
- Realised peak demand — **via PZEM-004T max(P(t))**

**Why legitimate:** These are direct physical measurements of the system under control. They validate the energy model.

### MODELLED (from real-world sources, not measured in testbed)

- Processing times — **modelled as MSME-representative values**
- Job precedence constraints — **from MSME production structure (or synthetic)**
- ToU tariff — **from state SERC tariff order (Karnataka BESCOM / Maharashtra MSEDCL)**
- Demand charge rate — **from state SERC tariff order**
- Machine capabilities — **modelled**

**Why legitimate:** Tariff data is publicly available, officially published, and directly applicable. Processing times in OR are always parameterised. This is standard practice in every scheduling paper.

### SIMULATED (for scalability and sensitivity)

- Large-scale instances (20+ jobs × 8+ machines) — beyond physical testbed
- Monte Carlo perturbation scenarios — for uncertainty analysis
- Tariff structure variations — for sensitivity analysis

**Why legitimate:** Scaling experiments cannot be done physically (we don't have 50 machines). Simulation is the standard methodology in OR. The key is that the energy model used in simulation is **validated against physical measurements** from the testbed.

---

## 9. Closed-Loop Architecture

```
Physical loads (motor, heater, lamp)
      ↓
Power sensing (PZEM-004T)
      ↓
Energy model (P_proc, P_idle, E_start)
      ↓
Production model (jobs, operations, precedence)
      ↓
Tri-objective MILP optimizer (laptop)
      ↓
Schedule (Gantt chart)
      ↓
Controller (ESP32 → relays)
      ↓
Physical execution (loads turn ON/OFF)
      ↓
Measurement (PZEM-004T)
      ↓
Validation (predicted vs actual energy/peak)
```

### Architecture options

| Level | Architecture | What it shows | Prototype effort |
|---|---|---|---|
| 1 | Optimization only | MILP + Pareto analysis on synthetic data | Low |
| 2 | Optimization + monitoring | MILP + PZEM-004T measures real power | Medium |
| **3** | **Optimization + monitoring + control** | **MILP → ESP32 → relay → loads + measurement** | **Medium-High** |
| 4 | Closed-loop adaptive scheduling | Level 3 + deviation detection + re-optimisation | High |

**Selected: Level 3.** This provides:
- Real measurement (engineering depth)
- Physical execution (prototype demonstration)
- Predicted vs actual comparison (experimental validation)
- No rescheduling (avoids complexity risk)

Level 4 is stretch goal only.

---

## 10. Prototype Demonstration (5-minute evaluator demo)

### Setup

Three physical loads (motor, heater, lamp) connected via relay module to ESP32. PZEM-004T monitors total power. Laptop runs optimizer + dashboard.

### Demo script

1. **[30s] Problem setup:** Show 3 "machines" (loads), 5 "jobs" with processing times and precedence. Show Indian ToU tariff structure on screen.

2. **[60s] Baseline execution:** Run FCFS schedule. ESP32 turns loads on/off per FCFS order. Dashboard shows real-time power trace, accumulating cost, peak demand.

3. **[30s] Optimization:** Run tri-objective MILP on laptop. Show solver log. Show Pareto surface (3D scatter: makespan × cost × peak). Let evaluator pick a Pareto-efficient solution.

4. **[60s] Optimised execution:** ESP32 executes the selected schedule. Dashboard shows real-time power trace, cost, peak — overlaid with baseline for comparison.

5. **[30s] Comparison table:**

```
                Baseline (FCFS)    Optimised (Tri-obj)    Improvement
Energy Cost     ₹ ______          ₹ ______               ____%
Peak Demand     ______ kW         ______ kW               ____%
Total Bill      ₹ ______          ₹ ______               ____%
Makespan        ______ min        ______ min              ____%
Solver Time     N/A               ______ sec              N/A
```

6. **[30s] Ablation summary:** Show bar chart: FCFS vs SPT vs Makespan-only vs Bi-objective vs Tri-objective on total bill. Show that peak-demand awareness provides additional bill reduction.

7. **[30s] Pareto surface:** Interactive 3D plot. Evaluator can rotate and explore trade-offs.

**This demonstration shows decision-making and engineering behavior:** The optimizer makes a non-trivial choice (which machines to idle, when to start, how to spread load) and the physical system executes it, with measured results validating the prediction.

---

## 11. Research Questions

### Candidates

1. *Does incorporating peak demand as a third scheduling objective reduce total industrial electricity bills under Indian tariff structures, compared to energy-cost-only optimisation?*

2. *Under what demand-charge conditions does peak-demand-aware scheduling provide statistically significant bill reduction, and below what threshold is it unnecessary?*

3. *Does using measured machine power profiles (idle + processing + startup) change optimal schedules compared to constant-power assumptions, and by how much?*

4. *How does the quality of tri-objective Pareto approximation (NSGA-III) compare to exact AUGMECON solutions as problem size increases?*

5. *Does a deterministic energy-aware schedule maintain feasibility under stochastic processing time perturbations, or does uncertainty-aware scheduling provide measurably better outcomes?*

### Selection

**Primary RQ: Question 1+2 combined:**

> *Does incorporating peak demand as a third objective in energy-aware manufacturing scheduling reduce total electricity bills under Indian ToU + demand-charge tariff structures, and under what tariff conditions does this benefit become statistically significant?*

**Justification:**

| Criterion | Score | Rationale |
|---|---|---|
| Mathematical depth | **Strong** | Tri-objective MILP + AUGMECON + Pareto surface analysis. Genuine multi-objective optimization. |
| Novelty | **Moderate** | Peak-demand as explicit 3rd objective in manufacturing scheduling is less explored. Not algorithmic novelty, but formulation extension with practical justification. |
| Falsifiability | **Strong** | Clear null hypothesis: peak-demand awareness provides no statistically significant bill reduction. Testable with Wilcoxon on paired instances. |
| Engineering relevance | **Strong** | Demand charges are 30%+ of real Indian industrial bills. Directly useful. |
| Prototype feasibility | **Strong** | Tri-objective MILP is solvable; physical demo is the same as bi-objective. |
| Rubric fit | **Strong** | Mathematical formulation + physical prototype + quantitative comparison + clear results. |

---

## 12. Minimum Viable Research Project

### Mathematical contribution
`[PROPOSED]` Tri-objective MILP formulation (makespan + energy cost + peak demand) with AUGMECON solution, motivated by Indian demand-charge tariff structure. Systematic sensitivity analysis on demand-charge rate.

### Engineering contribution
Physical testbed: 3 loads + PZEM-004T + ESP32 + relay control. Measured power profiles feeding into optimizer. Schedule execution with measured validation.

### Experimental contribution
- 5 scheduling conditions: FCFS, SPT, makespan-only MILP, bi-objective MILP, tri-objective MILP.
- 20+ random instances per size category (5×3, 8×4, 10×5).
- Statistical comparison (Wilcoxon).
- Pareto surface visualisation and hypervolume comparison.
- Sensitivity analysis on demand-charge rate and tariff differential.
- Measured vs predicted energy validation.

### Prototype
Physical loads controlled by ESP32, powered by MILP optimizer, monitored by PZEM-004T, visualised on dashboard. 5-minute live demonstration.

### Evidence
- Total bill comparison (energy + demand charge) across conditions.
- Statistical significance of tri-objective benefit.
- Demand-charge threshold where benefit becomes significant.
- Predicted vs measured energy error.

---

## 13. Escalation Path

### Level 1 — Minimum viable (MUST work)
- Bi-objective MILP (makespan + energy cost) with AUGMECON
- Synthetic instances + Indian ToU tariff
- FCFS/SPT baseline comparison
- Software Gantt + cost dashboard
- Statistical comparison (20+ instances, Wilcoxon)

### Level 2 — Strong engineering (adds physical layer)
- Level 1 +
- PZEM-004T measured power profiles for 3 loads
- ESP32 + relay execution of schedule
- Predicted vs measured energy validation
- Live demonstration with physical loads

### Level 3 — Mathematical research (strongest contribution)
- Level 2 +
- **Tri-objective formulation: makespan + energy cost + peak demand**
- AUGMECON Pareto surface (3D)
- Sensitivity analysis on demand-charge rate
- Hypervolume comparison (2-obj vs 3-obj)
- Energy model ablation (constant vs measured)

### Level 4 — Stretch (only if L1–L3 are solid)
- Level 3 +
- Scenario-based uncertainty analysis (processing time perturbation)
- NSGA-III for larger instances (20+ jobs)
- Scalability analysis with Gurobi time limits
- Rolling-horizon rescheduling prototype

> [!WARNING]
> **Level 4 must not endanger Levels 1–3.** If Level 3 is not working by week 8, do NOT attempt Level 4. Ship a polished Level 2/3.

---

## 14. Failure Analysis

| Failure | Consequence | Mitigation | Residual risk |
|---|---|---|---|
| **Optimizer produces negligible improvement over FCFS** | Core claim fails; project becomes "verified that scheduling doesn't help" | Select instances with tight deadlines + high tariff differential. If still marginal, report honestly as negative result. | Low — OR literature consistently shows MILP beats dispatch heuristics when tariff differential > 1.2× |
| **Peak-demand extension gives negligible benefit** | Tri-objective contribution adds nothing beyond bi-objective | Report the demand-charge threshold. Negative result is valid: "peak awareness only matters when demand charges exceed ₹X/kVA." | Medium — depends on tariff structure. Mitigated by sensitivity analysis. |
| **PZEM-004T readings are noisy/unreliable** | Measured profiles unreliable; energy model validation fails | Use averaging over multiple readings. Calibrate against known load. Worst case: use manufacturer-spec power values + acknowledge limitation. | Low — PZEM-004T is well-characterised for ≥100W loads. |
| **Measured power differs significantly from constant model** | Schedules from constant model are suboptimal. But this is actually a positive result (shows measurement matters). | Report as finding: "constant-power assumption causes X% cost error." | Low — this failure mode is actually a research result. |
| **Schedule becomes infeasible with deadlines** | MILP returns infeasible | Relax deadlines; use tardiness penalty instead of hard constraint. | Low — standard OR technique. |
| **Solver too slow for 10×5 instances** | Cannot produce results in reasonable time | Use Gurobi with 60s time limit + report optimality gap. Fall back to NSGA-III for larger instances. | Low — Gurobi academic handles 10×5 in <60s typically. |
| **Physical testbed is unrepresentative** | Evaluator says "this isn't a real factory" | Acknowledge honestly. Testbed validates the energy model and control loop, not industrial scale. Simulation extends to realistic sizes. | Medium — inherent in any student project. Frame as "validated methodology, not deployed system." |
| **Relay control adds no value** | Evaluator says "you could have just simulated this" | The relay demonstrates that the schedule is physically executable and that predicted energy matches measured energy. This is the validation step. | Low — physical validation is the engineering contribution. |

---

## 15. Final Decision Gate

| Gate | Requirement | Status | Evidence |
|---|---|---|---|
| Real industrial problem | Evidence | ✅ PASS | Indian MSME energy costs documented by BEE, CEEW. ToD tariffs mandatory from April 2024 (MoP rules). Demand charges are 30%+ of industrial bills. |
| Mathematical research | Genuine contribution | ✅ PASS (conditional) | Tri-objective extension with peak demand. Not algorithmic novelty — formulation extension with practical motivation. Defensible for UG level. |
| Mathematical validation | Falsifiable experiments | ✅ PASS | 6 experiments designed. Clear null hypotheses. Statistical tests specified. |
| Engineering depth | Physical system | ✅ PASS | PZEM-004T + ESP32 + relay + 3 loads. Measures, executes, validates. |
| Prototype feasibility | Buildable | ✅ PASS | BOM ₹1,800. All components available on Amazon India. |
| Experimental validation | Baseline vs proposed | ✅ PASS | 5 conditions: FCFS, SPT, makespan MILP, bi-obj MILP, tri-obj MILP. |
| Research contribution | Defensible | ⚠️ CONDITIONAL | Defensible if framed as "extended formulation + validation" not "novel algorithm." Must cite prior art honestly. |
| SDG 9 connection | Concrete | ✅ PASS | SDG 9.4 (sustainable industrialisation). Direct: reduces MSME energy costs using optimised scheduling. |
| Rubric fit | Strong | ✅ PASS | Math + hardware + live demo + statistical results + Pareto visualisation. |
| Cost | Student feasible | ✅ PASS | ~₹1,800 hardware. Software free (PuLP/Gurobi academic/pymoo). |
| Time | Student feasible | ✅ PASS | 10–12 weeks. Core MILP: 3 weeks. Hardware: 2 weeks. Experiments: 3 weeks. Report: 2 weeks. |

---

## FINAL OUTPUT

### 1. Verdict

The project, **as originally proposed**, is a software optimisation demo with Indian parameters — insufficient for mathematical depth and prototype quality. **With the modifications below, it becomes a defensible research project.**

### 2. What is currently weak

- **No mathematical contribution** beyond parameterising an existing model
- **No physical prototype** — software-only Gantt chart
- **No sensitivity/robustness analysis** — single-point results
- **Novelty claim is contextual only** — "Indian tariffs" is not a research gap

### 3. Strongest mathematical research direction

**Tri-objective scheduling: Makespan + Energy Cost + Peak Demand**, motivated by the documented structure of Indian industrial tariffs (mandatory ToD since April 2024 + demand charges on peak kVA).

This is **not** a new algorithm. It is an extended formulation with:
- A specific, documented economic motivation (demand charges)
- A testable hypothesis (total-bill reduction)
- A non-trivial Pareto structure (3D surface)
- Ablation: show that the 3rd objective produces different schedules than 2-objective

### 4. Proposed mathematical formulation

See [§5 above](#5-mathematical-formulation). Tri-objective MILP with AUGMECON. Sets, parameters, variables, objectives, and constraints fully specified.

### 5. Research hypothesis

> Under Indian industrial tariff structures with demand charges, a tri-objective energy-aware manufacturing schedule (minimising makespan, energy cost, AND peak demand simultaneously) produces a lower total electricity bill than a bi-objective schedule (minimising makespan and energy cost only), and this benefit increases with the demand-charge rate.

**Null hypothesis:** Peak-demand-aware scheduling does not significantly reduce total electricity bills compared to energy-cost-only scheduling.

**Test:** Wilcoxon signed-rank on paired instances, α = 0.05.

### 6. Experiments needed

1. **Model comparison** (5 conditions × 20+ instances × 3 sizes): FCFS, SPT, makespan MILP, bi-obj, tri-obj.
2. **Sensitivity to demand-charge rate** (10 levels × 20 instances): Find threshold.
3. **Sensitivity to tariff differential** (10 levels × 20 instances): Find threshold.
4. **Scalability** (5×3 to 50×10): Solver time + NSGA-III comparison.
5. **Energy model ablation** (constant vs measured power): 3 model variants.
6. **Uncertainty** (stretch): Monte Carlo perturbation of processing times.

### 7. Physical prototype architecture

```
Laptop (optimizer + dashboard)
    ↕ WiFi/Serial
ESP32 (controller)
    ↓ UART → PZEM-004T (power measurement)
    ↓ GPIO → 4-channel relay (load control)
    ↓ loads: motor + heater + lamp
```

### 8. Minimum viable prototype

- Bi-objective MILP (makespan + energy cost)
- Synthetic instances + real Indian ToU tariff
- FCFS/SPT baselines
- Statistical comparison
- Software Gantt + cost dashboard

### 9. Strong version

- Tri-objective MILP with peak demand
- PZEM-004T measured power profiles
- ESP32 + relay physical execution
- Predicted vs measured validation
- 3D Pareto surface
- Sensitivity analysis
- Live 5-minute demonstration

### 10. Key risks

1. **Peak-demand extension gives negligible benefit** → Mitigated by sensitivity analysis; finding the threshold is itself a result.
2. **Evaluator sees it as "existing technique + Indian data"** → Must demonstrate physical testbed, live execution, and the specific demand-charge insight.
3. **Solver too slow** → Gurobi academic + time limits + NSGA-III fallback.
4. **PZEM-004T measurement noise** → Averaging + calibration. Low risk.

### 11. GO / MODIFY / REJECT

## **MODIFY then GO**

The core idea (energy-aware scheduling for MSMEs) is strong.

Modifications required:
1. ✅ Add peak demand as 3rd objective (mathematical research layer)
2. ✅ Add PZEM-004T + ESP32 + relay physical testbed (engineering depth)
3. ✅ Add sensitivity analysis on demand-charge rate (experimental depth)
4. ✅ Reframe novelty as "extended formulation with practical validation" (honesty)
5. ✅ Design 5-minute live demo with physical loads (prototype quality)

### 12. Exact next steps

| Priority | Action | Timeline | Effort |
|---|---|---|---|
| 1 | **Order hardware:** ESP32, PZEM-004T, relay module, 3 loads | Day 1 | ₹1,800 |
| 2 | **Implement bi-objective MILP** in PuLP with CBC solver. Test on 5×3 instance. Verify correctness. | Week 1 | 3 days |
| 3 | **Extend to tri-objective** by adding P^peak variable and constraint C8. Verify with AUGMECON. | Week 1–2 | 2 days |
| 4 | **Obtain Indian tariff data:** Download Karnataka BESCOM / Maharashtra MSEDCL tariff order. Extract ToD rates + demand charge. | Week 1 | 1 day |
| 5 | **Build instance generator:** Random job-shop instances with configurable size, processing times, machine eligibility. | Week 2 | 1 day |
| 6 | **Run Experiment 1** (model comparison) on synthetic instances. Verify that tri-objective produces different schedules. | Week 2–3 | 3 days |
| 7 | **Build hardware testbed:** Wire ESP32 + PZEM-004T + relay + loads. Test power measurement. Measure P_proc, P_idle, E_start for each load. | Week 3–4 | 4 days |
| 8 | **Integrate hardware with optimizer:** ESP32 receives schedule from laptop, executes via relays, reports measured power back. | Week 4–5 | 3 days |
| 9 | **Run Experiment 5** (energy model ablation): Compare constant vs measured power models. | Week 5 | 2 days |
| 10 | **Run Experiment 2+3** (sensitivity analysis): Vary demand charge and tariff differential. | Week 5–6 | 3 days |
| 11 | **Run Experiment 4** (scalability): Scale to 20×5, 50×10 with NSGA-III. | Week 6–7 | 2 days |
| 12 | **Build dashboard:** Real-time Gantt + power trace + cost accumulation + Pareto surface. | Week 7–8 | 4 days |
| 13 | **Full demo rehearsal:** Run baseline + optimised schedule live. Record results. | Week 8 | 1 day |
| 14 | **Phase I report:** Problem definition, literature review, methodology, flow chart. | Week 1–3 (parallel) | Ongoing |
| 15 | **Phase III report + poster/PPT:** Results, analysis, discussion. | Week 9–11 | Ongoing |
| 16 | **(Stretch) Experiment 6:** Uncertainty analysis. Only if Levels 1–3 are solid. | Week 9–10 | 3 days |
