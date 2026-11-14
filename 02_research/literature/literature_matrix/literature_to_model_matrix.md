# Literature-to-Model Matrix

**Project:** Peak-Aware Energy-Cost Production Scheduling for Small Manufacturing Systems Under Industrial Tariff Structures: A Multi-Objective Optimization Study with Physical Validation  
**Purpose:** Track research papers providing mathematical and methodological foundations for the project.  
**Status:** Round 2 verified matrix — full-text extractions completed for 9 accessible papers; 1 candidate marked pending/unavailable.  
**Companion Report:** Detailed equation-level extractions and mathematical derivations are recorded in [`literature_extraction_round_2.md`](file:///c:/Project/EL/02_research/literature/notes/literature_extraction_round_2.md).

---

## 1. Verification Rules

- Verify bibliographic details using publisher records and digital object identifiers (DOIs).
- Inspect the actual local full-text PDF before marking any mathematical formulation as verified.
- Record exact equation numbers and dual page references (printed journal page and PDF viewer page).
- Strictly distinguish between:
  1. A hard peak-power constraint ($P(t) \le \bar{P}_{\max}$);
  2. A peak-power minimization objective ($\min P_{\max}$);
  3. An explicit monetary demand charge ($DCR \cdot P_{\max}$ in $\$$).
- Do not assert a research gap as confirmed or novel based solely on preliminary search queries.

---

## 2. Core Literature Matrix

| ID | Verified Citation | Local PDF Path | Full-Text Status | Scheduling Class | Objective Functions | Energy-Cost Formulation | Peak / Demand-Charge Treatment | Solution Method | Equation & Page References | Potentially Adoptable Components | Required Adaptations & Limitations |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **P01** | Mouzon, Yildirim & Twomey (2007)<br>*Int. J. Prod. Res.* 45(18–19): 4247–4271.<br>DOI: [10.1080/00207540701450013](https://doi.org/10.1080/00207540701450013) | `02_research/literature/papers/Operational_methods_for_minimization_of_energy_con.pdf` | Full-text extracted (Author Accepted Manuscript) | Single Machine ($1$) | $\min \sum C_j$,<br>$\min \text{TEC}$ | Physical energy only ($SE + PE + IE$); constant tariff | **None** (no peak constraint, no peak objective, no demand charge) | Weighted-sum MILP (CPLEX 9.0) & dispatching heuristics | Breakeven $S$: p. 4253 (manuscript p. 7, PDF p. 9)<br>LMIP-MTCTEC: p. 4266 (manuscript p. 23, PDF p. 25)<br>LMIP-MTCTEC-W: p. 4267 (manuscript p. 24, PDF p. 26) | Breakeven idle shutdown rule $S = SE/IP$; linearization of idle vs setup | Fixed sequence (FIFO); no ToU rates; no peak-power tracking |
| **P02** | Gahm, Denz, Dirr & Tuma (2016)<br>*Eur. J. Oper. Res.* 248(3): 744–757.<br>DOI: [10.1016/j.ejor.2015.07.017](https://doi.org/10.1016/j.ejor.2015.07.017) | `02_research/literature/papers/Energy-efficient scheduling in manufacturing companies A review and research framework.pdf` | Full-text extracted | Review ($1, P, F, J, HS$) | Survey of monetary & non-monetary metrics | Classifies ToU, CPP, RTP, and contracted power tariffs | Classifies power limits ($PE$) vs demand penalties ($CS-P$) | Survey (MIP, metaheuristics, standard solvers) | Framework: pp. 747–751 (PDF pp. 4–8)<br>Table 3 & 4 classifications | Taxonomy of energy coverage, supply, and demand; validation benchmark | High-level survey; no single executable mathematical model |
| **P03** | Mavrotas (2009)<br>*Appl. Math. Comput.* 213(2): 455–465.<br>DOI: [10.1016/j.amc.2009.03.037](https://doi.org/10.1016/j.amc.2009.03.037) | `02_research/literature/papers/Effective implementation of the ε-constraint method in Multi-Objective Mathematical Programming problems.pdf` | Full-text extracted | General MOMP / MOIP | $\max (f_1 + eps \sum \frac{s_k}{r_k})$ | N/A (methodology paper) | N/A | Augmented $\epsilon$-constraint (AUGMECON, GAMS/CPLEX) | Payoff table: p. 458 (PDF p. 4)<br>AUGMECON (Eq. 3): p. 459 (PDF p. 5) | Exact Pareto generation avoiding weakly efficient solutions; slack scaling | Needs solver integration (OR-Tools / CP-SAT); grid tuning required |
| **P04** | Catanzaro, Pesenti & Ronco (2023)<br>*Eur. J. Oper. Res.* 308(3): 1091–1109.<br>DOI: [10.1016/j.ejor.2023.01.029](https://doi.org/10.1016/j.ejor.2023.01.029) | `02_research/literature/papers/Job scheduling under Time-of-Use energy tariffs for sustainable, a survey.pdf` | Full-text extracted | Survey ($1, P, F, J, FJ$) | $\min E(S) = \sum c_t$ subject to $C_{\max} \le D$ | Time-of-Use (ToU) energy cost over discrete slots | **Completely absent across 135+ papers** (0 occurrences of "demand charge" or "peak demand"; "peak" refers solely to tariff periods) | Survey of exact time-indexed IP & metaheuristics | BJSTP model: p. 1093 (PDF p. 3)<br>Taxonomy: pp. 1095–1103 | Canonical BJSTP definition; evidence of peak-demand gap in ToU literature | Pure energy-cost survey; demonstrates lack of demand-charge literature |
| **P05** | Dai, Tang, Giret & Salido (2019)<br>*Robot. Comput. Integr. Manuf.* 59: 143–157.<br>DOI: [10.1016/j.rcim.2019.04.006](https://doi.org/10.1016/j.rcim.2019.04.006) | `02_research/literature/papers/Multi-objective optimization for energy-efficient flexible job shop scheduling problem with transportation constrainst.pdf` | Full-text extracted | Flexible Job Shop ($FJSP$) | $\min C_{\max}$,<br>$\min E$ ($SE+PE+IE+TE+AE$) | Physical energy consumption (kWh) with constant rate | **None** (no peak constraint, no peak objective, no demand charge) | Modified Genetic Algorithm & MILP (CPLEX) | Energy modules (Eq. 1–5): pp. 146–147 (PDF pp. 4–5)<br>Model (Eq. 6–16): pp. 147–148 (PDF pp. 5–6) | Multi-component energy breakdown (processing, idle, auxiliary) | Constant energy prices; no ToU; no demand charges; complex AGV logistics |
| **P06** | Sung & Kwon (2026)<br>*Appl. Energy* 415: 127953.<br>DOI: [10.1016/j.apenergy.2026.127953](https://doi.org/10.1016/j.apenergy.2026.127953) | `02_research/literature/papers/Demand charge determination for managing peak demand in energy-aware production scheduling.pdf` | Full-text extracted | Identical Parallel ($P$) | $\min ec$,<br>$\min (ec + DCR \cdot p_{\max})$ | Time-varying energy charge ($C_t \cdot E_j$) under ToU & RTP | **Explicitly models both:** Hard limit constraint (Eq. 1f, p. 5) & $\$ / kW$ Demand Charge (Eq. 4a, p. 10) | $\epsilon$-constraint with Gurobi 12.0.2; Peak-Energy Curve regression | TI-IP: pp. 4–5 (PDF pp. 4–5)<br>PD: p. 8 (PDF p. 8)<br>DCR: p. 7 (PDF p. 8)<br>TEC: p. 10 (PDF p. 10) | Time-indexed interval peak constraint; dual-component economic objective ($ec + DCR \cdot p_{\max}$) | Identical parallel machines only (zero machine heterogeneity); zero idle power; zero transition states |
| **P07** | Mavrotas & Florios (2013)<br>*Appl. Math. Comput.* 219(18): 9652–9669.<br>DOI: [10.1016/j.amc.2013.03.002](https://doi.org/10.1016/j.amc.2013.03.002) | `02_research/literature/papers/An improved version of the augmented.pdf` | Full-text extracted (MPRA Paper No. 105034 Preprint) | General MOIP / MOMILP | $\max (f_1 + eps \sum 10^{-(k-2)} \frac{S_k}{r_k})$ | N/A (methodology paper) | N/A | AUGMECON2 with bypass coefficient $b = \lfloor S_2 / step_2 \rfloor$ (GAMS/CPLEX) | Formulation: journal p. 9657 (MPRA p. 7)<br>Bypass formula: journal p. 9658 (MPRA p. 8) | Exact Pareto set generation for integer objectives; dramatic solver speedup via bypass | Requires integer coefficients for exact bypass; needs CP-SAT adaptation |
| **P08** | Fang, Lin & Tang (2013)<br>*Ann. Oper. Res.*<br>DOI: [10.1007/s10479-012-1294-z](https://doi.org/10.1007/s10479-012-1294-z) | Local PDF not present in workspace | Unavailable / Pending | Flow Shop ($F$) | *Pending retrieval* | *Pending retrieval* | Candidate peak-power constraint | *Pending retrieval* | *Pending retrieval* | Candidate peak-power formulation | Full text unavailable; do not adopt equations until verified |
| **P09** | Moon, Shin & Park (2013)<br>*Int. J. Adv. Manuf. Technol.* 68(1–4): 523–535.<br>DOI: [10.1007/s00170-013-4749-8](https://doi.org/10.1007/s00170-013-4749-8) | `02_research/literature/papers/2013_IJAMT_OptimizationOfProductionSchedulingWithTime-dependentAndMachine-dependentElectricityCostForIndustrialEnergyEfficiency.pdf` | Full-text extracted | Unrelated Parallel ($R$) | $\min (C_{\max} \cdot PC + EC)$ | Machine-dependent power ($c_i$) with hourly ToU rate ($e_k$) | **None** (no peak constraint, no peak objective, no demand charge) | Hybrid Inserted Genetic Algorithm (HIGA) & MILP (CPLEX) | Equations (1)–(6): p. 528 (PDF p. 6)<br>Tariff data: p. 527 (PDF p. 5) | Machine-power heterogeneity ($c_i$); intentional idle insertion for ToU | Flawed makespan equation (Eq. 2 defines workload sum); missing non-overlap constraint $\sum_j x_{ijk} \le 1$; zero idle power |
| **P10** | Aghelinejad, Ouazene & Yalaoui (2019)<br>*Oper. Res. Perspect.* 6: 100108.<br>DOI: [10.1016/j.orp.2019.100108](https://doi.org/10.1016/j.orp.2019.100108) | `02_research/literature/papers/Complexity analysis of energy-efficient single machine scheduling problems.pdf` | Full-text extracted | Single Machine ($1$) | $\min \text{TEC} = \sum e_k c_t$ | Multi-state energy consumption ($ON, OFF, Idle, Ton, Toff$) under ToU | **None** (no peak constraint, no peak objective, no demand charge) | Graph Dynamic Programming ($O(PT^2)$) & CPLEX | State power rules: p. 3 (PDF p. 3)<br>Strong NP-hardness proof: Theorem 3, p. 7 | Exact complexity proofs; multi-state energy transition formulation | Single machine only; constant job power; no peak demand charges |
| **P17** | Physical validation literature | Investigation note | Pre-modelling audit completed | Multi-environment | Multiple | Multiple | Multiple | Multiple | Review across 222+ articles in P02 & P04 + 9 primary PDFs | Zero physical testbeds reported in analyzed corpus | Physical testbed validation is a defensible primary contribution addressing simulation gap |

---

## 3. Individual Evidence Summaries

### Summary 3.1: Mouzon et al. (2007) — [P01]
- **Verified Problem:** Single-machine dispatching and mathematical scheduling minimizing total completion time and energy consumption.
- **Energy State Formulation:** Identifies that de-energizing an idle machine is only economically beneficial if the idle gap exceeds the breakeven threshold $S = SE / IP$, where $SE$ is turn-off/turn-on setup energy and $IP$ is idle power.
- **Project Role:** Provides the physical switching threshold for machine-load emulators.
- **Limitation:** Does not model time-of-use tariffs, peak power limits, or demand charges.

### Summary 3.2: Gahm et al. (2016) — [P02]
- **Verified Scope:** Taxonomy of 87 Energy-Efficient Scheduling papers across energetic coverage, energy supply, and energy demand.
- **Key Evidence:** Identifies that contractual power penalties ($CS-P$) and peak limits ($PE$) are modeled in only a tiny fraction of studies compared to energy-only metrics. Documents zero physical testbed validations across all 87 papers.
- **Project Role:** Taxonomic foundation for framing research contributions and experimental design.

### Summary 3.3: Mavrotas (2009) — [P03]
- **Verified Method:** Augmented $\epsilon$-constraint method (AUGMECON) for multi-objective mathematical programming.
- **Key Evidence:** Proves that the conventional weighting method fails to generate unsupported efficient solutions on non-convex integer Pareto fronts. Eliminates weakly efficient solutions by transforming inequalities into equalities with scaled slack variables.
- **Project Role:** Primary mathematical algorithm for generating exact Pareto fronts between Makespan, Energy Cost, and Peak Demand.

### Summary 3.4: Catanzaro et al. (2023) — [P04]
- **Verified Scope:** Survey of 135+ papers on job scheduling under Time-of-Use tariffs published between 2011 and 2022.
- **Critical Gap Discovered:** "Peak" refers exclusively to on-peak tariff hours. Across all 135+ reviewed papers, **not a single paper models maximum power limits, peak-power minimization, or demand-charge rates**.
- **Project Role:** Establishes the authoritative academic gap justifying the investigation of peak-aware versus energy-cost-only scheduling.

### Summary 3.5: Dai et al. (2019) — [P05]
- **Verified Model:** Flexible Job Shop Scheduling Problem with multi-AGV transportation and comprehensive energy components ($SE + PE + IE + TE + AE$).
- **Key Evidence:** Proves that idle energy ($IE$) and facility auxiliary energy ($AE$) scale directly with total schedule makespan ($C_{\max}$).
- **Project Role:** Provides the mathematical structure for idle power accumulation across multi-machine workcells.

### Summary 3.6: Sung & Kwon (2026) — [P06]
- **Verified Model:** Identical parallel machine scheduling under time-varying electricity prices and explicit demand charges.
- **Key Evidence:**
  1. Formulates interval-averaged peak power demand over fixed utility billing windows (Eq. 1f, 4c).
  2. Formulates the dual-component economic objective: $\min TEC = ec + DCR \cdot p_{\max}$ (Eq. 4a).
  3. Derives the Peak-Energy Curve (PEC) showing that marginal demand charge rate is $dcr = -f'(x)$.
- **Project Role:** Foundational source for our project's peak demand constraints and demand-charge economic objective.

### Summary 3.7: Mavrotas & Florios (2013) — [P07]
- **Verified Method:** AUGMECON2 exact multi-objective integer programming algorithm.
- **Key Evidence:** Introduces the bypass coefficient $b = \lfloor S_2 / step_2 \rfloor$ to skip redundant solver runs when constraints are non-binding. Proves exact Pareto set generation for integer objectives.
- **Project Role:** Acceleration algorithm for computing the 3D Pareto frontier ($C_{\max}$, Energy Cost, Peak Demand).

### Summary 3.8: Fang et al. (2013) — [P08]
- **Audit Note:** Full text unavailable locally. Marked pending. No mathematical formulations or claims are adopted from this paper until a verified local copy is inspected.

### Summary 3.9: Moon et al. (2013) — [P09]
- **Verified Problem:** Unrelated parallel machine scheduling ($R || C_{\max} \cdot PC + EC$) under Korean 3-tier ToU tariffs.
- **Formulation Audit:** Incorporates machine-dependent power heterogeneity ($c_i$). Full-text audit revealed two major formulation defects in the paper: Eq. (2) defines makespan incorrectly as machine workload sum, and the model omits the machine non-overlap constraint $\sum_j x_{ijk} \le 1$.
- **Project Role:** Provides precedent for machine-power heterogeneity ($P_{im}$); warns against repeating their formulation errors.

### Summary 3.10: Aghelinejad et al. (2019) — [P10]
- **Verified Problem:** Single machine scheduling with multi-state energy consumption ($ON, OFF, Idle, Ton, Toff$) under ToU tariffs.
- **Theoretical Contribution:** Proves that while fixed-sequence problems are solvable in polynomial time $O(P \cdot T^2)$, the general problem without fixed sequence under ToU tariffs is **NP-hard in the strong sense** (via 3-PARTITION reduction).
- **Project Role:** Theoretical justification for using mathematical programming solvers and branch-and-cut / CP-SAT methods.

---

## 4. Literature-to-Model Traceability Table

| Proposed Model Component | Source Paper(s) | Original Equation / Page | Original Assumptions | Directly Transferable? | Required Adaptation for Project | Evidence Status |
|---|---|---|---|---|---|---|
| **Job non-preemption & start time** | Sung & Kwon (2026) [P06]<br>Catanzaro et al. (2023) [P04] | Eq. (1c), p. 5 [P06]<br>Eq. (1), p. 1093 [P04] | Deterministic integer processing times; single start | **Yes** | Standard time-indexed start variable $x_{j,t} \in \{0, 1\}$ | Fully verified |
| **Machine capacity / non-overlap** | Sung & Kwon (2026) [P06]<br>Catanzaro et al. (2023) [P04] | Eq. (1e), p. 5 [P06]<br>Eq. (1), p. 1093 [P04] | Identical parallel machines in [P06]; single machine in [P04] | **With Adaptation** | Must reintroduce machine index $m$ to enforce $\sum_{j} x_{j,m,t} \le 1$ for heterogeneous machines | Fully verified |
| **Machine-power heterogeneity** | Moon et al. (2013) [P09]<br>Dai et al. (2019) [P05] | Eq. (3), p. 528 [P09]<br>Eq. (2), p. 146 [P05] | Machine-dependent power $c_i$; job-machine power $P_{ijk}$ | **Yes** | Formulate machine-specific power parameter $P_{jm}$ or $P_m$ | Fully verified |
| **Machine idle & transition states** | Mouzon et al. (2007) [P01]<br>Aghelinejad et al. (2019) [P10] | LMIP-MTCTEC, p. 4266 [P01]<br>Eq. (1)–(4), p. 3 [P10] | Single machine; known idle durations; state power hierarchy | **With Adaptation** | Formulate idle power tracking across parallel machines | Fully verified |
| **ToU energy consumption cost** | Sung & Kwon (2026) [P06]<br>Catanzaro et al. (2023) [P04]<br>Moon et al. (2013) [P09] | Eq. (1b), p. 5 [P06]<br>Eq. (2), p. 1093 [P04]<br>Eq. (3), p. 528 [P09] | Discretized time horizon; time-varying tariff vector $C_t$ | **Yes** | Use Karnataka KERC LT-5 / HT-2 tariff schedule (normal, peak, off-peak rates) | Fully verified |
| **Interval peak demand constraint** | Sung & Kwon (2026) [P06] | Eq. (1f), p. 5 [P06] | Fixed intervals $k \in K$ of length $L$; identical machines | **With Adaptation** | Expand to heterogeneous machine power: $\frac{1}{L} \sum_{k} \sum_{m} P_m \le \bar{P}_{\max}$ | Fully verified |
| **Monetary demand-charge objective** | Sung & Kwon (2026) [P06] | Eq. (4a), p. 10 [P06] | Total electricity cost $\min (ec + DCR \cdot p_{\max})$ | **Yes** | Directly transferable; apply KERC demand charge rates ($\text{Rs.}/kW$ or $\text{Rs.}/kVA$) | Fully verified |
| **Multi-objective exact Pareto generation** | Mavrotas (2009) [P03]<br>Mavrotas & Florios (2013) [P07] | AUGMECON: p. 459 [P03]<br>AUGMECON2: pp. 9657–9658 [P07] | General MOMIP/MOCO; payoff table via lexicographic optimization | **Yes** | Implement AUGMECON2 with bypass coefficient in OR-Tools / CP-SAT | Fully verified |

---

## 5. Research-Gap Assessment

### 5.1. Findings from Full-Text Screening
1. **The Peak Demand Gap in ToU Scheduling:**  
   Catanzaro et al.'s (2023) comprehensive EJOR survey proves that the mainstream scheduling literature has concentrated heavily on **energy-cost-only** scheduling under ToU tariffs, completely ignoring peak demand charges.
2. **The Heterogeneity & Idle Power Gap in Demand-Charge Scheduling:**  
   Sung & Kwon (2026) introduces the state-of-the-art demand-charge formulation, but restricts the model to identical machines, ignores machine-power heterogeneity, and omits idle/standby power states.
3. **Absence of Physical Hardware Validation in Analyzed Corpus:**  
   Across all 222+ articles synthesized in the authoritative reviews of Gahm et al. (2016) (87 papers) and Catanzaro et al. (2023) (135+ papers), as well as the 9 primary full-text PDFs in this study, experimental evaluation is conducted exclusively via numerical simulation. None of these studies report physical hardware-in-the-loop validation, sensor-instrumented power bus measurement, or validation against electrical transients. Physical testbed validation addresses this documented simulation gap.

### 5.2. Defensible Core Research Question
*Under what combinations of demand-charge intensity ($DCR$), time-of-use tariff variation (peak-to-off-peak ratio), workload intensity (tightness of due dates / job density), and machine-power heterogeneity does peak-aware production scheduling provide a statistically significant economic benefit over energy-cost-only scheduling?*

---

## 6. Decision Log

| Date | Decision / Correction | Evidence | Consequence for Project |
|---|---|---|---|
| 2026-10-18 | Correct Moon et al. (2013) classification | Abstract / author postprint analysis | Changed problem class from Job Shop to Unrelated Parallel Machine ($R$). |
| 2026-10-18 | Correct Dai et al. (2019) page numbers | Publisher metadata check | Corrected page numbers from 263–276 to 143–157 (*RCIM* Vol. 59). |
| 2026-10-18 | Separate peak power from demand charges | Initial literature audit | Enforced strict tripartite distinction: peak constraint vs peak objective vs demand charge. |
| 2026-10-26 | Identify Catanzaro et al. (2023) peak omission | Full-text extraction of 19 pages | Confirmed zero coverage of peak power limits or demand charges across 135+ ToU scheduling papers. |
| 2026-10-26 | Adopt Sung & Kwon (2026) peak demand equations | Full-text extraction of Applied Energy paper | Formally adopted Eq. (1f) for interval peak demand and Eq. (4a) for dual-component economic objective. |
| 2026-10-26 | Uncover Moon et al. (2013) formulation errors | Full-text mathematical analysis of p. 528 | Identified defective makespan equation (Eq. 2) and missing non-overlap constraint; flagged to avoid in our formulation. |
| 2026-10-26 | Adopt AUGMECON2 exact method | Full-text extraction of Mavrotas & Florios (2013) | Selected AUGMECON2 with bypass coefficient as primary multi-objective solver framework. |
| 2026-10-26 | Mark Fang et al. (2013) as pending | Workspace PDF inventory audit | Marked full text unavailable; avoided inventing equations or claims pending physical document retrieval. |
| 2026-10-26 | Complete pre-modelling literature audit | Comprehensive verification report `literature_audit_before_model_v1.md` | Verified Sung & Kwon (2026) Eq. (4a) monetary objective and Eq. (1f) peak constraint; confirmed restriction to identical machines and processing power only. |
| 2026-10-26 | Correct document source for Mavrotas & Florios (2013) | Textual audit of local PDF metadata | Identified local PDF as MPRA Paper No. 105034 preprint (PDF pp. 7–8 vs journal pp. 9657–9658); verified bypass logic $b = \lfloor S_2 / step_2 \rfloor$. |
| 2026-10-26 | Correct dual pagination for Mouzon et al. (2007) | Textual audit of local manuscript PDF | Verified manuscript p. 7 (PDF p. 9) for breakeven threshold $S$, manuscript p. 23 (PDF p. 25) for LMIP-MTCTEC, matching journal pp. 4253 and 4266. |
| 2026-10-26 | Refine physical validation gap scope | Textual audit of Gahm (2016) and Catanzaro (2023) | Restricted claim to the 222+ reviewed survey articles and 9 primary PDFs, avoiding unsupported universal generalizations. |
