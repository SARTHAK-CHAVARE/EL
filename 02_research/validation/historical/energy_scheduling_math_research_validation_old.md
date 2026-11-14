> [!WARNING]
> # HISTORICAL / REFERENCE DOCUMENT
>
> This document contains earlier project assumptions and designs.
> Some hardware references may be superseded.
>
> Current project specifications are defined by:
>
> - `00_project_overview/energy_scheduling_project_master_context.md`
> - `05_planning/master_execution_plan.md`
> - `03_tariff/tariff_reference.md`
> - `09_hardware/current_hardware_spec.md`

# Energy Scheduling — Mathematical Research & Engineering Depth Validation

## Goal

We have chosen **Energy Scheduling for Manufacturing / MSMEs** under **SDG 9**.

The previous audit found that the scheduling formulation is valid, but the key question is:

> **Can we create enough genuine mathematical research, engineering depth, and prototype quality to make this a strong project rather than “MILP + dashboard + simulated values”?**

Do **not** protect the idea. Challenge it and redesign it if necessary.

### Critical requirement

This project must contain **actual mathematical research**, not just measurement.

A strong contribution could involve:
- a new/extended scheduling formulation,
- multi-objective optimization and Pareto analysis,
- robust/stochastic scheduling,
- uncertainty-aware scheduling,
- rolling-horizon/receding-horizon optimization,
- peak-demand-aware scheduling,
- adaptive rescheduling,
- exact vs heuristic comparison,
- sensitivity/scalability analysis,
- decomposition/approximation,
- or another defensible mathematical contribution discovered during research.

Do **not** add mathematical complexity just for appearance.

---

## 1. Audit the Existing Idea

Using the attached audit, extract only:

- current problem formulation
- mathematical model
- proposed hardware
- optimizer
- baseline
- innovation claim
- prototype
- weaknesses
- feasibility concerns
- relevant rubric requirements

Label claims:

`[ESTABLISHED]` `[OBSERVED GAP]` `[INFERENCE]` `[PROPOSED]` `[HYPOTHESIS]`

Do not silently upgrade claims.

---

## 2. Answer the Core Question

> **Can energy-aware manufacturing scheduling become a mathematically rigorous, experimentally falsifiable engineering project with a compelling working prototype?**

Evaluate:

1. Mathematical research depth
2. Physical engineering depth
3. Experimental depth
4. Prototype quality
5. SDG 9 relevance

---

## 3. Prior-Art / State-of-the-Art Research

Search:

- IEEE Xplore
- ACM DL
- ScienceDirect
- SpringerLink
- Wiley
- Google Scholar
- relevant industrial/government sources

Search for:

- energy-aware manufacturing scheduling
- energy-aware job-shop / flow-shop scheduling
- multi-objective scheduling
- time-of-use production scheduling
- peak-demand scheduling
- machine ON/OFF scheduling
- robust/stochastic energy scheduling
- dynamic/real-time rescheduling
- measured power + production scheduling
- MSME energy optimization
- closed-loop manufacturing scheduling

Build a concise table:

| Work | Model | Objectives | Uncertainty | Physical validation | Main limitation |
|---|---|---|---|---|---|

Explicitly identify what is **already solved**.

Do not claim novelty without evidence.

---

# 4. Find the Mathematical Research Gap

This is the most important section.

Investigate whether the project can move beyond the standard:

> `minimize makespan + energy`

model.

For each candidate mathematical contribution, provide:

| Research direction | Baseline | Proposed change | Why it matters | How to test | Difficulty |
|---|---|---|---|---|---|

Investigate at least:

### A. Multi-objective optimization

For example:

\[
\min \{Makespan,\ Energy,\ Cost,\ PeakDemand\}
\]

Determine whether weighted-sum optimization, epsilon-constraint, or Pareto optimization is most defensible.

Do not simply assign arbitrary weights.

### B. Uncertainty

Investigate uncertainty in:

- processing time
- machine power
- job arrival
- machine availability
- electricity price

Compare deterministic vs robust/stochastic/rolling-horizon scheduling.

### C. Dynamic / rolling-horizon scheduling

Instead of generating one schedule:

`optimize → execute`

investigate:

`measure → optimize → execute → detect deviation → re-optimize`

Determine whether this provides a genuine research question.

### D. Peak-demand-aware scheduling

Investigate whether minimizing total energy is insufficient because peak power can affect industrial electricity costs.

Formulate and test peak-aware scheduling if justified.

### E. Energy model realism

Compare:

- constant machine power
- idle + processing power
- startup/shutdown energy
- measured power profiles

Determine whether a richer energy model materially changes the optimal schedule.

### F. Scalability / computational research

Study how solution quality and solver time change with:

- jobs
- machines
- objectives
- uncertainty
- scheduling horizon

Compare exact optimization against a heuristic/metaheuristic only if useful.

---

# 5. Mathematical Formulation

Develop a rigorous formulation.

Define:

- sets
- parameters
- decision variables
- objective functions
- hard constraints
- assumptions

Potential variables:

\[
x_{ijm} = 	ext{assignment}
\]

\[
S_i = 	ext{start time}
\]

\[
C_i = 	ext{completion time}
\]

\[
y_{mt} = 	ext{machine state}
\]

\[
z_{mt} = 	ext{startup indicator}
\]

Potential objectives:

\[
\min C_{max}
\]

\[
\min E
\]

\[
\min Cost
\]

\[
\min PeakDemand
\]

Then investigate the strongest formulation rather than automatically combining everything.

Explain:

- why each variable exists
- why each constraint is needed
- which assumptions are unrealistic
- what mathematical contribution is actually ours
- computational complexity / NP-hardness where relevant
- whether the formulation is solvable within student resources

---

# 6. Mathematical Experiment — NOT Just Measurement

Design experiments that answer mathematical research questions.

Examples:

### Experiment 1 — Model comparison

Compare:

`Baseline scheduling`

vs

`Energy-aware scheduling`

vs

`Proposed enhanced formulation`

Measure:

- objective values
- Pareto quality
- feasibility
- solver runtime
- optimality gap

### Experiment 2 — Uncertainty

Compare deterministic scheduling against the proposed uncertainty-aware method under multiple realizations.

Measure:

- expected cost
- worst-case cost
- deadline violations
- schedule stability
- robustness

### Experiment 3 — Sensitivity

Vary:

- tariff
- machine power
- processing time
- deadline tightness
- workload

Determine when the proposed formulation provides an advantage and when it does not.

### Experiment 4 — Scalability

Increase:

`jobs × machines × horizon`

and analyze:

- runtime
- optimality gap
- memory
- solution quality

### Experiment 5 — Ablation

Remove the proposed mathematical component and determine whether performance changes.

The project must be capable of **failing**.

If the proposed method performs no better than the baseline under relevant conditions, that is a valid research result.

---

# 7. Physical Engineering Layer

Determine the minimum physical testbed.

Potential components:

- ESP32 / Arduino
- PZEM-004T or equivalent
- current/power sensing
- small motors/heaters/loads
- relay or safe switching hardware
- dashboard
- machine-state sensing

For every component state:

**What technical purpose does it serve?**

Do not add hardware merely for presentation.

---

# 8. Real Data vs Simulation

Clearly separate:

### REAL

- machine power
- machine state
- measured energy
- controller response

### MODELLED

- processing time
- machine capability
- job precedence
- tariff
- scheduling constraints

### SIMULATED

- large-scale production scenarios
- uncertainty scenarios
- scalability experiments

Explain why each category is scientifically legitimate.

---

# 9. Closed-Loop Architecture

Evaluate:

```text
Physical machines
      ↓
Power/state sensing
      ↓
Energy model
      ↓
Production model
      ↓
Optimization
      ↓
Schedule
      ↓
Controller
      ↓
Physical execution
      ↓
Measurement
      ↓
Rescheduling
```

Compare:

1. Optimization only
2. Optimization + monitoring
3. Optimization + monitoring + control
4. Closed-loop adaptive scheduling

Select the minimum architecture that provides genuine engineering depth.

---

# 10. Prototype Demonstration

Design a **5-minute evaluator demonstration**.

Show:

1. Multiple physical loads representing machines
2. Real power/state measurement
3. Jobs and constraints
4. Baseline schedule
5. Proposed mathematical optimizer
6. Physical execution
7. Feedback/rescheduling if implemented
8. Final comparison

Display:

```text
                Baseline     Proposed
Energy          ______       ______
Cost            ______       ______
Peak Power      ______       ______
Makespan        ______       ______
Tardiness       ______       ______
Solver Time     ______       ______
```

The demonstration must show **decision-making and engineering behavior**, not just a dashboard.

---

# 11. Research Question

Generate 3–5 genuinely falsifiable research questions.

Avoid:

> “Can AI optimize manufacturing?”

Prefer questions involving a measurable mathematical hypothesis, for example:

> Can an uncertainty-aware energy scheduling formulation maintain production constraints more reliably than deterministic scheduling when processing times and machine power vary?

Improve the question after literature analysis.

Select one based on:

- mathematical depth
- novelty
- falsifiability
- engineering relevance
- prototype feasibility
- rubric fit

---

# 12. Minimum Viable Research Project

Define the smallest version that still contains:

### Mathematical contribution
A clearly identifiable research component.

### Engineering contribution
Real sensing/control or another meaningful physical mechanism.

### Experimental contribution
Baseline + proposed method + controlled comparison.

### Prototype
A working demonstrator.

### Evidence
Quantitative results that can support or reject the hypothesis.

---

# 13. Escalation Path

Design four levels:

### Level 1 — Minimum viable
Must work.

### Level 2 — Strong engineering
Adds real measurement/control.

### Level 3 — Mathematical research
Adds the strongest justified mathematical contribution.

### Level 4 — Stretch
Advanced feature only if Levels 1–3 work.

Do not allow Level 4 to endanger the core project.

---

# 14. Failure Analysis

Try to disprove the project.

Check:

- optimizer produces no meaningful improvement
- mathematical extension gives negligible benefit
- physical measurements are noisy
- measured power differs from model
- schedule becomes infeasible
- solver becomes too slow
- physical testbed is not representative
- closed-loop control is unreliable

For each:

**Failure → consequence → mitigation → residual risk**

---

# 15. Final Decision Gate

| Gate | Requirement | Status |
|---|---|---|
| Real industrial problem | Evidence | |
| Mathematical research | Genuine contribution | |
| Mathematical validation | Falsifiable experiments | |
| Engineering depth | Physical system | |
| Prototype feasibility | Buildable | |
| Experimental validation | Baseline vs proposed | |
| Research contribution | Defensible | |
| SDG 9 connection | Concrete | |
| Rubric fit | Strong | |
| Cost | Student feasible | |
| Time | Student feasible | |

Conclude:

### GO
if the project has sufficient mathematical + engineering depth.

### MODIFY
if the core idea is good but a specific research/engineering layer is required.

### REJECT
if it remains primarily a software optimization demo.

---

# FINAL OUTPUT — KEEP IT CONCISE

Return only:

1. **Verdict**
2. **What is currently weak**
3. **What mathematical research direction is strongest**
4. **Proposed mathematical formulation**
5. **Research hypothesis**
6. **Experiments needed to test it**
7. **Physical prototype architecture**
8. **Minimum viable prototype**
9. **Strong version**
10. **Key risks**
11. **GO / MODIFY / REJECT**
12. **Exact next steps**

## Non-negotiable rules

- No manufactured novelty.
- No unsupported improvement percentages.
- No “AI/IoT/blockchain” buzzwords without technical necessity.
- No arbitrary complexity.
- No treating measurement alone as research.
- No fake mathematical contribution.
- Distinguish `[ESTABLISHED]`, `[OBSERVED GAP]`, `[INFERENCE]`, `[PROPOSED]`, `[HYPOTHESIS]`.
- Challenge the project aggressively.
- Prefer one strong mathematical research question over five shallow features.
- Keep the entire analysis concise enough to avoid wasting model context.
