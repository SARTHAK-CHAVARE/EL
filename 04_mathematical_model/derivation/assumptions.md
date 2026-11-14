# Mathematical Model Assumptions, Simplifications, and Scope Limits

**Project:** Peak-Aware Energy-Cost Production Scheduling for Small Manufacturing Systems Under Industrial Tariff Structures: A Multi-Objective Optimization Study with Physical Validation  
**Phase:** Mathematical Foundation (Phase 2 Deliverable)  
**Date:** 2026-10-27  
**Status:** Approved for Model V1.0  

---

## 1. Classification of Model Assumptions

To ensure complete research integrity, all assumptions in Mathematical Model V1.0 are classified into three distinct categories:
1. **LITERATURE-DERIVED:** Directly established and validated in published academic scheduling research.
2. **REGULATORY-DERIVED:** Grounded in official electricity regulatory orders (KERC Tariff Order 2025).
3. **PROJECT-SPECIFIC MODELLING ASSUMPTIONS:** Deliberately introduced for computational tractability, experimental control, or physical testbed hardware alignment.

---

## 2. Table of Core Assumptions

| # | Assumption | Classification | Rationale & Academic/Physical Basis | Impact on Model V1 | Threat to Validity & Documented Limitation |
|---|---|---|---|---|---|
| **A01** | **Deterministic Processing Times** | Literature-Derived | Standard scheduling foundation (Sung & Kwon 2026, Catanzaro et al. 2023, Moon et al. 2013). Jobs have known processing durations $p_{jm}$. | Removes stochastic variables; enables exact optimization. | Real-world processing has minor tool-wear/operator variability; can be addressed in stretch uncertainty testing. |
| **A02** | **Static / Offline Job Pool** | Literature-Derived | All jobs $j \in \mathcal{J}$ are available at the beginning of the scheduling horizon or have known release times $r_j$. | Fixes problem dimension $N$ for deterministic optimization. | Does not model dynamic real-time job arrivals (out of scope per Master Plan). |
| **A03** | **Non-Preemptive Operations** | Literature-Derived | Once job $j$ starts on machine $m$, it runs continuously for $p_{jm}$ contiguous slots without interruption. | Standard for CNC machining, 3D printing, and automated manufacturing processes. | Preemption could theoretically improve peak avoidance, but is physically inadmissible for machining. |
| **A04** | **Unrelated Parallel Machine Topology** | Project-Specific / Hardware Match | $M$ parallel machines with machine-dependent processing times $p_{jm}$ and power ratings $P_{jm}$. | Maps directly to the 3–4 channel INA226 testbed (DC motor, heater, lamp, fan). | Does not capture multi-stage routing or WIP buffer storage of a job shop. |
| **A05** | **Constant Processing Power During Operation** | Project-Specific / Testbed-Derived | Electrical power draw $P_{jm}$ is treated as constant throughout the duration of job $j$ on machine $m$. | Verified on resistive and steady-state DC motor testbed loads; drastically simplifies power accounting. | Ignores transient electrical inrush currents or tool feed-rate variations; physical testbed measures this exact gap. |
| **A06** | **Omission of Dynamic Idle / Standby States in V1** | Project-Specific Simplification | Machines draw zero dynamic power when not processing jobs; constant background load $P_{\text{base}}$ accounts for facility auxiliary power. | Prevents binary variable explosion in CP-SAT on Raspberry Pi 5; isolates causal effect of scheduling decisions. | In facilities with heavy standby loads, baseline peak is higher. Extended multi-state model derived in Section 9 of V1 specification. |
| **A07** | **Unity Power Factor ($PF = 1.0$)** | Physical Testbed Constraint | Active power in $\text{kW}$ is equated to apparent power in $\text{kVA}$ ($P = S$). | Physical testbed uses low-voltage DC loads (purely active power). | Industrial AC motors operate at $PF \approx 0.80–0.90$, increasing commercial kVA demand. Documented in Model A vs B distinction. |
| **A08** | **Discretized Time-Slot Horizon** | Literature-Derived | Planning horizon $H$ is partitioned into uniform slots of $\Delta t$ ($5\text{ min}$ or $15\text{ min}$). | Necessary for time-varying ToU rate lookup ($C_t$) and interval peak demand averaging ($p_k^{\text{int}}$). | Time resolution must be chosen to balance solver speed against schedule precision. |
| **A09** | **Normalized Research Demand Charge (Model A)** | Literature-Derived | Demand charge is parameterized as $\rho \cdot P_{\max}$ ($\text{₹}/\text{kW}$ per scheduling horizon) following Sung & Kwon (2026). | Enables systematic sensitivity sweeps over demand-charge intensity without claiming a commercial monthly bill. | Commercial demand charges are monthly and subject to a 90% contract demand ratchet under KERC HT-2(a). |
| **A10** | **Independent Non-Interfering Machines** | Physical Testbed Reality | Operation of machine $m_1$ does not affect the voltage or power draw of machine $m_2$. | DC power supply is sized with sufficient overhead to prevent bus voltage collapse during concurrent switching. | Verified during hardware commissioning (power bus stability testing). |

---

## 3. Justification for Model Boundary Freezes

### 3.1. Why Flow Shops and Flexible Job Shops Were Excluded
While flexible job shop scheduling ($FJSP$) is common in literature (Dai et al. 2019), it introduces complex sequencing dependencies, automated guided vehicle (AGV) routing, and buffer congestion. In this project, the primary research question concerns **the economic trade-off between energy-cost-only scheduling and peak-demand charges**. The unrelated parallel machine environment isolates this exact causal trade-off without confounding routing delays.

### 3.2. Why Dynamic Idle States Were Omitted from V1
Mouzon et al. (2007) and Aghelinejad et al. (2019) demonstrated that shutting down idle equipment requires a minimum breakeven gap $S = SE / IP$. For small manufacturing cells (e.g. 3D printing farms, benchtop CNCs), warmup times, bed-heating delays, and recalibration penalties make frequent shutdown impractical during an active working shift. By absorbing idle power into a constant baseline $P_{\text{base}}$, Model V1 maintains focus on peak operational concurrency.

---

*End of Assumptions Document.*
