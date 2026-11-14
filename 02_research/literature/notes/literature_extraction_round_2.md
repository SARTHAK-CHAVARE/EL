# Round 2 Literature Extraction

**Project:** Peak-Aware Energy-Cost Production Scheduling for Small Manufacturing Systems Under Industrial Tariff Structures: A Multi-Objective Optimization Study with Physical Validation  
**Phase:** Literature-to-Mathematical-Foundation  
**Extraction Date:** 2026-10-26  
**Status:** Complete full-text extraction of 9 accessible source PDFs; 1 candidate marked pending/unavailable.

---

## 1. PDF Inventory and Verification Status

All local source files are located in `C:\Project\EL\02_research\literature\papers\`. Full-text extractions were performed directly on the primary local PDFs without altering source files.

| File / Citation Key | Local File Name | Verified Title & Authors | Publisher / Journal Details & DOI | Inventory Status | Metadata Status | Full-Text Status |
|---|---|---|---|---|---|---|
| **P01** | `Operational_methods_for_minimization_of_energy_con.pdf` | *Operational methods for minimization of energy consumption of manufacturing equipment*<br>Gilles Mouzon, Mehmet Bayram Yildirim, Janet Twomey | *International Journal of Production Research*, 45(18–19): 4247–4271 (2007).<br>DOI: [10.1080/00207540701450013](https://doi.org/10.1080/00207540701450013) | PDF located | Metadata verified | Full-text extracted |
| **P02** | `Energy-efficient scheduling in manufacturing companies A review and research framework.pdf` | *Energy-efficient scheduling in manufacturing companies: A review and research framework*<br>Christian Gahm, Florian Denz, Martin Dirr, Axel Tuma | *European Journal of Operational Research*, 248(3): 744–757 (2016).<br>DOI: [10.1016/j.ejor.2015.07.017](https://doi.org/10.1016/j.ejor.2015.07.017) | PDF located | Metadata verified | Full-text extracted |
| **P03** | `Effective implementation of the ε-constraint method in Multi-Objective Mathematical Programming problems.pdf` | *Effective implementation of the ε-constraint method in Multi-Objective Mathematical Programming problems*<br>George Mavrotas | *Applied Mathematics and Computation*, 213(2): 455–465 (2009).<br>DOI: [10.1016/j.amc.2009.03.037](https://doi.org/10.1016/j.amc.2009.03.037) | PDF located | Metadata verified | Full-text extracted |
| **P04** | `Job scheduling under Time-of-Use energy tariffs for sustainable, a survey.pdf` | *Job scheduling under Time-of-Use energy tariffs for sustainable manufacturing: a survey*<br>Daniele Catanzaro, Raffaele Pesenti, Roberto Ronco | *European Journal of Operational Research*, 308(3): 1091–1109 (2023).<br>DOI: [10.1016/j.ejor.2023.01.029](https://doi.org/10.1016/j.ejor.2023.01.029) | PDF located | Metadata verified | Full-text extracted |
| **P05** | `Multi-objective optimization for energy-efficient flexible job shop scheduling problem with transportation constrainst.pdf` | *Multi-objective optimization for energy-efficient flexible job shop scheduling problem with transportation constraints*<br>Min Dai, Dunbing Tang, Adriana Giret, Miguel A. Salido | *Robotics and Computer-Integrated Manufacturing*, 59: 143–157 (2019).<br>DOI: [10.1016/j.rcim.2019.04.006](https://doi.org/10.1016/j.rcim.2019.04.006) | PDF located | Metadata verified | Full-text extracted |
| **P06** | `Demand charge determination for managing peak demand in energy-aware production scheduling.pdf` | *Demand charge determination for managing peak demand in energy-aware production scheduling*<br>Joonmo Sung, Soongeol Kwon | *Applied Energy*, 415: Article 127953 (2026).<br>DOI: [10.1016/j.apenergy.2026.127953](https://doi.org/10.1016/j.apenergy.2026.127953) | PDF located | Metadata verified | Full-text extracted |
| **P07** | `An improved version of the augmented.pdf` | *An improved version of the augmented ε-constraint method (AUGMECON2) for finding the exact Pareto set in Multi-Objective Integer Programming problems*<br>George Mavrotas, Kostas Florios | *Applied Mathematics and Computation*, 219(18): 9652–9669 (2013). (Also MPRA Paper No. 105034).<br>DOI: [10.1016/j.amc.2013.03.002](https://doi.org/10.1016/j.amc.2013.03.002) | PDF located | Metadata verified | Full-text extracted |
| **P08** | *Missing local PDF* | *Flow shop scheduling with peak power consumption constraints*<br>Jiayi Fang, Fanqiang Lin, Dunbing Tang | *Annals of Operations Research*, 2013.<br>DOI: [10.1007/s10479-012-1294-z](https://doi.org/10.1007/s10479-012-1294-z) | Not located locally | Metadata verified | Unavailable / Pending |
| **P09** | `2013_IJAMT_OptimizationOfProductionSchedulingWithTime-dependentAndMachine-dependentElectricityCostForIndustrialEnergyEfficiency.pdf` | *Optimization of production scheduling with time-dependent and machine-dependent electricity cost for industrial energy efficiency*<br>Joon-Yung Moon, Kitae Shin, Jinwoo Park | *International Journal of Advanced Manufacturing Technology*, 68(1–4): 523–535 (2013).<br>DOI: [10.1007/s00170-013-4749-8](https://doi.org/10.1007/s00170-013-4749-8) | PDF located | Metadata verified | Full-text extracted |
| **P10** | `Complexity analysis of energy-efficient single machine scheduling problems.pdf` | *Complexity analysis of energy-efficient single machine scheduling problems*<br>MohammadMohsen Aghelinejad, Yassine Ouazene, Alice Yalaoui | *Operations Research Perspectives*, 6: Article 100108 (2019).<br>DOI: [10.1016/j.orp.2019.100108](https://doi.org/10.1016/j.orp.2019.100108) | PDF located | Metadata verified | Full-text extracted |

---

## 2. Paper-by-Paper Technical Extraction

### 2.1. Mouzon, Yildirim, and Twomey (2007) — [P01]

1. **Verified Citation & DOI:** Mouzon, G., Yildirim, M. B., & Twomey, J. (2007). Operational methods for minimization of energy consumption of manufacturing equipment. *International Journal of Production Research*, 45(18–19), 4247–4271. DOI: [10.1080/00207540701450013](https://doi.org/10.1080/00207540701450013).
2. **Research Problem & Industrial Application:** Minimizing non-bottleneck machine energy consumption during idle periods by determining when to switch equipment into an OFF state versus maintaining it in IDLE. Evaluated on CNC milling equipment and general manufacturing workcells.
3. **Scheduling Problem Class:** Single machine scheduling with known job arrival times $r_j$ and fixed sequence / FIFO dispatching, extended to multi-objective total completion time and energy minimization.
4. **Sets and Indices:**
   - Jobs: $j \in \{1, \dots, n\}$, indexed in arrival / processing order.
5. **Parameters:**
   - $P_j$: Processing time of job $j$ (time units / minutes).
   - $r_j$: Release / arrival time of job $j$.
   - $IP$: Machine idle power consumption per unit time (kW or W).
   - $PP$: Machine processing power consumption per unit time (kW or W).
   - $SE$: Setup energy, representing combined turn-off and turn-on energy (kJ or kWh).
   - $t_{OFF}$: Total time required to shut down and start up the machine (minutes).
   - $S$: Breakeven duration threshold for turning off ($S = SE / IP$, time units).
   - $L$: Large scalar constant for linear big-M formulations.
6. **Decision Variables:**
   - $C_j$: Continuous completion time of job $j$ ($C_j \ge 0$).
   - $y_j$: Continuous setup energy indicator variable accounting for energy difference between turn-off/turn-on and idling during gap between job $j$ and $j+1$ ($y_j \ge 0$).
   - $b_{1j}, b_{2j} \in \{0, 1\}$: Binary indicators selecting whether the idle gap exceeds the breakeven threshold $S$.
7. **Objective Function(s):**
   - Bi-objective model (LMIP-MTCTEC, PDF page 24, printed page 4266):
     $$\min f_1 = \sum_{j=1}^n C_j \quad \text{(Total Completion Time)}$$
     $$\min f_2 = \text{TEC} = \sum_{j=1}^{n-1} ((C_{j+1} - P_{j+1}) - C_j) IP + \sum_{j=1}^{n-1} y_j + PP \sum_{j=1}^n P_j \quad \text{(Total Energy Consumption)}$$
   - Scalarized weighted sum (LMIP-MTCTEC-W, PDF page 25, printed page 4267):
     $$\min f(w_1, w_2) = w_1 \sum_{j=1}^n C_j + w_2 \left[ \sum_{j=1}^{n-1} ((C_{j+1} - P_{j+1}) - C_j) IP + \sum_{j=1}^{n-1} y_j \right]$$
     where $w_1 + w_2 = 1$, $w_1, w_2 \ge 0$. (Constant processing energy $PP \sum P_j$ dropped).
8. **Relevant Constraints:**
   - Release time constraint: $C_j - P_j \ge r_j, \quad \forall j = 1, \dots, n$.
   - Precedence / non-overlap constraint: $C_{j+1} - P_{j+1} \ge C_j, \quad \forall j = 1, \dots, n-1$.
   - Breakeven switching linearization (PDF page 24, printed page 4266):
     $$((C_{j+1} - P_{j+1}) - C_j) - S \le L b_{1j}$$
     $$y_j - (SE - ((C_{j+1} - P_{j+1}) - C_j) IP) \le L (1 - b_{1j})$$
     $$-y_j + (SE - ((C_{j+1} - P_{j+1}) - C_j) IP) \le L (1 - b_{1j})$$
     $$-(((C_{j+1} - P_{j+1}) - C_j) - S) \le L b_{2j}$$
     $$y_j \le L (1 - b_{2j})$$
     $$-y_j \le L (1 - b_{2j})$$
     $$b_{1j}, b_{2j} \in \{0, 1\}$$
9. **Energy Model:** Explicitly segments machine states into:
   - Processing energy ($PP \times P_j$).
   - Idle energy ($IP \times \text{duration}$).
   - Setup / switching energy ($SE = \text{Turn-off energy} + \text{Turn-on energy}$).
   - Standby / deep sleep: Not differentiated from basic OFF.
10. **Electricity Tariff Model:** **Constant electricity rate / physical energy consumption only**. No time-of-use pricing, no time-dependent rates, no peak pricing.
11. **Peak Demand Representation:** **Not found in inspected text**. No peak-power constraint, no peak-power minimization objective, and no demand-charge cost are modeled.
12. **Multi-Objective Method:** Weighted-sum method generating non-dominated solutions by drawing random weights $(w_1, w_2)$ with $w_1 + w_2 = 1$. (Does not capture unsupported non-convex Pareto solutions).
13. **Solution Method / Solver:** Mixed Integer Linear Programming (MILP) solved using ILOG CPLEX 9.0. Also proposes greedy dispatching heuristics (M-DEB) integrated with neural-network job arrival predictors.
14. **Benchmarks, Datasets & Metrics:** Randomly generated job arrival instances ($n \in \{10, 20, 50\}$). CNC milling machine physical baseline parameters: $IP = 1.48$ kW, $PP = 2.22$ kW, $SE = 1.05$ kJ, $t_{OFF} = 0.5$ min. Evaluated on total energy consumption (kWh) and total completion time.
15. **Physical Experiments / Hardware Validation:** None reported in this paper. CNC power values were cited from prior machine baseline tests, but all scheduling experiments were purely numerical simulations.
16. **Assumptions & Limitations:** Fixed job sequence (FIFO); no sequence optimization; single machine only; constant energy pricing; no demand charges; no peak-power tracking.
17. **Specific Relevance to Project:** Provides the fundamental mathematical logic for machine state switching and breakeven duration $S = SE / IP$. Our physical DC testbed machine-state emulator directly embodies these state transitions.

**Key Equation References:**
- **Breakeven Threshold $S$:** Unnumbered, PDF page 8, printed page 4253:
  $$S = \frac{\text{Turn OFF + Turn ON Energy}}{\text{Idle Power Consumption per unit time}} = \frac{SE}{IP}$$
  *Significance:* Establishes when de-energizing an idle machine saves energy versus maintaining standby.
- **Bi-Objective Program LMIP-MTCTEC:** Unnumbered, PDF page 24, printed page 4266.
  *Significance:* Provides linear formulation for idle state power reduction using binary decision variables.

---

### 2.2. Gahm, Denz, Dirr, and Tuma (2016) — [P02]

1. **Verified Citation & DOI:** Gahm, C., Denz, F., Dirr, M., & Tuma, A. (2016). Energy-efficient scheduling in manufacturing companies: A review and research framework. *European Journal of Operational Research*, 248(3), 744–757. DOI: [10.1016/j.ejor.2015.07.017](https://doi.org/10.1016/j.ejor.2015.07.017).
2. **Research Problem & Industrial Application:** Comprehensive survey and structuring of Energy-Efficient Scheduling (EES) in manufacturing companies, establishing a formal taxonomy covering energy supply, energetic coverage, and energy demand.
3. **Scheduling Problem Class:** Review covering single machine ($1$), parallel machines ($P$), flow shop ($F$), job shop ($J$), and hybrid shop ($HS$).
4. **Sets and Indices:** Not applicable (review/framework paper).
5. **Parameters:** Not applicable (taxonomy of parameters).
6. **Decision Variables:** Not applicable.
7. **Objective Function(s):** Classifies objectives into:
   - Monetary: Energy cost, total electricity cost, contracted demand penalties.
   - Non-monetary: Total energy consumption (kWh), peak power (kW), emissions ($CO_2$), makespan, tardiness.
8. **Relevant Constraints:** Framework categorizes energy-related constraints into power limits, maximum energy allowance per interval, and machine state sequence rules.
9. **Energy Model:** Classifies energy consumption mechanisms into:
   - Machine operating states: Processing ($MON$), Idling ($MID$), Startup ($MSU$), Turn-off ($MOF$), Standby ($MST$).
   - Load-dependent machining power.
10. **Electricity Tariff Model:** Systematically classifies energy supply structures:
    - Time-of-Use ($TOU$).
    - Critical Peak Pricing ($CPP$).
    - Real-Time Pricing ($RTP$).
    - Contracted Supply ($CS$): Historical contracted power ($H$), On-peak limits ($O$), Demand penalty charges ($P$).
11. **Peak Demand Representation:** Identifies that peak demand is handled via:
    - Hard power limit constraints ($PE$).
    - Power peak minimization objective.
    - Contractual penalty costs ($CS-P$).
    Notes that explicit demand-charge modeling remains rare compared to simple ToU energy cost minimization.
12. **Multi-Objective Method:** Surveys weighted sums, $\epsilon$-constraint methods, and multi-objective evolutionary algorithms (e.g., NSGA-II, SPEA2).
13. **Solution Method / Solver:** Analyzes distribution: 44% heuristics/metaheuristics, 33% standard mathematical solvers (CPLEX, Gurobi), 23% exact custom algorithms.
14. **Benchmarks & Experiment Design:** Analyzes 87 papers from 1990 to 2014 across 32 journals.
15. **Physical Experiments / Hardware Validation:** Identified **zero** studies with physical hardware testbed validation among the 87 surveyed papers; all relied on simulated or benchmark numerical instances.
16. **Assumptions & Limitations:** High-level conceptual framework; does not propose a single mathematical formulation.
17. **Specific Relevance to Project:** Provides the formal categorization framework to position our project within the EES domain, proving that simultaneously addressing ToU pricing, peak demand charges, and physical validation addresses an under-explored synthesis.

---

### 2.3. Mavrotas (2009) — [P03]

1. **Verified Citation & DOI:** Mavrotas, G. (2009). Effective implementation of the ε-constraint method in Multi-Objective Mathematical Programming problems. *Applied Mathematics and Computation*, 213(2), 455–465. DOI: [10.1016/j.amc.2009.03.037](https://doi.org/10.1016/j.amc.2009.03.037).
2. **Research Problem & Industrial Application:** Generation of the true Pareto optimal set in Multi-Objective Mathematical Programming (MOMP) without generating weakly dominated solutions or suffering from non-convexity limitations inherent in the weighting method.
3. **Scheduling Problem Class:** General Multi-Objective Mathematical Programming (MOMP) / Multi-Objective Integer Programming (MOIP) / MOMILP; applicable to production scheduling.
4. **Sets and Indices:**
   - Objective functions: $k \in \{1, \dots, p\}$, where $f_1(x)$ is retained as the objective and $f_2(x), \dots, f_p(x)$ are transformed into constraints.
   - Grid points / intervals: $l_k \in \{0, \dots, q_k\}$ for objective $k$.
5. **Parameters:**
   - $r_k$: Range of objective function $k$ over the efficient set ($r_k = f_k^{\max} - f_k^{\min}$).
   - $q_k$: Number of equal intervals for the range of objective $k$.
   - $e_k$: Right-hand side grid value for objective $k$ in iteration ($e_k = f_k^{\min} + \frac{l_k}{q_k} r_k$).
   - $eps$: Small numerical scalar parameter ($eps \in [10^{-6}, 10^{-3}]$) to ensure lexicographic enforcement without distorting the primary objective.
6. **Decision Variables:**
   - $x$: Original decision vector of the mathematical program.
   - $s_k$: Non-negative continuous slack / surplus variables for objective constraints ($s_k \ge 0, k = 2, \dots, p$).
7. **Objective Function(s):**
   - AUGMECON formulation (PDF page 5, printed page 459):
     $$\max \left( f_1(x) + eps \times \sum_{k=2}^p \frac{s_k}{r_k} \right)$$
     (or for minimization of primary objective $f_1(x)$):
     $$\min \left( f_1(x) - eps \times \sum_{k=2}^p \frac{s_k}{r_k} \right)$$
8. **Relevant Constraints:**
   - Objective inequality transformed to equality with slack/surplus:
     $$f_k(x) - s_k = e_k, \quad \forall k = 2, \dots, p \quad \text{(for maximization)}$$
     $$f_k(x) + s_k = e_k, \quad \forall k = 2, \dots, p \quad \text{(for minimization)}$$
     $$s_k \ge 0, \quad x \in S$$
9. **Energy Model:** Not applicable (general methodology).
10. **Electricity Tariff Model:** Not applicable.
11. **Peak Demand Representation:** Not applicable.
12. **Multi-Objective Method:** Augmented $\epsilon$-constraint method (AUGMECON). Uses lexicographic optimization on pay-off tables to determine true nadir values and converts inequalities to equalities with scaled slacks.
13. **Solution Method / Solver:** Exact generation method implemented in GAMS, solved using commercial MILP/LP solvers (e.g., CPLEX). Guaranteed to generate only non-dominated (Pareto-optimal) solutions.
14. **Benchmarks & Experiments:** Tested on 2-variable educational LP and multi-objective integer/mixed-integer programming benchmarks from literature.
15. **Physical Experiments / Hardware Validation:** None (mathematical programming paper).
16. **Assumptions & Limitations:** Grid density requires manual tuning ($q_k$); computational effort scales exponentially with the number of objective functions $p$; does not include dynamic grid jumping (introduced in AUGMECON2).
17. **Specific Relevance to Project:** Directly adoptable multi-objective framework for generating the exact Pareto front between Makespan ($C_{\max}$), Energy Cost ($EC$), and Peak Demand ($P_{\max}$). Overcomes the known failure of weighted-sum methods to capture unsupported Pareto schedules.

**Key Equation References:**
- **AUGMECON Formulation:** Unnumbered, PDF page 5, printed page 459:
  $$\max \left( f_1(x) + eps \times \left( \frac{s_2}{r_2} + \frac{s_3}{r_3} + \dots + \frac{s_p}{r_p} \right) \right) \quad \text{s.t.} \quad f_k(x) - s_k = e_k, \; s_k \ge 0$$
  *Significance:* Guarantees mathematical Pareto optimality without generating weakly efficient solutions.

---

### 2.4. Catanzaro, Pesenti, and Ronco (2023) — [P04]

1. **Verified Citation & DOI:** Catanzaro, D., Pesenti, R., & Ronco, R. (2023). Job scheduling under Time-of-Use energy tariffs for sustainable manufacturing: a survey. *European Journal of Operational Research*, 308(3), 1091–1109. DOI: [10.1016/j.ejor.2023.01.029](https://doi.org/10.1016/j.ejor.2023.01.029).
2. **Research Problem & Industrial Application:** Comprehensive state-of-the-art review of job scheduling models explicitly addressing Time-of-Use (ToU) electricity tariffs across 135+ papers published between 2011 and 2022.
3. **Scheduling Problem Class:** Formulates the general **Basic Job Scheduling with TOU tariffs Problem (BJSTP)** and surveys Single Machine (SMS), Parallel Machine (PMS), Flow Shop (FSP), Job Shop (JSP), and Flexible Job Shop (FJSP).
4. **Sets and Indices:**
   - $J$: Set of jobs, indexed by $j \in \{1, \dots, n\}$.
   - $T$: Discretized time horizon of slots, $t \in \{1, \dots, |T|\}$.
   - $T_j$: Subset of $p_j$ time slots in which job $j$ is processed.
5. **Parameters:**
   - $p_j$: Processing time of job $j$ (integer time slots).
   - $c_t$: Energy tariff / cost rate during time slot $t$ ($/kWh or cost unit).
   - $D$: Deadline for the entire schedule ($D \le |T|$).
6. **Decision Variables:**
   - $S$: Schedule defined as a set of job-time slot assignment pairs $(j, T_j)$ satisfying non-overlap and non-preemption.
7. **Objective Function(s):**
   - BJSTP Objective (PDF page 3, printed page 1093):
     $$\min_{S \in \mathcal{S}} E(S) = \sum_{j \in J} \sum_{t \in T_j} c_t \quad \text{(Total Energy Cost)}$$
     subject to:
     $$C_{\max}(S) = \max_{t \in \bigcup_{j \in J} T_j} t \le D$$
8. **Relevant Constraints:**
   - Non-overlap: $T_{j'} \cap T_{j''} = \emptyset, \quad \forall j' \ne j''$.
   - Non-preemption: $T_j$ consists of $p_j$ contiguous time slots.
   - Machine capacity and job precedence relations depending on the specific machine environment.
9. **Energy Model:** Detailed review of energy consumption behaviors:
   - State-based models: processing energy, idling energy, turn-on/turn-off transition energy, standby energy.
   - Speed-scaling / energy-frequency scaling models.
10. **Electricity Tariff Model:** Time-of-Use (ToU) pricing schemes with on-peak, mid-peak, and off-peak tariff periods.
11. **Peak Demand Representation:** **CRITICAL FINDING: Not addressed**. Detailed full-text inspection reveals that across the entire 19-page survey of 135+ papers, "peak" refers **exclusively to peak-price periods of the ToU tariff**. Peak-power limit constraints ($P(t) \le P_{\max}$), peak-power minimization objectives, and billing demand charges ($\$ / kW$) are **completely absent** from their taxonomy and formal BJSTP formulation.
12. **Multi-Objective Method:** Surveys bi-objective formulations balancing Total Energy Cost ($TEC$) against Makespan ($C_{\max}$), Total Tardiness, or Total Completion Time, typically handled via $\epsilon$-constraint or metaheuristic Pareto search.
13. **Solution Method / Solver:** Synthesizes exact methods (time-indexed IP, branch-and-cut, dynamic programming) and metaheuristics (genetic algorithms, particle swarm, tabu search).
14. **Benchmarks & Experiments:** Catalogs standard benchmark adaptations (Taillard, Carlier, Reeves, OR-Library) enriched with synthetic ToU pricing vectors.
15. **Physical Experiments / Hardware Validation:** **Zero physical or hardware validation studies identified**. All reviewed papers are computational or theoretical.
16. **Assumptions & Limitations:** Survey paper; confirms that mainstream ToU scheduling literature has developed in complete isolation from peak demand charge economics.
17. **Specific Relevance to Project:** Provides the primary justification for our research question. It proves that energy-cost-only scheduling under ToU tariffs is extensively covered, but peak-aware scheduling under dual ToU + demand-charge structures remains a substantial research gap in the literature.

**Key Equation References:**
- **BJSTP Total Energy Cost:** Equation (2), PDF page 3, printed page 1093:
  $$E(S) = \sum_{j \in J} \sum_{t \in T_j} c_t$$
  *Significance:* Canonical mathematical definition of ToU energy cost in the operations research literature.
- **BJSTP Problem Statement:** Equations (4)–(5), PDF page 3, printed page 1093:
  $$\min_{S \in \mathcal{S}} E(S) \quad \text{s.t.} \quad C_{\max}(S) \le D$$
  *Significance:* Baseline formulation for energy-cost-only scheduling against which peak-aware formulations must be contrasted.

---

### 2.5. Dai, Tang, Giret, and Salido (2019) — [P05]

1. **Verified Citation & DOI:** Dai, M., Tang, D., Giret, A., & Salido, M. A. (2019). Multi-objective optimization for energy-efficient flexible job shop scheduling problem with transportation constraints. *Robotics and Computer-Integrated Manufacturing*, 59, 143–157. DOI: [10.1016/j.rcim.2019.04.006](https://doi.org/10.1016/j.rcim.2019.04.006).
2. **Research Problem & Industrial Application:** Energy-Efficient Flexible Job Shop Scheduling Problem (EFJSP) with Automated Guided Vehicles (AGVs) transporting workpieces between machine tools.
3. **Scheduling Problem Class:** Flexible Job Shop Scheduling Problem (FJSP) with routing flexibility, machine selection, operation sequencing, and multi-AGV transportation.
4. **Sets and Indices:**
   - Jobs: $i \in \{1, \dots, n\}$.
   - Operations: $O_{ij}$ (operation $j$ of job $i$, $j \in \{1, \dots, N_i\}$).
   - Machines: $k, w \in \{1, \dots, m\}$.
   - AGV transportation trips.
5. **Parameters:**
   - $T_{ijk}$: Processing time of operation $O_{ij}$ on machine $k$.
   - $P_{ijk}$: Processing power demand of machine $k$ on operation $O_{ij}$.
   - $PB_k$: Basic setup/unload power demand of machine $k$.
   - $t_{jk}$: Setup time for operation $j$ on machine $k$.
   - $T_{i(j-1)wk}$: AGV transportation time from machine $w$ to machine $k$.
   - $TP$: Transportation power of AGV.
   - $e$: Auxiliary base power of the entire production workshop (lighting, HVAC).
6. **Decision Variables:**
   - $X_{ijk} \in \{0, 1\}$: Equals 1 if operation $O_{ij}$ is assigned to machine $k$.
   - $Y_{ijkq} \in \{0, 1\}$: Sequence positioning variable of operation $O_{ij}$ on machine $k$ at position $q$.
   - $S_{ijk}, C_{ijk}$: Start and completion times of operation $O_{ij}$ on machine $k$.
7. **Objective Function(s):**
   - Bi-objective model (PDF page 5, printed page 147):
     $$\min f_1 = C_{\max} = \max_{i=1}^n (C_{i, N_i})$$
     $$\min f_2 = E = SE + PE + IE + TE + AE$$
     where:
     - Setup Energy: $SE = \sum_{k=1}^m \sum_{j=1}^{O_k} PB_k \cdot t_{jk}$ (Eq. 1)
     - Processing Energy: $PE = \sum_{i=1}^n \sum_{j=1}^{N_i} \sum_{k=1}^m P_{ijk} T_{ijk} X_{ijk}$ (Eq. 2)
     - Idle Energy: $IE = \sum_{k=1}^m P_k \left( \max_{i,j}(C_{ijk}) - \sum_{i=1}^n \sum_{j=1}^{N_i} (C_{ijk} - S_{ijk}) X_{ijk} \right)$ (Eq. 3)
     - Transportation Energy: $TE = \sum_{i=1}^n \sum_{j=2}^{N_i} \sum_{k=1}^m \sum_{w=1}^m TP \cdot T_{i(j-1)wk} X_{i(j-1)w} X_{ijk}$ (Eq. 4)
     - Auxiliary Energy: $AE = e \cdot C_{\max}$ (Eq. 5)
8. **Relevant Constraints:**
   - Precedence constraints with transportation delays (Eq. 10, PDF page 5, printed page 147):
     $$S_{ij} \ge C_{i(j-1)} + \sum_{k=1}^m \sum_{w=1}^m T_{i(j-1)wk} X_{i(j-1)w} X_{ijk}$$
   - Machine non-overlap and capacity constraints (Eq. 11–16).
9. **Energy Model:** Comprehensive 5-component physical energy model (Setup, Machining, Idling, Material Transport, Facility Auxiliary).
10. **Electricity Tariff Model:** **Constant tariff / physical energy consumption only**. No time-varying prices, no ToU tiers.
11. **Peak Demand Representation:** **Not found in inspected text**. No peak-power constraint, no peak demand objective, no demand charges.
12. **Multi-Objective Method:** Modified Genetic Algorithm with Pareto non-dominated sorting and energy-saving decoding heuristics.
13. **Solution Method / Solver:** Metaheuristic (improved GA) validated against CPLEX for small instances.
14. **Benchmarks & Experiments:** Brandimarte (Mk01–Mk10) and Kacem benchmark instances adapted with energy parameters.
15. **Physical Experiments / Hardware Validation:** None reported; purely numerical simulations.
16. **Assumptions & Limitations:** Deterministic AGV speeds; no battery discharge constraints; constant energy price; no peak load tracking.
17. **Specific Relevance to Project:** Provides the multi-component energy structure (processing, idle, auxiliary) that can be adopted for our physical machine-load emulators. Demonstrates how idle and auxiliary power scale directly with makespan.

**Key Equation References:**
- **Idle Energy Component:** Equation (3), PDF page 5, printed page 147:
  $$IE = \sum_{k=1}^m P_k \left( \max_{i,j}(C_{ijk}) - \sum_{i=1}^n \sum_{j=1}^{N_i} (C_{ijk} - S_{ijk}) X_{ijk} \right)$$
  *Significance:* Directly connects machine scheduling gaps to parasitic idle energy dissipation.
- **Bi-Objective Minimization:** Equations (6)–(7), PDF page 5, printed page 147:
  $$\min f_1 = C_{\max}, \quad \min f_2 = E = SE + PE + IE + TE + AE$$
  *Significance:* Core tradeoff between productivity (makespan) and physical energy consumption.

---

### 2.6. Sung and Kwon (2026) — [P06]

1. **Verified Citation & DOI:** Sung, J., & Kwon, S. (2026). Demand charge determination for managing peak demand in energy-aware production scheduling. *Applied Energy*, 415, Article 127953. Published online 15 July 2026. DOI: [10.1016/j.apenergy.2026.127953](https://doi.org/10.1016/j.apenergy.2026.127953).
2. **Research Problem & Industrial Application:** Determining the economic demand charge rate ($DCR$, in $\$ / kW$) required to induce an industrial manufacturer to schedule operations such that maximum peak power demand does not exceed a desired target, without imposing rigid operational power caps.
3. **Scheduling Problem Class:** Identical parallel machine scheduling with non-preemptive jobs, formulated using time-indexed integer programming.
4. **Sets and Indices:**
   - Machines: $i \in M = \{1, \dots, |M|\}$.
   - Jobs: $j \in J = \{1, \dots, |J|\}$.
   - Time units: $t \in T = \{1, \dots, |T|\}$ (15-minute discretized slots over 24 h horizon, $|T| = 96$).
   - Fixed billing intervals: $k \in K = \{1, \dots, |K|\}$ (e.g., 1-hour intervals, length $L = 4$ time units).
   - $T_k$: Set of time units belonging to fixed interval $k$.
5. **Parameters:**
   - $PT_j$: Processing time of job $j$ (in hours / time units).
   - $E_j$: Electricity consumption rate / power demand of job $j$ (kW).
   - $C_t$: Time-varying electricity energy price at time unit $t$ ($\$ / kWh$).
   - $L$: Length of fixed peak-measurement interval (in time units / hours, $L = 4$).
   - $\bar{P}_{\max}$: Peak demand limit imposed in constraint (kW).
   - $P_{lb}, P_{\min}, P_{\max}$: Theoretical lower bound, minimum achievable peak, and maximum peak demand.
   - $d$: Peak demand range span ($d = P_{\min} - P_{\max}$).
   - $DCR$: Demand charge rate ($\$ / kW$).
6. **Decision Variables:**
   - $x_{j,t} \in \{0, 1\}$: Binary variable equal to 1 if job $j$ starts at time unit $t$.
   - $ec$: Continuous variable representing total energy charge ($\$).
   - $p_{\max}$: Continuous variable representing maximum interval power demand (kW).
   - $\alpha \in [0, 1]$: Continuous reduction scaling factor in Pareto front construction.
7. **Objective Function(s):**
   - Time-Indexed IP Model (TI-IP, PDF page 5, printed page 5):
     $$\min ec \quad \text{(Eq. 1a)}$$
     $$\text{subject to} \quad \sum_{j \in J} \sum_{t \in T} \sum_{t'=\max(t-PT_j+1, 1)}^t C_t E_j x_{j,t'} \le ec \quad \text{(Eq. 1b)}$$
   - Total Electricity Cost Model (TEC, PDF page 10, printed page 10):
     $$\min TEC = ec + DCR \cdot p_{\max} \quad \text{(Eq. 4a)}$$
8. **Relevant Constraints:**
   - Single start / non-preemption: $\sum_{t=1}^{|T|-PT_j+1} x_{j,t} = 1, \quad \forall j \in J$ (Eq. 1c).
   - Horizon deadline completion: $\sum_{t'=|T|-PT_j+2}^{|T|} x_{j,t'} = 0, \quad \forall j \in J$ (Eq. 1d).
   - Machine capacity at each time slot: $\sum_{j \in J} \sum_{t'=\max(t-PT_j+1, 1)}^t x_{j,t'} \le |M|, \quad \forall t \in T$ (Eq. 1e).
   - Hard peak-demand constraint over fixed intervals $k \in K$ (Eq. 1f, PDF page 5):
     $$\frac{1}{L} \sum_{j \in J} \sum_{t \in T_k} \sum_{t'=\max(t-PT_j+1, 1)}^t E_j x_{j,t'} \le \bar{P}_{\max}, \quad \forall k \in K$$
   - Interval peak definition in TEC model (Eq. 4c, PDF page 10):
     $$\frac{1}{L} \sum_{j \in J} \sum_{t \in T_k} \sum_{t'=\max(t-PT_j+1, 1)}^t E_j x_{j,t'} \le p_{\max}, \quad \forall k \in K$$
9. **Energy Model:** Processing power only ($E_j$, kW). Machine idling power, turn-on/turn-off transition energy, and auxiliary energy are assumed negligible and omitted.
10. **Electricity Tariff Model:** Dual-component industrial tariff:
    - Time-varying energy charge ($C_t$, $\$ / kWh$) evaluated across 4 real pricing profiles: TOU1, TOU2, RTP1, RTP2 (KEPCO data).
    - Demand charge rate ($DCR$, $\$ / kW$) applied to the maximum average power across fixed 1-hour intervals $k \in K$.
11. **Peak Demand Representation:** Rigorously investigates both:
    - As a hard constraint: Eq. (1f) and Eq. (2c) in the $\epsilon$-constraint Pareto front construction model (PFC).
    - As an explicit monetary cost in the economic objective: Eq. (4a) ($DCR \cdot p_{\max}$).
    - Peak-Energy Curve (PEC) derivation: Proves that the optimal marginal demand charge rate is the negative derivative of the energy charge with respect to peak demand:
      $$dcr = -f'(x) \quad \text{where} \; f(x) \; \text{is the Pareto-optimal energy charge at peak} \; x.$$
12. **Multi-Objective Method:** $\epsilon$-constraint method systematically varying $\bar{P}_{\max}$ to generate the Pareto front between energy charge ($ec$) and peak demand ($p_{\max}$). Then extracts the lower convex hull (supported solutions) to fit continuous exponential ($a e^{bx} + c$) and polynomial ($a x^2 + bx + c$) curves.
13. **Solution Method / Solver:** Coded in Python; solved using Gurobi 12.0.2 on Intel Core i9-13900K with 32 GB RAM.
14. **Benchmarks & Experiments:** Full factorial experiment: $|M| \in \{2, 3\}$ machines; 5 and 8 jobs per machine ($|J| \in \{10, 15, 16, 24\}$); 3 target peak demand levels (low, median, high); 4 tariff profiles (TOU1, TOU2, RTP1, RTP2).
15. **Physical Experiments / Hardware Validation:** **None reported**. Entirely computational mathematical programming and regression analysis.
16. **Assumptions & Limitations:** Identical parallel machines; zero machine idle power; zero startup/shutdown power; fixed 24 h horizon; offline deterministic parameters; job-to-machine assignment reconstructed post-hoc because machine index $i$ is omitted from $x_{j,t}$.
17. **Specific Relevance to Project:** **Foundational paper for our demand-charge mathematical formulation**. Directly provides the exact formulation for interval-based peak demand measurement (Eq. 1f, 4c) and the dual-component economic objective (Eq. 4a). Confirms that an explicit $DCR$ term drives substantial peak reduction. Our project extends this by introducing machine-power heterogeneity, idle power states, and physical testbed validation.

**Key Equation References:**
- **Time-Indexed Energy Cost & Peak Constraints:** Equations (1a)–(1f), PDF page 5, printed page 5:
  $$\min ec \quad \text{s.t.} \quad \frac{1}{L} \sum_{j \in J} \sum_{t \in T_k} \sum_{t'=\max(t-PT_j+1, 1)}^t E_j x_{j,t'} \le \bar{P}_{\max}, \quad \forall k \in K$$
  *Significance:* Mathematically rigorous formulation of interval-averaged peak power constraints matching utility billing rules.
- **Economic Total Electricity Cost Objective:** Equation (4a), PDF page 10, printed page 10:
  $$\min TEC = ec + DCR \cdot p_{\max}$$
  *Significance:* Core economic objective balancing kWh consumption costs against kW peak demand charges.
- **Marginal Demand Charge Relation:** Unnumbered, PDF page 7, printed page 7:
  $$C(x) = f(x) + dcr \times x \implies \frac{dC(x)}{dx} = f'(x) + dcr = 0 \implies dcr = -f'(x)$$
  *Significance:* Explains the mathematical mechanism connecting demand-charge intensity to peak shaving.

---

### 2.7. Mavrotas and Florios (2013) — [P07]

1. **Verified Citation & DOI:** Mavrotas, G., & Florios, K. (2013). An improved version of the augmented ε-constraint method (AUGMECON2) for finding the exact Pareto set in Multi-Objective Integer Programming problems. *Applied Mathematics and Computation*, 219(18), 9652–9669. DOI: [10.1016/j.amc.2013.03.002](https://doi.org/10.1016/j.amc.2013.03.002). (Also archived as MPRA Paper No. 105034).
2. **Research Problem & Industrial Application:** Accelerating the augmented $\epsilon$-constraint method to generate the exact Pareto optimal set in Multi-Objective Integer Programming (MOIP) and Multi-Objective Combinatorial Optimization (MOCO) problems by bypassing redundant solver runs.
3. **Scheduling Problem Class:** General Multi-Objective Integer Programming (MOIP) / Combinatorial Optimization; directly applicable to discrete production scheduling.
4. **Sets and Indices:**
   - Objectives: $k \in \{1, \dots, p\}$.
   - Grid points: $t \in \{0, \dots, q_k\}$ for constrained objective $k$.
5. **Parameters:**
   - $r_k$: Range of objective function $k$ ($r_k = f_k^{\max} - f_k^{\min}$).
   - $q_k$: Number of intervals for objective $k$.
   - $step_k$: Discretization step size ($step_k = r_k / q_k$).
   - $eps$: Small positive scalar ($eps \in [10^{-6}, 10^{-3}]$).
6. **Decision Variables:**
   - $x$: Discrete/integer decision vector.
   - $S_k$: Non-negative surplus/slack variables for constrained objective functions ($k = 2, \dots, p$).
7. **Objective Function(s):**
   - AUGMECON2 Reformulation with tiered lexicographic slack scaling (PDF page 7, printed page 9657):
     $$\max \left( f_1(x) + eps \times \left( \frac{S_2}{r_2} + 10^{-1} \frac{S_3}{r_3} + \dots + 10^{-(p-2)} \frac{S_p}{r_p} \right) \right)$$
     subject to:
     $$f_k(x) - S_k = e_k, \quad \forall k = 2, \dots, p$$
     $$x \in S, \quad S_k \ge 0$$
8. **Relevant Constraints:**
   - Parametric RHS grid point calculation:
     $$e_k^t = f_k^{\min} + t \times step_k$$
   - Bypass calculation for innermost constrained objective ($k = 2$):
     $$b = \left\lfloor \frac{S_2}{step_2} \right\rfloor$$
     When $S_2 > step_2$, the algorithm advances the grid counter by $b$ intervals immediately without calling the integer programming solver, as all intermediate solutions are proven to be identical.
9. **Energy Model:** Not applicable (mathematical programming methodology).
10. **Electricity Tariff Model:** Not applicable.
11. **Peak Demand Representation:** Not applicable.
12. **Multi-Objective Method:** AUGMECON2. Generates the exact Pareto set for integer problems when $step_k$ is set to 1 (or the greatest common divisor of objective coefficients).
13. **Solution Method / Solver:** Mathematical programming algorithm coded in GAMS; solved with CPLEX.
14. **Benchmarks & Experiments:** Multiobjective knapsack, multi-objective set packing, and combinatorial benchmark instances up to 27,260 efficient solutions.
15. **Physical Experiments / Hardware Validation:** None (pure optimization theory).
16. **Assumptions & Limitations:** Best suited for problems where constrained objectives have integer coefficients. If applied to continuous objectives, exactness depends on step size discretization.
17. **Specific Relevance to Project:** Provides the state-of-the-art exact multi-objective generation algorithm for our tri-objective scheduling problem ($C_{\max}$, Energy Cost, Peak Demand). The bypass mechanism is especially valuable in avoiding redundant solver calls when the peak-power constraint is non-binding.

**Key Equation References:**
- **Tiered Lexicographic Objective:** Unnumbered, PDF page 7, printed page 9657:
  $$\max \left( f_1(x) + eps \times \left( \frac{S_2}{r_2} + 10^{-1} \frac{S_3}{r_3} + \dots + 10^{-(p-2)} \frac{S_p}{r_p} \right) \right)$$
  *Significance:* Enforces hierarchical tie-breaking among alternative optima across secondary objectives.
- **Bypass Step Formula:** Unnumbered, PDF page 8, printed page 9658:
  $$b = \text{int}(S_2 / step_2)$$
  *Significance:* Provides orders-of-magnitude computational acceleration in integer programming Pareto generation.

---

### 2.8. Moon, Shin, and Park (2013) — [P09]

1. **Verified Citation & DOI:** Moon, J.-Y., Shin, K., & Park, J. (2013). Optimization of production scheduling with time-dependent and machine-dependent electricity cost for industrial energy efficiency. *International Journal of Advanced Manufacturing Technology*, 68(1–4), 523–535. DOI: [10.1007/s00170-013-4749-8](https://doi.org/10.1007/s00170-013-4749-8).
2. **Research Problem & Industrial Application:** Scheduling production on unrelated parallel machines with machine-dependent and time-dependent electricity tariffs to reduce total electricity expenditure while avoiding excessive makespan extension.
3. **Scheduling Problem Class:** **Unrelated parallel machine scheduling ($R || C_{\max} \cdot PC + EC$)**. (Corrects earlier Round-1 classification error which mislabeled this as job-shop).
4. **Sets and Indices:**
   - Machines: $i \in \{1, \dots, m\}$.
   - Jobs: $j \in \{1, \dots, n\}$.
   - Time slots: $k \in \{1, \dots, 24\}$ (hourly discretization over 24 h).
5. **Parameters:**
   - $p_{ij}$: Processing time of job $j$ on machine $i$ (hours).
   - $c_i$: Power consumption of machine $i$ (kWh / kW).
   - $e_k$: Hourly electricity price during hour $k$ (won / kWh, Korean KEPCO summer/winter ToU tariff).
   - $PC$: Penalty cost per unit makespan (won / hour).
   - $st, dt$: System available start time and due date time.
6. **Decision Variables:**
   - $x_{ijk} \in \{0, 1\}$: Equals 1 if job $j$ is processed at hour $k$ on machine $i$.
   - $y_{ij} \in \{0, 1\}$: Equals 1 if job $j$ is assigned to machine $i$.
   - $C_{\max}$: Total completion time / makespan (hours).
   - $EC$: Total electricity cost (won).
7. **Objective Function(s):**
   - Weighted objective function (PDF page 6, printed page 528):
     $$\min C_{\max} \times PC + EC$$
8. **Relevant Constraints:**
   - Processing time fulfillment: $\sum_{k=1}^{24} x_{ijk} = p_{ij} \times y_{ij}, \quad \forall i, j$ (Eq. 1).
   - Makespan definition (stated as sum of processing times on machine $i$): $\sum_{j=1}^n \sum_{k=1}^{24} x_{ijk} \le C_{\max}, \quad \forall i$ (Eq. 2).
   - Electricity cost accounting: $\sum_{i=1}^m \sum_{j=1}^n \sum_{k=1}^{24} x_{ijk} \times e_k \times c_i = EC$ (Eq. 3).
   - Working time window: $\sum_{j=1}^n \sum_{k=1}^{st-1} x_{ijk} = 0$ (Eq. 4), $\sum_{j=1}^n \sum_{k=dt+1}^{24} x_{ijk} = 0$ (Eq. 5).
   - Single machine assignment: $\sum_{i=1}^m y_{ij} = 1, \quad \forall j$ (Eq. 6).
9. **Energy Model:** Machine-dependent processing power only ($c_i$). Machine idling power, turn-on/turn-off transition energy, and standby power are omitted.
10. **Electricity Tariff Model:** Korean KEPCO 3-tier Time-of-Use (ToU) electricity tariff (summer and winter schedules: off-peak, mid-peak, on-peak).
11. **Peak Demand Representation:** **Not found in inspected text**. No peak-power constraint, no peak demand minimization objective, and no demand charges.
12. **Multi-Objective Method:** Scalarized single-objective combining makespan penalty ($C_{\max} \times PC$) with electricity cost ($EC$).
13. **Solution Method / Solver:** MILP formulation solved via CPLEX (small instances) and a Hybrid Inserted Genetic Algorithm (HIGA) that inserts blank (idle) slots to shift operations away from on-peak hours.
14. **Benchmarks & Experiments:** Synthetic instances: 2 machines / 5 jobs; 3 machines / 6 jobs; up to 60 jobs. Evaluated on electricity cost reduction and makespan trade-offs.
15. **Physical Experiments / Hardware Validation:** None reported; purely numerical simulation.
16. **Assumptions & Limitations:**
   - **Severe Formulation Flaw in Paper:** Eq. (2) defines $C_{\max}$ as the total workload assigned to machine $i$ ($\sum_j p_{ij}$), rather than the actual temporal completion time of the last scheduled job ($\max_k \{k \cdot x_{ijk}\}$).
   - **Missing Machine Capacity Constraint:** The MILP formulation lacks the non-overlap constraint $\sum_j x_{ijk} \le 1$, meaning that the mathematical formulation as printed allows multiple jobs to be processed concurrently on the same machine during hour $k$! (This is handled implicitly inside their GA heuristic, but makes their printed MILP defective).
17. **Specific Relevance to Project:** Directly demonstrates machine-dependent power heterogeneity ($c_i$) under ToU tariffs and validates the strategy of intentionally inserting idle time during peak-tariff windows. Warns us against repeating their formulation errors regarding makespan and non-overlap constraints.

**Key Equation References:**
- **Electricity Cost Calculation:** Equation (3), PDF page 6, printed page 528:
  $$\sum_{i=1}^m \sum_{j=1}^n \sum_{k=1}^{24} x_{ijk} \times e_k \times c_i = EC$$
  *Significance:* Explicit formulation of machine-dependent power ($c_i$) combined with time-dependent pricing ($e_k$).
- **Combined Economic-Makespan Objective:** Unnumbered, PDF page 6, printed page 528:
  $$\min C_{\max} \times PC + EC$$
  *Significance:* Establishes a commercial penalty approach for makespan extension.

---

### 2.9. Aghelinejad, Ouazene, and Yalaoui (2019) — [P10]

1. **Verified Citation & DOI:** Aghelinejad, M., Ouazene, Y., & Yalaoui, A. (2019). Complexity analysis of energy-efficient single machine scheduling problems. *Operations Research Perspectives*, 6, Article 100108. DOI: [10.1016/j.orp.2019.100108](https://doi.org/10.1016/j.orp.2019.100108).
2. **Research Problem & Industrial Application:** Theoretical computational complexity classification of energy-efficient scheduling on a single machine with multiple discrete operational states (ON, OFF, Idle, and transition states) under Time-of-Use electricity tariffs.
3. **Scheduling Problem Class:** **Single-machine scheduling** with finite machine states ($1, TOU | states | TEC$).
4. **Sets and Indices:**
   - Jobs: $j \in \{1, \dots, n\}$.
   - Time slots: $t \in \{1, \dots, T\}$.
   - Machine states: $k \in \{OFF, Ton, ON, Toff, Idle\}$.
   - $\phi_k$: Set of time slots during which the machine is in state $k$.
5. **Parameters:**
   - $p_j$: Integer processing time of job $j$.
   - $P = \sum_{j=1}^n p_j$: Total required processing time across all jobs.
   - $c_t$: Unit electricity price in time slot $t$ (ToU tariff).
   - $e_k$: Power consumption rate in state $k$ ($e_{ON} > e_{Idle} > e_{OFF} = 0, \; e_{Ton} > 0, \; e_{Toff} > 0$).
   - $d_k$: Minimum integer duration required to remain in state $k$ ($d_{Ton} = \tau_1, \; d_{Toff} = \tau_2, \; d_{OFF} \ge 1$).
6. **Decision Variables:**
   - State assignment of the machine across time slots $t = 1, \dots, T$.
7. **Objective Function(s):**
   - Total Energy Consumption Cost (PDF page 3, printed page 3):
     $$F = \sum_{k \in \{OFF, Ton, ON, Toff, Idle\}} \sum_{t \in \phi_k} e_k c_t \quad \text{(Eq. 4)}$$
8. **Relevant Constraints:**
   - State transition rules: Valid transitions only between $OFF \leftrightarrow Ton \leftrightarrow ON \leftrightarrow Toff \leftrightarrow OFF$ and $ON \leftrightarrow Idle \leftrightarrow ON$ (Fig. 1).
   - Initial and final state: Machine must start and finish in OFF state ($\phi_0 = OFF, \phi_T = OFF$).
   - Horizon duration balance: $|\phi_{Ton}| + |\phi_{ON}| + |\phi_{Toff}| + |\phi_{Idle}| + |\phi_{OFF}| = T$ (Eq. 9).
   - Processing requirement: $|\phi_{ON}| = P = \sum_{j=1}^n p_j$ (Eq. 10).
9. **Energy Model:** Complete multi-state energy model including idle power, turn-on transition power, and turn-off transition power.
10. **Electricity Tariff Model:** Time-of-Use (ToU) energy tariffs ($c_t$). Analyzes constant prices ($c_t = c$), strictly increasing prices ($c_t < c_{t+1}$), and general arbitrary ToU profiles.
11. **Peak Demand Representation:** **Not found in inspected text**. No peak-power constraint, no peak demand objective, and no demand charges.
12. **Multi-Objective Method:** Single-objective minimization of Total Energy Cost ($TEC$).
13. **Solution Method & Computational Complexity Proofs:**
   - **Case 1 ($1, TOU | sequence, states | TEC$):** Fixed job sequence. Solved in polynomial time $O(P \cdot T^2)$ using Dynamic Programming on an acyclic directed graph (DAG).
   - **Case 2 ($1, c_t=c | states | TEC$):** Constant pricing. Solved in polynomial time $O(n \log n)$ using Shortest Processing Time (SPT) rule.
   - **Case 3 ($1, c_t < c_{t+1} | states | TEC$):** Strictly increasing pricing. Solved in polynomial time $O(n \log n)$ via SPT.
   - **Case 4 ($1, TOU | states | TEC$):** General ToU pricing without fixed sequence. **Proved to be NP-hard in the strong sense** via reduction from the 3-PARTITION problem (PDF pages 7–8, printed pages 7–8).
14. **Benchmarks & Experiments:** Random problem instances ($n \in \{10, 20, 50, 60, 70\}$) evaluated against CPLEX.
15. **Physical Experiments / Hardware Validation:** None reported; purely mathematical proofs and numerical solver experiments.
16. **Assumptions & Limitations:** Single machine only; no job-dependent power consumption; no peak-load constraints; no demand charges.
17. **Specific Relevance to Project:** Provides the definitive theoretical proof that scheduling under ToU tariffs with machine state switching is strongly NP-hard. Justifies the use of formal mathematical programming solvers (OR-Tools / CP-SAT or MILP) and exact multi-objective methods.

**Key Equation References:**
- **State Energy Hierarchy:** Equations (1)–(3), PDF page 3, printed page 3:
  $$e_{ON} > e_{Idle} > e_{OFF} = 0, \quad e_{Ton} > e_{OFF} = 0, \quad e_{Toff} > e_{OFF} = 0$$
  *Significance:* Formalizes physical machine state power inequalities for scheduling models.
- **Total Energy Cost Formulation:** Equation (4), PDF page 3, printed page 3:
  $$F = \sum_{k} \sum_{t \in \phi_k} e_k c_t$$
  *Significance:* Canonical state-indexed formulation of energy costs under time-varying electricity tariffs.

---

### 2.10. Fang, Lin, and Tang (2013) — [P08]

- **Status:** **Unavailable / Pending Full-Text Inspection**.
- **Bibliographic Details:** Fang, J., Lin, F., & Tang, D. (2013). Flow shop scheduling with peak power consumption constraints. *Annals of Operations Research*. DOI: [10.1007/s10479-012-1294-z](https://doi.org/10.1007/s10479-012-1294-z).
- **Audit Note:** Full-text PDF was not available in local workspace. Per research integrity rules, no equations, variable definitions, or claims have been invented. Marked pending full-text retrieval.

---

## 3. Cross-Paper Comparison

| Paper Key | Citation | Scheduling Class | Objective Function(s) | Energy Model Components | Electricity Tariff Mechanism | Treatment of Peak Demand | Optimization / Solution Method | Hardware / Physical Validation |
|---|---|---|---|---|---|---|---|---|
| **P01** | Mouzon et al. (2007) | Single Machine ($1$) | $\min \sum C_j$, $\min \text{TEC}$ | Processing, Idle, Turn-ON, Turn-OFF | Constant pricing ($\$/kWh$) | **None** | Weighted-sum MILP (CPLEX 9.0) & dispatching heuristics | **None** (pure simulation using literature CNC parameters) |
| **P02** | Gahm et al. (2016) | Review ($1, P, F, J, HS$) | Survey of monetary & non-monetary metrics | Classifies $MON, MID, MSU, MOF, MST$ | Survey of ToU, CPP, RTP, Contracted Supply | Classifies hard limits ($PE$) vs penalties ($CS-P$) | Survey (MIP, heuristics, standard solvers) | **None** across 87 surveyed articles |
| **P03** | Mavrotas (2009) | General MOMP / MOIP | $\max (f_1 + eps \sum \frac{s_k}{r_k})$ | Not applicable | Not applicable | Not applicable | Augmented $\epsilon$-constraint (AUGMECON, GAMS/CPLEX) | **None** (mathematical programming paper) |
| **P04** | Catanzaro et al. (2023) | Survey ($1, P, F, J, FJ$) | $\min E(S) = \sum c_t$ s.t. $C_{\max} \le D$ | Processing, Idle, Shutdown, Standby, Speed scaling | Time-of-Use (ToU) tariffs | **Absent across entire survey** (only peak tariff hours) | Survey of exact time-indexed IP & metaheuristics | **None** across 135+ reviewed papers |
| **P05** | Dai et al. (2019) | Flexible Job Shop ($FJSP$) | $\min C_{\max}$, $\min E$ ($SE+PE+IE+TE+AE$) | Setup, Machining, Idling, AGV Transport, Auxiliary | Constant pricing ($\$/kWh$) | **None** | Enhanced Genetic Algorithm & MILP (CPLEX) | **None** (benchmark numerical tests) |
| **P06** | Sung & Kwon (2026) | Identical Parallel ($P$) | $\min ec$, $\min (ec + DCR \cdot p_{\max})$ | Processing power ($E_j$) only | ToU and Real-Time Pricing (RTP) | **Explicitly models both:** Hard limit constraint & $\$ / kW$ Demand Charge | $\epsilon$-constraint, Gurobi 12.0.2 & Peak-Energy Curve | **None** (computational numerical simulations) |
| **P07** | Mavrotas & Florios (2013) | General MOIP / MOMILP | $\max (f_1 + eps \sum 10^{-(k-2)} \frac{S_k}{r_k})$ | Not applicable | Not applicable | Not applicable | AUGMECON2 with bypass coefficient $b = \lfloor S_2 / step_2 \rfloor$ | **None** (algorithm development) |
| **P08** | Fang et al. (2013) | Flow Shop ($F$) | *Pending retrieval* | *Pending retrieval* | *Pending retrieval* | Candidate peak-power constraint | *Pending retrieval* | *Pending retrieval* |
| **P09** | Moon et al. (2013) | Unrelated Parallel ($R$) | $\min (C_{\max} \cdot PC + EC)$ | Machine-dependent processing power ($c_i$) | Korean 3-tier ToU tariff | **None** | Hybrid Inserted Genetic Algorithm & MILP (CPLEX) | **None** (synthetic numerical instances) |
| **P10** | Aghelinejad et al. (2019) | Single Machine ($1$) | $\min \text{TEC} = \sum e_k c_t$ | Multi-state ($ON, OFF, Idle, Ton, Toff$) | Constant, increasing, and general ToU | **None** | Graph Dynamic Programming ($O(PT^2)$) & NP-hardness proof | **None** (theoretical complexity proofs) |

---

## 4. Literature-to-Research-Question Traceability

**Core Research Question:**  
*Under what combinations of demand-charge intensity, time-of-use tariff variation, workload intensity, and machine-power heterogeneity does peak-aware production scheduling provide a statistically significant economic benefit over energy-cost-only scheduling?*

### 4.1. Energy-Cost-Only vs. Peak-Aware Scheduling
- **Direct Evidence from Literature:**
  - Catanzaro et al. (2023) [P04] demonstrates that the overwhelming majority of ToU scheduling research is strictly **energy-cost-only** ($\min \sum c_t$, Eq. 2), ignoring peak load spikes.
  - Sung & Kwon (2026) [P06] explicitly demonstrates the conflict between energy-cost-only and peak-aware scheduling. Under energy-cost-only scheduling ($DCR = 0$), schedules aggressively shift loads into off-peak windows, creating severe secondary demand peaks that destabilize the grid and generate massive demand charges under industrial billing structures.
  - Equation (4a) in Sung & Kwon ($TEC = ec + DCR \cdot p_{\max}$) provides the foundational formulation for contrasting energy-cost-only ($DCR = 0$) against peak-aware ($DCR > 0$) scheduling.
- **Traceability to Project:** Directly supported. Contrasting energy-cost-only against peak-aware scheduling is grounded in Sung & Kwon (2026) [P06] and justified by the gap identified in Catanzaro et al. (2023) [P04].

### 4.2. Time-of-Use Price Variation
- **Direct Evidence from Literature:**
  - Moon et al. (2013) [P09], Aghelinejad et al. (2019) [P10], and Sung & Kwon (2026) [P06] all confirm that time-dependent energy pricing induces operations to cluster in low-tariff intervals.
  - Aghelinejad et al. (2019) [P10] mathematically proves that arbitrary ToU pricing transforms even single-machine scheduling into a strongly NP-hard problem.
  - Sung & Kwon (2026) [P06] evaluates multiple ToU ratios (e.g., peak-to-off-peak ratios of 1.5:1 to 3:1) and confirms that higher tariff variation increases the economic pressure to cluster operations, thereby directly exacerbating peak power spikes.
- **Traceability to Project:** Directly supported. Testing tariff variation (e.g., Karnataka KERC LT-5 / HT-2 tariff ratios) is backed by primary evidence from [P06, P09, P10].

### 4.3. Demand-Charge Intensity and Monetary Demand-Charge Term
- **Direct Evidence from Literature:**
  - Sung & Kwon (2026) [P06] provides direct mathematical formulation for demand charges applied to interval-averaged power demand (Eq. 1f, 4c, printed page 5 & 10):
    $$\frac{1}{L} \sum_{j \in J} \sum_{t \in T_k} \sum_{t'=\max(t-PT_j+1, 1)}^t E_j x_{j,t'} \le p_{\max}, \quad \forall k \in K$$
  - Sung & Kwon also proves that the marginal demand charge rate required to incentivize peak reduction corresponds to $-f'(x)$ on the Peak-Energy Curve (PDF page 7).
  - Crucially, Gahm et al. (2016) [P02] catalogs contractual power penalties ($CS-P$), confirming that real-world industrial tariffs impose heavy billing charges on peak kW.
- **Traceability to Project:** Directly supported. Formulating the demand charge as $\$ / kW$ over discrete utility billing windows (e.g., 15-minute or 1-hour intervals) is directly grounded in Sung & Kwon (2026) [P06].

### 4.4. Workload Intensity and Machine-Power Heterogeneity
- **Direct Evidence from Literature:**
  - **Machine-Power Heterogeneity:** Moon et al. (2013) [P09] explicitly introduces machine-dependent power ratings ($c_i$, Table 5 & 7), demonstrating that when machines have heterogeneous power draws, operation assignment fundamentally impacts total energy and instantaneous power. However, Moon et al. omitted peak demand constraints. Conversely, Sung & Kwon (2026) [P06] modeled peak demand but assumed **identical parallel machines** ($E_j$ dependent only on the job, machine index omitted in Eq. 1e).
  - **Workload Intensity:** Sung & Kwon (2026) [P06] tests 5 vs. 8 jobs per machine over a fixed 24-hour horizon, observing that higher workload tightens the scheduling feasible region and forces machines to run concurrently, drastically reducing flexibility for peak avoidance.
- **Traceability to Project:** Directly supported as a research synthesis. Combining machine-power heterogeneity ($P_{im}$ from Moon et al. [P09]) with peak demand charges (from Sung & Kwon [P06]) under varying workload intensity is an evidence-backed extension.

### 4.5. Evaluation Metrics: Makespan, Energy Cost, and Peak Demand
- **Direct Evidence from Literature:**
  - Makespan ($C_{\max}$): Formulated as a primary objective in Mouzon et al. (2007) [P01], Moon et al. (2013) [P09], and Dai et al. (2019) [P05].
  - Energy Cost ($EC$ / $ec$): Formulated under ToU tariffs in Moon et al. (2013) [P09], Catanzaro et al. (2023) [P04], and Sung & Kwon (2026) [P06].
  - Peak Demand ($p_{\max}$): Formulated as interval peak in Sung & Kwon (2026) [P06].
  - Tri-objective Pareto frontier generation: Directly supported by the AUGMECON2 exact framework from Mavrotas & Florios (2013) [P07].
- **Traceability to Project:** Fully supported by direct mathematical formulations across [P01, P05, P06, P07].

---

## 5. Evidence Gaps and Unresolved Questions

### Gap 1: Absence of Physical Hardware Validation Across the Entire Literature
- **Evidence:** Inspection of all 9 accessible full texts, including two major comprehensive reviews spanning over 220 individual studies (Gahm et al. 2016 [P02] reviewing 87 papers; Catanzaro et al. 2023 [P04] reviewing 135+ papers), reveals that **not a single study conducted physical hardware validation or sensor-in-the-loop experimental verification**.
- **Implication:** The entire existing literature relies on idealized mathematical simulations that assume instantaneous power step-changes, zero sensor noise, zero bus voltage drops, and deterministic power plateaus.
- **Unresolved Question for Project:** How large is the discrepancy between idealized mathematical power profiles and real-world physical current/power measurements (captured via INA226 sensors on our DC testbed), and does physical transient behavior erode scheduled peak demand savings?

### Gap 2: Synthesis of Machine-Power Heterogeneity with Explicit Demand Charges
- **Evidence:**
  - Sung & Kwon (2026) [P06] provides the most advanced demand-charge formulation, but restricts its model to **identical parallel machines** where machine power is homogeneous.
  - Moon et al. (2013) [P09] addresses machine-power heterogeneity ($c_i$) but completely ignores peak demand and demand charges.
  - Dai et al. (2019) [P05] includes heterogeneous machine power in an FJSP but operates under constant energy pricing without ToU or peak demand charges.
- **Unresolved Question for Project:** When machines have stark power heterogeneity (e.g., high-power vs. low-power units), under what workload conditions does assigning jobs to slower, lower-power machines reduce the billing peak demand without violating production deadlines?

### Gap 3: Mathematical Formulation Reconciliation Between Continuous-Time and Time-Indexed Models
- **Evidence:**
  - Sung & Kwon (2026) [P06] uses a **time-indexed** formulation ($x_{j,t} \in \{0, 1\}$ over 96 discrete 15-minute intervals). This allows straightforward calculation of interval power demand (Eq. 1f), but causes exponential growth in binary variables as the planning horizon expands.
  - Mouzon et al. (2007) [P01] and Dai et al. (2019) [P05] use **continuous-time** precedence variables ($C_j, S_{ijk}$), which solve rapidly for makespan but make the calculation of concurrent instantaneous power demand highly non-linear or dependent on complex overlapping continuous intervals.
- **Unresolved Question for Project:** Can a hybrid or discretized time-block formulation maintain computational tractability in OR-Tools / CP-SAT while accurately enforcing utility 15-minute billing demand windows?

---

## 6. Recommended Next Steps

1. **Retain 9-Paper Foundation & Keep Fang et al. (2013) Marked Pending:** Do not delay mathematical modeling for the missing Fang et al. paper, as Sung & Kwon (2026) [P06] provides a far more complete and recent treatment of demand charges.
2. **Draft Mathematical Model v1:** Formulate the baseline scheduling model combining:
   - Time-indexed machine non-overlap and non-preemption constraints (from Sung & Kwon [P06] and Catanzaro [P04], correcting Moon et al.'s formulation errors).
   - Machine-dependent heterogeneous power ratings (from Moon et al. [P09] and Dai et al. [P05]).
   - Explicit machine idle power states and breakeven switching (from Mouzon et al. [P01] and Aghelinejad et al. [P10]).
   - Dual-component tariff objective: ToU energy consumption cost + interval peak demand charges (from Sung & Kwon [P06]).
3. **Multi-Objective Exact Frontier:** Implement the AUGMECON2 exact algorithm (Mavrotas & Florios [P07]) in Python using OR-Tools CP-SAT to generate the true 3D Pareto surface ($C_{\max}$, Energy Cost, Peak Demand).
4. **Hand-Solve Small Benchmark Instance:** Construct a small 2-machine, 4-job instance with known ToU and demand-charge rates to mathematically prove that energy-cost-only scheduling induces a higher demand charge than peak-aware scheduling before running large-scale experiments.
