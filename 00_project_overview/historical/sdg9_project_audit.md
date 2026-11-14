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
