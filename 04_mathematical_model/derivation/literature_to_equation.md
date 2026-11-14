# Literature-to-Equation Traceability Map

**Project:** Peak-Aware Energy-Cost Production Scheduling for Small Manufacturing Systems Under Industrial Tariff Structures: A Multi-Objective Optimization Study with Physical Validation  
**Phase:** Mathematical Foundation (Phase 2 Deliverable)  
**Date:** 2026-10-27  
**Status:** Complete Traceability for Mathematical Model V1.0  

---

## 1. Traceability Matrix: Model V1 Equations to Literature Sources

| Model V1 Eq. # | Mathematical Equation / Constraint | Source Paper(s) | Original Equation & Page | Degree of Transferability & Required Adaptations | Audit Status |
|---|---|---|---|---|---|
| **Eq. (1)–(4)** | Job single assignment and start window bounds:<br>$\sum_{m} z_{jm} = 1$<br>$\sum_t x_{jmt} = z_{jm}$ | Sung & Kwon (2026) [P06]<br>Catanzaro et al. (2023) [P04] | Eq. (1c)–(1d), p. 5 [P06]<br>Eq. (1), p. 1093 [P04] | **Adapted:** Sung & Kwon used identical machines without machine index $m$. We reintroduced machine index $m$ ($x_{jmt}$) for unrelated parallel machines. | **Fully Verified** |
| **Eq. (5)** | Non-preemptive execution indicator:<br>$y_{jmt} = \sum_{t'=\max(t-p_{jm}+1, 1)}^t x_{jmt'}$ | Sung & Kwon (2026) [P06] | Eq. (1b), (1e), p. 5 [P06] | **Adapted:** Extended lookback summation to define binary activity indicator $y_{jmt}$ on specific machine $m$. | **Fully Verified** |
| **Eq. (6)** | Machine capacity / non-overlap:<br>$\sum_{j} y_{jmt} \le 1, \quad \forall m, t$ | Catanzaro et al. (2023) [P04]<br>Standard Scheduling Theory | Section 2, p. 1093 [P04] | **Directly Adopted:** Enforces non-overlap on each machine. Corrects Moon et al. (2013) which lacked this constraint. | **Fully Verified** |
| **Eq. (7)–(10)** | Actual temporal completion time and true makespan:<br>$C_j = \sum_m \sum_t (t+p_{jm}-1) x_{jmt}$<br>$C_{\max} \ge C_j$ | Classical Scheduling Theory<br>(Pinedo 2016) | Standard makespan definition | **Directly Adopted:** Formulates true completion time. Avoids Moon et al. (2013) error where makespan was defined as workload sum. | **Fully Verified** |
| **Eq. (11)** | Aggregate electrical power demand:<br>$P(t) = \sum_m \sum_j P_{jm} y_{jmt} + P_{\text{base}}$ | Moon et al. (2013) [P09]<br>Dai et al. (2019) [P05] | Eq. (3), p. 528 [P09]<br>Eq. (2), p. 146 [P05] | **Adapted:** Synthesizes machine power draw with time-indexed slot activity, plus facility base load. | **Fully Verified** |
| **Eq. (12)–(15)** | Utility interval demand and peak demand bounds:<br>$p_k^{\text{int}} = \frac{1}{L} \sum_{t \in \mathcal{T}_k} P(t)$<br>$P_{\max} \ge p_k^{\text{int}}$ | Sung & Kwon (2026) [P06] | Eq. (1f), p. 5 [P06]<br>Eq. (4c), p. 10 [P06] | **Directly Adopted:** Discrete integration window matching utility billing rules (e.g. 15-min windows). | **Fully Verified** |
| **Eq. (16)–(17)** | Time-of-Use energy cost:<br>$EC = \Delta t \sum_t C_t P(t)$ | Sung & Kwon (2026) [P06]<br>Catanzaro et al. (2023) [P04]<br>Moon et al. (2013) [P09] | Eq. (1b), p. 5 [P06]<br>Eq. (2), p. 1093 [P04]<br>Eq. (3), p. 528 [P09] | **Directly Adopted:** Canonical formulation of time-varying electricity consumption costs under discrete slots. | **Fully Verified** |
| **Eq. (18)** | Production baseline objective:<br>$\min Z_A = C_{\max} + \epsilon_A \sum C_j$ | Pinedo (2016)<br>Mouzon et al. (2007) [P01] | LMIP-MTCTEC, p. 4266 [P01] | **Directly Adopted:** Primary makespan minimization with flow time secondary tie-breaker; strictly zero energy bias. | **Fully Verified** |
| **Eq. (19)–(20)** | Energy-cost-only objective:<br>$\min Z_B = EC + \epsilon_B C_{\max}$ s.t. $C_{\max} \le D$ | Catanzaro et al. (2023) [P04] | BJSTP formulation, p. 1093 [P04] | **Directly Adopted:** Canonical ToU energy minimization subject to deadline. | **Fully Verified** |
| **Eq. (21)–(22)** | Peak-aware total cost objective:<br>$\min Z_C = EC + \rho P_{\max} + \epsilon_C C_{\max}$ | Sung & Kwon (2026) [P06] | Eq. (4a), p. 10 [P06] | **Directly Adopted:** Canonical dual-tariff monetary formulation balancing kWh consumption against kW peak demand. | **Fully Verified** |

---

## 2. Theoretical Grounding of Project Contributions

1. **Academic Synthesis (Engineering Integration):**  
   The mathematical model synthesizes the time-indexed interval demand-charge formulation of Sung & Kwon (2026) with the unrelated parallel machine environment and machine-dependent power characteristics of Moon et al. (2013), correcting the mathematical flaws present in Moon et al.'s original formulation.
2. **Empirical Sensitivity Testing:**  
   The model enables the first systematic evaluation of how demand-charge intensity ($\rho$) interacts with ToU differentials ($\gamma$), workload density ($W$), and machine heterogeneity ($\sigma_P$).
3. **Physical-to-Model Validation:**  
   The decision variables and power accounting equations ($P(t)$) map directly to real-time physical current and voltage logs collected from the INA226 hardware sensors on the 12V DC testbed.

---

*End of Literature-to-Equation Traceability Map.*
