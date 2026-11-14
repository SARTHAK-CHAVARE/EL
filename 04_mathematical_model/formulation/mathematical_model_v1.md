# Mathematical Model Formulation V1.0: Peak-Aware Production Scheduling

**Project:** Peak-Aware Energy-Cost Production Scheduling for Small Manufacturing Systems Under Industrial Tariff Structures: A Multi-Objective Optimization Study with Physical Validation  
**Phase:** Mathematical Foundation (Phase 2 Deliverable)  
**Date:** 2026-10-27  
**Author:** Antigravity AI Pair Programmer  
**Status:** Canonical Formulation V1.0 — Ready for Verification and Hand-Solving  

---

## 1. Context, Scope, and Modelling Philosophy

### 1.1. Research Problem and Philosophy
The central objective of this research is to evaluate the economic and operational trade-offs of industrial production scheduling when electricity tariffs impose both **time-varying energy consumption charges** ($\text{₹}/\text{kWh}$) and **peak power demand charges** ($\text{₹}/\text{kW}$ or $\text{₹}/\text{kVA}$).

The governing research question is:
> *Under what combinations of demand-charge intensity, time-of-use tariff variation, workload intensity, and machine-power heterogeneity does peak-aware production scheduling provide a statistically significant economic benefit over energy-cost-only scheduling?*

To answer this question rigorously, the mathematical formulation must satisfy four core methodological requirements:
1. **Unified Feasibility Foundation:** All scheduling strategies must operate over an identical set of operational constraints (job processing requirements, machine capacities, non-preemption, non-overlap, and completion deadlines). Feasible solution spaces must be identical across strategies.
2. **Controlled Objective Separation:** Strategies must differ solely in their objective functions, enabling strict paired comparisons of schedules generated from the exact same manufacturing instances.
3. **Dimensional and Physical Consistency:** Energy, power, time, and monetary units must be mathematically and dimensionally coherent.
4. **Empirical Defensibility:** The model must not claim algorithmic novelty from combining existing literature elements. The contribution is a **candidate modelling synthesis and empirical sensitivity study** validated on a physical machine-load emulation testbed.

---

### 1.2. The Three Evaluated Scheduling Strategies

The formulation supports three distinct scheduling strategies:

```
+--------------------------------------------------------------------------------------------------+
|                                  SHARED CONSTRAINT FOUNDATION                                    |
|   (Machine non-overlap, job non-preemption, single assignment, deadline & horizon bounds)        |
+--------------------------------------------------------------------------------------------------+
                                                 |
         +---------------------------------------+---------------------------------------+
         |                                       |                                       |
         v                                       v                                       v
+-------------------------------+   +-------------------------------+   +-------------------------------+
|     STRATEGY A: BASELINE      |   |  STRATEGY B: ENERGY-COST-ONLY |   |   STRATEGY C: PEAK-AWARE      |
|  Minimise Makespan (C_max)    |   |  Minimise Energy Cost (EC)    |   |  Minimise Total Cost (EC + DC)|
|  - High concurrency           |   |  - Off-peak load clustering   |   |  - Coordinated load staggering|
|  - Oblivious to tariffs       |   |  - Secondary peak spikes      |   |  - Peak shaving & valley fill |
+-------------------------------+   +-------------------------------+   +-------------------------------+
```

#### Strategy A: Production-Oriented Baseline ($\min C_{\max}$)
- **Operational Focus:** Maximizing throughput and equipment productivity by completing all jobs in the shortest possible time.
- **Expected Behavioral Mechanism:** Tightly packs operations as soon as machines and jobs become available. Ignores electricity price variations and simultaneous power draw, often running all machines concurrently. This minimizes makespan but produces high coincidental peak power demands and operates indiscriminately during expensive on-peak tariff hours.

#### Strategy B: Energy-Cost-Only Scheduling ($\min EC$)
- **Operational Focus:** Minimizing electricity consumption expenditure under time-varying (Time-of-Use / Time-of-Day) tariffs subject to a production deadline $D$.
- **Expected Behavioral Mechanism:** Intentionally shifts production activities into low-tariff windows (e.g., night-time off-peak hours). However, because the objective assigns zero cost to instantaneous power spikes, the solver has an economic incentive to run all available machines **simultaneously** during cheap tariff hours to finish within the low-rate window. This creates severe **coincident demand spikes (secondary peaks)** that destabilize the local power supply and incur high demand charges under two-part industrial tariffs.

#### Strategy C: Peak-Aware Production Scheduling ($\min TEC = EC + DC$)
- **Operational Focus:** Minimizing total electricity costs by explicitly balancing time-varying energy charges against peak demand penalties over the utility billing interval.
- **Expected Behavioral Mechanism:** Operates at the trade-off frontier. When the demand charge rate is sufficiently high, the scheduler intentionally staggers machine execution during off-peak periods, selectively allocates power-heavy jobs to more energy-efficient machines, and accepts small makespan increases to keep the maximum interval demand below critical thresholds.

---

## 2. Selection and Justification of the Scheduling Problem Class

### 2.1. Comparison of Candidate Problem Classes

| Scheduling Problem Class | Assignment Flexibility | Machine Heterogeneity Supported? | Data Requirements | Complexity Class | Physical Testbed Compatibility | Recommendation |
|---|---|---|---|---|---|---|
| **Identical Parallel Machines** ($P || \dots$) | None (all machines equal) | **No** (homogeneous power $P_m = P$) | Low ($p_j, E_j$) | Strongly NP-hard under ToU | Poor (testbed has distinct load types: motor, heater, lamp) | **Rejected** (Cannot test Factor 4: machine-power heterogeneity) |
| **Unrelated Parallel Machines** ($R || \dots$) | **High** (jobs assigned across machines) | **Yes** ($p_{jm}, P_{jm}$ or $P_m$) | Moderate ($p_{jm}, P_m$) | Strongly NP-hard (Aghelinejad 2019) | **Ideal** (1-to-1 match to 3–4 distinct 12V DC load emulators) | **SELECTED FOR V1** |
| **Flexible Job Shop** ($FJSP$) | Very high (routing + sequencing) | **Yes** ($P_{ijk}$) | High (operation orders, routing tables) | Extremely high (combinatorial explosion) | Poor (requires artificial multi-stage transfers on 3-channel testbed) | **Rejected for V1** (Adds routing confounders; obscures tariff causal effects) |

### 2.2. Selection Rationale for V1
The **Unrelated Parallel Machine Scheduling Problem with Machine-Dependent Power draws ($R | p_{jm}, P_{jm}, \text{ToU} | C_{\max}, EC, P_{\max}$)** is chosen as the foundational problem class for V1:
1. **Direct Research Question Alignment:** It provides the minimal mathematical structure necessary to simultaneously vary all four experimental factors:
   - *Demand-charge intensity:* Evaluated via the demand charge parameter in the objective.
   - *ToU variation:* Evaluated via time-indexed tariff vectors.
   - *Workload intensity:* Evaluated via the ratio of total job processing workload to available machine-hours.
   - *Machine-power heterogeneity:* Evaluated via differences in power draws across parallel machines.
2. **Direct Hardware-in-the-Loop Mapping:** The project's experimental testbed consists of 3 to 4 distinct 12V DC electrical load emulators (e.g., DC motor ~15W, DC heating cartridge ~25W, LED bank ~10W, DC fan ~8W) connected to independent switching channels and instrumented with INA226 voltage/current sensors. Each physical channel represents a machine with distinct power and operational characteristics.
3. **Solver Tractability on Edge Hardware:** For instance sizes typical of small manufacturing cells ($n = 6 \text{ to } 20$ jobs, $m = 3 \text{ to } 4$ machines over an 8-to-24 hour shift), the unrelated parallel machine model can be solved to proven optimality or bounded optimality gap on a Raspberry Pi 5 within documented computational limits (e.g., 60–300 seconds), whereas an FJSP would frequently timeout.

---

### 2.3. Decision on Machine Operating States (Idle, Standby, Transition)

The literature audit ([`literature_audit_before_model_v1.md`](file:///c:/Project/EL/02_research/literature/notes/literature_audit_before_model_v1.md)) verified that while multi-state switching (processing, idle, warmup, cooldown, OFF) is formulated in single-machine studies (Mouzon et al. 2007; Aghelinejad et al. 2019), it is completely omitted in demand-charge scheduling models (Sung & Kwon 2026).

**Decision for Core V1 Model:**
- Machine state is binary: **Processing** ($ON$) vs. **Non-Processing** ($OFF$).
- During non-processing intervals, the machine draws zero dynamic processing power.
- A constant facility baseline load ($P_{\text{base}}$) is incorporated to represent unmanaged auxiliary loads (lighting, facility control, sensors).
- **Justification for Omission in V1:**
  1. Incorporating dynamic idle/standby power and turn-off/turn-on breakeven transitions ($S = SE / IP$) requires introducing $O(M \times T)$ auxiliary binary variables and big-M linearization constraints.
  2. In small manufacturing systems (e.g., 3D printer clusters, light assembly tools), idle power is a small fraction of active power, and machines are rarely fully de-energized during short inter-job gaps due to recalibration overhead.
  3. Omitting dynamic state switching in V1 allows unambiguous causal attribution of peak-shaving benefits to job assignment and temporal shifting.
- **Documented Limitation & Extension:** This omission is an explicit model simplification. An extended multi-state formulation is formally specified in Section 9 of this document as an architectural extension for future work.

---

## 3. Mathematical Notation, Sets, Parameters, and Variables

### 3.1. Sets and Indices

| Symbol | Definition | Domain / Range |
|---|---|---|
| $\mathcal{J}$ | Set of independent production jobs to be scheduled | $\{1, 2, \dots, N\}$, index $j$ |
| $\mathcal{M}$ | Set of heterogeneous parallel machines | $\{1, 2, \dots, M\}$, index $m$ |
| $\mathcal{T}$ | Set of uniform discrete scheduling time slots | $\{1, 2, \dots, T\}$, index $t$ |
| $\mathcal{K}$ | Set of consecutive, non-overlapping utility demand measurement intervals | $\{1, 2, \dots, K\}$, index $k$ |
| $\mathcal{T}_k$ | Set of time slots belonging to demand interval $k$ | $\mathcal{T}_k \subset \mathcal{T}$, $|\mathcal{T}_k| = L$ |
| $\mathcal{M}_j$ | Set of eligible machines capable of processing job $j$ | $\mathcal{M}_j \subseteq \mathcal{M}$ |

---

### 3.2. Input Parameters and Dimensional Consistency

All physical and economic parameters must satisfy strict dimensional consistency:

| Symbol | Description | Canonical Unit | Typical Experimental Range |
|---|---|---|---|
| $\Delta t$ | Duration of a single discrete scheduling time slot | $\text{hours } (\text{h})$ | $0.0833\text{ h } (5\text{ min}) \text{ or } 0.25\text{ h } (15\text{ min})$ |
| $L$ | Length of utility demand billing interval in time slots | integer | $L = 3 \text{ (if } \Delta t = 5\text{ min, window } = 15\text{ min})$<br>$L = 1 \text{ (if } \Delta t = 15\text{ min, window } = 15\text{ min})$ |
| $H$ | Total scheduling time horizon | $\text{hours } (\text{h})$ | $T \cdot \Delta t$ (e.g., $8\text{ h, } 12\text{ h, or } 24\text{ h}$) |
| $p_{jm}$ | Processing time of job $j$ on machine $m$ | integer slots | $p_{jm} \ge 1$, duration in hours is $p_{jm} \cdot \Delta t$ |
| $P_{jm}$ | Electrical active power demand when job $j$ runs on machine $m$ | $\text{kW}$ | $0.005\text{ kW to } 50.0\text{ kW}$ (testbed: $5\text{W to } 30\text{W}$) |
| $P_{\text{base}}$ | Constant facility background/auxiliary electrical power | $\text{kW}$ | $P_{\text{base}} \ge 0$ |
| $C_t$ | Time-of-Use energy tariff rate at time slot $t$ | $\text{₹} / \text{kWh}$ | Off-peak: ₹5.60; Normal: ₹6.60; Peak: ₹7.60 |
| $\rho$ | Normalized demand charge parameter (Model A) | $\text{₹} / \text{kW}$ | Parameterized sensitivity sweep ($0 \text{ to } 500\text{ ₹/kW}$) |
| $D$ | Global production completion deadline for all jobs | integer slots | $D \le T$ |
| $r_j$ | Earliest release time slot of job $j$ | integer slot | $1 \le r_j \le T$ (Default $r_j = 1$) |
| $d_j$ | Individual due date time slot of job $j$ | integer slot | $r_j + p_{jm} \le d_j \le D$ |

---

### 3.3. Decision Variables

| Variable | Mathematical Domain | Interpretation |
|---|---|---|
| $x_{jmt}$ | Binary $\in \{0, 1\}$ | Equals $1$ if job $j$ **starts** on machine $m$ at the beginning of time slot $t$; $0$ otherwise. |
| $y_{jmt}$ | Binary $\in \{0, 1\}$ | Equals $1$ if job $j$ is **actively processing** on machine $m$ during time slot $t$; $0$ otherwise. |
| $z_{jm}$ | Binary $\in \{0, 1\}$ | Equals $1$ if job $j$ is **assigned** to machine $m$; $0$ otherwise. |
| $C_j$ | Continuous / Integer $\in [0, T]$ | Actual temporal completion time slot of job $j$. |
| $C_{\max}$ | Continuous / Integer $\in [0, T]$ | Schedule makespan (completion time of the last job across all machines). |
| $P(t)$ | Continuous $\ge 0$ ($\text{kW}$) | Total aggregate facility power demand during time slot $t$. |
| $p_k^{\text{int}}$ | Continuous $\ge 0$ ($\text{kW}$) | Average active electrical power demand during demand interval $k \in \mathcal{K}$. |
| $P_{\max}$ | Continuous $\ge 0$ ($\text{kW}$) | Peak demand over the entire scheduling horizon across all measurement intervals. |
| $EC$ | Continuous $\ge 0$ ($\text{₹}$) | Total Time-of-Use electrical energy consumption cost. |
| $DC$ | Continuous $\ge 0$ ($\text{₹}$) | Total modeled electrical demand charge. |
| $TEC$ | Continuous $\ge 0$ ($\text{₹}$) | Total electricity cost ($TEC = EC + DC$). |

---

## 4. Demand-Charge Modelling: Mandatory Conceptual Distinction

A major finding of the pre-modelling audit is that academic literature benchmarks must not be conflated with commercial utility bills. This formulation establishes two distinct, fully documented models:

```
+--------------------------------------------------------------------------------------------------+
|                                    DEMAND-CHARGE TAXONOMY                                        |
+--------------------------------------------------------------------------------------------------+
|                                                                                                  |
|   MODEL A: NORMALIZED RESEARCH BENCHMARK            MODEL B: ACTUAL TARIFF MAPPING               |
|   - Purpose: Controlled experimental sensitivity    - Purpose: Real-world economic calibration   |
|   - Demand Metric: Peak Active Power (kW)           - Demand Metric: Billing Apparent Demand (kVA|
|   - Window: Rolling/Fixed Interval (15-min)         - Window: 15-min Integration Window          |
|   - Horizon: Shift / Day (8–24 h)                   - Horizon: Monthly Utility Billing Cycle     |
|   - Rate: Parameterized intensity rho (₹/kW)        - Rate: ₹350/kVA/month with 90% CD Ratchet   |
|   - Role: Optimization objective engine             - Role: Empirical discussion & extrapolation |
|                                                                                                  |
+--------------------------------------------------------------------------------------------------+
```

### 4.1. Model A — Normalized Research Benchmark (Optimization Engine)

In Model A, the demand charge represents the economic cost of peak electrical capacity over the scheduling horizon:

$$DC_A = \rho \cdot P_{\max}$$

Where:
- $P_{\max}$ is the maximum interval-averaged demand (in $\text{kW}$) recorded over any fixed measurement interval $k \in \mathcal{K}$ of duration $L \cdot \Delta t$ (typically 15 minutes).
- $\rho$ is the **demand-charge intensity parameter**, expressed in $\text{₹}/\text{kW}$ per scheduling horizon.

#### Parameter Calibration and Normalization
To enable fair comparison across different instance sizes, workloads, and scheduling horizons, $\rho$ is calibrated using two complementary reference bases:

1. **Daily-Equivalent Tariff Reference ($\rho_{\text{daily}}$):**
   Derived by prorating a standard monthly industrial demand rate over working days:
   $$\rho_{\text{daily}} = \frac{\text{Monthly Demand Charge Rate } (\text{₹}/\text{kVA})}{N_{\text{billing days}}}$$
   For the KERC HT-2(a) rate of ₹350/kVA/month over 25 working days (assuming power factor $PF = 1.0$ on the testbed):
   $$\rho_{\text{daily}} \approx \frac{350}{25} = 14.00 \text{ ₹/kW/day}$$

2. **Dimensionless Ratio to Energy Cost ($\rho_{\text{ratio}}$):**
   Defined relative to the average base energy price $\bar{C}$:
   $$\kappa = \frac{\rho \cdot 1\text{ kW}}{\bar{C} \cdot (1\text{ kW} \times 1\text{ h})} = \frac{\rho}{\bar{C} \cdot 1\text{ h}}$$
   This parameter $\kappa$ governs the trade-off slope: how many kilowatt-hours of off-peak energy savings an operator is willing to sacrifice to reduce peak demand by $1\text{ kW}$.

---

### 4.2. Model B — Actual Industrial Tariff Mapping (Regulatory Grounding)

#### Tariff Category Applicability Audit
Inspection of the official KERC Tariff Order 2025 and [`tariff_reference.md`](file:///c:/Project/EL/03_tariff/tariff_reference.md) reveals:
- **HT-2(a) (High Tension Industrial):** Applies to industrial installations supplied at High Voltage ($\ge 11\text{ kV}$), typically with contract demand $\ge 100\text{ kVA}$. It imposes:
  - Energy charge: Base rate ₹6.60/kWh.
  - Time-of-Day (ToD) adjustments (Dec–June): Peak (+₹1.00/kWh, 06:00–09:00 and 18:00–22:00); Off-peak (−₹1.00/kWh, 22:00–06:00); Normal (₹0.00/kWh, 09:00–18:00).
  - Demand charge: ₹350/kVA/month of **Billing Demand ($BD$)**.
  - Billing Demand Rule: $BD = \max(MD, 0.90 \times CD)$, where $MD$ is the maximum demand recorded in any 15-minute window during the month, and $CD$ is the contract demand.
- **LT-5 (Low Tension Industrial):** Applies to small and micro manufacturing units connected at 415V/230V with loads $< 67\text{ kW}$ ($< 100\text{ kVA}$). Crucially, standard LT-5 tariffs bill fixed charges based on **Sanctioned Load (kW)**, rather than dynamically recorded maximum demand!

#### Mandatory Real-World Caveats and Omissions Documented
When comparing Model A with Model B, the following real-world regulatory boundaries must be explicitly declared:
1. **Apparent Demand vs. Active Power ($\text{kVA}$ vs. $\text{kW}$):** Commercial utility meters record apparent power $S = \sqrt{P^2 + Q^2}$ in kVA over 15-minute integration windows. The DC testbed operates at unity power factor ($PF = 1.0$, $P = S$). In AC industrial settings with motors and inductive loads, $MD_{\text{kVA}} = MD_{\text{kW}} / PF$. If $PF = 0.85$, a $100\text{ kW}$ peak incurs a $117.6\text{ kVA}$ billing demand.
2. **Monthly Aggregation and Ratchet Mechanism:** Utility demand charges are billed monthly based on the single highest 15-minute peak across the entire month. A daily production schedule only incurs marginal demand savings if that specific day's peak establishes the monthly maximum. Furthermore, if $MD \le 0.90 \times CD$, reducing peak power yields **zero demand charge savings** under the KERC 90% contract ratchet!
3. **Power Factor Penalties and Tax Surcharges:** KERC imposes low power factor surcharges for $PF < 0.90$ and state electricity tax (9%). These are excluded from the core optimization engine.

**Conclusion:** Model A is the primary mathematical model used for optimization and sensitivity analysis. Model B provides the empirical discussion framework for real-world translation.

---

## 5. Complete Mathematical Constraint Formulation

### 5.1. Job Assignment and Single Execution Constraints

Each job $j \in \mathcal{J}$ must be assigned to exactly one eligible machine $m \in \mathcal{M}_j$, and must start exactly once within the scheduling horizon:

$$\sum_{m \in \mathcal{M}_j} z_{jm} = 1, \quad \forall j \in \mathcal{J} \tag{1}$$

$$\sum_{t=r_j}^{D - p_{jm} + 1} x_{jmt} = z_{jm}, \quad \forall j \in \mathcal{J}, \forall m \in \mathcal{M}_j \tag{2}$$

$$x_{jmt} = 0, \quad \forall j \in \mathcal{J}, \forall m \notin \mathcal{M}_j, \forall t \in \mathcal{T} \tag{3}$$

$$x_{jmt} = 0, \quad \forall j \in \mathcal{J}, \forall m \in \mathcal{M}_j, \forall t < r_j \text{ or } t > D - p_{jm} + 1 \tag{4}$$

*Explanation:* Constraint (1) guarantees single machine assignment. Constraint (2) links the start-time binary variable $x_{jmt}$ to the assignment variable $z_{jm}$, ensuring that if job $j$ is assigned to machine $m$, it starts at exactly one valid time slot between its release time $r_j$ and latest feasible start time $D - p_{jm} + 1$. Constraints (3)–(4) forbid assignment to ineligible machines and invalid start times.

---

### 5.2. Non-Preemption and Operation Continuity Constraints

Once a job begins execution on machine $m$, it must occupy the machine for $p_{jm}$ contiguous time slots without preemption or interruption:

$$y_{jmt} = \sum_{t' = \max(t - p_{jm} + 1, 1)}^t x_{jmt'}, \quad \forall j \in \mathcal{J}, \forall m \in \mathcal{M}_j, \forall t \in \mathcal{T} \tag{5}$$

*Explanation:* Variable $y_{jmt}$ indicates whether job $j$ is actively running on machine $m$ during time slot $t$. Equation (5) enforces that $y_{jmt} = 1$ if and only if job $j$ was started at some time slot $t'$ within the lookback window $[t - p_{jm} + 1, t]$. This formulation avoids big-M inequalities and guarantees non-preemption.

---

### 5.3. Machine Capacity and Non-Overlap Constraints

Each machine $m$ can process at most one job at any given time slot $t$:

$$\sum_{j \in \mathcal{J} : m \in \mathcal{M}_j} y_{jmt} \le 1, \quad \forall m \in \mathcal{M}, \forall t \in \mathcal{T} \tag{6}$$

*Audit Note:* This constraint directly corrects the critical defect identified in Moon et al. (2013), where the absence of a machine non-overlap constraint permitted multiple jobs to execute simultaneously on the same machine.

---

### 5.4. Valid Job Completion Times and Makespan Definition

The actual temporal completion time slot $C_j$ of job $j$ is determined by its start time and machine-dependent processing duration:

$$C_j = \sum_{m \in \mathcal{M}_j} \sum_{t=r_j}^{D - p_{jm} + 1} (t + p_{jm} - 1) \cdot x_{jmt}, \quad \forall j \in \mathcal{J} \tag{7}$$

Individual job due dates are enforced by:
$$C_j \le d_j, \quad \forall j \in \mathcal{J} \tag{8}$$

The schedule makespan $C_{\max}$ is defined as the latest actual completion time among all scheduled jobs:

$$C_{\max} \ge C_j, \quad \forall j \in \mathcal{J} \tag{9}$$

$$C_{\max} \le D \tag{10}$$

*Audit Note:* In Moon et al. (2013), makespan was incorrectly formulated as the sum of assigned processing times ($\sum_j p_{ij} \le C_{\max}$). Equation (9) correctly defines makespan using actual temporal completion times ($C_j$), accounting for inserted idle periods and schedule delays.

---

### 5.5. Aggregate Facility Electrical Power Demand

The total active electrical power demand $P(t)$ of the manufacturing facility at time slot $t$ is the sum of all active machine loads plus the baseline load:

$$P(t) = \sum_{m \in \mathcal{M}} \sum_{j \in \mathcal{J} : m \in \mathcal{M}_j} P_{jm} \cdot y_{jmt} + P_{\text{base}}, \quad \forall t \in \mathcal{T} \tag{11}$$

*Dimensional check:* $P_{jm} \in \text{kW}$, $y_{jmt}$ dimensionless binary, $P_{\text{base}} \in \text{kW} \implies P(t) \in \text{kW}$.

---

### 5.6. Utility Measurement Interval Demand and Peak Demand Formulation

Following utility billing standards (KERC 15-minute integration windows) and the validated formulation of Sung & Kwon (2026, Eq. 1f & 4c), the average electrical power demand $p_k^{\text{int}}$ during measurement interval $k \in \mathcal{K}$ is defined by the duration-weighted integral of active power over the interval window $W_k$:

$$p_k^{\text{int}} = \frac{1}{W_k} \int_{t_{\text{start}}^k}^{t_{\text{end}}^k} P(t) \, dt = \frac{\sum_{t \in \mathcal{T}_k} P(t) \cdot \delta_t}{\sum_{t \in \mathcal{T}_k} \delta_t} \tag{12a}$$

Where $\delta_t$ is the physical duration of time slot $t$, and $W_k = \sum_{t \in \mathcal{T}_k} \delta_t$ is the total duration of measurement interval $k$ (e.g., $0.25\text{ h } = 15\text{ minutes}$).

**Uniform Slot Simplification:** If and only if all discrete slots within measurement interval $k$ have an **identical uniform duration** $\delta_t = \Delta t$, with $|\mathcal{T}_k| = L$ slots per window ($W_k = L \cdot \Delta t$), Equation (12a) mathematically simplifies to the arithmetic average:

$$p_k^{\text{int}} = \frac{\sum_{t \in \mathcal{T}_k} P(t) \cdot \Delta t}{L \cdot \Delta t} = \frac{1}{L} \sum_{t \in \mathcal{T}_k} P(t), \quad \forall k \in \mathcal{K} \tag{12b}$$

Substituting Equation (11) into (12b):

$$p_k^{\text{int}} = \frac{1}{L} \sum_{t \in \mathcal{T}_k} \left( \sum_{m \in \mathcal{M}} \sum_{j \in \mathcal{J} : m \in \mathcal{M}_j} P_{jm} \cdot y_{jmt} \right) + P_{\text{base}}, \quad \forall k \in \mathcal{K} \tag{13}$$

The maximum billing demand $P_{\max}$ over the scheduling horizon is bounded by:

$$P_{\max} \ge p_k^{\text{int}}, \quad \forall k \in \mathcal{K} \tag{14}$$

$$P_{\max} \ge 0 \tag{15}$$

*Dimensional check:* Average power over interval $k$ has units $\text{kW}$. $P_{\max}$ has units $\text{kW}$.

---

### 5.7. Time-of-Use Energy Cost Accounting

The total electrical energy consumption cost $EC$ across all scheduling time slots is:

$$EC = \sum_{t \in \mathcal{T}} C_t \cdot P(t) \cdot \Delta t \tag{16}$$

Substituting Equation (11) into (16):

$$EC = \Delta t \sum_{t \in \mathcal{T}} C_t \left( \sum_{m \in \mathcal{M}} \sum_{j \in \mathcal{J} : m \in \mathcal{M}_j} P_{jm} \cdot y_{jmt} + P_{\text{base}} \right) \tag{17}$$

*Dimensional check:* $C_t \in \text{₹}/\text{kWh}$, $P(t) \in \text{kW}$, $\Delta t \in \text{h} \implies C_t \cdot P(t) \cdot \Delta t \in \text{₹}$. Total $EC \in \text{₹}$.

---

## 6. Objective Functions for Strategy Comparisons: Sequential Lexicographic Optimization

### 6.1. Methodological Justification: Why Sequential Lexicographic Optimization Replaces Weighted Sums
Pre-implementation verification audit (Audit Finding ISS-06) established that single-pass linear combination objectives of the form $\min (f_1 + \epsilon f_2)$ fail under Google OR-Tools CP-SAT integer scaling:
1. **Truncation / Vanishing Tie-Breaker:** Small scaling factors round $\epsilon$ to $0$, discarding the secondary tie-breaker.
2. **Objective Corruption:** Large scaling factors risk $\epsilon \cdot \Delta f_2 > \Delta f_1$, causing the solver to sacrifice the primary objective for a secondary gain.

To guarantee **100% strict objective priority** without numerical distortion, all three strategies are solved using **Sequential Lexicographic Optimization** across the **identical shared constraint set (1)–(15)**:

```
+--------------------------------------------------------------------------------------------------+
|                   SEQUENTIAL LEXICOGRAPHIC OPTIMIZATION PROTOCOL (CP-SAT)                        |
+--------------------------------------------------------------------------------------------------+
|                                                                                                  |
|   SHARED CONSTRAINTS: Equations (1)–(15), Horizon T, Global Deadline D, identical for A, B, C    |
|                                                                                                  |
|   STRATEGY A (Production Baseline):                                                              |
|     Phase 1: Solve min C_max s.t. Constraints (1)–(15). Record optimal C_max*.                   |
|     Phase 2: Fix C_max <= C_max*. Solve min sum_j C_j (Total Flow Time). Zero energy bias.       |
|                                                                                                  |
|   STRATEGY B (Energy-Cost-Only):                                                                 |
|     Phase 1: Solve min EC s.t. Constraints (1)–(15) and C_max <= D. Record optimal EC*.          |
|     Phase 2: Fix EC <= EC*. Solve min C_max (Compactness). Zero peak bias (rho = 0).             |
|                                                                                                  |
|   STRATEGY C (Peak-Aware Total Cost):                                                            |
|     Phase 1: Solve min TEC = EC + rho * P_max s.t. Constraints (1)–(15) and C_max <= D.         |
|              Record optimal TEC*.                                                                |
|     Phase 2: Fix TEC <= TEC*. Solve min C_max (Compactness).                                     |
|                                                                                                  |
+--------------------------------------------------------------------------------------------------+
```

---

### 6.2. Strategy A: Production-Oriented Baseline

- **Phase 1 (Primary Solve — Makespan Minimization):**
  $$\min Z_A^{(1)} = C_{\max} \tag{18a}$$
  $$\text{Subject to Constraints (1)–(15)}$$
  - Solver proves global optimality. Record optimal makespan $C_{\max}^*$.
- **Phase 2 (Secondary Solve — Flow-Time Tie-Breaker):**
  $$\min Z_A^{(2)} = \sum_{j \in \mathcal{J}} C_j \tag{18b}$$
  $$\text{Subject to Constraints (1)–(15)} \quad \text{and} \quad C_{\max} \le C_{\max}^* \tag{18c}$$
  - Solves for the schedule with minimum work-in-process flow time among all makespan-optimal schedules.
  - **CRITICAL ANTI-BIAS GUARANTEE:** Strictly zero energy cost or peak demand terms in either phase.

---

### 6.3. Strategy B: Energy-Cost-Only Scheduling

- **Phase 1 (Primary Solve — ToU Energy Cost Minimization):**
  $$\min Z_B^{(1)} = EC = \Delta t \sum_{t \in \mathcal{T}} C_t \cdot P(t) \tag{19a}$$
  $$\text{Subject to Constraints (1)–(15)} \quad \text{and} \quad C_{\max} \le D \tag{19b}$$
  - Solver proves global optimality. Record optimal energy cost $EC^*$.
  - **CRITICAL PROPERTY:** Demand charge parameter $\rho \equiv 0$.
- **Phase 2 (Secondary Solve — Schedule Compactness Tie-Breaker):**
  $$\min Z_B^{(2)} = C_{\max} \tag{19c}$$
  $$\text{Subject to Constraints (1)–(15)}, \quad C_{\max} \le D, \quad \text{and} \quad EC \le EC^* \tag{19d}$$
  - Solves for the earliest-completing schedule among all energy-cost-optimal schedules.

---

### 6.4. Strategy C: Peak-Aware Total Electricity Cost Scheduling

- **Phase 1 (Primary Solve — Total Dual-Tariff Cost Minimization):**
  $$\min Z_C^{(1)} = TEC = EC + \rho \cdot P_{\max} \tag{21a}$$
  $$\text{Subject to Constraints (1)–(15)} \quad \text{and} \quad C_{\max} \le D \tag{21b}$$
  - Where $EC$ is defined by Eq. (17) and $P_{\max}$ is bounded by Eq. (14).
  - Solver proves global optimality. Record optimal total bill $TEC^*$.
- **Phase 2 (Secondary Solve — Schedule Compactness Tie-Breaker):**
  $$\min Z_C^{(2)} = C_{\max} \tag{21c}$$
  $$\text{Subject to Constraints (1)–(15)}, \quad C_{\max} \le D, \quad \text{and} \quad TEC \le TEC^* \tag{21d}$$
  - Solves for the most compact schedule that achieves exact minimum total cost $TEC^*$.

---

## 7. Multi-Objective Analysis: Methodological Evaluation and Recommendation

### 7.1. Methodological Comparison: Weighted-Sum vs. $\epsilon$-Constraint (AUGMECON2)

The master context and execution plan outline a multi-objective trade-off between productivity ($C_{\max}$) and electricity cost ($TEC$).

| Criterion | Weighted-Sum Method ($\sum w_i f_i$) | Standard $\epsilon$-Constraint | AUGMECON2 (Mavrotas & Florios 2013) |
|---|---|---|---|
| **Capture of Non-Convex Pareto Front** | **Fails:** Cannot obtain unsupported efficient solutions on non-convex integer frontiers. | **Succeeds:** Captures all Pareto-optimal points by treating objectives as constraints. | **Succeeds:** Proves exact Pareto set generation for integer/combinatorial programs. |
| **Weakly Efficient Solutions** | Generates weakly efficient points when weights are zero. | Can produce dominated points on flat boundary regions. | **Eliminates weakly dominated points** via tiered lexicographic slack scaling. |
| **Computational Efficiency** | Fast (single solve per weight), but produces redundant points. | Slow (solves full MIP for every grid point, even when redundant). | **Fast:** Uses bypass coefficient $b = \lfloor S_2 / step_2 \rfloor$ to skip redundant solver runs. |
| **CP-SAT Solver Integration** | Straightforward (linear objective). | Requires iterative loop resetting constraint bounds. | Requires programmatic loop managing integer bounds and slack extraction. |

---

### 7.2. Recommendation for V1: Controlled 3-Strategy Comparison + Selective Pareto Benchmarking

**Recommendation:**
1. **Primary Experimental Engine for V1:** **Three-Strategy Comparison (A, B, C).**
   - The central research question asks: *Under what combinations of factors does peak-aware scheduling (C) provide a statistically significant economic benefit over energy-cost-only scheduling (B)?*
   - This hypothesis-testing question is answered directly by paired comparison of Strategies A, B, and C across full factorial instances, without needing full Pareto frontier sweeps for every replication.
2. **Selective Pareto-Front Analysis:**
   - To address Secondary RQ1 (Pareto structure), implement the **bifactorial $\epsilon$-constraint method** on a representative subset of benchmark instances (e.g., small 3-machine 10-job and 4-machine 16-job instances).
   - In this analysis, $C_{\max}$ is constrained to discrete grid levels $\epsilon_l \in [C_{\max}^{\min}, D]$, while optimizing $TEC$ (Strategy C) and $EC$ (Strategy B), explicitly mapping the trade-off surface.
   - Full 3D Pareto frontier generation via AUGMECON2 is reserved as a specialized computational study to prevent combinatorial timeout on edge devices (Raspberry Pi 5).

---

## 8. Implementation Design for Google OR-Tools CP-SAT

### 8.1. Native CP-SAT Construct Mapping

Google OR-Tools CP-SAT is a finite-domain constraint programming solver utilizing SAT techniques. It natively excels with **Interval Variables** and built-in global scheduling constraints.

```
+--------------------------------------------------------------------------------------------------+
|                                   OR-TOOLS CP-SAT MAPPING                                        |
+--------------------------------------------------------------------------------------------------+
|   Mathematical Element          CP-SAT Implementation Construct                                  |
|   -------------------------     --------------------------------------------------------------   |
|   Job Start Time                start_var = model.NewIntVar(r_j, D - p_jm, "start_j")             |
|   Job Duration                  duration = p_jm                                                  |
|   Job Completion Time           end_var = model.NewIntVar(r_j + p_jm, D, "end_j")                |
|   Job Execution Interval        interval_var = model.NewIntervalVar(start, p_jm, end, "int_j")   |
|   Machine Non-Overlap           model.AddNoOverlap(machine_intervals[m])                         |
|   Machine Assignment            model.AddExactlyOne(assignment_bools)                            |
|   Time-Slot Indicator           model.Add(start_var <= t).OnlyEnforceIf(is_active)               |
|                                 model.Add(end_var > t).OnlyEnforceIf(is_active)                  |
|   Interval Peak Demand          model.AddMaxEquality(peak_demand, interval_power_vars)           |
+--------------------------------------------------------------------------------------------------+
```

### 8.2. Integer Scaling for CP-SAT Solvers

CP-SAT requires all decision variables, parameters, and objective coefficients to be **integers**. Floating-point rates must be scaled by exact scalar multipliers:

1. **Power Scaling Factor ($S_P = 1000$):**
   - Active power $P_{jm}$ and $P_{\text{base}}$ are converted from $\text{kW}$ to **watts ($\text{W}$)**:
     $$\tilde{P}_{jm} = \text{round}(P_{jm} \cdot 1000) \in \mathbb{Z}^+$$
2. **Energy Tariff Scaling Factor ($S_C = 100$):**
   - Tariff rate $C_t$ is converted from $\text{₹}/\text{kWh}$ to **paise per kWh** ($\text{₹ } 1 = 100 \text{ paise}$):
     $$\tilde{C}_t = \text{round}(C_t \cdot 100) \in \mathbb{Z}^+$$
3. **Demand Charge Scaling Factor ($S_D = 100$):**
   - Demand charge rate $\rho$ is converted to paise per kW:
     $$\tilde{\rho} = \text{round}(\rho \cdot 100) \in \mathbb{Z}^+$$
4. **Objective Integer Function:**
   To maintain integer arithmetic without precision loss:
   $$\text{Scaled } EC = \sum_{t \in \mathcal{T}} \tilde{C}_t \cdot \left( \sum_{m} \sum_{j} \tilde{P}_{jm} y_{jmt} + \tilde{P}_{\text{base}} \right)$$
   $$\text{True } EC = \frac{\text{Scaled } EC}{S_P \cdot S_C} \cdot \Delta t$$

---

## 9. Experimental Factor Mapping and Metric Definitions

### 9.1. Factorial Parameterization

The model directly operationalizes the four primary factors of the central research question:

```
+--------------------------------------------------------------------------------------------------+
|                                    FOUR-FACTOR DESIGN MATRIX                                     |
+--------------------------------------------------------------------------------------------------+
|                                                                                                  |
|   FACTOR 1: Demand-Charge Intensity (rho)                                                        |
|   - Low (0 ₹/kW), Medium (14 ₹/kW/day), High (50–100 ₹/kW)                                       |
|   - Mechanism: Governs marginal penalty on coincident machine power                              |
|                                                                                                  |
|   FACTOR 2: Time-of-Use Tariff Variation (gamma)                                                 |
|   - Flat (1.0x), Moderate (1.35x), High (1.75x peak-to-off-peak ratio)                           |
|   - Mechanism: Drives operational clustering into cheap off-peak hours                           |
|                                                                                                  |
|   FACTOR 3: Workload Intensity (W)                                                               |
|   - Low (40% capacity), Medium (70% capacity), High (90% capacity / tight deadline)             |
|   - Mechanism: Restricts temporal shifting; forces machines to run concurrently                  |
|                                                                                                  |
|   FACTOR 4: Machine-Power Heterogeneity (sigma_P)                                                |
|   - Low (equal power), Medium (+/- 30% spread), High (+/- 80% spread across machines)            |
|   - Mechanism: Provides assignment flexibility to allocate jobs to low-power units               |
|                                                                                                  |
+--------------------------------------------------------------------------------------------------+
```

1. **Factor 1: Demand-Charge Intensity ($\rho$):**
   - Controllable parameter: $\rho \in \{0, \rho_{\text{low}}, \rho_{\text{med}}, \rho_{\text{high}}\}$ ($\text{₹}/\text{kW}$).
   - Expected Mechanism: As $\rho$ increases, Strategy C penalizes peak spikes more heavily, widening the cost gap between Strategy B (which ignores $\rho$) and Strategy C.
2. **Factor 2: Time-of-Use Price Differential ($\gamma$):**
   - Controllable parameter: Tariff ratio $\gamma = C_{\text{peak}} / C_{\text{off-peak}} \in \{1.0, 1.35, 1.75, 2.2\}$.
   - Expected Mechanism: Higher $\gamma$ creates intense economic pressure in Strategy B to compress production into off-peak windows, paradoxically exacerbating the secondary peak and increasing Strategy B's total bill under high $\rho$.
3. **Factor 3: Workload Intensity ($W$):**
   - Controllable parameter: $W = \frac{\sum_{j} \min_m p_{jm}}{M \cdot D} \in \{0.40, 0.70, 0.90\}$.
   - Expected Mechanism: Under high workload intensity ($W \approx 0.90$), scheduling slack is minimal; machines must run concurrently to meet deadline $D$, constraining Strategy C's ability to shave peaks. The benefit of peak awareness is expected to peak at intermediate workload intensities ($W \approx 0.60–0.75$).
4. **Factor 4: Machine-Power Heterogeneity ($\sigma_P$):**
   - Controllable parameter: Coefficient of variation of machine power ratings $CV_P = \sigma_P / \bar{P} \in \{0.0, 0.35, 0.75\}$.
   - Expected Mechanism: Higher power heterogeneity provides machine-selection flexibility, enabling Strategy C to achieve peak shaving via intelligent machine assignment rather than solely through temporal delay.

---

### 9.2. Quantitative Output Metrics

For each experimental scenario and strategy $s \in \{A, B, C\}$, the model outputs:

1. **Makespan ($C_{\max}^{(s)}$):** Total schedule completion duration ($\text{h}$).
2. **Energy Consumption ($E_{\text{total}}^{(s)}$):** Total electrical energy consumed ($\text{kWh}$):
   $$E_{\text{total}} = \sum_{t=1}^T P(t) \cdot \Delta t$$
3. **Energy Charge ($EC^{(s)}$):** Total expenditure on energy consumption ($\text{₹}$).
4. **Peak Demand ($P_{\max}^{(s)}$):** Maximum interval-averaged active power demand ($\text{kW}$).
5. **Demand Charge ($DC^{(s)}$):** Total modeled demand charge ($\text{₹}$):
   $$DC = \rho \cdot P_{\max}$$
6. **Total Modeled Electricity Bill ($TEC^{(s)}$):** Combined energy and demand cost ($\text{₹}$):
   $$TEC = EC + DC$$
7. **Economic Benefit of Peak Awareness ($\Delta TEC_{\%}$):**
   $$\Delta TEC_{\%} = \frac{TEC^{(B)} - TEC^{(C)}}{TEC^{(B)}} \times 100\%$$
   *(Positive values indicate economic cost reduction achieved by peak-aware scheduling over energy-cost-only scheduling).*
8. **Peak Demand Reduction ($\Delta P_{\%}$):**
   $$\Delta P_{\%} = \frac{P_{\max}^{(B)} - P_{\max}^{(C)}}{P_{\max}^{(B)}} \times 100\%$$
9. **Makespan Penalty ($\Delta C_{\max,\%}$):**
   $$\Delta C_{\max,\%} = \frac{C_{\max}^{(C)} - C_{\max}^{(B)}}{C_{\max}^{(B)}} \times 100\%$$
10. **Solver Computational Metrics:** Solve wall-clock time ($\text{seconds}$), branch-and-bound iterations, and proven optimality gap ($\%$) on Raspberry Pi 5.

---

## 10. Architectural Extension: Multi-State Energy Model (Future Work / V2)

To preserve scientific continuity with Mouzon et al. (2007) and Aghelinejad et al. (2019), the core V1 model can be seamlessly augmented to include dynamic machine state switching:

### Extended State Set
For each machine $m$: State $k \in \{\text{Processing } (ON), \text{Idle } (IDLE), \text{Turn-ON } (SU), \text{Turn-OFF } (SD), \text{OFF}\}$.

### Extended Parameters
- $P_{m}^{\text{idle}}$: Electrical power draw while idling between jobs ($\text{kW}$).
- $E_{m}^{\text{setup}}$: Total electrical energy required to shut down and restart machine $m$ ($\text{kWh}$).
- $S_m$: Breakeven shutdown threshold duration ($S_m = E_{m}^{\text{setup}} / P_{m}^{\text{idle}}$) ($\text{h}$).
- $t_{m}^{\text{delay}}$: Minimum duration required for shutdown/startup sequence ($\text{h}$).

### Extended Power Function
$$P_{\text{ext}}(t) = \sum_{m=1}^M \left( \sum_{j} P_{jm} y_{jmt} + P_m^{\text{idle}} \cdot y_{mt}^{\text{idle}} + P_m^{\text{setup}} \cdot y_{mt}^{\text{setup}} \right) + P_{\text{base}}$$

This extension will be benchmarked after baseline V1 empirical sensitivity testing is completed.

---

*End of Mathematical Model Formulation V1.0.*
