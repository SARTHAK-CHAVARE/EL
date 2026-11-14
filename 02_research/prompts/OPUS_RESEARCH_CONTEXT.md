# PROJECT MASTER CONTEXT

# PROJECT MASTER CONTEXT — VERSION 2.0

> **Status:** CURRENT / AUTHORITATIVE  
> **Updated:** 2026-10-03  
> **Purpose:** Single source of truth for the project.  
> **Current hardware:** INA226 + ESP32 + low-voltage 12V DC machine-load emulation testbed.  
> **Primary optimizer:** Raspberry Pi 5.  
> **Primary solver:** OR-Tools CP-SAT.  
> **Research posture:** Evidence-first, literature-derived mathematics, no manufactured novelty.

---

## 0. DOCUMENT CONTROL

This document is the current authoritative description of the project.

Older files are retained for historical/reference purposes. If an older document conflicts with this document, this document takes precedence.

### Evidence classes

Every important statement should be treated as one of:

- **LITERATURE-DERIVED** — directly supported by a peer-reviewed paper or recognized methodology source.
- **OFFICIAL-SOURCE-DERIVED** — supported by KERC or another authoritative regulatory source.
- **PROJECT-DERIVED / ASSUMED** — introduced for this project and explicitly labeled.

### Current source-of-truth hierarchy

```text
PROJECT MASTER CONTEXT
        ↓
MASTER EXECUTION PLAN
        ↓
CURRENT TARIFF REFERENCE
        ↓
CURRENT HARDWARE SPECIFICATION
        ↓
MATHEMATICAL MODEL
        ↓
CODE
        ↓
EXPERIMENTS
        ↓
VALIDATION
        ↓
REPORT
```

---

# 1. PROJECT IDENTITY

## 1.1 Working title

**Peak-Aware Energy-Cost Production Scheduling for Small Manufacturing Systems Under Industrial Tariff Structures: A Multi-Objective Optimization Study with Physical Validation**

This title may be refined after the literature-to-model audit.

## 1.2 SDG

Primary alignment:

**SDG 9 — Industry, Innovation and Infrastructure**

Relevant framing:

**SDG 9.4** — sustainable industrialization and improved resource-use efficiency.

The project studies how production scheduling can affect electricity consumption cost and peak demand in a small manufacturing-system abstraction.

Important limitation:

The physical setup is a **programmable machine-load emulation testbed**, not a real industrial factory.

---

# 2. CORE PROBLEM

Small manufacturing systems can face electricity costs with two conceptually important components:

1. Energy charges based on consumed electrical energy, potentially varying by time of day.
2. Demand charges associated with maximum/billing demand.

A conventional production schedule may prioritize production order, completion time, or dispatch rules without explicitly considering electricity cost.

An energy-cost-aware scheduler can shift operations toward lower-cost time periods. However, shifting operations can change simultaneous machine activity and therefore peak electrical demand.

This can create a trade-off:

```text
Production performance
        ↕
Energy cost
        ↕
Peak electrical demand
```

The project does **not** assume that the peak effect is always economically important. The magnitude and existence of useful trade-offs are empirical questions.

---

# 3. CENTRAL RESEARCH QUESTION

> **Under what combinations of demand-charge intensity, time-of-use tariff variation, workload intensity, and machine power heterogeneity does peak-aware production scheduling provide a statistically significant economic benefit over energy-cost-only scheduling?**

The project is deliberately framed so that:

- positive benefit is possible,
- negligible benefit is possible,
- and a negative/null result is valid.

---

# 4. SECONDARY RESEARCH QUESTIONS

### RQ1 — Pareto structure

Does explicitly considering peak demand produce schedules occupying regions of objective space not obtained by optimizing makespan and energy cost alone?

### RQ2 — Demand-charge sensitivity

How does the economic difference between energy-only and peak-aware schedules change as demand-charge intensity varies?

### RQ3 — ToD sensitivity

How does the result change as the electricity price differential between time periods changes?

### RQ4 — Workload intensity

How does system utilization/overlap affect the value of peak-aware scheduling?

### RQ5 — Power heterogeneity

Does greater variation in machine/load power draw affect the value of peak awareness?

### RQ6 — Model fidelity

How accurately can measured electrical load profiles predict actual schedule energy and peak power?

### RQ7 — Edge feasibility

Can the validated optimization workflow run on Raspberry Pi 5 for the selected instance sizes within a documented computational limit?

---

# 5. WORKING HYPOTHESES

These are hypotheses to test, not conclusions.

## H1

Peak-aware scheduling can reduce simulated total electricity cost relative to energy-cost-only scheduling in regions where peak-demand exposure is sufficiently important.

The threshold, if one exists, is unknown before experimentation.

## H2

The economic effect can vary with:

- demand-charge intensity,
- ToD differential,
- workload intensity,
- power heterogeneity.

Any monotonic relationship must be established experimentally.

## H3

Energy-cost-only optimization does not necessarily increase peak demand under every workload condition.

## H4

A model calibrated from measured machine-load power profiles can predict physically executed schedule energy and peak within an empirically characterized error range.

---

# 6. WHAT THIS PROJECT IS NOT

Do not describe the project as:

- a novel optimization algorithm,
- a novel mathematical optimization technique,
- a new solver,
- an AI/deep-learning project,
- a blockchain project,
- an IoT novelty project,
- a real factory deployment,
- a real-time industrial control system,
- a production digital twin of a real plant,
- a guaranteed industrial savings system.

Correct characterization:

> **An established energy-aware production-scheduling formulation, parameterized using a real industrial tariff structure, investigated systematically through controlled experiments, and physically validated using measured low-voltage machine-load emulation.**

---

# 7. EXPECTED CONTRIBUTIONS

## 7.1 Integrated formulation

Combine established scheduling, energy-cost, and peak-demand components.

**Classification:** Engineering integration.

## 7.2 Systematic sensitivity study

Characterize when peak-awareness matters and when it does not.

**Classification:** Empirical contribution.

## 7.3 Pareto analysis

Study the makespan–energy-cost–peak relationship.

**Classification:** Empirical contribution.

## 7.4 Physical validation

Measure physical loads and compare model predictions with actual execution.

**Classification:** Physical validation / engineering contribution.

## 7.5 Edge deployment

Run the validated scheduler on Raspberry Pi 5.

**Classification:** Engineering integration.

---

# 8. HONEST NOVELTY POSITION

The following are established components and are not novel by themselves:

- job-shop scheduling,
- flexible job-shop scheduling,
- parallel-machine scheduling,
- makespan minimization,
- energy-aware scheduling,
- machine-state energy models,
- time-of-use scheduling,
- demand/peak formulations,
- epsilon-constraint methods,
- AUGMECON,
- NSGA-II / NSGA-III,
- constraint programming,
- ESP32 sensing/control,
- MQTT,
- Raspberry Pi edge computation,
- Gantt visualization.

Potentially under-explored areas to investigate, without claiming novelty in advance:

1. systematic 3-objective production scheduling analysis involving peak demand,
2. systematic sensitivity characterization of peak-awareness under demand-charge and ToD conditions,
3. physical execution and predicted-vs-measured validation of optimized schedules.

---

# 9. LITERATURE-FIRST METHODOLOGY

This is a non-negotiable rule.

## Wrong workflow

```text
Invent formulation
      ↓
Find papers that sound similar
      ↓
Claim support
```

## Correct workflow

```text
Find papers
      ↓
Verify papers
      ↓
Extract exact formulations
      ↓
Compare formulations
      ↓
Choose mathematical foundation
      ↓
Adapt to our project
      ↓
Hand-verify
      ↓
Implement
```

No final mathematical equation should be accepted simply because it “looks right.”

---

# 10. LITERATURE SEARCH SCOPE

Search for:

1. energy-aware manufacturing/job-shop scheduling,
2. multi-objective production scheduling,
3. flexible job-shop energy optimization,
4. time-of-use production scheduling,
5. demand-charge-aware manufacturing scheduling,
6. peak-demand-aware production scheduling,
7. joint energy-cost and peak-demand optimization,
8. makespan + energy + peak formulations,
9. epsilon-constraint and AUGMECON scheduling,
10. constraint programming/CP-SAT scheduling,
11. machine power profiling,
12. physical validation of energy-aware scheduling,
13. Indian industrial tariff modeling,
14. MSME energy-management context,
15. robust/stochastic energy-aware scheduling as stretch context.

---

# 11. LITERATURE SEARCH QUERIES

```text
"energy-aware" AND "job shop scheduling" AND ("multi-objective" OR "Pareto")
"peak demand" AND "production scheduling" AND optimization
"time-of-use" AND "manufacturing scheduling" AND (MILP OR "constraint programming")
"demand charge" AND scheduling AND manufacturing
"demand charge" AND "production scheduling"
"peak demand" AND "job shop" AND scheduling
"makespan" AND "energy cost" AND "peak demand" scheduling
"flexible job shop" AND "time-of-use" AND energy
"augmented epsilon constraint" AND scheduling
"AUGMECON" AND manufacturing
"constraint programming" AND energy-aware scheduling
"physical validation" AND scheduling AND energy consumption
"measured power" AND manufacturing scheduling
"machine power" AND scheduling AND electricity cost
"Indian industrial tariff" AND ToD
"Karnataka" AND industrial tariff AND demand charge
```

---

# 12. LITERATURE COLLECTION TARGET

Initial target:

**15–20 verified candidate papers**

Then select:

**5–8 foundational papers**

The strongest papers should contain explicit mathematics, assumptions, and methodology.

Do not select a paper simply because the abstract uses “green manufacturing” or “energy efficiency.”

---

# 13. LITERATURE MATRIX

File:

```text
02_research/literature/literature_matrix/literature_to_model_matrix.md
```

Required fields:

```text
ID
Authors
Year
Title
Venue
DOI
Verification status
Scheduling problem
Sets
Parameters
Decision variables
Objectives
Constraints
Energy model
Tariff model
Peak model
Demand-charge model
Multi-objective method
Solver
Instance generation
Physical validation
Assumptions
Exact equation/page references
Adoptable components
Required modifications
Limitations
Relevance
Notes
```

---

# 14. FOUNDATIONAL-PAPER MATHEMATICAL AUDIT

For each of the 5–8 foundational papers extract:

- exact scheduling problem,
- sets,
- parameters,
- decision variables,
- objective functions,
- constraint families,
- energy formulation,
- tariff formulation,
- peak-demand formulation,
- demand-charge formulation,
- multi-objective mechanism,
- optimization method,
- assumptions,
- instance generation,
- important limitations.

Every exact equation reference must use the real page/equation number.

No invented equation numbers.

---

# 15. LITERATURE-TO-EQUATION TRACEABILITY

File:

```text
04_mathematical_model/derivation/literature_to_equation.md
```

For each major project equation:

```text
Source paper
    ↓
Original equation/formulation
    ↓
Physical meaning
    ↓
Assumptions
    ↓
Applicability
    ↓
Required adaptation
    ↓
Project equation
    ↓
Classification
```

Classification must be:

- `[LITERATURE-DERIVED]`
- `[DERIVED]`
- `[PROJECT ASSUMPTION]`

---

# 16. SCHEDULING PROBLEM CLASS

Do not automatically call the model FJSP.

The final class must be selected after literature analysis and project definition.

Candidates:

- parallel-machine scheduling,
- job-shop scheduling,
- flexible job-shop scheduling.

Selection criteria:

1. actual machine/job structure,
2. mathematical literature strength,
3. CP-SAT feasibility,
4. physical-testbed representability,
5. experimental tractability.

---

# 17. MATHEMATICAL MODEL — CURRENT STATUS

The final model is **not frozen yet**.

The intended structure is:

```text
Sets
↓
Parameters
↓
Decision variables
↓
Scheduling constraints
↓
Energy model
↓
ToD/tariff model
↓
Peak-power model
↓
Demand-charge mapping
↓
Objective functions
↓
Multi-objective solution method
```

A candidate objective set is:

\[
f_1=C_{\max}
\]

\[
f_2=EC
\]

\[
f_3=P^{peak}
\]

This is a current direction, not yet the final literature-validated formulation.

---

# 18. CANDIDATE SCHEDULING VARIABLES

Depending on the selected scheduling class, candidate variables include:

- operation start times,
- operation completion times,
- machine assignments,
- interval variables,
- optional intervals for alternative machines,
- sequencing relationships.

Candidate processing relation:

\[
C_o=S_o+p_o
\]

Candidate precedence:

\[
S_{o_2}\ge C_{o_1}
\]

for a predecessor/successor pair.

The exact final formulation must come from the literature audit.

---

# 19. ENERGY MODEL — CURRENT CONCEPT

For a discrete time model:

\[
P_t=\sum_m P_m a_{mt}
\]

where \(a_{mt}\) indicates whether machine/load \(m\) is active during period \(t\).

Energy:

\[
E_t=P_t\Delta t
\]

Total energy:

\[
E=\sum_tE_t
\]

These relationships are basic physical derivations, while their optimization embedding must follow the chosen research formulation.

---

# 20. ENERGY-COST MODEL

General form:

\[
EC=\sum_t\pi_tE_t
\]

where \(\pi_t\) is the applicable electricity price for time period \(t\).

The actual \(\pi_t\) must be taken from the tariff scenario.

---

# 21. PEAK-POWER MODEL

Candidate:

\[
P^{peak}\ge P_t\quadorall t
\]

and, when minimized or otherwise correctly linked:

\[
P^{peak}=\max_tP_t
\]

This is the scheduling/electrical peak variable.

It is not automatically equal to KERC billing demand.

---

# 22. KERC TARIFF — CURRENT AUTHORITATIVE REFERENCE

Source:

**Karnataka Electricity Regulatory Commission Tariff Order 2025 — All ESCOMs, Annexure 9**

## Category

**HT-2(a) — Industrial**

The order includes industries such as MSMEs, factories, industrial workshops, R&D centres, and multiple industrial/IT-related activities.

## Study period

**FY 2026–27**

Effective from:

**1 April 2026**

## Base energy charge

\[
oxed{₹6.60/	ext{kWh}}
\]

## Demand charge

\[
oxed{₹350/	ext{kVA/month of billing demand}}
\]

## Billing demand

\[
oxed{BD=\max(MD,0.90CD)}
\]

where:

- \(MD\) = maximum demand recorded during the month,
- \(CD\) = contract demand.

The tariff order additionally specifies demand-rounding rules and treatment of demand exceeding contract demand.

## ToD

### July–November

| Time | Adjustment |
|---|---:|
| 06:00–09:00 | 0 paise/unit |
| 09:00–18:00 | 0 paise/unit |
| 18:00–22:00 | 0 paise/unit |
| 22:00–06:00 | 0 paise/unit |

### December–June

| Time | Adjustment |
|---|---:|
| 06:00–09:00 | +100 paise/unit |
| 09:00–18:00 | 0 paise/unit |
| 18:00–22:00 | +100 paise/unit |
| 22:00–06:00 | −100 paise/unit |

Simplified December–June prices under the ₹6.60 base rate:

- 06:00–09:00 → ₹7.60/kWh,
- 09:00–18:00 → ₹6.60/kWh,
- 18:00–22:00 → ₹7.60/kWh,
- 22:00–06:00 → ₹5.60/kWh.

## ToD applicability

The order states compulsory ToD for relevant HT-2 categories with contract demand of 500 kVA and above, and optional ToD below 500 kVA.

The experiment must explicitly declare which tariff scenario is being represented.

## Discounted Energy Rate Scheme

ToD has a stated interaction with the discounted-energy-rate scheme.

Core project scope should exclude this scheme unless it becomes part of the research question.

## Power factor

The order contains an average PF requirement and surcharge rule for PF below 0.90 under the stated conditions.

The DC testbed does not reproduce industrial AC PF behavior.

---

# 23. KVA VS KW

This distinction is mandatory.

The scheduling model primarily works with electrical load in kW:

\[
P^{peak}_{kW}
\]

The KERC demand tariff uses kVA:

\[
MD_{kVA}
\]

Do not silently equate them.

A simplification such as:

\[
kVApprox kW
\]

must be explicitly identified as a PF≈1 assumption.

---

# 24. REAL TARIFF VS NORMALIZED RESEARCH DEMAND PARAMETER

Actual KERC demand charge:

\[
₹350/	ext{kVA/month}
\]

Research sensitivity parameter:

\[
ho
\]

A normalized experiment may use:

\[
C_ho(S)=EC(S)+ho P^{peak}(S)
\]

But:

> **\(ho\) is a research sensitivity parameter, not the actual KERC demand tariff.**

Never report a short testbed result as an actual monthly industrial bill.

---

# 25. BILLING-HORIZON ISSUE

KERC demand billing is monthly.

A 10-minute or 30-minute testbed execution is not a monthly billing period.

Therefore:

- physical measurements validate the load model,
- normalized demand-charge sensitivity studies examine economic relationships,
- actual KERC values provide real-world tariff context.

Do not write “the testbed saves ₹X per month” without a defensible monthly aggregation model.

---

# 26. ELECTRICAL PARAMETERS

Candidate measured parameters:

\[
P^{proc}_m
\]

Processing power of load \(m\).

\[
P^{idle}_m
\]

Idle power.

\[
E^{start}_m
\]

Startup energy, when relevant.

These must be measured from the actual testbed if included in the final model.

Do not add machine-state complexity without evidence that it matters.

---

# 27. CURRENT HARDWARE ARCHITECTURE

The core physical system is a **low-voltage 12V DC machine-load emulation testbed**.

```text
Raspberry Pi 5
      │
      │ Wi-Fi / MQTT
      ▼
    ESP32
      │
      ├── INA226 #1 → Load 1
      ├── INA226 #2 → Load 2
      ├── INA226 #3 → Load 3
      └── optional additional channel
      │
      ▼
Relay / MOSFET switching
      │
      ▼
12V DC load emulators
```

The final number of channels is a hardware verification decision.

---

# 28. INA226

Current measurement direction:

**INA226 DC power monitor**

Role:

- DC bus voltage measurement,
- shunt-current measurement,
- electrical power calculation,
- I²C communication to ESP32.

Before purchase/assembly, verify the exact breakout-board:

- shunt value,
- maximum voltage,
- current range,
- address configuration,
- module supply,
- shunt heating,
- ESP32 I²C compatibility.

Do not blindly copy generic internet specifications into the final report.

---

# 29. SUPERSEDED PZEM-004T DESIGN

PZEM-004T appeared in earlier project versions.

It is **superseded for the planned 12V DC testbed**.

Reason:

- PZEM-004T is an AC measurement solution,
- the core testbed is based on 12V DC loads,
- INA226 is the current DC measurement direction.

Historical references to PZEM should be preserved where they explain project evolution, but must be marked historical.

---

# 30. PHYSICAL LOAD EMULATORS

Candidate load types:

- 12V DC motor,
- 12V heater/resistive load,
- 12V LED load,
- 12V DC fan/pump.

These represent different power profiles; they do not represent actual industrial machines.

Final electrical ratings must be verified from the actual purchased components.

---

# 31. ESP32 ROLE

The ESP32 is the sensing/control node.

Responsibilities:

1. read INA226,
2. collect voltage/current/power,
3. control load switching,
4. timestamp load states,
5. communicate with Raspberry Pi,
6. publish measurements where MQTT is used.

The ESP32 is not the optimization engine.

---

# 32. RASPBERRY PI ROLE

The Raspberry Pi 5 is the local edge optimization and experiment server.

Responsibilities:

1. receive/load job data,
2. load tariff configuration,
3. build scheduling model,
4. run OR-Tools CP-SAT,
5. execute epsilon-constraint loops,
6. generate schedules,
7. send schedule commands,
8. receive measurements,
9. log experimental results,
10. benchmark solver performance.

MQTT broker/experiment controller functions are supporting engineering infrastructure.

---

# 33. COMMUNICATION

Primary communication:

```text
Raspberry Pi 5 ↔ Wi-Fi ↔ ESP32
```

MQTT can carry:

- schedule commands,
- load states,
- measurements,
- timestamps,
- run identifiers,
- status messages.

Serial can be retained as a debugging fallback.

---

# 34. SOFTWARE STACK

Core:

- Python,
- OR-Tools,
- NumPy,
- pandas,
- SciPy,
- matplotlib,
- PyYAML.

Communication:

- Mosquitto,
- paho-mqtt.

Potential stretch:

- pymoo / NSGA-III.

No machine-learning framework is required for the core project.

---

# 35. CP-SAT TERMINOLOGY

Use:

> **OR-Tools CP-SAT / constraint programming solver**

Do not call CP-SAT simply a “MILP solver.”

A mathematical formulation can contain MILP-like relationships while the implementation uses CP-SAT interval variables and scheduling constraints.

---

# 36. MULTI-OBJECTIVE STRATEGY

Candidate objectives:

\[
(C_{\max},EC,P^{peak})
\]

Current intended solution approach:

**epsilon-constraint / AUGMECON-style method**

Important:

- avoid unconditional “guarantee” language,
- state solver and implementation assumptions,
- document any infeasible epsilon combinations.

---

# 37. COMMON EVALUATION SPACE

A 2-objective solution set lives in:

\[
(C_{\max},EC)
\]

A 3-objective solution set lives in:

\[
(C_{\max},EC,P^{peak})
\]

Therefore, raw comparison of their hypervolumes in different dimensions is invalid.

For comparison:

1. generate schedules under both formulations,
2. evaluate all schedules on the same complete metric set,
3. compare in a common space,
4. apply the same external tariff/cost mapping,
5. use consistent normalization/reference points if hypervolume is calculated.

---

# 38. BASELINES

## B0 — FCFS

First-come-first-served.

## B1 — SPT

Shortest-processing-time heuristic.

## B2 — Makespan-only

\[
\min C_{\max}
\]

## B3 — Energy-cost-only

\[
\min EC
\]

or a two-objective \((C_{\max},EC)\) formulation, depending on final experimental design.

## Proposed peak-aware formulation

\[
(C_{\max},EC,P^{peak})
\]

with epsilon-constraint/AUGMECON-style solution.

All schedules must be evaluated under the same external metrics.

---

# 39. INSTANCE GENERATION

Use reproducible synthetic workload instances.

Store:

- job count,
- machine count,
- operation count,
- processing times,
- machine eligibility,
- machine power,
- workload intensity,
- power heterogeneity,
- horizon,
- tariff profile,
- seed.

Earlier candidate seeds:

```text
1000, 1001, ..., 1019
```

Final seed policy is an implementation choice.

---

# 40. WORKLOAD INTENSITY

Define:

\[
\lambda
\]

as a normalized workload/utilization measure.

The final definition must be explicit, such as total required processing capacity divided by available capacity.

Candidate levels:

\[
\{0.3,0.5,0.7,0.9\}
\]

These are not final until the experiment design is approved.

---

# 41. POWER HETEROGENEITY

Define:

\[
\sigma
\]

through an explicit numerical measure of variation in machine power.

Candidate qualitative levels:

- low,
- medium,
- high.

Do not assign labels without defining their numerical meaning.

---

# 42. TOD DIFFERENTIAL FACTOR

Define:

\[
lpha
\]

as an experimental parameter only if needed.

Candidate levels from earlier planning:

\[
\{1.0,1.1,1.2,1.3,1.5\}
\]

These are experimental scenarios, not KERC facts.

---

# 43. DEMAND PARAMETER

Define:

\[
ho
\]

for sensitivity experiments.

Earlier candidate levels included:

\[
\{0,25,50,100,150,200,300,400,500\}
\]

These are candidate research values.

The official KERC reference is separate:

\[
₹350/	ext{kVA/month}
\]

---

# 44. EXPERIMENT A — BASELINE COMPARISON

Question:

How do FCFS, SPT, makespan-only and energy-aware scheduling methods compare on matched instances?

Metrics:

- makespan,
- energy,
- energy cost,
- peak power,
- normalized total-cost metric.

Candidate:

20 medium instances.

Use matched instances across all methods.

---

# 45. EXPERIMENT B — BI-OBJECTIVE PARETO

Question:

What is the structure of the makespan–energy-cost trade-off?

Generate:

\[
(C_{\max},EC)
\]

Pareto solutions.

Also record:

\[
P^{peak}
\]

as an observed third metric.

Analyze whether peak varies along the bi-objective frontier.

---

# 46. EXPERIMENT C — BI VS TRI

Question:

Does adding peak-awareness generate schedules that become economically useful under demand-sensitive evaluation?

Procedure:

1. generate bi-objective solution set,
2. generate tri-objective solution set,
3. evaluate all schedules on the common metric set,
4. compare under the same normalized demand-charge scenario.

Avoid circular “best solution” selection that changes the metric definition between methods.

---

# 47. EXPERIMENT D — DEMAND-CHARGE SENSITIVITY

Question:

How does comparative cost change with \(ho\)?

Output:

\[
Savings(ho)
\]

The exact savings denominator and reference schedule must be frozen before running the experiment.

Do not predeclare the threshold.

---

# 48. EXPERIMENT E — TOD SENSITIVITY

Question:

How does the result change when the time-of-day price differential changes?

Measure:

- energy cost,
- normalized total cost,
- peak,
- schedule shifts.

---

# 49. EXPERIMENT F — WORKLOAD SENSITIVITY

Question:

Does increased utilization change the value of peak-aware scheduling?

Candidate:

\[
\lambda \in \{0.3,0.5,0.7,0.9\}
\]

Measure:

- peak power,
- energy cost,
- normalized total cost,
- schedule overlap.

---

# 50. EXPERIMENT G — POWER HETEROGENEITY

Question:

Does machine power heterogeneity affect peak-aware scheduling value?

Measure:

- heterogeneity statistic,
- peak,
- energy cost,
- total normalized cost.

---

# 51. EXPERIMENT H — SCALABILITY

Candidate sizes:

```text
5×3
8×4
10×5
12×5
15×6
```

Potential stretch:

```text
20×8
30×10
50×10
```

Measure:

- solve time,
- solver status,
- optimality/bound information,
- number of Pareto solutions,
- memory where practical.

Compare:

- laptop,
- Raspberry Pi 5.

---

# 52. EXPERIMENT I — MODEL FIDELITY

Compare candidate energy models:

A. constant power,

B. measured idle + processing,

C. measured idle + processing + startup.

For physically executed schedules calculate:

\[
E_{pred}
\]

and:

\[
E_{meas}
\]

and similarly for peak.

---

# 53. EXPERIMENT J — PHYSICAL VALIDATION

Execute selected baseline and optimized schedules physically.

Record:

- actual execution time,
- actual energy,
- actual peak,
- actual load state,
- timestamps,
- predicted values,
- prediction errors.

Repeat executions enough to characterize variability.

---

# 54. VALIDATION METRICS

Energy relative error:

\[
rac{|E_{pred}-E_{meas}|}{E_{meas}}
\]

Peak relative error:

\[
rac{|P^{peak}_{pred}-P^{peak}_{meas}|}{P^{peak}_{meas}}
\]

Power-trace MAE:

\[
MAE=
rac1T\sum_t|P_{pred}(t)-P_{meas}(t)|
\]

Power-trace RMSE:

\[
RMSE=
\sqrt{rac1T\sum_t(P_{pred}(t)-P_{meas}(t))^2}
\]

Do not invent acceptable thresholds before calibration.

Report measurement uncertainty alongside error.

---

# 55. STATISTICAL DESIGN

For matched instance \(i\):

\[
\Delta_i = B_{method1,i}-B_{method2,i}
\]

Potential methods:

- paired parametric test if assumptions hold,
- Wilcoxon signed-rank where appropriate,
- Friedman test for multiple related methods,
- suitable post-hoc analysis.

Report:

- sample size,
- effect size where appropriate,
- uncertainty,
- p-values,
- paired design.

Statistical significance and engineering significance are different quantities.

---

# 56. PHASE MAP

Core relationship:

\[
(ho,lpha,\lambda,\sigma)ightarrow\Delta Bill
\]

Primary visualization:

\[
(ho,lpha)ightarrow\Delta Bill
\]

with fixed \(\lambda,\sigma\).

Plot:

- heatmap,
- contour,
- zero boundary,
- factor slices.

The zero boundary is an empirical result, not a predeclared threshold.

---

# 57. FULL FACTORIAL CANDIDATE

Earlier candidate design:

\[
6	imes5	imes4	imes3=360
\]

cells.

With 5 instances:

\[
1800
\]

instances per compared model.

This may be computationally expensive.

Reduced pilot:

\[
ho	imeslpha
\]

first, while fixing workload and heterogeneity.

Candidate reduced design:

\[
30	imes5=150
\]

instances.

Final experimental design should be frozen after pilot tests.

---

# 58. PROJECT LEVELS

## Level 1 — Core foundation

- literature audit,
- problem definition,
- mathematical formulation,
- KERC mapping,
- hand verification,
- CP-SAT base model,
- reproducible instance generator.

## Level 2 — Target

- energy objective,
- peak objective,
- epsilon-constraint/Pareto,
- baseline comparison,
- sensitivity analysis,
- physical testbed,
- physical validation,
- Raspberry Pi deployment.

## Level 3 — Advanced stretch

- Monte Carlo uncertainty,
- NSGA-III,
- exact vs approximate comparison,
- additional large instances.

## Level 4 — Stretch

- event-triggered/rolling-horizon rescheduling,
- state updates,
- disruption injection.

Do not build Level 4 before Levels 1–2 are stable.

---

# 59. UNCERTAINTY EXTENSION — STRETCH

Potential experiment:

Perturb processing times around the deterministic schedule.

Evaluate:

- expected cost,
- worst-case cost,
- deadline violations,
- peak deviations.

Candidate:

\[
K=100
\]

scenarios.

This is scenario evaluation unless a full stochastic optimization model is explicitly developed.

---

# 60. HARDWARE DEPENDENCY

Physical testbed work depends on a validated computational model.

Core dependency:

```text
Literature
↓
Mathematics
↓
Hand verification
↓
CP-SAT
↓
Energy model
↓
Peak model
↓
Baselines
↓
Pareto
↓
Sensitivity
↓
Physical validation
```

Hardware procurement can occur in parallel, but full integration should wait for a stable core model.

---

# 61. DATA CLASSIFICATION

## REAL / MEASURED

- voltage,
- current,
- power,
- energy,
- actual peak,
- actual ON/OFF timing,
- calibration observations.

## MODELLED / DESIGNED

- jobs,
- processing times,
- precedence,
- machine eligibility,
- deadlines,
- tariff parameters,
- sensitivity factors.

## SIMULATED

- large workload sets,
- parameter sweeps,
- Monte Carlo scenarios,
- large-scale optimization experiments.

Never present synthetic data as physical measurements.

---

# 62. REPOSITORY STRUCTURE

```text
EL/
│
├── 00_project_overview/
├── 01_rubric/
├── 02_research/
│   ├── literature/
│   │   ├── papers/
│   │   ├── literature_matrix/
│   │   └── notes/
│   ├── prompts/
│   └── validation/
│
├── 03_tariff/
│   ├── official/
│   ├── supporting/
│   ├── extracted/
│   └── tariff_reference.md
│
├── 04_mathematical_model/
│   ├── derivation/
│   ├── formulation/
│   └── verification/
│       └── test_instances/
│
├── 05_planning/
├── 06_data/
├── 07_src/
├── 08_experiments/
├── 09_hardware/
│   ├── esp32/
│   ├── ina226/
│   ├── testbed/
│   └── raspberry_pi/
├── 10_results/
├── 11_report/
├── 12_tools/
├── tests/
├── PROJECT_STATUS.md
├── README.md
└── requirements.txt
```

---

# 63. CURRENT FILE ORGANIZATION

Current master:

```text
00_project_overview/energy_scheduling_project_master_context.md
```

Current plan:

```text
05_planning/master_execution_plan.md
```

Historical validation:

```text
02_research/validation/energy_scheduling_full_validation.md
02_research/validation/energy_scheduling_research_validation.md
```

Current tariff reference:

```text
03_tariff/tariff_reference.md
```

Current hardware specification:

```text
09_hardware/current_hardware_spec.md
```

Current mathematical files:

```text
04_mathematical_model/
├── derivation/literature_to_equation.md
├── formulation/mathematical_model_v1.md
└── verification/
```

---

# 64. HISTORICAL DOCUMENT POLICY

The following earlier reports may contain PZEM or older tariff/model assumptions.

Mark them:

```markdown
> [!WARNING]
> HISTORICAL / REFERENCE DOCUMENT
>
> This document records an earlier project state.
> It may contain superseded PZEM-004T hardware references or earlier
> tariff/model assumptions.
>
> Use the current project master context, master execution plan,
> current tariff reference, and current hardware specification
> for the present project design.
```

Do not modify historical claims merely to make history look current.

---

# 65. CURRENT HARDWARE SPECIFICATION CONTENT

Create:

```text
09_hardware/current_hardware_spec.md
```

Required content:

```text
Current status
Physical testbed purpose
INA226 measurement layer
ESP32 sensing/control layer
Relay/MOSFET load control
12V DC loads
Raspberry Pi role
Communication
Safety
PZEM superseded note
Exact component verification checklist
```

---

# 66. CURRENT TARIFF SPECIFICATION CONTENT

Create:

```text
03_tariff/tariff_reference.md
```

Required content:

- KERC source,
- tariff category,
- study year,
- effective date,
- base energy charge,
- demand charge,
- billing demand formula,
- demand rounding,
- excess-demand condition,
- PF condition,
- ToD periods,
- ToD applicability,
- discounted energy scheme caveat,
- kVA versus kW distinction,
- monthly billing versus testbed horizon,
- normalized \(ho\) research model.

---

# 67. MATHEMATICAL FOUNDATION FILES

Create:

```text
04_mathematical_model/
├── derivation/
│   ├── literature_to_equation.md
│   └── assumptions.md
├── formulation/
│   └── mathematical_model_v1.md
└── verification/
    ├── hand_calculations.md
    └── test_instances/
```

Do not call `mathematical_model_v1.md` final until literature extraction is finished.

---

# 68. VALIDATION REQUIREMENT

Before optimization experiments:

```text
Hand calculation
      =
Python evaluator
      =
CP-SAT solution
```

for small hand-solvable instances.

Minimum expected checks:

- job assignment,
- precedence,
- machine non-overlap,
- duration,
- energy,
- tariff slot,
- peak power,
- objective values.

---

# 69. REPRODUCIBILITY REQUIREMENTS

Use:

- Git,
- fixed random seeds,
- versioned input instances,
- solver configuration logs,
- raw CSV outputs,
- experiment IDs,
- timestamps,
- stored measured calibration data,
- requirements.txt,
- README reproduction instructions.

---

# 70. FAILURE MODES

| Failure | Likely cause | Response |
|---|---|---|
| CP-SAT infeasible | invalid constraints/epsilon | inspect model and bounds |
| Solver timeout | instance too large | report limit or reduce size |
| Few Pareto points | weak conflict/coarse grid | verify formulation before changing method |
| All methods similar | tariff/instance conditions | report valid null finding |
| INA226 zero reading | wiring/address | inspect I²C and wiring |
| Relay fails | logic/drive issue | verify module and switching circuit |
| MQTT failure | Wi-Fi/broker | debug or use serial fallback |
| Measurement above prediction | calibration/model mismatch | recalibrate |
| Measurement below prediction | incomplete load model | inspect actual behavior |
| Raspberry Pi slow | compute limitation | report scalability |
| Timing drift | software clock | improve timing/document error |
| Supply overload | simultaneous load current | verify supply margin |
| Wrong schedule | solver/model bug | return to hand test |
| Trivial instances | excessive slack | revise workload generator |

---

# 71. DEFINITION OF DONE

## Research

- [ ] 15–20 candidate papers identified.
- [ ] 5–8 foundational papers verified.
- [ ] Literature matrix complete.
- [ ] Literature-to-equation traceability complete.
- [ ] Research gap written conservatively.

## Tariff

- [ ] Official KERC PDF preserved.
- [ ] HT-2(a) reference established.
- [ ] FY2026–27 rate recorded.
- [ ] ToD schedule recorded.
- [ ] Billing-demand rule recorded.
- [ ] kVA/kW distinction documented.
- [ ] Monthly-vs-testbed issue documented.

## Mathematics

- [ ] Problem class selected.
- [ ] Sets defined.
- [ ] Parameters defined.
- [ ] Variables defined.
- [ ] Constraints defined.
- [ ] Objectives defined.
- [ ] Each major equation traceable.
- [ ] Small hand instance verified.

## Software

- [ ] M0 validated.
- [ ] Energy model validated.
- [ ] Peak model validated.
- [ ] Baselines validated.
- [ ] epsilon-constraint validated.
- [ ] Pareto outputs validated.
- [ ] Instance generator reproducible.
- [ ] Unit/integration tests implemented.

## Experiments

- [ ] Baseline comparison.
- [ ] Pareto analysis.
- [ ] Bi-vs-tri common evaluation.
- [ ] Demand sensitivity.
- [ ] ToD sensitivity.
- [ ] Workload sensitivity.
- [ ] Heterogeneity sensitivity.
- [ ] Scalability.
- [ ] Statistics.
- [ ] Phase map.

## Hardware

- [ ] Physical testbed assembled.
- [ ] INA226 calibrated.
- [ ] Measurements logged.
- [ ] Schedule execution works.
- [ ] Predicted-vs-measured comparison completed.
- [ ] Uncertainty characterized.

## Raspberry Pi

- [ ] CP-SAT runs on RPi.
- [ ] Benchmark instances executed.
- [ ] Timing recorded.
- [ ] Limitations documented.

## Documentation

- [ ] README.
- [ ] requirements.txt.
- [ ] raw CSV results.
- [ ] plots.
- [ ] experiment metadata.
- [ ] limitations.
- [ ] report.
- [ ] poster/presentation.

---

# 72. EXACT CURRENT STATUS

## Completed

- SDG 9 project direction.
- Rubric analysis.
- Project idea selection.
- Research-gap audit.
- Research-validation report.
- Master execution plan.
- Project folder reorganization.
- KERC tariff-order acquisition and verification.
- Correction from PZEM-004T to INA226 for the planned DC testbed.

## Current phase

**Literature-to-Mathematical-Foundation**

## Immediate milestone

```text
15–20 verified papers
        ↓
5–8 foundational papers
        ↓
literature-to-model matrix
        ↓
literature-to-equation map
        ↓
mathematical model v1
        ↓
hand verification
```

## Do not start yet

- large experiments,
- full hardware integration,
- dashboard development,
- rolling-horizon scheduling,
- ML/deep learning,
- NSGA-III,
- unnecessary IoT features.

---

# 73. EXACT NEXT EXECUTION ORDER

### Step 1
Replace the old canonical project context with this V2 context.

### Step 2
Create:

```text
09_hardware/current_hardware_spec.md
```

### Step 3
Create:

```text
03_tariff/tariff_reference.md
```

### Step 4
Mark the old PZEM validation documents as historical.

### Step 5
Create:

```text
02_research/prompts/literature_search_prompt.md
```

### Step 6
Use Gemini 3.1 Pro High to search for verified papers.

### Step 7
Save:

```text
02_research/literature/notes/literature_search_round_1.md
```

### Step 8
Download the strongest papers to:

```text
02_research/literature/papers/
```

### Step 9
Populate:

```text
02_research/literature/literature_matrix/
literature_to_model_matrix.md
```

### Step 10
Create:

```text
04_mathematical_model/derivation/literature_to_equation.md
```

### Step 11
Select the actual scheduling problem class.

### Step 12
Write Mathematical Model v1.

### Step 13
Hand-verify it.

### Step 14
Only then implement CP-SAT.

---

# 74. GEMINI WORKFLOW

Gemini should be given the **current** project context first:

```text
energy_scheduling_project_master_context.md
master_execution_plan.md
current_hardware_spec.md
tariff_reference.md
```

Then provide the literature-search task.

Instruction:

> **Do not design the final mathematical model yet. Find and verify peer-reviewed formulations first.**

Gemini should not have to infer which architecture is current.

---

# 75. LITERATURE SEARCH OUTPUT FORMAT

For each paper Gemini should provide:

```text
Citation
Verification source
DOI
Problem class
Decision variables
Objectives
Constraints
Energy model
Tariff model
Peak model
Demand-charge model
Solution method
Assumptions
Equation/page references
Reusable component
Required adaptation
Limitations
Relevance
```

The final selection should contain enough evidence to derive the project model transparently.

---

# 76. FINAL PROJECT PIPELINE

```text
SDG 9 RUBRIC
      ↓
PROJECT DEFINITION
      ↓
RESEARCH-GAP AUDIT
      ↓
OFFICIAL KERC TARIFF
      ↓
LITERATURE SEARCH
      ↓
PAPER VERIFICATION
      ↓
LITERATURE → EQUATION MATRIX
      ↓
MATHEMATICAL MODEL
      ↓
HAND VERIFICATION
      ↓
CP-SAT IMPLEMENTATION
      ↓
BASELINES
      ↓
ENERGY MODEL
      ↓
PEAK MODEL
      ↓
EPSILON-CONSTRAINT / PARETO
      ↓
STATISTICAL EXPERIMENTS
      ↓
SENSITIVITY / PHASE MAP
      ↓
PHYSICAL CALIBRATION
      ↓
PHYSICAL EXECUTION
      ↓
PREDICTED vs MEASURED VALIDATION
      ↓
RASPBERRY PI DEPLOYMENT
      ↓
SCALABILITY BENCHMARK
      ↓
FINAL REPORT
```

---

# 77. NON-NEGOTIABLE RULES

1. No fabricated citations.
2. No fabricated DOI or equation numbers.
3. No unsupported novelty claims.
4. No preclaimed improvement percentages.
5. No silent kW/kVA substitution.
6. No claim that short physical runs equal monthly industrial bills.
7. No claim that the testbed is a real factory.
8. No claim that MQTT/ESP32/RPi is research novelty.
9. No arbitrary threshold presented as discovered fact.
10. No adaptive scheduling before static scheduling works.
11. No large experiments before model verification.
12. No global rewrite of historical documents that falsifies project history.
13. Every major equation must be literature-derived, mathematically derived, or explicitly assumed.
14. Experimental factors must have definitions.
15. Negative results must be reported.

---

# 78. SINGLE-SENTENCE PROJECT DEFINITION

> **We study an established energy-aware production-scheduling problem under a verified Karnataka industrial tariff, examine the additional role of peak electrical demand through systematic parameterized analysis, and physically validate the resulting electrical predictions using a low-voltage measured machine-load emulation testbed.**

---

# 79. CURRENT PRIORITY

\[
oxed{	extbf{LITERATURE → EQUATIONS → MODEL}}
\]

This is the immediate project priority.



---

# TARIFF REFERENCE


---

# LITERATURE SEARCH PROMPT

