# PROJECT MASTER CONTEXT / SINGLE SOURCE OF TRUTH
## Peak-Aware Energy-Cost Production Scheduling Under Industrial Tariff Structures

**Document type:** Comprehensive project context, research foundation, technical specification, execution plan, decision log, and preserved source archive  
**Version:** 1.0-consolidated  
**Prepared:** 2026-10-02  
**Project status:** **Planning → mathematical-foundation audit → implementation**  
**Institution:** RV College of Engineering, Bengaluru  
**Course context:** Experiential Learning (EL), III Semester, 2025 Batch  
**SDG:** SDG 9 — Industry, Innovation and Infrastructure  

> **Purpose of this file:** This is the consolidated master context for the entire project discussion. It preserves the project problem, research question, rubric logic, literature direction, verified KERC tariff facts, mathematical direction, software/hardware architecture, experimental plan, AI research workflow, corrections, risks, timelines, and all major decisions made during planning. It also preserves historical source documents in appendices so earlier details are not silently lost.

---

# 0. CANONICAL STATUS AND AUTHORITY ORDER

This file intentionally distinguishes **current/canonical decisions** from **superseded ideas and earlier drafts**.

### Authority order

1. **Verified official KERC tariff order uploaded to the project:** `tarif order.pdf` / KERC Tariff Order 2025 All ESCOMs, especially Annexure 9, pp. 545, 550, 552.
2. **Current literature-to-model audit:** peer-reviewed research and original papers verified during the literature stage.
3. **This consolidated master file:** current project decisions and explicit corrections recorded below.
4. `master_execution_plan.md`: detailed execution plan, preserved below.
5. `energy_scheduling_full_validation.md`, `energy_scheduling_math_research_validation.md`, `energy_scheduling_research_validation.md`: earlier validation/audit documents, preserved below.
6. Earlier brainstorming artifacts: useful for history and rationale, but not authoritative for the current formulation.

### Critical rule

**Do not silently reuse a superseded value or component from an earlier draft.** In particular:

- PZEM-004T for the planned DC testbed is **superseded** by INA226.
- Approximate/unverified tariff values from earlier drafts are **superseded** by the verified KERC FY2026–27 HT-2(a) values in Section 9.
- The real KERC demand charge is **₹350/kVA/month**, not a generic ₹350/kW experimental coefficient.
- The real billing-demand rule is **max(monthly maximum demand, 90% of contract demand)**, subject to the order's rounding and excess-demand rules.
- CP-SAT is a **constraint programming / SAT-based scheduling solver**, not a conventional MILP solver. A time-indexed MILP may be a literature formulation, but the implementation target is CP-SAT using interval variables and scheduling constraints.
- Real tariff demand billing is monthly and in kVA; a short physical testbed run must not be presented as an actual monthly bill.
- Arbitrary thresholds (5%, 10%, 20%, etc.) must not be presented as known outcomes before experimentation.
- Algorithmic novelty is **not claimed**.

---

# 1. PROJECT IDENTITY

## 1.1 Final working title

> **Peak-Aware Energy-Cost Production Scheduling for Small Manufacturing Systems Under Industrial Tariff Structures: A Multi-Objective Optimization Study with Physical Validation**

Short working name:

> **Peak-Aware Energy-Cost Production Scheduling**

Possible shorthand:

> **PAECS / Peak-Aware Scheduling**

## 1.2 Core problem statement

Small manufacturing units operate under electricity costs that can contain both energy charges and demand-related charges. Production scheduling traditionally focuses on production constraints and makespan, while electricity-cost structure may be ignored. An energy-cost-aware scheduler can move work toward cheaper tariff periods, but concentration of high-power operations can create higher coincident demand. The project therefore studies whether explicitly accounting for peak demand can change scheduling decisions and total electricity cost, and under what operating/tariff conditions that effect becomes economically meaningful.

The project is deliberately framed as an **applied operations-research and engineering study**, not as a claim of a new optimization algorithm.

## 1.3 Core research question

> **Under what combinations of demand-charge intensity, time-of-use tariff variation, workload intensity, and machine power heterogeneity does peak-aware multi-objective production scheduling provide a statistically significant economic benefit over energy-cost-only scheduling?**

## 1.4 Research interpretation

The project is asking a conditional question, not assuming a positive result.

Possible outcomes include:

- peak-awareness produces a meaningful benefit under some conditions;
- peak-awareness has little/no benefit at small scale;
- energy-cost-only scheduling does not systematically raise peak demand;
- the benefit appears only under specific combinations of tariff differential, workload density, and power heterogeneity;
- the richer mathematical model gives little practical improvement.

A negative or weak result is still scientifically valid if the experimental design is sound.

---

# 2. ORIGIN OF THE PROJECT / SDG 9 CONTEXT

The project was selected while brainstorming engineering ideas for **SDG 9: Industry, Innovation and Infrastructure**.

The original brainstorming deliberately rejected generic “AI slop”: chatbots, basic prediction models, dashboards without decision value, and arbitrary combinations of AI + IoT + blockchain.

The selection criteria were:

- real industrial/infrastructure problem;
- concrete innovation gap;
- technically feasible undergraduate prototype;
- measurable improvement over a baseline;
- mathematically defensible formulation;
- research-paper support;
- physical proof where possible;
- strong fit to the evaluation rubric;
- manageable scope for a student team.

Energy-aware production scheduling emerged as **Idea 3** in the broader SDG-9 idea set.

Other ideas considered during brainstorming included:

1. Optimal sensor placement for water-distribution leak detection using graph theory.
2. Edge-TinyML bearing fault diagnosis with domain adaptation for variable-speed MSME motors.
3. **Multi-objective energy-aware production scheduling for Indian MSMEs under ToU tariffs.** ← selected direction.
4. Optimal cleaning scheduling for solar-panel arrays using soiling-loss prediction.
5. Edge-first cold-chain monitoring with commodity-specific spoilage prediction.
6. Graph-optimized vehicle routing for MSME last-mile distribution.
7. Low-cost structural-health monitoring of bridges with MEMS and modal analysis.
8. Adaptive traffic-signal control using multi-agent reinforcement learning.
9. Power-quality disturbance classification using wavelet features + lightweight ML on edge hardware.
10. Biomass collection network design for crop-residue pelletization.
11. MSME warehouse order-picking route optimization.
12. Predictive road-maintenance scheduling using pavement-condition-index modeling.
13. Industrial motor-current-signature anomaly detection.
14. Disaster-resilient LoRa communication mesh for infrastructure monitoring.
15. Indoor air-quality control using MPC-based ventilation optimization.

The earlier audit found the energy-scheduling idea particularly strong on **feasibility**, while explicitly warning that the standard energy-aware formulation itself is not algorithmically novel.

---

# 3. SDG 9 / RVCE RUBRIC CONTEXT

## 3.1 Evaluation structure

The project sits in the RVCE Experiential Learning rubric context summarized as:

- **Total:** 200 marks
- **Phase I:** 40 marks
- **Phase II:** 60 marks
- **Phase III:** 100 marks
- **Bonus:** +20 for notable outcomes such as publications, patents, or product development.

### Phase I — Problem Definition / Objectives / Methodology

| Criterion | Weight | What matters |
|---|---:|---|
| Clarity | 20 sub-mark block | Problem stated precisely |
| Relevance | 20 sub-mark block | Direct SDG 9 significance |
| Context | 20 sub-mark block | Literature/background depth |
| Flow Chart | 20 sub-mark block | Complete methodology flow |
| Specificity | 10 | Measurable objectives |
| Alignment | 10 | Objective ↔ problem coherence |
| Achievability | 10 | Realistic scope |
| Appropriateness | 10 | Method justified |
| Detail | 10 | Method documented deeply |

### Phase II — Execution / Tools / Partial Results

| Criterion | Weight |
|---|---:|
| Adherence | 30 | Follow planned methodology |
| Timeliness | 30 | Deliver on schedule |
| Quality | 30 | High-quality implementation |
| Selection | 20 | Appropriate/sophisticated tools |
| Application | 20 | Effective use |
| Integration | 20 | Tools work together |
| Clarity | 10 | Partial results documentation |
| Progress | 10 | Visible progress |
| Analysis | 10 | Early-data interpretation |

### Phase III — Prototype / Results / Report / Poster

| Criterion | Weight |
|---|---:|
| Functionality | 30 | Fully working prototype |
| Innovation | 30 | Innovation/creativity |
| Usability | 30 | User-friendly polished demonstration |
| Results Clarity | 20 | Clear results |
| Results Analysis | 20 | Deep analysis |
| Interpretation | 20 | Supported conclusions |
| Report Organization | 20 | Strong structure |
| Report Clarity | 20 | Professional writing |
| Report Completeness | 20 | All required sections |
| Poster/PPT Visual Appeal | 10 | Professional visuals |
| Poster/PPT Clarity | 10 | Easy to understand |
| Poster/PPT Content | 10 | Complete information |

### Bonus

+20 for notable outcomes such as publication, patent, product development.

## 3.2 Implications for this project

The project should prioritize:

1. **A fully functioning prototype.**
2. **A real mathematical formulation.**
3. **Baseline-vs-proposed quantitative comparison.**
4. **Research-backed context.**
5. **A physical testbed that validates the computational model.**
6. **A polished demo and report.**

Technologies must not be added solely to look advanced.

---

# 4. HONEST NOVELTY POSITION

## 4.1 What is established

The following are considered established and must not be presented as algorithmic novelty:

- job-shop / flexible job-shop scheduling formulations;
- makespan minimization;
- energy-aware production scheduling;
- machine-state energy models;
- ToU-aware scheduling;
- peak-demand minimax formulations in energy systems;
- ε-constraint / AUGMECON multi-objective methodology;
- NSGA-II/III;
- CP-SAT scheduling primitives;
- MQTT + ESP32 control;
- Raspberry Pi as an optimization server;
- power monitoring as an IoT pattern.

## 4.2 What is the intended contribution

The contribution is an **extended formulation study with empirical validation**, comprising:

### Engineering integration

Combining established scheduling, tariff, peak-load, measurement and edge-computing components into one reproducible workflow.

### Empirical contribution

Systematic analysis of the **makespan–energy-cost–peak-demand trade-off** under multiple tariff/workload conditions.

### Physical-validation contribution

Executing selected schedules on a programmable machine-load emulation testbed and comparing predicted versus measured power/energy/peak.

### Parametric/sensitivity contribution

Characterizing when peak-awareness matters, when it does not, and where the transition occurs in parameter space.

### Edge-deployment contribution

Benchmarking the validated scheduling workflow on Raspberry Pi 5 to demonstrate edge feasibility. This is engineering evidence, not algorithmic novelty.

## 4.3 Claims that must not be made

Do not say:

- “novel algorithm”;
- “new optimization algorithm”;
- “new mathematical technique”;
- “AI-powered optimization” unless a justified AI component is separately researched;
- “guaranteed cost savings”;
- “X% improvement” before measurements exist;
- “factory-ready” or “industrial deployment validated” from a student testbed;
- “IoT innovation” simply because MQTT/ESP32 is present;
- “Raspberry Pi makes the project novel.”

---

# 5. RESEARCH PRIOR ART / LITERATURE DIRECTION

## 5.1 Initial search methodology used in the earlier validation

The project validation search covered:

- Google Scholar;
- IEEE Xplore via Scholar indexing;
- ScienceDirect;
- MDPI;
- SpringerLink;
- arXiv;
- ResearchGate.

Search themes included:

- energy-aware scheduling;
- multi-objective job-shop scheduling;
- ToU scheduling;
- peak-demand scheduling;
- robust scheduling;
- rolling-horizon manufacturing;
- measured-power scheduling;
- edge-computing scheduling;
- MSME energy management;
- closed-loop scheduling.

**Limitation:** the earlier audit did not have direct IEEE Xplore or ACM Digital Library API access, so absence of an exact paper must not be interpreted as proof of absence.

## 5.2 Key literature families identified

The following research families are central to the project:

### Foundational energy-aware scheduling

- **Mouzon et al. (2007, IIE Transactions)** — single-machine ON/OFF MILP, energy minimization, foundational energy-aware scheduling.
- **Gahm et al. (2016, European Journal of Operational Research)** — survey of 100+ papers on energy-efficient manufacturing scheduling; useful taxonomy/background source.

### ToU-aware production scheduling

- **Che et al. (2017)** — unrelated parallel-machine scheduling under time-of-use electricity pricing; useful foundation for time-dependent electricity cost in production scheduling.
- **Park & Ham (2022)** — flexible job-shop scheduling under ToU pricing, considering makespan/energy-cost trade-offs and comparing ILP/constraint-programming approaches.

### Demand-charge / peak-aware scheduling

- **Abikarram, McConky & Proano (2019)** — production scheduling with both consumption charges and demand charges; particularly close to the project's question about how demand-charge intensity affects production schedules.
- **Cui & Lu (2020)** — peak-demand-aware manufacturing/scheduling formulation using maximum average power over a time interval.
- **2026 Applied Energy work on peak–energy relationships in production scheduling** — identified as especially relevant to the proposed peak–energy trade-off / demand-charge sensitivity direction.

### Multi-objective solution methodology

- **Mavrotas (2009)** — AUGMECON / augmented ε-constraint methodology; foundational reference for extracting Pareto-efficient solutions from multi-objective optimization.

### Other research families that are relevant but secondary

- machine-state energy models;
- robust/stochastic scheduling;
- scenario-based processing-time perturbation;
- rolling-horizon / model-predictive scheduling;
- digital-twin scheduling;
- power profiling with measured signals;
- edge scheduling;
- uncertainty and dynamic rescheduling.

## 5.3 What earlier literature validation concluded

### Established

1. Bi-objective makespan + energy scheduling is well studied.
2. Machine-state energy modeling is standard.
3. ToU-aware scheduling is extensively studied.
4. ε-constraint / NSGA methodologies are established.
5. Peak-demand minimax formulations are standard in energy systems.
6. Physical execution of a mathematically optimized schedule is much less common than simulation-only evaluation.

### Less studied / candidate gap areas

1. Systematic tri-objective manufacturing scheduling analysis with **makespan + energy cost + peak demand** and explicit Pareto-surface analysis.
2. Systematic characterization of **when** peak-awareness produces economically meaningful benefit.
3. Physical execution and measured validation of optimized schedules.
4. Simulation-to-measurement comparison using calibrated machine power profiles.

### Confidence / caution

These gap statements are **not** absolute claims of novelty. They require the dedicated literature-to-model audit described below.

---

# 6. LITERATURE-TO-MODEL AUDIT — IMMEDIATE RESEARCH TASK

## 6.1 Critical principle

We explicitly decided **not to invent the mathematical formulation first**.

The correct sequence is:

```text
peer-reviewed paper
      ↓
original formulation / equation
      ↓
assumptions
      ↓
comparison with other formulations
      ↓
legitimate adaptation
      ↓
KERC tariff parameterization
      ↓
validated implementation
```

## 6.2 Target paper set

Collect approximately **15–20 candidate papers**, then reduce to **5–8 foundational papers**.

Suggested coverage:

| Category | Target |
|---|---:|
| Foundational scheduling | 3–5 |
| Recent energy-aware scheduling | 8–12 |
| Peak/demand-charge scheduling | 3–5 |
| Physical validation | 2–3 |
| ε-constraint / CP methodology | 2–3 |
| Tariff/policy | 2–3 |

The same paper may cover multiple categories.

## 6.3 Required literature matrix

Recommended columns:

```text
ID | Authors | Year | Title | Venue | DOI | Model_Type | Objectives | Machines |
Uncertainty | Physical_Validation | Tariff_Type | Peak_Demand_Addressed |
Solution_Method | Instance_Size | Key_Finding | Limitation | Relevance_to_Us |
PDF_Available | Notes
```

## 6.4 For each foundational paper, extract

- scheduling problem class;
- sets;
- parameters;
- decision variables;
- objective function(s);
- precedence constraints;
- assignment constraints;
- machine non-overlap constraints;
- energy state variables;
- tariff model;
- peak-demand model;
- demand-charge model;
- multi-objective method;
- solver;
- data/instance generation;
- assumptions;
- exact equation/page references;
- what can be adopted;
- what cannot be adopted;
- where our adaptation begins.

## 6.5 Literature evidence discipline

For each equation in our final model, classify it as one of:

- `[LITERATURE-DERIVED]`
- `[ALGEBRAIC DERIVATION]`
- `[PROJECT ASSUMPTION]`
- `[PROJECT DESIGN CHOICE]`
- `[EXPERIMENTAL PARAMETER]`
- `[UNRESOLVED / NEEDS VERIFICATION]`

Never imply that a paper says something it does not say.

---

# 7. AI / RESEARCH TOOLING WORKFLOW

## 7.1 Model available in Antigravity

The user has access to models including:

- Gemini 3.8 Flash Medium
- Gemini 3.7 Flash Medium
- Gemini 3.6 Flash High
- Gemini 3.1 Pro Low

The recommended research model from the available set is:

> **Gemini 3.1 Pro — High**, when the interface allows the high reasoning level for the Pro model.

Use Flash High models for routine coding/debugging after the formulation is frozen.

## 7.2 Intended AI division of labor

### Gemini 3.1 Pro High

Primary literature-to-model research assistant:

- broad paper discovery;
- formulation extraction;
- literature synthesis;
- identifying competing models;
- identifying assumptions and gaps.

### Elicit (free tier)

Useful as a paper-first extraction/indexing tool:

- systematic literature table;
- query-based paper screening;
- paper-level metadata extraction.

### NotebookLM (free)

Useful after collecting PDFs:

- verify claims against the actual documents;
- ask questions constrained to uploaded papers;
- reduce citation hallucination risk.

### GPT-5.6 / current assistant workflow

Use as the integrator and skeptical reviewer:

- reconcile literature with KERC;
- build the final mathematical formulation;
- check whether every equation is supported;
- implementation design;
- experiment design;
- statistical analysis;
- final report architecture.

## 7.3 AI workflow

```text
Gemini / Elicit
      ↓
15–20 candidate papers
      ↓
5–8 foundational papers
      ↓
NotebookLM / source-PDF verification
      ↓
Literature → Equation → Assumption matrix
      ↓
GPT-5.6 / critical synthesis
      ↓
Mathematical Foundation v1
      ↓
Independent challenge / audit
      ↓
MODEL FREEZE
```

## 7.4 Exact literature-search prompt for Gemini Deep Research / Antigravity

Use the following prompt **before asking the AI to design the mathematical model**:

```text
I am developing an undergraduate engineering research project on:

“Peak-Aware Energy-Cost Production Scheduling Under Industrial Tariff Structures”

Core research question:
Under what combinations of demand-charge intensity, time-of-use (ToU) tariff variation, workload intensity, and machine power heterogeneity does peak-aware production scheduling provide an economically meaningful benefit over energy-cost-only scheduling?

I do NOT want you to invent a mathematical model.

Your task is to conduct a rigorous literature search and identify the strongest peer-reviewed research papers that can provide the mathematical foundation for this project.

SEARCH SCOPE

Find papers covering as many of these as possible:

1. Production/job scheduling with electricity cost
2. Job-shop scheduling / flexible job-shop scheduling / parallel-machine scheduling with energy considerations
3. Production scheduling under Time-of-Use electricity tariffs
4. Demand-charge-aware production scheduling
5. Peak-demand-aware manufacturing scheduling
6. Joint energy-cost and peak-demand optimization
7. Multi-objective production scheduling involving makespan, energy cost and/or peak demand
8. ε-constraint / AUGMECON methods for multi-objective scheduling
9. Peak-energy trade-off or peak-demand sensitivity analysis in manufacturing scheduling

PRIORITY

Prioritize:

- Peer-reviewed journal papers
- Operations Research / Production Planning / Manufacturing / Energy / Applied Energy literature
- Established mathematical formulations rather than purely heuristic papers
- Papers containing explicit mathematical models
- Papers with equations for decision variables, objectives and constraints
- Papers with reproducible experimental methodology
- Recent papers (preferably 2015–2026), while including older foundational papers when necessary

IMPORTANT: Do not select papers merely because they mention “energy-efficient manufacturing.” The paper must contain mathematical material that could genuinely support our formulation.

FOR EACH PAPER, EXTRACT

Create a table with:

1. Full citation
2. Year
3. Journal/conference
4. DOI or official URL
5. Scheduling problem type
6. Decision variables
7. Objective function(s)
8. Production constraints
9. Energy-consumption formulation
10. Electricity-cost formulation
11. ToU formulation, if present
12. Peak-demand/demand-charge formulation, if present
13. Multi-objective method, if present
14. Optimization/solution method
15. Dataset/instance generation
16. Key assumptions
17. Exact equations or equation numbers that are relevant
18. What mathematical component we could legitimately adopt
19. What cannot be adopted because the assumptions differ
20. Relevance to our project: HIGH / MEDIUM / LOW

MATHEMATICAL AUDIT

For the 5–8 strongest papers, go deeper.

For each paper:

- Identify the exact mathematical formulation.
- Define every important variable and parameter.
- Reconstruct the objective functions in clean notation.
- Reconstruct the major constraints.
- Explain the physical meaning of each equation.
- Give the page/equation number where each formulation appears.
- Distinguish clearly between equations explicitly stated by the paper and your own algebraic interpretation.

Then construct a:

LITERATURE → MATHEMATICAL COMPONENT MATRIX

Example:

Paper A → production scheduling constraints
Paper B → ToU energy-cost formulation
Paper C → peak-demand formulation
Paper D → demand-charge formulation
Paper E → multi-objective / ε-constraint method

PROJECT GAP ANALYSIS

After reviewing the papers, determine:

1. Which parts of our proposed model are already established?
2. Which combinations have already been studied?
3. What is genuinely missing or insufficiently studied?
4. Is our proposed research question still defensible?
5. What should our contribution be if algorithmic novelty is not justified?

Do NOT claim novelty unless the literature strongly supports it.

KARNATAKA TARIFF CONTEXT

Our eventual application will use the Karnataka Electricity Regulatory Commission (KERC) FY2026–27 HT-2(a) industrial tariff.

However, do NOT force the papers to match KERC.

Instead:

First identify the established mathematical formulation from the literature.

Then explain how a real industrial tariff such as KERC could be inserted into that framework.

IMPORTANT RESEARCH RULES

- Do not fabricate papers, DOIs, equation numbers or results.
- Verify every paper using the publisher page, DOI, Crossref, Google Scholar, or another authoritative source.
- Prefer the original paper over reviews when extracting equations.
- Do not use blog posts, generic websites or AI-generated summaries as evidence.
- If a paper cannot be verified, mark it as UNVERIFIED and exclude it from the foundational set.
- Do not infer that a paper supports demand charges, peak demand or ToU unless it actually models them.
- Explicitly state when evidence is missing.
- Avoid papers whose mathematics cannot be inspected.

FINAL OUTPUT

Produce these sections:

A. Executive summary
B. 15–20 candidate papers
C. Ranked foundational set of 5–8 papers
D. Detailed mathematical extraction from the foundational papers
E. Literature → Equation → Project-component matrix
F. Comparison of competing mathematical formulations
G. Research-gap analysis
H. Recommended mathematical foundation for our project
I. References with DOI/official links

The most important goal is:

DO NOT GIVE ME A NEW MODEL YET.

First establish, from real peer-reviewed research, exactly which mathematical formulations already exist and which components can legitimately form the foundation of our project.
```

## 7.5 Short Elicit prompt

```text
Find peer-reviewed papers on mathematical production scheduling models that incorporate:

- job-shop, flexible job-shop, or parallel-machine scheduling
- time-of-use electricity pricing
- energy consumption/cost
- peak demand or demand charges
- multi-objective scheduling
- makespan + energy cost + peak demand
- ε-constraint methods

Prioritize papers with explicit mathematical formulations and equations.

For each paper extract:
problem type, decision variables, objective functions, constraints, energy model, electricity pricing model, peak-demand model, optimization method, assumptions, DOI, and exact equation/page references.

Exclude papers that only discuss energy efficiency conceptually without an explicit optimization formulation.

Identify the 5–8 papers that provide the strongest mathematical foundation for constructing an energy-cost and peak-aware production scheduling model.
Do not invent or infer equations or citations.
```

---

# 8. VERIFIED KERC TARIFF FOUNDATION

## 8.1 Authoritative uploaded source

**Document:** `tarif order.pdf`  
**Official document:** Karnataka Electricity Regulatory Commission Tariff Order 2025 — All ESCOMs  
**Relevant section:** Annexure 9 — Electricity Tariff 2026, Part II High Tension Supply  
**Most relevant pages:** 545–552  

## 8.2 Relevant tariff category

### HT-2(a) Industrial

The order states that HT-2(a) applies to industries including MSMEs, factories, industrial workshops, R&D centres, industrial estates, IT industries, start-ups and many other industrial activities.

This makes HT-2(a) an appropriate **reference tariff category** for the project's industrial/MSME framing.

## 8.3 FY2026–27 base tariff

For HT-2(a):

| Component | FY2026–27 |
|---|---:|
| Demand charge | **₹350/kVA/month of billing demand** |
| Energy charge | **₹6.60/kWh** |

Source: KERC Tariff Order 2025, Annexure 9, p. 550.

## 8.4 Effective date

The multi-year tariff order applies the FY2026–27 tariff from:

> **1 April 2026**

The order was issued/signed by KERC at Bengaluru on 27 March 2025.

## 8.5 HT billing-demand rule

The order's HT billing condition states:

\[
BD=\max(MD,0.90CD)
\]

where:

- \(BD\) = billing demand;
- \(MD\) = maximum demand recorded during the month;
- \(CD\) = contract demand.

Additional tariff-order details:

- if recorded maximum demand exceeds contract demand, excess demand is subject to **two times the normal rate** as deterrent charge;
- during a full billing-month disconnection, billing demand is 90% of contract demand;
- billing demand at or above 0.5 kVA is rounded to the next higher kVA;
- billing demand below 0.5 kVA is ignored.

Source: Annexure 9, pp. 545–546.

## 8.6 Power factor

The order states:

- HT consumers are responsible for PF correction;
- average PF should not be less than 0.90 lag;
- if PF falls below 0.90 lag, a surcharge of 3 paise per unit applies for every reduction of PF by 0.01 below 0.90 lag, under the specified rounding rules;
- PF is computed through KWh/KVAh as specified, with smart/electronic tri-vector meter provisions.

Source: Annexure 9, pp. 545–546.

## 8.7 ToD / ToD tariff

The tariff order's ToD table for HT-2(a), HT-2(b), HT-2(c)(i), and HT-2(c)(ii) gives:

| Time | July–November (monsoon period) | December–June |
|---|---:|---:|
| 06:00–09:00 | 0 paise/unit | **+100 paise/unit** |
| 09:00–18:00 | 0 | 0 |
| 18:00–22:00 | 0 | **+100 paise/unit** |
| 22:00–06:00 | 0 | **−100 paise/unit** |

Therefore, for the FY2026–27 study year, the base energy price plus the ToD adjustment can be represented as:

### December–June

\[
\pi_t=
\begin{cases}
7.60 & 06{:}00-09{:}00 \\
6.60 & 09{:}00-18{:}00 \\
7.60 & 18{:}00-22{:}00 \\
5.60 & 22{:}00-06{:}00
\end{cases}
\quad ₹/kWh
\]

### July–November

\[
\pi_t=6.60\quad ₹/kWh
\]

for the ToD adjustment itself, because the table specifies zero adjustment in all listed periods during the monsoon period.

**Source:** Annexure 9, p. 552.

## 8.8 ToD applicability by contract demand

The tariff order states that:

- compulsory ToD continues for HT2(a), HT2(b), and HT2(c) consumers with **contract demand of 500 kVA and above**;
- optional ToD continues for HT2(a), HT2(b), and HT2(c) consumers with contract demand below 500 kVA;
- the specified ToD conditions apply to the relevant categories;
- BMRCL and Railway Traction are exceptions in the table.

The model must therefore state the assumed contract-demand regime when reproducing a real tariff scenario.

## 8.9 Discounted Energy Rate Scheme interaction

The order states that ToD tariff does **not** apply to energy billed under the new Discounted Energy Rate Scheme, while ToD applies up to the base monthly average consumption as computed by the licensee.

For the core project, the Discounted Energy Rate Scheme should be **excluded unless the research question specifically expands to it**, because it complicates the tariff model.

## 8.10 HT supply scope

Part II High Tension Supply applies to bulk supply at 11 kV and above at standard high voltage/EHV when contract demand is 50 kW / 67 HP and above.

## 8.11 Real tariff vs research tariff parameter

This distinction is mandatory.

### Real tariff layer

For an actual HT-2(a) reference scenario:

\[
EC_{ToD}(S)=\sum_t E_t(S)\pi_t
\]

and a base demand-charge component can be represented through the actual billing-demand rule:

\[
BD(S)=\max(MD_{kVA}(S),0.90CD)
\]

\[
DC_{base}=350\times BD
\]

for FY2026–27, before accounting for any applicable additional charge/surcharge components that the project explicitly excludes or models separately.

### Research sensitivity layer

For systematic parametric experiments, define a normalized demand-intensity parameter:

\[
Cost_\rho(S)=EC(S)+\rho P^{peak}(S)
\]

where \(\rho\) is a **research parameter**, not the real KERC monthly tariff rate.

The project must never describe \(\rho\) as “the KERC demand tariff” unless it is being explicitly mapped to the actual tariff with its correct units and assumptions.

## 8.12 DC testbed and kVA issue

The physical testbed is based on low-voltage DC loads measured with INA226. That naturally gives DC voltage/current/power, i.e. kW-like quantities.

The KERC tariff is expressed in **kVA** for demand billing.

Therefore, the core project should distinguish:

- scheduling/electrical-model peak power in kW;
- tariff billing demand in kVA;
- any PF≈1 mapping used for a simplified laboratory comparison.

The mapping

\[
kVA\approx kW
\]

is a **PF≈1 laboratory assumption**, not a statement that industrial machines universally have unity power factor.

---

# 9. MATHEMATICAL FOUNDATION — CURRENT DIRECTION

## 9.1 Fundamental principle

The mathematical model must be **derived from established production-scheduling and energy-scheduling literature**, then adapted to KERC.

Do not start with an arbitrary weighted objective.

Do not assign arbitrary weights such as:

\[
0.4C_{max}+0.3EC+0.3P^{peak}
\]

without a research reason.

## 9.2 Preferred conceptual structure

The fundamental objectives are:

\[
f_1=C_{max}
\]

\[
f_2=EC
\]

\[
f_3=P^{peak}
\]

where:

- \(C_{max}\) = makespan;
- \(EC\) = ToD-aware energy cost;
- \(P^{peak}\) = maximum concurrent modeled electrical power over the scheduling slots.

## 9.3 Why not blindly make “total bill” the third objective

A cleaner research structure is:

- treat makespan, energy cost, and peak demand as scheduling objectives;
- use the tariff model to translate energy/peak into economic consequences;
- evaluate total bill under specific tariff/demand scenarios.

This allows the project to answer both:

1. what the Pareto structure looks like; and
2. whether that structure matters economically.

## 9.4 Candidate scheduling classes

The model must first settle the exact scheduling class after the literature audit:

- unrelated parallel machines;
- job-shop scheduling;
- flexible job-shop scheduling.

The current implementation direction favors **job-shop/flexible job-shop style scheduling with interval variables**, especially if operations can choose among eligible machines.

Do not choose FJSP merely because it sounds more advanced. Use it only if alternative machine assignments are part of the actual problem definition.

## 9.5 Sets

Candidate canonical notation:

\[
\mathcal{J}=\{1,\dots,n\}
\]

jobs;

\[
\mathcal{O}_j
\]

ordered operations belonging to job \(j\);

\[
\mathcal{M}=\{1,\dots,m\}
\]

machines;

\[
\mathcal{T}=\{1,\dots,H\}
\]

discrete time slots;

\[
\mathcal{M}_o\subseteq\mathcal{M}
\]

machines eligible for operation \(o\).

## 9.6 Candidate parameters

| Symbol | Meaning | Unit | Status |
|---|---|---|---|
| \(p_o\) / \(p_{om}\) | processing time | slots or hours | Model input |
| \(P^{proc}_m\) | processing power | W | measured |
| \(P^{idle}_m\) | idle power | W | measured if modeled |
| \(E^{start}_m\) | startup energy | Wh | measured if modeled |
| \(\pi_t\) | electricity price | ₹/kWh | KERC/parametric |
| \(\rho\) | demand-intensity research parameter | normalized ₹/kW | experimental parameter |
| \(CD\) | contract demand | kVA | tariff scenario |
| \(d_j\) | job deadline | time | optional |
| \(H\) | horizon | slots/time | derived |
| \(\Delta\) | slot width | h | design choice |

## 9.7 Candidate decision variables — two formulations to be reconciled

### Literature/time-indexed formulation

Potential binary variable:

\[
x_{omt}=1
\]

if operation \(o\) starts on machine \(m\) at time \(t\).

Potential state variables:

\[
y_{mt}=1
\]

if machine \(m\) is processing in slot \(t\);

\[
w_{mt}=1
\]

if machine \(m\) is idle/on in slot \(t\);

\[
z_{mt}=1
\]

for a startup transition.

### CP-SAT implementation formulation

For each operation:

- `start_o`
- `end_o`
- `interval_o`

For flexible machine choice:

- `mchoice[o,m]`
- optional interval per candidate machine.

For slot accounting:

- `load[m,t]`
- `slot_power[t]`
- `peak_power`.

These formulations describe the **same underlying physical scheduling logic in different computational forms** and must be reconciled through the literature audit before final freeze.

---

# 10. CANDIDATE MATHEMATICAL MODEL

> **Status:** provisional architecture. The exact final formulation must be literature-audited before implementation.

## 10.1 Base scheduling constraints

### Assignment

Each operation must be assigned once:

\[
\sum_{m\in\mathcal{M}_o}\sum_{t\in\mathcal{T}}x_{omt}=1
\qquad \forall o
\]

For CP-SAT with alternate machines:

```python
model.AddExactlyOne(mchoice[o, m] for m in eligible[o])
```

### Precedence

For consecutive operations \(o_k,o_{k+1}\):

\[
S_{o_{k+1}}\ge C_{o_k}
\]

and:

\[
C_o=S_o+p_o
\]

For a time-indexed formulation, a selected start time can be represented algebraically through the binary assignment/start variables.

### Machine non-overlap

For operations that use the same machine, they cannot overlap.

CP-SAT implementation:

```python
model.AddNoOverlap(intervals_on_machine[m])
```

### Makespan

\[
C_{max}\ge C_o
\]

for the final operation of each job, and:

\[
\min C_{max}
\]

as the production-only objective.

---

# 11. ENERGY MODEL

## 11.1 Core physical relationship

At the scheduling layer:

\[
E=P\Delta t
\]

For slot \(t\):

\[
E_t=P_t\Delta
\]

Total energy:

\[
E=\sum_tP_t\Delta
\]

## 11.2 Aggregate machine power

If the machine-processing state is represented by \(a_{mt}\):

\[
P_t=\sum_mP_m a_{mt}
\]

If richer state modeling is experimentally justified:

\[
P_t=\sum_m\left(
P^{proc}_m y_{mt}
+
P^{idle}_m w_{mt}
+
\frac{E^{start}_m}{\Delta}z_{mt}
\right)
\]

The richer state model is a candidate extension and must be justified through measurement.

## 11.3 Energy cost

\[
EC(S)=\sum_t\pi_tE_t
\]

or:

\[
EC(S)=\sum_t\pi_tP_t\Delta
\]

For CP-SAT, scale costs to integers, e.g. by multiplying by 1000, because CP-SAT works with integer objective coefficients/variables.

## 11.4 Important implementation issue: slot overlap

The most technically delicate computational component is correctly determining whether an operation overlaps a time slot.

For a slot covering:

\[
[t\Delta,(t+1)\Delta)
\]

an operation is active if its interval overlaps the slot.

Candidate implementation approaches:

1. reified/element-based overlap logic;
2. carefully constructed cumulative/state-channeling formulation.

The first implementation should prioritize correctness and hand verification over speed.

---

# 12. PEAK-DEMAND MODEL

## 12.1 Modeled production peak

Define:

\[
P^{peak}\ge P_t
\qquad \forall t
\]

so at optimum:

\[
P^{peak}=\max_tP_t
\]

CP-SAT:

```python
model.AddMaxEquality(peak_power, slot_power_vars)
```

## 12.2 Important distinction

The project has **two related but distinct quantities**:

### Scheduling peak

\[
P^{peak}_{kW}
\]

maximum aggregate load in the modeled scheduling slots.

### KERC billing demand

\[
BD_{kVA}=\max(MD_{kVA},0.90CD)
\]

subject to the tariff order's rules.

The two must not be conflated.

---

# 13. OBJECTIVE STRUCTURE

## 13.1 Model M0 — production-only

\[
\min C_{max}
\]

Purpose: scheduling baseline.

## 13.2 Model M1 — energy-cost-aware

\[
\min EC
\]

subject to production constraints.

## 13.3 Model M2 — bi-objective

\[
\min\{C_{max},EC\}
\]

solved by ε-constraint / Pareto generation.

## 13.4 Model M3 — tri-objective

\[
\min\{C_{max},EC,P^{peak}\}
\]

solved via an ε-constraint/AUGMECON-style approach after implementation details are verified.

## 13.5 Economic evaluation

For normalized experiments:

\[
Bill_\rho(S)=EC(S)+\rho P^{peak}(S)
\]

For real-tariff reference scenarios:

\[
Bill_{KERC}(S)=EC_{ToD}(S)+DC(S)+\text{explicitly modeled additional tariff components}
\]

The exact final real-bill equation depends on which KERC conditions the project includes/excludes.

---

# 14. MULTI-OBJECTIVE SOLUTION METHOD

## 14.1 Why weighted-sum is not the default

Weighted sums introduce subjective weights and can miss non-convex regions of a Pareto set.

Given that job-shop scheduling can produce non-convex trade-offs, ε-constraint methods are a more transparent choice.

## 14.2 ε-constraint / AUGMECON-style approach

A candidate 3-objective formulation:

\[
\min F_2-\delta\left(\frac{s_1}{r_1}+\frac{s_2}{r_2}\right)
\]

subject to:

\[
F_1\le \epsilon_1+s_1
\]

\[
F_3\le \epsilon_3+s_2
\]

plus the scheduling constraints.

Where:

- \(F_1\) = makespan;
- \(F_2\) = energy cost;
- \(F_3\) = peak power;
- \(s_1,s_2\ge0\) are surplus variables;
- \(r_1,r_2\) are objective ranges;
- \(\delta\) is a small augmentation coefficient.

## 14.3 Guarantee caveat

AUGMECON is only as exact as the subproblem solutions.

If the underlying solver proves the relevant subproblem optimality, the resulting solution has the intended Pareto-efficiency guarantees.

If the solver stops with a suboptimal feasible solution because of a time limit, do not claim mathematical Pareto optimality without qualification.

Always record:

- solver status;
- feasibility;
- bound/gap;
- runtime.

## 14.4 Anchor-point workflow

1. solve \(\min C_{max}\);
2. solve \(\min EC\);
3. solve \(\min P^{peak}\);
4. record objective ranges;
5. construct ε-grid;
6. solve subproblems;
7. retain feasible solutions;
8. remove dominated duplicates;
9. evaluate every surviving schedule in the common objective/economic space.

## 14.5 Recommended initial grid

Start with roughly:

\[
k_1=k_2=10
\]

for a 3-objective grid, giving about 100 subproblems per instance.

Do not lock the per-subproblem timeout before pilot runs. First measure median/upper-quantile runtime on small instances, then choose a defensible limit.

## 14.6 Reproducibility

Use a fixed solver seed, e.g.:

```python
solver.parameters.random_seed = 42
```

and record all other relevant solver settings.

---

# 15. COMPUTATIONAL COMPLEXITY / SOLVER POSITION

## 15.1 Problem complexity

Job-shop scheduling is NP-hard.

The computational burden comes primarily from:

- job sequencing;
- machine assignment;
- precedence;
- time horizon;
- multi-objective enumeration.

## 15.2 CP-SAT terminology

Correct phrasing:

> **OR-Tools CP-SAT is the primary constraint-programming / SAT-based optimization solver.**

Do not describe it as “the MILP solver” in the final report.

A time-indexed MILP formulation may be used in the literature review, but the project implementation can use a CP-SAT interval formulation for scheduling efficiency and direct scheduling primitives.

## 15.3 Solver choices

### Primary

- OR-Tools CP-SAT.

### Optional secondary/reference

- PuLP + CBC if needed for a simplified literature-style MILP prototype.

### Not required

- Gurobi as a dependency for the core implementation, particularly because the Raspberry Pi deployment target favors software that supports ARM64.

NSGA-II/NSGA-III can be considered for **stretch/scalability** experiments rather than the core exact-Pareto study.

---

# 16. MODEL HIERARCHY / PROJECT LEVELS

## Level 1 — Minimum viable computational research

Components:

- bi-objective / energy-aware scheduling;
- FCFS and SPT baselines;
- synthetic instances;
- standard tariff parametrization;
- quantitative comparison.

This is a foundation only, not enough to distinguish the project strongly from existing literature.

## Level 2 — Core strong project / target

Adds:

- peak demand as explicit third objective;
- 3D Pareto analysis;
- demand/tariff sensitivity study;
- physical power measurement;
- physical schedule execution;
- predicted-vs-measured validation;
- Raspberry Pi deployment as an edge optimization server.

**Target level.**

## Level 3 — Advanced

Only after Level 2 is solid:

- Monte Carlo processing-time perturbation;
- robust/stochastic analysis;
- NSGA-III on larger instances;
- exact-vs-approximate Pareto comparison.

## Level 4 — Stretch / rolling-horizon adaptive scheduling

Only if Levels 1–3 are complete and stable.

Workflow:

```text
optimize
  ↓
execute
  ↓
detect deviation
  ↓
update state
  ↓
re-optimize remaining schedule
```

Possible perturbation:

- delay one machine by N slots;
- detect via ESP32 state feedback;
- re-solve remaining schedule on Raspberry Pi.

**Do not build the project around Level 4.**

---

# 17. BASELINES

The essential computational comparisons are:

| ID | Method | Description |
|---|---|---|
| B0 | FCFS | First-come-first-served dispatcher, no optimization |
| B1 | SPT | Shortest-processing-time heuristic |
| B2 | Makespan-only | CP-SAT minimizing makespan |
| B3 | Energy-only | CP-SAT minimizing energy cost |
| P1 | Bi-objective | Pareto set for makespan + energy cost |
| P2 | Tri-objective | Pareto set for makespan + energy cost + peak power |

Every schedule, regardless of how generated, must be evaluated on the same external metrics.

---

# 18. INSTANCE GENERATION / DATA MODEL

## 18.1 Candidate sizes

| Size | Jobs | Machines | Ops/job | Processing-time range |
|---|---:|---:|---:|---|
| Small | 5 | 3 | 2–3 | U(1,6) |
| Medium | 8 | 4 | 2–4 | U(1,8) |
| Large | 10–15 | 5–6 | 3–5 | U(1,10) |

Eligibility:

- small: 1–2 eligible machines per operation;
- medium: 1–3;
- large: 1–3.

Initial horizon suggestions:

- small: 48 slots;
- medium: 64 slots;
- large: 96 slots.

## 18.2 Time scaling

Computational model:

- example slot width: 15 minutes = 0.25 h.

Physical testbed:

- one model “time unit” can map to approximately **15 seconds** during the physical demonstration.

This is **time-scaled emulation**. It is not meant to claim physical runtime equivalence to the model-time horizon.

## 18.3 Power heterogeneity

Candidate processing-power levels:

| Level | Processing power range |
|---|---|
| Low | U(100,150) W |
| Medium | U(50,250) W |
| High | U(30,400) W |

The specific numerical ranges are **experimental design choices**, not industrial truths.

## 18.4 Workload intensity

Define:

\[
\lambda=\frac{\sum_op_o}{mH}
\]

Candidate levels:

| Level | \(\lambda\) | Interpretation |
|---|---:|---|
| Light | 0.3 | Large scheduling slack |
| Moderate | 0.5 | Moderate flexibility |
| Heavy | 0.7 | Tight schedule |
| Very heavy | 0.9 | Very little slack |

Adjust processing times or horizon to achieve target \(\lambda\).

## 18.5 Reproducibility

Earlier master plan:

- 20 instances per size × heterogeneity × workload combination;
- seeds 1000–1019;
- deterministic generator;
- save all instances with metadata.

The experimental design can be reduced initially if computational load is too high.

---

# 19. EXPERIMENTAL DESIGN

## Experiment A — Baseline comparison

**Question:** How do FCFS, SPT, makespan-only, and energy-only compare?

- IV: scheduling method;
- DVs: makespan, energy cost, peak power, total bill;
- initial sample: 20 medium instances;
- potential statistics: Friedman test + post-hoc Nemenyi for multiple related methods.

## Experiment B — Bi-objective Pareto structure

**Question:** What is the structure of the makespan–energy-cost Pareto front?

- vary makespan bound / ε;
- observe energy cost, peak power, total bill;
- determine whether peak power changes along the bi-objective front.

## Experiment C — Tri-objective vs bi-objective

**Question:** Does adding peak demand generate materially different Pareto-efficient schedules?

Important methodological correction:

> Do **not** compare a 2D Pareto front and a 3D Pareto surface with an ordinary raw hypervolume directly. Evaluate all resulting schedules in a **common 3D space** first.

Procedure:

1. generate P1 schedules;
2. generate P2 schedules;
3. compute \((C_{max},EC,P^{peak})\) for every schedule;
4. compare total bill under the same demand scenario;
5. optionally compute 3D hypervolume after common-space normalization.

Potential paired statistical comparison:

- best-bill(P1) vs best-bill(P2) for each matched instance;
- Wilcoxon signed-rank test.

## Experiment D — Demand-charge sensitivity

Study:

\[
\rho\rightarrow \Delta Bill
\]

Candidate research grid from the master plan:

\[
\rho\in\{0,25,50,100,150,200,300,400,500\}
\]

units for the normalized research model should be stated carefully and **not confused with the actual KERC ₹/kVA/month tariff**.

Primary plot:

- savings vs \(\rho\).

## Experiment E — ToD sensitivity

Vary peak/off-peak price differential.

Candidate multiplier grid from the master plan:

\[
\{1.0,1.05,1.10,1.15,1.20,1.30,1.50,2.0\}
\]

But these are **experimental values**, not KERC values.

Measure:

- energy cost savings;
- total-bill savings.

## Experiment F — Workload intensity

Vary:

\[
\lambda\in\{0.3,0.5,0.7,0.9\}
\]

Measure:

- peak power;
- total bill;
- objective trade-offs.

The relationship “higher workload intensity → more overlap → larger peak” is a **hypothesis**, not an assumed universal law.

## Experiment G — Machine power heterogeneity

Vary:

- low;
- medium;
- high heterogeneity.

Measure:

- peak-power statistics;
- total bill;
- whether peak-aware scheduling selects different assignments/sequences.

## Experiment H — Scalability

Candidate sizes:

- 5×3;
- 8×4;
- 10×5;
- 12×5;
- 15×6.

Measure:

- solve time;
- optimality gap;
- number of Pareto points;
- solution quality.

Compare:

- laptop;
- Raspberry Pi 5.

## Experiment I — Model fidelity

**Question:** How accurately does the model predict physical energy/peak?

Earlier protocol:

- 5 schedule variants;
- 3 repetitions each;
- measured vs predicted energy and peak.

Metrics:

\[
\text{RelativeError}_{E}=\frac{|E_{pred}-E_{meas}|}{E_{meas}}
\]

\[
\text{RelativeError}_{P}=\frac{|P_{pred}-P_{meas}|}{P_{meas}}
\]

plus MAE/RMSE on the power trace.

## Experiment J — Physical schedule comparison

Compare physically:

- FCFS;
- optimized schedule.

Measure:

- measured energy;
- measured peak;
- execution time.

Earlier plan: 3 repetitions per schedule.

---

# 20. STATISTICAL DESIGN PRINCIPLES

## 20.1 Matched instances

Whenever possible, methods must be compared on the **same generated instance**.

For paired comparison define, for instance \(i\):

\[
\Delta_i=Bill_{A,i}-Bill_{B,i}
\]

or the sign can be reversed depending on the metric convention, but must be fixed before analysis.

## 20.2 Hypothesis testing

For paired nonparametric comparison:

\[
H_0:\operatorname{median}(\Delta)=0
\]

vs.

\[
H_1:\operatorname{median}(\Delta)>0
\]

when “positive” means savings of the proposed method under the chosen difference definition.

The exact statistical test and multiple-comparison correction should be finalized when the experimental design and sample sizes are frozen.

## 20.3 Do not preselect outcome thresholds

Earlier drafts proposed thresholds such as 5%, 10%, 20%. These are not to be treated as known facts.

Use the data to estimate:

- effect size;
- confidence interval;
- distribution;
- sensitivity;
- transition/phase boundary.

---

# 21. PARETO ANALYSIS

## 21.1 Common Evaluation Space

All generated schedules have values for:

\[
(C_{max},EC,P^{peak})
\]

regardless of whether peak was explicitly optimized.

Therefore:

1. evaluate all P1 and P2 schedules on all three metrics;
2. normalize within the relevant common instance comparison;
3. calculate 3D hypervolume only after bringing both solution sets into the same objective space;
4. separately calculate best-bill under the chosen economic scenario.

## 21.2 Suggested metrics

- best total bill;
- 3D normalized hypervolume;
- spacing;
- number of non-dominated solutions;
- Pareto-front coverage if appropriate.

## 21.3 Normalization

Earlier master plan proposal:

- normalize each objective to [0,1] using global min/max across all P1 ∪ P2 solutions for that instance;
- reference point approximately (1.1,1.1,1.1).

This is an **analysis design choice**, not a mathematical truth.

---

# 22. SENSITIVITY / PHASE-MAP STUDY

## 22.1 Main factorization

The project aims to study the relationship:

\[
(\rho,\alpha,\lambda,\sigma)\rightarrow\Delta Bill
\]

where:

- \(\rho\) = normalized demand-charge intensity;
- \(\alpha\) = ToD differential / multiplier;
- \(\lambda\) = workload intensity;
- \(\sigma\) = power heterogeneity descriptor.

## 22.2 Initial full-factorial concept

| Factor | Candidate levels |
|---|---|
| \(\rho\) | 0, 50, 100, 200, 365, 500 |
| \(\alpha\) | 1.0, 1.1, 1.2, 1.3, 1.5 |
| \(\lambda\) | 0.3, 0.5, 0.7, 0.9 |
| \(\sigma\) | low, medium, high |

Full factorial:

\[
6\times5\times4\times3=360
\]

cells.

At five instances per cell:

\[
360\times5=1800
\]

runs per model.

## 22.3 Reduced initial design

If computationally heavy:

- fix \(\lambda=0.7\);
- fix \(\sigma=\text{medium}\);
- sweep \(\rho\times\alpha\);
- 30 cells × 5 instances = 150 runs.

Expand only after the core model is stable.

## 22.4 Phase boundary

Define:

\[
\Delta Bill(\%)=
\frac{BestBill_{P1}-BestBill_{P2}}
{BestBill_{P1}}	imes100
\]

and visualize the zero contour:

\[
\Delta Bill=0
\]

as a boundary between regions where peak-awareness changes total bill and where it does not.

A strong scientific result could be a map rather than a single “best” number.

---

# 23. RESEARCH QUESTIONS / HYPOTHESES

## RQ1 — Peak-demand Pareto structure

Does explicit peak-demand awareness produce a Pareto-efficient solution region that is not represented by the bi-objective makespan–energy-cost solution set?

Potential measurements:

- 3D Pareto coverage;
- non-dominated-solution count;
- total bill under fixed demand scenarios.

## RQ2 — Demand-charge threshold

At what demand-intensity level does peak-aware scheduling start producing a measurable economic benefit?

The threshold is **unknown before experimentation**.

## RQ3 — Energy-model fidelity

How accurately do constant-power, measured processing-power, and measured processing+startup models predict the actual physical load/energy trace?

## RQ4 — ToD sensitivity

How does increasing peak/off-peak price differential change the benefit of energy-aware and peak-aware scheduling?

## RQ5 — Edge feasibility

What instance sizes can the validated optimization workflow solve within a practical time on Raspberry Pi 5 compared with a laptop?

## RQ6 — Robustness (stretch)

How does a deterministic schedule degrade under processing-time perturbations?

Potential levels:

\[
0\%,5\%,10\%,15\%,20\%,30\%
\]

with e.g. K=100 Monte Carlo realizations.

---

# 24. HYPOTHESES — CURRENT STATUS

Earlier hypotheses, preserved but to be treated as **testable hypotheses rather than expected truths**:

### H1 — Primary

Peak-aware scheduling may produce lower simulated total electricity cost than energy-cost-only scheduling when demand-charge intensity is sufficiently high. The transition point and magnitude of benefit are unknown before experimentation.

### H2

The benefit may increase with:

- demand-charge intensity;
- ToD differential;
- workload intensity;
- machine power heterogeneity.

This is a hypothesis to test, not a conclusion.

### H3

Energy-cost-only scheduling may or may not increase peak demand relative to makespan-only scheduling, depending on workload conditions.

### H4

A model using measured machine power profiles may predict physical energy within an experimentally characterized error band.

### Previous numerical hypotheses that MUST NOT be treated as pre-validated facts

Earlier draft thresholds such as:

- “>5% savings”;
- “<10% prediction error”;
- “<3% below a tariff ratio”;
- “1% gap in 60 s on RPi”;

are useful as **pilot acceptance/experiment-design ideas**, but must not become reported results or assumed truths before measurement.

---

# 25. PHYSICAL TESTBED

## 25.1 What the testbed is

A **programmable machine-load emulation testbed** using low-voltage DC loads.

It is not a factory.

## 25.2 What it demonstrates

- physical schedule execution;
- real machine-load switching;
- measured power traces;
- measured energy;
- peak-power observation;
- simulation-to-measurement validation;
- baseline vs optimized execution behavior.

## 25.3 What it does NOT demonstrate

- industrial-machine equivalence;
- actual monthly KERC billing savings;
- factory-scale scheduling;
- unsupervised industrial operation;
- full AC power-factor behavior.

---

# 26. HARDWARE ARCHITECTURE — CURRENT CORRECTED VERSION

## 26.1 Critical correction

Earlier drafts proposed **PZEM-004T** for the testbed.

That is **incorrect for the planned 12V DC load setup** because PZEM-004T is an AC measurement device.

### Canonical measurement device

> **INA226** DC voltage/current/power monitor.

## 26.2 Components

| Component | Qty | Purpose |
|---|---:|---|
| ESP32-WROOM-32 DevKit | 1 | Controller, Wi-Fi, GPIO, I²C |
| INA226 breakout | 3 | DC V/I/P measurement |
| 4-channel relay module | 1 | Load switching |
| 12V DC motor | 1 | Machine emulator |
| 12V heater | 1 | Machine emulator |
| 12V LED strip | 1 | Machine emulator |
| Optional 4th load/fan | 1 | Extra machine emulator if required |
| 12V 10A enclosed SMPS | 1 | Low-voltage DC power |
| Breadboard + wiring | 1 | Prototyping |
| Raspberry Pi 5 | 1 | Borrowed edge optimization server |

## 26.3 Candidate INA226 addresses

Planned addresses from the current hardware document:

- sensor 1: 0x40;
- sensor 2: 0x41;
- sensor 3: 0x44.

These must be checked on the actual breakout modules before assembly; do not purchase/install without verifying the specific board's address pins and electrical specifications.

## 26.4 Safety architecture

- All primary testbed loads remain on **12V DC**.
- No mains wiring on the breadboard.
- The commercial 12V supply remains enclosed.
- Students do not open/modify the SMPS.
- Total current must remain within the supply rating.
- Switching/control circuitry must be designed so ESP32 GPIO levels do not directly carry load current.
- Use correct relay-driver logic/level shifting or MOSFET arrangements as required by the actual relay board.

## 26.5 Planned load-to-machine mapping

| Load | Machine | Candidate operating power |
|---|---|---:|
| 775-type DC motor | M1 | ~24 W |
| 12V ceramic heater | M2 | ~40 W |
| 12V LED strip | M3 | ~12 W |
| Optional fan | M4 | measure experimentally |

These power figures are **planning estimates only**. Final model parameters come from measurement.

## 26.6 Physical time mapping

One “processing operation” can be implemented as:

> relay ON for a chosen duration in physical demo time.

Earlier design:

- 1 model time unit ≈ 15 seconds on the testbed.

The mapping is time-scaled and must be documented as such.

---

# 27. HARDWARE BOM — EARLIER ESTIMATE

Earlier corrected BOM:

| Component | Qty | Approx. unit ₹ | Approx. total ₹ |
|---|---:|---:|---:|
| ESP32-WROOM-32 DevKit | 1 | 500 | 500 |
| INA226 breakout | 3 | 180 | 540 |
| 4-channel relay | 1 | 200 | 200 |
| 775 DC motor | 1 | 250 | 250 |
| 12V ceramic heater | 1 | 100 | 100 |
| 12V LED strip | 1 | 150 | 150 |
| 12V 10A SMPS | 1 | 350 | 350 |
| Breadboard + wires | 1 | 200 | 200 |
| **Approximate subtotal** | | | **₹2,290** |
| Raspberry Pi 5 | 1 | borrowed | 0 |

This is a planning estimate, not a guaranteed current-market quote. Verify parts and ratings before purchase.

---

# 28. CALIBRATION PROTOCOL

For each physical load:

## Step 1 — Steady-state processing power

- turn load ON;
- wait about 5 s for stabilization;
- sample at approximately 10 Hz for 60 s;
- record mean power and standard deviation.

## Step 2 — Idle power

If the load has a meaningful idle state:

- place in the idle state;
- sample approximately 60 s;
- record mean and standard deviation.

## Step 3 — Startup energy

- record OFF → ON transient;
- integrate power until steady-state criteria are reached;
- repeat 5 times;
- calculate mean and variance.

## Step 4 — Repeat across occasions

Repeat calibration on 3 occasions and report:

- mean;
- standard deviation;
- coefficient of variation (CoV).

## 28.1 Output file

`data/measured/machine_profiles.csv`

Suggested columns:

```csv
machine_id,P_proc_mean_W,P_proc_std_W,P_idle_mean_W,P_idle_std_W,E_start_mean_Wh,E_start_std_Wh,n_trials,date
```

---

# 29. SIMULATION ↔ HARDWARE VALIDATION

## 29.1 Predicted vs measured quantities

Compare:

- predicted power trace;
- measured power trace;
- predicted energy;
- measured energy;
- predicted peak;
- measured peak;
- timing alignment.

## 29.2 Metrics

### Energy relative error

\[
\frac{|E_{pred}-E_{meas}|}{E_{meas}}
\]

### Peak relative error

\[
\frac{|P^{peak}_{pred}-P^{peak}_{meas}|}{P^{peak}_{meas}}
\]

### MAE

\[
MAE=\frac1T\sum_t|P_{pred}(t)-P_{meas}(t)|
\]

### RMSE

\[
RMSE=\sqrt{\frac1T\sum_t(P_{pred}(t)-P_{meas}(t))^2}
\]

## 29.3 Acceptance philosophy

Do not predeclare an arbitrary target as if it were proven.

Instead:

1. quantify calibration/measurement uncertainty;
2. report prediction error;
3. compare error against uncertainty;
4. explain whether the model is adequate for the scheduling scale tested.

---

# 30. RASPBERRY PI ROLE

## 30.1 Primary justified role

> **Local optimization server / edge scheduler**

The Raspberry Pi should actually run the optimization workflow.

## 30.2 Practical secondary role

- MQTT broker (Mosquitto);
- experiment controller;
- result logger.

## 30.3 Roles that are not research contributions

- dashboard hosting;
- local database alone;
- simple IoT gateway.

## 30.4 Honest contribution statement

> The Raspberry Pi deployment demonstrates that the validated energy-aware scheduling workflow can run on low-cost edge hardware without requiring a cloud-based optimizer.

This is an engineering deployment claim, not algorithmic novelty.

## 30.5 Raspberry Pi software target

Example environment:

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv mosquitto
python3 -m venv ~/env
source ~/env/bin/activate
pip install ortools numpy pandas paho-mqtt pyyaml matplotlib
```

Use the exact supported Python/library versions chosen for reproducibility.

## 30.6 Benchmark

For the same instances, record:

\[
T_{laptop}
\]

and:

\[
T_{RPi}
\]

and optionally the simple ratio:

\[
R=\frac{T_{RPi}}{T_{laptop}}
\]

Do not interpret the ratio as a measure of algorithmic quality; it is an edge-deployment benchmark.

---

# 31. END-TO-END ARCHITECTURE

```text
                ┌───────────────────────────────┐
                │ Real tariff + model inputs    │
                │ Jobs / machines / power data  │
                └───────────────┬───────────────┘
                                │
                                ▼
                 ┌───────────────────────────┐
                 │      Raspberry Pi 5       │
                 │                           │
                 │ instance + tariff loader  │
                 │ scheduling model builder  │
                 │ OR-Tools CP-SAT            │
                 │ ε-constraint/AUGMECON     │
                 │ Pareto evaluation         │
                 │ experiment controller     │
                 │ MQTT broker/logging        │
                 └─────────────┬─────────────┘
                               │ MQTT
                               ▼
                 ┌───────────────────────────┐
                 │           ESP32            │
                 │ schedule execution        │
                 │ relay control              │
                 │ INA226 acquisition         │
                 │ timing/state reporting     │
                 └─────────────┬─────────────┘
                               │
             ┌─────────────────┼─────────────────┐
             ▼                 ▼                 ▼
          Load/M1           Load/M2           Load/M3
          motor              heater             LED
             │                 │                 │
             └───────────── measurements ───────┘
                               │
                               ▼
                        Raspberry Pi logs
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
        predicted trace                 measured trace
                │                             │
                └──────────────┬──────────────┘
                               ▼
                    model validation / plots
```

---

# 32. OPTIMIZATION LOOP

## Core Level 2 — Open-loop

```text
input
 ↓
optimize
 ↓
schedule
 ↓
execute
 ↓
measure
 ↓
compare
```

No re-optimization during execution.

## Level 4 — Stretch closed-loop

```text
input
 ↓
optimize
 ↓
execute
 ↓
measure state
 ↓
detect deviation
 ↓
re-optimize remaining schedule
 ↓
execute remainder
```

---

# 33. DATA CLASSIFICATION

## REAL / MEASURED

- processing power;
- idle power;
- startup energy;
- actual power traces;
- actual energy per schedule execution;
- actual peak power;
- actual ON/OFF timing.

## MODELLED FROM REAL-WORLD SOURCES / DESIGN

- job precedence;
- processing times;
- machine eligibility;
- deadlines;
- tariff rates;
- demand-charge parameters;
- scheduling horizon.

## SIMULATED

- large-scale instances;
- sensitivity sweeps;
- uncertainty scenarios;
- solver scalability experiments beyond physical capability.

The distinction is critical in the report.

---

# 34. SOFTWARE ARCHITECTURE

Recommended project directory:

```text
energy_scheduling/
├── README.md
├── requirements.txt
├── config/
│   ├── default_config.yaml
│   └── tariff_profiles/
│       ├── kerc_ht2a.yaml
│       └── parametric.yaml
├── data/
│   ├── instances/
│   │   ├── small/
│   │   ├── medium/
│   │   └── large/
│   └── measured/
│       ├── machine_profiles.csv
│       └── calibration_logs/
├── src/
│   ├── __init__.py
│   ├── model/
│   │   ├── __init__.py
│   │   ├── instance.py
│   │   ├── tariff.py
│   │   └── solution.py
│   ├── solver/
│   │   ├── __init__.py
│   │   ├── cpsat_model.py
│   │   ├── epsilon_constraint.py
│   │   └── baselines.py
│   ├── evaluation/
│   │   ├── __init__.py
│   │   ├── metrics.py
│   │   ├── pareto.py
│   │   └── statistics.py
│   ├── generators/
│   │   ├── __init__.py
│   │   └── instance_generator.py
│   └── visualization/
│       ├── __init__.py
│       ├── gantt.py
│       ├── pareto_plot.py
│       ├── sensitivity_plot.py
│       └── power_trace.py
├── experiments/
│   ├── exp_a_baseline.py
│   ├── exp_b_biobj_pareto.py
│   ├── exp_c_triobj_vs_biobj.py
│   ├── exp_d_demand_charge.py
│   ├── exp_e_tod_sensitivity.py
│   ├── exp_f_workload.py
│   ├── exp_g_heterogeneity.py
│   ├── exp_h_scalability.py
│   ├── exp_i_model_fidelity.py
│   ├── exp_j_physical.py
│   └── run_all.py
├── hardware/
│   ├── esp32/
│   │   └── firmware.ino
│   ├── calibration/
│   │   └── calibrate.py
│   └── testbed_controller.py
├── deployment/
│   ├── rpi_setup.sh
│   └── benchmark.py
├── results/
│   ├── raw/
│   ├── processed/
│   └── plots/
└── tests/
    ├── test_model.py
    ├── test_solver.py
    ├── test_baselines.py
    └── test_metrics.py
```

## 34.1 Core dataclasses

Candidate structure:

```python
from dataclasses import dataclass

@dataclass
class Operation:
    job_id: int
    op_index: int
    eligible_machines: list[int]
    processing_time: int

@dataclass
class Machine:
    machine_id: int
    power_processing_w: float
    power_idle_w: float
    startup_energy_wh: float

@dataclass
class TariffSlot:
    slot_index: int
    price_per_kwh: float

@dataclass
class Instance:
    name: str
    jobs: list[list[Operation]]
    machines: list[Machine]
    tariff_slots: list[TariffSlot]
    demand_charge_rate: float
    time_slot_width_hours: float
    horizon: int
    deadlines: dict[int, int] | None = None
    seed: int = 0
```

The data model must be revised after the literature-based mathematical formulation is frozen.

## 34.2 Result schema

Suggested CSV fields:

```text
experiment_id,
instance_name,
method,
makespan,
energy_cost,
peak_power_w,
total_bill,
solve_time_s,
solver_status,
optimality_gap,
seed,
timestamp
```

Add relevant tariff/sensitivity identifiers when needed.

---

# 35. REQUIRED UNIT TESTS

Before large experiments, test:

- every operation scheduled exactly once;
- machine overlap never occurs;
- precedence always respected;
- start/end arithmetic is correct;
- machine assignment is valid;
- slot-overlap calculation is correct;
- slot power equals sum of active machine powers;
- peak equals maximum slot power;
- energy equals manual \(\sum P\Delta t\);
- tariff slot mapping is correct;
- ToD adjustments are correct for each season/period;
- real KERC billing-demand calculation is correct;
- normalized \(\rho\) model is distinct from KERC billing model;
- Pareto dominance filtering is correct;
- duplicate solution handling is correct.

---

# 36. HAND-VERIFICATION REQUIREMENT

The model must be validated on tiny instances **before** large coding/experiments.

Minimum sequence:

```text
2×2 or 3×2 instance
      ↓
manual schedule enumeration / hand calculation
      ↓
manual makespan
manual energy
manual tariff cost
manual peak
      ↓
Python evaluator
      ↓
CP-SAT
      ↓
all results agree
```

Canonical gate:

> **Hand solution = independent evaluator = solver result**

If these disagree, do not proceed to large experiments.

---

# 37. FIRST 10 ACTIONS — ORIGINAL MASTER PLAN

These are preserved because they define the original implementation entry point:

### Action 1 — Install OR-Tools and verify

```bash
pip install ortools numpy pandas pyyaml matplotlib scipy
python -c "from ortools.sat.python import cp_model; print('CP-SAT OK')"
```

### Action 2 — Create project directory structure

```bash
mkdir -p energy_scheduling/{config/tariff_profiles,data/{instances/{small,medium,large},measured/calibration_logs},src/{model,solver,evaluation,generators,visualization},experiments,hardware/{esp32,calibration},deployment,results/{raw,processed,plots},tests,docs}
cd energy_scheduling && git init
```

### Action 3 — Implement instance data model

Create:

- `src/model/instance.py`
- `src/model/tariff.py`

### Action 4 — Build a 2×2 test instance by hand

Create:

`data/instances/small/test_2x2.csv`

and hand-calculate the optimal makespan/Gantt chart.

### Action 5 — Implement M0 makespan-only CP-SAT

Use interval variables, precedence and `AddNoOverlap`.

### Action 6 — Implement FCFS and SPT

Verify both produce valid schedules.

### Action 7 — Add energy-cost accounting

Use a simple two-price tariff first, e.g. 5 vs 8 ₹/kWh, for debugging.

### Action 8 — Add peak-demand model

Add `peak_power` and verify against the hand-drawn Gantt chart.

### Action 9 — Implement 2-objective ε-constraint

Start with 3×2 or similar small instance and a small ε-grid.

### Action 10 — Verify/document KERC tariff

**Important current update:** this action is already substantially complete because the actual KERC tariff order has been uploaded and checked. The remaining work is to create the final canonical tariff configuration using the verified values in Section 8.

---

# 38. REVISED IMMEDIATE EXECUTION ORDER

Because the mathematical foundation is now explicitly literature-driven, the preferred sequence is **not** simply to start coding immediately.

## Step 0 — Freeze current project scope

Confirm:

- research question;
- target Level 2 scope;
- no algorithmic novelty claim;
- static/open-loop core;
- hardware as validation, not factory replacement.

## Step 1 — Literature-to-model audit

Find and verify 15–20 candidate papers; select 5–8 foundations.

## Step 2 — Decide scheduling class

Choose parallel-machine, job-shop or flexible job-shop based on:

- actual project assumptions;
- strongest literature basis;
- implementation feasibility.

## Step 3 — Write `docs/MATHEMATICAL_FOUNDATION_v1.md`

Required sections:

1. problem definition;
2. selected literature;
3. notation;
4. decision variables;
5. objectives;
6. constraints;
7. energy model;
8. ToD model;
9. peak model;
10. KERC mapping;
11. multi-objective method;
12. assumptions;
13. hand-worked example;
14. literature-origin matrix.

## Step 4 — Derive a tiny hand-solvable example

Prefer 2–3 jobs, 2 machines initially.

## Step 5 — Implement an independent evaluator

Before optimizing, make sure a schedule can be evaluated independently for:

- makespan;
- energy;
- ToD cost;
- peak;
- normalized bill;
- KERC reference bill under stated assumptions.

## Step 6 — Implement M0 CP-SAT

Match the hand result.

## Step 7 — Implement M1 energy cost

Match manual energy calculations.

## Step 8 — Implement peak

Match manual peak.

## Step 9 — Implement baselines

FCFS + SPT + makespan-only + energy-only.

## Step 10 — Implement ε-constraint / Pareto generation

First 2D, then 3D.

## Step 11 — Validate all computational modules

Only after tests pass should the research experiment generator be scaled.

## Step 12 — Run Experiments A–C

These establish whether the core phenomenon exists before the full parameter sweep.

## Step 13 — Run D–G sensitivity analysis

Generate the phase map.

## Step 14 — Hardware order/assembly/calibration

Can proceed in parallel after the core computational structure is stable, but do not let hardware delay mathematical validation.

## Step 15 — Physical validation

Run model-fidelity and physical comparison experiments.

## Step 16 — Raspberry Pi deployment/benchmark

Move the validated pipeline to the Pi.

## Step 17 — Report/poster/demo

Only after the evidence is complete.

---

# 39. FAILURE MODES AND RESPONSES

| Failure | Likely cause | Response |
|---|---|---|
| CP-SAT infeasible | ε bound too tight | mark cell infeasible, continue grid, document |
| CP-SAT timeout | instance too large | increase pilot limit, reduce size, report gap |
| Few Pareto points | coarse grid / objectives not conflicting | refine grid; verify model |
| All methods produce same bill | demand/ToD effects too weak | treat as valid result; analyze conditions |
| Slot-overlap bug | incorrect interval↔slot mapping | hand-check on tiny instances |
| Wrong tariff result | incorrect season/period mapping | unit test tariff slot function against order |
| kW/kVA confusion | DC testbed mapped directly to industrial bill | separate scheduling peak from tariff billing demand |
| INA226 reads zero | wiring/address issue | I²C scan, wiring inspection, module replacement |
| Relay fails | GPIO/logic incompatibility | verify board driver, use suitable level-shift/driver/MOSFET |
| MQTT drops | network/broker problem | restart/check broker; serial fallback if necessary |
| Measured power much higher than predicted | poor calibration / load behavior | recalibrate and update model assumptions |
| Measured power much lower | partial load / switching issue | inspect relay/load and calibration |
| RPi too slow | ARM compute limitations | reduce instance size; report limitation |
| Timing drift | software clock drift | hardware timing / synchronization / documented uncertainty |
| Supply overloaded | aggregate current exceeds rating | calculate total load; stagger operation or upgrade supply |
| Constraints wrong | model bug | test suite + hand examples |
| Instances trivial | too much slack | adjust workload intensity / horizon |
| Peak-awareness appears useless | peak range too small / workload lacks overlap | treat as a valid result and characterize boundary |
| Physical testbed not representative | simple loads | explicitly frame as emulation; do not overclaim |

---

# 40. PROJECT LIMITATIONS — MUST BE DISCLOSED

1. **Testbed is not a factory.**
2. Loads are emulators, not CNC/industrial machines.
3. Processing times are deterministic in the core model.
4. Machine breakdowns are excluded.
5. Dynamic job arrival is excluded.
6. The core scheduler is static/open-loop.
7. The largest physical experiment is limited by the number of controllable loads.
8. Simulation extends beyond physical scale.
9. DC measurement does not fully represent industrial AC power factor behavior.
10. Real KERC demand billing is monthly and in kVA; short-run experiments do not replicate monthly billing mechanics.
11. Results are tariff-specific unless additional tariff regimes are studied.
12. Edge solver performance depends on the specific Raspberry Pi and software build.
13. Exact literature-gap claims remain subject to ongoing search limitations.
14. Any unmodeled tariff components must be explicitly listed as exclusions in the report.

---

# 41. REPRODUCIBILITY REQUIREMENTS

Git structure:

```text
energy-scheduling/
├── .gitignore
├── README.md
├── requirements.txt
├── config/
├── data/instances/
├── data/measured/
├── src/
├── experiments/
├── hardware/
├── deployment/
├── results/
├── tests/
└── docs/
```

## Required reproducibility metadata

- pinned package versions;
- random seeds;
- CP-SAT random seed;
- instance-generation seed;
- tariff version;
- experiment identifier;
- timestamp;
- solver status;
- optimality gap where available;
- calibration date;
- hardware configuration.

## Results policy

Save raw results as CSV.

Do not overwrite original raw measurements.

Keep processed results derived from raw files.

---

# 42. END-TO-END COMPUTATIONAL + PHYSICAL WORKFLOW

```text
1. Define instance
2. Load KERC / parametric tariff
3. Build schedule model
4. Run FCFS/SPT
5. Run makespan-only solver
6. Run energy-only solver
7. Generate bi-objective Pareto set
8. Generate tri-objective Pareto set
9. Evaluate all solutions in common 3D space
10. Compute scenario-specific bill
11. Aggregate matched-instance statistics
12. Sweep tariff/workload/power parameters
13. Generate phase maps
14. Select representative schedules
15. Calibrate hardware loads
16. Execute selected schedules physically
17. Measure power/energy/peak
18. Compare predicted vs measured
19. Benchmark on laptop vs Raspberry Pi
20. Generate report/poster/demo evidence
```

---

# 43. 5-MINUTE DEMO CONCEPT

## Setup

Display:

- 3–4 controllable loads;
- INA226 readings;
- ESP32 state;
- Raspberry Pi optimization screen;
- schedule/Gantt visualization;
- live power trace.

## Suggested script

### 1. Establish the problem

Show a baseline FCFS schedule.

### 2. Show baseline power

Run or replay the load schedule and show power overlap.

### 3. Run optimizer

On the Raspberry Pi, solve for an energy/peak-aware schedule.

### 4. Show altered schedule

Highlight how operations moved to different periods or were staggered.

### 5. Execute physically

ESP32 switches the loads.

### 6. Show measured result

Display:

| Metric | Baseline | Optimized |
|---|---:|---:|
| Makespan | ___ | ___ |
| Energy | ___ | ___ |
| Energy cost | ___ | ___ |
| Peak | ___ | ___ |
| Scenario bill | ___ | ___ |
| Solver time | ___ | ___ |

### 7. State evidence carefully

Do not say “the method always wins.” Say what the experiment actually demonstrated.

---

# 44. PROJECT TIMELINE

## One-week emergency path

| Day | Work | Output |
|---|---|---|
| 1 | environment, data model, tiny instances | working setup |
| 2 | M0 | hand-verified solver |
| 3 | energy + FCFS/SPT | first comparison |
| 4 | 2D ε-constraint | Pareto front |
| 5 | peak + tri-objective | 3D points |
| 6 | instance generator + Exp A | baseline dataset |
| 7 | Exp C + small demand sweep | first research result |

## Four-week realistic path

| Week | Focus |
|---|---|
| 1 | M0–M3, baselines, tests, generator |
| 2 | Experiments A–E, statistics |
| 3 | Hardware assembly/calibration/validation |
| 4 | Experiments F–G, phase map, RPi, report draft |

## Eight-week complete path

| Week | Focus |
|---|---|
| 1 | literature + tariff + formulation |
| 2 | solver/model implementation |
| 3 | ε-constraint/Pareto |
| 4 | Experiments A–C |
| 5 | D–G sensitivity |
| 6 | hardware + calibration |
| 7 | physical validation + RPi |
| 8 | report/poster/final polish |

## Longer contingency plan

Earlier plan also allowed:

- weeks 9–10: uncertainty experiments if the core is finished;
- weeks 10–12: report, poster, presentation completion.

---

# 45. DEFINITION OF DONE

The project is not “done” merely because a demo works.

### Literature

- [ ] 15–20 candidate papers collected.
- [ ] 5–8 foundational papers verified.
- [ ] Exact mathematical origins recorded.
- [ ] Research gap claim supported with primary sources.

### Tariff

- [ ] KERC tariff order archived.
- [ ] HT-2(a) verified.
- [ ] FY2026–27 values recorded.
- [ ] ToD table implemented and unit-tested.
- [ ] Billing-demand rule implemented or explicitly excluded from the optimization model.
- [ ] kW/kVA distinction documented.

### Mathematics

- [ ] Problem class frozen.
- [ ] Variables defined.
- [ ] Objectives defined.
- [ ] Constraints justified.
- [ ] Energy equation traced to literature/physics.
- [ ] Peak equation traced to literature.
- [ ] ε-constraint method justified.
- [ ] Assumptions documented.
- [ ] Hand verification complete.

### Software

- [ ] M0 correct.
- [ ] M1 correct.
- [ ] Peak model correct.
- [ ] P1/P2 Pareto generation correct.
- [ ] Baselines correct.
- [ ] Unit tests pass.
- [ ] Instance generator reproducible.

### Experiments

- [ ] A complete.
- [ ] B complete.
- [ ] C complete.
- [ ] D complete.
- [ ] E complete.
- [ ] F complete.
- [ ] G complete.
- [ ] H complete.
- [ ] I complete.
- [ ] J complete.

### Physical

- [ ] Testbed assembled.
- [ ] Calibration complete.
- [ ] Measurement uncertainty characterized.
- [ ] Physical schedule execution works.
- [ ] Predicted vs measured error reported.

### Raspberry Pi

- [ ] Solver runs on Pi.
- [ ] Same instances benchmarked on laptop and Pi.
- [ ] Edge benchmark results recorded.

### Documentation

- [ ] Raw results saved.
- [ ] Plots generated.
- [ ] Limitations documented.
- [ ] Novelty claims are honest.
- [ ] README works.
- [ ] requirements.txt pinned.
- [ ] poster complete.
- [ ] PPT complete.
- [ ] final report complete.

---

# 46. FINAL DECISION FROM THE EARLIER HOSTILE AUDIT

The earlier independent validation concluded:

> **MODIFY then GO**

The project was considered:

- mathematically rigorous enough for undergraduate research if implemented carefully;
- a genuine but narrow research-gap study;
- experimentally falsifiable;
- feasible with open-source tools;
- physically demonstrable;
- reproducible;
- directly aligned with SDG 9.4 / sustainable industrialization.

The major modifications required were:

1. no algorithmic-novelty claim;
2. explicit peak-demand layer;
3. physical testbed;
4. sensitivity analysis;
5. correct solver terminology;
6. Raspberry Pi used meaningfully as an optimizer rather than decoration.

---

# 47. DECISION LOG / IMPORTANT CORRECTIONS

## Decision 1 — Project direction

**Selected:** peak-aware energy-cost production scheduling.

## Decision 2 — Research contribution framing

**Selected:** empirical + engineering integration / physical validation.

**Rejected:** algorithmic novelty claim.

## Decision 3 — Static vs adaptive

**Core:** static/open-loop.

**Stretch:** rolling-horizon adaptive scheduling only after core completion.

## Decision 4 — Measurement device

**Old:** PZEM-004T.

**Correction:** INA226 because the planned testbed uses DC loads.

## Decision 5 — Tariff source

**Old:** approximate web summaries / annual report values.

**Current:** actual uploaded KERC Tariff Order 2025 All ESCOMs.

## Decision 6 — Tariff year

**Current reference:** FY2026–27, effective 1 April 2026.

## Decision 7 — HT-2(a) tariff values

**Current verified:** ₹350/kVA/month demand + ₹6.60/kWh energy.

## Decision 8 — Billing demand

**Current verified:**

\[
BD=\max(MD,0.90CD)
\]

plus rounding and excess-demand rules.

## Decision 9 — ToD

Use actual KERC ToD table, with seasonal structure and contract-demand applicability.

## Decision 10 — Demand sensitivity

Use normalized \(\rho\) as a research parameter, clearly separate from actual KERC ₹/kVA/month demand billing.

## Decision 11 — Solver

**Current:** OR-Tools CP-SAT.

## Decision 12 — Multi-objective method

**Current:** ε-constraint / AUGMECON-style Pareto generation, with solver-status caveat.

## Decision 13 — Hypervolume

Use **common evaluation space** before comparing P1 and P2 Pareto solutions.

## Decision 14 — Arbitrary thresholds

Removed from “known outcome” status. Determine empirically.

## Decision 15 — Hardware role

RPi is an edge optimization server and controller, not the research novelty itself.

---

# 48. WHAT WE SHOULD DO NEXT — IMMEDIATE CHECKLIST

### A. Literature-to-model audit

**Do this first.**

1. Run the Gemini 3.1 Pro High literature prompt.
2. Obtain 15–20 candidate papers.
3. Verify DOIs and original PDFs.
4. Reduce to 5–8 foundational papers.
5. Extract exact equations/pages.
6. Build the literature-to-equation matrix.

### B. Mathematical foundation

1. Decide exact scheduling class.
2. Freeze notation.
3. Map every equation to literature/derivation/assumption.
4. Hand-solve the tiny example.
5. Write `MATHEMATICAL_FOUNDATION_v1.md`.

### C. Software

1. Build independent schedule evaluator.
2. Implement M0.
3. Implement M1.
4. Implement peak.
5. Implement baselines.
6. Implement ε-constraint/Pareto.
7. Build tests.

### D. Research experiments

1. Run A–C first.
2. Validate whether the phenomenon exists.
3. Run D–G sensitivity.
4. Run H scalability.

### E. Hardware

1. Verify actual INA226 boards and addresses.
2. Verify relay electrical interface.
3. Assemble only low-voltage DC hardware.
4. Calibrate.
5. Run physical schedule validation.

### F. Edge deployment

1. Install software on Pi.
2. Benchmark identical instances.
3. Demonstrate schedule generation on Pi.
4. Send schedule to ESP32.

---

# 49. SOURCE FILE INVENTORY

The project currently has these major uploaded/generated project documents available in the working environment:

| File | Purpose |
|---|---|
| `tarif order.pdf` | **Official KERC Tariff Order 2025 All ESCOMs — canonical tariff source** |
| `energy_scheduling_full_validation.md` | Hostile-evaluator research validation and novelty/gap audit |
| `master_execution_plan.md` | Detailed project execution plan |
| `energy_scheduling_math_research_validation.md` | Mathematical/engineering-depth audit |
| `energy_scheduling_research_validation.md` | Expanded research validation |
| `sdg9_project_analysis.md` | SDG-9 rubric analysis and initial idea generation |
| `sdg9_project_audit.md` | Independent SDG-9 audit and candidate comparison |
| `media_to_upload1765180920.pdf` | KERC 26th Annual Report 2024–25; useful contextual source, superseded by the actual tariff order for exact tariff values |

---

# 50. PRESERVED SOURCE ARCHIVE

The following source documents are preserved verbatim after this point for traceability and to ensure that no minor planning detail is lost. **They are historical/source records. The canonical corrections in Sections 0–49 take precedence where a source document contains an outdated estimate, terminology error, or superseded hardware choice.**

---

## APPENDIX A — `energy_scheduling_full_validation.md`

# Energy-Aware Manufacturing Scheduling — Research Validation

> **Date:** 2026-10-02  
> **Posture:** Hostile evaluator. No manufactured novelty. No unsupported claims.  
> **Standard:** Every claim must earn its classification.

---

## TASK 1 — Literature Research

### 1.1 Search methodology

Searched: Google Scholar, IEEE Xplore (via Scholar indexing), ScienceDirect, MDPI, SpringerLink, arXiv, ResearchGate. Terms: energy-aware scheduling, multi-objective job-shop, ToU scheduling, peak-demand scheduling, robust scheduling, rolling-horizon manufacturing, measured power scheduling, edge computing scheduling, MSME energy, closed-loop scheduling.

**Limitation:** No direct IEEE Xplore or ACM DL API access. Some papers may be missed. Absence of evidence ≠ evidence of absence.

### 1.2 Evidence table

| # | Work / Area | Model | Objectives | Uncertainty? | Measured power? | Physical execution? | Key limitation |
|---|---|---|---|---|---|---|---|
| 1 | Mouzon et al. (2007, IIE Trans.) | Single-machine ON/OFF MILP | Energy | No | No | No | Single machine; no ToU; foundational |
| 2 | Gahm et al. (2016, EJOR) | Survey: 100+ papers | Various | Rarely | Rarely | No | Pre-2016 snapshot; most work deterministic |
| 3 | Machine-state MILP (MDPI 2023–24) | Job-shop + idle/startup states | Makespan + Energy | No | No | No | Standard formulation; Western tariffs |
| 4 | Period-indexed ToU MILP (SciTePress 2024) | ToU-aware scheduling | Energy cost | No | No | No | Computational-only |
| 5 | Multi-obj green scheduling (MDPI 2023) | Bi-obj FJSP | Makespan + Energy | No | No | No | NSGA-II on benchmarks only |
| 6 | AUGMECON ε-constraint studies (2022–24) | Multi-obj MILP | Cost + Emissions (+ Peak in some) | Rarely | No | No | Peak as objective exists but is less explored in manufacturing scheduling specifically |
| 7 | DRL + rolling horizon (MDPI 2024) | Dynamic scheduling MDP | Makespan + Energy | Machine breakdown | Digital twin | Simulated | Complex; not student-feasible |
| 8 | Robust FJSP (Atlantis Press 2024) | Robust MILP / scenario-based | Makespan robustness | Processing time | No | No | No energy awareness |
| 9 | Energy + production co-scheduling (arXiv 2024) | MILP with decision-dependent uncertainty | Cost | Energy price | No | Simulation | Advanced; limited applicability |
| 10 | MPC-based scheduling (arXiv 2024) | Receding horizon QP/MILP | Energy cost | Price volatility | No | Simulation | Requires real-time solver |
| 11 | Event-based load disaggregation (GI.de 2024) | Data-driven power profiling | Accuracy | N/A | **Yes** — measured | Lab testbed | Profiling only, not scheduling |
| 12 | Demand charge peak shaving (various 2022–24) | MILP with P_peak variable | Energy + Demand charge | Some (BESS) | Mixed | Mostly simulation | Focus on building/grid, not production scheduling |
| 13 | RPi edge scheduling (various 2024) | CP-SAT / lightweight heuristics | Various | Limited | No | Some lab demos | Performance-limited vs desktop |
| 14 | India ToD tariff rules (MoP, April 2024) | Regulatory — not academic | N/A | N/A | N/A | N/A | Mandatory ToD for ≥10 kW; demand charges documented |

### 1.3 What is already solved

These are `[ESTABLISHED]` and should not be claimed as contributions:

1. **Bi-objective makespan + energy MILP** — Solved since Mouzon (2007), refined extensively.
2. **Machine-state energy models** (idle/processing/startup/off) — Standard since ~2016.
3. **ε-constraint and NSGA-II/III for Pareto fronts** — Textbook multi-objective methodology.
4. **ToU-aware scheduling** — Dozens of papers; standard formulation.
5. **Job-shop scheduling NP-hardness and solver behavior** — Well-characterised.
6. **PZEM-004T + ESP32 power monitoring** — Widely documented hobbyist/industrial pattern.
7. **MQTT + Raspberry Pi + dashboard** — Standard IoT stack. Not research.
8. **Demand charge peak-shaving formulation** (P_peak ≥ Σ P_m(t)) — Standard in energy systems literature.

### 1.4 What is less studied (genuine gaps)

These are `[OBSERVED GAP]` with varying confidence:

1. **Tri-objective manufacturing scheduling (makespan + energy cost + peak demand) with systematic Pareto surface analysis** — Peak demand as explicit objective in *production scheduling* (not building energy or microgrid) is less explored than bi-objective. Multiple papers mention it, but rigorous 3D Pareto analysis with sensitivity to tariff parameters is uncommon. **Confidence: Moderate.**

2. **Physical execution of an energy-aware schedule on a testbed with measured validation** — Virtually all papers use simulation or benchmark instances. Papers that measure real machine power exist, but papers that *execute the optimized schedule physically and compare predicted vs. actual energy* are rare. **Confidence: High.**

3. **Systematic study of when peak-awareness matters and when it doesn't** — No paper I found produces a sensitivity map showing: "Peak-demand awareness provides X% bill reduction when demand charges are Y ₹/kVA and tariff differential is Z." This parametric analysis is absent. **Confidence: Moderate-High.**

4. **Static vs. adaptive scheduling comparison with energy objectives on a physical testbed** — Comparisons exist in simulation/DRL contexts, but not on student-scale physical systems with measured feedback. **Confidence: Moderate.**

### 1.5 Honesty check

None of these gaps constitute algorithmic novelty. They are:
- Extensions of existing formulations to a third objective
- Empirical/validation studies that close the simulation-to-reality gap
- Parametric sensitivity analyses that characterise when a method is useful

This is honest, defensible undergraduate work. It is **not** a new algorithm, **not** a new mathematical technique, and **not** a breakthrough. Framing it otherwise would be dishonest.

---

## TASK 2 — Mathematical Research Gap

### 2A. Peak-aware scheduling: Is there a real research question?

**The claim to investigate:** Adding peak demand as a third objective changes the Pareto front in a non-trivial way.

**Why this might be true:**
- `[ESTABLISHED]` Indian industrial tariffs have two components: energy charges (kWh × ToD rate) and demand charges (peak kVA × ₹/kVA/month).
- `[ESTABLISHED]` Demand charges are 30%+ of industrial bills in many Indian states.
- `[INFERENCE]` Minimising energy cost alone can *increase* peak demand. Example: if all energy-intensive operations are packed into cheap off-peak slots, they overlap and create a power spike. The energy charge drops, but the demand charge rises.
- `[HYPOTHESIS]` There is a structural trade-off between energy cost and peak demand that produces a distinct Pareto surface region: schedules exist that slightly increase total kWh cost but substantially reduce peak demand, lowering the total bill.

**Why this might be false:**
- If the machine count is small (3–5), the peak power range is narrow, and the demand charge component may be negligible.
- If processing times are short relative to time slots, there is little overlap.
- If tariff differential is small, energy-aware scheduling itself provides little benefit.

**Verdict:** This is a testable hypothesis, not an assumed truth. The research question is: *Under what conditions does peak-demand awareness provide meaningful total-bill reduction beyond energy-cost-only optimization?* The answer "it doesn't matter for small systems" is a valid finding.

### 2B. Uncertainty: Is it feasible?

**Scenario-based robust scheduling** (sample K scenarios of processing time, solve a min-max or expectation formulation) is conceptually straightforward but:

- Multiplies MILP complexity by K.
- Requires distributional assumptions (what distribution do processing times follow?).
- Validation requires running the perturbed instances — feasible computationally but hard to replicate physically.

**Verdict:** Feasible as a computational experiment (Monte Carlo perturbation of the deterministic solution). NOT feasible as a full stochastic MILP for undergraduates. Suitable for Level 3 (stretch), not core.

### 2C. Static vs. Adaptive: Is there a real research question?

**The ideal experiment:**
1. Generate static schedule S*.
2. Execute S* on testbed.
3. Inject perturbation (e.g., delay one machine by 2 time slots).
4. Measure the degradation in cost/peak/makespan.
5. Generate adaptive schedule S'_t by re-solving with updated state.
6. Compare S* degraded vs. S'_t adapted.

**Why this is valuable:** It directly answers whether re-optimization after disruption helps — a question most papers answer only in simulation.

**Why this is risky:** 
- Implementation complexity is high (state estimation, trigger logic, solver speed).
- On a small testbed with 3 machines, the adaptation may be trivial (just swap two operations).
- The improvement may be too small to detect statistically.

**Verdict:** Genuine research question but HIGH risk for undergraduates. Reserve for Level 4. The core project must not depend on this.

### 2D. The strongest research question (synthesis)

After analysing all three directions, the strongest mathematically defensible and undergraduate-feasible research question is:

> **Under realistic industrial tariff structures with demand charges, does peak-demand-aware multi-objective scheduling produce a structurally different Pareto front and lower total electricity bill compared to energy-cost-only scheduling — and under what tariff conditions does this benefit become significant?**

This is:
- Mathematically precise (Pareto analysis, hypervolume comparison, sensitivity)
- Falsifiable (null hypothesis: no significant difference)
- Parameterically rich (can sweep demand-charge rate, tariff ratio, workload intensity)
- Physically validatable (execute both schedules on testbed, measure actual peak and cost)
- Feasible with standard tools (MILP + AUGMECON + Gurobi/OR-Tools)

It is NOT:
- A new algorithm
- A new solver
- A new heuristic

It IS:
- An extended formulation study with systematic empirical analysis
- An experimental comparison with physical validation

---

## TASK 3 — Mathematical Formulation

### Sets

| Symbol | Definition |
|---|---|
| $\mathcal{J} = \{1, \ldots, n\}$ | Jobs |
| $\mathcal{O}_j = \{1, \ldots, n_j\}$ | Operations of job $j$ (ordered) |
| $\mathcal{M} = \{1, \ldots, m\}$ | Machines |
| $\mathcal{T} = \{1, \ldots, H\}$ | Discrete time slots of width $\Delta$ |
| $\mathcal{M}_o \subseteq \mathcal{M}$ | Eligible machines for operation $o$ |

### Parameters

| Symbol | Definition | Source |
|---|---|---|
| $p_o$ | Processing time of operation $o$ (in time slots) | Modelled / estimated |
| $P^{\text{proc}}_m$ | Processing power draw of machine $m$ (W) | **Measured** via PZEM-004T |
| $P^{\text{idle}}_m$ | Idle power draw of machine $m$ (W) | **Measured** |
| $E^{\text{start}}_m$ | Startup energy of machine $m$ (Wh) | **Measured** |
| $\pi_t$ | Electricity price in slot $t$ (₹/kWh) | From SERC tariff order |
| $\rho$ | Demand charge rate (₹/kW/month) | From SERC tariff order |
| $d_j$ | Deadline for job $j$ (time slot) | Modelled |
| $\Delta$ | Time slot width (hours) | Design choice (e.g., 0.25 h = 15 min) |

### Decision variables

| Variable | Domain | Meaning |
|---|---|---|
| $x_{omt}$ | $\{0,1\}$ | Operation $o$ starts on machine $m$ at time $t$ |
| $y_{mt}$ | $\{0,1\}$ | Machine $m$ is processing during slot $t$ |
| $w_{mt}$ | $\{0,1\}$ | Machine $m$ is idle (on, not processing) during slot $t$ |
| $z_{mt}$ | $\{0,1\}$ | Machine $m$ has a startup transition at slot $t$ |
| $C_{\max}$ | $\mathbb{R}^+$ | Makespan |
| $P^{\text{peak}}$ | $\mathbb{R}^+$ | Peak total power over all time slots |

### Objective functions

**F1 — Makespan:**

$$\min\ C_{\max}$$

**F2 — Electricity cost (energy charge only):**

$$\min\ \sum_{t \in \mathcal{T}} \sum_{m \in \mathcal{M}} \Big[ P^{\text{proc}}_m \cdot y_{mt} + P^{\text{idle}}_m \cdot w_{mt} + \tfrac{E^{\text{start}}_m}{\Delta} \cdot z_{mt} \Big] \cdot \pi_t \cdot \Delta$$

**F3 — Peak power:**

$$\min\ P^{\text{peak}}$$

**Total bill (for evaluation, not directly optimised):**

$$\text{Bill} = F2 + \rho \cdot P^{\text{peak}}$$

### Constraints

**C1 — Assignment:** Each operation assigned exactly once.
$$\sum_{m \in \mathcal{M}_o} \sum_{t \in \mathcal{T}} x_{omt} = 1 \qquad \forall\ o$$

**C2 — Precedence:** Operations within a job respect ordering.
$$\sum_{m,t} x_{o_k m t} \cdot (t + p_{o_k}) \leq \sum_{m,t} x_{o_{k+1} m t} \cdot t \qquad \forall\ j,\ k < n_j$$

(Note: this constraint is bilinear in the general form. For time-indexed formulations, it linearises because $x_{omt}$ selects a unique $t$.)

**C3 — No overlap:** At most one operation on each machine at any time.
$$\sum_{o : m \in \mathcal{M}_o}\ \sum_{\tau=\max(1,t-p_o+1)}^{t} x_{om\tau} \leq 1 \qquad \forall\ m,\ t$$

**C4 — Processing state link:**
$$y_{mt} = \sum_{o : m \in \mathcal{M}_o}\ \sum_{\tau=\max(1,t-p_o+1)}^{t} x_{om\tau} \qquad \forall\ m,\ t$$

**C5 — State exclusivity:**
$$y_{mt} + w_{mt} \leq 1 \qquad \forall\ m,\ t$$

(Machine is either processing, idle, or off. Off is the implicit third state: $1 - y_{mt} - w_{mt}$.)

**C6 — Startup detection:**
$$z_{mt} \geq (y_{mt} + w_{mt}) - (y_{m,t-1} + w_{m,t-1}) \qquad \forall\ m,\ t > 1$$

**C7 — Makespan:**
$$C_{\max} \geq \sum_{m,t} x_{omt} \cdot (t + p_o) \cdot \Delta \qquad \forall\ o = \text{last operation of some job}$$

**C8 — Peak power (the proposed extension):**
$$P^{\text{peak}} \geq \sum_{m \in \mathcal{M}} \Big[ P^{\text{proc}}_m \cdot y_{mt} + P^{\text{idle}}_m \cdot w_{mt} + \tfrac{E^{\text{start}}_m}{\Delta} \cdot z_{mt} \Big] \qquad \forall\ t$$

**C9 — Deadline (optional):**
$$\sum_{m,t} x_{omt} \cdot (t + p_o) \cdot \Delta \leq d_j \qquad \forall\ j,\ o = \text{last}(j)$$

### Multi-objective solution method

**AUGMECON (Augmented ε-constraint):**

For a 3-objective problem, fix one objective as primary (e.g., $F2$), treat $F1$ and $F3$ as ε-bounded constraints:

$$\min\ F2 - \delta \cdot (s_1/r_1 + s_2/r_2)$$

subject to: $F1 \leq \varepsilon_1 + s_1$, $F3 \leq \varepsilon_3 + s_3$, plus all scheduling constraints.

Grid $\varepsilon_1$ over $[F1^{\min}, F1^{\max}]$ and $\varepsilon_3$ over $[F3^{\min}, F3^{\max}]$ with $k$ steps each → $k^2$ MILP solves.

**Why AUGMECON, not weighted-sum:**
- `[ESTABLISHED]` Weighted-sum cannot find solutions on non-convex Pareto regions. Job-shop Pareto fronts are typically non-convex.
- `[ESTABLISHED]` AUGMECON guarantees Pareto-efficient solutions and avoids weakly-dominated points.
- `[ESTABLISHED]` For 3 objectives, AUGMECON with $k=10$ per dimension requires 100 MILP solves. At 10–60 seconds each for small instances (5×3 to 10×5), total runtime: 15–100 minutes. Feasible on laptop or RPi 5 with OR-Tools.

**Why not NSGA-III:**
- NSGA-III is appropriate for large instances where MILP is intractable.
- For the core research question (does peak-awareness change the Pareto structure?), exact solutions are preferable because they remove the noise of metaheuristic approximation.
- Use NSGA-III only for scalability experiments (Level 2+).

### Complexity

`[ESTABLISHED]` Job-shop scheduling is NP-hard. The time-indexed MILP has $O(n \cdot m \cdot H)$ binary variables. For 10 jobs × 5 machines × 48 time slots (12-hour horizon with 15-min slots): ~2,400 binaries. Gurobi solves this in seconds. OR-Tools CP-SAT handles similar scale.

Adding the $P^{\text{peak}}$ variable and C8 constraints adds $H$ linear constraints and one continuous variable — negligible overhead.

### Assumptions (stated honestly)

| Assumption | Realistic? | What happens if violated | Mitigation |
|---|---|---|---|
| Deterministic processing times | No (real times vary ±10-30%) | Schedule may miss deadlines | Uncertainty experiment (Level 3) |
| Constant $P^{\text{proc}}_m$ during processing | Approximately (steady-state motors/heaters) | Energy estimate error | Use measured average; report error |
| No machine breakdowns | Unrealistic for long horizons | Schedule becomes infeasible | Excluded; acknowledge limitation |
| Jobs known in advance | Yes for batch manufacturing | N/A | Appropriate for MSME batch |
| Piecewise-constant tariff | Yes — Indian ToD tariffs are block rates | N/A | Matches real tariff structure |
| Demand charge on peak kW | Yes — standard Indian industrial billing | N/A | Verified from SERC tariff orders |

---

## TASK 4 — Level Hierarchy

### Level 1 — Minimum Viable Research

**What it is:** Bi-objective MILP (makespan + energy cost) + FCFS/SPT baselines + synthetic instances + statistical comparison.

| Dimension | Assessment |
|---|---|
| Mathematical difficulty | Low-Medium. Standard MILP; ε-constraint is textbook. |
| Implementation difficulty | Low. PuLP or OR-Tools; 200–400 lines of Python. |
| Hardware | None required. |
| Data | Synthetic instances + published Indian tariff data. |
| Experiments | Model comparison across 60+ instances (3 sizes × 20 random). |
| Research contribution | **Nil.** This is a known formulation with known results. It only verifies that MILP beats heuristics — already proven hundreds of times. |
| Risk of failure | Very low — but contribution is also very low. |

**Verdict:** Necessary foundation. Not sufficient alone.

### Level 2 — Strong Project

**What it adds to Level 1:**
- **Third objective: peak demand** (F3 + constraint C8)
- **3D Pareto surface** via AUGMECON
- **Physical testbed** with measured power profiles
- **Physical schedule execution** (ESP32 → relays → loads → PZEM-004T)
- **Predicted vs. actual energy comparison**
- **Sensitivity analysis:** sweep demand-charge rate ρ and tariff ratio

| Dimension | Assessment |
|---|---|
| Mathematical difficulty | Medium. Tri-objective AUGMECON with parametric sweep. |
| Implementation difficulty | Medium. Hardware integration + multi-run experiments. |
| Hardware | ESP32, PZEM-004T, relay module, 3–4 loads (~₹2,300). Optional: RPi. |
| Data | Measured power profiles + synthetic instances + real tariff. |
| Experiments | 6 experiments (see Task 5). |
| Research contribution | **Empirical contribution + engineering integration.** Systematic Pareto analysis + physical validation + sensitivity characterisation. Not algorithmic novelty. |
| Risk of failure | Low-Medium. Peak-demand benefit may be negligible for small testbed — but characterising *when* it matters is itself a result. |

**Verdict: This is the target level.** Strong enough for a high-scoring undergraduate project with genuine analytical depth and physical validation.

### Level 3 — Advanced

**What it adds to Level 2:**
- **Uncertainty experiment:** Monte Carlo perturbation of processing times. Evaluate deterministic schedule under K=100 scenarios. Measure expected cost, worst-case cost, deadline violation rate.
- **NSGA-III for larger instances** (20×8, 50×10): scalability study.
- **Hypervolume indicator comparison** between exact (AUGMECON) and approximate (NSGA-III).

| Dimension | Assessment |
|---|---|
| Mathematical difficulty | Medium-High. Scenario evaluation requires scripting. NSGA-III via pymoo requires parameter tuning. |
| Implementation difficulty | Medium. Computational but no new hardware. |
| Research contribution | **Methodological contribution** (comparison of exact vs. approximate on energy-peak scheduling). |
| Risk of failure | Low for computation; moderate for finding meaningful differences. |

**Verdict:** Valuable addition if Level 2 is complete by week 7. Do not attempt if Level 2 is shaky.

### Level 4 — Stretch (Rolling-Horizon Adaptive)

**What it adds to Level 3:**
- **Event-triggered rescheduling:** Inject a disruption (delay one machine by N slots). Detect via measured state. Re-solve remaining schedule on RPi. Compare adapted vs. original.
- **State estimation loop:** ESP32 reports machine states via MQTT; RPi maintains system state; optimizer uses current state as initial condition.

| Dimension | Assessment |
|---|---|
| Mathematical difficulty | High. Rolling-horizon MILP requires warm-starting, state bookkeeping, and solving under deadline. |
| Implementation difficulty | High. Full MQTT pipeline, state machine, trigger logic, solver integration, error handling. |
| Research contribution | **Genuine empirical research question** — does rescheduling help on this scale? But answer may be "no" for small testbed. |
| Risk of failure | **High.** Integration complexity is the main risk. Single-point-of-failure: if MQTT drops or solver is too slow, demo fails. |

**Verdict:** Attempt ONLY if Levels 1–3 are rock-solid and time remains. Do NOT build the project around this.

---

## TASK 5 — Experiments

### Experiment 1 — Does energy-aware scheduling beat heuristics?

| Item | Detail |
|---|---|
| Independent variable | Scheduling method: FCFS, SPT, LPT, Makespan-MILP, Bi-obj-MILP |
| Dependent variables | Makespan, energy cost, peak power, total bill |
| Instances | 20 random instances × 3 sizes: 5×3, 8×4, 10×5 |
| Statistical method | Wilcoxon signed-rank test (paired), α = 0.05 |
| Hypothesis | Bi-obj-MILP reduces energy cost by >10% vs FCFS with <15% makespan increase |
| Falsifiability | If energy cost reduction < 5% on >50% of instances, the MILP provides negligible practical benefit |
| Purpose | Establish that energy-aware scheduling provides measurable benefit. **Baseline validation.** |

### Experiment 2 — Does peak-demand awareness change the Pareto front?

| Item | Detail |
|---|---|
| Independent variable | Number of objectives: 2-obj (F1, F2) vs 3-obj (F1, F2, F3) |
| Dependent variables | Pareto front structure (hypervolume), total bill |
| Instances | Same 60 instances |
| Statistical method | Paired Wilcoxon on total bill; hypervolume comparison |
| Hypothesis | 3-obj scheduling produces different Pareto-efficient solutions that reduce total bill (energy + demand charge) |
| Falsifiability | If hypervolume difference < 2% and total bill difference is not significant (p > 0.05), peak awareness adds nothing |
| Purpose | **Core research question.** |

### Experiment 3 — Sensitivity to demand-charge rate

| Item | Detail |
|---|---|
| Independent variable | $\rho$ ∈ {0, 50, 100, 150, 200, 250, 300, 400, 500} ₹/kW/month |
| Dependent variable | Total bill difference: 2-obj solution evaluated vs 3-obj solution |
| Instances | Fixed set of 10 medium instances (8×4) |
| Analysis | Plot bill savings vs ρ. Identify threshold ρ* below which savings < 5% |
| Hypothesis | Benefit of peak-awareness increases monotonically with ρ; there exists ρ* below which it is negligible |
| Falsifiability | If benefit is flat (constant or random) across ρ, the relationship does not exist |
| Purpose | **Characterise when peak-awareness matters.** |

### Experiment 4 — Sensitivity to tariff differential

| Item | Detail |
|---|---|
| Independent variable | Peak/off-peak price ratio ∈ {1.0, 1.1, 1.2, 1.3, 1.5, 1.8, 2.0} |
| Dependent variable | Energy cost savings: energy-aware vs FCFS |
| Instances | Same 10 medium instances; fixed ρ at Karnataka BESCOM rate |
| Hypothesis | Savings increase with tariff differential; at ratio ≈ 1.0, savings approach zero |
| Falsifiability | If savings are significant even at ratio 1.0, then scheduling benefit is independent of tariff structure (contradicts model) |
| Purpose | Determine whether ToU differential is the main driver or whether machine-state management alone provides benefit. |

### Experiment 5 — Energy model fidelity

| Item | Detail |
|---|---|
| Independent variable | Energy model: (A) constant power, (B) measured idle + processing, (C) B + measured startup |
| Dependent variable | Prediction error: |predicted energy − measured energy| / measured energy |
| Procedure | Generate 10 schedules using model A. Execute physically. Compute prediction error for A, B, C. |
| Hypothesis | Measured profiles (B, C) reduce prediction error below 10%; constant-power (A) has >20% error |
| Falsifiability | If all three models have similar error (<5% difference), measured profiles add no value |
| Purpose | Justify (or reject) the physical measurement layer. |

### Experiment 6 — Scalability (Level 3)

| Item | Detail |
|---|---|
| Independent variable | Instance size: 5×3, 8×4, 10×5, 15×6, 20×8, 30×10, 50×10 |
| Dependent variables | Solver time (s), optimality gap (%), memory (MB), hypervolume |
| Solvers | OR-Tools CP-SAT (on RPi 5 and laptop), NSGA-III via pymoo (laptop) |
| Analysis | Log-log plot of time vs. size; identify crossover where exact becomes intractable |
| Purpose | Determine feasible problem scale for each solver and platform. |

---

## TASK 6 — Physical Prototype

### What it is and what it is NOT

This is a **programmable machine-load emulation testbed.** It uses controllable electrical loads to emulate machine behavior (processing, idle, startup, off). It is NOT a factory, NOT a production line, and should NOT be presented as one.

**What it proves:**
1. The energy model (P_proc, P_idle, E_start) can be measured from real loads.
2. The optimised schedule can be physically executed via controller + relays.
3. The predicted energy consumption matches the measured energy consumption.
4. The predicted peak power matches the measured peak power.
5. The difference between baseline and optimised schedules is physically observable.

**What it does NOT prove:**
- That the method works in a real factory.
- That the improvement percentages transfer to industrial machines.
- That the tariff savings are industrially significant.

### Architecture

```
┌──────────────┐        Serial/UART       ┌─────────────────┐
│  PZEM-004T   │◄────────────────────────►│     ESP32        │
│  (V, I, P,   │                          │  - Read PZEM     │
│   E, PF)     │                          │  - Control relays│
└──────┬───────┘                          │  - MQTT publish  │
       │ measures                         │  - State report  │
       ▼                                  └────────┬────────┘
┌──────────────┐                                   │ WiFi/MQTT
│  4ch Relay   │◄──── GPIO ────────────────────────┘
│  Module      │                                   │
└──────┬───────┘                          ┌────────▼────────┐
       │ switches                         │  Raspberry Pi 5  │
       ▼                                  │  - MQTT broker   │
┌──────────────┐                          │  - OR-Tools      │
│  Load 1:     │                          │  - Scheduler     │
│  DC Motor    │                          │  - Database      │
│  (12V, ~2A)  │                          │  - Dashboard     │
├──────────────┤                          └─────────────────┘
│  Load 2:     │
│  Heater coil │
│  (12V, ~3A)  │
├──────────────┤
│  Load 3:     │
│  LED array   │
│  (12V, ~1A)  │
├──────────────┤
│  Load 4:     │
│  Fan/pump    │
│  (12V, ~1.5A)│
└──────────────┘
```

**Safety:** All loads are 12V DC, powered from a bench supply or battery. The PZEM-004T measures the DC supply line (or a separate AC line if using small AC loads with appropriate isolation). No mains voltage exposure.

**Alternative for AC measurement:** Use small AC loads (desk lamp, small fan, soldering iron on low) with the PZEM-004T on the AC side, housed in an insulated enclosure. This gives more realistic AC power factor data.

### BOM

| Component | Qty | Unit (₹) | Total (₹) | Purpose |
|---|---|---|---|---|
| ESP32-WROOM-32 | 1 | 500 | 500 | Controller: relay control, PZEM reading, MQTT |
| PZEM-004T v3 (100A CT) | 1 | 500 | 500 | Power measurement: V, I, P, E |
| 4-channel relay module | 1 | 200 | 200 | Load switching |
| DC motor (775, 12V) | 1 | 250 | 250 | Load 1: emulates motor-type machine |
| Ceramic heater element (12V) | 1 | 100 | 100 | Load 2: emulates thermal process |
| LED strip (12V, 1m) | 1 | 150 | 150 | Load 3: emulates light-duty machine |
| 12V DC fan | 1 | 100 | 100 | Load 4: emulates auxiliary equipment |
| 12V 10A power supply | 1 | 300 | 300 | Power for all loads |
| Breadboard + jumper wires | 1 | 200 | 200 | Prototyping |
| **Total** | | | **₹2,300** | |
| Raspberry Pi 5 (borrowed) | 1 | 0 | 0 | Optimization server |

### Data classification

| Category | What | Source | Justification |
|---|---|---|---|
| **REAL (measured)** | P_proc, P_idle, E_start for each load; actual energy per schedule execution; actual peak power; actual ON/OFF timing | PZEM-004T + ESP32 timestamps | Direct physical measurement of the system under control |
| **MODELLED (real-world sources)** | Processing times; job precedence; tariff rates; demand charge rates; deadlines | Designed + SERC tariff orders | Processing times are design parameters of the experiment; tariffs are publicly documented |
| **SIMULATED** | Large-scale instances (20+ jobs); uncertainty scenarios; tariff sweeps | Python scripts | Cannot physically build 50 machines; simulation extends results using the measured energy model |

---

## TASK 7 — Raspberry Pi Role Analysis

### Possible roles and honest assessment

| Role | Justified? | Reasoning |
|---|---|---|
| **Optimization server** | **YES — if solver actually runs on it** | Running OR-Tools CP-SAT on RPi 5 to solve 10×5 instances in real-time demonstrates edge-feasible scheduling. This is technically meaningful: it shows the optimizer doesn't require a cloud server. Benchmark: solve time on RPi vs. laptop. |
| **MQTT broker** | **Marginal** | Mosquitto on RPi is trivial. Not a research contribution, but necessary infrastructure. |
| **Local database** | **No — not research** | SQLite/InfluxDB for logging. Useful but not a contribution. |
| **State estimator** | **Only at Level 4** | Needed for rolling-horizon rescheduling. Not justified at Level 2. |
| **Dashboard server** | **No — not research** | Flask/Grafana for display. Useful for demo, not a contribution. |
| **Experiment controller** | **YES — practical** | Orchestrates run sequences, logs results, triggers ESP32. Useful engineering. |

### Verdict

**The RPi is justified as the optimization server** if and only if:
1. The solver actually runs on it (OR-Tools CP-SAT — confirmed feasible on ARM64).
2. You report solve time on RPi vs. laptop as a scalability result.
3. You demonstrate that the schedule is generated *on the RPi* and sent to the ESP32 for execution.

**This makes the RPi an edge scheduler**, which is technically defensible. It is NOT research novelty — it is engineering integration.

**Gurobi does NOT run on ARM.** Use OR-Tools CP-SAT or PuLP + CBC (both support ARM64 natively).

### Honest framing

> "We deploy the multi-objective scheduler on a Raspberry Pi 5 to demonstrate that energy-aware scheduling is computationally feasible on low-cost edge hardware, eliminating the need for cloud infrastructure."

This is **engineering integration**, not algorithmic novelty.

---

## TASK 8 — Falsifiable Research Questions

### RQ1 — Peak-demand Pareto structure

**Question:** Does adding peak demand as a third scheduling objective produce a Pareto surface that is structurally distinct from the bi-objective (makespan, energy cost) Pareto front?

- **IV:** Number of objectives (2 vs 3)
- **DV:** Hypervolume indicator, number of Pareto-efficient solutions, total bill
- **Baseline:** 2-objective AUGMECON solution set
- **Outcome:** Hypervolume difference and bill comparison
- **Hypothesis:** The 3-objective Pareto surface occupies a distinct region of solution space, and at least 20% of its solutions are not dominated by any 2-objective solution when evaluated on total bill (energy + demand charge).
- **Falsification:** If all 3-obj solutions are dominated by some 2-obj solution on total bill, peak-awareness adds no value.

### RQ2 — Demand-charge threshold

**Question:** At what demand-charge rate (₹/kW/month) does peak-demand-aware scheduling begin to provide statistically significant total-bill reduction?

- **IV:** Demand charge rate ρ
- **DV:** Total bill savings (2-obj vs 3-obj)
- **Baseline:** 2-objective optimal schedule evaluated at each ρ
- **Outcome:** Threshold ρ* identified via regression or segmented analysis
- **Hypothesis:** There exists a threshold ρ* such that for ρ > ρ*, the 3-objective solution reduces total bill by >5%.
- **Falsification:** If no threshold exists (benefit is negligible at all ρ, or always significant), the relationship is trivial.

### RQ3 — Energy model fidelity

**Question:** Does using measured machine power profiles significantly improve the accuracy of schedule energy predictions compared to constant-power assumptions?

- **IV:** Energy model variant (constant vs. measured idle+processing vs. measured+startup)
- **DV:** Prediction error |predicted − measured| / measured
- **Baseline:** Constant-power model with datasheet values
- **Outcome:** Prediction error comparison
- **Hypothesis:** Measured profiles reduce prediction error to <10%; constant-power exceeds 20%.
- **Falsification:** If constant-power error is already <10%, measurement adds no value for scheduling.

### RQ4 — Tariff differential sensitivity

**Question:** Below what peak/off-peak tariff ratio does energy-aware scheduling fail to provide meaningful cost savings over FCFS?

- **IV:** Peak/off-peak price ratio (1.0 to 2.0)
- **DV:** Energy cost savings (MILP vs FCFS)
- **Baseline:** FCFS scheduling
- **Outcome:** Savings vs ratio curve; identify ratio below which savings < 3%
- **Hypothesis:** Savings are <3% when ratio < 1.1 and increase approximately linearly with ratio above 1.2.
- **Falsification:** If savings are >10% even at ratio 1.0, the benefit comes from machine-state management, not tariff exploitation (a valid alternative finding).

### RQ5 — Edge solver feasibility

**Question:** Can OR-Tools CP-SAT on Raspberry Pi 5 solve the tri-objective scheduling MILP to within 1% optimality gap in under 60 seconds for instances up to 10 jobs × 5 machines?

- **IV:** Instance size (5×3 to 15×6)
- **DV:** Solve time, optimality gap, solution quality vs laptop
- **Baseline:** Same solver on laptop (Intel i5/i7)
- **Outcome:** Speed ratio (RPi/laptop) and maximum feasible instance size
- **Hypothesis:** RPi 5 solves 10×5 instances in <60s with <1% gap.
- **Falsification:** If RPi cannot solve 8×4 within 120s, edge deployment is not feasible for this formulation.

### RQ6 — Schedule robustness (Level 3)

**Question:** Does the deterministic energy-aware schedule remain cost-effective when processing times are perturbed by ±20%?

- **IV:** Perturbation level (0%, 5%, 10%, 15%, 20%, 30%)
- **DV:** Expected cost overrun, deadline violation rate, peak demand exceedance
- **Baseline:** Deterministic optimal schedule evaluated under perturbation scenarios (K=100)
- **Outcome:** Cost overrun and violation rate vs perturbation level
- **Hypothesis:** Below 15% perturbation, cost overrun is <8% and violations are <10%. Above 20%, degradation is significant.
- **Falsification:** If the schedule is robust even at 30% (overrun <5%), uncertainty-aware extensions are unnecessary for this problem scale.

---

## TASK 9 — Novelty Audit

| Component | Classification | Honest statement |
|---|---|---|
| **MILP formulation for job-shop scheduling** | `ESTABLISHED` | Standard since 1960s. Not novel. |
| **Machine-state energy model (idle/processing/startup/off)** | `ESTABLISHED` | Standard since ~2016. Not novel. |
| **ε-constraint / AUGMECON for multi-objective** | `ESTABLISHED` | Textbook methodology (Mavrotas, 2009). Not novel. |
| **ToU-aware scheduling** | `ESTABLISHED` | Dozens of papers. Not novel. |
| **NSGA-II/III for scheduling** | `ESTABLISHED` | Textbook. Not novel. |
| **Peak demand as minimax variable** | `ESTABLISHED` | Used in energy systems. Less common in *manufacturing scheduling* specifically but the formulation (P_peak ≥ Σ P(t)) is standard. |
| **ESP32 + PZEM-004T power monitoring** | `ESTABLISHED` | Well-documented IoT pattern. Not novel. |
| **Raspberry Pi as edge optimizer** | `ENGINEERING INTEGRATION` | Running a solver on ARM is not research. Benchmarking its performance for scheduling is a minor empirical contribution. |
| **MQTT + relay control of loads** | `ENGINEERING INTEGRATION` | Standard automation. Not novel. |
| **Dashboard / Gantt visualisation** | `ENGINEERING INTEGRATION` | Not novel. |
| **Indian ToU tariff parameterisation** | `CONTEXTUAL NOVELTY` | Applying known model to Indian tariff data. The parameters are new; the mathematics is not. |
| **Tri-objective Pareto surface for manufacturing scheduling** | `EMPIRICAL CONTRIBUTION` | The specific analysis (3D Pareto + sensitivity to demand-charge rate) on manufacturing scheduling instances with measured power data appears under-explored. This is NOT algorithmic novelty — it is a systematic empirical study of an extended formulation. |
| **Physical schedule execution + predicted vs actual comparison** | `EMPIRICAL CONTRIBUTION` | Rare in the literature. Most papers are simulation-only. Physically executing and validating is a genuine engineering contribution. |
| **Demand-charge threshold characterisation** | `EMPIRICAL CONTRIBUTION` | Identifying *when* peak-awareness matters is a parametric study that appears absent from the literature. Not algorithmic novelty. |
| **Sensitivity analysis across tariff structures** | `EMPIRICAL CONTRIBUTION` | Characterising the problem space rather than proposing a new solution. Valid empirical research. |

### Summary of honest framing

> This project does NOT propose a new algorithm, a new solver, or a new mathematical technique. Every component is individually established. The contribution is: (1) a systematic empirical study of the tri-objective makespan-cost-peak trade-off under realistic industrial tariff structures, (2) parametric sensitivity analysis characterising when peak-demand awareness provides meaningful benefit, and (3) physical validation of an energy-aware schedule on a measured testbed. This is an **extended formulation study with empirical validation**, not an algorithmic innovation.

---

## TASK 10 — Final Project Architecture

### 1. Problem

Indian MSMEs face electricity costs comprising energy charges (kWh-based, ToD-differentiated) and demand charges (peak kW-based). Production scheduling in these settings ignores energy costs entirely (FCFS/manual). Optimised scheduling can reduce both components, but minimising energy cost alone may increase peak demand, raising the total bill.

### 2. Existing approaches

Bi-objective scheduling (makespan + energy) is extensively studied. Machine-state energy models are standard. Peak demand is addressed in energy systems but less explored as a production scheduling objective. Physical validation of energy-aware schedules is rare.

### 3. Exact research gap

No systematic study characterises (a) the structure of the tri-objective Pareto surface for manufacturing scheduling with peak demand, (b) under what tariff conditions peak-demand awareness provides significant total-bill reduction, or (c) validates the predicted energy savings of an optimised schedule against physical measurements on a testbed.

### 4. Mathematical formulation

See Task 3. Tri-objective MILP with AUGMECON. Seven constraint families. Three objective functions.

### 5. Proposed method

AUGMECON with OR-Tools CP-SAT as MILP solver. Parametric sweep over demand-charge rate and tariff differential. Physical execution on testbed. Predicted vs. actual comparison.

### 6. Physical prototype

Machine-load emulation testbed: 4 controllable loads (DC motor, heater, LED, fan) + PZEM-004T + ESP32 + relay module. ~₹2,300 BOM.

### 7. Raspberry Pi role

**Local optimization server.** Runs OR-Tools CP-SAT to solve the scheduling MILP. Serves as MQTT broker and experiment controller. Benchmarked against laptop for solver time comparison.

### 8. ESP32 role

**Sensing and control node.** Reads PZEM-004T power data. Controls relay module to execute schedule. Reports machine states and measured power via MQTT to RPi.

### 9. Data flow

```
[Tariff data + Job data + Measured power profiles]
                    │
                    ▼
        ┌─────────────────────┐
        │   Raspberry Pi 5    │
        │                     │
        │  MILP model build   │
        │  OR-Tools CP-SAT    │
        │  AUGMECON loop      │
        │  → Pareto surface   │
        │  → Selected schedule│
        └─────────┬───────────┘
                  │ MQTT: schedule commands
                  ▼
        ┌─────────────────────┐
        │      ESP32          │
        │  Execute schedule   │
        │  Control relays     │
        │  Read PZEM-004T     │
        │  Report measurements│
        └─────────┬───────────┘
                  │ MQTT: power data
                  ▼
        ┌─────────────────────┐
        │   Raspberry Pi 5    │
        │  Log measurements   │
        │  Compare predicted  │
        │    vs actual        │
        │  Display dashboard  │
        └─────────────────────┘
```

### 10. Optimization loop

**Level 2 (target):** Open-loop. Optimize → execute → measure → compare. No re-optimization during execution.

**Level 4 (stretch):** Closed-loop. Optimize → execute → detect deviation → re-optimize remaining schedule.

### 11. Baselines

| Baseline | Description |
|---|---|
| B1: FCFS | First-come-first-served dispatch. No optimisation. |
| B2: SPT | Shortest-processing-time dispatch. No energy awareness. |
| B3: Makespan-MILP | Single-objective: minimise makespan. Ignores energy. |
| B4: Bi-objective | Minimise {makespan, energy cost}. ε-constraint. No peak. |
| **Proposed: P1** | **Minimise {makespan, energy cost, peak demand}. AUGMECON.** |

### 12. Experiments

See Task 5. Six experiments covering: model comparison, Pareto structure, demand-charge sensitivity, tariff sensitivity, energy model fidelity, scalability.

### 13. Evaluation metrics

| Metric | Unit | From |
|---|---|---|
| Makespan | time slots or hours | Solver output |
| Energy cost | ₹ | Solver output + validation from PZEM-004T |
| Peak power | W or kW | Solver output + validation from PZEM-004T |
| Total bill | ₹ | Computed: energy cost + ρ × peak |
| Prediction error | % | |predicted − measured| / measured |
| Hypervolume indicator | dimensionless | From Pareto front analysis |
| Solver time | seconds | Timed on RPi and laptop |
| Optimality gap | % | From solver output |
| Deadline violation rate | % | Count of jobs finishing after deadline |

### 14. Expected contribution

1. **Empirical:** Systematic 3D Pareto analysis of makespan × energy cost × peak demand for manufacturing scheduling.
2. **Empirical:** Parametric characterisation of when peak-demand awareness provides meaningful total-bill reduction (demand-charge threshold).
3. **Engineering:** Physical validation of energy-aware scheduling on a measured testbed.
4. **Engineering:** Demonstration of edge-feasible scheduling on Raspberry Pi.

All of these are empirical/engineering contributions. None are algorithmic novelty.

### 15. Limitations

1. **Testbed is not a factory.** Results demonstrate methodology validation, not industrial-scale savings.
2. **Loads are emulators.** A DC motor is not a CNC machine. Power profiles are representative, not identical.
3. **Deterministic model.** Processing times are fixed. Real manufacturing has variability.
4. **Small scale.** Largest physically executable instance is 4 machines. Simulation extends to larger.
5. **No machine breakdowns.** Excluded from model.
6. **Indian tariff specificity.** Results depend on tariff structure. Generalisation requires additional experiments with other tariff regimes.
7. **Solver limitations.** OR-Tools CP-SAT is less powerful than Gurobi for large MILP. Edge solver comparison is limited by ARM architecture.

---

## FINAL DECISION

### Decision: **MODIFY then GO**

### Justification matrix

| Criterion | Assessment | Evidence |
|---|---|---|
| Mathematical rigour | ✅ Adequate | Tri-objective MILP + AUGMECON + parametric sensitivity. Not novel math, but rigorous applied math. |
| Real research gap | ⚠️ Narrow but genuine | Systematic Pareto analysis with demand-charge sensitivity for manufacturing scheduling is under-explored. Physical validation is rare. |
| Experimental falsifiability | ✅ Strong | Six experiments with null hypotheses and specific falsification conditions. |
| Undergraduate feasibility | ✅ Strong | OR-Tools + Python + ESP32 + PZEM-004T. All tools are free and well-documented. |
| Data availability | ✅ Strong | Synthetic instances (standard). Indian tariffs (public). Machine power (self-measured). |
| Prototype feasibility | ✅ Strong | ₹2,300 BOM. Safe low-voltage. Borrowed RPi. |
| Reproducibility | ✅ Strong | Open-source tools. Published tariff data. Measured profiles can be shared. |
| Measurable contribution | ✅ Clear | Pareto analysis, threshold identification, prediction validation, solver benchmarking. |
| SDG 9 alignment | ✅ Direct | SDG 9.4 (sustainable industrialisation). Energy cost reduction for MSMEs. |

### What must be modified

1. **Do NOT claim algorithmic novelty.** Frame as "extended formulation study with empirical validation."
2. **Add peak demand as third objective.** This is the mathematical layer that elevates beyond textbook.
3. **Build physical testbed.** This is the engineering layer that elevates beyond simulation.
4. **Add sensitivity analysis.** This is the research layer — characterising *when* peak-awareness matters.
5. **Use OR-Tools CP-SAT, not Gurobi** — runs natively on RPi ARM64.
6. **Raspberry Pi is justified only as optimization server with benchmarked performance.** Not as IoT decoration.

### What must NOT be done

- Do NOT call this "novel algorithm."
- Do NOT add blockchain, computer vision, chatbot, or "AI" without technical justification.
- Do NOT claim specific improvement percentages before running experiments.
- Do NOT treat the dashboard as a contribution.
- Do NOT treat MQTT/IoT as research.
- Do NOT build Level 4 before Level 2 works flawlessly.

### Critical path

| Week | Deliverable | Level |
|---|---|---|
| 1 | Implement bi-objective MILP in OR-Tools. Verify on 5×3 instance. | L1 |
| 1 | Download Karnataka BESCOM tariff order. Extract ToD rates + demand charge. | L1 |
| 2 | Extend to tri-objective (add P_peak). Implement AUGMECON loop. | L2 |
| 2 | Build instance generator. Generate 60 test instances. | L1 |
| 3 | Run Experiment 1 (model comparison) and Experiment 2 (Pareto structure). | L2 |
| 3 | Order and assemble hardware. Wire ESP32 + PZEM-004T + relay + loads. | L2 |
| 4 | Measure P_proc, P_idle, E_start for each load. Calibrate PZEM-004T. | L2 |
| 5 | Integrate RPi ↔ ESP32 via MQTT. Execute baseline + optimised schedules. | L2 |
| 5 | Run Experiment 5 (energy model fidelity). | L2 |
| 6 | Run Experiment 3 (demand-charge sensitivity) and Experiment 4 (tariff sensitivity). | L2 |
| 7 | Run Experiment 6 (scalability) on RPi vs laptop. | L3 |
| 7 | Build dashboard for demo. | L2 |
| 8 | Full demo rehearsal. Record results. Begin report. | L2 |
| 9–10 | (If ahead) Attempt Experiment 6 uncertainty analysis. | L3 |
| 10–12 | Report, poster, presentation. | All |

---

## APPENDIX B — `master_execution_plan.md`

# MASTER EXECUTION PLAN
## Peak-Aware Energy-Cost Production Scheduling Under Industrial Tariff Structures

> **Version:** 1.0 — 2026-10-02  
> **Status:** PLANNING → Awaiting team review  
> **Corrections applied:** PZEM→INA226, tariff verification, demand-charge modelling, AUGMECON caveats, CP-SAT terminology, arbitrary thresholds removed.

---

# PART 1 — PROJECT FREEZE

## Final project title

**Peak-Aware Energy-Cost Production Scheduling for Small Manufacturing Systems Under Industrial Tariff Structures: A Multi-Objective Optimization Study with Physical Validation**

## Problem statement

Small manufacturing units operate under industrial electricity tariffs comprising (a) time-differentiated energy charges and (b) demand charges based on recorded peak power. Current production scheduling in these settings ignores electricity costs entirely. Energy-cost-only scheduling can reduce energy charges but may inadvertently increase peak demand, raising the total bill through demand charges. No systematic study characterises under what tariff and workload conditions peak-demand-aware scheduling provides economically meaningful benefit over energy-cost-only scheduling.

## Research question

> Under what combinations of demand-charge intensity, time-of-use tariff differential, workload intensity, and machine power heterogeneity does peak-aware multi-objective production scheduling provide a statistically significant economic benefit over energy-cost-only scheduling?

## Hypotheses

**H1 (Primary):** Peak-aware scheduling (minimising makespan + energy cost + peak demand) produces schedules with a lower simulated total electricity bill than energy-cost-only scheduling (minimising makespan + energy cost) when demand-charge intensity exceeds a threshold value. The threshold and magnitude of benefit are unknown prior to experimentation.

**H2:** The economic benefit of peak-aware scheduling increases with: (a) demand-charge rate, (b) time-of-use price differential, (c) workload intensity (ratio of total processing time to available time), and (d) machine power heterogeneity.

**H3:** Energy-cost-only scheduling does not significantly increase peak demand relative to makespan-only scheduling in all workload conditions; there exist workload conditions where it does and conditions where it does not.

**H4:** A deterministic scheduling model using measured machine power profiles (idle, processing, startup) predicts total energy consumption within an experimentally-determined error bound when validated against physical testbed measurements.

## Objectives

1. Formulate a tri-objective production scheduling model (makespan, energy cost, peak demand) using constraint programming.
2. Implement the model using OR-Tools CP-SAT and solve via ε-constraint method (AUGMECON variant).
3. Implement appropriate baseline scheduling methods (FCFS, SPT, makespan-only, energy-only).
4. Design and execute a systematic sensitivity study over demand-charge rate, ToU differential, workload intensity, and power heterogeneity.
5. Build a programmable machine-load emulation testbed and validate predicted vs. measured energy/peak.
6. Deploy the optimization workflow on a Raspberry Pi 5 and benchmark solver performance.
7. Report findings with statistical analysis, including identification of conditions under which peak-awareness is and is not beneficial.

## Scope

### In scope (CORE)

- Static/open-loop scheduling (schedule computed once, then executed)
- Deterministic processing times
- Synthetic workload instances parameterised for sensitivity analysis
- OR-Tools CP-SAT as primary solver
- ε-constraint (AUGMECON-style) multi-objective method
- Sensitivity analysis over 4 factors
- Physical testbed with 3–4 DC loads, INA226 power measurement, ESP32 control
- Raspberry Pi 5 as edge optimization platform
- Comparison against FCFS, SPT, makespan-only, and energy-cost-only baselines

### In scope (STRETCH — only after CORE is complete)

- Uncertainty analysis (Monte Carlo perturbation of processing times)
- NSGA-III for larger instances
- Rolling-horizon / adaptive rescheduling

### Out of scope

- Real factory deployment
- AC mains measurement or mains-voltage switching
- Machine learning / deep learning
- Blockchain, computer vision, chatbot / voice interface
- Real-time dynamic job arrival
- Multi-factory or supply-chain scheduling

## Expected contribution (taxonomy)

| # | Contribution | Classification |
|---|---|---|
| 1 | Tri-objective formulation (makespan + energy cost + peak demand) for production scheduling | `ENGINEERING INTEGRATION` — combines known components. The formulation uses established techniques. |
| 2 | Systematic sensitivity study: under what tariff/workload conditions does peak-awareness matter? | `EMPIRICAL CONTRIBUTION` — produces new experimental data. Not algorithmic novelty. |
| 3 | Comparison of scheduling strategies across multiple baselines | `EMPIRICAL CONTRIBUTION` — standard experimental methodology. |
| 4 | Physical validation of predicted vs. measured energy/peak on testbed | `PHYSICAL VALIDATION CONTRIBUTION` — rare in scheduling literature. |
| 5 | Deployment and benchmarking on Raspberry Pi edge platform | `ENGINEERING INTEGRATION` — demonstrates feasibility. Not a research contribution per se. |

## Assumptions

1. Processing times are deterministic (known and fixed for each instance).
2. All jobs and their operations are known at scheduling time (no dynamic arrivals).
3. Machine power draw is approximately constant during processing (verified via measurement).
4. Tariff parameters are modelled after verified Indian industrial tariff structure but parameterised for sensitivity analysis.
5. The physical testbed emulates machine behavior; it does not replicate a real factory.
6. No machine breakdowns occur during schedule execution.

## Limitations

1. Testbed scale (3–4 loads) limits physical validation to small instances.
2. Deterministic model does not capture real-world processing time variability.
3. Results are specific to the parameterised tariff structure; generalisation requires additional study.
4. DC loads do not fully represent industrial AC machinery (no power factor effects).
5. Edge solver performance is hardware-dependent.

## Terminology

| Term | Definition |
|---|---|
| Makespan ($C_{\max}$) | Completion time of the last operation across all jobs |
| Energy cost | Total (power × duration × time-slot price) for all machine activity |
| Peak demand ($P^{\text{peak}}$) | Maximum total instantaneous power across all machines over all time slots |
| Total bill | Energy cost + demand charge component (peak demand × demand-charge rate, scaled to billing period) |
| Demand charge | Fixed cost per unit of peak demand per billing period (₹/kVA/month in real tariffs) |
| ToU / ToD | Time-of-Use / Time-of-Day: time-varying electricity price |
| Pareto-efficient | A solution where no objective can be improved without worsening another |
| CP-SAT | Google OR-Tools Constraint Programming with SAT solver — a constraint programming solver, NOT a MILP solver |
| AUGMECON | Augmented ε-constraint method for multi-objective optimization |
| Machine-load emulation testbed | Physical system with controllable electrical loads representing machines |

---

# PART 2 — LITERATURE AND RESEARCH FOUNDATION

## 2.1 Topics to search

| # | Topic | Purpose |
|---|---|---|
| 1 | Energy-aware manufacturing/job-shop scheduling | Core domain |
| 2 | Multi-objective production scheduling (makespan + energy) | Baseline formulations |
| 3 | Peak demand / demand-charge-aware scheduling | Gap verification |
| 4 | Time-of-use electricity scheduling in manufacturing | Tariff-aware precedents |
| 5 | ε-constraint / AUGMECON method | Solution methodology |
| 6 | Constraint programming for scheduling (CP-SAT) | Solver methodology |
| 7 | Robust / stochastic scheduling (energy-aware) | Context (stretch) |
| 8 | Physical validation of scheduling models | Gap verification |
| 9 | Edge computing for manufacturing optimization | RPi context |
| 10 | Indian industrial tariff structure | Tariff parameterisation |
| 11 | MSME / small-manufacturer energy management | Application context |

## 2.2 Search query templates

```
"energy-aware" AND "job shop scheduling" AND ("multi-objective" OR "Pareto")
"peak demand" AND "production scheduling" AND "optimization"
"time-of-use" AND "manufacturing scheduling" AND ("MILP" OR "constraint programming")
"demand charge" AND ("scheduling" OR "peak shaving") AND "manufacturing"
"augmented epsilon-constraint" AND "scheduling"
"CP-SAT" AND "scheduling" AND "energy"
"robust scheduling" AND "processing time uncertainty" AND "energy"
"physical validation" AND "scheduling" AND "energy consumption"
"Raspberry Pi" AND "optimization" AND ("scheduling" OR "edge")
"Indian industrial tariff" AND ("ToD" OR "time-of-day" OR "demand charge")
```

## 2.3 Databases

1. **Google Scholar** — primary
2. **IEEE Xplore** — via Scholar links
3. **ScienceDirect** — EJOR, Computers & Industrial Engineering
4. **SpringerLink** — OR Spectrum, JMSY
5. **MDPI** — open access (Sustainability, Algorithms, Energies)
6. **arXiv** — preprints

## 2.4 Paper collection targets

| Category | Target | Purpose |
|---|---|---|
| Foundational (pre-2020) | 3–5 | Mouzon 2007, Gahm 2016 survey, AUGMECON (Mavrotas 2009) |
| Recent scheduling (2020–2026) | 8–12 | Current state of energy scheduling |
| Peak demand / demand charge | 3–5 | Verify gap claim |
| Physical validation | 2–3 | Confirm rarity |
| Methodology (ε-constraint, CP) | 2–3 | Solution method references |
| Tariff / policy | 2–3 | KERC orders, national ToD rules |
| **Total** | **20–30** | Sufficient for undergraduate project |

## 2.5 Literature review spreadsheet columns

```
ID | Authors | Year | Title | Venue | Model_Type | Objectives | Machines |
Uncertainty | Physical_Validation | Tariff_Type | Peak_Demand_Addressed |
Solution_Method | Instance_Size | Key_Finding | Limitation | Relevance_to_Us |
PDF_Available | Notes
```

## 2.6 Claims requiring primary/official sources

| Claim | Required source |
|---|---|
| Indian industrial tariffs include demand charges on peak kVA | KERC tariff order (official PDF) |
| ToD is mandatory for ≥10 kW consumers | MoP Electricity (Rights of Consumers) Amendment Rules, 2023 |
| Peak hours are 6–9 AM, 6–10 PM in Karnataka | KERC tariff order |
| ToD incentive/penalty is ±20% | KERC regulation or national rule |
| Demand charges are ~₹365/kVA for HT-2a | Latest KERC tariff order |

---

# PART 3 — TARIFF RESEARCH

## 3.1 Verified tariff structure (Karnataka / BESCOM / KERC)

> [!IMPORTANT]
> The values below are sourced from web-accessible summaries of KERC tariff orders (FY 2025-26, March 2026 revision). **BEFORE USING IN THE FINAL REPORT**, download and verify against the official KERC tariff order PDF from kerc.karnataka.gov.in or bescom.karnataka.gov.in.

### Consumer categories relevant to MSMEs

| Category | Description | Metering | Demand basis |
|---|---|---|---|
| **LT-5** | LT Industrial (Motive Power) | LT metering | Sanctioned load in **kW**; fixed charge per kW |
| **HT-2(a)** | HT Industrial | HT metering (≥11 kV supply) | Billing demand in **kVA** |

**For our model, HT-2(a) is the more appropriate reference** because it has explicit demand charges in ₹/kVA billed on recorded peak demand, directly analogous to our peak-demand objective. LT-5 uses fixed charges per kW of sanctioned load, not recorded peak.

### HT-2(a) tariff components (approximate FY 2025-26)

| Component | Value | Unit | Notes | Verification status |
|---|---|---|---|---|
| Demand charge | ~₹365 | per kVA per month | Billed on max of (recorded MD, ~75% of sanctioned demand) | `REQUIRES OFFICIAL PDF VERIFICATION` |
| Energy charge | ~₹6.60 | per kWh | May vary by slab | `REQUIRES VERIFICATION` |
| ToD peak surcharge | +20% | of energy charge | During peak hours | `CONSISTENT WITH NATIONAL RULE` |
| ToD off-peak rebate | −20% | of energy charge | During off-peak hours | `CONSISTENT WITH NATIONAL RULE` |
| Peak hours | 06:00–09:00, 18:00–22:00 | | 7 hours total | `REPORTED CONSISTENTLY` |
| Off-peak hours | 22:00–06:00 | | 8 hours total | `REPORTED CONSISTENTLY` |
| Normal hours | 09:00–18:00 | | 9 hours total | `INFERRED` |
| Electricity tax | 9% | of total | Additional surcharge | `REPORTED` |
| FPPCA | Variable | per kWh | Monthly fuel adjustment | `VARIABLE` |
| Power factor penalty | Surcharge if PF < 0.90 | | Additional | `REPORTED` |
| Billing period | 1 month | | | `STANDARD` |
| MD measurement | 15-min or 30-min sliding window | kVA | Highest average kVA in any window | `REPORTED` |

### How tariff maps to mathematical model

**Energy charge:**

$$\text{EnergyCost} = \sum_{t \in \mathcal{T}} \left( \sum_{m \in \mathcal{M}} P_m(t) \cdot \Delta \right) \cdot \pi_t$$

where $\pi_t$ is the ToD-adjusted price:

$$\pi_t = \begin{cases} \pi_{\text{base}} \times 1.20 & \text{if } t \in \text{Peak hours} \\ \pi_{\text{base}} \times 0.80 & \text{if } t \in \text{Off-peak hours} \\ \pi_{\text{base}} & \text{if } t \in \text{Normal hours} \end{cases}$$

**Demand charge:**

$$\text{DemandCharge} = \rho \cdot P^{\text{peak}}$$

where $\rho$ is in ₹/kW/scheduling-horizon (see §3.2).

**Total bill:**

$$\text{TotalBill} = \text{EnergyCost} + \text{DemandCharge}$$

## 3.2 Demand-charge scaling for experiments

> [!WARNING]
> Real demand charges are ₹/kVA/**month**. Our scheduling horizon is hours, not months. We cannot claim "this 8-hour experiment saves ₹X per month."

**Approach:**

1. Define a per-experiment demand-charge parameter $\rho$ with units ₹/kW (not ₹/kVA/month).
2. Sweep $\rho$ across a range including the monthly-equivalent rate and fractions of it.
3. Report: "For a demand-charge parameter of $\rho$ ₹/kW applied to the scheduling horizon, the peak-aware schedule reduces total cost by Y% vs energy-only."
4. Map to real tariff in discussion: "If the scheduling horizon covers the month's expected peak period, then $\rho = 365$ ₹/kVA (the HT-2a rate). If the schedule covers one of $N$ identical shifts, a conservative estimate is $\rho = 365/N$."

This parameterises $\rho$ and reports sensitivity rather than claiming specific monthly savings.

## 3.3 Power factor

Our DC testbed has PF = 1.0 (DC loads are purely resistive/motor). In the model we use kW directly. In real industrial settings, low PF increases kVA demand. This is a documented limitation.

---

# PART 4 — MATHEMATICAL FORMULATION

## 4.1 Modelling approach: CP-SAT with interval variables

> [!IMPORTANT]
> **Correction from previous report.** The previous report described a time-indexed MILP with binary variables $x_{omt}$. OR-Tools CP-SAT performs much better with **interval variables** and built-in scheduling constraints (`AddNoOverlap`). We reformulate using CP-SAT's native constructs.

### Sets

| Symbol | Definition |
|---|---|
| $\mathcal{J} = \{1, \ldots, n\}$ | Jobs |
| $\mathcal{O}_j = \{(j,1), \ldots, (j,n_j)\}$ | Ordered operations of job $j$ |
| $\mathcal{M} = \{1, \ldots, m\}$ | Machines |
| $\mathcal{T}_{\text{slots}}$ | Set of discrete time-slot boundaries (for energy/peak accounting) |
| $\mathcal{M}_o \subseteq \mathcal{M}$ | Eligible machines for operation $o$ |

### Parameters

| Symbol | Definition | Unit | Source |
|---|---|---|---|
| $p_o$ | Processing time of operation $o$ | integer time units | Model input |
| $P^{\text{proc}}_m$ | Power draw of machine $m$ when processing | W | Measured (INA226) |
| $P^{\text{idle}}_m$ | Power draw of machine $m$ when idle | W | Measured |
| $E^{\text{start}}_m$ | Startup energy of machine $m$ | Wh | Measured |
| $\pi_t$ | Electricity price in time slot $t$ | ₹/kWh | Tariff model |
| $\rho$ | Demand-charge parameter | ₹/kW | Parameterised |
| $d_j$ | Deadline for job $j$ | time units | Optional |
| $H$ | Scheduling horizon | time units | Derived |

### Decision variables (CP-SAT interval formulation)

For each operation $o$ (with duration $p_o$):

| Variable | CP-SAT type | Meaning |
|---|---|---|
| $\text{start}_o$ | `NewIntVar(0, H)` | Start time of operation $o$ |
| $\text{end}_o$ | `NewIntVar(0, H)` | End time of operation $o$ |
| $\text{interval}_o$ | `NewIntervalVar(start, p_o, end)` | Interval representation |

For flexible job-shop (operation assignable to multiple machines):

| Variable | CP-SAT type | Meaning |
|---|---|---|
| $\text{mchoice}_{o,m}$ | `NewBoolVar()` | 1 if $o$ assigned to machine $m$ |
| $\text{opt\_interval}_{o,m}$ | `NewOptionalIntervalVar(...)` | Optional interval per candidate |

For time-slot accounting:

| Variable | CP-SAT type | Meaning |
|---|---|---|
| $\text{load}_{m,t}$ | `NewBoolVar()` | 1 if machine $m$ is processing during slot $t$ |
| $\text{slot\_power}_t$ | `NewIntVar(0, ...)` | Total power in slot $t$ (watts, integer) |
| $P^{\text{peak}}$ | `NewIntVar(0, ...)` | Maximum of all $\text{slot\_power}_t$ |

### Objective functions

**F1 — Makespan:**
$$\min\ C_{\max} = \max_{j} \text{end}_{(j, n_j)}$$

CP-SAT: `model.AddMaxEquality(makespan, [end_vars of last operations])`

**F2 — Energy cost:**

$$\text{EnergyCost} = \sum_{t} \text{slot\_power}_t \cdot \Delta \cdot \pi_t \cdot 10^{-3}$$

Since CP-SAT works with integers, multiply all costs by a scaling factor (e.g., 1000) to avoid floating-point.

**F3 — Peak demand:**
$$\min\ P^{\text{peak}} = \max_{t} \text{slot\_power}_t$$

CP-SAT: `model.AddMaxEquality(peak_power, slot_power_vars)`

### Constraints

**C1 — Precedence:** Operations within a job must execute in order.
```python
for j in jobs:
    for k in range(len(j.operations) - 1):
        model.Add(start[j,k+1] >= end[j,k])
```
*Each operation starts after its predecessor finishes.*

**C2 — Machine non-overlap:** At most one operation on each machine at any time.
```python
for m in machines:
    model.AddNoOverlap(intervals_on_machine[m])
```
*No two operations on the same machine can overlap.*

**C3 — Assignment (flexible job-shop):** Each operation assigned to exactly one eligible machine.
```python
for o in operations:
    model.AddExactlyOne(mchoice[o, m] for m in eligible[o])
```

**C4 — Time-slot power accounting:** For each slot $t$ and machine $m$, determine if $m$ is processing.

This requires channelling constraints between interval variables and boolean slot variables. For each operation $o$ on machine $m$, if $o$'s interval overlaps slot $t$:

```python
# For each slot t (covering [t*delta, (t+1)*delta)):
# load[m,t] = 1 iff some operation on m overlaps slot t
# This uses reification and interval overlap logic
```

**Implementation note:** This is the most complex part. Two approaches:
1. **Element-based:** For each slot, check if start ≤ t*delta and end > t*delta.
2. **Cumulative-based:** Use `AddCumulative` with capacity 1 per machine and energy demands linked to intervals.

Start with approach 1 for clarity; optimise if slow.

**C5 — Slot power summation:**
```python
for t in slots:
    model.Add(slot_power[t] == sum(load[m,t] * P_proc[m] for m in machines))
```
*Total power in slot $t$ equals sum of processing power of all active machines.*

**C6 — Peak demand:**
```python
for t in slots:
    model.Add(peak_power >= slot_power[t])
```
*Peak power must be at least as large as power in any slot.*

**C7 — Makespan:**
```python
for j in jobs:
    model.Add(makespan >= end[j, last_op[j]])
```

**C8 — Deadline (optional):**
```python
for j in jobs:
    if deadline[j] is not None:
        model.Add(end[j, last_op[j]] <= deadline[j])
```

### Model hierarchy

| Model | Objectives | Constraints | Purpose |
|---|---|---|---|
| M0: Makespan-only | min $C_{\max}$ | C1, C2, C3, C7 | Baseline |
| M1: Energy-only | min EnergyCost | C1, C2, C3, C4, C5, C7 | Baseline |
| M2: Bi-objective | min {$C_{\max}$, EnergyCost} via ε-constraint | C1–C5, C7 | Comparison |
| **M3: Tri-objective** | **min {$C_{\max}$, EnergyCost, $P^{\text{peak}}$}** | **C1–C7** | **Proposed** |

### Assumptions stated honestly

| Assumption | Realistic? | If violated | Mitigation |
|---|---|---|---|
| Deterministic processing times | No (±10-30% in reality) | Schedule may miss deadlines | Document; stretch: uncertainty study |
| Constant $P^{\text{proc}}_m$ during processing | Approximately yes for steady-state loads | Energy estimate error | Use measured average; report error |
| No machine breakdowns | Unrealistic long-term | Schedule becomes infeasible | Excluded; acknowledge |
| Jobs known in advance | Yes for batch production | N/A | Appropriate for MSME batch |
| Piecewise-constant tariff | Yes — Indian ToD tariffs are block rates | N/A | Matches real structure |
| PF = 1 (DC testbed) | No (real machines have PF < 1) | kW ≠ kVA | Document as limitation |

---

# PART 5 — OPTIMIZATION METHOD

## 5.1 Method comparison

| Method | Multi-obj? | Non-convex Pareto? | Guarantees | Solves needed | Feasibility |
|---|---|---|---|---|---|
| Weighted sum | Yes | **No** — misses non-convex regions | Optimal per weight | 1 per weight combo | Easy |
| ε-constraint | Yes | **Yes** | Optimal per ε (if solver proves optimal) | 1 per ε | Easy |
| AUGMECON | Yes | **Yes** | Pareto-efficient (not weakly dominated) if solver optimal | k² for 3-obj | Moderate |
| NSGA-II/III | Yes | Yes | No optimality guarantee | Population × generations | Moderate |
| CP-SAT direct | Single | N/A | Proves optimality or reports gap | 1 | Easy |

## 5.2 Selected: ε-constraint via CP-SAT (AUGMECON-style)

### What AUGMECON guarantees (precisely)

> [!WARNING]
> AUGMECON guarantees that every returned solution is **Pareto-efficient** (not weakly dominated) — **IF the underlying solver finds the true global optimum for each sub-problem.** If the solver returns sub-optimal solutions (e.g., due to time limits), the guarantees weaken: solutions are feasible and high-quality but not provably Pareto-efficient. Always report solver status and optimality gap.

### ε-constraint workflow (pseudocode)

```
INPUT: instance I, grid sizes k1, k2
OUTPUT: Pareto-efficient solution set S

# Step 1: Find anchor points
C_max_min = solve(min C_max, subject to C1-C3,C7)
EC_min    = solve(min EnergyCost, subject to C1-C5,C7)
PP_min    = solve(min P_peak, subject to C1-C7)

C_max_max = max(C_max across individual optima)
EC_max    = max(EC across individual optima)
PP_max    = max(PP across individual optima)

# Ranges
r1 = C_max_max - C_max_min   # makespan range
r2 = PP_max - PP_min          # peak power range

# Step 2: ε-grid over makespan and peak power
S = empty set
for i = 0 to k1:
    eps_cmax = C_max_min + i * r1 / k1
    for j = 0 to k2:
        eps_pp = PP_min + j * r2 / k2

        # Step 3: Sub-problem (AUGMECON formulation)
        # Primary: min EnergyCost - delta*(s1/r1 + s2/r2)
        # Subject to:
        #   C_max <= eps_cmax + s1   (s1 >= 0, surplus variable)
        #   P_peak <= eps_pp + s2    (s2 >= 0, surplus variable)
        #   all scheduling constraints C1-C7
        # delta = small (e.g., 1e-3 * EC_range)

        result = solve_augmecon_subproblem(eps_cmax, eps_pp)
        if result.status in [OPTIMAL, FEASIBLE]:
            S.add(result.solution)

# Step 4: Filter dominated solutions
S = remove_dominated(S)

RETURN S
```

### Key implementation details

- **Grid size:** Start with k1 = k2 = 10 (100 sub-problems). Increase if Pareto surface is sparse.
- **Solver time limit per sub-problem:** Do NOT pre-specify. Start with pilot runs on 2–3 instances to determine typical solve time. Set limit to 2× median solve time.
- **Objective scaling for AUGMECON:** Surplus variables $s_1$, $s_2$ are scaled by objective ranges $r_1$, $r_2$.
- **Integer scaling:** CP-SAT uses integers. Multiply energy cost by 1000 to preserve 3 decimal places.
- **Infeasibility:** If sub-problem infeasible (ε too tight), skip. Record as infeasible cell.
- **Solver seed:** `solver.parameters.random_seed = 42` for reproducibility.

---

# PART 6 — SOFTWARE ARCHITECTURE

## 6.1 Folder structure

```
energy_scheduling/
├── README.md
├── requirements.txt
├── config/
│   ├── default_config.yaml
│   └── tariff_profiles/
│       ├── bescom_ht2a.yaml
│       └── parametric.yaml
├── data/
│   ├── instances/
│   │   ├── small/                 # 5x3
│   │   ├── medium/                # 8x4
│   │   └── large/                 # 10x5, 15x6
│   └── measured/
│       ├── machine_profiles.csv
│       └── calibration_logs/
├── src/
│   ├── __init__.py
│   ├── model/
│   │   ├── __init__.py
│   │   ├── instance.py            # Data classes
│   │   ├── tariff.py              # Tariff model
│   │   └── solution.py            # Schedule solution
│   ├── solver/
│   │   ├── __init__.py
│   │   ├── cpsat_model.py         # CP-SAT model builder
│   │   ├── epsilon_constraint.py  # AUGMECON loop
│   │   └── baselines.py           # FCFS, SPT dispatchers
│   ├── evaluation/
│   │   ├── __init__.py
│   │   ├── metrics.py             # Cost, peak, makespan, bill
│   │   ├── pareto.py              # Dominance, hypervolume
│   │   └── statistics.py          # Wilcoxon, Friedman
│   ├── generators/
│   │   ├── __init__.py
│   │   └── instance_generator.py
│   └── visualization/
│       ├── __init__.py
│       ├── gantt.py
│       ├── pareto_plot.py
│       ├── sensitivity_plot.py
│       └── power_trace.py
├── experiments/
│   ├── exp_a_baseline.py
│   ├── exp_b_biobj_pareto.py
│   ├── exp_c_triobj_vs_biobj.py
│   ├── exp_d_demand_charge.py
│   ├── exp_e_tod_sensitivity.py
│   ├── exp_f_workload.py
│   ├── exp_g_heterogeneity.py
│   ├── exp_h_scalability.py
│   ├── exp_i_model_fidelity.py
│   ├── exp_j_physical.py
│   └── run_all.py
├── hardware/
│   ├── esp32/
│   │   └── firmware.ino
│   ├── calibration/
│   │   └── calibrate.py
│   └── testbed_controller.py
├── deployment/
│   ├── rpi_setup.sh
│   └── benchmark.py
├── results/
│   ├── raw/
│   ├── processed/
│   └── plots/
└── tests/
    ├── test_model.py
    ├── test_solver.py
    ├── test_baselines.py
    └── test_metrics.py
```

## 6.2 Key data class: `src/model/instance.py`

```python
from dataclasses import dataclass, field

@dataclass
class Operation:
    job_id: int
    op_index: int
    eligible_machines: list[int]
    processing_time: int  # integer time units

@dataclass
class Machine:
    machine_id: int
    power_processing_w: float
    power_idle_w: float
    startup_energy_wh: float

@dataclass
class TariffSlot:
    slot_index: int
    price_per_kwh: float  # ₹/kWh, ToD-adjusted

@dataclass
class Instance:
    name: str
    jobs: list[list[Operation]]
    machines: list[Machine]
    tariff_slots: list[TariffSlot]
    demand_charge_rate: float  # rho, ₹/kW
    time_slot_width_hours: float
    horizon: int
    deadlines: dict[int, int] | None = None
    seed: int = 0
```

## 6.3 Input/output CSV formats

**Instance CSV:** See Part 7 for specification.

**Results CSV columns:**
```
experiment_id, instance_name, method, makespan, energy_cost, peak_power_w,
total_bill, solve_time_s, solver_status, optimality_gap, seed, timestamp
```

---

# PART 7 — DATA MODEL

## 7.1 Instance parameters

| Parameter | Small | Medium | Large |
|---|---|---|---|
| Jobs ($n$) | 5 | 8 | 10–15 |
| Machines ($m$) | 3 | 4 | 5–6 |
| Ops per job | 2–3 | 2–4 | 3–5 |
| Processing times | U(1, 6) | U(1, 8) | U(1, 10) |
| Machine eligibility | 1–2 per op | 1–3 | 1–3 |
| Power (processing, W) | Depends on heterogeneity level | | |
| Time slot width | 1 unit (maps to 15 min in model, 15 sec in testbed) | | |
| Horizon | 48 slots | 64 slots | 96 slots |

## 7.2 Power heterogeneity levels

| Level | $P^{\text{proc}}$ range (W) | Meaning |
|---|---|---|
| Low | U(100, 150) | All machines similar |
| Medium | U(50, 250) | Moderate spread |
| High | U(30, 400) | One machine 13× another |

## 7.3 Workload intensity

$$\lambda = \frac{\sum_o p_o}{m \times H}$$

| Level | $\lambda$ | Meaning |
|---|---|---|
| Light | 0.3 | Plenty of slack |
| Moderate | 0.5 | Some scheduling freedom |
| Heavy | 0.7 | Tight |
| Very heavy | 0.9 | Very little room |

Adjust processing times or horizon to achieve target $\lambda$.

## 7.4 Reproducibility

- 20 instances per (size, heterogeneity, intensity) combination
- Seeds: 1000, 1001, ..., 1019
- All instances saved as CSV with full metadata
- Generator script is deterministic given seed

---

# PART 8 — BASELINES

| ID | Method | Algorithm | Objective optimised | Implementation |
|---|---|---|---|---|
| B0 | FCFS | Schedule operations in job order. Assign to first available eligible machine. | None (arrival order) | Greedy dispatcher |
| B1 | SPT | Sort all operations by shortest processing time. Assign to earliest-available eligible machine. | Heuristic: reduce flow time | Greedy dispatcher |
| B2 | Makespan-only | CP-SAT: min $C_{\max}$ subject to C1, C2, C3, C7. | min makespan | CP-SAT |
| B3 | Energy-only | CP-SAT: min EnergyCost subject to C1–C5, C7. | min energy cost | CP-SAT |
| P1 | Bi-objective | ε-constraint: min {$C_{\max}$, EnergyCost}. | Pareto front (2D) | ε-constraint |
| P2 | Tri-objective | ε-constraint: min {$C_{\max}$, EnergyCost, $P^{\text{peak}}$}. | Pareto surface (3D) | AUGMECON |

**Essential:** B0, B1, B2, B3, P1, P2.

---

# PART 9 — EXPERIMENTAL DESIGN

## Experiment A — Baseline comparison (CORE)

- **RQ:** How do FCFS, SPT, makespan-only, energy-only compare on all metrics?
- **IV:** Scheduling method (B0, B1, B2, B3)
- **DV:** Makespan, energy cost, peak power, total bill
- **Controlled:** 20 medium instances (8×4), BESCOM reference tariff, $\rho$ = reference
- **Statistical test:** Friedman test + post-hoc Nemenyi
- **Plots:** Box plots per metric per method

## Experiment B — Bi-objective Pareto front (CORE)

- **RQ:** What is the shape of the makespan–energy-cost Pareto front?
- **IV:** ε (makespan bound)
- **DV:** Energy cost, peak power (observed), total bill
- **Instances:** 10 medium
- **Key analysis:** Does peak power change as you move along the front? If yes → coupled. If no → independent.

## Experiment C — Tri-obj vs bi-obj (CORE)

- **RQ:** Does adding peak demand as a 3rd objective produce different Pareto-efficient schedules?
- **IV:** Model (P1 vs P2)
- **DV:** Total bill (Common Evaluation Space — see Part 10)
- **Instances:** 20 medium
- **Test:** Wilcoxon signed-rank on best-bill from each Pareto set

## Experiment D — Demand-charge sensitivity (CORE)

- **RQ:** How does benefit of peak-awareness change with $\rho$?
- **IV:** $\rho \in \{0, 25, 50, 100, 150, 200, 300, 400, 500\}$ ₹/kW
- **DV:** Total bill difference (P1 best-bill vs P2 best-bill)
- **Instances:** 10 medium
- **Plots:** Savings vs $\rho$ curve
- **Expected:** Benefit increases with $\rho$; at $\rho = 0$, no difference

## Experiment E — ToD sensitivity (CORE)

- **RQ:** How does peak/off-peak price ratio affect benefit?
- **IV:** Peak multiplier ∈ {1.0, 1.05, 1.10, 1.15, 1.20, 1.30, 1.50, 2.0}
- **DV:** Energy cost savings, total bill savings
- **Instances:** 10 medium
- **Plots:** Savings vs multiplier

## Experiment F — Workload intensity (CORE)

- **RQ:** Does utilisation affect peak-aware scheduling benefit?
- **IV:** $\lambda \in \{0.3, 0.5, 0.7, 0.9\}$
- **DV:** Peak power, total bill
- **Instances:** 10 per level
- **Hypothesis:** Higher $\lambda$ → more machine overlap → higher peak → more benefit

## Experiment G — Machine power heterogeneity (CORE)

- **RQ:** Does heterogeneity in power draw affect benefit?
- **IV:** Heterogeneity level: low, medium, high
- **DV:** Peak power variance, total bill
- **Instances:** 10 per level

## Experiment H — Scalability (CORE: laptop; STRETCH: RPi)

- **RQ:** At what size does CP-SAT fail to find good solutions within time limits?
- **IV:** Size: 5×3, 8×4, 10×5, 12×5, 15×6
- **DV:** Solve time, optimality gap, Pareto points
- **Platform:** Laptop AND RPi 5

## Experiment I — Model fidelity (CORE — physical)

- **RQ:** How accurately does the model predict energy and peak?
- **IV:** Schedule variant (FCFS, optimised)
- **DV:** Prediction error (energy, peak)
- **Procedure:** 5 schedules × 3 repetitions on testbed
- **Metrics:** MAE, RMSE, relative error
- **Acceptance:** Error characterised relative to measurement uncertainty (see Part 15)

## Experiment J — Physical validation (CORE — physical)

- **RQ:** Does the optimised schedule produce lower measured cost/peak than FCFS on the testbed?
- **IV:** Schedule: FCFS vs optimised
- **DV:** Measured energy, measured peak, execution time
- **Repetitions:** 3 per schedule

---

# PART 10 — PARETO ANALYSIS

## 10.1 The comparison problem

Comparing a 2-objective Pareto front (P1) against a 3-objective Pareto surface (P2) using raw hypervolume is invalid — they live in different objective spaces.

## 10.2 Solution: Common Evaluation Space

Both P1 and P2 produce *schedules*. Every schedule has values for ALL three objectives (makespan, energy cost, peak power) even if peak was not optimised by P1.

1. Evaluate ALL P1 and P2 solutions on the SAME 3 metrics.
2. Compute total bill: $\text{Bill} = \text{EC} + \rho \cdot P^{\text{peak}}$.
3. For each instance, compare best-bill from P1 vs best-bill from P2.
4. Hypervolume in 3D: compute HV for P1 solutions (in 3D) vs P2 solutions (in 3D) using same reference point.

## 10.3 Metrics

| Metric | Use |
|---|---|
| Best-bill | Primary comparison |
| Hypervolume (3D, normalised) | Pareto approximation quality |
| Spacing | Distribution |
| Number of Pareto points | Coverage |

## 10.4 Normalisation

Each objective normalised to [0, 1] using global min/max across ALL solutions (P1 ∪ P2) per instance. Reference point: (1.1, 1.1, 1.1).

---

# PART 11 — SENSITIVITY / PHASE-MAP STUDY

## 11.1 Factor grid

| Factor | Symbol | Levels |
|---|---|---|
| Demand-charge rate | $\rho$ | {0, 50, 100, 200, 365, 500} ₹/kW |
| ToD multiplier | $\alpha$ | {1.0, 1.1, 1.2, 1.3, 1.5} |
| Workload intensity | $\lambda$ | {0.3, 0.5, 0.7, 0.9} |
| Power heterogeneity | $\sigma$ | {low, medium, high} |

Full factorial: 6 × 5 × 4 × 3 = 360 cells, 5 instances each → 1,800 runs per model.

If too many: use a reduced design (fix $\lambda$ = 0.7, $\sigma$ = medium, sweep $\rho$ × $\alpha$ first → 30 cells × 5 = 150 runs. Expand later.).

## 11.2 Metric per cell

$$\Delta\text{Bill}(\%) = \frac{\text{BestBill}_{P1} - \text{BestBill}_{P2}}{\text{BestBill}_{P1}} \times 100$$

## 11.3 Visualisation

- 2D heatmap of $\Delta\text{Bill}(\%)$ vs ($\rho$, $\alpha$) at fixed ($\lambda$, $\sigma$)
- Contour line where $\Delta\text{Bill} = 0$ — "phase boundary"
- Slice plots for each factor

## 11.4 Evidence criteria

- **For H1:** A region where $\Delta\text{Bill} > 0$ consistently AND a region where ≈ 0, with clear boundary.
- **Against H1:** $\Delta\text{Bill} ≈ 0$ everywhere (peak-awareness never helps) — valid negative result.
- **Trivial support:** Benefit only at extreme unrealistic parameters.

---

# PART 12 — HARDWARE ARCHITECTURE

## 12.1 Measurement correction

> [!IMPORTANT]
> **PZEM-004T is an AC measurement device. It cannot measure DC power.** Our testbed uses 12V DC loads. We use **INA226** modules (I²C, 16-bit, DC) instead.

### Component table

| Component | Purpose | Interface | Notes |
|---|---|---|---|
| **INA226** (×3) | DC V/I/P measurement per load | I²C to ESP32 | 16-bit, ~±0.1%, 0–36V, up to 3.2A |
| **ESP32-WROOM-32** | Controller + I²C + relay + WiFi | GPIO, I²C, WiFi | |
| **4-channel relay module** | Load switching | GPIO | 5V coil, switches 12V |
| **12V DC loads** | Machine emulators | Relay-switched | |
| **12V 10A SMPS** | Power for loads | Mains (enclosed unit) | **Students do NOT open** |
| **Raspberry Pi 5** (borrowed) | Optimization server | WiFi | |

### Block diagram

```
┌─────────────── 12V DC Supply (enclosed) ──────────────────┐
│                                                            │
├──→ Relay 1 ──→ INA226(0x40) ──→ Load 1 (Motor, ~24W) ──→ GND
├──→ Relay 2 ──→ INA226(0x41) ──→ Load 2 (Heater, ~40W) ──→ GND
├──→ Relay 3 ──→ INA226(0x44) ──→ Load 3 (LED, ~12W) ──→ GND
│
│   ┌──────────┐  I²C (SDA/SCL)  ┌──────────────────────────┐
│   │  ESP32   │◄───────────────►│ INA226 × 3 (shared bus)  │
│   │          │  GPIO           └──────────────────────────┘
│   │          │──────────────────→ Relay Module (4ch)
│   │          │  WiFi/MQTT
│   │          │◄──────────────────────► Raspberry Pi 5
│   └──────────┘
```

### I²C addresses

- INA226 #1: A0=GND, A1=GND → 0x40
- INA226 #2: A0=VS, A1=GND → 0x41
- INA226 #3: A0=GND, A1=VS → 0x44

### Safety

- ALL loads are 12V DC. No mains on breadboard.
- 12V supply is enclosed commercial unit — not opened or modified.
- Max total current ~8A, within 10A supply rating.
- Relay module provides galvanic isolation (ESP32 3.3V ↔ load 12V).

## 12.2 BOM

| Component | Qty | ₹/unit | Total ₹ |
|---|---|---|---|
| ESP32-WROOM-32 DevKit | 1 | 500 | 500 |
| INA226 breakout | 3 | 180 | 540 |
| 4-channel relay module | 1 | 200 | 200 |
| DC motor (775, 12V) | 1 | 250 | 250 |
| Ceramic heater (12V, 40W) | 1 | 100 | 100 |
| LED strip (12V, 1m) | 1 | 150 | 150 |
| 12V 10A SMPS | 1 | 350 | 350 |
| Breadboard + wires | 1 | 200 | 200 |
| **Total** | | | **₹2,290** |
| Raspberry Pi 5 (borrowed) | 1 | — | 0 |

---

# PART 13 — PHYSICAL TESTBED

## 13.1 Load-to-machine mapping

| Load | Machine | Expected P_proc | Notes |
|---|---|---|---|
| DC Motor (775) | M1 | ~24W | Motor-type process |
| Ceramic heater (12V) | M2 | ~40W | Thermal process |
| LED strip (12V) | M3 | ~12W | Light-duty process |

## 13.2 Operation mapping

One "processing operation" = relay ON for $p_o$ time units. Time unit = 15 seconds (physical demo).

## 13.3 What it proves / does not prove

| Can demonstrate | Cannot demonstrate |
|---|---|
| Energy model predicts measured energy within quantified error | Works on real industrial machines |
| Optimised schedule physically executes correctly | Monthly demand charge savings |
| Peak power matches prediction | Scales to factory size |
| Observable difference between FCFS and optimised | System works unsupervised |

---

# PART 14 — CALIBRATION PROTOCOL

For each load:

**Step 1: Steady-state power.** Turn ON. Wait 5s. Sample INA226 at 10 Hz for 60s. Record mean(P), std(P).

**Step 2: Idle power.** If modelled: apply idle config. Sample 60s. Record.

**Step 3: Startup energy.** Record OFF→ON transient. Integrate power until stable (within 5%). Repeat 5×. Report mean, variance.

**Step 4: Repeat** on 3 occasions. Report overall mean, std, CoV.

**Output:** `data/measured/machine_profiles.csv`:
```csv
machine_id,P_proc_mean_W,P_proc_std_W,P_idle_mean_W,P_idle_std_W,E_start_mean_Wh,E_start_std_Wh,n_trials,date
```

---

# PART 15 — SIMULATION ↔ HARDWARE VALIDATION

## Metrics

| Metric | Formula |
|---|---|
| Energy relative error | $\|E_{\text{pred}} - E_{\text{meas}}\| / E_{\text{meas}}$ |
| Peak relative error | $\|P^{\text{peak}}_{\text{pred}} - P^{\text{peak}}_{\text{meas}}\| / P^{\text{peak}}_{\text{meas}}$ |
| Power trace MAE | $\frac{1}{T}\sum_t \|P_{\text{pred}}(t) - P_{\text{meas}}(t)\|$ |
| Power trace RMSE | $\sqrt{\frac{1}{T}\sum_t (P_{\text{pred}}(t) - P_{\text{meas}}(t))^2}$ |

## Acceptance

Do NOT pre-specify thresholds. Instead:
1. Calibration uncertainty (Part 14) sets the measurement floor.
2. If calibration shows ±5% power variability → prediction error <10% is reasonable.
3. Report BOTH the error AND the measurement uncertainty.

---

# PART 16 — RASPBERRY PI DEPLOYMENT

## Software

```bash
# Raspberry Pi OS Lite 64-bit (Bookworm)
sudo apt update && sudo apt install -y python3-pip python3-venv mosquitto
python3 -m venv ~/env && source ~/env/bin/activate
pip install ortools numpy pandas paho-mqtt pyyaml matplotlib
```

## Benchmark

Solve same instances on laptop and RPi 5. Report speedup ratio = time(RPi)/time(laptop).

This is an **engineering/deployment evaluation**, not research novelty.

---

# PART 17 — END-TO-END WORKFLOW

```
1. Generate instance → CSV
2. Load instance + tariff config → Instance object
3. Run baselines (B0–B3) → schedules + metrics → CSV
4. Run bi-objective ε-constraint (P1) → Pareto front → CSV
5. Run tri-objective AUGMECON (P2) → Pareto surface → CSV
6. Evaluate ALL solutions in Common 3D Space → total bill → CSV
7. [Physical] Select FCFS + optimised schedule
8. [Physical] RPi → MQTT → ESP32 → execute → INA226 → measure
9. [Physical] Compare predicted vs measured → validation metrics
10. Aggregate across instances → statistical tests → plots
11. Generate sensitivity heatmaps → phase maps
```

---

# PART 18 — FAILURE MODES

| # | Symptom | Cause | Fix | Fallback |
|---|---|---|---|---|
| 1 | CP-SAT INFEASIBLE | ε too tight | Skip cell; expected near Pareto boundary | Normal |
| 2 | CP-SAT timeout | Instance too large | Increase time limit; reduce size | Report gap |
| 3 | Few Pareto points | Grid too coarse; objectives not conflicting | Finer grid; verify formulation | Report sparse front |
| 4 | All methods same bill | $\rho$ too low; tariff flat | Valid result | Report "no benefit" |
| 5 | INA226 reads 0 | Wiring error; wrong address | I²C scan; check wiring | Swap module |
| 6 | Relay won't switch | GPIO issue; needs 5V logic | Level shifter or transistor | MOSFET switch |
| 7 | MQTT drops | WiFi; Mosquitto down | Check service; serial fallback | Direct serial |
| 8 | Measured ≫ predicted | Load draws more than calibrated | Recalibrate | Update model |
| 9 | Measured ≪ predicted | Load partial; relay intermittent | Check connections | Replace load |
| 10 | RPi too slow | ARM limitations | Reduce instance size | Report as limit |
| 11 | Timing drift | ESP32 millis() drift | Hardware timer; NTP sync | Document error |
| 12 | Supply overloaded | All loads simultaneous | Check total; stagger | Higher-rated supply |
| 13 | Wrong constraints | Bug in CP-SAT model | Verify on 2×2 by hand | Test suite |
| 14 | Trivial instances | Too much slack | Check $\lambda$; adjust | Regenerate |

---

# PART 19 — REPRODUCIBILITY

## Git structure

```
energy-scheduling/
├── .gitignore          # __pycache__, .env, results/raw/
├── README.md           # Setup, run, reproduce
├── requirements.txt    # Pinned versions
├── config/             # Committed
├── data/instances/     # Committed (generated, deterministic)
├── data/measured/      # Committed (calibration data)
├── src/                # Committed
├── experiments/        # Committed
├── hardware/           # Committed
├── tests/              # Committed
├── results/            # .gitignore (use releases for data)
└── docs/               # Committed
```

## Checklist

- [ ] `requirements.txt` with pinned versions
- [ ] Random seeds in instance files
- [ ] CP-SAT seed: `solver.parameters.random_seed = 42`
- [ ] All instances committed
- [ ] README: clone → install → run
- [ ] Hardware BOM, wiring, firmware committed
- [ ] Calibration data committed
- [ ] Raw results as CSV with experiment ID + timestamp

---

# PART 20 — PROJECT TIMELINE

## 20.1 One-week emergency plan

| Day | Task | Output |
|---|---|---|
| 1 | Install OR-Tools. Implement data classes. Build 3 test instances by hand. | Python env; 3 CSVs |
| 2 | Implement M0 (makespan-only CP-SAT). Verify on 2×2 by hand. | Working solver |
| 3 | Add energy cost (M1). Add FCFS/SPT. First comparison table. | B0, B1, M0, M1 |
| 4 | Implement ε-constraint for bi-obj (P1). Generate Pareto front. | 2D Pareto plot |
| 5 | Add peak demand (M3). Tri-objective loop (P2). | 3D Pareto points |
| 6 | Instance generator. 20 medium instances. Run Exp A. | Baseline results |
| 7 | Run Exp C (P1 vs P2). First sensitivity (Exp D, 3 values of $\rho$). | Core results draft |

## 20.2 Four-week realistic plan

| Week | Focus | Deliverables |
|---|---|---|
| 1 | Software: M0–M3, B0–B3, P1, P2, instance generator, tests | Working system. Verified on small instances. |
| 2 | Experiments A–E. Statistical analysis. Plots. | Results CSVs. Preliminary analysis. |
| 3 | Hardware: order → assemble → calibrate → validate model. | Testbed. Calibration data. Exp I, J. |
| 4 | Experiments F–G. Phase-map. RPi deploy + benchmark. Report. | Complete results. Heatmaps. Draft report. |

## 20.3 Eight-week complete plan

| Week | Focus | Deliverables |
|---|---|---|
| 1 | Literature review. Tariff verification. KERC PDF. | Lit spreadsheet. Tariff doc. |
| 2 | Core software. Instance generator. Unit tests. | Working M0–M3, baselines, 60 instances. |
| 3 | ε-constraint. Pareto code. Visualisation. | P1, P2. Pareto plots. |
| 4 | Experiments A–C. | Baseline comparison. Bi vs tri. |
| 5 | Experiments D–G. Phase-map. | Sensitivity plots. Heatmaps. |
| 6 | Hardware: order, assemble, calibrate. | Testbed. Calibration log. |
| 7 | Physical validation (Exp I, J). RPi deploy + benchmark. | Validation. RPi results. |
| 8 | Report. Poster. Final polish. | Complete deliverables. |

### Critical path

```
Tariff verify (W1) → Formulation (W1) → CP-SAT (W2) → ε-constraint (W3)
→ Experiments A–C (W4) → Sensitivity (W5) → Report (W8)

[Parallel:] Hardware order (W2) → Assemble (W6) → Calibrate (W6) → Validate (W7)
```

---

# PART 21 — DEFINITION OF DONE

- [ ] Tariff verified against official KERC PDF (downloaded, cited)
- [ ] Formulation documented, all symbols defined, verified by hand on 2×2
- [ ] CP-SAT solves M0, M1, M2, M3 correctly
- [ ] ε-constraint produces Pareto front (2D) and surface (3D)
- [ ] Baselines (FCFS, SPT, makespan-only, energy-only) correct
- [ ] Instance generator creates reproducible instances
- [ ] Experiment A complete with statistical test
- [ ] Experiment C complete with Common Evaluation Space
- [ ] Experiment D complete with savings-vs-ρ plot
- [ ] Experiment E complete
- [ ] Experiment F complete
- [ ] Phase-map produced (at least ρ × α heatmap)
- [ ] Physical testbed assembled and powered
- [ ] Calibration complete with uncertainty
- [ ] Experiment I: prediction error reported with uncertainty
- [ ] Experiment J: FCFS vs optimised on testbed
- [ ] RPi deployment working
- [ ] RPi benchmark reported
- [ ] All results saved as CSV
- [ ] All plots generated
- [ ] Limitations documented honestly
- [ ] Novelty claims match Part 1 taxonomy
- [ ] Code committed with README + requirements.txt
- [ ] Report complete

---

# PART 22 — START HERE

The first 10 concrete actions to begin immediately.

---

### Action 1: Install OR-Tools and verify

**Task:** Install Python dependencies.

```bash
pip install ortools numpy pandas pyyaml matplotlib scipy
python -c "from ortools.sat.python import cp_model; print('CP-SAT OK')"
```

**Output:** No errors. CP-SAT imports.
**Done when:** Import succeeds.

---

### Action 2: Create project directory structure

**Task:** Create folders from Part 6.1. Initialise Git.

```bash
mkdir -p energy_scheduling/{config/tariff_profiles,data/{instances/{small,medium,large},measured/calibration_logs},src/{model,solver,evaluation,generators,visualization},experiments,hardware/{esp32,calibration},deployment,results/{raw,processed,plots},tests,docs}
cd energy_scheduling && git init
```

**Output:** Full directory tree. `.git/` exists.
**Done when:** `find . -type d` shows all directories.

---

### Action 3: Implement Instance data model

**Task:** Create `src/model/instance.py` with dataclasses from Part 6.2. Create `src/model/tariff.py` with `build_tariff_slots()`.

**Output:** Two .py files that import without error.
**Done when:** `python -c "from src.model.instance import Instance"` works.

---

### Action 4: Build a 2×2 test instance by hand

**Task:** Create `data/instances/small/test_2x2.csv`: 2 jobs, 2 machines, 2 operations per job. Compute optimal makespan on paper. Draw the Gantt chart.

**Output:** CSV file + hand-computed answer written in `docs/verification_notes.md`.
**Done when:** You can explain the optimal makespan and why.

---

### Action 5: Implement makespan-only CP-SAT model (M0)

**Task:** Create `src/solver/cpsat_model.py`. Implement interval variables, precedence, NoOverlap, makespan objective. Solve `test_2x2`.

**Output:** Solver returns makespan matching hand calculation.
**Done when:** Optimal makespan matches paper answer.

---

### Action 6: Implement FCFS and SPT baselines

**Task:** Create `src/solver/baselines.py`. Implement FCFS and SPT dispatchers. Run on `test_2x2`.

**Output:** Valid schedules (no overlap, precedence respected).
**Done when:** Both schedules are valid. SPT makespan ≤ FCFS (usually).

---

### Action 7: Add energy-cost accounting

**Task:** Extend `cpsat_model.py`: time-slot-to-operation mapping, tariff prices, energy cost computation. Create 2-slot tariff (cheap=5, expensive=8 ₹/kWh). Verify by hand.

**Output:** Energy cost for a schedule, matching hand calculation.
**Done when:** Computed cost = manual Σ(P × duration × price) calculation.

---

### Action 8: Add peak-demand constraint and objective

**Task:** Add $P^{\text{peak}}$ variable, slot_power variables, constraint C6. Solve `test_2x2` with `min P_peak`. Check peak = max simultaneous power.

**Output:** $P^{\text{peak}}$ matches manual Gantt inspection.
**Done when:** Peak equals max sum of concurrent machine powers.

---

### Action 9: Implement ε-constraint loop (2-objective)

**Task:** Create `src/solver/epsilon_constraint.py`. Implement Part 5.2 workflow for 2 objectives (makespan, energy cost). Run on 3×2 instance with k=5.

**Output:** 5 Pareto-efficient solutions. 2D scatter plot.
**Done when:** All solutions non-dominated. Plot shows expected tradeoff.

---

### Action 10: Download and verify KERC tariff order

**Task:** Visit kerc.karnataka.gov.in or bescom.karnataka.gov.in. Download latest tariff order PDF. Find HT-2(a) section. Record: demand charge (₹/kVA), energy charge (₹/kWh), ToD multipliers, peak hours, MD measurement.

**Output:** `docs/tariff_reference.md` with values and page-number citations.
**Done when:** Document has demand charge, energy charge, ToD multipliers, peak hours — all with PDF page references.

---

## APPENDIX C — `energy_scheduling_math_research_validation.md`

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

---

## APPENDIX D — `energy_scheduling_research_validation.md`

# Energy Scheduling — Mathematical Research & Engineering Depth Validation

> **Date:** 2026-10-02
> **Posture:** Hostile evaluator. No manufactured novelty. No unsupported percentages.

---

## 1. Audit of the Existing Idea

**Source:** [sdg9_project_audit.md](file:///c:/Project/EL/sdg9_project_audit.md), §6.2, §10.2

### Current formulation

`[ESTABLISHED]` Bi-objective MILP: min{C_max, EnergyCost} with machine-state energy (processing/idle/startup), Indian ToU tariffs, MSME batch production.

### Mathematical model

`[ESTABLISHED]` Standard job-shop MILP with precedence, no-overlap, machine-state variables. ε-constraint for Pareto + NSGA-II for scale.

### Proposed hardware

`[PROPOSED]` PZEM-004T power meter for machine energy profiling. Optional—not load-bearing for core research.

### Optimizer

`[ESTABLISHED]` PuLP / Gurobi (academic). Standard MILP solvers.

### Baseline

`[ESTABLISHED]` FCFS, SPT, energy-unaware MILP.

### Innovation claim

`[OVERCLAIMED]` Prior audit classified this as "contextual novelty (E) and experimental novelty (D)." The formulation is textbook. The Indian-tariff parameterisation is the only differentiator.

### Prototype

`[PROPOSED]` Software-only Gantt + cost dashboard. Prior audit flagged this as "less visually dramatic" and potentially weak on Phase III Innovation/Usability (30 marks).

### Weaknesses (from prior audit)

1. **No mathematical contribution.** The formulation is literally Mouzon (2007) + Gahm (2016) with different parameters.
2. **Software-only prototype** risks scoring poorly on Innovation criterion.
3. **Novelty claim is indefensible** as algorithmic or mathematical contribution.
4. **No uncertainty handling.** Deterministic model only.
5. **No physical validation.** Synthetic instances only.

### Feasibility concerns

- Energy savings may be marginal if tariff differential is small.
- Evaluator sees "applying existing technique with different data."

### Relevant rubric requirements

- **Phase III Prototype (30/200):** Functionality, Innovation, Usability — the highest-weight single criterion.
- **Phase III Results (20/200):** Requires thorough analysis and logical interpretation — needs statistical validation, not single-run.
- **Phase II Tools (20/200):** "Cutting-edge, highly appropriate" tools — standard PuLP/MILP may not score here.

---

## 2. Core Question Answer

> **Can energy-aware manufacturing scheduling become a mathematically rigorous, experimentally falsifiable engineering project with a compelling working prototype?**

| Dimension | Current State | Verdict |
|---|---|---|
| Mathematical research depth | **Zero.** Formulation is textbook MILP from 2007–2016 literature. | ❌ Insufficient |
| Physical engineering depth | **Minimal.** PZEM-004T is optional; core is software-only. | ⚠️ Weak |
| Experimental depth | **Reasonable.** Synthetic instances + statistical comparison is standard OR practice. | ✅ Adequate |
| Prototype quality | **Weak.** Gantt chart + dashboard is standard; no physical demonstration. | ⚠️ Weak |
| SDG 9 relevance | **Strong.** Indian MSMEs + ToU tariffs + SDG 9.4. | ✅ Strong |

**Assessment:** The project as originally proposed is a software optimization demo with Indian parameters. It needs a genuine mathematical research layer and a physical engineering layer. Both are achievable. **MODIFY, then GO.**

---

## 3. Prior-Art / State-of-the-Art

| Work | Model | Objectives | Uncertainty | Physical validation | Main limitation |
|---|---|---|---|---|---|
| Mouzon et al. (2007, IIE) | Single-machine ON/OFF | Energy | None | None | Single machine; no ToU |
| Gahm et al. (2016, EJOR) | Survey: 100+ papers | Various | Rarely addressed | Rarely | Pre-2016 snapshot |
| State-dependent MILP (MDPI 2023–24) | Job-shop + machine states | Makespan + Energy | None | None (synthetic) | Western tariffs; no peak demand |
| Period-indexed MILP (SciTePress 2024) | ToU-aware MILP | Energy cost | None | None | Computational only |
| Multi-obj green scheduling (MDPI 2023) | Bi-objective FJSP | Makespan + Energy | None | None (NSGA-II) | No real data validation |
| AUGMECON ε-constraint (2022–24) | Multi-obj MILP | Cost + Emissions + Peak | None | Mixed | No uncertainty; no MSME |
| DRL + rolling horizon (MDPI 2024) | Dynamic scheduling | Makespan + Energy | Machine breakdown | Digital twin | Complex; no student feasibility |
| Robust FJSP (Atlantis Press 2024) | Robust MILP | Makespan robustness | Processing time | None | No energy awareness |
| Co-scheduling with DDU (arXiv 2024) | Energy + production | Cost | Decision-dependent | Simulation | Advanced; limited applicability |
| MPC-based scheduling (arXiv 2024) | Receding horizon | Energy cost | Price volatility | Simulation | Requires real-time solver |

### What is already solved

`[ESTABLISHED]` The following are standard, well-studied, and have extensive published solutions:

- Bi-objective makespan + energy MILP: **Solved since 2007.**
- Machine-state energy models (idle/processing/startup): **Standard since 2016.**
- ε-constraint and NSGA-II for Pareto front: **Textbook methodology.**
- ToU-aware scheduling: **Standard in OR literature.**
- Multi-objective green scheduling: **Hundreds of papers.**

### What is less studied

`[OBSERVED GAP]` These gaps are genuine but narrow:

1. **Peak demand as an explicit objective** (not just total energy): Most papers minimise total energy cost, ignoring demand charges. Indian tariffs include demand charges based on 15-minute peak kVA.
2. **Uncertainty-aware energy scheduling with physical validation**: Most robust/stochastic models are purely computational; very few validate with measured machine power.
3. **Tri-objective scheduling (makespan + energy cost + peak demand)**: The three-objective version is genuinely less explored than bi-objective.
4. **Rolling-horizon rescheduling with measured energy feedback**: Closed-loop scheduling where measured power feeds back into re-optimisation is rare in student-feasible implementations.

### Honesty check

`[ESTABLISHED]` None of these gaps constitute major algorithmic breakthroughs. They are **extensions and combinations** of existing techniques applied to a specific, practical context. This is honest and defensible for an undergraduate project, but must not be sold as "novel algorithm."

---

## 4. Mathematical Research Gap Analysis

| Research direction | Baseline | Proposed change | Why it matters | How to test | Difficulty |
|---|---|---|---|---|---|
| **A. Tri-objective: Makespan + Cost + Peak** | Bi-objective (makespan + energy cost) | Add peak demand as third objective; use AUGMECON for 3D Pareto | Indian industrial tariffs charge for peak kVA separately. Ignoring peak can make "optimal" schedules expensive in practice. | Generate Pareto surfaces; compare 2-obj vs 3-obj on total bill (energy + demand charge). | Medium |
| **B. Processing time uncertainty** | Deterministic MILP | Scenario-based robust MILP: solve over K scenarios of processing time drawn from measured distributions | Real processing times vary ±10–30%. Deterministic schedule may violate deadlines. | Compare expected cost + deadline violations under Monte Carlo perturbation. | Medium-High |
| **C. Rolling-horizon rescheduling** | Single-shot optimize-then-execute | Measure → optimise → execute → detect deviation → re-optimise | Single-shot schedules break when disruptions occur. Rolling-horizon adapts. | Compare schedule stability and realised cost between single-shot and rolling-horizon under simulated disruptions. | High |
| **D. Peak-demand-aware scheduling** | Minimise total energy cost only | Add peak power constraint or objective: min max_t Σ_m P_m(t) | Demand charges can be 30%+ of Indian industrial bills. Shaving peak saves money even if total kWh stays the same. | Measure difference in peak demand and demand charge between cost-only and peak-aware schedules. | Medium |
| **E. Measured vs constant energy models** | Constant P_proc per machine | Measure real power profiles (variable power during processing); use measured profiles in MILP | Constant-power assumption may misestimate energy by 15–40%. If the model is wrong, the schedule is wrong. | Compare schedules from constant vs measured models; validate with PZEM-004T. | Low-Medium |
| **F. Scalability analysis** | Small instances (5×3) | Systematic scaling: 5×3 → 10×5 → 20×8 → 50×10 | Must know where MILP becomes intractable and heuristic is needed. | Plot solver time, gap, and solution quality vs instance size. | Low |

### Strongest defensible research direction

**Direction D+A combined: Tri-objective scheduling with peak demand awareness.**

Justification:

1. `[ESTABLISHED]` Indian industrial tariffs (as of April 2024) include mandatory ToD pricing AND demand charges based on 15-minute peak kVA. This is a documented structural feature, not an assumption.
2. `[OBSERVED GAP]` Most energy-aware scheduling papers minimise total energy cost (kWh × price), ignoring demand charges. This means the "optimal" schedule can actually increase the total electricity bill if it creates power spikes.
3. `[INFERENCE]` Adding peak demand as a third objective changes the Pareto front structure in a non-trivial way — there are genuine trade-offs between spreading work (to reduce peak) and concentrating work in cheap periods (to reduce energy cost).
4. `[HYPOTHESIS]` A peak-demand-aware schedule will reduce the total electricity bill (energy charge + demand charge) compared to a cost-only schedule, even if total kWh is slightly higher.

This is **not** a new algorithm. It is an **extended formulation** with a mathematically defensible reason (demand charge structure) and a testable hypothesis (total-bill reduction). This is honest.

### Directions to deprioritise

- **B (Uncertainty):** Genuine research, but adds significant complexity. Risk of intractability. Reserve for Level 3/4.
- **C (Rolling-horizon):** Genuine research question, but requires real-time implementation. Too complex for minimum viable.
- **E (Measured profiles):** Important for engineering depth but not mathematically novel. Use as hardware integration layer.
- **F (Scalability):** Standard experiment, not research contribution. Include as supporting experiment.

---

## 5. Mathematical Formulation

### Sets

- $\mathcal{J} = \{1, \ldots, n\}$: set of jobs
- $\mathcal{O}_i$: set of operations for job $i$
- $\mathcal{M}$: set of machines
- $\mathcal{T} = \{1, \ldots, T\}$: set of discrete time slots (e.g., 15-minute intervals)
- $\mathcal{M}_o \subseteq \mathcal{M}$: set of machines eligible for operation $o$

### Parameters

- $p_o$: processing time of operation $o$ (time slots)
- $P^{proc}_m$: processing power of machine $m$ (kW) — **measured via PZEM-004T**
- $P^{idle}_m$: idle power of machine $m$ (kW) — **measured**
- $E^{start}_m$: startup energy of machine $m$ (kWh) — **measured**
- $\text{tariff}(t)$: energy price in time slot $t$ (₹/kWh) — **from state SERC tariff order**
- $D^{charge}$: demand charge rate (₹/kVA/month) — **from state SERC tariff order**
- $\Delta t$: time slot duration (hours)
- $d_i$: deadline for job $i$ (optional)
- $\text{prec}(o', o)$: 1 if operation $o'$ must precede $o$

### Decision variables

- $x_{omt} \in \{0, 1\}$: operation $o$ starts on machine $m$ at time $t$
- $y_{mt} \in \{0, 1\}$: machine $m$ is processing during time slot $t$
- $w_{mt} \in \{0, 1\}$: machine $m$ is idle (on but not processing) during time slot $t$
- $z_{mt} \in \{0, 1\}$: machine $m$ has a startup event at time slot $t$
- $C_{max} \in \mathbb{R}^+$: makespan
- $P^{peak} \in \mathbb{R}^+$: peak total power across all time slots

### Why each variable exists

| Variable | Purpose | Without it |
|---|---|---|
| $x_{omt}$ | Assigns each operation to a machine and start time | Cannot construct a schedule |
| $y_{mt}$ | Tracks whether machine is actively processing | Cannot compute processing energy |
| $w_{mt}$ | Distinguishes idle from off | Cannot model idle energy (real machines draw power when on but not processing) |
| $z_{mt}$ | Detects startup transitions | Cannot model startup energy cost |
| $C_{max}$ | Makespan objective | Cannot optimise production time |
| $P^{peak}$ | Peak power variable | Cannot optimise demand charge |

### Objective functions

**Objective 1 — Makespan:**
$$\min C_{max} = \max_{i \in \mathcal{J}} \left( \max_{o \in \mathcal{O}_i} \sum_{m,t} x_{omt} \cdot (t + p_o) \right) \cdot \Delta t$$

**Objective 2 — Energy cost:**
$$\min \text{EnergyCost} = \sum_{t \in \mathcal{T}} \sum_{m \in \mathcal{M}} \left[ P^{proc}_m \cdot y_{mt} + P^{idle}_m \cdot w_{mt} + \frac{E^{start}_m}{\Delta t} \cdot z_{mt} \right] \cdot \text{tariff}(t) \cdot \Delta t$$

**Objective 3 — Peak demand (our proposed extension):**
$$\min P^{peak}$$

where $P^{peak}$ is constrained by:
$$P^{peak} \geq \sum_{m \in \mathcal{M}} \left[ P^{proc}_m \cdot y_{mt} + P^{idle}_m \cdot w_{mt} + \frac{E^{start}_m}{\Delta t} \cdot z_{mt} \right] \quad \forall t \in \mathcal{T}$$

**Total electricity bill (for comparison, not optimisation):**
$$\text{TotalBill} = \text{EnergyCost} + D^{charge} \cdot P^{peak}$$

### Constraints

**C1 — Assignment:** Each operation assigned to exactly one machine and start time:
$$\sum_{m \in \mathcal{M}_o} \sum_{t \in \mathcal{T}} x_{omt} = 1 \quad \forall o$$

**C2 — Precedence:** If $\text{prec}(o', o) = 1$:
$$\sum_{m,t} x_{o'mt} \cdot (t + p_{o'}) \leq \sum_{m,t} x_{omt} \cdot t$$

**C3 — No overlap:** At most one operation on each machine at any time:
$$\sum_{o : m \in \mathcal{M}_o} \sum_{\tau = t - p_o + 1}^{t} x_{om\tau} \leq 1 \quad \forall m, t$$

**C4 — Machine state logic:**
$$y_{mt} + w_{mt} \leq 1 \quad \forall m, t$$

$y_{mt} = 1$ if and only if some operation is being processed on machine $m$ at time $t$:
$$y_{mt} = \sum_{o : m \in \mathcal{M}_o} \sum_{\tau = \max(1, t - p_o + 1)}^{t} x_{om\tau} \quad \forall m, t$$

**C5 — Startup detection:**
$$z_{mt} \geq (y_{mt} + w_{mt}) - (y_{m,t-1} + w_{m,t-1}) \quad \forall m, t > 1$$

**C6 — Makespan:**
$$C_{max} \geq \sum_{m,t} x_{omt} \cdot (t + p_o) \cdot \Delta t \quad \forall o \text{ that is the last operation of some job}$$

**C7 — Deadline (optional):**
$$\sum_{m,t} x_{omt} \cdot (t + p_o) \cdot \Delta t \leq d_i \quad \forall i, o = \text{last}(i)$$

**C8 — Peak demand:**
$$P^{peak} \geq \sum_{m \in \mathcal{M}} \left[ P^{proc}_m \cdot y_{mt} + P^{idle}_m \cdot w_{mt} + \frac{E^{start}_m}{\Delta t} \cdot z_{mt} \right] \quad \forall t$$

### Multi-objective solution method

**AUGMECON (Augmented ε-constraint):**

1. Optimise each objective individually to find anchor points.
2. Choose one primary objective (e.g., EnergyCost).
3. Treat others as constraints with systematically varied ε values.
4. Generate Pareto-efficient solution set.

For the 3-objective case, this produces a **Pareto surface** (not just a front), which is visualisable as a 3D scatter plot.

### Assumptions (stated honestly)

| Assumption | Realistic? | Consequence if violated |
|---|---|---|
| Processing times are deterministic | **No** — real times vary ±10–30% | Schedule may violate deadlines; addressed by uncertainty experiments |
| Machine power is constant during processing | **Roughly yes** for most MSME machines (motors, CNC at steady state) | If violated, measured profiles provide correction |
| No machine breakdowns | **Unrealistic** for long horizons | Rolling-horizon would address; excluded from minimum viable |
| Jobs are known in advance | **Roughly yes** for batch MSME production | Dynamic arrival excluded from minimum viable |
| Linear ToU tariff | **Yes** — Indian tariffs are piecewise-constant per time block | Directly matches real tariff structure |
| Demand charge based on peak kW | **Yes** — standard Indian industrial tariff structure | Directly matches real billing |

### What mathematical contribution is actually ours

`[PROPOSED]` **The extension from bi-objective to tri-objective (adding peak demand), motivated by the specific structure of Indian industrial tariffs where demand charges are a documented significant cost component.**

This is:
- NOT a new algorithm ← `[ESTABLISHED]` AUGMECON, MILP, and NSGA-II are all standard
- NOT a new model structure ← `[ESTABLISHED]` machine-state MILP exists
- An **extended formulation** with a **specific practical motivation** (demand charges) and **testable consequences** (different Pareto structure, different total bill)
- Honest for an undergraduate project

### Computational complexity

`[ESTABLISHED]` Job-shop scheduling is NP-hard. The tri-objective extension does not change the complexity class but increases the number of MILP solves required (grid over 2 ε dimensions → O(k²) solves for k grid points per dimension). For small instances (≤10 jobs × 5 machines), exact solution via Gurobi is feasible. For larger instances, NSGA-III (3-objective extension of NSGA-II) is the standard metaheuristic.

### Solvability within student resources

- **Gurobi Academic License:** Free. Handles 10×5 instances in seconds to minutes.
- **PuLP with CBC:** Free, open-source. Slower but adequate for small instances.
- **NSGA-III via pymoo:** Free Python library. Handles larger instances.
- **Estimated computation:** 3-objective AUGMECON with 10×10 ε-grid = 100 MILP solves. At ~10 seconds each = ~17 minutes total. Feasible on a laptop.

---

## 6. Mathematical Experiments

### Experiment 1 — Model comparison (ablation)

**Question:** Does adding peak demand as an objective change the optimal schedule?

| Condition | Objectives | Method |
|---|---|---|
| A (baseline heuristic) | None (FCFS) | Dispatch rule |
| B (baseline heuristic) | None (SPT) | Dispatch rule |
| C (single-obj) | min Makespan | MILP |
| D (bi-objective) | min {Makespan, EnergyCost} | AUGMECON |
| E (tri-objective) | min {Makespan, EnergyCost, PeakDemand} | AUGMECON |

**Measures:** Makespan, energy cost (₹), peak demand (kW), total bill (₹), solver time (s), optimality gap (%).

**Instances:** 20 random instances per size category: 5×3, 8×4, 10×5.

**Statistical test:** Wilcoxon signed-rank test on total bill, D vs E.

**Falsifiability:** If E does not reduce total bill compared to D on ≥60% of instances, the peak-demand extension provides no benefit. This would be a valid negative result.

### Experiment 2 — Sensitivity to tariff structure

**Question:** Under what tariff conditions does peak-demand-aware scheduling matter?

**Design:** Vary demand charge rate from ₹0 to ₹500/kVA/month in 10 steps. For each, run bi-objective (D) and tri-objective (E). Plot total bill difference vs demand charge rate.

**Expected outcome:** `[HYPOTHESIS]` Benefit of peak-demand awareness increases with demand charge rate. There exists a threshold below which it provides negligible benefit. Finding this threshold is a research contribution.

### Experiment 3 — Sensitivity to tariff differential

**Question:** Does the peak/off-peak price ratio affect whether energy-aware scheduling is worthwhile?

**Design:** Vary peak/off-peak ratio from 1.0 (flat tariff) to 2.0 (steep differential). Fix demand charge at Karnataka BESCOM rate. Compare FCFS vs tri-objective on total bill.

**Expected outcome:** `[HYPOTHESIS]` Benefit increases with price differential. At ratio ≈ 1.0, benefit approaches zero.

### Experiment 4 — Scalability

**Question:** At what problem size does exact MILP become intractable?

**Design:** Increase from 5×3 to 50×10. Measure solver time, optimality gap (1% threshold), and memory. Compare MILP (Gurobi) vs NSGA-III (pymoo).

**Measures:** Wall-clock time, optimality gap, hypervolume indicator, number of Pareto-efficient solutions found.

### Experiment 5 — Energy model realism (ablation)

**Question:** Does using measured power profiles instead of constant power change the optimal schedule?

**Design:** 
- F1: Constant P_proc (literature default)
- F2: Measured P_proc + P_idle (from PZEM-004T)
- F3: F2 + measured startup energy

Run tri-objective MILP on same instances with each energy model. Compare resulting schedules and costs.

**Falsifiability:** If F1, F2, F3 produce identical schedules on >80% of instances, the energy model refinement is unnecessary.

### Experiment 6 — Uncertainty (stretch goal)

**Question:** Does a deterministic schedule remain good when processing times are perturbed?

**Design:** Generate 100 perturbation scenarios (processing times drawn from N(p_o, 0.15·p_o)). Evaluate the deterministic schedule under each scenario. Measure deadline violations, realised cost, and peak demand.

**Falsifiability:** If the deterministic schedule violates deadlines in <5% of scenarios, robustness extensions are unnecessary for this problem scale.

---

## 7. Physical Engineering Layer

### Minimum testbed

| Component | Technical purpose | Required? |
|---|---|---|
| PZEM-004T energy meter | Measures real V, I, P, E of physical loads — provides measured P_proc, P_idle, E_start | **Yes** — transforms project from simulation to measurement |
| ESP32 microcontroller | Reads PZEM-004T via UART; transmits data to optimizer; controls relays | **Yes** — provides edge computing and I/O |
| 4-channel relay module | Switches physical loads on/off per schedule — demonstrates schedule execution | **Yes** — closes the loop from optimizer to physical world |
| 3 small loads (motor, heater, lamp) | Represent 3 "machines" with different power profiles | **Yes** — minimum for scheduling (need >1 machine) |
| Dashboard (laptop/tablet) | Displays schedule, real-time power, cost accumulation | **Yes** — evaluator needs to see the system working |

### What each component demonstrates

1. **PZEM-004T → ESP32:** Real power measurement feeds the energy model. This is NOT simulated data.
2. **ESP32 → Relay → Loads:** Schedule execution. The optimizer's output physically turns machines on/off at the right times.
3. **Loads → PZEM-004T:** Closed loop. Measured power validates that the executed schedule matches the prediction.
4. **Dashboard:** Visualises the Gantt chart, power timeline, cost accumulation, and comparison between baseline and optimised schedules in real time.

### BOM

| Component | Qty | Unit Cost (₹) | Total (₹) |
|---|---|---|---|
| ESP32-WROOM-32 | 1 | 500 | 500 |
| PZEM-004T (with CT) | 1 | 500 | 500 |
| 4-channel relay module (5V) | 1 | 200 | 200 |
| Small DC motor (775) | 1 | 250 | 250 |
| Heating element (small) | 1 | 100 | 100 |
| LED lamp/load | 1 | 50 | 50 |
| Breadboard + wires | 1 | 200 | 200 |
| **Total** | | | **₹1,800** |

---

## 8. Real Data vs Simulation

### REAL (measured from physical testbed)

- Machine power profiles: P_proc, P_idle for each load — **via PZEM-004T**
- Startup energy: E_start for each load — **via PZEM-004T**
- Schedule execution: actual ON/OFF times — **via relay + timestamp logging**
- Realised energy consumption — **via PZEM-004T integration over time**
- Realised peak demand — **via PZEM-004T max(P(t))**

**Why legitimate:** These are direct physical measurements of the system under control. They validate the energy model.

### MODELLED (from real-world sources, not measured in testbed)

- Processing times — **modelled as MSME-representative values**
- Job precedence constraints — **from MSME production structure (or synthetic)**
- ToU tariff — **from state SERC tariff order (Karnataka BESCOM / Maharashtra MSEDCL)**
- Demand charge rate — **from state SERC tariff order**
- Machine capabilities — **modelled**

**Why legitimate:** Tariff data is publicly available, officially published, and directly applicable. Processing times in OR are always parameterised. This is standard practice in every scheduling paper.

### SIMULATED (for scalability and sensitivity)

- Large-scale instances (20+ jobs × 8+ machines) — beyond physical testbed
- Monte Carlo perturbation scenarios — for uncertainty analysis
- Tariff structure variations — for sensitivity analysis

**Why legitimate:** Scaling experiments cannot be done physically (we don't have 50 machines). Simulation is the standard methodology in OR. The key is that the energy model used in simulation is **validated against physical measurements** from the testbed.

---

## 9. Closed-Loop Architecture

```
Physical loads (motor, heater, lamp)
      ↓
Power sensing (PZEM-004T)
      ↓
Energy model (P_proc, P_idle, E_start)
      ↓
Production model (jobs, operations, precedence)
      ↓
Tri-objective MILP optimizer (laptop)
      ↓
Schedule (Gantt chart)
      ↓
Controller (ESP32 → relays)
      ↓
Physical execution (loads turn ON/OFF)
      ↓
Measurement (PZEM-004T)
      ↓
Validation (predicted vs actual energy/peak)
```

### Architecture options

| Level | Architecture | What it shows | Prototype effort |
|---|---|---|---|
| 1 | Optimization only | MILP + Pareto analysis on synthetic data | Low |
| 2 | Optimization + monitoring | MILP + PZEM-004T measures real power | Medium |
| **3** | **Optimization + monitoring + control** | **MILP → ESP32 → relay → loads + measurement** | **Medium-High** |
| 4 | Closed-loop adaptive scheduling | Level 3 + deviation detection + re-optimisation | High |

**Selected: Level 3.** This provides:
- Real measurement (engineering depth)
- Physical execution (prototype demonstration)
- Predicted vs actual comparison (experimental validation)
- No rescheduling (avoids complexity risk)

Level 4 is stretch goal only.

---

## 10. Prototype Demonstration (5-minute evaluator demo)

### Setup

Three physical loads (motor, heater, lamp) connected via relay module to ESP32. PZEM-004T monitors total power. Laptop runs optimizer + dashboard.

### Demo script

1. **[30s] Problem setup:** Show 3 "machines" (loads), 5 "jobs" with processing times and precedence. Show Indian ToU tariff structure on screen.

2. **[60s] Baseline execution:** Run FCFS schedule. ESP32 turns loads on/off per FCFS order. Dashboard shows real-time power trace, accumulating cost, peak demand.

3. **[30s] Optimization:** Run tri-objective MILP on laptop. Show solver log. Show Pareto surface (3D scatter: makespan × cost × peak). Let evaluator pick a Pareto-efficient solution.

4. **[60s] Optimised execution:** ESP32 executes the selected schedule. Dashboard shows real-time power trace, cost, peak — overlaid with baseline for comparison.

5. **[30s] Comparison table:**

```
                Baseline (FCFS)    Optimised (Tri-obj)    Improvement
Energy Cost     ₹ ______          ₹ ______               ____%
Peak Demand     ______ kW         ______ kW               ____%
Total Bill      ₹ ______          ₹ ______               ____%
Makespan        ______ min        ______ min              ____%
Solver Time     N/A               ______ sec              N/A
```

6. **[30s] Ablation summary:** Show bar chart: FCFS vs SPT vs Makespan-only vs Bi-objective vs Tri-objective on total bill. Show that peak-demand awareness provides additional bill reduction.

7. **[30s] Pareto surface:** Interactive 3D plot. Evaluator can rotate and explore trade-offs.

**This demonstration shows decision-making and engineering behavior:** The optimizer makes a non-trivial choice (which machines to idle, when to start, how to spread load) and the physical system executes it, with measured results validating the prediction.

---

## 11. Research Questions

### Candidates

1. *Does incorporating peak demand as a third scheduling objective reduce total industrial electricity bills under Indian tariff structures, compared to energy-cost-only optimisation?*

2. *Under what demand-charge conditions does peak-demand-aware scheduling provide statistically significant bill reduction, and below what threshold is it unnecessary?*

3. *Does using measured machine power profiles (idle + processing + startup) change optimal schedules compared to constant-power assumptions, and by how much?*

4. *How does the quality of tri-objective Pareto approximation (NSGA-III) compare to exact AUGMECON solutions as problem size increases?*

5. *Does a deterministic energy-aware schedule maintain feasibility under stochastic processing time perturbations, or does uncertainty-aware scheduling provide measurably better outcomes?*

### Selection

**Primary RQ: Question 1+2 combined:**

> *Does incorporating peak demand as a third objective in energy-aware manufacturing scheduling reduce total electricity bills under Indian ToU + demand-charge tariff structures, and under what tariff conditions does this benefit become statistically significant?*

**Justification:**

| Criterion | Score | Rationale |
|---|---|---|
| Mathematical depth | **Strong** | Tri-objective MILP + AUGMECON + Pareto surface analysis. Genuine multi-objective optimization. |
| Novelty | **Moderate** | Peak-demand as explicit 3rd objective in manufacturing scheduling is less explored. Not algorithmic novelty, but formulation extension with practical justification. |
| Falsifiability | **Strong** | Clear null hypothesis: peak-demand awareness provides no statistically significant bill reduction. Testable with Wilcoxon on paired instances. |
| Engineering relevance | **Strong** | Demand charges are 30%+ of real Indian industrial bills. Directly useful. |
| Prototype feasibility | **Strong** | Tri-objective MILP is solvable; physical demo is the same as bi-objective. |
| Rubric fit | **Strong** | Mathematical formulation + physical prototype + quantitative comparison + clear results. |

---

## 12. Minimum Viable Research Project

### Mathematical contribution
`[PROPOSED]` Tri-objective MILP formulation (makespan + energy cost + peak demand) with AUGMECON solution, motivated by Indian demand-charge tariff structure. Systematic sensitivity analysis on demand-charge rate.

### Engineering contribution
Physical testbed: 3 loads + PZEM-004T + ESP32 + relay control. Measured power profiles feeding into optimizer. Schedule execution with measured validation.

### Experimental contribution
- 5 scheduling conditions: FCFS, SPT, makespan-only MILP, bi-objective MILP, tri-objective MILP.
- 20+ random instances per size category (5×3, 8×4, 10×5).
- Statistical comparison (Wilcoxon).
- Pareto surface visualisation and hypervolume comparison.
- Sensitivity analysis on demand-charge rate and tariff differential.
- Measured vs predicted energy validation.

### Prototype
Physical loads controlled by ESP32, powered by MILP optimizer, monitored by PZEM-004T, visualised on dashboard. 5-minute live demonstration.

### Evidence
- Total bill comparison (energy + demand charge) across conditions.
- Statistical significance of tri-objective benefit.
- Demand-charge threshold where benefit becomes significant.
- Predicted vs measured energy error.

---

## 13. Escalation Path

### Level 1 — Minimum viable (MUST work)
- Bi-objective MILP (makespan + energy cost) with AUGMECON
- Synthetic instances + Indian ToU tariff
- FCFS/SPT baseline comparison
- Software Gantt + cost dashboard
- Statistical comparison (20+ instances, Wilcoxon)

### Level 2 — Strong engineering (adds physical layer)
- Level 1 +
- PZEM-004T measured power profiles for 3 loads
- ESP32 + relay execution of schedule
- Predicted vs measured energy validation
- Live demonstration with physical loads

### Level 3 — Mathematical research (strongest contribution)
- Level 2 +
- **Tri-objective formulation: makespan + energy cost + peak demand**
- AUGMECON Pareto surface (3D)
- Sensitivity analysis on demand-charge rate
- Hypervolume comparison (2-obj vs 3-obj)
- Energy model ablation (constant vs measured)

### Level 4 — Stretch (only if L1–L3 are solid)
- Level 3 +
- Scenario-based uncertainty analysis (processing time perturbation)
- NSGA-III for larger instances (20+ jobs)
- Scalability analysis with Gurobi time limits
- Rolling-horizon rescheduling prototype

> [!WARNING]
> **Level 4 must not endanger Levels 1–3.** If Level 3 is not working by week 8, do NOT attempt Level 4. Ship a polished Level 2/3.

---

## 14. Failure Analysis

| Failure | Consequence | Mitigation | Residual risk |
|---|---|---|---|
| **Optimizer produces negligible improvement over FCFS** | Core claim fails; project becomes "verified that scheduling doesn't help" | Select instances with tight deadlines + high tariff differential. If still marginal, report honestly as negative result. | Low — OR literature consistently shows MILP beats dispatch heuristics when tariff differential > 1.2× |
| **Peak-demand extension gives negligible benefit** | Tri-objective contribution adds nothing beyond bi-objective | Report the demand-charge threshold. Negative result is valid: "peak awareness only matters when demand charges exceed ₹X/kVA." | Medium — depends on tariff structure. Mitigated by sensitivity analysis. |
| **PZEM-004T readings are noisy/unreliable** | Measured profiles unreliable; energy model validation fails | Use averaging over multiple readings. Calibrate against known load. Worst case: use manufacturer-spec power values + acknowledge limitation. | Low — PZEM-004T is well-characterised for ≥100W loads. |
| **Measured power differs significantly from constant model** | Schedules from constant model are suboptimal. But this is actually a positive result (shows measurement matters). | Report as finding: "constant-power assumption causes X% cost error." | Low — this failure mode is actually a research result. |
| **Schedule becomes infeasible with deadlines** | MILP returns infeasible | Relax deadlines; use tardiness penalty instead of hard constraint. | Low — standard OR technique. |
| **Solver too slow for 10×5 instances** | Cannot produce results in reasonable time | Use Gurobi with 60s time limit + report optimality gap. Fall back to NSGA-III for larger instances. | Low — Gurobi academic handles 10×5 in <60s typically. |
| **Physical testbed is unrepresentative** | Evaluator says "this isn't a real factory" | Acknowledge honestly. Testbed validates the energy model and control loop, not industrial scale. Simulation extends to realistic sizes. | Medium — inherent in any student project. Frame as "validated methodology, not deployed system." |
| **Relay control adds no value** | Evaluator says "you could have just simulated this" | The relay demonstrates that the schedule is physically executable and that predicted energy matches measured energy. This is the validation step. | Low — physical validation is the engineering contribution. |

---

## 15. Final Decision Gate

| Gate | Requirement | Status | Evidence |
|---|---|---|---|
| Real industrial problem | Evidence | ✅ PASS | Indian MSME energy costs documented by BEE, CEEW. ToD tariffs mandatory from April 2024 (MoP rules). Demand charges are 30%+ of industrial bills. |
| Mathematical research | Genuine contribution | ✅ PASS (conditional) | Tri-objective extension with peak demand. Not algorithmic novelty — formulation extension with practical motivation. Defensible for UG level. |
| Mathematical validation | Falsifiable experiments | ✅ PASS | 6 experiments designed. Clear null hypotheses. Statistical tests specified. |
| Engineering depth | Physical system | ✅ PASS | PZEM-004T + ESP32 + relay + 3 loads. Measures, executes, validates. |
| Prototype feasibility | Buildable | ✅ PASS | BOM ₹1,800. All components available on Amazon India. |
| Experimental validation | Baseline vs proposed | ✅ PASS | 5 conditions: FCFS, SPT, makespan MILP, bi-obj MILP, tri-obj MILP. |
| Research contribution | Defensible | ⚠️ CONDITIONAL | Defensible if framed as "extended formulation + validation" not "novel algorithm." Must cite prior art honestly. |
| SDG 9 connection | Concrete | ✅ PASS | SDG 9.4 (sustainable industrialisation). Direct: reduces MSME energy costs using optimised scheduling. |
| Rubric fit | Strong | ✅ PASS | Math + hardware + live demo + statistical results + Pareto visualisation. |
| Cost | Student feasible | ✅ PASS | ~₹1,800 hardware. Software free (PuLP/Gurobi academic/pymoo). |
| Time | Student feasible | ✅ PASS | 10–12 weeks. Core MILP: 3 weeks. Hardware: 2 weeks. Experiments: 3 weeks. Report: 2 weeks. |

---

## FINAL OUTPUT

### 1. Verdict

The project, **as originally proposed**, is a software optimisation demo with Indian parameters — insufficient for mathematical depth and prototype quality. **With the modifications below, it becomes a defensible research project.**

### 2. What is currently weak

- **No mathematical contribution** beyond parameterising an existing model
- **No physical prototype** — software-only Gantt chart
- **No sensitivity/robustness analysis** — single-point results
- **Novelty claim is contextual only** — "Indian tariffs" is not a research gap

### 3. Strongest mathematical research direction

**Tri-objective scheduling: Makespan + Energy Cost + Peak Demand**, motivated by the documented structure of Indian industrial tariffs (mandatory ToD since April 2024 + demand charges on peak kVA).

This is **not** a new algorithm. It is an extended formulation with:
- A specific, documented economic motivation (demand charges)
- A testable hypothesis (total-bill reduction)
- A non-trivial Pareto structure (3D surface)
- Ablation: show that the 3rd objective produces different schedules than 2-objective

### 4. Proposed mathematical formulation

See [§5 above](#5-mathematical-formulation). Tri-objective MILP with AUGMECON. Sets, parameters, variables, objectives, and constraints fully specified.

### 5. Research hypothesis

> Under Indian industrial tariff structures with demand charges, a tri-objective energy-aware manufacturing schedule (minimising makespan, energy cost, AND peak demand simultaneously) produces a lower total electricity bill than a bi-objective schedule (minimising makespan and energy cost only), and this benefit increases with the demand-charge rate.

**Null hypothesis:** Peak-demand-aware scheduling does not significantly reduce total electricity bills compared to energy-cost-only scheduling.

**Test:** Wilcoxon signed-rank on paired instances, α = 0.05.

### 6. Experiments needed

1. **Model comparison** (5 conditions × 20+ instances × 3 sizes): FCFS, SPT, makespan MILP, bi-obj, tri-obj.
2. **Sensitivity to demand-charge rate** (10 levels × 20 instances): Find threshold.
3. **Sensitivity to tariff differential** (10 levels × 20 instances): Find threshold.
4. **Scalability** (5×3 to 50×10): Solver time + NSGA-III comparison.
5. **Energy model ablation** (constant vs measured power): 3 model variants.
6. **Uncertainty** (stretch): Monte Carlo perturbation of processing times.

### 7. Physical prototype architecture

```
Laptop (optimizer + dashboard)
    ↕ WiFi/Serial
ESP32 (controller)
    ↓ UART → PZEM-004T (power measurement)
    ↓ GPIO → 4-channel relay (load control)
    ↓ loads: motor + heater + lamp
```

### 8. Minimum viable prototype

- Bi-objective MILP (makespan + energy cost)
- Synthetic instances + real Indian ToU tariff
- FCFS/SPT baselines
- Statistical comparison
- Software Gantt + cost dashboard

### 9. Strong version

- Tri-objective MILP with peak demand
- PZEM-004T measured power profiles
- ESP32 + relay physical execution
- Predicted vs measured validation
- 3D Pareto surface
- Sensitivity analysis
- Live 5-minute demonstration

### 10. Key risks

1. **Peak-demand extension gives negligible benefit** → Mitigated by sensitivity analysis; finding the threshold is itself a result.
2. **Evaluator sees it as "existing technique + Indian data"** → Must demonstrate physical testbed, live execution, and the specific demand-charge insight.
3. **Solver too slow** → Gurobi academic + time limits + NSGA-III fallback.
4. **PZEM-004T measurement noise** → Averaging + calibration. Low risk.

### 11. GO / MODIFY / REJECT

## **MODIFY then GO**

The core idea (energy-aware scheduling for MSMEs) is strong.

Modifications required:
1. ✅ Add peak demand as 3rd objective (mathematical research layer)
2. ✅ Add PZEM-004T + ESP32 + relay physical testbed (engineering depth)
3. ✅ Add sensitivity analysis on demand-charge rate (experimental depth)
4. ✅ Reframe novelty as "extended formulation with practical validation" (honesty)
5. ✅ Design 5-minute live demo with physical loads (prototype quality)

### 12. Exact next steps

| Priority | Action | Timeline | Effort |
|---|---|---|---|
| 1 | **Order hardware:** ESP32, PZEM-004T, relay module, 3 loads | Day 1 | ₹1,800 |
| 2 | **Implement bi-objective MILP** in PuLP with CBC solver. Test on 5×3 instance. Verify correctness. | Week 1 | 3 days |
| 3 | **Extend to tri-objective** by adding P^peak variable and constraint C8. Verify with AUGMECON. | Week 1–2 | 2 days |
| 4 | **Obtain Indian tariff data:** Download Karnataka BESCOM / Maharashtra MSEDCL tariff order. Extract ToD rates + demand charge. | Week 1 | 1 day |
| 5 | **Build instance generator:** Random job-shop instances with configurable size, processing times, machine eligibility. | Week 2 | 1 day |
| 6 | **Run Experiment 1** (model comparison) on synthetic instances. Verify that tri-objective produces different schedules. | Week 2–3 | 3 days |
| 7 | **Build hardware testbed:** Wire ESP32 + PZEM-004T + relay + loads. Test power measurement. Measure P_proc, P_idle, E_start for each load. | Week 3–4 | 4 days |
| 8 | **Integrate hardware with optimizer:** ESP32 receives schedule from laptop, executes via relays, reports measured power back. | Week 4–5 | 3 days |
| 9 | **Run Experiment 5** (energy model ablation): Compare constant vs measured power models. | Week 5 | 2 days |
| 10 | **Run Experiment 2+3** (sensitivity analysis): Vary demand charge and tariff differential. | Week 5–6 | 3 days |
| 11 | **Run Experiment 4** (scalability): Scale to 20×5, 50×10 with NSGA-III. | Week 6–7 | 2 days |
| 12 | **Build dashboard:** Real-time Gantt + power trace + cost accumulation + Pareto surface. | Week 7–8 | 4 days |
| 13 | **Full demo rehearsal:** Run baseline + optimised schedule live. Record results. | Week 8 | 1 day |
| 14 | **Phase I report:** Problem definition, literature review, methodology, flow chart. | Week 1–3 (parallel) | Ongoing |
| 15 | **Phase III report + poster/PPT:** Results, analysis, discussion. | Week 9–11 | Ongoing |
| 16 | **(Stretch) Experiment 6:** Uncertainty analysis. Only if Levels 1–3 are solid. | Week 9–10 | 3 days |

---

## APPENDIX E — `sdg9_project_analysis.md`

# SDG 9 Engineering Project — Rubric Analysis & Research-Backed Idea Generation

> **Institution:** RV College of Engineering, Bengaluru  
> **Course:** Experiential Learning (EL) — III Semester, 2025 Batch  
> **Grand Total:** 200 Marks (Phase I: 40 | Phase II: 60 | Phase III: 100)  
> **+20 Bonus Marks** for notable outcomes (publications, patents, product development)

---

## Part 1: Rubric Analysis

### 1.1 Evaluation Criteria

| Criterion | Phase | Weight | What It Actually Evaluates | What a High-Scoring Project Needs |
|---|---|---:|---|---|
| **Clarity** | I — Problem Definition | /20 (sub) | How clearly & concisely the problem is stated | A problem that can be stated in 1–2 sentences with no ambiguity |
| **Relevance** | I — Problem Definition | /20 (sub) | Significance of the problem to SDG 9 | Direct, undeniable link to industry/infrastructure — not a stretch |
| **Context** | I — Problem Definition | /20 (sub) | Background research and literature context | Thorough survey of prior work, statistics, existing systems |
| **Flow Chart** | I — Problem Definition | /20 (sub) | Methodology clarity via visual representation | Accurate, complete, precise step-by-step process diagram |
| **Specificity** | I — Objectives | /10 | Measurability of stated objectives | SMART objectives with concrete metrics (e.g., "reduce X by Y%") |
| **Alignment** | I — Objectives | /10 | Objective-problem coherence | Objectives must directly address the stated problem |
| **Achievability** | I — Objectives | /10 | Feasibility within academic scope | Realistic yet challenging — not trivially easy, not impossible |
| **Appropriateness** | I — Methodology | /10 | Right method for the problem | Justified selection of tools/algorithms/approaches |
| **Detail** | I — Methodology | /10 | Depth of methodological documentation | Detailed steps, parameter choices, experimental design |
| **Adherence** | II — Project Execution | /30 | Following the proposed methodology | Actually executing what was planned, not pivoting without reason |
| **Timeliness** | II — Project Execution | /30 | On-schedule delivery | Staying within the semester timeline |
| **Quality** | II — Project Execution | /30 | Build quality of deliverables | High-quality code, hardware, documentation |
| **Selection** | II — Tools & Techniques | /20 | Appropriateness & sophistication of tools | Cutting-edge, highly appropriate tools — not default/obvious ones |
| **Application** | II — Tools & Techniques | /20 | How well tools are used | Expert-level usage, not superficial |
| **Integration** | II — Tools & Techniques | /20 | Seamless combination of tools | Tools work together cohesively, not bolted on |
| **Clarity** | II — Partial Results | /10 | Documentation of intermediate results | Clear, well-documented partial outputs |
| **Progress** | II — Partial Results | /10 | Visible forward momentum | Significant measurable progress by midpoint |
| **Analysis** | II — Partial Results | /10 | Interpretation of early data | Thoughtful analysis, not just raw outputs |
| **Functionality** | III — Prototype Demo | /30 | Does it actually work? | **Perfectly functioning** prototype — the single highest-weight criterion |
| **Innovation** | III — Prototype Demo | /30 | Novelty and creativity | **Highly innovative** — not a replication of existing work |
| **Usability** | III — Prototype Demo | /30 | User experience quality | Intuitive, user-friendly, polished |
| **Clarity** | III — Results & Discussion | /20 | Clear presentation of results | Well-explained, easy to follow |
| **Analysis** | III — Results & Discussion | /20 | Depth of result interpretation | Thorough, insightful, statistically sound |
| **Interpretation** | III — Results & Discussion | /20 | Logical, well-supported conclusions | Claims supported by data, not opinion |
| **Organization** | III — Report | /20 | Structure and flow of final report | Well-organized, logical narrative |
| **Clarity** | III — Report | /20 | Writing quality | Concise, error-free, professional |
| **Completeness** | III — Report | /20 | Coverage of all required sections | All sections present and thorough |
| **Visual Appeal** | III — Poster/PPT | /10 | Design quality of presentation | Professional, highly appealing visual design |
| **Clarity** | III — Poster/PPT | /10 | Information clarity in visuals | Easy to understand at a glance |
| **Content** | III — Poster/PPT | /10 | Completeness of key components | All key results, methods, conclusions included |
| **Notable Outcomes** | Bonus | +20 | Publications, patents, product impact | Journal publications, conference proceedings, filed patents |

### 1.2 Weight Distribution Analysis

```
Phase I  — Problem Definition + Objectives + Methodology:  40 marks (20%)
Phase II — Execution + Tools + Partial Results:             60 marks (30%)
Phase III — Prototype + Results + Report + Poster:         100 marks (50%)
Bonus — Publications/Patents/Products:                     +20 marks
```

**Critical observation:** Phase III alone is **50% of the total grade**. Within Phase III:
- **Prototype Demonstration: 30 marks** — highest single component
- **Results & Discussion: 20 marks** — requires quantitative depth
- **Report: 20 marks** — completeness and quality
- **Poster/PPT: 10 marks** — visual polish

### 1.3 Hidden Priorities

These are **my interpretations** of what the rubric implicitly rewards, distinguished from explicit requirements:

| Priority | Explicit or Implicit | Evidence |
|---|---|---|
| **Working prototype above all else** | Explicit | 30/200 marks (15%) — largest single block |
| **Innovation/novelty** | Explicit | Separate "Innovation" criterion in Phase III (within 30-mark block) |
| **Quantitative results** | Implicit | "Thorough analysis," "logical, well supported" in Results require numbers |
| **Tool sophistication** | Explicit | "Cutting-edge, highly appropriate" in Tools & Techniques (20 marks) |
| **Research context** | Explicit | "Thorough background/context" in Problem Definition |
| **Methodological rigor** | Explicit | "Detailed, well documented" methodology |
| **Publication potential** | Explicit | +20 bonus marks for papers/patents |
| **Usability/polish** | Explicit | "Highly user-friendly" in Prototype Demo |
| **Measurable objectives** | Explicit | "Clear, specific, measurable" in Objectives |
| **Execution discipline** | Implicit | Phase II rewards adherence, timeliness, quality |
| **Visual communication** | Explicit | 10 marks for poster/PPT design quality |
| **Seamless tool integration** | Explicit | "Seamlessly integrated" in Tools criterion |

### 1.4 Project Requirements

#### Must-Have Requirements
1. **Clearly defined, specific problem** with direct SDG 9 relevance
2. **Thorough literature/context** establishing the problem's significance
3. **SMART objectives** with measurable metrics
4. **Detailed, appropriate methodology** documented step-by-step
5. **Fully functional prototype** — this is non-negotiable
6. **Quantitative results** with proper analysis and interpretation
7. **Complete, well-organized report** covering all sections
8. **Professional poster/PPT** with visual appeal

#### Strongly Beneficial Features
1. **Genuine innovation** — novel approach, not just applying existing tools
2. **Cutting-edge, well-integrated tools** — sophisticated tech stack
3. **Mathematical/engineering formulation** supporting the approach
4. **Measurable improvement over a baseline** — quantitative evidence
5. **Publication-quality work** — targeting the +20 bonus
6. **Polished, user-friendly interface** for the prototype

#### Optional Features
1. Patent-worthy invention
2. Industry collaboration or real-world deployment
3. Multi-disciplinary integration (cross-department collaboration)

#### Things Unlikely to Add Meaningful Marks
1. Excessive theoretical complexity without prototype results
2. Name-dropping technologies (AI, blockchain, IoT) without justified use
3. Overly ambitious scope that leads to incomplete execution
4. Beautiful presentation with no working demo

### 1.5 Common Failure Modes

| Failure Mode | Why It Loses Marks | Affected Criteria |
|---|---|---|
| **Non-functional prototype** | Devastating — kills 30+ marks in Phase III | Functionality, Innovation, Usability |
| **Vague problem statement** | Cascading failure — objectives and methodology become unfocused | Clarity, Relevance, Specificity |
| **No baseline comparison** | Cannot demonstrate improvement | Analysis, Interpretation, Innovation |
| **AI/ML without justification** | Fails "Appropriateness" and "Selection" | Methodology, Tools & Techniques |
| **Generic IoT monitoring** | Zero innovation score | Innovation |
| **Poor execution discipline** | Phase II collapse | Adherence, Timeliness, Quality |
| **Superficial results** | No depth = poor analysis marks | Analysis, Interpretation |
| **Incomplete report** | Direct marks lost | Completeness |
| **Over-scope** | Nothing works well | Functionality, Quality, Timeliness |

### 1.6 Ideal Project Profile

> An ideal high-scoring project is one that:
> 1. Solves a **clearly defined, real problem** with obvious SDG 9 relevance
> 2. Is grounded in **existing research** with a **specific, defensible gap** identified
> 3. Has a **mathematically sound formulation** that guides the engineering solution
> 4. Uses **appropriate, cutting-edge tools** that are **well-integrated**
> 5. Produces a **fully functional, polished prototype** that demonstrates the solution
> 6. Shows **quantitative improvement** over a measurable baseline
> 7. Is **realistically scoped** for an academic semester
> 8. Generates results suitable for **publication** (bonus marks)
> 9. Is communicated through a **professional report and presentation**

### 1.7 Project Selection Checklist

Every idea must pass **all** of the following:

- [ ] **Problem Clarity:** Can I state the problem in 2 sentences?
- [ ] **SDG 9 Relevance:** Is the link to industry/innovation/infrastructure direct and obvious?
- [ ] **Research Foundation:** Is there established literature on this problem?
- [ ] **Identifiable Gap:** Is there a specific, defensible gap in existing solutions?
- [ ] **Mathematical Depth:** Can the problem be formulated mathematically?
- [ ] **Innovation:** Is our contribution genuinely novel (not just "existing system + AI")?
- [ ] **Prototype Feasibility:** Can we build a working demo within a semester?
- [ ] **Measurable Baseline:** Is there a clear before/after comparison possible?
- [ ] **Tool Justification:** Is every technology used technically necessary?
- [ ] **Resource Availability:** Can we access the data, hardware, and software needed?
- [ ] **Scalability:** Does the solution have potential beyond the prototype?
- [ ] **Publication Potential:** Could the work be submitted to a conference or journal?

---

## Part 2: Problem-Space Exploration & Idea Generation (15 Ideas)

> **Note:** Each idea below has been explored against recent literature. Ideas that failed the research gap test during exploration were discarded before inclusion.

---

### Idea 1: Optimal Sensor Placement for Water Distribution Network Leak Detection Using Graph-Theoretic Methods

**Problem:** Indian urban water distribution networks (WDNs) lose 30–50% of treated water as non-revenue water (NRW), primarily through undetected leaks. Municipal bodies have limited budgets for sensor deployment.

**Existing Solutions:** EPANET-based hydraulic simulation; commercial SCADA-based monitoring (expensive); basic IoT flow/pressure sensors (ad-hoc placement).

**Existing Research:**
- GNN-based leak localization (2024) shows promise but requires dense sensor networks
- Greedy and information-theoretic sensor placement methods exist but are tested on benchmark networks, not Indian topologies
- Most work focuses on abrupt burst detection, not incipient background leaks

**Research Gap:** No integrated framework that combines graph-theoretic optimal sensor placement with background leak sensitivity analysis on Indian-scale irregular network topologies. Existing placement methods optimize for burst detection only.

**Our Proposed Solution:** A two-stage framework: (1) Model the WDN as a graph and formulate sensor placement as a set-cover / p-median problem to maximize background leak detection sensitivity; (2) Simulate leak scenarios using EPANET and validate placement optimality using pressure residual analysis.

**Innovation:** Shifting the optimization objective from burst detection to background leak sensitivity — a different objective function that no existing sensor placement paper has specifically targeted for Indian WDN topologies.

**Mathematical Formulation:**
- **Decision variables:** Binary variables x_j ∈ {0,1} for sensor at node j
- **Objective:** Maximize the expected detection probability over all potential leak locations: max Σ_i P(detect leak at node i | sensor configuration X)
- **Constraints:** Budget constraint: Σ x_j ≤ K (max K sensors); connectivity constraints from graph topology
- **Problem type:** Combinatorial optimization (NP-hard p-median variant)
- **Solution approach:** Greedy heuristic + NSGA-II for multi-objective (detection probability vs. localization accuracy vs. cost)

**Required Technology:** Python (NetworkX, WNTR/EPANET toolkit), OR-Tools or PuLP for optimization, simulation via EPANET

**Prototype:** Software tool that takes WDN topology as input, runs leak simulations, and outputs optimal sensor positions with coverage maps

**Evaluation Methodology:** Compare detection rates of our optimized placement vs. random placement and vs. existing greedy methods on benchmark networks (Net1, Net2, Net3) and a real Indian municipal network topology

**Expected Improvement:** 25–40% improvement in background leak detection coverage with same number of sensors vs. random placement

**SDG 9 Relevance:** Directly improves resilient water infrastructure (SDG 9.1) and upgrades infrastructure with resource efficiency (SDG 9.4)

**Key Sources:**
- Sarrate et al. (2014) — Sensor placement for leak detection in WDNs, survey
- Hu et al. (2023) — GNN-based leak localization
- Giustolisi et al. (2008) — Graph theory in WDN analysis
- EPANET documentation and benchmark networks

---

### Idea 2: Edge-TinyML Bearing Fault Diagnosis with Domain Adaptation for Variable-Speed MSME Motors

**Problem:** Indian MSMEs (70M+ units) rely on rotating machinery (motors, pumps, lathes) where unplanned downtime costs ≈₹1.5L/day. Most cannot afford commercial vibration monitoring systems (₹5L+/unit).

**Existing Solutions:** CWRU-dataset-trained CNNs (lab only); commercial systems (SKF, Brüel & Kjær — expensive); basic threshold-based vibration alerts.

**Existing Research:**
- TinyML on ESP32/STM32 for vibration classification (2024) — achieves >95% on CWRU
- Domain adaptation for bearing faults (transfer learning) — active area
- Lightweight CNNs (MobileNet, ShuffleNet) for edge deployment

**Research Gap:** Models trained on constant-speed benchmark datasets (CWRU) fail when deployed on real MSME machines with variable loads and speeds. No existing work provides a complete, validated pipeline from MEMS sensor → edge inference → interpretable output specifically adapted for variable-speed operation on sub-₹5000 hardware.

**Our Proposed Solution:** (1) Collect vibration data from MEMS accelerometer (ADXL345/MPU6050) on a lab motor at variable speeds; (2) Extract order-tracking features (speed-normalized) instead of raw FFT; (3) Train a compact 1D-CNN and deploy via TFLite on ESP32; (4) Implement domain adaptation using Maximum Mean Discrepancy (MMD) loss to generalize from CWRU → our lab data.

**Innovation:** Order-tracking-based feature extraction as a physics-informed preprocessing step that makes the ML model inherently speed-invariant, combined with MMD-based domain adaptation — addressing the core failure mode of existing TinyML bearing diagnostics.

**Mathematical Formulation:**
- **Feature extraction:** Order spectrum O(k) = DFT(x(θ)), where θ = ∫ω(t)dt is angular position (resampled from time-domain)
- **Domain adaptation loss:** L_total = L_classification + λ · MMD²(F_source, F_target)
- **MMD:** MMD²(P,Q) = E[k(x,x')] - 2E[k(x,y)] + E[k(y,y')] where k is RBF kernel
- **Model compression:** Post-training quantization (INT8) to fit ESP32 flash constraints
- **Objective:** Minimize classification error while maximizing domain invariance

**Required Technology:** MEMS accelerometer (ADXL345, ≈₹200), ESP32 (≈₹500), TensorFlow Lite Micro, Python (scipy, scikit-learn, tensorflow), lab motor with controllable speed

**Prototype:** Self-contained edge device that clips onto a motor, classifies bearing health (Normal / Inner Race / Outer Race / Ball fault) on-device, and displays status on OLED + sends alerts via WiFi

**Evaluation Methodology:**
- Accuracy, F1-score on CWRU (baseline) vs. lab-collected variable-speed data
- Compare: raw FFT features vs. order-tracking features vs. domain-adapted model
- Inference time and memory footprint on ESP32

**Expected Improvement:** Maintain >90% accuracy under variable speed (vs. <70% for non-adapted CWRU models) on hardware costing <₹2000

**SDG 9 Relevance:** Enables affordable predictive maintenance for MSMEs (SDG 9.3 — increase access of small-scale industrial enterprises to technology)

**Key Sources:**
- Smith & Randall (2015) — Rolling element bearing diagnostics using order tracking
- Long et al. (2015) — Learning transferable features with deep adaptation networks (MMD)
- Banerjee et al. (2024) — TinyML for predictive maintenance on MCUs
- CWRU Bearing Data Center

---

### Idea 3: Multi-Objective Energy-Aware Production Scheduling for Indian MSMEs Under Time-of-Use Tariffs

**Problem:** Indian MSME manufacturers (steel, textile, ceramic) face industrial electricity tariffs of ₹8–12/kWh with time-of-use (ToU) variation. Most schedule production manually without considering energy costs, leading to 15–25% avoidable energy expenditure.

**Existing Solutions:** Commercial MES/ERP systems (SAP, Siemens — too expensive for MSMEs); manual scheduling based on order priority only; basic load-shedding during peak hours.

**Existing Research:**
- MILP-based energy-aware job-shop scheduling (Gahm et al., 2016 — seminal survey)
- Multi-objective makespan + energy minimization (Zhang et al., 2023)
- Robust optimization under uncertainty for energy scheduling

**Research Gap:** Existing MILP models assume continuous processes and Western tariff structures. No model specifically addresses the combination of (a) Indian ToU tariff structures with demand charges, (b) batch/intermittent production typical of Indian MSMEs, and (c) the inclusion of machine idle-power and startup-energy costs that dominate in small-batch production.

**Our Proposed Solution:** Formulate a bi-objective MILP for job-shop scheduling that minimizes both makespan and total energy cost under Indian ToU tariffs, incorporating realistic machine states (idle, startup, processing, shutdown) with empirically measured energy profiles.

**Innovation:** Incorporating machine-state-dependent energy consumption (not just processing energy) into the scheduling model, specifically calibrated for Indian tariff structures and MSME batch sizes. This addresses a gap where most models assume steady-state processing.

**Mathematical Formulation:**
- **Decision variables:** s_ij (start time of operation j of job i), y_mk (binary: machine m is ON during time slot k)
- **Objective 1:** min C_max = max(completion times) [makespan]
- **Objective 2:** min Σ_k Σ_m [P_proc(m) · proc_time(m,k) + P_idle(m) · idle_time(m,k) + E_startup(m) · startup(m,k)] × tariff(k)
- **Constraints:** Precedence constraints (operation ordering), machine capacity (no overlap), time-window constraints
- **Solution:** ε-constraint method to generate Pareto front; NSGA-II for larger instances
- **Parameters:** Empirically measured P_proc, P_idle, E_startup from a local MSME

**Required Technology:** Python (PuLP/Gurobi academic license, pymoo for NSGA-II), IoT power meter (PZEM-004T, ≈₹500) to measure machine energy profiles, state electricity board ToU tariff data

**Prototype:** Software tool: input job list + machine specs + tariff → output Gantt chart with energy cost overlay + Pareto-optimal schedules showing makespan-energy tradeoffs

**Evaluation Methodology:**
- Compare our schedule vs. FCFS and SPT baselines on energy cost and makespan
- Test on synthetic instances (5, 10, 20 jobs × 3–5 machines) and one real MSME case study
- Statistical comparison using Wilcoxon signed-rank test

**Expected Improvement:** 12–20% reduction in energy costs with <5% increase in makespan vs. energy-unaware scheduling

**SDG 9 Relevance:** Directly supports SDG 9.4 — upgrade infrastructure and retrofit industries for resource efficiency

**Key Sources:**
- Gahm et al. (2016) — "Energy-efficient scheduling in manufacturing companies" (survey)
- Zhang et al. (2023) — Multi-objective green scheduling with variable speed machines
- Mouzon et al. (2007) — Operational methods for minimization of energy consumption in manufacturing
- Indian state electricity regulatory commission ToU tariff orders

---

### Idea 4: Optimal Cleaning Scheduling for Solar Panel Arrays Using Soiling Loss Prediction

**Problem:** Dust soiling reduces solar panel output by 15–40% in Indian conditions. Fixed-interval cleaning wastes water and labor; under-cleaning causes revenue loss. No cost-optimal, data-driven cleaning scheduler exists for rooftop and small-farm installations.

**Existing Solutions:** Fixed-interval cleaning (weekly/monthly); autonomous cleaning robots (expensive, >₹50K); manual visual inspection.

**Existing Research:**
- Soiling rate models using environmental factors (Sarver et al., 2013 — comprehensive review)
- ML-based soiling prediction (Micheli et al., 2023)
- Economic analysis of cleaning frequency (cleaning cost vs. energy recovery)

**Research Gap:** Existing soiling models predict loss but do not solve the scheduling optimization problem — "when should I clean to maximize net revenue?" Most cleaning optimization papers assume uniform soiling, ignoring panel-level variation and local microclimate effects.

**Our Proposed Solution:** (1) Build a soiling rate prediction model using environmental sensors (dust, humidity, wind, temperature); (2) Formulate cleaning scheduling as a stochastic dynamic programming problem that triggers cleaning when the expected marginal energy recovery exceeds cleaning cost.

**Innovation:** Framing cleaning as an optimal stopping problem (Bellman equation) rather than threshold-based triggering, incorporating stochastic soiling rate and weather forecasts.

**Mathematical Formulation:**
- **State:** s_t = (current soiling level, weather forecast, days since last clean)
- **Action:** a_t ∈ {clean, wait}
- **Reward:** R(clean) = energy_recovered − cleaning_cost; R(wait) = −energy_lost_today
- **Bellman equation:** V(s_t) = max{R(clean) + γV(s_0), R(wait) + γE[V(s_{t+1})]}
- **Soiling model:** ΔPower/day = f(PM2.5, humidity, wind_speed, tilt_angle) — fitted via regression
- **Problem type:** Markov Decision Process (MDP) / optimal stopping

**Required Technology:** PM2.5 sensor (SDS011, ≈₹1500), DHT22 (temp/humidity, ≈₹200), anemometer (≈₹800), current sensor (ACS712) on solar panel, ESP32, Python (gym, stable-baselines3)

**Prototype:** IoT device that monitors soiling proxies + panel output, runs MDP solver, and sends "CLEAN NOW" / "WAIT" recommendations with expected savings

**Evaluation Methodology:** Compare: (a) fixed weekly cleaning, (b) threshold-based cleaning, (c) our MDP-optimal cleaning over a 30–60 day observation period. Metric: net revenue (energy produced − cleaning cost).

**Expected Improvement:** 10–15% improvement in net revenue vs. fixed-interval cleaning

**SDG 9 Relevance:** SDG 9.4 — sustainable infrastructure with efficient resource use; supports India's renewable energy infrastructure

**Key Sources:**
- Sarver et al. (2013) — "A comprehensive review of the impact of dust on the use of solar energy"
- Micheli et al. (2023) — ML-based soiling prediction models
- Bertsekas (2017) — Dynamic Programming and Optimal Control (MDP theory)

---

### Idea 5: Edge-First Cold Chain Monitoring with Commodity-Specific Spoilage Prediction for First-Mile Agricultural Transport

**Problem:** India loses 20–40% of perishable produce (₹92,000 crore/year) in the first-mile journey from farm to cold storage. Current monitoring is cloud-dependent and uses generic temperature thresholds, ignoring commodity-specific spoilage kinetics.

**Existing Solutions:** Cloud-based IoT loggers (Emerson, Carrier — expensive, require connectivity); simple max-min thermometers; manual inspection.

**Existing Research:**
- IoT cold chain monitoring (numerous papers) — mostly cloud-centric
- Commodity-specific quality kinetics (Arrhenius-based models for different produce)
- Edge/TinyML for agriculture (emerging, 2024)

**Research Gap:** No integrated system combines (a) offline-capable edge inference, (b) commodity-specific thermal-kinetic spoilage models (not just generic thresholds), and (c) remaining shelf-life prediction for Indian first-mile conditions (unreliable connectivity, ambient temperatures 35–45°C, short transport in non-refrigerated vehicles).

**Our Proposed Solution:** Deploy a low-cost sensor node (temperature, humidity, ethylene proxy) that runs a commodity-specific Arrhenius-based shelf-life model on-device (ESP32) to provide real-time remaining shelf-life estimates, independent of cloud connectivity.

**Innovation:** On-device, physics-informed spoilage prediction (not a black-box ML model) that uses the Arrhenius equation calibrated for specific Indian produce (mango, tomato, leafy greens) — providing interpretable, actionable "hours remaining" estimates.

**Mathematical Formulation:**
- **Arrhenius model:** k(T) = A · exp(−Ea / RT), where k = spoilage rate, T = temperature (K), Ea = activation energy (commodity-specific)
- **Quality integral:** Q(t) = ∫₀ᵗ k(T(τ)) dτ; spoilage when Q(t) ≥ Q_threshold
- **Remaining shelf life:** RSL(t) = (Q_threshold − Q(t)) / k(T_current)
- **Calibration:** Fit A, Ea per commodity using published literature + controlled experiments
- **Alert logic:** Trigger alert when RSL < transport_time_remaining

**Required Technology:** DS18B20 (temperature, ≈₹100), DHT22 (humidity), MQ-3 or gas sensor (ethylene proxy, ≈₹300), ESP32, OLED display, SD card for offline logging, Python for calibration

**Prototype:** Portable sensor unit (palm-sized) that attaches to crate/vehicle. Displays commodity name, current temperature, estimated RSL, and alert status. Works fully offline. Data syncs when WiFi available.

**Evaluation Methodology:** Controlled experiment: place sensor + produce samples at varying temperatures, compare predicted RSL vs. actual observed spoilage onset (visual + firmness). Metrics: Mean Absolute Error of RSL prediction, false alarm rate.

**Expected Improvement:** RSL prediction within ±2 hours (vs. no prediction in current systems); 15–20% reduction in spoilage through timely alerts

**SDG 9 Relevance:** SDG 9.1 — develop quality, reliable, sustainable infrastructure supporting economic development; agricultural cold chain is critical infrastructure

**Key Sources:**
- Giannakourou & Taoukis (2003) — Kinetic modelling of Vitamin C loss in frozen green vegetables
- Taoukis & Labuza (1989) — Applicability of time-temperature indicators as shelf life monitors
- Jedermann et al. (2014) — Intelligent perishable goods logistics (review)

---

### Idea 6: Graph-Optimized Vehicle Routing for MSME Last-Mile Distribution in Indian Cities

**Problem:** Indian MSMEs spend 13–15% of product cost on logistics, with last-mile delivery being the most inefficient segment. Manual route planning leads to 25–35% excess travel distance.

**Existing Solutions:** Google Maps (no multi-stop optimization), commercial fleet management (FarEye, Locus — expensive), manual dispatch.

**Existing Research:**
- Capacitated VRP with time windows (CVRPTW) — extensively studied
- Metaheuristics for VRP (genetic algorithms, ant colony optimization)
- Indian urban VRP with heterogeneous fleet (limited work)

**Research Gap:** Most VRP research assumes homogeneous fleets and Western road networks. Indian MSMEs use heterogeneous vehicles (auto-rickshaws, mini-trucks, two-wheelers) with different capacities, speed profiles, and access restrictions in narrow Indian urban lanes.

**Our Proposed Solution:** Formulate a heterogeneous fleet CVRPTW with Indian-specific constraints (vehicle access restrictions by road width, traffic-dependent travel times, multiple depot capability) and solve using a hybrid genetic algorithm with local search.

**Innovation:** Vehicle-road compatibility constraints (matching vehicle type to road accessibility) — a real-world constraint largely absent from VRP literature.

**Mathematical Formulation:**
- **Decision variables:** x_ijk = 1 if vehicle k travels from node i to node j
- **Objective:** min Σ_i Σ_j Σ_k c_ij · x_ijk (total travel cost/distance)
- **Constraints:** Each customer visited exactly once; vehicle capacity Q_k; time windows [a_i, b_i]; vehicle-road compatibility: x_ijk = 0 if vehicle k cannot access road(i,j)
- **Solution:** Hybrid GA with Clarke-Wright savings initialization + 2-opt local search

**Required Technology:** Python (OR-Tools, DEAP for GA), OpenStreetMap data for road network, Overpass API for road width data

**Prototype:** Web application: input customer locations + vehicle fleet → output optimized routes on a map with estimated savings

**Evaluation Methodology:** Compare against manual routes (if available from a local MSME) and Google Maps sequential navigation. Metrics: total distance, total time, fuel cost.

**Expected Improvement:** 15–25% reduction in total travel distance vs. manual planning

**SDG 9 Relevance:** SDG 9.1 — develop quality, reliable infrastructure supporting economic development; efficient logistics is critical infrastructure

**Key Sources:**
- Toth & Vigo (2014) — "Vehicle Routing: Problems, Methods, and Applications" (reference text)
- Golden et al. (1984) — Heterogeneous fleet VRP
- Koç et al. (2016) — Heterogeneous VRP review

---

### Idea 7: Low-Cost Structural Health Monitoring of Bridges Using MEMS Accelerometers and Modal Analysis

**Problem:** India has 150,000+ bridges, with many structurally deficient. MoRTH mandated real-time SHM in 2024, but commercial systems cost ₹50L+. Low-cost alternatives lack validated accuracy.

**Existing Solutions:** Commercial SHM systems (NI, HBM — very expensive); visual inspection (subjective, infrequent); research-grade MEMS prototypes (not validated against commercial systems).

**Existing Research:**
- MEMS-based SHM with modal analysis (Albarbar et al., 2009)
- Damage detection via natural frequency shifts (Doebling et al., 1996 — foundational)
- ML-based anomaly detection from vibration data (2024)

**Research Gap:** Validation gap — few studies rigorously compare low-cost MEMS accelerometer accuracy against commercial reference sensors for structural modal parameters (natural frequencies, mode shapes, damping ratios) on real or scaled bridge structures.

**Our Proposed Solution:** Build a multi-node MEMS sensor array, deploy on a scaled bridge model, extract modal parameters using Operational Modal Analysis (OMA), and rigorously compare accuracy against a reference commercial accelerometer (borrow from lab).

**Innovation:** Systematic quantification of the accuracy-cost tradeoff — answering: "How much modal parameter accuracy do you lose with ₹200 MEMS vs. ₹2L commercial sensor?" This validation study fills a critical adoption barrier.

**Mathematical Formulation:**
- **OMA:** Frequency Domain Decomposition (FDD) — SVD of PSD matrix: G(f) = U(f) · S(f) · U^H(f)
- **Natural frequency identification:** Peaks in first singular value spectrum
- **Damage index:** Δf_n = (f_n_healthy − f_n_damaged) / f_n_healthy — relative frequency shift
- **Statistical validation:** Concordance correlation coefficient (CCC) between MEMS and reference measurements
- **MAC (Modal Assurance Criterion):** MAC = |φ_MEMS^T · φ_ref|² / (|φ_MEMS|² · |φ_ref|²)

**Required Technology:** ADXL345 MEMS accelerometer (×4–6, ≈₹200 each), commercial accelerometer (borrow from lab), Arduino/ESP32, Python (scipy.signal for FFT/PSD, modal analysis), scaled bridge structure (can build from aluminum beams)

**Prototype:** Multi-node wireless sensor array + software for OMA + damage detection on scaled bridge with induced damage (added mass or bolt loosening)

**Evaluation Methodology:** Compare MEMS-derived modal parameters vs. reference accelerometer on same structure. Introduce known damage, verify detection capability. Metrics: frequency accuracy (Hz), MAC values, damage detection sensitivity.

**Expected Improvement:** Demonstrate <5% frequency estimation error at <1% of commercial sensor cost

**SDG 9 Relevance:** SDG 9.1 — resilient infrastructure; directly addresses India's bridge safety mandate

**Key Sources:**
- Doebling et al. (1996) — Damage identification and health monitoring from changes in vibration characteristics (foundational review)
- Brincker et al. (2001) — Modal identification from ambient vibration (FDD method)
- MoRTH 2024 mandate on bridge sensor instrumentation

---

### Idea 8: Adaptive Traffic Signal Control Using Multi-Agent Reinforcement Learning for Heterogeneous Indian Traffic

**Problem:** Indian urban intersections suffer extreme congestion due to heterogeneous traffic (auto-rickshaws, two-wheelers, buses, pedestrians, cattle) with no lane discipline. Fixed-cycle signals waste 20–40% of green time.

**Existing Solutions:** Fixed-time signals (majority of Indian cities); SCATS/SCOOT (deployed in Bengaluru/Delhi but expensive); single-intersection RL (simulation only).

**Existing Research:**
- DQN/PPO for single intersection (well-studied in SUMO)
- Multi-agent RL for corridor coordination (Wei et al., 2019)
- Indian traffic simulation challenges (heterogeneous vehicles, lane-free driving)

**Research Gap:** The "sim-to-real" gap for Indian conditions — existing MARL models are trained on lane-based Western traffic models (SUMO default). No published work validates MARL on a calibrated Indian heterogeneous traffic simulation with realistic vehicle-type distributions.

**Our Proposed Solution:** (1) Calibrate SUMO with Indian traffic parameters (vehicle mix, lane-free behavior, speed distributions from local traffic surveys); (2) Implement MAPPO (Multi-Agent PPO) for a 4-intersection corridor; (3) Design a reward function that explicitly penalizes phase flickering (a known instability issue).

**Innovation:** Anti-flickering reward penalty + Indian-calibrated simulation — addressing two specific documented failure modes of existing RL traffic controllers.

**Mathematical Formulation:**
- **State:** s_i = (queue lengths, phase, elapsed green time, neighboring intersection phases)
- **Action:** a_i = next phase selection
- **Reward:** R_i = −(total_wait_time) − α·(phase_change_count) − β·(max_queue_length)
- **MAPPO objective:** max Σ_t γ^t R_t with centralized training, decentralized execution
- **Anti-flickering:** Penalty term −α·I(phase changed in last Δt seconds)

**Required Technology:** SUMO traffic simulator, Python (stable-baselines3, FLOW/SUMO-RL), local traffic survey data (camera counts)

**Prototype:** SUMO simulation environment with 4 Indian-calibrated intersections + trained MARL agents + dashboard showing performance metrics

**Evaluation Methodology:** Compare: (a) fixed-time Webster's optimal, (b) actuated control, (c) single-agent RL, (d) our MARL on the calibrated Indian network. Metrics: average delay, throughput, queue length, number of stops.

**Expected Improvement:** 20–30% reduction in average delay vs. fixed-time; <5% phase flickering rate

**SDG 9 Relevance:** SDG 9.1 — resilient transport infrastructure; SDG 9.4 — sustainable upgrading

**Key Sources:**
- Wei et al. (2019) — PressLight: traffic signal control with reinforcement learning
- Zheng et al. (2019) — Learning phase competition for traffic signal control
- Yu et al. (2022) — MAPPO (multi-agent PPO)

---

### Idea 9: Power Quality Disturbance Classification Using Wavelet-Based Features and Lightweight ML on Edge Hardware

**Problem:** Microgrids and distributed energy resources in India face power quality disturbances (sags, swells, harmonics, flicker) that damage industrial equipment. Current PQ monitoring requires expensive analyzers (₹5L+).

**Existing Solutions:** Commercial PQ analyzers (Fluke, Hioki — expensive); MATLAB/Simulink-based offline analysis; basic RMS voltage monitoring.

**Existing Research:**
- Wavelet transform (DWT) + SVM for PQ classification (extensively studied)
- Deep learning (CNN, Transformer) for PQ (high accuracy but computationally heavy)
- Edge deployment of PQ classifiers (emerging area)

**Research Gap:** Trade-off between classification accuracy and edge deployability is poorly characterized. No systematic comparison of feature extraction methods (DWT vs. S-transform vs. HHT) × classifier architectures (SVM vs. RF vs. lightweight CNN) under varying noise levels, specifically targeting ESP32/STM32 deployment constraints.

**Our Proposed Solution:** Systematic benchmarking study: extract features using 3 methods, train 4 classifiers, evaluate under 4 noise levels, and deploy the Pareto-optimal (accuracy vs. memory vs. inference time) model on ESP32.

**Innovation:** The contribution is the systematic Pareto-optimal model selection framework for edge PQ classification, not just another classifier — providing a decision tool for practitioners.

**Mathematical Formulation:**
- **DWT:** x(t) = Σ c_{j,k} · ψ_{j,k}(t) (multiresolution decomposition)
- **Features:** Energy per subband: E_j = Σ_k |c_{j,k}|²; entropy: H_j = −Σ p·log(p)
- **Classification:** Multi-class (sag, swell, harmonics, flicker, interruption, notch, spike)
- **Pareto optimization:** min{1 − accuracy, memory_footprint, inference_time}
- **Noise robustness:** Test at SNR = {40dB, 30dB, 20dB, 10dB}

**Required Technology:** MATLAB/Simulink (for PQ signal generation), Python (pywt, scikit-learn, TFLite), ESP32, voltage sensor (ZMPT101B, ≈₹200), current sensor (ACS712)

**Prototype:** ESP32-based device that samples voltage waveform, classifies PQ events in real-time, logs events, and alerts via WiFi

**Evaluation Methodology:** Classification accuracy, F1-score across disturbance types, inference time on ESP32, memory usage; comparison against published benchmarks.

**Expected Improvement:** Achieve >95% accuracy at 30dB SNR on ESP32 with <100ms inference time — demonstrating feasibility of low-cost PQ monitoring

**SDG 9 Relevance:** SDG 9.1 — reliable energy infrastructure; SDG 9.4 — upgrading technology for sustainability

**Key Sources:**
- Mahela et al. (2015) — Power quality assessment using wavelet transform (review)
- IEEE 1159 — Power quality monitoring standard
- Biswal & Dash (2013) — Measurement of PQ disturbances using DWT

---

### Idea 10: Optimal Biomass Collection Network Design for Crop Residue Pelletization in North India

**Problem:** Despite policy mandates requiring thermal power plants to co-fire 5–7% biomass pellets, the organized collection capacity (2.5 MT/year) is far below demand (15–20 MT/year). The core bottleneck is the biomass supply chain from farm to pelletization unit — low bulk density makes transport uneconomical beyond 25 km.

**Existing Solutions:** Informal collection by local agents; government subsidies for pelletization units; manual baling machines.

**Existing Research:**
- Biomass supply chain optimization (Lin et al., 2014; You & Wang, 2011)
- Facility location problems for bioenergy (multi-stage models)
- Indian crop residue management policy analysis

**Research Gap:** No published optimization model specifically addresses the Indian context of (a) extreme seasonality (harvest window of 20–30 days), (b) smallholder fragmented land parcels (avg. <2 hectares), and (c) road network quality variation for collection vehicle routing.

**Our Proposed Solution:** Formulate a two-stage stochastic facility location + vehicle routing model: Stage 1 — locate collection depots and pelletization units optimally; Stage 2 — route collection vehicles under uncertain residue availability.

**Innovation:** Integrating farm-level residue availability uncertainty (stochastic programming) with road-network-aware collection routing in a single optimization framework for Indian conditions.

**Mathematical Formulation:**
- **Stage 1:** min Σ f_j · y_j + E_ξ[Q(x, ξ)] where y_j = facility opening decisions, ξ = stochastic residue availability
- **Stage 2 (recourse):** min Σ c_ij · x_ij (transport cost) s.t. capacity, demand, availability constraints
- **Constraints:** Facility capacity, vehicle capacity, seasonal time window, road accessibility
- **Solution:** L-shaped decomposition (Benders) for stochastic program

**Required Technology:** Python (PuLP, Pyomo, or Gurobi academic), GIS data (district-level), ICAR crop residue generation data, OpenStreetMap road network

**Prototype:** GIS-based decision support tool: input district crop data → output optimal depot locations, pelletization unit sites, collection routes with cost estimates

**Evaluation Methodology:** Compare cost-efficiency (₹/tonne delivered) of optimized network vs. current ad-hoc collection for a pilot district in Punjab/Haryana

**Expected Improvement:** 20–30% reduction in biomass collection cost per tonne

**SDG 9 Relevance:** SDG 9.1 — sustainable infrastructure; SDG 9.4 — resource-efficient industrial processes; directly supports India's circular economy goals

**Key Sources:**
- You & Wang (2011) — Optimal design of sustainable cellulosic biofuel supply chains
- Lin et al. (2014) — Biomass supply chain network design
- ICAR crop residue generation estimates by district

---

### Idea 11: Optimal Order-Picking Route Optimization for MSME Warehouses Using Modified TSP Heuristics

**Problem:** Indian MSME warehouses (e-commerce fulfillment, auto parts, FMCG distribution) operate with manual picking, where pickers walk 60–70% of their shift. No affordable tool optimizes pick paths.

**Existing Solutions:** Commercial WMS (Manhattan Associates, Blue Yonder — enterprise only); S-shape routing (common heuristic); manual by memory.

**Research Gap:** Most warehouse routing research assumes rectangular aisle layouts. Indian MSME warehouses are typically irregular, constrained spaces with non-standard layouts.

**Our Proposed Solution:** Model the warehouse as a graph (nodes = pick locations, edges = walkable paths with distances), solve order-picking as a Steiner TSP variant, and compare heuristic performance on irregular layouts.

**Innovation:** Graph-based routing that works on any layout shape (not just rectangular aisles), validated against real MSME warehouse floor plans.

**Mathematical Formulation:** Steiner TSP on warehouse graph. Objective: min total travel distance to visit all pick locations and return to depot.

**Required Technology:** Python (NetworkX, OR-Tools), floor plan digitization, simulation

**Prototype:** Web tool: upload warehouse floor plan → digitize layout → input pick list → output optimal route visualization + estimated distance savings

**Evaluation:** Compare optimized route distance vs. S-shape and manual routing on 3 real MSME warehouse layouts. Target: 20–35% distance reduction.

**SDG 9 Relevance:** SDG 9.3 — small-scale enterprise technology access

---

### Idea 12: Predictive Road Maintenance Scheduling Using Pavement Condition Index Modeling and Optimization

**Problem:** Indian municipal bodies spend road maintenance budgets reactively (fix after failure), leading to 2–3× higher costs than proactive maintenance. No optimization tool prioritizes which road segments to maintain first.

**Existing Solutions:** Annual visual surveys (PCI estimation); GIS-based road inventories; reactive complaint-based repairs.

**Research Gap:** Transition from PCI measurement to PCI-driven maintenance optimization — specifically, formulating the budget-constrained road segment selection as a knapsack problem with deterioration dynamics.

**Our Proposed Solution:** (1) Model pavement deterioration over time using Markov chains or sigmoid decay functions calibrated to Indian data; (2) Formulate maintenance scheduling as a 0-1 knapsack / resource-constrained scheduling problem: maximize total network PCI improvement within annual budget.

**Innovation:** Combining time-series pavement deterioration modeling with budget-constrained combinatorial optimization for Indian municipal road networks.

**Mathematical Formulation:**
- **Deterioration model:** PCI(t+1) = f(PCI(t), traffic_load, climate) — Markov transition probabilities
- **Optimization:** max Σ ΔPCI_i · x_i s.t. Σ cost_i · x_i ≤ Budget, x_i ∈ {0,1}
- **Multi-period extension:** Dynamic programming over T years

**Required Technology:** Python (PuLP, scipy), open road condition data (PMG-SY, NHAI databases), Excel for data preparation

**Prototype:** Decision support tool: input road network PCI scores + budget → output prioritized maintenance schedule with projected PCI improvement

**Evaluation:** Compare total network PCI achieved by optimized schedule vs. worst-first and random strategies over 5-year simulation.

**SDG 9 Relevance:** SDG 9.1 — resilient, sustainable transport infrastructure

---

### Idea 13: Anomaly Detection in Industrial Motor Current Signatures for Non-Invasive Fault Diagnosis

**Problem:** Motor failures account for 70% of unplanned downtime in Indian manufacturing. Motor Current Signature Analysis (MCSA) can detect faults non-invasively from the power cable — no need to attach sensors to the motor itself.

**Existing Solutions:** Commercial MCSA analyzers (expensive); vibration-based monitoring (requires physical contact); thermal imaging (costly cameras).

**Research Gap:** While MCSA research is mature for large motors (>50 kW), there is limited validated work on small induction motors (0.5–5 kW) commonly used in Indian MSMEs, where the fault signatures are weaker and harder to distinguish from noise.

**Our Proposed Solution:** Build a low-cost current acquisition system (ACS712 + ESP32), collect current signatures from small motors with seeded faults, and develop an anomaly detection pipeline using spectral analysis (motor slip frequency estimation) + lightweight classifier.

**Innovation:** Validated MCSA pipeline specifically for small motors with quantified detection limits — answering: "How small a fault can MCSA detect in a 1 HP motor?"

**Mathematical Formulation:**
- **Fault signature:** f_fault = f_supply ± k · f_rotor_slip (for eccentricity, broken bars)
- **Feature extraction:** FFT → identify sideband amplitudes relative to fundamental
- **Detection metric:** Sideband amplitude ratio (dB) relative to healthy baseline
- **Classification:** One-class SVM for anomaly detection (trained on healthy data only)

**Required Technology:** ACS712 current sensor (≈₹150), ESP32, small induction motor (0.5–1 HP), Python (scipy, scikit-learn)

**Prototype:** Non-invasive clip-on device that monitors motor current and flags anomalies

**Evaluation:** ROC curve for fault detection at various severity levels on seeded-fault motor

**SDG 9 Relevance:** SDG 9.3 — small-scale industrial enterprise technology access

---

### Idea 14: Disaster-Resilient Communication Mesh Network Using LoRa for Infrastructure Monitoring

**Problem:** During natural disasters (floods, earthquakes), cellular infrastructure fails, cutting off monitoring of critical infrastructure (bridges, dams, buildings). India faces 12–15 significant natural disasters annually.

**Existing Solutions:** Satellite phones (expensive); amateur radio (manual); dedicated public safety networks (FirstNet — US only).

**Research Gap:** Self-healing mesh network protocols optimized for LoRa's duty cycle and bandwidth constraints, specifically for sensor data relay (not human voice/text), with emphasis on network lifetime maximization under node failures.

**Our Proposed Solution:** Implement a LoRa mesh network with adaptive routing that maintains connectivity for critical infrastructure sensor data even with up to 30% node failure.

**Innovation:** Energy-aware adaptive routing protocol for LoRa mesh that dynamically reroutes around failed nodes while maximizing network lifetime — a specific gap in LoRa mesh literature.

**Mathematical Formulation:**
- **Graph:** G = (V, E) where V = nodes, E = communication links with weight = energy cost
- **Routing objective:** min-max(energy consumed per node) subject to end-to-end connectivity
- **Network lifetime:** max min_v∈V {E_remaining(v) / E_consumption_rate(v)}
- **Routing algorithm:** Modified Dijkstra with energy-balanced cost metric

**Required Technology:** LoRa modules (SX1278, ≈₹400 each × 6–8), ESP32, Python (simulation via NS-3 or custom simulator)

**Prototype:** 6–8 node LoRa mesh with simulated node failures, demonstrating data relay continuity

**Evaluation:** Network throughput, latency, and connectivity maintenance under progressive node failure (10%, 20%, 30%)

**SDG 9 Relevance:** SDG 9.1 — resilient infrastructure; SDG 9.a — facilitating sustainable infrastructure development

---

### Idea 15: Intelligent Indoor Air Quality Control for Industrial Workshops Using MPC-Based Ventilation Optimization

**Problem:** Indian industrial workshops (welding, painting, textile) have poor indoor air quality (IAQ) — PM2.5 levels 5–20× above OSHA limits. Existing ventilation is either always-on (energy waste) or manually controlled (inadequate).

**Existing Solutions:** Fixed-speed exhaust fans; commercial HVAC systems (expensive for SMEs); manual window opening.

**Research Gap:** Model Predictive Control (MPC) for ventilation is well-studied for commercial buildings but not validated for small industrial workshops where pollutant sources are intermittent and spatially non-uniform (e.g., welding at one station, grinding at another).

**Our Proposed Solution:** Deploy a low-cost sensor grid (PM2.5 + CO2 + VOC at 3–4 points), build a simple zone-based pollutant dispersion model, and implement MPC to control exhaust fan speeds for minimum energy while maintaining IAQ below thresholds.

**Innovation:** Zone-based MPC for multi-point pollutant control in small workshops — a different application domain than the well-studied office/commercial building MPC.

**Mathematical Formulation:**
- **System model:** C_{k+1} = A · C_k + B · u_k + D · d_k (state-space: C = concentration vector, u = fan speeds, d = source disturbance)
- **MPC objective:** min Σ_{k=0}^{N} [Σ (fan_power_k) + λ · Σ max(0, C_k − C_limit)²]
- **Constraints:** C_k ≤ C_max (IAQ limits), 0 ≤ u_k ≤ u_max (fan speed limits)
- **Prediction horizon:** N = 10–30 minutes
- **System identification:** Fit A, B, D from step-response experiments with sensor data

**Required Technology:** PMS5003 PM2.5 sensors (×3–4, ≈₹1000 each), SGP30 VOC sensor (≈₹500), PWM-controlled exhaust fan, ESP32, Python (do-mpc or casadi for MPC)

**Prototype:** Sensor network + fan controller that automatically adjusts ventilation based on real-time IAQ, with energy consumption logging

**Evaluation:** Compare energy consumption and IAQ compliance: (a) always-on fans, (b) manual control, (c) threshold-based ON/OFF, (d) our MPC. Metrics: average PM2.5, energy consumed (kWh), time above limit (%).

**Expected Improvement:** 30–40% energy reduction vs. always-on, with 95%+ time within IAQ limits

**SDG 9 Relevance:** SDG 9.2 — promote inclusive and sustainable industrialization; SDG 9.4 — resource efficiency

---

## Part 3: Research-Backed Shortlisting — Top 5 Ideas

Based on the project selection checklist and evidence gathered, I score the 15 ideas on 11 factors (1–10 scale):

| Factor | Weight | Idea 2 (Bearing TinyML) | Idea 3 (Energy Scheduling) | Idea 4 (Solar Cleaning) | Idea 5 (Cold Chain) | Idea 15 (IAQ MPC) |
|---|---:|---:|---:|---:|---:|---:|
| Rubric alignment | 15% | 9 | 9 | 8 | 8 | 9 |
| Problem significance | 10% | 9 | 8 | 7 | 9 | 8 |
| Research gap strength | 15% | 8 | 8 | 7 | 8 | 8 |
| Genuine novelty | 10% | 8 | 7 | 8 | 7 | 8 |
| Mathematical depth | 10% | 7 | 9 | 9 | 6 | 9 |
| Feasibility | 15% | 9 | 9 | 7 | 8 | 7 |
| Prototype potential | 10% | 9 | 8 | 7 | 9 | 8 |
| Data/resource availability | 5% | 9 | 8 | 6 | 7 | 7 |
| Measurable improvement | 5% | 9 | 9 | 8 | 8 | 9 |
| SDG 9 relevance | 3% | 9 | 9 | 8 | 8 | 8 |
| Defensibility | 2% | 8 | 8 | 7 | 7 | 8 |
| **Weighted Score** | | **8.50** | **8.40** | **7.55** | **7.85** | **8.15** |

### Justification for Scores:

**Idea 2 (Bearing TinyML — rank #1):**
- Feasibility: 9 — CWRU dataset publicly available, ESP32 and MEMS are cheap, motor available in any lab
- Problem significance: 9 — 70M+ MSMEs affected, documented ₹1.5L/day downtime cost
- Research gap: 8 — Variable-speed domain adaptation is a documented, active research gap (arXiv 2024)
- Prototype: 9 — Self-contained hardware device with clear demo (attach to motor, see classification on screen)

**Idea 3 (Energy Scheduling — rank #2):**
- Mathematical depth: 9 — Genuine bi-objective MILP with Pareto analysis
- Feasibility: 9 — Purely software + one power meter for calibration
- Research gap: 8 — Indian ToU tariffs + MSME batch production is an underexplored intersection
- Prototype: 8 — Software tool, slightly less visually impressive but technically deep

**Idea 15 (IAQ MPC — rank #3):**
- Mathematical depth: 9 — Full state-space MPC formulation
- Rubric alignment: 9 — Has hardware (sensors + fan control) + software (MPC) + measurable results
- Novelty: 8 — MPC for workshops is genuinely underexplored vs. commercial buildings
- Feasibility: 7 — Requires physical setup (sensors, fans, a workshop space); slightly harder logistics

**Idea 5 (Cold Chain — rank #4):**
- Problem significance: 9 — ₹92,000 crore annual loss is massive
- Prototype: 9 — Compelling physical demo with produce samples
- Research gap: 8 — Edge-first + commodity-specific is a documented gap
- Mathematical depth: 6 — Arrhenius model is relatively straightforward (less optimization depth)

**Idea 4 (Solar Cleaning — rank #5):**
- Mathematical depth: 9 — MDP/optimal stopping is elegant
- Novelty: 8 — Framing as optimal stopping problem is genuinely new
- Feasibility: 7 — Requires 30–60 day outdoor deployment + weather dependency

---

## Part 4: Stress-Testing the Top 3

### Stress-Test: Idea 2 — Edge-TinyML Bearing Fault Diagnosis

**Does this actually fill a research gap?**
Yes, partially. Order-tracking for speed normalization is well-known in vibration analysis (Smith & Randall, 2015), but its combination with TinyML edge deployment and domain adaptation (MMD) for MSMEs is not a published, validated end-to-end pipeline. The gap is real but incremental — it's integration innovation, not algorithmic novelty.

**What papers already do something similar?**
- Banerjee et al. (2024) — TinyML bearing diagnostics but on fixed-speed, CWRU-only
- Long et al. (2015) — Domain adaptation (MMD) but on desktop, not edge
- No paper combines order-tracking + MMD + TinyML in one pipeline

**What exactly is our contribution?**
A validated end-to-end pipeline from variable-speed MEMS data → order-tracking preprocessing → domain-adapted lightweight CNN → ESP32 inference. The contribution is the *integration* and *validation*, not any single component.

**Is our mathematical formulation valid?**
Yes. Order tracking and MMD are well-established. The risk is in implementation quality — getting TFLite model to fit ESP32 memory constraints.

**Is it technically solvable within our resources?**
Yes. Hardware cost: <₹3000. CWRU dataset: free. Lab motor: available. ESP32 programming: well-documented. Timeline: 8–10 weeks.

**Where could our approach fail?**
1. MEMS noise floor may be too high for subtle fault signatures on small motors
2. ESP32 may not have enough memory for the CNN after quantization
3. Order tracking requires a tachometer signal — adding complexity

**What assumptions are we making?**
- ADXL345 has sufficient bandwidth (3200 Hz max — adequate for most bearing faults)
- INT8 quantization doesn't degrade accuracy below usability
- Lab motor faults are representative of real MSME conditions

**Baseline:** Raw FFT + CNN on CWRU dataset (standard benchmark)

**Data needed:** CWRU dataset (free) + lab-collected variable-speed data (we generate this)

**Experimental validation:** Accuracy comparison across 3 conditions: (a) CWRU constant speed, (b) lab variable speed without adaptation, (c) lab variable speed with adaptation

**What would an evaluator challenge?**
- "This is just combining known techniques" → Counter: the combination is novel and specifically validated for a real-world constraint (variable speed + edge)
- "CWRU is overused" → Counter: we specifically address CWRU's limitations by testing on variable-speed data

**What would make it scientifically weak?**
- If accuracy improvement from domain adaptation is marginal (<5%)
- If we only test on CWRU and don't collect our own data

> **Verdict: GO** — Strong feasibility, clear demo, defensible gap. Ensure we collect our own variable-speed data.

---

### Stress-Test: Idea 3 — Energy-Aware Production Scheduling

**Does this actually fill a research gap?**
Partially. Energy-aware scheduling is well-studied (Gahm et al., 2016 surveys 100+ papers). However, the specific intersection of Indian ToU tariffs + machine-state energy + MSME batch production is genuinely underexplored. The gap is narrow but real.

**What papers already do something similar?**
- Mouzon et al. (2007) — Energy minimization via machine idle/off control (foundational)
- Zhang et al. (2023) — Multi-objective green scheduling
- None specifically model Indian tariff structures or MSME batch patterns

**What exactly is our contribution?**
A validated MILP model parameterized with real Indian tariff data and empirically measured machine energy profiles from an actual MSME. The contribution is *context-specific validation*, not a new algorithm.

**Is our mathematical formulation valid?**
Yes. Standard job-shop scheduling MILP with added energy terms. Well-grounded in OR literature.

**Is it technically solvable within our resources?**
Yes. PuLP is free. Gurobi academic license is free. One power meter (₹500). Need access to a local MSME for data collection — this is the risk.

**Where could our approach fail?**
1. MSME access may be difficult → Mitigation: use synthetic but realistic instances
2. MILP may become intractable for large instances → Mitigation: use NSGA-II for larger problems
3. Energy savings may be small (<5%) if tariff variation is low → Mitigation: test with multiple state tariff structures

**Baseline:** First-Come-First-Served (FCFS) and Shortest-Processing-Time (SPT) scheduling without energy consideration

**What would an evaluator challenge?**
- "This is standard MILP with different parameters" → Counter: context-specific parameterization and validation is the contribution; we provide the first model with Indian tariff data
- "Is 12% energy saving worth the implementation complexity?" → Counter: at MSME scale, 12% × ₹50L annual energy cost = ₹6L savings

> **Verdict: GO** — Strong mathematical foundation, clear measurable output. Slightly less visually impressive prototype (software only). Try to get real MSME data.

---

### Stress-Test: Idea 15 — IAQ MPC for Industrial Workshops

**Does this actually fill a research gap?**
Yes. MPC for building HVAC is well-studied, but industrial workshop application with multi-point pollutant sources and low-cost sensors is genuinely novel. Workshop environments differ fundamentally from office buildings — intermittent, high-intensity pollutant sources.

**What papers already do something similar?**
- Numerous MPC-for-HVAC papers (Afram & Janabi-Sharifi, 2014 — review)
- None specifically for small industrial workshops with multi-point pollutant control

**What exactly is our contribution?**
Adapting MPC to workshop IAQ with zone-based modeling, using low-cost sensors, and demonstrating energy-IAQ tradeoff quantitatively.

**Is it technically solvable within our resources?**
Mostly. Sensors are affordable. Main challenge: need a workshop-like space (even a lab with a simulated pollutant source like incense). Python MPC libraries (do-mpc) are available.

**Where could our approach fail?**
1. System identification may be poor with low-cost sensors → noisy state estimates
2. Workshop airflow is turbulent and hard to model → simple zone model may be inaccurate
3. Need a physical space with controllable fans → logistics

**Baseline:** Always-on fans (constant speed) and manual on/off control

**What would an evaluator challenge?**
- "Your zone model is too simplified" → Counter: we validate against measured data and show it works within acceptable error bounds
- "Is MPC overkill for a fan controller?" → Counter: threshold-based control wastes 30–40% energy; MPC demonstrates the value of model-based control

> **Verdict: GO with modifications** — Strongest mathematical depth but highest implementation risk. Consider using a lab space with a controllable smoke/incense source to simulate pollutants.

---

## Part 5: Final Decision Framework

### Candidate A — Strongest Research Opportunity: Idea 2 (Edge-TinyML Bearing Fault Diagnosis)

**Problem Statement:** Existing bearing fault diagnosis models trained on constant-speed benchmark datasets fail when deployed on real MSME machines with variable loads and speeds, and no complete edge-deployable pipeline exists.

**Research Gap:** The intersection of (order-tracking-based speed-invariant feature extraction) + (MMD domain adaptation) + (TinyML edge deployment on ESP32) is an unvalidated combination addressing a documented failure mode of existing systems.

**State-of-the-Art:** TinyML bearing diagnostics achieve >95% on CWRU (constant speed) but <70% on variable-speed data without adaptation.

**Proposed Contribution:** A validated end-to-end pipeline proving that physics-informed preprocessing (order tracking) combined with domain adaptation enables >90% accuracy on variable-speed data within ESP32 constraints.

**Mathematical Formulation:** Order spectrum + MMD loss + INT8-quantized 1D-CNN (see Idea 2 details)

**Prototype Architecture:**
```
MEMS Accelerometer → ESP32 (sampling) → Order Tracking → 1D-CNN (TFLite) → OLED Display + WiFi Alert
```

**Required Resources:** ADXL345 (₹200), ESP32 (₹500), lab motor with VFD (borrow from lab), tachometer sensor (₹300), total: <₹3000

**Baseline:** CWRU-trained CNN without adaptation on variable-speed data

**Evaluation Metrics:** Accuracy, F1-score, inference time (ms), memory footprint (KB), classification per fault type

**Expected Contribution:** First validated low-cost (<₹2000) bearing diagnostic device for variable-speed MSME motors

**Major Risks:** MEMS noise; ESP32 memory constraints; order tracking requires shaft speed signal

**Key Papers:**
| Paper | Problem | Method | Key Finding | Limitation | Relevance |
|---|---|---|---|---|---|
| Smith & Randall (2015) | Bearing diagnostics | Order tracking | Speed normalization improves diagnosis | Desktop only, no edge | Our preprocessing basis |
| Long et al. (2015) | Domain adaptation | DAN/MMD | Transfer learning improves cross-domain accuracy | Not applied to bearing/edge | Our adaptation method |
| Banerjee et al. (2024) | TinyML PdM | CNN on MCU | >95% on CWRU | Constant speed only | Our deployment target |
| CWRU Dataset | Benchmark bearing data | Various | Standard benchmark | Constant speed, lab conditions | Our training baseline |

---

### Candidate B — Strongest Feasibility: Idea 3 (Energy-Aware Production Scheduling)

**Problem Statement:** Indian MSMEs waste 15–25% on energy costs because production scheduling ignores time-of-use electricity tariffs and machine-state energy consumption.

**Research Gap:** No energy-aware scheduling model is parameterized and validated with Indian ToU tariffs and real MSME machine energy profiles (including idle/startup power).

**State-of-the-Art:** Energy-aware scheduling is well-studied theoretically but rarely validated with real industrial data, especially for Indian MSMEs.

**Proposed Contribution:** A context-validated bi-objective MILP model with empirically measured energy parameters from an Indian MSME, demonstrating quantifiable savings.

**Mathematical Formulation:** Bi-objective MILP (makespan + energy cost) with ε-constraint method and NSGA-II fallback (see Idea 3 details)

**Prototype Architecture:**
```
Job Data Input → Machine Energy Profiles → MILP Solver (PuLP/Gurobi) → Pareto Front Visualization → Gantt Chart Output
```

**Required Resources:** Python (free), PuLP/Gurobi academic (free), power meter PZEM-004T (₹500), state tariff data (publicly available), total: <₹1000

**Baseline:** FCFS and SPT scheduling without energy consideration

**Evaluation Metrics:** Total energy cost (₹), makespan (hours), Pareto optimality gap, computational time

**Expected Contribution:** First MILP model validated with Indian ToU tariffs showing 12–20% energy cost savings

**Major Risks:** MSME data access; MILP tractability for large instances; energy savings may be small if tariff differential is low

**Key Papers:**
| Paper | Problem | Method | Key Finding | Limitation | Relevance |
|---|---|---|---|---|---|
| Gahm et al. (2016) | Energy-efficient scheduling survey | Literature review | Comprehensive taxonomy | No Indian context | Our survey foundation |
| Mouzon et al. (2007) | Machine idle/off energy | MILP | Significant savings from idle control | Single machine, no tariffs | Our foundational model |
| Zhang et al. (2023) | Multi-objective green scheduling | NSGA-II | Pareto front exploration | No real data validation | Our methodology reference |

---

### Candidate C — Strongest Technical Ambition: Idea 15 (IAQ MPC for Workshops)

**Problem Statement:** Indian industrial workshops expose workers to PM2.5 levels 5–20× above safety limits, while always-on ventilation wastes 30–40% energy. No model-predictive control system exists for small workshop ventilation.

**Research Gap:** MPC for IAQ is studied for commercial buildings but not for small industrial workshops with intermittent, spatially non-uniform pollutant sources. The dynamics, disturbance patterns, and control architecture are fundamentally different.

**State-of-the-Art:** Building MPC achieves 20–30% HVAC energy savings. No workshop-specific validation exists.

**Proposed Contribution:** First MPC implementation for workshop IAQ with zone-based pollutant modeling, demonstrated on a real or simulated workshop with measurable energy savings.

**Mathematical Formulation:** State-space model + receding horizon optimization (see Idea 15 details)

**Prototype Architecture:**
```
PM2.5/VOC Sensors (×3–4) → ESP32 Hub → Python MPC Controller → PWM Fan Speed Control → Energy + IAQ Logging
```

**Required Resources:** PMS5003 sensors (₹1000×3 = ₹3000), SGP30 (₹500), PWM-controlled fan (₹2000), ESP32 (₹500×2), power meter (₹500), total: <₹8000

**Baseline:** Always-on fans (constant max speed); threshold-based ON/OFF control

**Evaluation Metrics:** Average PM2.5 (μg/m³), energy consumed (kWh), percentage of time above IAQ limit, MPC solve time

**Expected Contribution:** 30–40% energy reduction vs. always-on ventilation with 95%+ IAQ compliance time

**Major Risks:** Zone model accuracy; sensor calibration drift; need physical workshop space; MPC computation latency

**Key Papers:**
| Paper | Problem | Method | Key Finding | Limitation | Relevance |
|---|---|---|---|---|---|
| Afram & Janabi-Sharifi (2014) | Building HVAC MPC review | MPC variants | 20–30% energy savings | Office buildings only | Our methodology basis |
| Goyal & Barber (2017) | Multi-zone MPC | Linear MPC | Effective zone-based control | Commercial HVAC, not workshops | Our control framework |
| India OSHA PM2.5 limits | Regulatory standard | — | Workplace exposure limits | Not connected to control | Our constraint values |

---

## Part 6: Go / Modify / Reject Checklist

### Candidate A: Edge-TinyML Bearing Fault Diagnosis

| Checkpoint | Status | Notes |
|---|---|---|
| Problem | ✅ GO | Real, significant, well-documented |
| Literature | ✅ GO | Extensive prior work establishes the space |
| Gap | ✅ GO | Variable-speed + edge is specific and defensible |
| Mathematics | ✅ GO | Order tracking + MMD + quantization are well-grounded |
| Engineering | ✅ GO | Clear hardware + software integration |
| Prototype | ✅ GO | Self-contained device with compelling demo |
| Validation | ✅ GO | CWRU baseline + own variable-speed data |
| SDG 9 | ✅ GO | Direct — MSME technology access (9.3) |
| Rubric | ✅ GO | Innovation (high), Functionality (demonstrable), Tools (TinyML + edge) |

> **Overall: ✅ GO** — Strongest all-around candidate. Balances research depth with feasibility and demo potential.

---

### Candidate B: Energy-Aware Production Scheduling

| Checkpoint | Status | Notes |
|---|---|---|
| Problem | ✅ GO | Real, significant |
| Literature | ✅ GO | Extensive OR foundation |
| Gap | ⚠️ MODIFY | Gap is real but narrow — strengthen by emphasizing Indian tariff specificity |
| Mathematics | ✅ GO | Strong MILP/Pareto formulation |
| Engineering | ⚠️ MODIFY | Software-only prototype — add basic hardware (power meter visualization) for demo impact |
| Prototype | ⚠️ MODIFY | Add interactive web UI with Gantt chart for visual impact |
| Validation | ✅ GO | Clear baseline comparisons possible |
| SDG 9 | ✅ GO | Direct — resource efficiency (9.4) |
| Rubric | ⚠️ MODIFY | Needs stronger "Innovation" and "Usability" demonstration |

> **Overall: ⚠️ MODIFY then GO** — Excellent technical depth. Add a hardware component (real-time energy monitoring dashboard) and a polished web UI to strengthen Innovation and Usability scores.

---

### Candidate C: IAQ MPC for Workshops

| Checkpoint | Status | Notes |
|---|---|---|
| Problem | ✅ GO | Real, significant, documented worker health impact |
| Literature | ✅ GO | Strong MPC foundation |
| Gap | ✅ GO | Workshop MPC is genuinely novel |
| Mathematics | ✅ GO | Strongest mathematical depth (MPC/control theory) |
| Engineering | ⚠️ MODIFY | Need to secure workshop space or build simulated environment in lab |
| Prototype | ⚠️ MODIFY | Physical setup complexity is highest of the three |
| Validation | ⚠️ MODIFY | Need to validate zone model accuracy — add system identification step |
| SDG 9 | ✅ GO | Direct — sustainable industrialization (9.2, 9.4) |
| Rubric | ✅ GO | Innovation + Functionality + Mathematical depth all strong |

> **Overall: ⚠️ MODIFY then GO** — Highest technical ambition and strongest mathematical depth. Mitigate setup risk by planning a controlled lab experiment with a simulated pollutant source (incense + fan setup) as fallback if workshop access is unavailable.

---

## Final Recommendation

| Rank | Candidate | Strength | Risk Level | Recommended Action |
|---|---|---|---|---|
| **#1** | **Idea 2: Edge-TinyML Bearing Diagnosis** | Best overall balance — feasible, demonstrable, defensible gap, hardware+software | Low | **GO — Primary choice** |
| **#2** | **Idea 3: Energy-Aware Scheduling** | Strongest OR/mathematical depth, lowest cost | Low-Medium | **MODIFY — Add hardware component, then GO** |
| **#3** | **Idea 15: IAQ MPC for Workshops** | Highest technical ambition, most impressive if executed | Medium | **MODIFY — Secure physical setup, then GO** |

> **The evidence supports Idea 2 (Edge-TinyML Bearing Fault Diagnosis) as the strongest candidate.** It maximizes rubric alignment across all phases: clear problem definition (Phase I), sophisticated tool integration (Phase II), and a compelling, functional, innovative prototype (Phase III — the highest-weighted phase). The research gap is specific and defensible, the mathematics are rigorous but not excessive, the prototype cost is minimal, and the results are quantitatively measurable. It also has strong publication potential for the +20 bonus marks.


---

## APPENDIX F — `sdg9_project_audit.md`

# SDG 9 Engineering Project — Independent Critical Audit

> **Audit Date:** 2026-10-01
> **Auditor Posture:** Hostile evaluator — every claim must earn its place.
> **Source Documents:** [030 EL Rubrics (1).pdf](file:///c:/Project/EL/030%20EL%20Rubrics%20(1).pdf) and [sdg9_project_analysis.md](file:///c:/Project/EL/sdg9_project_analysis.md)

---

## 1. Executive Diagnosis

Your analysis document is **above-average student work** — it demonstrates genuine research effort, proper problem structuring, and avoids some of the most common traps. However, it has systematic weaknesses that could cost you marks or, worse, lead to a project that falls apart during execution:

1. **Inflated confidence in novelty claims.** Phrases like "no existing work provides," "first validated low-cost system," and "no published work validates" are stated without a visible systematic search. Recent literature (2024–2025) shows substantially more overlap with your proposals than the document acknowledges.
2. **Arbitrary numerical scoring.** The 1–10 scoring table in Part 3 creates false precision. A "8.50 vs 8.40" difference is meaningless without calibration.
3. **Expected improvement percentages are unsupported.** "25–40% improvement," "12–20% energy savings," "30–40% energy reduction" appear repeatedly without any basis — these are targets presented as predictions.
4. **The rubric was misread in key areas.** Marks were reported as sub-criteria within larger blocks, but several weight distributions in the analysis don't match the actual rubric.
5. **The strongest idea (Idea 2) has more prior art than acknowledged.** Domain adaptation + TinyML for bearing faults is an active, competitive research area in 2024–2025. The "gap" is narrower than presented.

**Bottom line:** You have viable project concepts, but the framing needs to be rebuilt — less grandiose claims, tighter gap definition, and honest acknowledgment of what is truly novel vs. what is system integration.

---

## 2. Rubric Reconstruction

### 2.1 Accurate Rubric Table (from original PDF)

| Phase & Section | Marks | Sub-Criteria | Explicit Requirement | What Evaluators Are Likely Testing | Implication for Project |
|---|---:|---|---|---|---|
| **Phase I — Problem Definition** | **20** | Clarity, Relevance, Context, Flow Chart | Clear problem statement; SDG relevance; literature context; visual methodology | Can the student articulate a real, specific problem grounded in literature? | Must have a crisp 1–2 sentence problem + thorough survey + process diagram |
| **Phase I — Objectives** | **10** | Specificity, Alignment, Achievability | Measurable objectives aligned with problem; realistic scope | Are the objectives SMART and traceable to the problem? | State concrete metrics (e.g., "classify with >90% F1") — not vague aspirations |
| **Phase I — Methodology** | **10** | Appropriateness, Detail | Justified method selection; detailed documentation | Is the method a good fit, or was it chosen because "AI is cool"? | Justify every tool/algorithm choice with a technical rationale |
| **Phase II — Project Execution** | **30** | Adherence, Timeliness, Quality | Follow the methodology; on-time; high build quality | Did they actually do what they said they would, on time, well? | Don't over-promise in Phase I — you'll be graded on adherence |
| **Phase II — Tools & Techniques** | **20** | Selection, Application, Integration | Cutting-edge & appropriate tools; expert application; seamless integration | Technical sophistication and depth of tool usage | Tools must be demonstrably well-chosen and deeply used, not surface-level |
| **Phase II — Partial Results** | **10** | Clarity, Progress, Analysis | Clear documentation; significant progress; thoughtful analysis | Is the team on track by midpoint? | Must have tangible, analyzed intermediate results by mid-semester |
| **Phase III — Prototype Demonstration** | **30** | Functionality, Innovation, Usability | Working prototype; innovative approach; user-friendly | Does it work? Is it new? Can someone use it? | **HIGHEST-WEIGHT SECTION.** Non-functional prototype is catastrophic. |
| **Phase III — Results & Discussion** | **20** | Clarity, Analysis, Interpretation | Clear results; thorough analysis; logical interpretation | Quantitative depth and honest interpretation of findings | Need statistical analysis, not just "it works" |
| **Phase III — Report** | **20** | Organization, Clarity, Completeness | Well-organized; concise; all sections | Professional technical writing | Must be complete — no missing sections |
| **Phase III — Poster/PPT** | **10** | Visual Appeal, Clarity, Content | Professional design; clear communication; key content | Can they present visually and verbally? | Polish matters — don't neglect this |
| **Bonus** | **+20** | Notable Outcomes | Publications, patents, product development, conference | Exceptional impact beyond academic requirements | Realistic only if work quality supports a conference paper |
| **TOTAL** | **200 + 20** | | | | |

### 2.2 Discrepancies with Your Analysis

> [!WARNING]
> Your analysis document states marks like "/20 (sub)" for individual criteria within Problem Definition. This is **incorrect**. The rubric gives **20 marks total** for Problem Definition, divided among 4 sub-criteria (Clarity, Relevance, Context, Flow Chart). Each sub-criterion has a 5-level scale (Excellent 20–16, Very Good 15–12, Good 11–8, Satisfactory 7–4, Needs Improvement 3–0), but the marks shown are the **total section marks**, not per-criterion.

The sub-criteria scores appear to be holistic — the evaluator gives a single mark for the section, guided by where the project falls on each sub-criterion. This means:

- You cannot game individual sub-criteria independently.
- A weakness in any one sub-criterion drags the whole section down.

### 2.3 Corrected Weight Distribution

```
Phase I:   40 / 200 = 20%    (Problem: 20, Objectives: 10, Methodology: 10)
Phase II:  60 / 200 = 30%    (Execution: 30, Tools: 20, Partial Results: 10)
Phase III: 100 / 200 = 50%   (Prototype: 30, Results: 20, Report: 20, Poster: 10)
Bonus:     +20 (uncapped?)
```

**Your document got this correct.** The weight distribution analysis on lines 50–55 is accurate.

---

### 2.4 Hidden Project Requirements

**Explicit Rubric Requirements:**
1. Working prototype that is functional, innovative, and usable
2. Clear, specific, measurable objectives
3. Appropriate methodology with detailed documentation
4. Literature context (background research)
5. Cutting-edge tools, expertly applied, seamlessly integrated
6. Clear quantitative results with thorough analysis
7. Complete, well-organized report
8. Professional poster/PPT
9. Adherence to proposed methodology
10. On-time delivery

**Strongly Implied Requirements (not stated verbatim but tested):**
1. **Baseline comparison** — "thorough analysis" and "logical, well supported interpretation" are impossible without one
2. **Measurable improvement** — "Innovation" criterion requires demonstrating something new actually works better
3. **Statistical rigor** — "thoroughly analyzed/interpreted" means confidence intervals, not single-run results
4. **Engineering depth** — "cutting-edge, highly appropriate tools" means the evaluator expects technical sophistication
5. **SDG 9 connection that survives scrutiny** — "highly relevant/significant" means the SDG link must be direct, not stretched

**Useful But NOT Actually Required:**
1. Publication / patent (this is bonus, not mandatory)
2. Industry collaboration or deployment
3. Mathematical formulation (the rubric does not explicitly require it — but it's hard to score "excellent" without one)
4. Hardware (software-only can score well if demonstrably functional and innovative)

---

### 2.5 Failure Modes

| Failure Mode | Mechanism | Rubric Impact |
|---|---|---|
| Non-functional prototype | Kills Functionality (30 marks), drags Innovation and Usability | Loss of 20–30 marks in Phase III alone |
| Superficial AI usage | "AI" bolted on without justification; evaluator sees through it | Fails Appropriateness (Methodology) and Selection (Tools) |
| No measurable baseline | Cannot demonstrate improvement; results section becomes hand-waving | Kills Analysis and Interpretation (20 marks) |
| Weak problem definition | Cascading: vague problem → vague objectives → unfocused methodology | Loses marks across all of Phase I (40 marks) |
| Over-scope | Nothing works well; deadline missed | Kills Functionality, Timeliness, Quality |
| "Solution searching for a problem" | Problem is manufactured to justify a cool technology | Evaluator detects this immediately; Relevance and Alignment suffer |
| Unverifiable novelty claims | "First ever" / "novel" without evidence | Evaluator may challenge; Innovation score drops |
| Prototype disconnected from math | Math in report, prototype does something else | Adherence fails; tools seem bolted on |
| Claims unsupported by experiments | "30% improvement" with no data | Interpretation criterion: "illogical/no interpretation" |

### What Our Final Project MUST Demonstrate

1. **A clearly stated, real problem** with direct SDG 9 relevance that can be explained to a non-specialist in 2 sentences.
2. **Literature-grounded context** with at least 8–12 credible sources establishing the problem and existing solutions.
3. **A specific, defensible gap** — not "nobody has done exactly this" but "existing solutions fail at X because of Y."
4. **Measurable objectives** with concrete metrics and targets (e.g., "achieve >90% F1-score at <100ms inference time on ESP32").
5. **A fully functional prototype** that an evaluator can interact with during demonstration.
6. **Quantitative baseline comparison** — at minimum two conditions: baseline vs. proposed method.
7. **Statistical analysis of results** — multiple trials, confidence intervals, or hypothesis tests.
8. **Justified tool selection** — every technology used must have a documented reason for selection.
9. **Ablation or component analysis** — show which part of the system provides the improvement.
10. **Complete documentation** — report with all sections, professional poster/PPT.

---

## 3. Audit of Existing Analysis

### 3.1 Claim Classification

| Document Claim | Location | Classification | Audit Notes |
|---|---|---|---|
| Indian MSMEs (70M+ units) lose ≈₹1.5L/day to unplanned downtime | Idea 2 | [ESTABLISHED] | Widely cited figure from MSME Ministry reports, though the per-unit figure varies significantly by sector |
| CWRU-trained models achieve >95% accuracy on constant speed | Idea 2 | [ESTABLISHED] | Well-documented benchmark, but recent 2024 papers warn many published results suffer from data leakage |
| CWRU models degrade to <70% on variable-speed data | Idea 2 | [INFERENCE] | Plausible and directionally supported by domain adaptation literature, but the "<70%" figure is not from a specific cited source — it's an estimate |
| "No existing work provides a complete, validated pipeline from MEMS sensor → edge inference → interpretable output specifically adapted for variable-speed operation on sub-₹5000 hardware" | Idea 2 | **[OVERCLAIMED]** | Multiple 2024–2025 papers combine MEMS + edge TinyML + domain adaptation. The exact combination on sub-₹5000 hardware for Indian MSMEs may be unvalidated, but the individual pipeline components have been demonstrated together |
| Order tracking + MMD + TinyML is "an unvalidated combination" | Idea 2 | **[OVERCLAIMED]** | Order tracking is a well-known preprocessing technique. MMD-based domain adaptation has been applied to bearing faults. TinyML deployment exists. The novelty is narrower than claimed — it's a specific integration, not a new technique |
| "First validated low-cost (<₹2000) bearing diagnostic device for variable-speed MSME motors" | Idea 2 | **[OVERCLAIMED]** | "First" claims require exhaustive search. Low-cost MEMS + ESP32 predictive maintenance systems are documented in Indian academic literature (2024). The "first" claim is unsafe |
| Indian MSMEs waste 15–25% on energy costs due to scheduling | Idea 3 | [INFERENCE] | Reasonable inference from BEE India data on industrial energy efficiency, but the 15–25% is a range estimate, not a precisely cited figure |
| "No model specifically addresses Indian ToU tariffs + MSME batch production" | Idea 3 | [INFERENCE] | Likely true as of 2024 that no paper explicitly uses Indian tariff data, but energy-aware scheduling with ToU tariffs + machine-state energy is well-studied. The gap is geographic/contextual, not algorithmic |
| 12–20% energy cost reduction expected | Idea 3 | [HYPOTHESIS] | Presented as "expected improvement" but is actually a target to be tested — no evidence is provided for this specific range |
| MPC for workshop IAQ is "genuinely novel" | Idea 15 | [INFERENCE] | MPC for buildings is well-studied. Workshop-specific MPC with multi-point pollutant sources appears less studied, but "genuinely novel" overstates the search confidence |
| 30–40% energy reduction vs. always-on ventilation | Idea 15 | [HYPOTHESIS] | This range is extrapolated from building HVAC MPC studies (20–30% savings). Workshop dynamics differ substantially — the transfer is not automatic |
| India loses 20–40% of perishable produce (₹92,000 crore/year) | Idea 5 | [ESTABLISHED] | Widely cited from ICAR and NABARD reports |
| "No integrated system combines offline-capable edge inference + commodity-specific thermal-kinetic spoilage models + remaining shelf-life prediction" | Idea 5 | [INFERENCE] | Spoilage kinetics + IoT monitoring each exist. The specific integration for Indian first-mile conditions is plausible as a gap, but "no integrated system" is a strong claim |

### 3.2 Systematic Problems in the Analysis

1. **Every idea claims to be the "first" or "no existing work."** This is a red flag. In an active research area, the probability that *none* of 15 ideas has any close prior art is extremely low. The search methodology is not documented.

2. **Expected improvement percentages appear to be aspirational targets, not evidence-based predictions.** The document treats them as features of the proposal rather than hypotheses to test.

3. **The scoring table (Part 3) uses false precision.** Scoring "Rubric alignment" at 9 vs. 8 for different ideas without any calibration methodology is opinion masquerading as data. The weighted score difference (8.50 vs. 8.40) is within noise.

4. **Stress tests (Part 4) are self-confirming.** The stress tests ask good questions but consistently arrive at "GO." A genuine stress test should find at least one dealbreaker or near-dealbreaker.

5. **References are sparse.** For a document claiming to be "research-backed," most ideas cite only 3–4 sources. A credible literature review should cite 8–15 per idea.

---

## 4. Research & Prior-Art Findings

### 4.1 Idea 2 — Edge-TinyML Bearing Fault Diagnosis: Evidence Table

| Source | Problem | Method | Key Finding | Limitation | Relevance to Idea 2 |
|---|---|---|---|---|---|
| MSACNN-IJMMD-DANN (MDPI, 2024) | Variable-speed bearing fault diagnosis | Multi-Scale Attention CNN + Joint MMD + DANN | Achieves domain-invariant features across operating conditions | Desktop only; not on edge hardware | **Directly overlapping** — domain adaptation for variable-speed is actively researched |
| Banerjee et al. (2024, adroidjournals) | TinyML predictive maintenance on ESP32 | 1D-CNN + TFLite on ESP32-S3 | >92% accuracy on CWRU; ~17.7 mJ per inference | Constant speed only; no domain adaptation | Close overlap on edge deployment; lacks the variable-speed element |
| CWT-SimAM-DAMS (MDPI, 2024) | Cross-domain bearing diagnosis | Attention mechanism + JMMD + CDAN | Effective distribution alignment | Not deployed on microcontroller | Same domain adaptation goal, different architecture |
| Smith & Randall (2015, MST) | Order tracking for bearing diagnostics | Angular resampling | Eliminates speed-related smearing | Desktop signal processing; no ML integration | Foundational technique your idea builds on — well-established, not novel |
| Long et al. (2015, ICML) | Transfer learning | DAN / MMD | MMD aligns domain distributions effectively | General computer vision; not bearing-specific originally | Your adaptation method — well-established, not novel |
| Selective Distillation (ResearchGate, 2025) | Joint compression + cross-domain diagnosis | Knowledge distillation + domain adaptation | Compresses models while maintaining cross-domain accuracy | Specific architecture; not ESP32 validated | **Directly addresses** the same space (edge + domain adaptation) |
| CWRU Benchmarking Issues (arXiv, 2024) | Data leakage in bearing diagnosis | Rigorous evaluation protocols | Many published >95% results are over-optimistic due to data leakage | Challenges the baseline accuracy claims | **Critical for your proposal** — you must use leakage-free evaluation |
| zbotic.in (Indian, 2024–2026) | Low-cost MEMS + ESP32 bearing monitoring | ADXL345 + ESP32 + FFT/RMS | Working systems at ₹2000–2600/unit documented for Indian MSMEs | No domain adaptation; threshold-based | **Partial overlap** — similar hardware, similar market, but no ML adaptation |

### 4.2 Idea 3 — Energy-Aware Scheduling: Evidence Table

| Source | Problem | Method | Key Finding | Limitation | Relevance to Idea 3 |
|---|---|---|---|---|---|
| Gahm et al. (2016, EJOR) | Energy-efficient scheduling survey | Literature review of 100+ papers | Comprehensive taxonomy of approaches | Pre-2016; no Indian context | Foundation — your starting point |
| Mouzon et al. (2007, IIE Trans.) | Machine idle/off energy minimization | MILP with machine state control | Significant savings from idle-state management | Single machine; no ToU tariffs | Your foundational model concept is based on this |
| State-dependent MILP (MDPI, 2023–2024) | Job-shop with idle/startup energy | MILP with machine state transitions | Machine-state energy models now standard in literature | Western tariff structures assumed | **Directly overlapping** — machine-state energy in scheduling is well-studied |
| Period-indexed MILP (SciTePress, 2024) | ToU-aware scheduling | Period-indexed MILP formulation | More computationally efficient than time-indexed | Not Indian-specific | Same computational approach |
| CEEW India (2024) | Indian MSME energy efficiency | Policy analysis | India adopting ToU/ToD tariffs; significant MSME opportunity | Not an optimization study | Validates the problem relevance |
| Multi-objective green scheduling (MDPI, 2023) | Bi-objective makespan + energy | NSGA-II | Pareto front exploration effective | No real industrial data validation | Same methodology (NSGA-II for Pareto) |

### 4.3 Idea 15 — IAQ MPC: Evidence Table

| Source | Problem | Method | Key Finding | Limitation | Relevance to Idea 15 |
|---|---|---|---|---|---|
| Afram & Janabi-Sharifi (2014, Appl. Energy) | MPC for building HVAC | MPC review | 20–30% energy savings demonstrated | Office/commercial buildings only | Your methodology basis — validates MPC for IAQ |
| MDPI Zone-Based MPC (2024) | Multi-zone IAQ control | Zone-based MPC with occupancy | Effective zone-level optimization | Commercial buildings, not workshops | Same concept, different domain |
| Liverpool Cleanroom MPC (2024) | Industrial cleanroom MPC | MPC for air cleanliness in cleanrooms | Significant energy savings while maintaining PM standards | Cleanroom (controlled environment), not workshop | **Close prior art** — MPC in industrial setting exists |
| Low-cost sensor calibration (MDPI, 2024) | LCS reliability for IAQ | ML-based field calibration | Calibration essential for reliable MPC inputs | Adds complexity to your system | You must address sensor drift and calibration |
| Surrogate model MPC (MDPI, 2024) | Real-time MPC with ANN surrogates | Neural network surrogate for CFD | Enables real-time MPC in complex environments | Requires training data from CFD or experiments | Alternative to your state-space approach |

---

## 5. Novelty Audit

### Idea 2 — Edge-TinyML Bearing Fault Diagnosis

| Search Dimension | Finding | Classification |
|---|---|---|
| Exact proposed system (order-tracking + MMD + TinyML on ESP32 for bearing faults) | No exact match found in a single paper | **PARTIALLY OVERLAPPING** |
| Same algorithmic combination (MMD + lightweight CNN for bearing DA) | Multiple papers (2024–2025) combine MMD/DANN with CNNs for bearing DA | **DIRECTLY EXISTING** (on desktop) |
| Similar hardware + software (ESP32 + MEMS + TFLite for bearing faults) | Multiple implementations documented (2024–2025), including Indian projects | **DIRECTLY EXISTING** |
| Similar mathematical formulation (order spectrum + MMD loss) | Order tracking is textbook; MMD is standard; combination is incremental | **PARTIALLY OVERLAPPING** |
| Similar application domain (low-cost bearing diagnostics for Indian MSMEs) | Active area with documented Indian projects at ₹2000–2600 price point | **DIRECTLY EXISTING** |
| Similar low-cost/student-deployable implementation | Yes — multiple academic projects at similar price points | **DIRECTLY EXISTING** |

**Novelty Assessment:**

> **Exactly what is new here?**
>
> The specific *combination* of order-tracking preprocessing + MMD-based domain adaptation + INT8-quantized 1D-CNN deployed on ESP32, *validated* on variable-speed MEMS data collected from a lab motor.

**This is system-level novelty (C) and experimental/validation novelty (D).** It is NOT algorithmic novelty (A) or mathematical novelty (B). Each component exists independently. The contribution is *integration and validation under specific constraints*.

**This is honest and defensible** — but the document should not call it "innovative" without qualification. Call it what it is: a validated end-to-end integration study.

**Search limitations:** My search covered Google Scholar-indexed sources, MDPI, ResearchGate, arXiv, and Indian academic databases. I did not search IEEE Xplore or ACM DL directly. There may be additional overlapping work in those databases.

---

### Idea 3 — Energy-Aware Scheduling

| Search Dimension | Finding | Classification |
|---|---|---|
| Exact proposed system (bi-objective MILP with Indian ToU + MSME batch + machine-state energy) | No exact match with Indian tariff data | **ADJACENT** |
| Same algorithmic combination (MILP + ε-constraint + NSGA-II for energy scheduling) | Standard in OR literature | **DIRECTLY EXISTING** |
| Similar mathematical formulation (makespan + energy cost with machine states) | Well-studied since Mouzon 2007; machine-state MILP is standard by 2024 | **DIRECTLY EXISTING** |
| Indian context specifically | No published MILP model with Indian ToU tariff parameters found | **POTENTIALLY UNEXPLORED** |

**Novelty Assessment:**

> **Exactly what is new here?**
>
> Parameterizing an existing MILP scheduling model with Indian ToU tariff data and MSME-measured machine energy profiles.

**This is contextual novelty (E) and experimental novelty (D).** The algorithm is standard. The model structure is known. The contribution is applying it with Indian-specific data — valuable but must be framed honestly.

---

### Idea 15 — IAQ MPC for Workshops

| Search Dimension | Finding | Classification |
|---|---|---|
| Exact proposed system (zone-based MPC with low-cost PM2.5 sensors for workshop ventilation) | No exact match for small workshop application | **ADJACENT** |
| MPC for IAQ generally | Extensively studied for commercial buildings | **DIRECTLY EXISTING** |
| MPC for industrial environments | Cleanroom MPC exists (Liverpool, 2024) | **PARTIALLY OVERLAPPING** |
| Zone-based MPC | Standard technique in building control | **DIRECTLY EXISTING** |
| Low-cost sensor + MPC integration | Documented in building context | **DIRECTLY EXISTING** |

**Novelty Assessment:**

> **Exactly what is new here?**
>
> Applying zone-based MPC specifically to small industrial workshops with intermittent, spatially non-uniform pollutant sources (welding, grinding) rather than steady-state HVAC systems.

**This is contextual novelty (E) with some system-level novelty (C).** The MPC framework is standard. The application domain (small workshop with intermittent sources) is genuinely less studied than commercial buildings, but "genuinely novel" is an overstatement.

---

## 6. Mathematical Validation

### 6.1 Idea 2 — Bearing Fault Diagnosis

**Mathematical Components:**
- **Order tracking:** O(k) = DFT(x(θ)), where θ = ∫ω(t)dt — **VALID.** This is established signal processing (Smith & Randall, 2015). Appropriate for variable-speed normalization.
- **MMD loss:** MMD²(P,Q) = E[k(x,x')] - 2E[k(x,y)] + E[k(y,y')] with RBF kernel — **VALID.** Standard domain adaptation formulation (Long et al., 2015).
- **Combined loss:** L_total = L_classification + λ·MMD² — **VALID.** Standard multi-task loss.
- **INT8 quantization:** Post-training quantization — **VALID.** Standard TFLite pipeline.

**Assessment:**
- The mathematics is **appropriate and well-grounded** but **not novel**. Every component is textbook.
- The mathematical depth is **moderate** — this is more of an engineering integration project than a mathematical contribution.
- The main mathematical challenge is **tuning λ** (the domain adaptation weight) — this is empirical, not theoretical.
- **Baseline comparison is well-defined:** raw FFT + CNN on CWRU vs. order-tracking + MMD-adapted model on variable-speed data.
- **Computational complexity:** 1D-CNN inference on ESP32 is O(N·K·C) per layer; quantized inference adds no asymptotic overhead. Fitting within 520KB SRAM is the real constraint.

**What students must understand and defend:**
- Fourier analysis and sampling theory
- Basics of convolutional neural networks
- Domain adaptation concept (why distributions shift)
- Quantization effects on accuracy
- Bearing fault mechanics (BPFO, BPFI, BSF frequencies)

**Verdict:** Mathematics is **valid but not deep**. This is an engineering project with mathematical support, not a mathematical project. That is fine for the rubric, but do not over-sell the mathematical contribution.

---

### 6.2 Idea 3 — Energy-Aware Scheduling

**Mathematical Formulation (reconstructed):**

**Decision Variables:**
- s_ij ∈ ℝ⁺ : start time of operation j of job i
- y_mkt ∈ {0,1} : machine m is in processing state during time slot t
- z_mt ∈ {0,1} : machine m has a startup event at time slot t
- w_mt ∈ {0,1} : machine m is idle during time slot t

**Parameters:**
- P_proc(m) : processing power of machine m (kW) — measured
- P_idle(m) : idle power of machine m (kW) — measured
- E_startup(m) : startup energy of machine m (kWh) — measured
- tariff(t) : electricity price in time slot t (₹/kWh) — from state utility data
- p_ij : processing time of operation j of job i
- Q_m : set of operations assignable to machine m

**Objective 1 (Makespan):**
min C_max = max_i {completion time of last operation of job i}

**Objective 2 (Energy Cost):**
min Σ_t Σ_m [P_proc(m)·y_mkt + P_idle(m)·w_mt + E_startup(m)·z_mt] × tariff(t) × Δt

**Constraints:**
- Precedence: s_{i,j+1} ≥ s_ij + p_ij ∀i,j
- No overlap: at most one operation on each machine at any time
- Machine state logic: y_mkt + w_mt + (off state) = 1
- Startup detection: z_mt ≥ y_mkt - y_{mk,t-1}
- Time windows: optional delivery deadlines

**Solution Approach:**
- ε-constraint method for Pareto front (exact, for small instances)
- NSGA-II for larger instances (approximate)

**Assessment:**
- The formulation is **standard and well-grounded** in OR literature (Gahm et al., 2016; Mouzon et al., 2007).
- **Mathematical depth is the strongest** among the three candidates — genuine combinatorial optimization with multi-objective analysis.
- **NP-hardness** of job-shop scheduling means exact solutions only work for small instances (≤10 jobs × 5 machines) — this is well-known and the NSGA-II fallback is appropriate.
- **Key trade-off:** Pareto front between makespan and energy cost is genuinely interesting and produces interpretable results.
- **What's different from existing work:** Not the formulation — it's the **parameterization** with Indian tariff data and measured MSME machine profiles.
- **Baseline is clear:** FCFS and SPT scheduling without energy consideration.

**What students must understand and defend:**
- MILP formulation and solver behavior
- Pareto optimality and ε-constraint method
- Multi-objective optimization concepts
- Job-shop scheduling complexity
- Statistical comparison methodology (Wilcoxon test)

**Verdict:** Mathematics is **strong and central** to the project. The formulation is standard but well-applied. This is the most mathematically honest of the three candidates.

---

### 6.3 Idea 15 — IAQ MPC

**Mathematical Formulation (reconstructed):**

**State-Space Model:**
C_{k+1} = A·C_k + B·u_k + D·d_k + w_k

Where:
- C_k ∈ ℝⁿ : pollutant concentration vector at n zones (μg/m³)
- u_k ∈ ℝᵐ : fan speed vector for m fans (duty cycle 0–1)
- d_k ∈ ℝᵖ : disturbance vector (pollutant source terms)
- w_k : process noise
- A, B, D : system matrices (identified from step-response experiments)

**MPC Objective:**
min_{u_0,...,u_{N-1}} Σ_{k=0}^{N-1} [Σ_j (fan_power_j(u_jk)) + λ·Σ_i max(0, C_ik - C_limit)²]

Subject to:
- C_{k+1} = A·C_k + B·u_k + D·d_k (dynamics)
- 0 ≤ u_k ≤ u_max (actuator limits)
- C_k ≤ C_max (hard IAQ limits — optional)

**Assessment:**
- The formulation is **valid and well-grounded** in control theory literature.
- **Mathematical depth is the highest** — MPC involves online optimization, system identification, and receding horizon control.
- **Main risk:** System identification (finding A, B, D matrices) in a turbulent workshop is **non-trivial**. The linear state-space model may be a poor approximation of real airflow dynamics.
- **Computational feasibility:** MPC on ESP32 may be challenging — the optimization problem must be solved in real-time (~1–10 second intervals). May need to run MPC on a laptop or Raspberry Pi.
- **Key trade-off:** IAQ compliance vs. energy consumption — genuinely interesting.

**What students must understand and defend:**
- State-space modeling and system identification
- Model Predictive Control theory
- Optimization (quadratic programming)
- Sensor calibration and noise handling
- PM2.5 measurement physics

**Verdict:** Mathematically the **deepest** candidate, but also the **highest risk**. If system identification fails, the entire project collapses.

---

## 7. Experimental Design

### 7.1 Idea 2 — Bearing Fault Diagnosis

**Baseline:** 
- A1: Raw FFT features + 1D-CNN trained on CWRU, tested on CWRU (standard benchmark — establishes ceiling)
- A2: Raw FFT features + 1D-CNN trained on CWRU, tested on lab variable-speed data (demonstrates the domain shift problem)

**Proposed Method Variants (Ablation):**
- B: Order-tracking features + 1D-CNN trained on CWRU, tested on lab variable-speed data (isolates preprocessing improvement)
- C: Raw FFT features + 1D-CNN with MMD domain adaptation, tested on lab variable-speed data (isolates DA improvement)
- D: Order-tracking features + 1D-CNN with MMD domain adaptation, tested on lab variable-speed data (full system)
- E: D quantized to INT8 on ESP32 (tests deployment accuracy loss)

**Dataset:**
- Source: CWRU Bearing Data Center (4 classes: Normal, Inner Race, Outer Race, Ball fault; multiple loads) — **free and available**
- Target: Lab-collected data from a 0.5–1 HP motor at 3–5 speed settings using ADXL345
- **Critical:** Use leakage-free data splitting (per 2024 arXiv recommendations)

**Experimental Setup:**
- Hardware: ADXL345 + ESP32 + lab motor with VFD (variable frequency drive)
- Data collection: 30-second recordings per condition, at 3+ speeds, 3+ loads = ~27–45 recordings
- **Requires:** Access to a lab motor with a VFD and ability to seed faults (or motor with known bearing damage)

**Metrics:**
- Accuracy, per-class F1-score (weighted and macro)
- Confusion matrix per condition
- Inference time on ESP32 (ms)
- Model size (KB)
- Memory usage on ESP32 (KB)

**Statistical Validation:**
- 5-fold cross-validation for model training
- Report mean ± std across folds
- Paired t-test or Wilcoxon signed-rank test for A2 vs. D comparison
- Effect size (Cohen's d)

**Testable Hypotheses:**
- H1: Order-tracking preprocessing improves F1-score on variable-speed data by >10 pp vs. raw FFT (B vs. A2)
- H2: MMD domain adaptation improves F1-score by >10 pp vs. non-adapted model (C vs. A2)
- H3: Combined system (D) achieves >85% F1-score on variable-speed data
- H4: INT8 quantization causes <3 pp accuracy degradation (E vs. D)

---

### 7.2 Idea 3 — Energy-Aware Scheduling

**Baseline:**
- A1: FCFS (First-Come-First-Served) scheduling — no energy consideration
- A2: SPT (Shortest Processing Time) scheduling — no energy consideration
- A3: Manual scheduling from MSME (if obtainable)

**Proposed Method:**
- B: Energy-unaware MILP (minimize makespan only)
- C: Energy-aware MILP (minimize energy cost only)
- D: Bi-objective MILP with ε-constraint (Pareto front)
- E: NSGA-II for larger instances

**Dataset:**
- Synthetic instances: 5×3, 10×4, 15×5, 20×5 (jobs × machines) — **generated programmatically**
- Indian ToU tariff data from state electricity regulatory commissions — **publicly available**
- Machine energy profiles: measure P_proc, P_idle, E_startup using PZEM-004T on actual machines — **requires MSME access or use published typical values**

**Metrics:**
- Total energy cost (₹)
- Makespan (hours)
- Pareto front visualization (makespan vs. energy cost)
- Computation time (seconds)
- Hypervolume indicator for multi-objective comparison

**Statistical Validation:**
- Generate 20+ random problem instances per size category
- Wilcoxon signed-rank test comparing D vs. A1 and D vs. A2 on energy cost
- Report Pareto front quality metrics (hypervolume, spread)

**Testable Hypotheses:**
- H1: Energy-aware scheduling reduces total energy cost by >10% vs. FCFS (D vs. A1)
- H2: Makespan increase under energy-aware scheduling is <10% vs. energy-unaware optimal (D vs. B)
- H3: NSGA-II approximation achieves >90% of exact Pareto front hypervolume (E vs. D)

---

### 7.3 Idea 15 — IAQ MPC

**Baseline:**
- A1: Always-on fans (constant maximum speed)
- A2: Threshold-based ON/OFF control (turn on when PM2.5 > threshold)
- A3: PID control (proportional to PM2.5 deviation from setpoint)

**Proposed Method:**
- B: Open-loop optimal fan schedule (computed offline, no feedback)
- C: MPC with single-zone model
- D: MPC with multi-zone model (full system)

**Dataset:**
- Collect real-time PM2.5, temperature, humidity data from sensor grid in test space
- Use controlled pollutant source (incense sticks at known burn rate) for repeatable experiments
- Record fan power consumption with power meter

**Experimental Setup:**
- Test space: lab room (~4×4m) with 2–3 PM2.5 sensors at different positions
- Controllable fans: 2 PWM-controlled exhaust fans
- Pollutant source: incense or mosquito coil (repeatable, safe, measurable)
- System ID experiments: Step responses (turn on pollutant source, measure sensor responses)
- Duration: 3–5 hour experiments per condition, minimum 3 repeats

**Metrics:**
- Average PM2.5 concentration (μg/m³)
- Time-weighted average exposure
- % time above IAQ limit (e.g., ISHRAE limit of 60 μg/m³)
- Total energy consumed by fans (kWh)
- MPC computation time per step (ms)

**Statistical Validation:**
- Minimum 3 replicate experiments per control condition
- ANOVA or Kruskal-Wallis test across conditions
- Report mean ± std for each metric

---

## 8. Feasibility Audit

### 8.1 Idea 2 — Edge-TinyML Bearing Fault Diagnosis

| Dimension | Assessment | Risk | Notes |
|---|---|---|---|
| **Data** | ✅ Feasible | Low | CWRU is free. Lab data collection requires motor access + 1–2 weeks |
| **Hardware** | ✅ Feasible | Low | ADXL345 (₹200) + ESP32 (₹500) + OLED (₹200) = ~₹1500 total BOM |
| **Software** | ✅ Feasible | Low | Python + TensorFlow Lite Micro — all free and well-documented |
| **Mathematics** | ✅ Feasible | Low | Order tracking and MMD are well-documented with code examples |
| **Experiment** | ⚠️ Moderate | Medium | **Requires a lab motor with VFD or speed control.** Requires either seeded bearing faults or pre-damaged bearings. Tachometer signal needed for order tracking |
| **Time** | ✅ Feasible | Low | Estimated 8–10 weeks of focused work |
| **Cost** | ✅ Feasible | Low | ~₹2000–3000 total prototype cost |
| **Demo** | ✅ Feasible | Low | Attach device to motor → see classification on OLED display. Very compelling |

**Critical dependency:** Access to a motor with variable speed capability and damaged bearings. If unavailable, the project degrades to CWRU-only, which weakens the contribution significantly.

---

### 8.2 Idea 3 — Energy-Aware Scheduling

| Dimension | Assessment | Risk | Notes |
|---|---|---|---|
| **Data** | ⚠️ Moderate | Medium | Tariff data is public. Machine energy profiles require MSME visit or published typical values |
| **Hardware** | ✅ Feasible | Low | PZEM-004T (₹500) for power measurement — optional but strengthening |
| **Software** | ✅ Feasible | Low | PuLP (free), Gurobi academic (free), Python — all accessible |
| **Mathematics** | ✅ Feasible | Low | MILP is covered in OR courses; students can learn PuLP in 1–2 weeks |
| **Experiment** | ✅ Feasible | Low | Synthetic instances can be generated programmatically; no physical experiment required for core validation |
| **Time** | ✅ Feasible | Low | Estimated 6–8 weeks |
| **Cost** | ✅ Feasible | Low | ~₹500–1000 (power meter only) |
| **Demo** | ⚠️ Moderate | Medium | Software tool with Gantt charts. Less visually dramatic than hardware projects. Needs a polished web UI to score well on Usability |

**Critical dependency:** MSME data access would strengthen the project enormously but is not strictly required (synthetic instances are standard in OR). The prototype is software-only, which may underperform on the "Functionality" and "Usability" criteria compared to a hardware-integrated demo.

---

### 8.3 Idea 15 — IAQ MPC

| Dimension | Assessment | Risk | Notes |
|---|---|---|---|
| **Data** | ⚠️ Moderate | Medium | Must collect all data experimentally — no public datasets for workshop IAQ |
| **Hardware** | ⚠️ Moderate | Medium | PMS5003 sensors (₹1000×3), PWM fans, ESP32 — total ~₹6000–8000 |
| **Software** | ⚠️ Moderate | Medium | do-mpc or CasADi for MPC — more specialized than TFLite or PuLP |
| **Mathematics** | ⚠️ Moderate | Medium-High | System identification and MPC tuning are non-trivial for undergraduates |
| **Experiment** | ⚠️ Moderate | Medium-High | Requires physical test space with controllable pollutant sources and fans. Experiments take hours and must be repeated |
| **Time** | ⚠️ Moderate | Medium | System ID alone may take 2–3 weeks. Full MPC pipeline: 10–12 weeks |
| **Cost** | ⚠️ Moderate | Low-Medium | ~₹6000–8000 |
| **Demo** | ✅ Feasible if built | Low | Sensor network + fan control with real-time dashboard. Very compelling if it works |

**Critical dependency:** Physical test space and successful system identification. If the linear model doesn't capture workshop dynamics, MPC performance degrades and the project's core claim fails.

---

## 9. Revised Candidate Table

| Idea | Real Problem | Research Foundation | Defensible Gap | Mathematical Depth | Prototype Feasibility | Experimental Feasibility | SDG 9 Fit | Main Risk | Decision |
|---|---|---|---|---|---|---|---|---|---|
| **Idea 2: Bearing TinyML** | Strong — MSME downtime is documented and costly | Strong — extensive literature on bearing DA and TinyML | **Narrow but defensible** — specific integration not validated as end-to-end pipeline on ESP32 under variable speed | Moderate — applied math, not novel math | Very high — cheap, simple hardware | High — if motor with VFD available | Direct (SDG 9.3) | Motor + bearing access; novelty is incremental | **GO** |
| **Idea 3: Energy Scheduling** | Strong — MSME energy costs are real | Very strong — decades of OR literature | **Narrow** — contextual novelty (Indian tariffs); algorithmic contribution is nil | **High** — genuine MILP + Pareto analysis | Very high — pure software + optional power meter | Very high — synthetic data available | Direct (SDG 9.4) | Gap is purely contextual; demo less impressive | **MODIFY** |
| **Idea 15: IAQ MPC** | Strong — documented worker health hazard | Strong — MPC for IAQ well-studied | **Moderate** — workshop application is less studied | **Highest** — full MPC control theory | Moderate — requires physical setup + sensor calibration | Moderate — time-intensive experiments | Direct (SDG 9.2, 9.4) | System identification failure; time and space requirements | **MODIFY** |
| Idea 1: Water Network | Strong — NRW in India is massive | Strong — graph theory + WDN literature | Moderate — Indian-topology optimization is less explored | High — combinatorial optimization | Moderate — pure software | Moderate — needs real WDN topology data | Direct (SDG 9.1) | Data access (municipal WDN topology) | Not shortlisted — data access risk too high |
| Idea 5: Cold Chain | Strong — ₹92K crore annual loss | Moderate — Arrhenius models are simple | Moderate — edge + commodity-specific | Low-Moderate — straightforward physics model | High — cheap sensors + ESP32 | High — controlled experiment with produce | Direct (SDG 9.1) | Mathematical depth too shallow for top score; spoilage validation needs time | Not shortlisted — math too thin |
| Ideas 4, 6–14 | Varying | Varying | Varying | Varying | Varying | Varying | Varying | Various | Not shortlisted — weaker combination of gap + feasibility |

---

## 10. Stress Test — Top 3

### 10.1 Stress Test: Idea 2 — Bearing TinyML

**1. Why does this problem matter?**
Unplanned downtime from bearing failures costs Indian MSMEs an estimated ₹1.5L/day. Commercial monitoring systems cost ₹5L+, creating a massive affordability gap.

**2. Why aren't existing solutions sufficient?**
[ESTABLISHED] CWRU-trained models degrade on variable-speed real machines. [ESTABLISHED] Commercial systems are unaffordable for MSMEs. [INFERENCE] Simple threshold-based vibration alerts miss incipient faults.

**3. What exactly is our contribution?**
An end-to-end validated pipeline: MEMS sensor → order-tracking preprocessing → MMD-adapted 1D-CNN → INT8 inference on ESP32. The contribution is *integration and validation*, not any single component.

**4. Has someone already done essentially the same thing?**
**Partially.** ESP32 + MEMS bearing diagnosis systems exist at similar price points in India. Domain adaptation for bearing faults is actively researched. The specific combination of order-tracking + MMD + TinyML on ESP32 for variable-speed conditions has not been found as a single validated system, but the components are all published.

**5. What is mathematically different?**
Nothing. Order tracking, MMD, and 1D-CNN are all standard. The mathematics serves the engineering, not the other way around.

**6. What is experimentally different?**
Validating the pipeline on lab-collected variable-speed MEMS data + comparing ablation variants. This experimental validation is the actual contribution.

**7. What is the baseline?**
CWRU-trained CNN on raw FFT features, tested on variable-speed data.

**8. What measurable improvement are we testing?**
F1-score improvement on variable-speed data (D vs. A2 in our experimental design).

**9. Can students actually build this?**
Yes, with caveats. ESP32 + MEMS is beginner-friendly. TFLite deployment is well-documented. Order tracking implementation requires signal processing knowledge. MMD loss implementation requires some PyTorch/TensorFlow proficiency.

**10. What happens if our main ML model fails?**
If the CNN doesn't fit ESP32 memory → use simpler features (statistical features + SVM). If domain adaptation doesn't improve accuracy → the project still demonstrates the *problem* (domain shift) and quantifies it, which is valuable.

**11. What data do we need?**
CWRU dataset (free) + lab-collected variable-speed vibration data (self-collected).

**12. What assumptions could invalidate the project?**
- ADXL345 noise floor may swamp bearing fault signatures on small motors (< 1 HP)
- Lab motor faults may not represent real MSME conditions
- Tachometer signal requirement may add impractical complexity

**13. What is the weakest part of the proposal?**
The novelty claim. "Combining known techniques" is a valid criticism. The response must be: "The combination hasn't been validated end-to-end under these constraints, and the validation is the contribution."

**14. What criticism could an evaluator make?**
"This is an integration project, not a research project." This is partially valid. Frame as engineering validation study, not algorithmic innovation.

**15. What evidence would defeat our proposal?**
A published paper that already combines order-tracking + domain adaptation + TinyML for variable-speed bearing diagnosis on a microcontroller. My search did not find one, but search limitations apply.

#### Why this project could fail
- MEMS sensor resolution insufficient for small motor bearing faults
- ESP32 memory cannot hold even the quantized model
- Order tracking requires a tachometer/encoder signal that adds cost and complexity
- Domain adaptation improvement is marginal (<5 pp), making the paper/demo unconvincing

#### How to redesign before implementation
1. **Drop the "first" and "novel" language.** Call it a "validated integration study" or "end-to-end deployment study."
2. **Verify ADXL345 can detect bearing fault frequencies** on your specific motor BEFORE committing to the full project. Run a 1-day feasibility test.
3. **Plan for order tracking WITHOUT a tachometer** — use instantaneous frequency estimation from the vibration signal itself (less accurate but simpler). Have this as a fallback.
4. **Set minimum success criteria:** If F1 > 80% on variable-speed data with < 200ms inference on ESP32, the project succeeds. If F1 < 70%, pivot to reporting the negative result (domain shift characterization study).
5. **Use leakage-free CWRU evaluation** — this alone differentiates from many published results.

---

### 10.2 Stress Test: Idea 3 — Energy Scheduling

**1. Why does this problem matter?**
Indian MSMEs spend 15–25% of operating costs on electricity. ToU tariffs create an optimization opportunity that manual scheduling ignores.

**2. Why aren't existing solutions sufficient?**
[ESTABLISHED] Commercial MES/ERP systems are unaffordable for MSMEs. [ESTABLISHED] Manual scheduling ignores energy costs. [INFERENCE] No published model uses Indian tariff data.

**3. What exactly is our contribution?**
An MILP model parameterized with Indian ToU tariff data and (ideally) empirically measured machine energy profiles, demonstrating quantifiable savings on realistic problem instances.

**4. Has someone already done essentially the same thing?**
**Algorithmically, yes.** Bi-objective MILP with machine-state energy is standard in OR. The specific parameterization with Indian tariffs is the differentiator. This is a narrow contextual gap.

**5. What is mathematically different?**
Nothing in the formulation. The parameters are different (Indian tariffs, MSME machine profiles).

**6-7. Baseline?**
FCFS and SPT — standard and defensible.

**9. Can students actually build this?**
Yes. PuLP is accessible. MILP formulation requires OR coursework, but textbook-level.

**10. What happens if our main approach fails?**
If MILP is intractable for larger instances → NSGA-II fallback is planned. If energy savings are marginal → the project still produces a validated model with Pareto analysis.

**13. What is the weakest part?**
The novelty claim. "Standard MILP with Indian parameters" is accurate and hard to rebut.

**14. What criticism could an evaluator make?**
"Where is the hardware? Where is the innovation?" A software-only scheduling tool may score poorly on Prototype Demonstration Innovation criterion.

#### Why this project could fail
- Energy savings may be marginal if tariff differential is small (some states have flat tariffs)
- Software-only prototype may score poorly on "Innovation" and "Usability" in Phase III
- Evaluator sees it as "applying existing technique with different data" — low innovation score

#### How to redesign before implementation
1. **Add a hardware component:** Connect the PZEM-004T power meter to a live machine, show real-time power monitoring feeding into the scheduler. This transforms the demo.
2. **Build a polished web UI** with interactive Gantt charts and energy cost visualizations.
3. **Frame as "decision support tool for MSME energy managers"** — emphasize usability and practical impact.
4. **Select a state with high ToU differential** (e.g., Maharashtra or Tamil Nadu) to maximize demonstrated savings.
5. **If possible, get even 1 day of real MSME data** for a case study.

---

### 10.3 Stress Test: Idea 15 — IAQ MPC

**1. Why does this problem matter?**
Indian workshop workers face PM2.5 exposure 5–20× above OSHA limits. Always-on ventilation wastes energy.

**3. What exactly is our contribution?**
MPC-based ventilation control for industrial workshops with zone-based pollutant modeling, demonstrated with low-cost sensors.

**4. Has someone already done essentially the same thing?**
MPC for IAQ in buildings: **yes, extensively.** MPC for cleanrooms: **yes** (Liverpool, 2024). MPC for small workshops specifically: **not found**, but the technical difference from existing work is the application domain, not the control theory.

**10. What happens if system identification fails?**
The project is in serious trouble. Without a good dynamic model, MPC reduces to a glorified PID controller, and the mathematical contribution evaporates.

**13. What is the weakest part?**
System identification in a turbulent, open workshop environment. Linear state-space models may be a poor fit for real workshop airflow.

#### Why this project could fail
- Linear state-space model doesn't capture turbulent workshop dynamics → poor prediction → MPC underperforms threshold control
- Sensor calibration drift over multi-hour experiments → noisy state estimates → MPC instability
- Physical setup takes too long → insufficient time for MPC development
- MPC computation is too slow for ESP32 → need Raspberry Pi or laptop, reducing "edge" claim

#### How to redesign before implementation
1. **Start with system identification FIRST** — before committing to MPC. If you can't get a usable model in 2 weeks, pivot.
2. **Use a simplified lab setup** — a sealed room with a controllable smoke source, not a real workshop.
3. **Have PID control as a comparison baseline** — if MPC doesn't clearly beat PID, the project's value diminishes.
4. **Run MPC on a laptop, not ESP32** — be honest that edge deployment is future work.
5. **Use do-mpc library** — it's well-documented and handles the QP solver internally.

---

## 11. Recommended Project Architecture — Idea 2 (Bearing TinyML)

### 11.1 Final Problem Statement

**[KNOWN FACT]** Bearing failures cause 40–50% of all rotating machinery breakdowns. Indian MSMEs cannot afford commercial monitoring systems (₹5L+/unit).

**[KNOWN FACT]** ML models trained on constant-speed benchmark datasets (CWRU) degrade significantly when deployed on real machines with variable speeds and loads (domain shift).

**[OUR DESIGN]** We propose a low-cost (<₹3000) end-to-end pipeline that addresses this domain shift through physics-informed preprocessing (order tracking) and statistical domain alignment (MMD), deployed as an INT8-quantized 1D-CNN on ESP32 for real-time edge inference.

### 11.2 Existing Solution Landscape

| Solution | Accuracy | Cost | Variable-Speed Support | Edge-Deployable |
|---|---|---|---|---|
| Commercial systems (SKF, B&K) | >95% | ₹5L+ | Yes | Yes |
| CWRU-trained CNNs (literature) | >95% on CWRU | Software only | No | Desktop only |
| ESP32 + MEMS (Indian projects) | ~90% on fixed speed | ~₹2000 | No | Yes |
| Domain adaptation CNNs (2024) | >90% cross-domain | Software only | Yes (desktop) | No |
| **Our proposal** | >85% (hypothesis) | ~₹2500 | Yes (hypothesis) | Yes |

### 11.3 Precisely Defined Gap

Existing low-cost ESP32-based systems do not address speed-induced domain shift. Existing domain adaptation methods are validated on desktops, not microcontrollers. The gap is: **no validated end-to-end pipeline from variable-speed MEMS data → speed-invariant features → domain-adapted model → microcontroller inference.**

This is a **system integration and validation gap**, not an algorithmic gap.

### 11.4 What Is Actually Novel

| Novelty Type | Claim | Confidence |
|---|---|---|
| Algorithmic | None — all components are standard | N/A |
| Mathematical | None — order tracking, MMD, CNN are textbook | N/A |
| **System-level** | End-to-end pipeline integrating order tracking + MMD + INT8 CNN on ESP32 | Moderate — no single paper combines all three for bearing faults |
| **Experimental** | Validation on self-collected variable-speed MEMS data with leakage-free evaluation | Moderate — addresses documented weaknesses in CWRU evaluations |
| Contextual | Low-cost deployment for Indian MSME motors | Low — similar price-point systems exist |

### 11.5 System Architecture

```
┌─────────────┐    I2C    ┌─────────────┐    WiFi    ┌─────────────┐
│  ADXL345     │──────────│   ESP32      │──────────│  Dashboard   │
│  (3-axis     │          │  - Sampling  │          │  (optional)  │
│  accel.)     │          │  - Order     │          │              │
│              │          │    Tracking  │          │              │
│              │          │  - CNN       │          │              │
│              │          │    Inference │          │              │
│              │          │  - OLED      │          │              │
│              │          │    Display   │          │              │
└─────────────┘          └─────────────┘          └─────────────┘
                               │
                          ┌────┴────┐
                          │  OLED   │
                          │ Display │
                          │ Normal/ │
                          │ IR/OR/  │
                          │ Ball    │
                          └─────────┘
```

### 11.6 Hardware BOM

| Component | Purpose | Qty | Unit Cost (₹) | Total (₹) |
|---|---|---|---|---|
| ESP32-WROOM-32 | Main controller | 1 | 500 | 500 |
| ADXL345 | 3-axis MEMS accelerometer | 1 | 200 | 200 |
| SSD1306 OLED | Status display | 1 | 200 | 200 |
| IR optocoupler (speed sensor) | Tachometer for order tracking | 1 | 100 | 100 |
| Breadboard + wires | Prototyping | 1 | 200 | 200 |
| USB power bank | Power supply | 1 | 300 | 300 |
| **Total** | | | | **₹1500** |

Lab motor with VFD: borrowed from lab (₹0 additional).

### 11.7 Software Architecture

```
Training Pipeline (Python, laptop):
  CWRU Dataset → Preprocessing → Order Tracking → Feature Extraction
  Lab Dataset → Preprocessing → Order Tracking → Feature Extraction
  ↓
  1D-CNN Training with L_class + λ·MMD²
  ↓
  TFLite Conversion → INT8 Quantization → .tflite model file
  ↓
  ESP32 Deployment via TFLite Micro

Inference Pipeline (ESP32):
  ADXL345 (I2C, 1600 Hz sampling)
  → Buffer (2048 samples)
  → Angular resampling (using tachometer signal)
  → Order spectrum computation (FFT of angular-resampled signal)
  → Feature vector extraction (subband energies)
  → 1D-CNN inference (TFLite Micro, INT8)
  → Classification result → OLED display + WiFi alert
```

### 11.8 Data Pipeline

1. **CWRU data:** Download from CWRU Bearing Data Center. 4 fault classes × 4 loads × 2 sampling rates. Use 12k sampling rate data.
2. **Lab data:** Collect from motor at 3–5 speed settings, 3 load conditions. 30-second recordings per condition. Healthy + 3 fault types (if available; otherwise healthy + 1–2 induced fault conditions).
3. **Preprocessing:** Resample to fixed angular domain using tachometer signal. Extract order spectrum. Compute subband energy features.
4. **Split:** Train/validation/test with **strict separation by recording session** (no data leakage).

### 11.9 Algorithm Pipeline

1. **Input:** Raw 3-axis vibration signal + tachometer pulse signal
2. **Angular resampling:** Convert time-domain signal to angle-domain using interpolation
3. **Order spectrum:** FFT of angle-domain signal → frequency axis in orders (multiples of shaft speed)
4. **Feature extraction:** Energy in predefined order bands corresponding to bearing fault frequencies (BPFO, BPFI, BSF, FTF)
5. **Classification:** 1D-CNN (3 conv layers + 2 dense layers, ~10K parameters) with softmax output
6. **Domain adaptation (training only):** MMD loss between source (CWRU) and target (lab) feature representations
7. **Quantization:** Post-training INT8 quantization for ESP32 deployment
8. **Inference:** TFLite Micro interpreter on ESP32

### 11.10 Evaluation Protocol

| Experiment | Condition | Purpose |
|---|---|---|
| Exp 1 | Train on CWRU, test on CWRU (same speed) | Establish ceiling accuracy |
| Exp 2 | Train on CWRU, test on lab variable-speed (no adaptation) | Quantify domain shift |
| Exp 3 | Same as Exp 2 with order-tracking features | Measure preprocessing benefit |
| Exp 4 | Same as Exp 2 with MMD adaptation (raw FFT) | Measure DA benefit |
| Exp 5 | Order tracking + MMD (full system) | Measure combined benefit |
| Exp 6 | Exp 5 quantized to INT8 on ESP32 | Measure quantization loss |

### 11.11 Expected Failure Modes

| Failure Mode | Probability | Impact | Mitigation |
|---|---|---|---|
| ADXL345 noise floor too high for small motor faults | Medium | High | Pre-test with known-faulty bearing before committing |
| ESP32 memory insufficient for CNN | Low-Medium | High | Reduce model to ~5K parameters; use statistical features + SVM as fallback |
| Order tracking requires tachometer (adds complexity) | Medium | Medium | Use instantaneous frequency estimation as fallback |
| Domain adaptation improvement is marginal | Medium | Medium | Report ablation honestly; the negative result (characterizing the problem) is still publishable |
| Lab motor faults not representative of real MSMEs | High | Low | Acknowledge limitation; focus on methodology validation |

### 11.12 Timeline

| Week | Task | Deliverable |
|---|---|---|
| 1–2 | Literature review; hardware procurement; CWRU baseline | Phase I report: Problem definition + methodology |
| 3–4 | ADXL345 + ESP32 integration; lab data collection setup | Working data acquisition system |
| 5–6 | Data collection (variable speeds); CWRU model training | Dataset + baseline model |
| 7–8 | Order tracking implementation; MMD adaptation; ablation | Trained models, ablation results |
| 9–10 | INT8 quantization; ESP32 deployment; edge testing | Working prototype |
| 11–12 | Statistical analysis; report writing; poster/PPT | Final report + presentation |

### 11.13 SDG 9 Mapping

| SDG 9 Target | Connection | Evidence |
|---|---|---|
| **9.3** — Increase access of small-scale industrial enterprises to financial services and technology | Direct — provides affordable (<₹3000) predictive maintenance technology to MSMEs | Cost comparison with commercial systems |
| **9.4** — Upgrade infrastructure and retrofit industries for sustainability | Supportive — reduces unplanned downtime and waste from unexpected failures | Downtime cost reduction analysis |
| **9.b** — Support domestic technology development in developing countries | Supportive — Indian-developed solution using locally available components | Hardware sourcing from Indian suppliers |

### 11.14 What We Can Demonstrate Physically

1. Attach the sensor device to a running motor
2. Show real-time classification on OLED display (Normal / Inner Race / Outer Race / Ball)
3. Change motor speed during demo → show that classification remains stable (speed invariance)
4. Show WiFi alert on phone/laptop dashboard
5. Show ablation results on poster: accuracy bar charts with/without order tracking, with/without DA

### 11.15 What Evidence We Need Before Claiming Success

- [ ] F1 > 85% on variable-speed lab data (full system, condition D)
- [ ] F1 improvement > 10 pp from domain adaptation (D vs. A2)
- [ ] F1 improvement > 5 pp from order tracking (B vs. A2)
- [ ] Inference time < 200ms on ESP32
- [ ] Model size < 100KB (INT8)
- [ ] Quantization accuracy loss < 5 pp
- [ ] Leakage-free evaluation protocol used

---

## 12. Final GO / MODIFY / REJECT Decision Gate

### Idea 2 — Edge-TinyML Bearing Fault Diagnosis

| Gate | Requirement | Status | Evidence / Reason |
|---|---|---|---|
| Real problem | Evidence of actual need | ✅ PASS | MSME downtime costs documented by MSME Ministry; affordability gap is real |
| Rubric fit | Strong alignment with all phases | ✅ PASS | Hardware + software prototype (Phase III); literature context (Phase I); tool integration (Phase II) |
| Research foundation | Sufficient credible literature | ✅ PASS | 10+ relevant papers identified across bearing DA, TinyML, CWRU benchmarking |
| Research gap | Specific and defensible | ⚠️ CONDITIONAL | Gap exists but is narrower than originally claimed. Must reframe as "integration and validation study" |
| Novelty | Contribution distinguishable | ⚠️ CONDITIONAL | System-level + experimental novelty. Must NOT claim algorithmic novelty |
| Mathematics | Valid and meaningful | ✅ PASS | Valid applied mathematics. Not the core contribution but supports engineering |
| Data | Obtainable | ✅ PASS | CWRU free; lab data self-collected |
| Prototype | Buildable | ✅ PASS | BOM ~₹1500; well-documented components |
| Baseline | Clear comparison | ✅ PASS | CWRU baseline + ablation variants defined |
| Experiment | Measurable validation | ✅ PASS | 6-experiment protocol with ablation |
| Metrics | Objective evaluation | ✅ PASS | F1-score, inference time, model size — all objective |
| Cost | Within student budget | ✅ PASS | ~₹1500–3000 |
| Time | Academically feasible | ✅ PASS | 12-week timeline with buffer |
| SDG 9 | Direct connection | ✅ PASS | SDG 9.3 (MSME technology access) |
| Risk | Manageable | ⚠️ CONDITIONAL | Motor/bearing access is the critical dependency |

**Overall: ⚠️ MODIFY then GO**

---

### What Must Be True Before We Commit to This Project

**Pre-commitment verification checklist:**

- [ ] **CRITICAL:** Verify access to a lab motor with variable speed control (VFD or multi-speed winding)
- [ ] **CRITICAL:** Verify ADXL345 can detect bearing fault characteristic frequencies on the available motor (1-day feasibility test: mount sensor, run FFT, look for BPFO/BPFI peaks)
- [ ] **CRITICAL:** Verify ESP32 can run a minimal 1D-CNN (~5K parameters, INT8) within memory constraints (1-day test with TFLite Micro hello world)
- [ ] **IMPORTANT:** Obtain or prepare a bearing with known damage for controlled experiments (either purchase a damaged bearing set or plan to induce damage on a spare bearing)
- [ ] **IMPORTANT:** Source or fabricate a tachometer signal (IR optocoupler + reflective tape on shaft is simplest)
- [ ] **NICE-TO-HAVE:** Identify fallback experiment plan if order tracking proves too complex (use raw vibration at multiple known speeds as separate domains)

**Commit/No-commit decision point: After completing the first 3 critical items (estimated 2–3 days of lab work).**

If any critical item fails:
- ADXL345 can't detect faults → Consider upgrading to IIS3DWB industrial accelerometer (~₹2000) or pivot to Idea 3
- ESP32 can't run the model → Use STM32 or Raspberry Pi Pico W (higher capability)
- No motor with VFD → Pivot to Idea 3 (Energy Scheduling) which has no hardware dependencies

---

## 13. Immediate Next Steps

| Priority | Action | Timeline | Owner |
|---|---|---|---|
| 1 | **Feasibility test:** Mount ADXL345 on lab motor, collect 30s data, run FFT, verify bearing frequencies visible | Day 1–2 | Hardware lead |
| 2 | **Feasibility test:** Deploy minimal TFLite model on ESP32, verify memory + inference speed | Day 1–2 | Software lead |
| 3 | **Literature deep-dive:** Search IEEE Xplore and ACM DL specifically for "order tracking + domain adaptation + microcontroller" to verify no exact prior art | Day 1–3 | Research lead |
| 4 | **Decision gate:** If all 3 pass → commit to Idea 2. If any fail → pivot to Idea 3 (Energy Scheduling) with hardware addon | Day 3 | Full team |
| 5 | **If GO:** Begin Phase I report (problem statement, literature review, methodology, flow chart) | Week 1–2 | Full team |
| 6 | **If GO:** Order remaining hardware components (OLED, IR optocoupler, breadboard) | Day 4 | Hardware lead |
| 7 | **Rewrite all novelty claims** per this audit — remove "first," "novel," and unsupported percentages | Immediately | Full team |

> [!IMPORTANT]
> **The single most important action is the 2-day feasibility test.** Do NOT spend weeks on literature review and report writing before verifying that the sensor can detect the signals you need. Hardware first, paper second.

---

## Appendix: Note on Scoring and Confidence

This audit was conducted with the following limitations:
- Web search was used rather than direct IEEE Xplore / ACM DL / Scopus access. Some relevant papers may have been missed.
- "Potentially unexplored" classifications carry LOW confidence — absence of evidence is not evidence of absence.
- Cost estimates are based on Indian online retailer pricing as of 2026 and may vary.
- Improvement predictions in the original document have been deliberately left as **hypotheses to test**, not expected results.
- All "established" classifications are based on widely-cited figures in publicly accessible reports and should be verified against primary sources before inclusion in the final report.
