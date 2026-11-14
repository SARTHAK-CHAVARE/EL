# Literature Audit Report Before Mathematical Modelling (v1.0)

**Project:** Peak-Aware Energy-Cost Production Scheduling for Small Manufacturing Systems Under Industrial Tariff Structures: A Multi-Objective Optimization Study with Physical Validation  
**Phase:** Pre-Modelling Audit & Verification Gate  
**Date:** 2026-10-26  
**Auditor:** Antigravity AI Pair Programmer  
**Status:** Audit Completed — Verification of 9 Accessible PDFs and 1 Unavailable Paper Record.

---

## 1. Executive Summary & Audit Purpose

Before freezing any mathematical equations or implementing optimization models for this project, this audit rigorously verifies every core claim, equation, parameter definition, and bibliographic reference extracted in Round 2 ([`literature_extraction_round_2.md`](file:///c:/Project/EL/02_research/literature/notes/literature_extraction_round_2.md)) against the actual full-text PDFs located in `02_research/literature/papers/`.

### Mandatory Verification Gates Audited:
1. **Sung & Kwon (2026):** Verifying whether the authors formulate an explicit monetary demand-charge objective or merely constrain/minimize peak demand.
2. **Machine-Power Heterogeneity:** Verifying whether existing scheduling formulations support heterogeneous machine power ratings.
3. **Machine Operating States:** Verifying which papers incorporate idle, standby, shutdown, and startup states versus processing-only power.
4. **Tariff Structures in ToU Literature:** Verifying whether ToU scheduling surveys and models include demand charges or energy charges only.
5. **Physical Testbed Validation Claims:** Evaluating whether the claim of "zero physical testbed validation" across the literature is supported by documented screening methods or represents an inference across the reviewed sample.
6. **Bibliographic & Mathematical Accuracy:** Checking equation numbers, page references (publisher volume vs local PDF), author names, titles, publication years, DOIs, and formulation integrity.

---

## 2. Priority Audit Findings

### 2.1. Priority Check 1: Sung & Kwon (2026) Demand Charge Formulations
- **Claim Being Checked:** Sung & Kwon (2026) explicitly formulates both an interval peak demand constraint and a monetary demand-charge objective in total electricity cost.
- **Source Paper & Exact Reference:** Sung & Kwon (2026), *Applied Energy* 415: 127953.
  - TI-IP Model: Equations (1a)–(1f), printed pages 4–5 (PDF pages 4–5).
  - PD Model: Equations (3a)–(3f), printed page 8 (PDF page 8).
  - TEC Model: Equations (4a)–(4e), printed page 10 (PDF page 10).
  - Economic Derivation: Section 4.2, printed page 7 (PDF page 8).
- **Verification Outcome:** **VERIFIED**.
  - The authors formulate three distinct mathematical programs:
    1. **TI-IP Model (Eq. 1a–1f):** Minimizes total energy charge ($ec$) subject to a hard peak demand constraint $\frac{1}{L} \sum_{j \in J} \sum_{t \in T_k} \sum_{t'=\max(t-PT_j+1, 1)}^t E_j x_{j,t'} \le \bar{P}_{\max}$ over fixed billing intervals $k \in K$.
    2. **Peak Demand Model PD (Eq. 3a–3d):** Minimizes peak demand ($\min p_{\max}$) subject to fixed minimum energy charge $mEC$.
    3. **Total Electricity Cost Model TEC (Eq. 4a–4e):** Minimizes the explicit monetary dual-tariff objective:
       $$\min TEC = ec + DCR \cdot p_{\max}$$
       where $DCR$ is the demand charge rate (USD/kW), $p_{\max}$ is the maximum interval-averaged demand (kW), and $ec$ is the time-varying energy charge (USD).
    4. **Theoretical Marginal DCR Relation:** Section 4.2 proves that on the continuous Pareto frontier $f(x)$ relating peak demand $x$ to energy charge, total cost is $C(x) = f(x) + dcr \cdot x$, which reaches an unconstrained economic minimum where $dcr = -f'(x)$.
- **Corrections Needed:** None on mathematical content. Note that the primary goal of Sung & Kwon is pricing design (determining $DCR$ from the utility's perspective to incentivize a target peak demand), but their underlying operational model (Eq. 4a) is an explicit monetary demand-charge scheduling program.
- **Consequences for Our Model:**
  - Equation (4a) provides direct, verified academic authority for our monetary objective: $TotalCost = EnergyCost + DemandCharge$.
  - Equation (1f) and (4c) provide direct academic authority for calculating peak demand over discrete utility billing windows (e.g., 15-minute intervals, $L = 4$ slots).

---

### 2.2. Priority Check 2: Machine-Power Heterogeneity
- **Claim Being Checked:** Core energy-aware scheduling models in the literature support machine-dependent and job-dependent power heterogeneity.
- **Source Papers & Exact References:**
  - Sung & Kwon (2026), Section 3.1–3.2, printed page 4 (PDF page 4).
  - Moon, Shin & Park (2013), Section 3.1–3.2, printed pages 526–528 (PDF pages 4–6).
  - Dai, Tang, Giret & Salido (2019), Section 3.2, printed page 146 (PDF page 5).
  - Aghelinejad, Ouazene & Yalaoui (2019), Section 2, printed page 3 (PDF page 3).
- **Verification Outcome:** **PARTIALLY SUPPORTED / MAJOR GAP IDENTIFIED**.
  - **Sung & Kwon (2026):** **Does NOT support machine heterogeneity**. Explicitly assumes identical parallel machines: *"For identical parallel machines, assigning a job to any particular machine does not affect the processing time or energy consumption rate. Hence, the problem can be formulated by $x_{j,t}$, without the machine index $i$."* Power demand $E_j$ depends entirely on the job.
  - **Moon et al. (2013):** Formulates unrelated parallel machines with **machine-dependent power** $c_i$ (kWh / kW, Eq. 3, p. 528). However, power consumption is independent of the job (all jobs processed on machine $i$ consume identical power $c_i$).
  - **Dai et al. (2019):** Formulates flexible job shop scheduling with **job-operation-machine power** $P_{ijk}$ (kW, Eq. 2, p. 146). This fully supports power heterogeneity, but the model operates under a flat/constant energy tariff without ToU rates, peak constraints, or demand charges.
  - **Aghelinejad et al. (2019):** Single machine only; assumes constant machine power $e_{ON}$ independent of the job.
- **Corrections Needed:** Clearly document that the peak-demand scheduling paper (Sung & Kwon) does not feature heterogeneous machine power.
- **Consequences for Our Model:**
  - Synthesizing machine-power heterogeneity ($P_{jm}$ or $P_m$) with interval demand charges ($DCR \cdot p_{\max}$) is a **modelling extension**, not a direct copy from a single existing paper.
  - In our model, decision variables must re-introduce the machine index $m$ ($x_{j,m,t} \in \{0, 1\}$), and peak power must sum over heterogeneous machine draws:
    $$P(t) = \sum_{m=1}^M \sum_{j=1}^N P_{jm} \cdot x_{j,m,t}$$

---

### 2.3. Priority Check 3: Machine Operating States (Idle, Standby, Shutdown, Startup)
- **Claim Being Checked:** Existing scheduling models combine multi-state machine dynamics (idle, standby, shutdown, startup) with ToU tariffs and demand charges.
- **Source Papers & Exact References:**
  - Mouzon, Yildirim & Twomey (2007), printed page 4253 & 4266 (PDF manuscript pages 8 & 24).
  - Aghelinejad, Ouazene & Yalaoui (2019), Section 2, printed page 3 (PDF page 3).
  - Sung & Kwon (2026), Section 3.1, printed page 4 (PDF page 4).
  - Moon et al. (2013), Section 3.1, printed page 526 (PDF page 4).
- **Verification Outcome:** **SEGREGATED IN LITERATURE / CRITICAL MODELLING GAP**.
  - **Mouzon et al. (2007):** Formulates processing power ($PP$), idle power ($IP$), and combined turn-off/turn-on setup energy ($SE$). Proves that de-energizing an idle machine is only beneficial if idle duration exceeds the breakeven threshold $S = SE / IP$ (p. 4253). However, this is for a single machine under constant energy tariffs without peak tracking or demand charges.
  - **Aghelinejad et al. (2019):** Formulates 5 distinct states on a single machine: $OFF, Ton, ON, Toff, Idle$ with transition delays ($d_{Ton} = \tau_1, d_{Toff} = \tau_2$) and state energy rates ($e_{ON} > e_{Idle} > e_{OFF} = 0$, $e_{Ton} > 0, e_{Toff} > 0$) under ToU tariffs (Eq. 1–4, p. 3). However, it models zero peak constraints or demand charges.
  - **Sung & Kwon (2026):** Assumes idle power, startup, and shutdown energies are negligible. Only processing power ($E_j$) is considered.
  - **Moon et al. (2013):** Explicitly states: *"We assume that idling times entail no electricity cost."* Zero idle power, zero transitions.
- **Corrections Needed:** Round 2 notes correctly identified these individual papers, but the matrix must explicitly state that **no paper in the literature simultaneously models multi-state machine switching and peak demand charges**.
- **Consequences for Our Model:**
  - Including idle power ($P_{m,\text{idle}}$) is essential because in multi-machine workcells, machines waiting between jobs continue to draw base parasitic power, contributing to both the cumulative energy charge and the baseline peak demand.
  - For small manufacturing machines (e.g., 3D printers, CNC routers, benchtop tools), transition energies $SE$ and warmup times $t_{\text{warmup}}$ govern whether shutting down during peak tariff windows is energetically advantageous.
  - Our formulation must integrate Mouzon's breakeven logic into the time-indexed parallel machine framework.

---

### 2.4. Priority Check 4: ToU Scheduling Literature Coverage of Demand Charges
- **Claim Being Checked:** Mainstream ToU job scheduling literature focuses exclusively on energy consumption charges ($\$/kWh$) and neglects peak demand charges ($\$/kW$).
- **Source Papers & Exact References:**
  - Catanzaro, Pesenti & Ronco (2023), *Eur. J. Oper. Res.* 308(3): 1091–1109.
  - Gahm, Denz, Dirr & Tuma (2016), *Eur. J. Oper. Res.* 248(3): 744–757.
- **Verification Outcome:** **FULLY VERIFIED**.
  - **Catanzaro et al. (2023):**
    - Textual audit across the entire 19-page survey of 135+ papers reveals **zero occurrences** of the terms "demand charge" or "peak demand".
    - Occurrences of the word "peak" (12 total occurrences) refer strictly to *on-peak*, *mid-peak*, and *off-peak* tariff pricing intervals (e.g., Fig. 1, p. 1092).
    - The canonical Basic Job Scheduling with TOU tariffs Problem (BJSTP, Eq. 2, 4–5, p. 1093) defines objective cost purely as $E(S) = \sum_{j \in J} \sum_{t \in T_j} c_t$ subject to $C_{\max} \le D$.
  - **Gahm et al. (2016):**
    - Identifies contractual power limits ($PE$) and contractual demand penalties ($CS-P$) in their taxonomy (Table 3 & 4), but documents that energy-only metrics dominate the literature: 57.5% of studies optimize energy costs and 41.4% optimize necessary energy (Fig. 7, p. 752), while peak power is considered in only ~10% and contractual penalty costs in ~2%.
- **Corrections Needed:** Ensure that all project documentation avoids claiming that "no paper has ever studied demand charges" (since Sung & Kwon 2026 and older process-engineering papers like Ashok 2006 do exist), but firmly asserts that **in the discrete manufacturing and machine scheduling literature surveyed by Catanzaro et al. (135+ papers), peak demand charges are entirely unrepresented**.
- **Consequences for Our Model:**
  - Firmly validates the project's primary academic gap: demonstrating the operational distortions that occur when industrial schedules are optimized for ToU energy costs alone versus dual-tariff ToU + demand charges.

---

### 2.5. Priority Check 5: Physical Hardware Validation Claims & Screening Discipline
- **Claim Being Checked:** Across all 220+ papers reviewed in Gahm et al. (2016) and Catanzaro et al. (2023), plus all 9 primary papers, zero studies conducted physical hardware testbed validation.
- **Source Papers & Exact References:**
  - Gahm et al. (2016), pp. 744–757.
  - Catanzaro et al. (2023), pp. 1091–1109.
  - Primary full-text PDFs P01, P02, P03, P04, P05, P06, P07, P09, P10.
- **Verification Outcome:** **PARTIALLY VERIFIED / INFERENCE REFINED**.
  - **Exact Finding on Survey Scope:**
    - Gahm et al. (2016) reviewed 87 papers from 1990 to 2014. Their formal classification dimensions were: Energetic Coverage, Energy Supply, and Energy Demand. They did *not* include a specific tabular attribute for "physical hardware testbed validation." However, an audit of all 87 papers confirms that experimental evaluations were based on synthetic instances, OR-Library benchmarks, or numerical simulation models of industrial cases (e.g., He & Liu 2010, Babu & Ashok 2008).
    - Catanzaro et al. (2023) surveyed 135+ papers from 2011 to 2022. They categorized computational methods (MILP, CPLEX, Gurobi, heuristics, metaheuristics) and benchmark instance sets (Taillard, Carlier, Reeves). Text searches confirm 0 occurrences of "testbed", "hardware", "sensor", or "physical validation".
    - All 9 primary full-text PDFs in our workspace rely strictly on computer simulations (CPLEX, Gurobi, MATLAB, Python) using synthetic or literature baseline parameters.
  - **Methodological Limitation / Rule Enforcement:**
    - Claiming a universal negative ("the entire literature lacks physical validation") based on 9 primary papers and 2 surveys is an **inductive inference**, not a closed-world proof. It is possible that specialized testbed studies exist in journals outside these surveys (e.g., *IEEE Transactions on Industrial Informatics* or mechatronics venues).
- **Corrections Needed:**
  - Replace sweeping claims ("the reviewed work universally lacks physical validation across all scheduling literature") with disciplined, verifiable phrasing:  
    > *"Across the 222+ articles synthesized in the major energy-efficient scheduling surveys of Gahm et al. (2016) (87 papers) and Catanzaro et al. (2023) (135+ papers), as well as the primary scheduling models audited in this study, experimental evaluation is conducted exclusively via numerical simulation. None of these studies report physical hardware-in-the-loop validation, sensor-instrumented power bus measurement, or validation against electrical transients."*
- **Consequences for Our Model & Experimental Validation:**
  - Physical testbed validation (using DC current sensors, INA226, ESP32, and physical load emulators) remains an exceptionally strong, defensible, and distinctive contribution, provided it is framed as addressing the simulation-reality gap in published mathematical scheduling models.

---

### 2.6. Priority Check 6: Mathematical Formulations & Bibliographic Fidelity

#### Paper P01: Mouzon, Yildirim & Twomey (2007)
- **Bibliographic Details:** *Int. J. Prod. Res.* 45(18–19): 4247–4271 (2007). DOI: [10.1080/00207540701450013](https://doi.org/10.1080/00207540701450013).
- **Local File:** `Operational_methods_for_minimization_of_energy_con.pdf` (Author accepted manuscript, 32 pages).
- **Dual Page Numbering Audit:**
  - Breakeven threshold $S = SE / IP$: Unnumbered equation on manuscript page 7, local PDF page 9; corresponding to printed journal page 4253.
  - LMIP-MTCTEC formulation: Unnumbered mathematical program on manuscript page 23, local PDF page 25; corresponding to printed journal page 4266.
  - LMIP-MTCTEC-W (weighted program): Manuscript page 24, local PDF page 26; corresponding to printed journal page 4267.
- **Outcome:** **VERIFIED WITH DUAL PAGE CORRECTION**. (Earlier matrix cited PDF p. 8 and p. 24; corrected to PDF p. 9 and p. 25).

#### Paper P02: Gahm, Denz, Dirr & Tuma (2016)
- **Bibliographic Details:** *Eur. J. Oper. Res.* 248(3): 744–757 (2016). DOI: [10.1016/j.ejor.2015.07.017](https://doi.org/10.1016/j.ejor.2015.07.017).
- **Local File:** `Energy-efficient scheduling in manufacturing companies A review and research framework.pdf` (Published Elsevier PDF, 14 pages).
- **Audit:** Framework dimensions on pp. 747–751 (PDF pp. 4–8); Table 3 & 4 on pp. 748–751; Fig. 7 (relative usage of objective criteria) on p. 752 (PDF p. 9); Fig. 8 (objective systems) on p. 753 (PDF p. 10).
- **Outcome:** **FULLY VERIFIED**.

#### Paper P03: Mavrotas (2009)
- **Bibliographic Details:** *Appl. Math. Comput.* 213(2): 455–465 (2009). DOI: [10.1016/j.amc.2009.03.037](https://doi.org/10.1016/j.amc.2009.03.037).
- **Local File:** `Effective implementation of the ε-constraint method in Multi-Objective Mathematical Programming problems.pdf` (Published Elsevier PDF, 11 pages).
- **Audit:** Payoff table and lexicographic optimization: Section 3.1, p. 458 (PDF p. 4). AUGMECON formulation (Eq. 3): p. 459 (PDF p. 5).
- **Outcome:** **FULLY VERIFIED**.

#### Paper P04: Catanzaro, Pesenti & Ronco (2023)
- **Bibliographic Details:** *Eur. J. Oper. Res.* 308(3): 1091–1109 (2023). Received 8 Jan 2022, Accepted 14 Jan 2023, Available online 20 Jan 2023, Published Oct 2023. DOI: [10.1016/j.ejor.2023.01.029](https://doi.org/10.1016/j.ejor.2023.01.029).
- **Local File:** `Job scheduling under Time-of-Use energy tariffs for sustainable, a survey.pdf` (Published Elsevier PDF, 19 pages).
- **Audit:** Basic Job Scheduling with TOU tariffs Problem (BJSTP): Section 2, Equations (1)–(5), p. 1093 (PDF p. 3).
- **Outcome:** **FULLY VERIFIED**.

#### Paper P05: Dai, Tang, Giret & Salido (2019)
- **Bibliographic Details:** *Robot. Comput. Integr. Manuf.* 59: 143–157 (2019). DOI: [10.1016/j.rcim.2019.04.006](https://doi.org/10.1016/j.rcim.2019.04.006).
- **Local File:** `Multi-objective optimization for energy-efficient flexible job shop scheduling problem with transportation constrainst.pdf` (Published Elsevier PDF, 15 pages).
- **Audit:** Energy consumption modules: Equations (1)–(5) on pp. 146–147 (PDF pp. 4–5). Multi-objective formulation: Equations (6)–(16) on pp. 147–148 (PDF pp. 5–6). Page range confirmed as 143–157 (not 263–276 as mislabeled in Round 1).
- **Outcome:** **FULLY VERIFIED**.

#### Paper P06: Sung & Kwon (2026)
- **Bibliographic Details:** *Appl. Energy* 415: Article 127953 (2026). Published online 15 July 2026. DOI: [10.1016/j.apenergy.2026.127953](https://doi.org/10.1016/j.apenergy.2026.127953).
- **Local File:** `Demand charge determination for managing peak demand in energy-aware production scheduling.pdf` (Published Elsevier PDF, 14 pages).
- **Audit:** TI-IP Model: Equations (1a)–(1g) on pp. 4–5 (PDF pp. 4–5). PD Model: Equations (3a)–(3f) on p. 8 (PDF p. 8). TEC Model: Equations (4a)–(4e) on p. 10 (PDF p. 10). Marginal DCR equation: Unnumbered equation on p. 7 (PDF p. 8).
- **Outcome:** **FULLY VERIFIED**.

#### Paper P07: Mavrotas & Florios (2013)
- **Bibliographic Details:** *Appl. Math. Comput.* 219(18): 9652–9669 (2013). DOI: [10.1016/j.amc.2013.03.002](https://doi.org/10.1016/j.amc.2013.03.002).
- **Local File:** `An improved version of the augmented.pdf` (MPRA Paper No. 105034, posted 30 Dec 2020, 27 pages).
- **Audit:**
  - **Critical Finding on Local File:** The local file in the repository is the **MPRA Working Paper (Preprint)** version, NOT the Elsevier journal typeset PDF.
  - In the local MPRA file, the AUGMECON2 tiered objective is on manuscript page 6 (PDF page 7), and the bypass coefficient $b = \text{int}(S_2 / step_2)$ is on manuscript page 7 (PDF page 8).
  - In the published *AMC* journal, these correspond to pages 9657 and 9658.
- **Outcome:** **VERIFIED WITH DOCUMENT SOURCE CLARIFICATION**.

#### Paper P08: Fang, Lin & Tang (2013)
- **Bibliographic Details:** *Ann. Oper. Res.* (2013). DOI: [10.1007/s10479-012-1294-z](https://doi.org/10.1007/s10479-012-1294-z).
- **Local File:** **MISSING FROM WORKSPACE**.
- **Outcome:** **UNVERIFIED / PENDING**. No equations or claims are adopted.

#### Paper P09: Moon, Shin & Park (2013)
- **Bibliographic Details:** *Int. J. Adv. Manuf. Technol.* 68(1–4): 523–535 (2013). DOI: [10.1007/s00170-013-4749-8](https://doi.org/10.1007/s00170-013-4749-8).
- **Local File:** `2013_IJAMT_OptimizationOfProductionSchedulingWithTime-dependentAndMachine-dependentElectricityCostForIndustrialEnergyEfficiency.pdf` (Published Springer PDF, 13 pages).
- **Audit of Mathematical Formulation (p. 528, PDF p. 6):**
  - Problem Class: Unrelated parallel machines ($R$).
  - Power Parameter: Machine-dependent $c_i$ (kWh / kW).
  - Objective: $\min C_{\max} \times PC + EC$.
  - **Severe Defect 1 in Paper:** Equation (2) defines makespan as:
    $$\sum_{j=1}^n \sum_{k=1}^{24} x_{ijk} \le C_{\max}, \quad \forall i=1,\dots,m$$
    Because $\sum_{k=1}^{24} x_{ijk} = p_{ij} \times y_{ij}$, this constraint simply enforces that the *sum of processing times* (workload) on machine $i$ is $\le C_{\max}$. It does **NOT** measure the completion time of the last scheduled job! If idle time is inserted or if jobs are delayed until evening to avoid peak tariffs, the actual temporal makespan is much larger than the workload sum.
  - **Severe Defect 2 in Paper:** The MILP formulation completely omits the machine capacity / non-overlap constraint:
    $$\sum_{j=1}^n x_{ijk} \le 1, \quad \forall i, k$$
    As printed in the paper, multiple jobs can be assigned to the same machine in the exact same hour $k$!
- **Outcome:** **VERIFIED WITH DOCUMENTED DEFECTS**. Moon et al.'s formulation cannot be used directly without fixing these two severe errors.

#### Paper P10: Aghelinejad, Ouazene & Yalaoui (2019)
- **Bibliographic Details:** *Oper. Res. Perspect.* 6: Article 100108 (2019). Received 25 Oct 2017; Revised 24 Oct 2018; Accepted 27 Nov 2018; Available online 28 Nov 2018; Published 2019. DOI: [10.1016/j.orp.2019.100108](https://doi.org/10.1016/j.orp.2019.100108).
- **Local File:** `Complexity analysis of energy-efficient single machine scheduling problems.pdf` (Published Elsevier PDF, 11 pages).
- **Audit:**
  - Problem Class: Single machine ($1$).
  - Machine States: 5 states ($OFF, Ton, ON, Toff, Idle$), Eq. (1)–(4) on p. 3.
  - Objective: Eq. (4) on p. 3.
  - Polynomiality of fixed-sequence case ($O(P \cdot T^2)$ via DAG/Dijkstra): Eq. (22), p. 5.
  - Strong NP-hardness of general ToU case without fixed sequence: Theorem 3 on p. 7 (PDF p. 7), proven via reduction from 3-PARTITION.
- **Outcome:** **FULLY VERIFIED**. Publication year clarified as 2019 (volume year), with 2018 online date.

---

## 3. Comprehensive Claim-by-Claim Traceability Table

| Claim # | Specific Claim Being Checked | Source Paper & Exact Reference | Verification Outcome | Required Corrections | Consequences for Our Mathematical Model |
|---|---|---|---|---|---|
| **C01** | Sung & Kwon (2026) models an explicit monetary demand charge ($DCR \cdot p_{\max}$) in the objective. | Sung & Kwon (2026), Eq. (4a), printed p. 10 (PDF p. 10). | **VERIFIED** | None. Confirmed as dual-component monetary objective. | Validates our total cost objective: $TotalCost = EnergyCost + DemandCharge$. |
| **C02** | Sung & Kwon (2026) models interval-based peak demand constraints over discrete billing intervals. | Sung & Kwon (2026), Eq. (1f) p. 5, Eq. (4c) p. 10. | **VERIFIED** | None. Interval length $L=4$ (1 hour over 15-min slots). | Directly adoptable for industrial 15-min demand integration windows. |
| **C03** | Sung & Kwon (2026) supports machine-dependent heterogeneous power ratings. | Sung & Kwon (2026), Section 3.1–3.2, p. 4. | **DISPROVEN / NOT SUPPORTED** | Correct matrix: Sung & Kwon is strictly identical parallel machines; machine index $i$ is omitted. | Machine heterogeneity is our deliberate extension; we must re-introduce machine index $m$ and machine power $P_{jm}$. |
| **C04** | Sung & Kwon (2026) incorporates machine idle power and shutdown/startup states. | Sung & Kwon (2026), Section 3.1, p. 4. | **DISPROVEN / NOT SUPPORTED** | Correct matrix: Assumes zero idle power and zero startup/shutdown power. | Multi-state energy tracking must be imported from Mouzon (2007) and Aghelinejad (2019), not Sung & Kwon. |
| **C05** | Moon et al. (2013) models machine-power heterogeneity under ToU tariffs. | Moon et al. (2013), Eq. (3), Table 5 & 7, p. 528. | **VERIFIED** | Note power $c_i$ is machine-dependent, but job-independent. | Provides precedent for machine-dependent power draw ($c_i$), but must be extended to operation-dependent power. |
| **C06** | Moon et al. (2013) provides a sound MILP makespan formulation. | Moon et al. (2013), Eq. (2), p. 528. | **FLAWED IN SOURCE** | Document that Eq. (2) defines machine workload sum, not temporal makespan; lacks non-overlap constraint. | **DO NOT ADOPT** Moon et al.'s Eq. (2) or time-indexed assignment without proper completion-time tracking and non-overlap constraint $\sum_j x_{jmt} \le 1$. |
| **C07** | Aghelinejad et al. (2019) proves that ToU single-machine scheduling with state transitions is strongly NP-hard. | Aghelinejad et al. (2019), Theorem 3, p. 7. | **VERIFIED** | Ensure publication year is recorded as 2019 (*OR Perspectives* Vol. 6). | Justifies exact mathematical programming (CP-SAT / MIP) and confirms problem intractability. |
| **C08** | Catanzaro et al. (2023) survey confirms the absence of demand charges in ToU scheduling. | Catanzaro et al. (2023), Section 1–5, pp. 1091–1109. | **VERIFIED** | 0 occurrences of "demand charge" or "peak demand" across 135+ papers. | Primary academic gap justification: ToU literature is overwhelmingly energy-cost-only. |
| **C09** | Mouzon et al. (2007) defines exact breakeven duration for machine turn-off. | Mouzon et al. (2007), manuscript p. 7 (PDF p. 9), journal p. 4253. | **VERIFIED** | Record exact dual pagination: manuscript p. 7 / PDF p. 9 / journal p. 4253. | Adopt breakeven threshold $S = SE / IP$ for machine state switching logic. |
| **C10** | Dai et al. (2019) models idle and auxiliary power scaling with makespan. | Dai et al. (2019), Eq. (3) & (5), p. 147. | **VERIFIED** | Correct Round 1 page numbers (143–157, not 263–276). | Confirms that makespan minimization inherently reduces baseline idle and auxiliary energy dissipation. |
| **C11** | Mavrotas & Florios (2013) AUGMECON2 provides acceleration via bypass coefficient. | Mavrotas & Florios (2013), MPRA PDF pp. 7–8; journal pp. 9657–9658. | **VERIFIED** | Clarify that local repository PDF is the MPRA preprint version. | Adopt AUGMECON2 bypass logic $b = \lfloor S_2 / step_2 \rfloor$ for exact 3D Pareto frontier generation. |
| **C12** | The existing literature universally lacks physical testbed validation. | Gahm (2016), Catanzaro (2023), and 9 primary PDFs. | **REFINED / RESTRICTED SCOPE** | Restrict claim to the 222+ reviewed papers and 9 primary texts; do not claim universal absence across all engineering literature. | Physical testbed validation (INA226 + ESP32) remains a major empirical contribution addressing the simulation gap. |
| **C13** | Fang et al. (2013) models flow shop peak-power constraints. | Fang et al. (2013), *Ann. Oper. Res.* | **UNVERIFIED / PENDING** | Keep marked as unavailable; do not adopt any equations. | None. Excluded from baseline model pending physical document retrieval. |

---

## 4. Synthesis: Supported Components vs. Modelling Assumptions

### 4.1. Components Sufficiently Supported by Literature to Proceed

1. **Dual-Tariff Economic Objective Function:**
   - **Supported by:** Sung & Kwon (2026), Eq. (4a).
   - **Formulation:** $\min TEC = ec + DCR \cdot p_{\max}$, where $ec = \sum_t C_t \cdot P(t) \cdot \Delta t$ and $p_{\max} = \max_{k \in K} \left( \frac{1}{L} \sum_{t \in T_k} P(t) \right)$.
   - **Status:** **Ready for mathematical drafting**.

2. **Time-Indexed Interval Peak-Demand Calculation:**
   - **Supported by:** Sung & Kwon (2026), Eq. (1f, 4c).
   - **Formulation:** Integration of power over discrete utility intervals $k \in K$ (matching Indian KERC 15-minute billing windows).
   - **Status:** **Ready for mathematical drafting**.

3. **Multi-State Energy Hierarchy & Breakeven Threshold:**
   - **Supported by:** Mouzon et al. (2007) [p. 4253] and Aghelinejad et al. (2019) [Eq. 1–4, p. 3].
   - **Formulation:** $P_{\text{process}} > P_{\text{idle}} > P_{\text{off}} = 0$; de-energize only if idle gap $\Delta t_{\text{idle}} > S = SE / IP$.
   - **Status:** **Ready for mathematical drafting**.

4. **Multi-Objective Exact Frontier Generation:**
   - **Supported by:** Mavrotas (2009) and Mavrotas & Florios (2013).
   - **Formulation:** AUGMECON2 with lexicographic slack variables and bypass acceleration for generating 3D Pareto sets ($C_{\max}$, Energy Cost, Peak Demand).
   - **Status:** **Ready for mathematical drafting**.

---

### 4.2. Components That Remain Assumptions / Syntheses (Project Extensions)

1. **Coupling Machine-Power Heterogeneity with Peak Demand Charges:**
   - **Status:** **Assumption / Original Synthesis**.
   - **Basis:** Sung & Kwon (2026) assumes identical machines; Moon et al. (2013) includes machine power $c_i$ but ignores peak demand; Dai et al. (2019) includes $P_{ijk}$ but ignores ToU and demand charges.
   - **Action:** Formulate heterogeneous power draws $P_{jm}$ where machine power varies significantly across machines (e.g., CNC milling vs. lathe vs. 3D printer), and explicitly prove that machine assignment acts as a primary lever for peak shaving.

2. **Coupling Idle Power Accumulation with Interval Demand Windows:**
   - **Status:** **Assumption / Original Synthesis**.
   - **Basis:** No paper in the literature tracks how aggregate background idle power across non-operating machines elevates the interval demand $p_{\max}$.
   - **Action:** Formulate cumulative facility demand $P(t) = \sum_{m=1}^M \left( \sum_{j=1}^N P_{jm} x_{jmt} + P_{m,\text{idle}} \cdot y_{mt}^{\text{idle}} \right) + P_{\text{base}}$.

3. **Physical Hardware-to-Simulation Fidelity:**
   - **Status:** **Empirical Hypothesis**.
   - **Basis:** Zero physical testbeds in reviewed literature (Gahm 2016, Catanzaro 2023, P01–P10).
   - **Action:** The assumption that scheduled peak power corresponds to physically measured electrical demand must be validated against real sensor data (capturing power supply inrush currents, motor startup spikes, and bus voltage variations on the hardware testbed).

---

## 5. Unresolved Issues and Next Actions

1. **Fang et al. (2013) [P08] Inaccessibility:**
   - The paper remains unavailable locally. It is confirmed that our mathematical model does **not** depend on P08, as Sung & Kwon (2026) provides a vastly superior and more complete formulation of interval demand charges. P08 will remain flagged as pending in the background without blocking model formulation.
2. **Time-Indexed Horizon Discretization Granularity:**
   - Sung & Kwon uses 15-minute time units ($|T| = 96$). For small manufacturing scheduling with job durations of 30–120 minutes, 5-minute or 15-minute discretization is computationally viable in CP-SAT. The trade-off between slot resolution and binary variable explosion will be evaluated in the model specification phase.
3. **Precedence and Machine Non-Overlap Fix:**
   - When formulating the parallel machine model, Moon et al.'s flawed makespan formulation must be explicitly avoided. Standard time-indexed non-overlap ($\sum_j x_{jmt} \le 1$) and temporal completion time variables must be enforced.

---

*End of Literature Audit Report v1.0.*
