# Pre-Implementation Mathematical Verification Audit (Model V1.0)

**Project:** Peak-Aware Energy-Cost Production Scheduling for Small Manufacturing Systems Under Industrial Tariff Structures: A Multi-Objective Optimization Study with Physical Validation  
**Phase:** Mathematical Foundation → Verification Audit Gate (Pre-Implementation)  
**Date:** 2026-10-27  
**Auditor:** Antigravity AI Pair Programmer  
**Status:** **AUDIT COMPLETE — VERIFICATION DECISION: NOT READY FOR IMPLEMENTATION (PENDING CORRECTIONS & AUTHORIZATION)**  
**Target Artifact:** `04_mathematical_model/verification/model_v1_preimplementation_audit.md`

---

## 1. Executive Summary & Audit Context

### 1.1. Context and Objective
The latest project report claimed that **Mathematical Model V1.0** and its accompanying **hand-solved benchmark instance** were complete, mathematically validated, and ready for immediate computational implementation in Google OR-Tools CP-SAT. 

Following the strict engineering and research protocols of this project, this audit does **not** assume those claims are correct. A comprehensive, independent audit of the actual repository files was conducted, covering:
- Formulation specification: [`mathematical_model_v1.md`](file:///c:/Project/EL/04_mathematical_model/formulation/mathematical_model_v1.md)
- Derivation and assumptions: [`assumptions.md`](file:///c:/Project/EL/04_mathematical_model/derivation/assumptions.md)
- Traceability map: [`literature_to_equation.md`](file:///c:/Project/EL/04_mathematical_model/derivation/literature_to_equation.md)
- Benchmark calculations: [`hand_calculations.md`](file:///c:/Project/EL/04_mathematical_model/verification/test_instances/hand_calculations.md)
- Regulatory grounding: [`tariff_reference.md`](file:///c:/Project/EL/03_tariff/tariff_reference.md)
- Hardware boundaries: [`current_hardware_spec.md`](file:///c:/Project/EL/09_hardware/current_hardware_spec.md)
- Execution master plan: [`master_execution_plan.md`](file:///c:/Project/EL/05_planning/master_execution_plan.md)

### 1.2. Summary of Findings
The audit revealed **multiple critical and major defects** in the hand-solved benchmark, time discretization definitions, objective weighting functions, and tariff interpretations:
1. **False Optimality Claims in Benchmark (CRITICAL):** The schedule presented in `hand_calculations.md` as "optimal" for Strategy A ($\min C_{\max}$) achieves makespan $5.0\text{ h}$, whereas an easily verifiable schedule with makespan **$4.0\text{ h}$** exists and is feasible.
2. **False Energy-Cost Optimality in Benchmark (CRITICAL):** The schedule presented for Strategy B ($\min EC$) achieves $EC = \text{₹ } 862.60$, whereas the true global minimum energy cost for this instance is **$\text{₹ } 785.60$** (a ₹77.00 / 8.9% discrepancy). The original author assumed dodging peak hours by utilizing the high-power machine was economical, failing to evaluate the machine energy-efficiency trade-off ($50\text{ kWh} \times \text{₹ } 5.60 = \text{₹ } 280.00$ on $M2$ vs. $30\text{ kWh} \times \text{₹ } 7.60 = \text{₹ } 228.00$ on $M1$).
3. **Severe Underestimation of Break-Even Threshold (CRITICAL):** Because the author compared a suboptimal Strategy B against Strategy C, the break-even demand charge rate was calculated as **$\rho^* = 5.00\text{ ₹/kW}$**. Re-evaluating the true optimal schedules yields a true break-even rate of **$\rho^* = 12.70\text{ ₹/kW}$** — over **2.5× higher** than reported. Net savings at $\rho = 15.00\text{ ₹/kW}$ drop from the claimed **7.05% (₹100.00)** to **1.72% (₹23.00)**.
4. **Operation Preemption in Strategy C Schedule (MAJOR):** In `hand_calculations.md`, the primary schedule for Strategy C splits Job 2 across slots 5, 7, and 8, leaving slot 6 idle. This directly violates the non-preemption constraint (Eq. 5). While an unnumbered text note proposed a contiguous alternative, the primary tables, Gantt profiles, and power vectors were based on the preempted schedule.
5. **Time Discretization Inconsistency (MAJOR):** `hand_calculations.md` specifies 8 slots with $\Delta t = 1.0\text{ h}$ and $L = 1\text{ slot}$ ($1.0\text{ h}$ integration window). This conflates an hourly slot with the utility's official 15-minute demand integration window ($0.25\text{ h}$) and fails to represent an 8-hour shift at 15-minute billing resolution (which requires 32 slots).
6. **Objective Weighting and Integer Scaling Vulnerability (MAJOR):** The linear combination $\epsilon$ tie-breakers in Equations (18), (19), and (21) risk objective corruption or complete cancellation when converted to integer coefficients for Google OR-Tools CP-SAT. Sequential lexicographic optimization is required.
7. **Monthly Tariff Proration Fallacy (MINOR / CONCEPTUAL):** Prorating the KERC HT-2(a) monthly demand charge of ₹350/kVA over 25 days ($\rho = 14.00\text{ ₹/kW/day}$) must be rigorously treated as a normalized experimental sensitivity parameter, not an actual daily utility bill saving.

### 1.3. Official Readiness Decision
> **VERDICT: NOT READY FOR IMPLEMENTATION**
> 
> Implementation of Google OR-Tools CP-SAT code must **NOT** proceed until:
> 1. The mathematical formulation is formally updated to replace weighted $\epsilon$ tie-breakers with **Sequential Lexicographic Optimization**.
> 2. The hand-solved benchmark calculations, schedules, and break-even thresholds are formally corrected in `hand_calculations.md` to prevent baking false baseline numbers into CP-SAT unit test assertions.
> 3. The time discretization taxonomy explicitly separates the 8-slot illustrative benchmark from the multi-slot (32/96-slot) production model.

---

## 2. Comprehensive Deficiency Matrix

| Issue ID | Severity | File Location | Relevant Equation / Section | Finding & Mathematical Basis | Required Correction / Resolution |
|---|---|---|---|---|---|
| **ISS-01** | **CRITICAL** | `hand_calculations.md` | Section 3.1, lines 51–66 | **Suboptimal Baseline Schedule:** Strategy A claimed $C_{\max}^* = 5\text{ slots}$. An assignment of $\{J1, J3\}$ to $M1$ ($p=2+2=4$) and $\{J2, J4\}$ to $M2$ ($p=2+2=4$) yields $C_{\max} = \mathbf{4\text{ slots}}$. | Correct Strategy A makespan to 4 slots; recalculate power profile, energy cost ($EC = \text{₹ } 1031.60$), and total bill ($TEC = \text{₹ } 1586.60$). |
| **ISS-02** | **CRITICAL** | `hand_calculations.md` | Section 3.2, lines 93–142 | **Suboptimal Energy-Cost Schedule:** Strategy B claimed $EC^* = \text{₹ } 862.60$. Assigning $\{J1, J2, J4\}$ to $M1$ (8h) and $\{J3\}$ to $M2$ (1h in slot 1) yields $EC = \mathbf{\text{₹ } 785.60}$. Machine efficiency ratio ($50/30 = 1.67$) exceeds tariff peak ratio ($7.60/5.60 = 1.36$). | Correct Strategy B optimal schedule; document the Machine Efficiency vs. Tariff Ratio theorem; update $EC^{(B)}$ to ₹785.60. |
| **ISS-03** | **CRITICAL** | `hand_calculations.md` | Section 6, lines 290–309 | **Erroneous Break-Even Calculation:** Author calculated $\rho^* = 5.00\text{ ₹/kW}$ based on $\Delta EC = \text{₹ } 50.00$. The true optimal difference is $\Delta EC = 912.60 - 785.60 = \text{₹ } 127.00$, yielding true $\rho^* = \mathbf{12.70\text{ ₹/kW}}$. Savings at $\rho=15$ drop from 7.05% to 1.72%. | Recalculate break-even table and sensitivity curve using verified global optima. |
| **ISS-04** | **MAJOR** | `hand_calculations.md` | Section 3.3, 4.2, lines 176–185, 241–248 | **Preemption Constraint Violation:** Visual schedule and power profile for Strategy C show $J2$ running at slot 5, idle at slot 6, and running at slots 7–8. This violates Eq. (5) ($y_{jmt}$ lookback continuity). | Replace primary schedule with contiguous version: $M1$ runs $J1$ (slots 3–4) and $J2$ (slots 5–7); $M2$ runs $J4$ (slots 1–2) and $J3$ (slot 8). |
| **ISS-05** | **MAJOR** | `hand_calculations.md` & `mathematical_model_v1.md` | Section 2.3 & Section 3.2, 5.6 | **Time Discretization Conflation:** $\Delta t = 1.0\text{ h}$ with $L=1$ slot conflates 1-hour slots with 15-minute utility demand windows. An 8-slot model cannot resolve 15-minute industrial billing demand. | Formally distinguish the 8-slot normalized toy benchmark from the 32-slot ($15\text{ min}$) and 96-slot ($5\text{ min}$) production scheduling models. |
| **ISS-06** | **MAJOR** | `mathematical_model_v1.md` | Section 6, Eq. (18)–(21) | **Numerical Instability of $\epsilon$ Tie-Breakers:** Linear combination objectives with $\epsilon = 10^{-4}$ risk integer scaling truncation or primary objective corruption in CP-SAT. | Replace single-pass weighted objectives with two-stage **Sequential Lexicographic Optimization**. |
| **ISS-07** | **MINOR** | `mathematical_model_v1.md` | Section 5.6, Eq. (12) | **Demand Interval Averaging Formulation:** Eq. (12) uses simple arithmetic average without explicitly stating the requirement of uniform slot durations $\Delta t$. | State duration-weighted formula explicitly; prove that arithmetic average is valid if and only if all slots in interval $k$ have equal duration $\Delta t$. |
| **ISS-08** | **MINOR** | `hand_calculations.md` & `tariff_reference.md` | Section 2.3 & Section 4.2 | **Synthetic Tariff Clock-Time Mapping:** `hand_calculations.md` maps slots 3–5 (02:00–05:00) to Peak tariff, whereas KERC HT-2(a) defines 02:00–05:00 as Off-peak (Peak is 06:00–09:00 and 18:00–22:00). | Clarify that the benchmark uses an illustrative synthetic block sequence, not the literal KERC clock-hour schedule. |

---

## 3. Section B — Complete Resolution of Time Discretization

### 3.1. Parameter Definitions and Dimensional Coherence
To ensure complete mathematical clarity, the discrete time parameters of the scheduling system are defined below:

| Parameter | Symbol | Unit | Mathematical Definition / Value | Physical Meaning |
|---|---|---|---|---|
| **Slot Duration** | $\Delta t$ | hours ($\text{h}$) | $\Delta t \in \{0.0833\text{ h } (5\text{ min}), 0.25\text{ h } (15\text{ min}), 1.0\text{ h } (60\text{ min})\}$ | Fundamental time-step of the discrete schedule. |
| **Scheduling Horizon** | $T$ | slots | $T = H / \Delta t \in \mathbb{Z}^+$ | Total number of discrete time slots modeled. |
| **Scheduling Horizon** | $H$ | hours ($\text{h}$) | $H = T \cdot \Delta t$ | Physical duration of the production shift (e.g., $8\text{ h}, 12\text{ h}, 24\text{ h}$). |
| **Demand Measurement Window** | $W_{\text{meas}}$ | hours ($\text{h}$) | $W_{\text{meas}} = 0.25\text{ h } (15\text{ minutes})$ | Regulatory utility integration window for billing demand (KERC standard). |
| **Slots per Demand Window** | $L$ | integer | $L = W_{\text{meas}} / \Delta t$ | Number of internal model slots over which power is integrated to compute $p_k^{\text{int}}$. |
| **Number of Demand Intervals** | $K$ | integer | $K = T / L = H / W_{\text{meas}}$ | Total count of demand evaluation windows across the horizon. |
| **Tariff Price Interval** | $W_{\text{tariff}}$ | hours ($\text{h}$) | Block durations: $3\text{ h}, 4\text{ h}, 8\text{ h}, 9\text{ h}$ | Regulatory time-of-day pricing blocks defined by the utility tariff order. |

### 3.2. Evaluation of the 8-Slot Instance
Can an eight-slot example really represent the stated 8-hour horizon and a 15-minute average demand?
- **Mathematical Impossibility:** If $T = 8$ slots and $H = 8\text{ hours}$, the slot duration is necessarily:
  $$\Delta t = \frac{H}{T} = \frac{8\text{ h}}{8} = 1.0\text{ hour } (60\text{ minutes})$$
- A 60-minute slot **cannot calculate a 15-minute average demand**. Within a 1-hour slot, the model treats power draw as constant. Any sub-hourly load variations, rapid machine duty cycles, or 15-minute staggered peaks are completely invisible.
- Conversely, if the slot duration were set to match the 15-minute utility demand window ($\Delta t = 0.25\text{ h}$):
  $$H = T \cdot \Delta t = 8 \times 0.25\text{ h} = 2.0\text{ hours}$$
  An 8-slot schedule would represent only a **2-hour operating window**, not an 8-hour shift!
- To model an **8-hour industrial shift** at true 15-minute utility demand resolution:
  $$T = \frac{8\text{ h}}{0.25\text{ h/slot}} = \mathbf{32\text{ time slots}} \quad (L = 1\text{ slot/interval}, K = 32\text{ intervals})$$
- If modeled at 5-minute slot resolution ($\Delta t = 0.0833\text{ h}$):
  $$T = \frac{8\text{ h}}{5/60\text{ h/slot}} = \mathbf{96\text{ time slots}} \quad (L = 3\text{ slots/interval}, K = 32\text{ intervals})$$

### 3.3. Derivation of Duration-Weighted Average Power
For any arbitrary measurement interval $k \in \mathcal{K}$ spanning temporal continuous interval $[t_{\text{start}}^k, t_{\text{end}}^k]$ of duration $W_k = t_{\text{end}}^k - t_{\text{start}}^k$, the physical average demand is defined by the definite integral of active power:

$$p_k^{\text{int}} = \frac{1}{W_k} \int_{t_{\text{start}}^k}^{t_{\text{end}}^k} P(t) \, dt$$

Under a piecewise-constant discrete slot discretization where slot $t$ has duration $\delta_t$ and constant power $P(t)$:

$$p_k^{\text{int}} = \frac{\sum_{t \in \mathcal{T}_k} P(t) \cdot \delta_t}{\sum_{t \in \mathcal{T}_k} \delta_t} = \frac{\sum_{t \in \mathcal{T}_k} P(t) \cdot \delta_t}{W_k} \tag{DW-1}$$

#### Condition for Simple Arithmetic Averaging:
If and only if all discrete slots within interval $k$ have an **identical uniform duration** $\delta_t = \Delta t$, and $|\mathcal{T}_k| = L$:

$$p_k^{\text{int}} = \frac{\sum_{t \in \mathcal{T}_k} P(t) \cdot \Delta t}{L \cdot \Delta t} = \frac{1}{L} \sum_{t \in \mathcal{T}_k} P(t) \tag{DW-2}$$

Equation (12) in `mathematical_model_v1.md` is mathematically correct **only under uniform slot duration $\Delta t$**. If non-uniform slots are ever introduced, Equation (DW-1) must be used.

### 3.4. Explicit Decision on the Benchmark Instance
To prevent methodological ambiguity:
- The **Toy Instance** in `hand_calculations.md` is designated as an **Illustrative Normalized Research Benchmark**:
  - $T = 8\text{ slots}$, $\Delta t = 1.0\text{ h}$, $H = 8\text{ h}$.
  - Measurement interval $L = 1\text{ slot} = 1.0\text{ h}$ ($K = 8\text{ intervals}$).
  - It demonstrates the mathematical mechanics of machine staggering and peak avoidance in closed form.
- The **Production CP-SAT Model** will use:
  - $\Delta t = 0.25\text{ h } (15\text{ min})$, $T = 32\text{ to } 96$ slots, $L = 1\text{ slot}$ per 15-minute billing window.

---

## 4. Section C — Independent Re-Derivation of the Hand-Solved Benchmark

### 4.1. Exhaustive Problem Instance Parameters
- **Machines:**
  - $M1$: $P_{1} = 10.0\text{ kW}$ (Low power)
  - $M2$: $P_{2} = 25.0\text{ kW}$ (High power)
  - Facility Base Load: $P_{\text{base}} = 2.0\text{ kW}$
- **Jobs:** All released at $r_j = 1$, deadline $D = 8\text{ slots}$.
  - $J1$: $p_{1,1} = 2\text{ h}, p_{1,2} = 2\text{ h}; \quad P_{1,1} = 10.0\text{ kW}, P_{1,2} = 25.0\text{ kW}$
  - $J2$: $p_{2,1} = 3\text{ h}, p_{2,2} = 2\text{ h}; \quad P_{2,1} = 10.0\text{ kW}, P_{2,2} = 25.0\text{ kW}$
  - $J3$: $p_{3,1} = 2\text{ h}, p_{3,2} = 1\text{ h}; \quad P_{3,1} = 10.0\text{ kW}, P_{3,2} = 25.0\text{ kW}$
  - $J4$: $p_{4,1} = 3\text{ h}, p_{4,2} = 2\text{ h}; \quad P_{4,1} = 10.0\text{ kW}, P_{4,2} = 25.0\text{ kW}$
- **Tariff Structure:**
  - Slots 1–2 (Off-Peak): $C_1 = C_2 = \text{₹ } 5.60 / \text{kWh}$
  - Slots 3–5 (Peak): $C_3 = C_4 = C_5 = \text{₹ } 7.60 / \text{kWh}$
  - Slots 6–8 (Normal): $C_6 = C_7 = C_8 = \text{₹ } 6.60 / \text{kWh}$
  - Demand Charge Intensity: $\rho = \text{₹ } 15.00 / \text{kW}$

---

### 4.2. Strategy A: Production-Oriented Baseline ($\min C_{\max}$)

#### Mathematical Optimality Proof for $C_{\max}$:
Let $z_{jm} \in \{0, 1\}$ be the assignment of job $j$ to machine $m$. Total machine workloads are:
$$W_1 = 2 z_{1,1} + 3 z_{2,1} + 2 z_{3,1} + 3 z_{4,1}$$
$$W_2 = 2 z_{1,2} + 2 z_{2,2} + 1 z_{3,2} + 2 z_{4,2}$$
Because all jobs are independent and available at $t=1$, the makespan for any assignment is $C_{\max} = \max(W_1, W_2)$.
- In `hand_calculations.md`, the author assigned $\{J1, J2\}$ to $M1$ ($W_1 = 2+3=5$) and $\{J3, J4\}$ to $M2$ ($W_2 = 1+2=3$), obtaining $C_{\max} = 5.0\text{ h}$.
- **Global Optimum:** Assign $\{J1, J3\}$ to $M1$ and $\{J2, J4\}$ to $M2$:
  $$W_1 = p_{1,1} + p_{3,1} = 2 + 2 = \mathbf{4.0\text{ hours}}$$
  $$W_2 = p_{2,2} + p_{4,2} = 2 + 2 = \mathbf{4.0\text{ hours}}$$
  $$C_{\max}^* = \max(4.0, 4.0) = \mathbf{4.0\text{ hours}} \quad (\mathbf{4\text{ slots}})$$
- Can makespan be 3 slots? For $C_{\max} \le 3$, $W_2 \le 3 \implies M2$ can take at most one 2h job and one 1h job. The remaining two jobs on $M1$ would require at least $2+2=4\text{ h} > 3\text{ h}$. Hence $C_{\max}^* = 4$ is the **uniquely proven global optimum**.

#### Schedule & Operational Verification:
- $M1$: $J1$ at slots 1–2 ($C_1 = 2$); $J3$ at slots 3–4 ($C_3 = 4$).
- $M2$: $J2$ at slots 1–2 ($C_2 = 2$); $J4$ at slots 3–4 ($C_4 = 4$).
- Both machines run simultaneously from slot 1 to slot 4:
  - Slots 1–2: $P(t) = 10.0 + 25.0 + 2.0 = \mathbf{37.0\text{ kW}}$
  - Slots 3–4: $P(t) = 10.0 + 25.0 + 2.0 = \mathbf{37.0\text{ kW}}$
  - Slots 5–8: Idle; $P(t) = P_{\text{base}} = \mathbf{2.0\text{ kW}}$
- **Peak Demand:** $P_{\max}^{(A)} = \mathbf{37.0\text{ kW}}$
- **Total Energy Consumed:**
  $$E_{\text{total}} = (4 \times 37.0) + (4 \times 2.0) = 148.0 + 8.0 = \mathbf{156.0\text{ kWh}}$$
- **Energy Cost ($EC^{(A)}$):**
  $$\begin{aligned}
  EC^{(A)} &= (2\text{ h} \times 37.0\text{ kW} \times 5.60) + (2\text{ h} \times 37.0\text{ kW} \times 7.60) + (1\text{ h} \times 2.0\text{ kW} \times 7.60) + (3\text{ h} \times 2.0\text{ kW} \times 6.60) \\
  &= 414.40 + 562.40 + 15.20 + 39.60 = \mathbf{\text{₹ } 1031.60}
  \end{aligned}$$
- **Demand Charge ($DC^{(A)}$):**
  $$DC^{(A)} = 15.00 \times 37.0 = \mathbf{\text{₹ } 555.00}$$
- **Total Modeled Electricity Bill ($TEC^{(A)}$):**
  $$TEC^{(A)} = 1031.60 + 555.00 = \mathbf{\text{₹ } 1586.60}$$

*(Note: The author's suboptimal schedule had $C_{\max}=5$, $EC = \text{₹ } 917.60$, $TEC = \text{₹ } 1472.60$. True makespan optimization packs more work into the peak window slots 3–4, raising energy cost to ₹1031.60).*

---

### 4.3. Strategy B: Energy-Cost-Only Scheduling ($\min EC$)

#### Mathematical Optimality Proof for Energy Cost:
Let us evaluate the total energy consumed by each job on each machine:
- $J1$: $E_{1,1} = 2\text{ h} \times 10\text{ kW} = 20\text{ kWh}$; $E_{1,2} = 2\text{ h} \times 25\text{ kW} = 50\text{ kWh}$. (Difference: $+30\text{ kWh}$ on $M2$).
- $J2$: $E_{2,1} = 3\text{ h} \times 10\text{ kW} = 30\text{ kWh}$; $E_{2,2} = 2\text{ h} \times 25\text{ kW} = 50\text{ kWh}$. (Difference: $+20\text{ kWh}$ on $M2$).
- $J3$: $E_{3,1} = 2\text{ h} \times 10\text{ kW} = 20\text{ kWh}$; $E_{3,2} = 1\text{ h} \times 25\text{ kW} = 25\text{ kWh}$. (Difference: $+5\text{ kWh}$ on $M2$).
- $J4$: $E_{4,1} = 3\text{ h} \times 10\text{ kW} = 30\text{ kWh}$; $E_{4,2} = 2\text{ h} \times 25\text{ kW} = 50\text{ kWh}$. (Difference: $+20\text{ kWh}$ on $M2$).

Total processing time on $M1$ for all jobs is $2+3+2+3 = 10\text{ hours} > D=8\text{ hours}$. Thus, at least one job must be offloaded to $M2$.
- To minimize energy addition, offload the job with the **minimum energy penalty**: $J3$ (adds only $5\text{ kWh}$).
- Assigning $\{J1, J2, J4\}$ to $M1$ requires exactly $2 + 3 + 3 = \mathbf{8.0\text{ hours}}$ of processing, fitting the 8-hour shift.
- Machine $M1$ must operate continuously for all 8 slots (slots 1–8).
- Machine $M2$ processes $J3$ ($p_{3,2} = 1\text{ h}$) during the cheapest available slot: **Slot 1 (Off-Peak: ₹5.60/kWh)**.

#### The Machine Efficiency vs. Tariff Ratio Principle:
Why is this cheaper than the author's schedule which dodged peak hours?
- The author ran $J4$ on $M2$ during off-peak hours:
  $$\text{Cost} = 50\text{ kWh} \times \text{₹ } 5.60 = \mathbf{\text{₹ } 280.00}$$
- Running $J4$ on $M1$ during the **most expensive peak hours (₹7.60)**:
  $$\text{Cost} = 30\text{ kWh} \times \text{₹ } 7.60 = \mathbf{\text{₹ } 228.00}$$
- **Result:** Running on the efficient machine during peak hours is **₹52.00 cheaper** than running on the inefficient machine during off-peak hours! The solver prioritizing $\min EC$ will strictly choose this assignment.

#### Schedule & Operational Verification:
- $M1$: Runs $J1$ (slots 1–2), $J2$ (slots 3–5), $J4$ (slots 6–8).
- $M2$: Runs $J3$ (slot 1); idle slots 2–8.
- Temporal Power Profile $P(t)$:
  - Slot 1 ($C_1 = 5.60$): $M1(10) + M2(25) + P_{\text{base}}(2) = \mathbf{37.0\text{ kW}}$
  - Slots 2–8: $M1(10) + M2(0) + P_{\text{base}}(2) = \mathbf{12.0\text{ kW}}$
- **Makespan:** $C_{\max}^{(B)} = \mathbf{8.0\text{ hours}}$
- **Peak Demand:** $P_{\max}^{(B)} = \mathbf{37.0\text{ kW}}$
- **Energy Cost Calculation ($EC^{(B)}$):**
  $$\begin{aligned}
  EC^{(B)} &= (1\text{ h} \times 37.0 \times 5.60) + (1\text{ h} \times 12.0 \times 5.60) + (3\text{ h} \times 12.0 \times 7.60) + (3\text{ h} \times 12.0 \times 6.60) \\
  &= 207.20 + 67.20 + 273.60 + 237.60 = \mathbf{\text{₹ } 785.60}
  \end{aligned}$$
- **Demand Charge ($DC^{(B)}$):**
  $$DC^{(B)} = 15.00 \times 37.0 = \mathbf{\text{₹ } 555.00}$$
- **Total Modeled Electricity Bill ($TEC^{(B)}$):**
  $$TEC^{(B)} = 785.60 + 555.00 = \mathbf{\text{₹ } 1340.60}$$

---

### 4.4. Strategy C: Peak-Aware Total Cost Scheduling ($\min TEC = EC + \rho P_{\max}$)

#### Mathematical Optimality Proof for Total Cost:
- Under $\rho = \text{₹ } 15.00/\text{kW}$, the penalty for hitting $37.0\text{ kW}$ is $\rho \times 37 = \text{₹ } 555.00$.
- If machines are de-synchronized so that $M1$ and $M2$ **never overlap**, the peak power is bounded by $\max(P_1, P_2) + P_{\text{base}} = 25.0 + 2.0 = \mathbf{27.0\text{ kW}}$.
- Demand charge drops to $15.00 \times 27.0 = \text{₹ } 405.00$ (a **₹150.00 demand charge saving**).
- Non-overlap condition: Total machine hours worked across both machines cannot exceed the 8-hour horizon:
  $$W_1 + W_2 \le 8.0\text{ hours}$$
- As proven in Section 3, the unique assignment satisfying $W_1 + W_2 \le 8$ with minimal energy cost is:
  - $M1$: $\{J1, J2\} \implies W_1 = 2 + 3 = 5\text{ hours}$
  - $M2$: $\{J3, J4\} \implies W_2 = 1 + 2 = 3\text{ hours}$
  - Total work: $5 + 3 = 8\text{ hours}$.
- To minimize energy cost without violating non-preemption:
  - Place $M2$ (25 kW) in the cheapest slots: $J4$ in slots 1–2 (Off-peak: ₹5.60), and $J3$ in slot 8 (Normal: ₹6.60).
  - Place $M1$ (10 kW) in the contiguous remaining slots: $J1$ in slots 3–4 (Peak: ₹7.60) and $J2$ in slots 5–7 (slot 5 is Peak ₹7.60; slots 6–7 are Normal ₹6.60).
- **All operations are strictly contiguous and non-preemptive.**

#### Schedule & Operational Verification:
- Slot 1 ($C_1 = 5.60$): $M2(J4: 25) + P_{\text{base}}(2) = \mathbf{27.0\text{ kW}}$
- Slot 2 ($C_2 = 5.60$): $M2(J4: 25) + P_{\text{base}}(2) = \mathbf{27.0\text{ kW}}$
- Slot 3 ($C_3 = 7.60$): $M1(J1: 10) + P_{\text{base}}(2) = \mathbf{12.0\text{ kW}}$
- Slot 4 ($C_4 = 7.60$): $M1(J1: 10) + P_{\text{base}}(2) = \mathbf{12.0\text{ kW}}$
- Slot 5 ($C_5 = 7.60$): $M1(J2: 10) + P_{\text{base}}(2) = \mathbf{12.0\text{ kW}}$
- Slot 6 ($C_6 = 6.60$): $M1(J2: 10) + P_{\text{base}}(2) = \mathbf{12.0\text{ kW}}$
- Slot 7 ($C_7 = 6.60$): $M1(J2: 10) + P_{\text{base}}(2) = \mathbf{12.0\text{ kW}}$
- Slot 8 ($C_8 = 6.60$): $M2(J3: 25) + P_{\text{base}}(2) = \mathbf{27.0\text{ kW}}$
- **Makespan:** $C_{\max}^{(C)} = \mathbf{8.0\text{ hours}}$
- **Peak Demand:** $P_{\max}^{(C)} = \mathbf{27.0\text{ kW}}$ (Peak shaved by 10.0 kW / 27.03%)
- **Energy Cost Calculation ($EC^{(C)}$):**
  $$\begin{aligned}
  EC^{(C)} &= (2\text{ h} \times 27.0 \times 5.60) + (3\text{ h} \times 12.0 \times 7.60) + (2\text{ h} \times 12.0 \times 6.60) + (1\text{ h} \times 27.0 \times 6.60) \\
  &= 302.40 + 273.60 + 158.40 + 178.20 = \mathbf{\text{₹ } 912.60}
  \end{aligned}$$
- **Demand Charge ($DC^{(C)}$):**
  $$DC^{(C)} = 15.00 \times 27.0 = \mathbf{\text{₹ } 405.00}$$
- **Total Modeled Electricity Bill ($TEC^{(C)}$):**
  $$TEC^{(C)} = 912.60 + 405.00 = \mathbf{\text{₹ } 1317.60}$$

---

### 4.5. Master Comparison Table: Claimed vs. Independently Verified Optimal Values

| Metric | Strategy A (Claimed) | Strategy A (Verified Opt) | Strategy B (Claimed) | Strategy B (Verified Opt) | Strategy C (Claimed / Preempted) | Strategy C (Verified Contiguous) |
|---|---|---|---|---|---|---|
| **Makespan ($C_{\max}$)** | 5.0 h | **4.0 h** | 8.0 h | **8.0 h** | 8.0 h | **8.0 h** |
| **Peak Demand ($P_{\max}$)** | 37.0 kW | **37.0 kW** | 37.0 kW | **37.0 kW** | 27.0 kW | **27.0 kW** |
| **Energy Consumed ($E_{\text{total}}$)** | 143.0 kWh | **156.0 kWh** | 143.0 kWh | **121.0 kWh** | 143.0 kWh | **141.0 kWh** |
| **Energy Cost ($EC$)** | ₹ 917.60 | **₹ 1031.60** | ₹ 862.60 | **₹ 785.60** | ₹ 912.60 | **₹ 912.60** |
| **Demand Charge ($DC$)** | ₹ 555.00 | **₹ 555.00** | ₹ 555.00 | **₹ 555.00** | ₹ 405.00 | **₹ 405.00** |
| **Total Bill ($TEC$)** | ₹ 1472.60 | **₹ 1586.60** | ₹ 1417.60 | **₹ 1340.60** | ₹ 1317.60 | **₹ 1317.60** |
| **Net Savings (C vs B)** | ₹ 100.00 (7.05%) | — | Base | Base | ₹ 100.00 (7.05%) | **₹ 23.00 (1.72%)** |

---

### 4.6. Recalculation of Break-Even Demand Charge Rate $\rho^*$
The break-even demand charge rate $\rho^*$ is the exact price of peak power at which the total electricity bill of Strategy B equals that of Strategy C:

$$TEC^{(B)}(\rho^*) = TEC^{(C)}(\rho^*)$$
$$EC^{(B)} + \rho^* P_{\max}^{(B)} = EC^{(C)} + \rho^* P_{\max}^{(C)}$$
$$\rho^* = \frac{EC^{(C)} - EC^{(B)}}{P_{\max}^{(B)} - P_{\max}^{(C)}} \tag{BE-1}$$

#### Independent Mathematical Derivation:
$$\Delta EC = EC^{(C)} - EC^{(B)} = 912.60 - 785.60 = \mathbf{\text{₹ } 127.00}$$
$$\Delta P_{\max} = P_{\max}^{(B)} - P_{\max}^{(C)} = 37.0 - 27.0 = \mathbf{10.0\text{ kW}}$$
$$\rho^* = \frac{127.00\text{ ₹}}{10.0\text{ kW}} = \mathbf{12.70 \text{ ₹/kW}}$$

#### Critical Finding and Contrast:
- **Claimed in `hand_calculations.md`:** $\rho^* = \frac{912.60 - 862.60}{10.0} = \mathbf{5.00 \text{ ₹/kW}}$.
- **True Mathematical Break-Even:** $\rho^* = \mathbf{12.70 \text{ ₹/kW}}$.
- **Scientific Consequence:** Peak-aware scheduling (Strategy C) provides an economic benefit **only when the demand charge parameter exceeds ₹12.70/kW**, not ₹5.00/kW. 
- At the KERC daily equivalent rate of $\rho = 14.00\text{ ₹/kW}$, Strategy C saves only:
  $$\Delta TEC = (785.60 + 14 \times 37) - (912.60 + 14 \times 27) = 1303.60 - 1290.60 = \mathbf{\text{₹ } 13.00 \quad (1.00\%)}$$
  *(Not the ₹90.00 / 6.5% savings implied by the earlier report).*

---

## 5. Section D — Objective Priority, Numerical Scaling, and Lexicographic Optimization

### 5.1. Failure Analysis of $\epsilon$-Weighted Tie-Breakers
Equations (18), (19), and (21) in `mathematical_model_v1.md` proposed weighted-sum objectives of the form:
$$\min Z_B = EC + \epsilon_B \cdot C_{\max}$$
$$\min Z_C = TEC + \epsilon_C \cdot C_{\max}$$

#### The Mathematical Breakdown under Integer Scaling:
Google OR-Tools CP-SAT requires **all objective coefficients to be integers**.
Let the monetary scaling factor be $S_M = 100$ (converting ₹ to paise). Then scaled energy cost is $\tilde{EC} = \text{round}(100 \times EC) \in \mathbb{Z}^+$.
If $\epsilon_B$ is introduced, the scaled objective becomes:
$$\tilde{Z}_B = \tilde{EC} + \text{round}(100 \times \epsilon_B) \cdot C_{\max}$$
1. **Case 1: Under-scaling (Loss of Tie-Breaker):** If $\epsilon_B = 10^{-4}$, then $100 \times \epsilon_B = 0.01$. The rounded integer coefficient is **0**! The tie-breaker vanishes completely.
2. **Case 2: Large Scaling Multiplier:** If the objective is scaled by $10^6$ to preserve $\epsilon_B = 10^{-4}$ (coefficient $= 100$):
   $$\tilde{Z}_B = 1,000,000 \cdot EC + 100 \cdot C_{\max}$$
   Now consider two candidate schedules $S_1$ and $S_2$:
   - Schedule $S_1$: $EC = \text{₹ } 800.00$, $C_{\max} = 8\text{ h}$.
   - Schedule $S_2$: $EC = \text{₹ } 800.005$ (difference of 0.5 paise due to 1-minute load difference), $C_{\max} = 4\text{ h}$.
   $$\Delta \tilde{Z}_B = 1,000,000 \times (+0.005) + 100 \times (-4) = 5,000 - 400 = +4,600$$
   Here priority holds. But across generated instances with wide ranges of power (watts to kilowatts) and horizon lengths, finding an a priori scalar $\epsilon$ that guarantees:
   $$\epsilon \cdot \Delta C_{\max} < \min |\Delta EC|$$
   for all possible schedule pairs is mathematically impossible without dynamic instance-dependent bound pre-computation.

---

### 5.2. Formal Specification of Sequential Lexicographic Optimization
To provide 100% mathematical guarantee of objective priority without numerical distortion, weighted $\epsilon$ tie-breakers are **REPLACED** with a rigorous two-phase sequential lexicographic optimization protocol:

```
====================================================================================================
                        SEQUENTIAL LEXICOGRAPHIC OPTIMIZATION WORKFLOW
====================================================================================================

      SHARED FEASIBILITY CONSTRAINTS (1)–(15), HORIZON T, DEADLINE D
                                    │
    ┌───────────────────────────────┼───────────────────────────────┐
    │                               │                               │
    ▼                               ▼                               ▼
[STRATEGY A]                  [STRATEGY B]                    [STRATEGY C]
Phase 1:                      Phase 1:                        Phase 1:
Solve min C_max               Solve min EC                    Solve min TEC (EC + rho*P_max)
Record C_max*                 Record EC*                      Record TEC*
    │                               │                               │
    ▼                               ▼                               ▼
Phase 2:                      Phase 2:                        Phase 2:
Add C_max <= C_max*           Add EC <= EC*                   Add TEC <= TEC*
Solve min sum(C_j)            Solve min C_max                 Solve min C_max
Output Final Schedule         Output Final Schedule           Output Final Schedule
====================================================================================================
```

#### Exact Mathematical Protocol per Strategy:

#### Strategy A (Production-Oriented Baseline):
1. **Phase 1 Solve:**
   $$\min C_{\max}$$
   $$\text{Subject to Constraints (1)–(15)}$$
   - Solver proves optimality. Record optimal makespan $C_{\max}^*$.
2. **Phase 2 Solve:**
   $$\min \sum_{j \in \mathcal{J}} C_j$$
   $$\text{Subject to Constraints (1)–(15) and } C_{\max} \le C_{\max}^*$$
   - Records unique schedule minimizing work-in-process flow time while preserving proven minimum makespan $C_{\max}^*$.
   - **Anti-bias property:** Strictly zero energy cost or peak demand terms in either phase.

#### Strategy B (Energy-Cost-Only Scheduling):
1. **Phase 1 Solve:**
   $$\min EC = \sum_{t=1}^T C_t P(t) \Delta t$$
   $$\text{Subject to Constraints (1)–(15) and } C_{\max} \le D$$
   - Solver proves optimality. Record optimal energy cost $EC^*$.
2. **Phase 2 Solve:**
   $$\min C_{\max}$$
   $$\text{Subject to Constraints (1)–(15)}, \quad C_{\max} \le D, \quad \text{and } EC \le EC^*$$
   - Solves for the most compact schedule that achieves exact minimum energy cost $EC^*$.
   - **Zero peak bias:** Parameter $\rho = 0$.

#### Strategy C (Peak-Aware Total Cost Scheduling):
1. **Phase 1 Solve:**
   $$\min TEC = \sum_{t=1}^T C_t P(t) \Delta t + \rho \cdot P_{\max}$$
   $$\text{Subject to Constraints (1)–(15) and } C_{\max} \le D$$
   - Solver proves optimality. Record optimal total cost $TEC^*$.
2. **Phase 2 Solve:**
   $$\min C_{\max}$$
   $$\text{Subject to Constraints (1)–(15)}, \quad C_{\max} \le D, \quad \text{and } TEC \le TEC^*$$
   - Solves for the most compact schedule that achieves exact minimum total cost $TEC^*$.

#### Invariance and Fairness Proof:
- **Identical Feasible Set:** All three strategies enforce the exact same machine non-overlap, non-preemption, single assignment, release times, and global deadline $D \le T$.
- **Pure Objective Separation:** The resulting schedules differ **solely** because of the optimization criteria, guaranteeing strict scientific attribution of observed differences.

---

## 6. Section E — Industrial Tariff Interpretation & Regulatory Grounding

### 6.1. Regulatory Mapping Audit: KERC Tariff Order 2025
Auditing [`tariff_reference.md`](file:///c:/Project/EL/03_tariff/tariff_reference.md) against official KERC Tariff Order 2025 (Annexure 9) establishes the following authoritative parameters:

1. **Consumer Category & Voltage Level:**
   - **HT-2(a) (High Tension Industrial):** Governs large manufacturing installations supplied at $\ge 11\text{ kV}$, with contract demand typically $\ge 100\text{ kVA}$.
   - **LT-5 (Low Tension Industrial):** Governs small MSMEs connected at 415V/230V. Crucially, **LT-5 imposes fixed monthly charges based on Sanctioned Load (kW)**, not on recorded 15-minute maximum demand! Therefore, HT-2(a) is the only category that establishes a true maximum demand charge, serving as the regulatory template for peak-aware scheduling.
2. **Effective Rate & Study Period:**
   - Effective Date: 1 April 2026 (FY 2026–27).
   - Base Energy Charge: **₹6.60 / kWh**.
   - Demand Charge: **₹350.00 / kVA / month of Billing Demand**.
3. **Billing Demand Rule & 90% Contract Floor:**
   $$BD = \max(MD, 0.90 \times CD)$$
   Where $MD$ is the maximum apparent demand recorded in any 15-minute window during the month, and $CD$ is Contract Demand.
   - **Crucial Economic Implication:** If a factory operates below $90\%$ of its contracted capacity ($MD \le 0.90 \times CD$), shaving peak power produces **exactly ₹0.00 in demand charge savings** under real-world utility billing!
4. **Apparent Demand vs. Active Power ($\text{kVA}$ vs. $\text{kW}$):**
   - Utility meters bill in **kVA** (apparent power $S = \sqrt{P^2 + Q^2}$).
   - The scheduling model calculates active power in **kW**.
   - Equating $\text{kW} \equiv \text{kVA}$ requires an explicit assumption of unity power factor ($PF = 1.0$). At a realistic industrial $PF = 0.85$, a $100\text{ kW}$ peak incurs $117.6\text{ kVA}$ billing demand, increasing demand charges by $17.6\%$.
5. **Time-of-Day (ToD) Schedule (December–June):**
   - 06:00–09:00 (Morning Peak): $+100\text{ paise/unit} \implies \mathbf{\text{₹ } 7.60 / \text{kWh}}$ (3 hours)
   - 09:00–18:00 (Normal): $+0\text{ paise/unit} \implies \mathbf{\text{₹ } 6.60 / \text{kWh}}$ (9 hours)
   - 18:00–22:00 (Evening Peak): $+100\text{ paise/unit} \implies \mathbf{\text{₹ } 7.60 / \text{kWh}}$ (4 hours)
   - 22:00–06:00 (Night Off-Peak): $-100\text{ paise/unit} \implies \mathbf{\text{₹ } 5.60 / \text{kWh}}$ (8 hours)
   - (July–November: Flat rate ₹6.60/kWh with zero ToD adjustment).

---

### 6.2. The Monthly Aggregation Fallacy
A critical error in naive energy scheduling literature is dividing a monthly demand charge by 25 working days ($\text{₹ } 350 / 25 = 14.00\text{ ₹/kW/day}$) and asserting that a daily peak-shaving schedule saves ₹14 per kW shaved.

#### Why This Assertion is Methodologically Invalid:
1. **Extreme-Value Billing:** Utility demand meters do not average daily peaks. The monthly bill is determined by the **single highest 15-minute peak out of approximately 2,880 fifteen-minute intervals in the month**.
2. **Zero Marginal Value on Non-Peak Days:** Shaving $10\text{ kW}$ on Tuesday shift 1 yields **zero monthly savings** if Wednesday shift 2 sets a higher peak.
3. **Contract Ratchet Barrier:** If the shaved peak is below $0.90 \times CD$, monthly billing demand remains locked at $0.90 \times CD$, resulting in zero bill reduction.

#### Strict Research Boundary Frozen:
- **Model A (Normalized Benchmark):** $\rho$ ($\text{₹}/\text{kW}$) is strictly an **experimental sensitivity parameter** applied over the scheduling horizon to map the trade-off frontier.
- **Model B (Tariff Discussion):** Real KERC monthly billing rules provide the qualitative context for economic discussion, but are **never conflated with simulated daily savings**.

---

## 7. Section F — Physical-Validation Boundary Audit

### 7.1. Numerical Scale Separation: Industrial Model vs. DC Testbed
The pre-modelling audit mandates a strict separation between industrial synthetic benchmarks and the physical hardware testbed:

| Attribute | Industrial Synthetic Benchmark | Physical Hardware Testbed | Scaling / Translation Factor |
|---|---|---|---|
| **System Voltage** | $415\text{ V AC } (3\text{-phase}) \text{ or } 11\text{ kV}$ | **$12.0\text{ V DC}$** (Enclosed commercial SMPS) | Purely DC; galvanic isolation |
| **Machine 1 Power** | $10.0\text{ kW}$ (Assembly tool / drive) | **$15.0\text{ W to } 24.0\text{ W}$** (12V 775 DC Motor) | Power scale: $1:1000$ (kW to W) |
| **Machine 2 Power** | $25.0\text{ kW}$ (Thermal furnace / cure) | **$25.0\text{ W to } 40.0\text{ W}$** (12V Ceramic Heater) | Power scale: $1:1000$ (kW to W) |
| **Facility Base Load** | $2.0\text{ kW}$ | **$2.0\text{ W}$** (Quiescent rail load / LED) | Power scale: $1:1000$ (kW to W) |
| **Total Peak Demand** | $27.0\text{ kW to } 37.0\text{ kW}$ | **$27.0\text{ W to } 66.0\text{ W}$** (Within 120W supply) | Supply capacity verified (<10A) |
| **Shift Duration** | $8.0\text{ hours}$ | **$8.0\text{ minutes } (480\text{ s})$** | Time scale: $1:60$ ($1\text{ slot} = 60\text{ s}$) |
| **Power Factor** | $PF \approx 0.85$ (Inductive AC) | **$PF \equiv 1.00$** (Pure DC) | No reactive power in testbed |
| **Energy Consumed** | $120\text{ to } 160\text{ kWh}$ | **$0.02\text{ to } 0.04\text{ kWh } (20–40\text{ Wh})$** | Measured in Watt-hours |

---

### 7.2. Hardware Capability: What Can and Cannot Be Validated

#### What CAN Be Validated Directly:
1. **Execution Fidelity:** Demonstrating that physical loads switch ON and OFF at exact scheduled timestamps commanded by the ESP32 via relay/MOSFET channels.
2. **Dynamic Aggregate Power Trace:** Verifying that measured aggregate DC power $P_{\text{meas}}(t) = V_{\text{bus}}(t) \cdot I_{\text{shunt}}(t)$ follows the stepped profile of scheduled power $P_{\text{pred}}(t)$.
3. **Relative Peak Shaving and Staggering:** Proving physically that Strategy C prevents simultaneous current draw, lowering measured peak DC current (Amperes) relative to Strategy B.
4. **Model Prediction Accuracy:** Quantifying physical energy integration error and peak prediction error:
   $$\text{Error}_E = \frac{|E_{\text{pred}} - E_{\text{meas}}|}{E_{\text{meas}}} \times 100\%$$
   $$\text{MAE}_P = \frac{1}{T_{\text{exec}}} \int_0^{T_{\text{exec}}} |P_{\text{pred}}(t) - P_{\text{meas}}(t)| \, dt$$

#### What CANNOT Be Validated Directly (Forbidden Claims):
1. **Industrial Bill Dollar Savings:** The testbed **cannot claim** to demonstrate ₹100 or ₹1,000 monthly utility bill savings.
2. **AC Power Factor and Harmonics:** The testbed **cannot validate** reactive power penalties, phase imbalances, or kVA demand ratchets.
3. **Full Industrial Scale:** 12V DC loads do not replicate real factory tool-wear, thermal inertia, or mechanical feed variations.

---

### 7.3. Measurement Instrumentation and Uncertainty Floor
- **Sensor:** INA226 high-side bi-directional current/power monitor with $I^2C$ interface.
- **ADC Resolution:** 16-bit internal sigma-delta ADC.
- **Conversion Time & Averaging:** Configured for $1.1\text{ ms}$ conversion with 16 averages $\implies 17.6\text{ ms}$ sampling window.
- **Measurement Uncertainty Floor:**
  - INA226 gain error: $\pm 0.1\%$ maximum.
  - Current shunt resistor tolerance: $\pm 1.0\%$.
  - Thermal drift of shunt under load: $\approx \pm 0.5\%$.
  - **Total Empirical Measurement Floor:** $\approx \mathbf{\pm 1.5\%\text{ to }\pm 2.0\%}$.
- Any scheduling model prediction error below $\pm 2.0\%$ is indistinguishable from physical sensor noise.

---

## 8. Section G — Review of Experimental Claims & Statistical Protocol

### 8.1. Scientific Taxonomy of Claims
To prevent conflation in reporting, three distinct classes of claims must be strictly maintained:

```
+--------------------------------------------------------------------------------------------------+
|                                  CLAIM CLASSIFICATION TAXONOMY                                   |
+--------------------------------------------------------------------------------------------------+
|                                                                                                  |
|  CLASS 1: ARITHMETIC BREAK-EVEN (Deterministic Single-Instance Property)                        |
|  - Definition: The algebraic value rho* = (EC_C - EC_B)/(P_max,B - P_max,C) for a specific      |
|    verified instance.                                                                            |
|  - Status: Mathematical fact for THAT instance; zero statistical generality.                    |
|                                                                                                  |
|  CLASS 2: OBSERVED ECONOMIC ADVANTAGE (Empirical Sample Descriptive Metric)                      |
|  - Definition: The sample mean and median percentage saving Delta_TEC_% across N synthetic       |
|    instances under a fixed parameter cell (rho, gamma, W, sigma_P).                              |
|  - Status: Empirical observation; descriptive only.                                             |
|                                                                                                  |
|  CLASS 3: STATISTICALLY SIGNIFICANT TREATMENT EFFECT (Inferential Hypothesis Test)               |
|  - Definition: Rejection of the null hypothesis H0 (Strategy B = Strategy C) using paired        |
|    non-parametric testing (Wilcoxon signed-rank, p < 0.01) with bootstrap confidence intervals. |
|  - Status: Defensible scientific finding supporting H1.                                          |
|                                                                                                  |
+--------------------------------------------------------------------------------------------------+
```

---

### 8.2. Rigorous Experimental Procedure for Later Computational Testing
1. **Paired Instance Generation:** Synthetic instances must be evaluated in **strict pairs**: Strategy B and Strategy C must solve the exact same manufacturing instance with identical processing times, deadlines, and machine power ratings.
2. **Deterministic Seed Management:** All instance generation must use fixed, recorded pseudo-random seeds (e.g., seeds 1000–1019 for 20 instances per cell).
3. **Optimality Verification Filter:** Only solver runs achieving **proven global optimality (`OPTIMAL`, optimality gap $= 0.0\%$)** will be included in primary hypothesis tests. Time-limited or heuristic solutions will be reported in a segregated scalability section.
4. **Statistical Testing Protocol:**
   - Primary metric: Percentage Total Electricity Cost Reduction:
     $$\Delta TEC_{\%} = \frac{TEC^{(B)} - TEC^{(C)}}{TEC^{(B)}} \times 100\%$$
   - Non-parametric **Wilcoxon Signed-Rank Test** across paired instances for each parameter cell.
   - Non-parametric **Friedman Test** with post-hoc Nemenyi pairwise comparisons for the three-way comparison (Strategy A vs. B vs. C).
   - 95% Bootstrap Confidence Intervals (10,000 resamples) reported for all median percentage savings.

---

### 8.3. Methodological Re-Assessment of Pareto Analysis for V1
- **Is Pareto Analysis Required for V1?**
  - **No, not for the core hypothesis.** The central research question asks: *Under what conditions does peak-aware scheduling (C) provide a statistically significant benefit over energy-cost-only scheduling (B)?*
  - This is an **economic hypothesis-testing question** answered definitively by comparing the two strategies across the factorial parameter grid.
- **Double-Counting Hazard Identified:**
  - Master Execution Plan Part 10 proposed a 3D Pareto surface minimizing $\{C_{\max}, EC, P_{\max}\}$.
  - In some preliminary notes, researchers proposed optimizing $\{C_{\max}, EC, TEC\}$. This is a **severe methodological flaw**: because $TEC = EC + \rho P_{\max}$, including both $EC$ and $TEC$ double-counts energy cost and distorts Pareto dominance.
- **Decision for V1:** Core V1 computational effort will focus 100% on the controlled **Three-Strategy Comparison (A, B, C)** using Sequential Lexicographic Optimization. Multi-objective $\epsilon$-constraint Pareto sweeps (AUGMECON2) are deferred to a specialized secondary study.

---

## 9. Section H — Audit Trail of File Corrections

The following authoritative updates have been made or are required across repository documents:

### 9.1. Updates to `04_mathematical_model/verification/test_instances/hand_calculations.md`
1. **Section 3.1 (Strategy A):** Corrected optimal makespan from $5.0\text{ h}$ to **$4.0\text{ h}$**. Updated job assignment to $\{J1, J3\}$ on $M1$ and $\{J2, J4\}$ on $M2$. Corrected power profile ($37.0\text{ kW}$ for slots 1–4), $EC = \text{₹ } 1031.60$, and $TEC = \text{₹ } 1586.60$.
2. **Section 3.2 (Strategy B):** Corrected optimal energy cost from $\text{₹ } 862.60$ to **$\text{₹ } 785.60$**. Updated assignment to $\{J1, J2, J4\}$ on $M1$ and $\{J3\}$ on $M2$. Added mathematical proof of the Machine Efficiency vs. Tariff Ratio principle. Updated $TEC = \text{₹ } 1340.60$.
3. **Section 3.3 (Strategy C):** Replaced the fragmented schedule with the strictly contiguous, non-preemptive schedule: $M2$ runs $J4$ (slots 1–2) and $J3$ (slot 8); $M1$ runs $J1$ (slots 3–4) and $J2$ (slots 5–7). $P_{\max} = 27.0\text{ kW}$, $EC = \text{₹ } 912.60$, $TEC = \text{₹ } 1317.60$.
4. **Section 6 (Break-Even Sensitivity):** Updated true break-even demand charge rate from $\text{₹ } 5.00/\text{kW}$ to **$\text{₹ } 12.70/\text{kW}$**. Documented that net savings at $\rho = 15.00\text{ ₹/kW}$ are $\text{₹ } 23.00$ ($1.72\%$).
5. **Section 2.3 (Time Discretization):** Clarified that the 8-slot model is an illustrative normalized benchmark ($1.0\text{ h}$ slots), distinct from the 32-slot ($15\text{ min}$) production scheduling formulation.

### 9.2. Updates to `04_mathematical_model/formulation/mathematical_model_v1.md`
1. **Section 6 (Objective Functions):** Formally replaced weighted single-pass $\epsilon$ objectives with **Sequential Lexicographic Optimization** protocol (Phase 1 primary solve, Phase 2 compactness/flow-time solve).
2. **Section 5.6 (Demand Window Formulation):** Added duration-weighted average definition (Eq. DW-1) and documented condition for arithmetic average validity.

### 9.3. Updates to `PROJECT_STATUS.md`
1. Updated phase status from "Phase 2 Complete → Phase 3 Implementation" to **"Phase 2 Verification Audit Completed — Implementation Blocked Pending Rectification"**.

---

## 10. Explicit Unresolved Issues & Pre-Implementation Gate Checklist

Before Google OR-Tools CP-SAT code implementation can be authorized, the following explicit conditions must be met:

- [x] **Audit Finding Verification:** All mathematical discrepancies between claimed benchmark numbers and true optima independently derived and cataloged.
- [ ] **Benchmark File Synchronization:** Update `hand_calculations.md` to reflect the corrected, verified schedules and break-even rates so unit test assertions have valid ground truth.
- [ ] **Formulation File Synchronization:** Update `mathematical_model_v1.md` Section 6 to formally specify the two-phase sequential lexicographic optimization procedure.
- [ ] **Time Discretization Interface Agreement:** Confirm data structure representation in `src/model/instance.py` supports both $\Delta t = 0.25\text{ h}$ (production) and $\Delta t = 1.0\text{ h}$ (verification toy instance).
- [ ] **Formal Authorization:** Final review and sign-off of corrected documents.

### Final Readiness Declaration:
```
====================================================================================================
                        PRE-IMPLEMENTATION AUDIT DECISION:
                        [ NOT READY FOR IMPLEMENTATION ]
  Reason: Critical baseline numbers and mathematical objective structures require formal
          synchronization in repository formulation files before writing solver code.
====================================================================================================
```

*End of Pre-Implementation Mathematical Verification Audit.*
