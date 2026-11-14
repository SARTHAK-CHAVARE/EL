# Benchmark Verification: Hand-Solved Toy Instance (Post-Audit Rectified)

**Project:** Peak-Aware Energy-Cost Production Scheduling for Small Manufacturing Systems Under Industrial Tariff Structures: A Multi-Objective Optimization Study with Physical Validation  
**Phase:** Mathematical Foundation (Phase 2 Deliverable)  
**Date:** 2026-10-27  
**Status:** Canonical Hand Verification & Exact Mathematical Benchmarks (Audit-Rectified)  
**Audit Reference:** `04_mathematical_model/verification/model_v1_preimplementation_audit.md`

---

## 1. Objectives of Hand Verification

Before implementing the optimization model in Google OR-Tools CP-SAT, this document provides a rigorous, hand-solved benchmark instance to achieve three vital scientific goals:
1. **Mathematical Consistency Check:** Verify that Equations (1)–(22) in [`mathematical_model_v1.md`](file:///c:/Project/EL/04_mathematical_model/formulation/mathematical_model_v1.md) are well-posed, complete, and mutually consistent.
2. **Behavioral Differentiation Proof:** Demonstrate through exact arithmetic how the three scheduling strategies (A: Makespan, B: Energy-cost-only, C: Peak-aware) diverge in their scheduling choices from the exact same input data.
3. **Causal Mechanism Illustration:** Mathematically confirm the central hypothesis: that energy-cost-only scheduling (Strategy B) induces coincident secondary peaks during cheap tariff hours, and that peak-aware scheduling (Strategy C) achieves net economic savings by trading a small energy penalty for a larger demand-charge reduction.
4. **Audit Trail Preservation:** Explicitly document the corrections identified during the Pre-Implementation Mathematical Verification Audit (Prompt 2B), distinguishing provably optimal schedules from illustrative heuristic baselines.

---

## 2. Toy Instance Specification

The toy instance represents a small manufacturing cell operating over an 8-hour shift, scaled for validation on the 12V DC physical testbed.

### 2.1. Machines ($\mathcal{M} = \{M1, M2\}$)
- **Machine 1 ($M1$):** Low-power unit (e.g., automated assembly tool / DC motor). Active power: $P_1 = 10.0\text{ kW}$ (testbed equivalent: $10.0\text{ W}$).
- **Machine 2 ($M2$):** High-power unit (e.g., thermal curing / DC heater). Active power: $P_2 = 25.0\text{ kW}$ (testbed equivalent: $25.0\text{ W}$).
- **Background Load ($P_{\text{base}}$):** Constant facility lighting and control power: $P_{\text{base}} = 2.0\text{ kW}$ (testbed equivalent: $2.0\text{ W}$).

### 2.2. Production Jobs ($\mathcal{J} = \{J1, J2, J3, J4\}$)
All jobs are released at slot 1 ($r_j = 1$) and have a global completion deadline of slot 8 ($D = 8$).

| Job $j$ | Machine Eligibility $\mathcal{M}_j$ | Processing Time on $M1$ ($p_{j,1}$) | Processing Time on $M2$ ($p_{j,2}$) | Power on $M1$ ($P_{j,1}$) | Power on $M2$ ($P_{j,2}$) |
|---|---|---|---|---|---|
| **$J1$** | $\{M1, M2\}$ | $2\text{ slots } (2\text{ h})$ | $2\text{ slots } (2\text{ h})$ | $10.0\text{ kW}$ | $25.0\text{ kW}$ |
| **$J2$** | $\{M1, M2\}$ | $3\text{ slots } (3\text{ h})$ | $2\text{ slots } (2\text{ h})$ | $10.0\text{ kW}$ | $25.0\text{ kW}$ |
| **$J3$** | $\{M1, M2\}$ | $2\text{ slots } (2\text{ h})$ | $1\text{ slot } (1\text{ h})$ | $10.0\text{ kW}$ | $25.0\text{ kW}$ |
| **$J4$** | $\{M1, M2\}$ | $3\text{ slots } (3\text{ h})$ | $2\text{ slots } (2\text{ h})$ | $10.0\text{ kW}$ | $25.0\text{ kW}$ |

### 2.3. Time Discretization and Electricity Tariff

> [!IMPORTANT]
> **Audit Clarification on Discretization Scale:**  
> This hand-solved benchmark uses a coarse time discretization of **$T = 8\text{ time slots}$** with duration **$\Delta t = 1.0\text{ hour}$** ($H = 8\text{ h}$) and an integration window of **$L = 1\text{ slot} = 1.0\text{ hour}$**.  
> This coarse discretization is designed specifically for **transparent, hand-derivable mathematical proof**. It must NOT be conflated with the production model, which uses $\Delta t = 0.25\text{ h } (15\text{ min})$ and $L = 1\text{ slot}$ over $T = 32$ slots to model real 15-minute utility demand integration windows.

- **Scheduling Horizon:** $T = 8\text{ time slots}$, with duration $\Delta t = 1.0\text{ hour}$ ($H = 8\text{ h}$).
- **Demand Measurement Interval:** $L = 1\text{ slot}$ ($1.0\text{ h}$ integration window; $K = 8$ intervals).
- **Time-of-Use Tariff Vector ($C_t$):**
  - **Slots 1–2 (00:00–02:00):** Off-Peak rate $C_t = \text{₹ } 5.60 / \text{kWh}$
  - **Slots 3–5 (02:00–05:00):** Peak rate $C_t = \text{₹ } 7.60 / \text{kWh}$
  - **Slots 6–8 (05:00–08:00):** Normal rate $C_t = \text{₹ } 6.60 / \text{kWh}$
- **Demand Charge Parameter:** $\rho = \text{₹ } 15.00 / \text{kW}$ per scheduling horizon.

---

## 3. Step-by-Step Evaluation of the Three Strategies

### 3.1. Strategy A: Production-Oriented Baseline ($\min C_{\max}$, tie-break $\min \sum C_j$)

#### Operational Logic
Strategy A prioritizes productivity and equipment utilization above all else. It packs jobs onto both machines to complete the entire batch in the absolute minimum possible time, completely indifferent to tariff rates $C_t$ or coincidental power spikes.

#### Optimal Schedule Assignment (Proven Global Optimum)
To minimize makespan $C_{\max} = \max(W_1, W_2)$, we partition the jobs between $M1$ and $M2$ to balance machine workloads:
- Total processing times if all jobs on $M1$: $2 + 3 + 2 + 3 = 10\text{ hours}$.
- Total processing times if all jobs on $M2$: $2 + 2 + 1 + 2 = 7\text{ hours}$.
- Optimal partitioning: Assign $\{J1, J3\}$ to $M1$ and $\{J2, J4\}$ to $M2$:
  - Workload on $M1$: $W_1 = p_{1,1} + p_{3,1} = 2 + 2 = \mathbf{4.0\text{ hours}}$.
  - Workload on $M2$: $W_2 = p_{2,2} + p_{4,2} = 2 + 2 = \mathbf{4.0\text{ hours}}$.
  - **Makespan ($C_{\max}^{(A)}$):** $\max(4.0, 4.0) = \mathbf{4.0\text{ slots}}$ (4.0 hours).
- *(Note on Previous Draft Suboptimality: The previous report assigned $\{J1, J2\}$ to $M1$ ($W_1=5$) and $\{J3, J4\}$ to $M2$ ($W_2=3$), achieving makespan 5.0 h. Exhaustive search proves that 4.0 h is the true global minimum).*

#### Job Execution Schedule & Completion Times:
- **Machine 1 ($M1$):**
  - $J1$: Starts at $t=1$, runs in slots 1, 2. Completes at $C_1 = 2$.
  - $J3$: Starts at $t=3$, runs in slots 3, 4. Completes at $C_3 = 4$.
- **Machine 2 ($M2$):**
  - $J2$: Starts at $t=1$, runs in slots 1, 2. Completes at $C_2 = 2$.
  - $J4$: Starts at $t=3$, runs in slots 3, 4. Completes at $C_4 = 4$.
- **Sum of Completion Times:** $\sum C_j = 2 + 4 + 2 + 4 = \mathbf{12\text{ slots}}$ (minimizes flow time).

#### Temporal Power Profile $P(t)$ (Eq. 11)
- **Slot 1 ($C_1 = 5.60$):** $M1(J1: 10\text{ kW}) + M2(J2: 25\text{ kW}) + P_{\text{base}}(2\text{ kW}) = \mathbf{37.0\text{ kW}}$
- **Slot 2 ($C_2 = 5.60$):** $M1(J1: 10\text{ kW}) + M2(J2: 25\text{ kW}) + P_{\text{base}}(2\text{ kW}) = \mathbf{37.0\text{ kW}}$
- **Slot 3 ($C_3 = 7.60$):** $M1(J3: 10\text{ kW}) + M2(J4: 25\text{ kW}) + P_{\text{base}}(2\text{ kW}) = \mathbf{37.0\text{ kW}}$
- **Slot 4 ($C_4 = 7.60$):** $M1(J3: 10\text{ kW}) + M2(J4: 25\text{ kW}) + P_{\text{base}}(2\text{ kW}) = \mathbf{37.0\text{ kW}}$
- **Slots 5–8 ($C_{5..8}$):** All machines idle; $P(t) = P_{\text{base}} = \mathbf{2.0\text{ kW}}$

#### Metric Accounting for Strategy A (Global Optimum)
- **Makespan ($C_{\max}$):** $\mathbf{4.0\text{ h}}$
- **Peak Demand ($P_{\max}$):** $\mathbf{37.0\text{ kW}}$
- **Total Energy Consumed:** $(4 \times 37.0) + (4 \times 2.0) = \mathbf{156.0\text{ kWh}}$
- **Energy Cost Calculation ($EC$):**
  $$\begin{aligned}
  EC^{(A)} &= (5.60 \times 37.0 \times 2) + (7.60 \times 37.0 \times 2) + (7.60 \times 2.0 \times 1) + (6.60 \times 2.0 \times 3) \\
  &= 414.40 + 562.40 + 15.20 + 39.60 = \mathbf{\text{₹ } 1031.60}
  \end{aligned}$$
- **Demand Charge Calculation ($DC$):**
  $$DC^{(A)} = \rho \cdot P_{\max} = 15.00 \times 37.0 = \mathbf{\text{₹ } 555.00}$$
- **Total Electricity Cost ($TEC$):**
  $$TEC^{(A)} = EC + DC = 1031.60 + 555.00 = \mathbf{\text{₹ } 1586.60}$$

---

### 3.2. Strategy B: Energy-Cost-Only Scheduling ($\min EC$, tie-break $\min C_{\max}$ s.t. $C_{\max} \le D$)

#### Operational Logic
Strategy B seeks exclusively to minimize energy consumption costs ($EC$) under the Time-of-Use tariff, subject to the deadline constraint $C_{\max} \le 8$.

#### Optimal Schedule Assignment (Proven Global Optimum)
Energy consumption per job on each machine:
- $J1$: $M1 = 20\text{ kWh}$; $M2 = 50\text{ kWh}$ ($\Delta = +30\text{ kWh}$ on $M2$).
- $J2$: $M1 = 30\text{ kWh}$; $M2 = 50\text{ kWh}$ ($\Delta = +20\text{ kWh}$ on $M2$).
- $J3$: $M1 = 20\text{ kWh}$; $M2 = 25\text{ kWh}$ ($\Delta = +5\text{ kWh}$ on $M2$).
- $J4$: $M1 = 30\text{ kWh}$; $M2 = 50\text{ kWh}$ ($\Delta = +20\text{ kWh}$ on $M2$).

Total processing time of all jobs on $M1$ is $10\text{ hours} > D=8\text{ hours}$. Thus, at least one job must run on $M2$.
To minimize total energy cost, the job with the **smallest energy penalty** ($J3$, adding only 5 kWh) is offloaded to $M2$.
- $M1$ is assigned $\{J1, J2, J4\}$, requiring $2 + 3 + 3 = \mathbf{8.0\text{ hours}}$ of work, occupying all 8 slots.
- $M2$ is assigned $\{J3\}$, requiring $1.0\text{ hour}$, placed in the cheapest off-peak slot: **Slot 1 (Off-peak: ₹5.60)**.

#### The Machine Efficiency vs. Tariff Ratio Principle:
Why is running $J4$ on $M1$ during peak hours cheaper than running $J4$ on $M2$ during off-peak hours?
- Running $J4$ on $M2$ off-peak: $50\text{ kWh} \times \text{₹ } 5.60 = \mathbf{\text{₹ } 280.00}$.
- Running $J4$ on $M1$ during peak: $30\text{ kWh} \times \text{₹ } 7.60 = \mathbf{\text{₹ } 228.00}$.
- Because the machine inefficiency ratio ($50/30 = 1.67$) is greater than the tariff peak ratio ($7.60/5.60 = 1.36$), running on the energy-efficient machine during expensive peak hours saves **₹52.00** over running on the inefficient machine during off-peak hours!

#### Job Execution Schedule & Completion Times:
- **Machine 1 ($M1$):**
  - $J1$: Starts at $t=1$, runs in slots 1, 2. Completes at $C_1 = 2$.
  - $J2$: Starts at $t=3$, runs in slots 3, 4, 5. Completes at $C_2 = 5$.
  - $J4$: Starts at $t=6$, runs in slots 6, 7, 8. Completes at $C_4 = 8$.
- **Machine 2 ($M2$):**
  - $J3$: Starts at $t=1$, runs in slot 1. Completes at $C_3 = 1$.
  - Slots 2–8: IDLE.
- **Makespan:** $C_{\max}^{(B)} = \mathbf{8.0\text{ hours}}$.

#### Temporal Power Profile $P(t)$ (Eq. 11)
- **Slot 1 ($C_1 = 5.60$):** $M1(J1: 10\text{ kW}) + M2(J3: 25\text{ kW}) + P_{\text{base}}(2\text{ kW}) = \mathbf{37.0\text{ kW}}$
- **Slot 2 ($C_2 = 5.60$):** $M1(J1: 10\text{ kW}) + M2(0) + P_{\text{base}}(2\text{ kW}) = \mathbf{12.0\text{ kW}}$
- **Slots 3–5 ($C_{3..5} = 7.60$):** $M1(J2: 10\text{ kW}) + M2(0) + P_{\text{base}}(2\text{ kW}) = \mathbf{12.0\text{ kW}}$
- **Slots 6–8 ($C_{6..8} = 6.60$):** $M1(J4: 10\text{ kW}) + M2(0) + P_{\text{base}}(2\text{ kW}) = \mathbf{12.0\text{ kW}}$

#### Metric Accounting for Strategy B (Global Optimum)
- **Makespan ($C_{\max}$):** $\mathbf{8.0\text{ h}}$
- **Peak Demand ($P_{\max}$):** $\mathbf{37.0\text{ kW}}$ (Created in Slot 1 due to inevitable machine overlap)
- **Total Energy Consumed:** $37.0 + (7 \times 12.0) = \mathbf{121.0\text{ kWh}}$
- **Energy Cost Calculation ($EC^{(B)}$):**
  $$\begin{aligned}
  EC^{(B)} &= (1\text{ h} \times 37.0 \times 5.60) + (1\text{ h} \times 12.0 \times 5.60) + (3\text{ h} \times 12.0 \times 7.60) + (3\text{ h} \times 12.0 \times 6.60) \\
  &= 207.20 + 67.20 + 273.60 + 237.60 = \mathbf{\text{₹ } 785.60}
  \end{aligned}$$
- **Demand Charge Calculation ($DC^{(B)}$):**
  $$DC^{(B)} = 15.00 \times 37.0 = \mathbf{\text{₹ } 555.00}$$
- **Total Modeled Electricity Bill ($TEC^{(B)}$):**
  $$TEC^{(B)} = EC + DC = 785.60 + 555.00 = \mathbf{\text{₹ } 1340.60}$$

---

### 3.3. Strategy C: Peak-Aware Total Cost Scheduling ($\min TEC = EC + \rho P_{\max}$, tie-break $\min C_{\max}$)

#### Operational Logic
Strategy C recognizes that peak power incurs a heavy capacity charge ($\rho = \text{₹ } 15.00/\text{kW}$). 
To eliminate the $37.0\text{ kW}$ coincidental spike, Strategy C enforces **complete temporal de-synchronization**: Machines $M1$ and $M2$ never run concurrently.
- Maximum power when $M2$ runs alone: $25.0 + 2.0 = \mathbf{27.0\text{ kW}}$.
- Maximum power when $M1$ runs alone: $10.0 + 2.0 = \mathbf{12.0\text{ kW}}$.
- Peak demand drops from $37.0\text{ kW}$ down to **$27.0\text{ kW}$ (a $10.0\text{ kW}$ reduction, saving ₹150.00 in demand charges)**.

#### Optimal Schedule Assignment (Proven Global Optimum & Strictly Contiguous)
Non-overlap requires $W_1 + W_2 \le 8\text{ hours}$. The unique optimal assignment is:
- $M1$: $\{J1, J2\} \implies W_1 = 2 + 3 = 5\text{ hours}$.
- $M2$: $\{J3, J4\} \implies W_2 = 1 + 2 = 3\text{ hours}$.
- Total machine workload: $5 + 3 = 8\text{ hours}$.

To strictly satisfy **non-preemption (Eq. 5)** and minimize energy cost:
- $M2$ runs $J4$ ($p=2$) in off-peak slots 1, 2 (₹5.60).
- $M1$ runs $J1$ ($p=2$) contiguously in peak slots 3, 4 (₹7.60).
- $M1$ runs $J2$ ($p=3$) contiguously in peak slot 5 (₹7.60) and normal slots 6, 7 (₹6.60).
- $M2$ runs $J3$ ($p=1$) in normal slot 8 (₹6.60).
- **All operations are 100% contiguous with zero preemption and zero machine overlap.**

#### Job Execution Schedule & Completion Times:
- **Machine 1 ($M1$):**
  - $J1$: Starts at $t=3$, runs in slots 3, 4. Completes at $C_1 = 4$.
  - $J2$: Starts at $t=5$, runs in slots 5, 6, 7. Completes at $C_2 = 7$.
- **Machine 2 ($M2$):**
  - $J4$: Starts at $t=1$, runs in slots 1, 2. Completes at $C_4 = 2$.
  - $J3$: Starts at $t=8$, runs in slot 8. Completes at $C_3 = 8$.
- **Makespan:** $C_{\max}^{(C)} = \mathbf{8.0\text{ hours}}$.

#### Temporal Power Profile $P(t)$ (Eq. 11)
- **Slot 1 ($C_1 = 5.60$):** $M1(\text{idle}) + M2(J4: 25) + P_{\text{base}}(2) = \mathbf{27.0\text{ kW}}$
- **Slot 2 ($C_2 = 5.60$):** $M1(\text{idle}) + M2(J4: 25) + P_{\text{base}}(2) = \mathbf{27.0\text{ kW}}$
- **Slot 3 ($C_3 = 7.60$):** $M1(J1: 10) + M2(\text{idle}) + P_{\text{base}}(2) = \mathbf{12.0\text{ kW}}$
- **Slot 4 ($C_4 = 7.60$):** $M1(J1: 10) + M2(\text{idle}) + P_{\text{base}}(2) = \mathbf{12.0\text{ kW}}$
- **Slot 5 ($C_5 = 7.60$):** $M1(J2: 10) + M2(\text{idle}) + P_{\text{base}}(2) = \mathbf{12.0\text{ kW}}$
- **Slot 6 ($C_6 = 6.60$):** $M1(J2: 10) + M2(\text{idle}) + P_{\text{base}}(2) = \mathbf{12.0\text{ kW}}$
- **Slot 7 ($C_7 = 6.60$):** $M1(J2: 10) + M2(\text{idle}) + P_{\text{base}}(2) = \mathbf{12.0\text{ kW}}$
- **Slot 8 ($C_8 = 6.60$):** $M1(\text{idle}) + M2(J3: 25) + P_{\text{base}}(2) = \mathbf{27.0\text{ kW}}$

#### Metric Accounting for Strategy C (Global Optimum)
- **Makespan ($C_{\max}$):** $\mathbf{8.0\text{ h}}$
- **Peak Demand ($P_{\max}$):** $\mathbf{27.0\text{ kW}}$ (Peak shaved by 10.0 kW / 27.03%)
- **Total Energy Consumed:** $(3 \times 27.0) + (5 \times 12.0) = \mathbf{141.0\text{ kWh}}$
- **Energy Cost Calculation ($EC^{(C)}$):**
  $$\begin{aligned}
  EC^{(C)} &= (2\text{ h} \times 27.0 \times 5.60) + (3\text{ h} \times 12.0 \times 7.60) + (2\text{ h} \times 12.0 \times 6.60) + (1\text{ h} \times 27.0 \times 6.60) \\
  &= 302.40 + 273.60 + 158.40 + 178.20 = \mathbf{\text{₹ } 912.60}
  \end{aligned}$$
- **Demand Charge Calculation ($DC^{(C)}$):**
  $$DC^{(C)} = 15.00 \times 27.0 = \mathbf{\text{₹ } 405.00}$$
- **Total Modeled Electricity Bill ($TEC^{(C)}$):**
  $$TEC^{(C)} = EC + DC = 912.60 + 405.00 = \mathbf{\text{₹ } 1317.60}$$

---

## 4. Comprehensive Strategy Comparison & Master Benchmark

### 4.1. Master Comparison Table (Verified Global Optima)

| Performance Metric | Strategy A (Baseline: $\min C_{\max}$) | Strategy B (Energy-Cost: $\min EC$) | Strategy C (Peak-Aware: $\min TEC$) | Impact (C vs. B) | Percentage Impact (C vs. B) |
|---|---|---|---|---|---|
| **Makespan ($C_{\max}$)** | **4.0 h** | 8.0 h | 8.0 h | 0.0 h | 0.0% |
| **Peak Power Demand ($P_{\max}$)** | 37.0 kW | 37.0 kW | **27.0 kW** | **−10.0 kW** | **−27.03% (Peak Shaved)** |
| **Energy Consumption ($E_{\text{total}}$)** | 156.0 kWh | **121.0 kWh** | 141.0 kWh | +20.0 kWh | +16.53% (Energy Trade-off) |
| **Energy Cost ($EC$)** | ₹ 1031.60 | **₹ 785.60** | ₹ 912.60 | +₹ 127.00 | +16.17% (Energy Trade-off) |
| **Demand Charge ($DC$)** | ₹ 555.00 | ₹ 555.00 | **₹ 405.00** | **−₹ 150.00** | **−27.03% (Capacity Savings)**|
| **Total Electricity Bill ($TEC$)** | ₹ 1586.60 | ₹ 1340.60 | **₹ 1317.60** | **−₹ 23.00** | **−1.72% (Net Economic Benefit)** |

---

### 4.2. Visual Schedule Profiles and Power Traces

```
====================================================================================================
SCHEDULE A: MAKESPAN MINIMIZATION (Proven Global Optimum: C_max = 4.0h, P_max = 37.0kW, TEC = ₹1586.60)
====================================================================================================
Slot:        1 (Off)    2 (Off)    3 (Peak)   4 (Peak)   5 (Peak)   6 (Norm)   7 (Norm)   8 (Norm)
M1 (10kW):  [  J1   ]  [  J1   ]  [  J3   ]  [  J3   ]  - idle -   - idle -   - idle -   - idle -
M2 (25kW):  [  J2   ]  [  J2   ]  [  J4   ]  [  J4   ]  - idle -   - idle -   - idle -   - idle -
P(t) (kW):    37.0       37.0       37.0       37.0       2.0        2.0        2.0        2.0
              ^^^^       ^^^^       ^^^^       ^^^^ (Dense concurrent packing across both machines)

====================================================================================================
SCHEDULE B: ENERGY-COST MINIMIZATION (Proven Global Optimum: C_max = 8.0h, EC = ₹785.60, TEC = ₹1340.60)
====================================================================================================
Slot:        1 (Off)    2 (Off)    3 (Peak)   4 (Peak)   5 (Peak)   6 (Norm)   7 (Norm)   8 (Norm)
M1 (10kW):  [  J1   ]  [  J1   ]  [  J2   ]  [  J2   ]  [  J2   ]  [  J4   ]  [  J4   ]  [  J4   ]
M2 (25kW):  [  J3   ]  - idle -   - idle -   - idle -   - idle -   - idle -   - idle -   - idle -
P(t) (kW):    37.0       12.0       12.0       12.0       12.0       12.0       12.0       12.0
              ^^^^ (Single unavoidable overlap spike; all other work routed to efficient M1)

====================================================================================================
SCHEDULE C: PEAK-AWARE TOTAL COST (Proven Global Optimum: C_max = 8.0h, P_max = 27.0kW, TEC = ₹1317.60)
====================================================================================================
Slot:        1 (Off)    2 (Off)    3 (Peak)   4 (Peak)   5 (Peak)   6 (Norm)   7 (Norm)   8 (Norm)
M1 (10kW):  - idle -   - idle -   [  J1   ]  [  J1   ]  [  J2   ]  [  J2   ]  [  J2   ]  - idle -
M2 (25kW):  [  J4   ]  [  J4   ]  - idle -   - idle -   - idle -   - idle -   - idle -   [  J3   ]
P(t) (kW):    27.0       27.0       12.0       12.0       12.0       12.0       12.0       27.0
              ****       **** (Peak shaved to 27kW via strict, non-preemptive load staggering)
====================================================================================================
```

---

## 5. Formal Verification Against Equations (1)–(15)

Every constraint formulated in [`mathematical_model_v1.md`](file:///c:/Project/EL/04_mathematical_model/formulation/mathematical_model_v1.md) is verified on Schedule C:

1. **Constraint (1) — Machine Single Assignment:**  
   $z_{1,1} = 1, z_{2,1} = 1, z_{3,2} = 1, z_{4,2} = 1$. Each job assigned to exactly one machine. (Satisfied)
2. **Constraint (2)–(4) — Start Time and Feasible Horizon:**  
   All jobs start and end within $[1, 8]$. $r_j = 1 \le \text{start}_j \le D - p_{jm} + 1$. (Satisfied)
3. **Constraint (5) — Non-Preemption and Continuity:**  
   - $J1$ executes continuously in slots 3, 4 ($p=2$). Lookback sum $y_{1,1,t} = 1$ for $t \in [3, 4]$ and 0 otherwise.
   - $J2$ executes continuously in slots 5, 6, 7 ($p=3$). Lookback sum $y_{2,1,t} = 1$ for $t \in [5, 7]$ and 0 otherwise.
   - $J4$ executes continuously in slots 1, 2 ($p=2$). Lookback sum $y_{4,2,t} = 1$ for $t \in [1, 2]$ and 0 otherwise.
   - $J3$ executes continuously in slot 8 ($p=1$). Lookback sum $y_{3,2,8} = 1$ and 0 otherwise.
   - **Zero preemption.** (Strictly Satisfied).
4. **Constraint (6) — Machine Non-Overlap:**  
   At every slot $t \in \{1..8\}$, $\sum_j y_{jmt} \le 1$ for both $M1$ and $M2$. (Satisfied)
5. **Constraint (7)–(10) — Makespan:**  
   $C_4 = 2, C_1 = 4, C_2 = 7, C_3 = 8 \implies C_{\max} = \max(2, 4, 7, 8) = 8 \le D$. (Satisfied)
6. **Constraint (11) — Aggregate Facility Power:**  
   $P(t) = \sum P_{jm} y_{jmt} + 2.0\text{ kW}$ is exactly 27.0 kW in slots 1, 2, 8 and 12.0 kW in slots 3–7. (Satisfied)
7. **Constraint (12)–(15) — Peak Demand Formulation:**  
   $P_{\max} = \max_t P(t) = 27.0\text{ kW}$. (Satisfied)

---

## 6. Parametric Sensitivity & Corrected Break-Even Threshold

### 6.1. Recalculation of Break-Even Demand-Charge Rate $\rho^*$
The true break-even demand-charge rate $\rho^*$ between the verified optimal Strategy B and verified optimal Strategy C is:

$$\rho^* = \frac{EC^{(C)} - EC^{(B)}}{P_{\max}^{(B)} - P_{\max}^{(C)}} = \frac{912.60 - 785.60}{37.0 - 27.0} = \frac{127.00}{10.0} = \mathbf{12.70 \text{ ₹/kW}}$$

### 6.2. Sensitivity Table Across Demand-Charge Intensities

| Demand Charge Intensity $\rho$ ($\text{₹}/\text{kW}$) | Strategy B Cost ($TEC^{(B)}$) | Strategy C Cost ($TEC^{(C)}$) | Net Saving ($\Delta TEC$) | Percentage Saving ($\%$) | Optimal Strategy |
|---|---|---|---|---|---|
| **$\rho = 0.0$** (Zero demand charge) | **₹ 785.60** | ₹ 912.60 | −₹ 127.00 | −16.17% | **Strategy B strictly dominates** |
| **$\rho = 5.0$** (Low intensity) | **₹ 970.60** | ₹ 1047.60 | −₹ 77.00 | −7.93% | **Strategy B strictly dominates** |
| **$\rho = 10.0$** (Moderate intensity) | **₹ 1155.60** | ₹ 1182.60 | −₹ 27.00 | −2.34% | **Strategy B dominates** |
| **$\rho = 12.70$** (Break-Even Threshold) | **₹ 1255.50** | **₹ 1255.50** | **₹ 0.00** | **0.00%** | **Equivalence Boundary ($\rho^* = 12.70$)** |
| **$\rho = 15.00$** (Benchmark Value) | ₹ 1340.60 | **₹ 1317.60** | **+₹ 23.00** | **+1.72%** | **Strategy C dominates** |
| **$\rho = 20.00$** (High intensity) | ₹ 1525.60 | **₹ 1452.60** | **+₹ 73.00** | **+4.79%** | **Strategy C dominates** |
| **$\rho = 30.00$** (Extreme demand charge) | ₹ 1895.60 | **₹ 1722.60** | **+₹ 173.00** | **+9.13%** | **Strategy C dominates** |

### 6.3. Essential Methodological Insights
1. **The Threshold Shift:** The true break-even rate ($\rho^* = 12.70\text{ ₹/kW}$) is **2.54× higher** than the erroneously claimed $\rho^* = 5.00\text{ ₹/kW}$. Peak awareness is an advantageous strategy only when capacity charges are substantially heavier than previously reported.
2. **Deterministic Instance Limit:** This break-even point is a mathematical property of this specific 4-job 2-machine instance. It serves as an exact unit-test benchmark for solver verification, but must not be cited as a general empirical conclusion for all manufacturing systems.

---

*End of Rectified Hand Calculations Document.*
