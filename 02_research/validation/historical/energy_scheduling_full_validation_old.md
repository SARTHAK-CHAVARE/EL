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

# Energy-Aware Manufacturing Scheduling — Research Validation

> **Date:** 2026-10-02  
> **Posture:** Hostile evaluator. No manufactured novelty. No unsupported claims.  
> **Standard:** Every claim must earn its classification.

---

## TASK 1 — Literature Research

### 1.1 Search methodology

Searched: Google Scholar, IEEE Xplore (via Scholar indexing), ScienceDirect, MDPI, SpringerLink, arXiv, ResearchGate. Terms: energy-aware scheduling, multi-objective job-shop, ToU scheduling, peak-demand scheduling, robust scheduling, rolling-horizon manufacturing, measured power scheduling, edge computing scheduling, MSME energy, closed-loop scheduling.

**Limitation:** No direct IEEE Xplore or ACM DL API access. Some papers may be missed. Absence of evidence ≠ evidence of absence.

### 1.2 Evidence table

| # | Work / Area | Model | Objectives | Uncertainty? | Measured power? | Physical execution? | Key limitation |
|---|---|---|---|---|---|---|---|
| 1 | Mouzon et al. (2007, IIE Trans.) | Single-machine ON/OFF MILP | Energy | No | No | No | Single machine; no ToU; foundational |
| 2 | Gahm et al. (2016, EJOR) | Survey: 100+ papers | Various | Rarely | Rarely | No | Pre-2016 snapshot; most work deterministic |
| 3 | Machine-state MILP (MDPI 2023–24) | Job-shop + idle/startup states | Makespan + Energy | No | No | No | Standard formulation; Western tariffs |
| 4 | Period-indexed ToU MILP (SciTePress 2024) | ToU-aware scheduling | Energy cost | No | No | No | Computational-only |
| 5 | Multi-obj green scheduling (MDPI 2023) | Bi-obj FJSP | Makespan + Energy | No | No | No | NSGA-II on benchmarks only |
| 6 | AUGMECON ε-constraint studies (2022–24) | Multi-obj MILP | Cost + Emissions (+ Peak in some) | Rarely | No | No | Peak as objective exists but is less explored in manufacturing scheduling specifically |
| 7 | DRL + rolling horizon (MDPI 2024) | Dynamic scheduling MDP | Makespan + Energy | Machine breakdown | Digital twin | Simulated | Complex; not student-feasible |
| 8 | Robust FJSP (Atlantis Press 2024) | Robust MILP / scenario-based | Makespan robustness | Processing time | No | No | No energy awareness |
| 9 | Energy + production co-scheduling (arXiv 2024) | MILP with decision-dependent uncertainty | Cost | Energy price | No | Simulation | Advanced; limited applicability |
| 10 | MPC-based scheduling (arXiv 2024) | Receding horizon QP/MILP | Energy cost | Price volatility | No | Simulation | Requires real-time solver |
| 11 | Event-based load disaggregation (GI.de 2024) | Data-driven power profiling | Accuracy | N/A | **Yes** — measured | Lab testbed | Profiling only, not scheduling |
| 12 | Demand charge peak shaving (various 2022–24) | MILP with P_peak variable | Energy + Demand charge | Some (BESS) | Mixed | Mostly simulation | Focus on building/grid, not production scheduling |
| 13 | RPi edge scheduling (various 2024) | CP-SAT / lightweight heuristics | Various | Limited | No | Some lab demos | Performance-limited vs desktop |
| 14 | India ToD tariff rules (MoP, April 2024) | Regulatory — not academic | N/A | N/A | N/A | N/A | Mandatory ToD for ≥10 kW; demand charges documented |

### 1.3 What is already solved

These are `[ESTABLISHED]` and should not be claimed as contributions:

1. **Bi-objective makespan + energy MILP** — Solved since Mouzon (2007), refined extensively.
2. **Machine-state energy models** (idle/processing/startup/off) — Standard since ~2016.
3. **ε-constraint and NSGA-II/III for Pareto fronts** — Textbook multi-objective methodology.
4. **ToU-aware scheduling** — Dozens of papers; standard formulation.
5. **Job-shop scheduling NP-hardness and solver behavior** — Well-characterised.
6. **PZEM-004T + ESP32 power monitoring** — Widely documented hobbyist/industrial pattern.
7. **MQTT + Raspberry Pi + dashboard** — Standard IoT stack. Not research.
8. **Demand charge peak-shaving formulation** (P_peak ≥ Σ P_m(t)) — Standard in energy systems literature.

### 1.4 What is less studied (genuine gaps)

These are `[OBSERVED GAP]` with varying confidence:

1. **Tri-objective manufacturing scheduling (makespan + energy cost + peak demand) with systematic Pareto surface analysis** — Peak demand as explicit objective in *production scheduling* (not building energy or microgrid) is less explored than bi-objective. Multiple papers mention it, but rigorous 3D Pareto analysis with sensitivity to tariff parameters is uncommon. **Confidence: Moderate.**

2. **Physical execution of an energy-aware schedule on a testbed with measured validation** — Virtually all papers use simulation or benchmark instances. Papers that measure real machine power exist, but papers that *execute the optimized schedule physically and compare predicted vs. actual energy* are rare. **Confidence: High.**

3. **Systematic study of when peak-awareness matters and when it doesn't** — No paper I found produces a sensitivity map showing: "Peak-demand awareness provides X% bill reduction when demand charges are Y ₹/kVA and tariff differential is Z." This parametric analysis is absent. **Confidence: Moderate-High.**

4. **Static vs. adaptive scheduling comparison with energy objectives on a physical testbed** — Comparisons exist in simulation/DRL contexts, but not on student-scale physical systems with measured feedback. **Confidence: Moderate.**

### 1.5 Honesty check

None of these gaps constitute algorithmic novelty. They are:
- Extensions of existing formulations to a third objective
- Empirical/validation studies that close the simulation-to-reality gap
- Parametric sensitivity analyses that characterise when a method is useful

This is honest, defensible undergraduate work. It is **not** a new algorithm, **not** a new mathematical technique, and **not** a breakthrough. Framing it otherwise would be dishonest.

---

## TASK 2 — Mathematical Research Gap

### 2A. Peak-aware scheduling: Is there a real research question?

**The claim to investigate:** Adding peak demand as a third objective changes the Pareto front in a non-trivial way.

**Why this might be true:**
- `[ESTABLISHED]` Indian industrial tariffs have two components: energy charges (kWh × ToD rate) and demand charges (peak kVA × ₹/kVA/month).
- `[ESTABLISHED]` Demand charges are 30%+ of industrial bills in many Indian states.
- `[INFERENCE]` Minimising energy cost alone can *increase* peak demand. Example: if all energy-intensive operations are packed into cheap off-peak slots, they overlap and create a power spike. The energy charge drops, but the demand charge rises.
- `[HYPOTHESIS]` There is a structural trade-off between energy cost and peak demand that produces a distinct Pareto surface region: schedules exist that slightly increase total kWh cost but substantially reduce peak demand, lowering the total bill.

**Why this might be false:**
- If the machine count is small (3–5), the peak power range is narrow, and the demand charge component may be negligible.
- If processing times are short relative to time slots, there is little overlap.
- If tariff differential is small, energy-aware scheduling itself provides little benefit.

**Verdict:** This is a testable hypothesis, not an assumed truth. The research question is: *Under what conditions does peak-demand awareness provide meaningful total-bill reduction beyond energy-cost-only optimization?* The answer "it doesn't matter for small systems" is a valid finding.

### 2B. Uncertainty: Is it feasible?

**Scenario-based robust scheduling** (sample K scenarios of processing time, solve a min-max or expectation formulation) is conceptually straightforward but:

- Multiplies MILP complexity by K.
- Requires distributional assumptions (what distribution do processing times follow?).
- Validation requires running the perturbed instances — feasible computationally but hard to replicate physically.

**Verdict:** Feasible as a computational experiment (Monte Carlo perturbation of the deterministic solution). NOT feasible as a full stochastic MILP for undergraduates. Suitable for Level 3 (stretch), not core.

### 2C. Static vs. Adaptive: Is there a real research question?

**The ideal experiment:**
1. Generate static schedule S*.
2. Execute S* on testbed.
3. Inject perturbation (e.g., delay one machine by 2 time slots).
4. Measure the degradation in cost/peak/makespan.
5. Generate adaptive schedule S'_t by re-solving with updated state.
6. Compare S* degraded vs. S'_t adapted.

**Why this is valuable:** It directly answers whether re-optimization after disruption helps — a question most papers answer only in simulation.

**Why this is risky:** 
- Implementation complexity is high (state estimation, trigger logic, solver speed).
- On a small testbed with 3 machines, the adaptation may be trivial (just swap two operations).
- The improvement may be too small to detect statistically.

**Verdict:** Genuine research question but HIGH risk for undergraduates. Reserve for Level 4. The core project must not depend on this.

### 2D. The strongest research question (synthesis)

After analysing all three directions, the strongest mathematically defensible and undergraduate-feasible research question is:

> **Under realistic industrial tariff structures with demand charges, does peak-demand-aware multi-objective scheduling produce a structurally different Pareto front and lower total electricity bill compared to energy-cost-only scheduling — and under what tariff conditions does this benefit become significant?**

This is:
- Mathematically precise (Pareto analysis, hypervolume comparison, sensitivity)
- Falsifiable (null hypothesis: no significant difference)
- Parameterically rich (can sweep demand-charge rate, tariff ratio, workload intensity)
- Physically validatable (execute both schedules on testbed, measure actual peak and cost)
- Feasible with standard tools (MILP + AUGMECON + Gurobi/OR-Tools)

It is NOT:
- A new algorithm
- A new solver
- A new heuristic

It IS:
- An extended formulation study with systematic empirical analysis
- An experimental comparison with physical validation

---

## TASK 3 — Mathematical Formulation

### Sets

| Symbol | Definition |
|---|---|
| $\mathcal{J} = \{1, \ldots, n\}$ | Jobs |
| $\mathcal{O}_j = \{1, \ldots, n_j\}$ | Operations of job $j$ (ordered) |
| $\mathcal{M} = \{1, \ldots, m\}$ | Machines |
| $\mathcal{T} = \{1, \ldots, H\}$ | Discrete time slots of width $\Delta$ |
| $\mathcal{M}_o \subseteq \mathcal{M}$ | Eligible machines for operation $o$ |

### Parameters

| Symbol | Definition | Source |
|---|---|---|
| $p_o$ | Processing time of operation $o$ (in time slots) | Modelled / estimated |
| $P^{\text{proc}}_m$ | Processing power draw of machine $m$ (W) | **Measured** via PZEM-004T |
| $P^{\text{idle}}_m$ | Idle power draw of machine $m$ (W) | **Measured** |
| $E^{\text{start}}_m$ | Startup energy of machine $m$ (Wh) | **Measured** |
| $\pi_t$ | Electricity price in slot $t$ (₹/kWh) | From SERC tariff order |
| $\rho$ | Demand charge rate (₹/kW/month) | From SERC tariff order |
| $d_j$ | Deadline for job $j$ (time slot) | Modelled |
| $\Delta$ | Time slot width (hours) | Design choice (e.g., 0.25 h = 15 min) |

### Decision variables

| Variable | Domain | Meaning |
|---|---|---|
| $x_{omt}$ | $\{0,1\}$ | Operation $o$ starts on machine $m$ at time $t$ |
| $y_{mt}$ | $\{0,1\}$ | Machine $m$ is processing during slot $t$ |
| $w_{mt}$ | $\{0,1\}$ | Machine $m$ is idle (on, not processing) during slot $t$ |
| $z_{mt}$ | $\{0,1\}$ | Machine $m$ has a startup transition at slot $t$ |
| $C_{\max}$ | $\mathbb{R}^+$ | Makespan |
| $P^{\text{peak}}$ | $\mathbb{R}^+$ | Peak total power over all time slots |

### Objective functions

**F1 — Makespan:**

$$\min\ C_{\max}$$

**F2 — Electricity cost (energy charge only):**

$$\min\ \sum_{t \in \mathcal{T}} \sum_{m \in \mathcal{M}} \Big[ P^{\text{proc}}_m \cdot y_{mt} + P^{\text{idle}}_m \cdot w_{mt} + \tfrac{E^{\text{start}}_m}{\Delta} \cdot z_{mt} \Big] \cdot \pi_t \cdot \Delta$$

**F3 — Peak power:**

$$\min\ P^{\text{peak}}$$

**Total bill (for evaluation, not directly optimised):**

$$\text{Bill} = F2 + \rho \cdot P^{\text{peak}}$$

### Constraints

**C1 — Assignment:** Each operation assigned exactly once.
$$\sum_{m \in \mathcal{M}_o} \sum_{t \in \mathcal{T}} x_{omt} = 1 \qquad \forall\ o$$

**C2 — Precedence:** Operations within a job respect ordering.
$$\sum_{m,t} x_{o_k m t} \cdot (t + p_{o_k}) \leq \sum_{m,t} x_{o_{k+1} m t} \cdot t \qquad \forall\ j,\ k < n_j$$

(Note: this constraint is bilinear in the general form. For time-indexed formulations, it linearises because $x_{omt}$ selects a unique $t$.)

**C3 — No overlap:** At most one operation on each machine at any time.
$$\sum_{o : m \in \mathcal{M}_o}\ \sum_{\tau=\max(1,t-p_o+1)}^{t} x_{om\tau} \leq 1 \qquad \forall\ m,\ t$$

**C4 — Processing state link:**
$$y_{mt} = \sum_{o : m \in \mathcal{M}_o}\ \sum_{\tau=\max(1,t-p_o+1)}^{t} x_{om\tau} \qquad \forall\ m,\ t$$

**C5 — State exclusivity:**
$$y_{mt} + w_{mt} \leq 1 \qquad \forall\ m,\ t$$

(Machine is either processing, idle, or off. Off is the implicit third state: $1 - y_{mt} - w_{mt}$.)

**C6 — Startup detection:**
$$z_{mt} \geq (y_{mt} + w_{mt}) - (y_{m,t-1} + w_{m,t-1}) \qquad \forall\ m,\ t > 1$$

**C7 — Makespan:**
$$C_{\max} \geq \sum_{m,t} x_{omt} \cdot (t + p_o) \cdot \Delta \qquad \forall\ o = \text{last operation of some job}$$

**C8 — Peak power (the proposed extension):**
$$P^{\text{peak}} \geq \sum_{m \in \mathcal{M}} \Big[ P^{\text{proc}}_m \cdot y_{mt} + P^{\text{idle}}_m \cdot w_{mt} + \tfrac{E^{\text{start}}_m}{\Delta} \cdot z_{mt} \Big] \qquad \forall\ t$$

**C9 — Deadline (optional):**
$$\sum_{m,t} x_{omt} \cdot (t + p_o) \cdot \Delta \leq d_j \qquad \forall\ j,\ o = \text{last}(j)$$

### Multi-objective solution method

**AUGMECON (Augmented ε-constraint):**

For a 3-objective problem, fix one objective as primary (e.g., $F2$), treat $F1$ and $F3$ as ε-bounded constraints:

$$\min\ F2 - \delta \cdot (s_1/r_1 + s_2/r_2)$$

subject to: $F1 \leq \varepsilon_1 + s_1$, $F3 \leq \varepsilon_3 + s_3$, plus all scheduling constraints.

Grid $\varepsilon_1$ over $[F1^{\min}, F1^{\max}]$ and $\varepsilon_3$ over $[F3^{\min}, F3^{\max}]$ with $k$ steps each → $k^2$ MILP solves.

**Why AUGMECON, not weighted-sum:**
- `[ESTABLISHED]` Weighted-sum cannot find solutions on non-convex Pareto regions. Job-shop Pareto fronts are typically non-convex.
- `[ESTABLISHED]` AUGMECON guarantees Pareto-efficient solutions and avoids weakly-dominated points.
- `[ESTABLISHED]` For 3 objectives, AUGMECON with $k=10$ per dimension requires 100 MILP solves. At 10–60 seconds each for small instances (5×3 to 10×5), total runtime: 15–100 minutes. Feasible on laptop or RPi 5 with OR-Tools.

**Why not NSGA-III:**
- NSGA-III is appropriate for large instances where MILP is intractable.
- For the core research question (does peak-awareness change the Pareto structure?), exact solutions are preferable because they remove the noise of metaheuristic approximation.
- Use NSGA-III only for scalability experiments (Level 2+).

### Complexity

`[ESTABLISHED]` Job-shop scheduling is NP-hard. The time-indexed MILP has $O(n \cdot m \cdot H)$ binary variables. For 10 jobs × 5 machines × 48 time slots (12-hour horizon with 15-min slots): ~2,400 binaries. Gurobi solves this in seconds. OR-Tools CP-SAT handles similar scale.

Adding the $P^{\text{peak}}$ variable and C8 constraints adds $H$ linear constraints and one continuous variable — negligible overhead.

### Assumptions (stated honestly)

| Assumption | Realistic? | What happens if violated | Mitigation |
|---|---|---|---|
| Deterministic processing times | No (real times vary ±10-30%) | Schedule may miss deadlines | Uncertainty experiment (Level 3) |
| Constant $P^{\text{proc}}_m$ during processing | Approximately (steady-state motors/heaters) | Energy estimate error | Use measured average; report error |
| No machine breakdowns | Unrealistic for long horizons | Schedule becomes infeasible | Excluded; acknowledge limitation |
| Jobs known in advance | Yes for batch manufacturing | N/A | Appropriate for MSME batch |
| Piecewise-constant tariff | Yes — Indian ToD tariffs are block rates | N/A | Matches real tariff structure |
| Demand charge on peak kW | Yes — standard Indian industrial billing | N/A | Verified from SERC tariff orders |

---

## TASK 4 — Level Hierarchy

### Level 1 — Minimum Viable Research

**What it is:** Bi-objective MILP (makespan + energy cost) + FCFS/SPT baselines + synthetic instances + statistical comparison.

| Dimension | Assessment |
|---|---|
| Mathematical difficulty | Low-Medium. Standard MILP; ε-constraint is textbook. |
| Implementation difficulty | Low. PuLP or OR-Tools; 200–400 lines of Python. |
| Hardware | None required. |
| Data | Synthetic instances + published Indian tariff data. |
| Experiments | Model comparison across 60+ instances (3 sizes × 20 random). |
| Research contribution | **Nil.** This is a known formulation with known results. It only verifies that MILP beats heuristics — already proven hundreds of times. |
| Risk of failure | Very low — but contribution is also very low. |

**Verdict:** Necessary foundation. Not sufficient alone.

### Level 2 — Strong Project

**What it adds to Level 1:**
- **Third objective: peak demand** (F3 + constraint C8)
- **3D Pareto surface** via AUGMECON
- **Physical testbed** with measured power profiles
- **Physical schedule execution** (ESP32 → relays → loads → PZEM-004T)
- **Predicted vs. actual energy comparison**
- **Sensitivity analysis:** sweep demand-charge rate ρ and tariff ratio

| Dimension | Assessment |
|---|---|
| Mathematical difficulty | Medium. Tri-objective AUGMECON with parametric sweep. |
| Implementation difficulty | Medium. Hardware integration + multi-run experiments. |
| Hardware | ESP32, PZEM-004T, relay module, 3–4 loads (~₹2,300). Optional: RPi. |
| Data | Measured power profiles + synthetic instances + real tariff. |
| Experiments | 6 experiments (see Task 5). |
| Research contribution | **Empirical contribution + engineering integration.** Systematic Pareto analysis + physical validation + sensitivity characterisation. Not algorithmic novelty. |
| Risk of failure | Low-Medium. Peak-demand benefit may be negligible for small testbed — but characterising *when* it matters is itself a result. |

**Verdict: This is the target level.** Strong enough for a high-scoring undergraduate project with genuine analytical depth and physical validation.

### Level 3 — Advanced

**What it adds to Level 2:**
- **Uncertainty experiment:** Monte Carlo perturbation of processing times. Evaluate deterministic schedule under K=100 scenarios. Measure expected cost, worst-case cost, deadline violation rate.
- **NSGA-III for larger instances** (20×8, 50×10): scalability study.
- **Hypervolume indicator comparison** between exact (AUGMECON) and approximate (NSGA-III).

| Dimension | Assessment |
|---|---|
| Mathematical difficulty | Medium-High. Scenario evaluation requires scripting. NSGA-III via pymoo requires parameter tuning. |
| Implementation difficulty | Medium. Computational but no new hardware. |
| Research contribution | **Methodological contribution** (comparison of exact vs. approximate on energy-peak scheduling). |
| Risk of failure | Low for computation; moderate for finding meaningful differences. |

**Verdict:** Valuable addition if Level 2 is complete by week 7. Do not attempt if Level 2 is shaky.

### Level 4 — Stretch (Rolling-Horizon Adaptive)

**What it adds to Level 3:**
- **Event-triggered rescheduling:** Inject a disruption (delay one machine by N slots). Detect via measured state. Re-solve remaining schedule on RPi. Compare adapted vs. original.
- **State estimation loop:** ESP32 reports machine states via MQTT; RPi maintains system state; optimizer uses current state as initial condition.

| Dimension | Assessment |
|---|---|
| Mathematical difficulty | High. Rolling-horizon MILP requires warm-starting, state bookkeeping, and solving under deadline. |
| Implementation difficulty | High. Full MQTT pipeline, state machine, trigger logic, solver integration, error handling. |
| Research contribution | **Genuine empirical research question** — does rescheduling help on this scale? But answer may be "no" for small testbed. |
| Risk of failure | **High.** Integration complexity is the main risk. Single-point-of-failure: if MQTT drops or solver is too slow, demo fails. |

**Verdict:** Attempt ONLY if Levels 1–3 are rock-solid and time remains. Do NOT build the project around this.

---

## TASK 5 — Experiments

### Experiment 1 — Does energy-aware scheduling beat heuristics?

| Item | Detail |
|---|---|
| Independent variable | Scheduling method: FCFS, SPT, LPT, Makespan-MILP, Bi-obj-MILP |
| Dependent variables | Makespan, energy cost, peak power, total bill |
| Instances | 20 random instances × 3 sizes: 5×3, 8×4, 10×5 |
| Statistical method | Wilcoxon signed-rank test (paired), α = 0.05 |
| Hypothesis | Bi-obj-MILP reduces energy cost by >10% vs FCFS with <15% makespan increase |
| Falsifiability | If energy cost reduction < 5% on >50% of instances, the MILP provides negligible practical benefit |
| Purpose | Establish that energy-aware scheduling provides measurable benefit. **Baseline validation.** |

### Experiment 2 — Does peak-demand awareness change the Pareto front?

| Item | Detail |
|---|---|
| Independent variable | Number of objectives: 2-obj (F1, F2) vs 3-obj (F1, F2, F3) |
| Dependent variables | Pareto front structure (hypervolume), total bill |
| Instances | Same 60 instances |
| Statistical method | Paired Wilcoxon on total bill; hypervolume comparison |
| Hypothesis | 3-obj scheduling produces different Pareto-efficient solutions that reduce total bill (energy + demand charge) |
| Falsifiability | If hypervolume difference < 2% and total bill difference is not significant (p > 0.05), peak awareness adds nothing |
| Purpose | **Core research question.** |

### Experiment 3 — Sensitivity to demand-charge rate

| Item | Detail |
|---|---|
| Independent variable | $\rho$ ∈ {0, 50, 100, 150, 200, 250, 300, 400, 500} ₹/kW/month |
| Dependent variable | Total bill difference: 2-obj solution evaluated vs 3-obj solution |
| Instances | Fixed set of 10 medium instances (8×4) |
| Analysis | Plot bill savings vs ρ. Identify threshold ρ* below which savings < 5% |
| Hypothesis | Benefit of peak-awareness increases monotonically with ρ; there exists ρ* below which it is negligible |
| Falsifiability | If benefit is flat (constant or random) across ρ, the relationship does not exist |
| Purpose | **Characterise when peak-awareness matters.** |

### Experiment 4 — Sensitivity to tariff differential

| Item | Detail |
|---|---|
| Independent variable | Peak/off-peak price ratio ∈ {1.0, 1.1, 1.2, 1.3, 1.5, 1.8, 2.0} |
| Dependent variable | Energy cost savings: energy-aware vs FCFS |
| Instances | Same 10 medium instances; fixed ρ at Karnataka BESCOM rate |
| Hypothesis | Savings increase with tariff differential; at ratio ≈ 1.0, savings approach zero |
| Falsifiability | If savings are significant even at ratio 1.0, then scheduling benefit is independent of tariff structure (contradicts model) |
| Purpose | Determine whether ToU differential is the main driver or whether machine-state management alone provides benefit. |

### Experiment 5 — Energy model fidelity

| Item | Detail |
|---|---|
| Independent variable | Energy model: (A) constant power, (B) measured idle + processing, (C) B + measured startup |
| Dependent variable | Prediction error: |predicted energy − measured energy| / measured energy |
| Procedure | Generate 10 schedules using model A. Execute physically. Compute prediction error for A, B, C. |
| Hypothesis | Measured profiles (B, C) reduce prediction error below 10%; constant-power (A) has >20% error |
| Falsifiability | If all three models have similar error (<5% difference), measured profiles add no value |
| Purpose | Justify (or reject) the physical measurement layer. |

### Experiment 6 — Scalability (Level 3)

| Item | Detail |
|---|---|
| Independent variable | Instance size: 5×3, 8×4, 10×5, 15×6, 20×8, 30×10, 50×10 |
| Dependent variables | Solver time (s), optimality gap (%), memory (MB), hypervolume |
| Solvers | OR-Tools CP-SAT (on RPi 5 and laptop), NSGA-III via pymoo (laptop) |
| Analysis | Log-log plot of time vs. size; identify crossover where exact becomes intractable |
| Purpose | Determine feasible problem scale for each solver and platform. |

---

## TASK 6 — Physical Prototype

### What it is and what it is NOT

This is a **programmable machine-load emulation testbed.** It uses controllable electrical loads to emulate machine behavior (processing, idle, startup, off). It is NOT a factory, NOT a production line, and should NOT be presented as one.

**What it proves:**
1. The energy model (P_proc, P_idle, E_start) can be measured from real loads.
2. The optimised schedule can be physically executed via controller + relays.
3. The predicted energy consumption matches the measured energy consumption.
4. The predicted peak power matches the measured peak power.
5. The difference between baseline and optimised schedules is physically observable.

**What it does NOT prove:**
- That the method works in a real factory.
- That the improvement percentages transfer to industrial machines.
- That the tariff savings are industrially significant.

### Architecture

```
┌──────────────┐        Serial/UART       ┌─────────────────┐
│  PZEM-004T   │◄────────────────────────►│     ESP32        │
│  (V, I, P,   │                          │  - Read PZEM     │
│   E, PF)     │                          │  - Control relays│
└──────┬───────┘                          │  - MQTT publish  │
       │ measures                         │  - State report  │
       ▼                                  └────────┬────────┘
┌──────────────┐                                   │ WiFi/MQTT
│  4ch Relay   │◄──── GPIO ────────────────────────┘
│  Module      │                                   │
└──────┬───────┘                          ┌────────▼────────┐
       │ switches                         │  Raspberry Pi 5  │
       ▼                                  │  - MQTT broker   │
┌──────────────┐                          │  - OR-Tools      │
│  Load 1:     │                          │  - Scheduler     │
│  DC Motor    │                          │  - Database      │
│  (12V, ~2A)  │                          │  - Dashboard     │
├──────────────┤                          └─────────────────┘
│  Load 2:     │
│  Heater coil │
│  (12V, ~3A)  │
├──────────────┤
│  Load 3:     │
│  LED array   │
│  (12V, ~1A)  │
├──────────────┤
│  Load 4:     │
│  Fan/pump    │
│  (12V, ~1.5A)│
└──────────────┘
```

**Safety:** All loads are 12V DC, powered from a bench supply or battery. The PZEM-004T measures the DC supply line (or a separate AC line if using small AC loads with appropriate isolation). No mains voltage exposure.

**Alternative for AC measurement:** Use small AC loads (desk lamp, small fan, soldering iron on low) with the PZEM-004T on the AC side, housed in an insulated enclosure. This gives more realistic AC power factor data.

### BOM

| Component | Qty | Unit (₹) | Total (₹) | Purpose |
|---|---|---|---|---|
| ESP32-WROOM-32 | 1 | 500 | 500 | Controller: relay control, PZEM reading, MQTT |
| PZEM-004T v3 (100A CT) | 1 | 500 | 500 | Power measurement: V, I, P, E |
| 4-channel relay module | 1 | 200 | 200 | Load switching |
| DC motor (775, 12V) | 1 | 250 | 250 | Load 1: emulates motor-type machine |
| Ceramic heater element (12V) | 1 | 100 | 100 | Load 2: emulates thermal process |
| LED strip (12V, 1m) | 1 | 150 | 150 | Load 3: emulates light-duty machine |
| 12V DC fan | 1 | 100 | 100 | Load 4: emulates auxiliary equipment |
| 12V 10A power supply | 1 | 300 | 300 | Power for all loads |
| Breadboard + jumper wires | 1 | 200 | 200 | Prototyping |
| **Total** | | | **₹2,300** | |
| Raspberry Pi 5 (borrowed) | 1 | 0 | 0 | Optimization server |

### Data classification

| Category | What | Source | Justification |
|---|---|---|---|
| **REAL (measured)** | P_proc, P_idle, E_start for each load; actual energy per schedule execution; actual peak power; actual ON/OFF timing | PZEM-004T + ESP32 timestamps | Direct physical measurement of the system under control |
| **MODELLED (real-world sources)** | Processing times; job precedence; tariff rates; demand charge rates; deadlines | Designed + SERC tariff orders | Processing times are design parameters of the experiment; tariffs are publicly documented |
| **SIMULATED** | Large-scale instances (20+ jobs); uncertainty scenarios; tariff sweeps | Python scripts | Cannot physically build 50 machines; simulation extends results using the measured energy model |

---

## TASK 7 — Raspberry Pi Role Analysis

### Possible roles and honest assessment

| Role | Justified? | Reasoning |
|---|---|---|
| **Optimization server** | **YES — if solver actually runs on it** | Running OR-Tools CP-SAT on RPi 5 to solve 10×5 instances in real-time demonstrates edge-feasible scheduling. This is technically meaningful: it shows the optimizer doesn't require a cloud server. Benchmark: solve time on RPi vs. laptop. |
| **MQTT broker** | **Marginal** | Mosquitto on RPi is trivial. Not a research contribution, but necessary infrastructure. |
| **Local database** | **No — not research** | SQLite/InfluxDB for logging. Useful but not a contribution. |
| **State estimator** | **Only at Level 4** | Needed for rolling-horizon rescheduling. Not justified at Level 2. |
| **Dashboard server** | **No — not research** | Flask/Grafana for display. Useful for demo, not a contribution. |
| **Experiment controller** | **YES — practical** | Orchestrates run sequences, logs results, triggers ESP32. Useful engineering. |

### Verdict

**The RPi is justified as the optimization server** if and only if:
1. The solver actually runs on it (OR-Tools CP-SAT — confirmed feasible on ARM64).
2. You report solve time on RPi vs. laptop as a scalability result.
3. You demonstrate that the schedule is generated *on the RPi* and sent to the ESP32 for execution.

**This makes the RPi an edge scheduler**, which is technically defensible. It is NOT research novelty — it is engineering integration.

**Gurobi does NOT run on ARM.** Use OR-Tools CP-SAT or PuLP + CBC (both support ARM64 natively).

### Honest framing

> "We deploy the multi-objective scheduler on a Raspberry Pi 5 to demonstrate that energy-aware scheduling is computationally feasible on low-cost edge hardware, eliminating the need for cloud infrastructure."

This is **engineering integration**, not algorithmic novelty.

---

## TASK 8 — Falsifiable Research Questions

### RQ1 — Peak-demand Pareto structure

**Question:** Does adding peak demand as a third scheduling objective produce a Pareto surface that is structurally distinct from the bi-objective (makespan, energy cost) Pareto front?

- **IV:** Number of objectives (2 vs 3)
- **DV:** Hypervolume indicator, number of Pareto-efficient solutions, total bill
- **Baseline:** 2-objective AUGMECON solution set
- **Outcome:** Hypervolume difference and bill comparison
- **Hypothesis:** The 3-objective Pareto surface occupies a distinct region of solution space, and at least 20% of its solutions are not dominated by any 2-objective solution when evaluated on total bill (energy + demand charge).
- **Falsification:** If all 3-obj solutions are dominated by some 2-obj solution on total bill, peak-awareness adds no value.

### RQ2 — Demand-charge threshold

**Question:** At what demand-charge rate (₹/kW/month) does peak-demand-aware scheduling begin to provide statistically significant total-bill reduction?

- **IV:** Demand charge rate ρ
- **DV:** Total bill savings (2-obj vs 3-obj)
- **Baseline:** 2-objective optimal schedule evaluated at each ρ
- **Outcome:** Threshold ρ* identified via regression or segmented analysis
- **Hypothesis:** There exists a threshold ρ* such that for ρ > ρ*, the 3-objective solution reduces total bill by >5%.
- **Falsification:** If no threshold exists (benefit is negligible at all ρ, or always significant), the relationship is trivial.

### RQ3 — Energy model fidelity

**Question:** Does using measured machine power profiles significantly improve the accuracy of schedule energy predictions compared to constant-power assumptions?

- **IV:** Energy model variant (constant vs. measured idle+processing vs. measured+startup)
- **DV:** Prediction error |predicted − measured| / measured
- **Baseline:** Constant-power model with datasheet values
- **Outcome:** Prediction error comparison
- **Hypothesis:** Measured profiles reduce prediction error to <10%; constant-power exceeds 20%.
- **Falsification:** If constant-power error is already <10%, measurement adds no value for scheduling.

### RQ4 — Tariff differential sensitivity

**Question:** Below what peak/off-peak tariff ratio does energy-aware scheduling fail to provide meaningful cost savings over FCFS?

- **IV:** Peak/off-peak price ratio (1.0 to 2.0)
- **DV:** Energy cost savings (MILP vs FCFS)
- **Baseline:** FCFS scheduling
- **Outcome:** Savings vs ratio curve; identify ratio below which savings < 3%
- **Hypothesis:** Savings are <3% when ratio < 1.1 and increase approximately linearly with ratio above 1.2.
- **Falsification:** If savings are >10% even at ratio 1.0, the benefit comes from machine-state management, not tariff exploitation (a valid alternative finding).

### RQ5 — Edge solver feasibility

**Question:** Can OR-Tools CP-SAT on Raspberry Pi 5 solve the tri-objective scheduling MILP to within 1% optimality gap in under 60 seconds for instances up to 10 jobs × 5 machines?

- **IV:** Instance size (5×3 to 15×6)
- **DV:** Solve time, optimality gap, solution quality vs laptop
- **Baseline:** Same solver on laptop (Intel i5/i7)
- **Outcome:** Speed ratio (RPi/laptop) and maximum feasible instance size
- **Hypothesis:** RPi 5 solves 10×5 instances in <60s with <1% gap.
- **Falsification:** If RPi cannot solve 8×4 within 120s, edge deployment is not feasible for this formulation.

### RQ6 — Schedule robustness (Level 3)

**Question:** Does the deterministic energy-aware schedule remain cost-effective when processing times are perturbed by ±20%?

- **IV:** Perturbation level (0%, 5%, 10%, 15%, 20%, 30%)
- **DV:** Expected cost overrun, deadline violation rate, peak demand exceedance
- **Baseline:** Deterministic optimal schedule evaluated under perturbation scenarios (K=100)
- **Outcome:** Cost overrun and violation rate vs perturbation level
- **Hypothesis:** Below 15% perturbation, cost overrun is <8% and violations are <10%. Above 20%, degradation is significant.
- **Falsification:** If the schedule is robust even at 30% (overrun <5%), uncertainty-aware extensions are unnecessary for this problem scale.

---

## TASK 9 — Novelty Audit

| Component | Classification | Honest statement |
|---|---|---|
| **MILP formulation for job-shop scheduling** | `ESTABLISHED` | Standard since 1960s. Not novel. |
| **Machine-state energy model (idle/processing/startup/off)** | `ESTABLISHED` | Standard since ~2016. Not novel. |
| **ε-constraint / AUGMECON for multi-objective** | `ESTABLISHED` | Textbook methodology (Mavrotas, 2009). Not novel. |
| **ToU-aware scheduling** | `ESTABLISHED` | Dozens of papers. Not novel. |
| **NSGA-II/III for scheduling** | `ESTABLISHED` | Textbook. Not novel. |
| **Peak demand as minimax variable** | `ESTABLISHED` | Used in energy systems. Less common in *manufacturing scheduling* specifically but the formulation (P_peak ≥ Σ P(t)) is standard. |
| **ESP32 + PZEM-004T power monitoring** | `ESTABLISHED` | Well-documented IoT pattern. Not novel. |
| **Raspberry Pi as edge optimizer** | `ENGINEERING INTEGRATION` | Running a solver on ARM is not research. Benchmarking its performance for scheduling is a minor empirical contribution. |
| **MQTT + relay control of loads** | `ENGINEERING INTEGRATION` | Standard automation. Not novel. |
| **Dashboard / Gantt visualisation** | `ENGINEERING INTEGRATION` | Not novel. |
| **Indian ToU tariff parameterisation** | `CONTEXTUAL NOVELTY` | Applying known model to Indian tariff data. The parameters are new; the mathematics is not. |
| **Tri-objective Pareto surface for manufacturing scheduling** | `EMPIRICAL CONTRIBUTION` | The specific analysis (3D Pareto + sensitivity to demand-charge rate) on manufacturing scheduling instances with measured power data appears under-explored. This is NOT algorithmic novelty — it is a systematic empirical study of an extended formulation. |
| **Physical schedule execution + predicted vs actual comparison** | `EMPIRICAL CONTRIBUTION` | Rare in the literature. Most papers are simulation-only. Physically executing and validating is a genuine engineering contribution. |
| **Demand-charge threshold characterisation** | `EMPIRICAL CONTRIBUTION` | Identifying *when* peak-awareness matters is a parametric study that appears absent from the literature. Not algorithmic novelty. |
| **Sensitivity analysis across tariff structures** | `EMPIRICAL CONTRIBUTION` | Characterising the problem space rather than proposing a new solution. Valid empirical research. |

### Summary of honest framing

> This project does NOT propose a new algorithm, a new solver, or a new mathematical technique. Every component is individually established. The contribution is: (1) a systematic empirical study of the tri-objective makespan-cost-peak trade-off under realistic industrial tariff structures, (2) parametric sensitivity analysis characterising when peak-demand awareness provides meaningful benefit, and (3) physical validation of an energy-aware schedule on a measured testbed. This is an **extended formulation study with empirical validation**, not an algorithmic innovation.

---

## TASK 10 — Final Project Architecture

### 1. Problem

Indian MSMEs face electricity costs comprising energy charges (kWh-based, ToD-differentiated) and demand charges (peak kW-based). Production scheduling in these settings ignores energy costs entirely (FCFS/manual). Optimised scheduling can reduce both components, but minimising energy cost alone may increase peak demand, raising the total bill.

### 2. Existing approaches

Bi-objective scheduling (makespan + energy) is extensively studied. Machine-state energy models are standard. Peak demand is addressed in energy systems but less explored as a production scheduling objective. Physical validation of energy-aware schedules is rare.

### 3. Exact research gap

No systematic study characterises (a) the structure of the tri-objective Pareto surface for manufacturing scheduling with peak demand, (b) under what tariff conditions peak-demand awareness provides significant total-bill reduction, or (c) validates the predicted energy savings of an optimised schedule against physical measurements on a testbed.

### 4. Mathematical formulation

See Task 3. Tri-objective MILP with AUGMECON. Seven constraint families. Three objective functions.

### 5. Proposed method

AUGMECON with OR-Tools CP-SAT as MILP solver. Parametric sweep over demand-charge rate and tariff differential. Physical execution on testbed. Predicted vs. actual comparison.

### 6. Physical prototype

Machine-load emulation testbed: 4 controllable loads (DC motor, heater, LED, fan) + PZEM-004T + ESP32 + relay module. ~₹2,300 BOM.

### 7. Raspberry Pi role

**Local optimization server.** Runs OR-Tools CP-SAT to solve the scheduling MILP. Serves as MQTT broker and experiment controller. Benchmarked against laptop for solver time comparison.

### 8. ESP32 role

**Sensing and control node.** Reads PZEM-004T power data. Controls relay module to execute schedule. Reports machine states and measured power via MQTT to RPi.

### 9. Data flow

```
[Tariff data + Job data + Measured power profiles]
                    │
                    ▼
        ┌─────────────────────┐
        │   Raspberry Pi 5    │
        │                     │
        │  MILP model build   │
        │  OR-Tools CP-SAT    │
        │  AUGMECON loop      │
        │  → Pareto surface   │
        │  → Selected schedule│
        └─────────┬───────────┘
                  │ MQTT: schedule commands
                  ▼
        ┌─────────────────────┐
        │      ESP32          │
        │  Execute schedule   │
        │  Control relays     │
        │  Read PZEM-004T     │
        │  Report measurements│
        └─────────┬───────────┘
                  │ MQTT: power data
                  ▼
        ┌─────────────────────┐
        │   Raspberry Pi 5    │
        │  Log measurements   │
        │  Compare predicted  │
        │    vs actual        │
        │  Display dashboard  │
        └─────────────────────┘
```

### 10. Optimization loop

**Level 2 (target):** Open-loop. Optimize → execute → measure → compare. No re-optimization during execution.

**Level 4 (stretch):** Closed-loop. Optimize → execute → detect deviation → re-optimize remaining schedule.

### 11. Baselines

| Baseline | Description |
|---|---|
| B1: FCFS | First-come-first-served dispatch. No optimisation. |
| B2: SPT | Shortest-processing-time dispatch. No energy awareness. |
| B3: Makespan-MILP | Single-objective: minimise makespan. Ignores energy. |
| B4: Bi-objective | Minimise {makespan, energy cost}. ε-constraint. No peak. |
| **Proposed: P1** | **Minimise {makespan, energy cost, peak demand}. AUGMECON.** |

### 12. Experiments

See Task 5. Six experiments covering: model comparison, Pareto structure, demand-charge sensitivity, tariff sensitivity, energy model fidelity, scalability.

### 13. Evaluation metrics

| Metric | Unit | From |
|---|---|---|
| Makespan | time slots or hours | Solver output |
| Energy cost | ₹ | Solver output + validation from PZEM-004T |
| Peak power | W or kW | Solver output + validation from PZEM-004T |
| Total bill | ₹ | Computed: energy cost + ρ × peak |
| Prediction error | % | |predicted − measured| / measured |
| Hypervolume indicator | dimensionless | From Pareto front analysis |
| Solver time | seconds | Timed on RPi and laptop |
| Optimality gap | % | From solver output |
| Deadline violation rate | % | Count of jobs finishing after deadline |

### 14. Expected contribution

1. **Empirical:** Systematic 3D Pareto analysis of makespan × energy cost × peak demand for manufacturing scheduling.
2. **Empirical:** Parametric characterisation of when peak-demand awareness provides meaningful total-bill reduction (demand-charge threshold).
3. **Engineering:** Physical validation of energy-aware scheduling on a measured testbed.
4. **Engineering:** Demonstration of edge-feasible scheduling on Raspberry Pi.

All of these are empirical/engineering contributions. None are algorithmic novelty.

### 15. Limitations

1. **Testbed is not a factory.** Results demonstrate methodology validation, not industrial-scale savings.
2. **Loads are emulators.** A DC motor is not a CNC machine. Power profiles are representative, not identical.
3. **Deterministic model.** Processing times are fixed. Real manufacturing has variability.
4. **Small scale.** Largest physically executable instance is 4 machines. Simulation extends to larger.
5. **No machine breakdowns.** Excluded from model.
6. **Indian tariff specificity.** Results depend on tariff structure. Generalisation requires additional experiments with other tariff regimes.
7. **Solver limitations.** OR-Tools CP-SAT is less powerful than Gurobi for large MILP. Edge solver comparison is limited by ARM architecture.

---

## FINAL DECISION

### Decision: **MODIFY then GO**

### Justification matrix

| Criterion | Assessment | Evidence |
|---|---|---|
| Mathematical rigour | ✅ Adequate | Tri-objective MILP + AUGMECON + parametric sensitivity. Not novel math, but rigorous applied math. |
| Real research gap | ⚠️ Narrow but genuine | Systematic Pareto analysis with demand-charge sensitivity for manufacturing scheduling is under-explored. Physical validation is rare. |
| Experimental falsifiability | ✅ Strong | Six experiments with null hypotheses and specific falsification conditions. |
| Undergraduate feasibility | ✅ Strong | OR-Tools + Python + ESP32 + PZEM-004T. All tools are free and well-documented. |
| Data availability | ✅ Strong | Synthetic instances (standard). Indian tariffs (public). Machine power (self-measured). |
| Prototype feasibility | ✅ Strong | ₹2,300 BOM. Safe low-voltage. Borrowed RPi. |
| Reproducibility | ✅ Strong | Open-source tools. Published tariff data. Measured profiles can be shared. |
| Measurable contribution | ✅ Clear | Pareto analysis, threshold identification, prediction validation, solver benchmarking. |
| SDG 9 alignment | ✅ Direct | SDG 9.4 (sustainable industrialisation). Energy cost reduction for MSMEs. |

### What must be modified

1. **Do NOT claim algorithmic novelty.** Frame as "extended formulation study with empirical validation."
2. **Add peak demand as third objective.** This is the mathematical layer that elevates beyond textbook.
3. **Build physical testbed.** This is the engineering layer that elevates beyond simulation.
4. **Add sensitivity analysis.** This is the research layer — characterising *when* peak-awareness matters.
5. **Use OR-Tools CP-SAT, not Gurobi** — runs natively on RPi ARM64.
6. **Raspberry Pi is justified only as optimization server with benchmarked performance.** Not as IoT decoration.

### What must NOT be done

- Do NOT call this "novel algorithm."
- Do NOT add blockchain, computer vision, chatbot, or "AI" without technical justification.
- Do NOT claim specific improvement percentages before running experiments.
- Do NOT treat the dashboard as a contribution.
- Do NOT treat MQTT/IoT as research.
- Do NOT build Level 4 before Level 2 works flawlessly.

### Critical path

| Week | Deliverable | Level |
|---|---|---|
| 1 | Implement bi-objective MILP in OR-Tools. Verify on 5×3 instance. | L1 |
| 1 | Download Karnataka BESCOM tariff order. Extract ToD rates + demand charge. | L1 |
| 2 | Extend to tri-objective (add P_peak). Implement AUGMECON loop. | L2 |
| 2 | Build instance generator. Generate 60 test instances. | L1 |
| 3 | Run Experiment 1 (model comparison) and Experiment 2 (Pareto structure). | L2 |
| 3 | Order and assemble hardware. Wire ESP32 + PZEM-004T + relay + loads. | L2 |
| 4 | Measure P_proc, P_idle, E_start for each load. Calibrate PZEM-004T. | L2 |
| 5 | Integrate RPi ↔ ESP32 via MQTT. Execute baseline + optimised schedules. | L2 |
| 5 | Run Experiment 5 (energy model fidelity). | L2 |
| 6 | Run Experiment 3 (demand-charge sensitivity) and Experiment 4 (tariff sensitivity). | L2 |
| 7 | Run Experiment 6 (scalability) on RPi vs laptop. | L3 |
| 7 | Build dashboard for demo. | L2 |
| 8 | Full demo rehearsal. Record results. Begin report. | L2 |
| 9–10 | (If ahead) Attempt Experiment 6 uncertainty analysis. | L3 |
| 10–12 | Report, poster, presentation. | All |
