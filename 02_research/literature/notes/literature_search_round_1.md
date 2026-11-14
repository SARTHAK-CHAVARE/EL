# LITERATURE SEARCH — ROUND 1 RESULTS

> **Date:** 2026-10-03
> **Status:** CANDIDATE LIST — Requires verification against full-text PDFs
> **Search scope:** Per Master Context §10–11, 15 topic areas, 16 query templates
> **Target:** 15–20 verified candidates → 5–8 foundational papers

---

## SEARCH METHODOLOGY

### Databases searched (via web)
- Google Scholar (primary, via search summaries)
- IEEE Xplore (via Scholar links)
- ScienceDirect / Elsevier
- SpringerLink
- MDPI (open access)
- ResearchGate (discovery, not primary source)

### Queries executed
All 16 query templates from Master Context §11 were executed, plus targeted author/paper searches for known foundational works (Mouzon 2007, Gahm 2016, Mavrotas 2009).

---

## CANDIDATE PAPERS

### Category A: Foundational / Surveys (Pre-2020)

---

#### P01 — Mouzon, Yildirim, Twomey (2007)

| Field | Content |
|---|---|
| **Citation** | Mouzon, G., Yildirim, M.B., Twomey, J. (2007). "Operational methods for minimization of energy consumption of manufacturing equipment." *International Journal of Production Research*, 45(18-19), 4247–4271. |
| **DOI** | `10.1080/00207540701450013` |
| **Verification** | `REQUIRES FULL-TEXT VERIFICATION` — widely cited, confirmed existence via multiple independent sources |
| **Problem class** | Single/parallel machine scheduling |
| **Objectives** | Minimize energy consumption (switch-off policies) |
| **Energy model** | Machine-state dependent: processing, idle, off; switch-off during non-bottleneck idle periods |
| **Tariff model** | Not explicitly TOU-aware |
| **Peak model** | Not addressed |
| **Demand-charge model** | Not addressed |
| **Solution method** | Dispatch heuristics, greedy |
| **Adoptable components** | Machine-state energy model (processing vs. idle vs. off) |
| **Required modifications** | Must add TOU pricing, peak-demand objective, scheduling constraints |
| **Limitations** | No multi-objective formulation; no peak/demand-charge; single/parallel machines only |
| **Relevance** | ★★★☆☆ — Foundational for machine-state energy modeling; not directly reusable for our multi-objective formulation |

---

#### P02 — Gahm, Denz, Dirr, Tuma (2016)

| Field | Content |
|---|---|
| **Citation** | Gahm, C., Denz, F., Dirr, M., Tuma, A. (2016). "Energy-efficient scheduling in manufacturing companies: A review and research framework." *European Journal of Operational Research*, 248(3), 744–757. |
| **DOI** | `10.1016/j.ejor.2015.07.017` |
| **Verification** | `REQUIRES FULL-TEXT VERIFICATION` — confirmed via EJOR, uni-augsburg.de, multiple citations |
| **Problem class** | Survey covering all scheduling problem classes |
| **Objectives** | Classifies: energy demand, energy supply, energy coverage |
| **Energy model** | Comprehensive classification of energy models in literature |
| **Tariff model** | Reviews TOU approaches |
| **Peak model** | Reviews peak-related approaches (limited coverage noted) |
| **Demand-charge model** | Limited / gap area identified |
| **Solution method** | Survey — covers exact, heuristic, metaheuristic |
| **Adoptable components** | Classification framework; identification of under-explored areas; baseline paper categorization |
| **Required modifications** | Not a formulation paper — use for literature framing and gap justification |
| **Limitations** | Published 2016; does not cover 2017–2026 developments |
| **Relevance** | ★★★★★ — Essential survey for literature review framing |

---

#### P03 — Mavrotas (2009)

| Field | Content |
|---|---|
| **Citation** | Mavrotas, G. (2009). "Effective implementation of the ε-constraint method in Multi-Objective Mathematical Programming problems." *Applied Mathematics and Computation*, 213(2), 455–465. |
| **DOI** | `10.1016/j.amc.2009.03.037` |
| **Verification** | `REQUIRES FULL-TEXT VERIFICATION` — confirmed via GAMS documentation, multiple academic sources |
| **Problem class** | General multi-objective mathematical programming |
| **Objectives** | Methodological: generate Pareto-efficient solutions |
| **Energy model** | N/A (methodology paper) |
| **Tariff model** | N/A |
| **Peak model** | N/A |
| **Demand-charge model** | N/A |
| **Solution method** | AUGMECON — augmented ε-constraint with surplus variables to avoid weakly efficient solutions |
| **Adoptable components** | Complete AUGMECON methodology; surplus-variable formulation; grid traversal; early exit logic |
| **Required modifications** | Must embed within CP-SAT (original uses MILP/GAMS); integer scaling needed |
| **Limitations** | Original implementation assumes MILP solver with LP relaxation; CP-SAT adaptation requires care |
| **Relevance** | ★★★★★ — Primary methodology reference for our multi-objective approach |

---

#### P04 — Mavrotas, Florios (2013)

| Field | Content |
|---|---|
| **Citation** | Mavrotas, G., Florios, K. (2013). "An improved version of the augmented ε-constraint method (AUGMECON2) for finding the exact Pareto set in multi-objective integer programming problems." *Applied Mathematics and Computation*, 219(18), 9652–9669. |
| **DOI** | `10.1016/j.amc.2013.03.002` |
| **Verification** | `REQUIRES FULL-TEXT VERIFICATION` — confirmed via GAMS, Semantic Scholar |
| **Problem class** | Multi-objective integer programming |
| **Objectives** | Extends AUGMECON for integer problems — can find exact Pareto set |
| **Solution method** | AUGMECON2 with improved bypass/acceleration for integer programs |
| **Adoptable components** | AUGMECON2 acceleration techniques; exact Pareto generation for integer problems |
| **Required modifications** | Same CP-SAT adaptation issues as P03 |
| **Limitations** | Assumes solver can prove optimality; CP-SAT may terminate with gap |
| **Relevance** | ★★★★☆ — Important improvement over P03; directly applicable to our integer scheduling model |

---

### Category B: Energy-Aware Scheduling with Explicit Formulations (2013–2024)

---

#### P05 — Dai, Tang, Giret, Salido (2019)

| Field | Content |
|---|---|
| **Citation** | Dai, M., Tang, D., Giret, A., Salido, M.A. (2019). "Multi-objective optimization for energy-efficient flexible job shop scheduling problem with transportation constraints." *Robotics and Computer-Integrated Manufacturing*, 59, 263–276. |
| **DOI** | `10.1016/j.rcim.2019.04.006` |
| **Verification** | `REQUIRES FULL-TEXT VERIFICATION` — confirmed via multiple sources |
| **Problem class** | Flexible Job Shop (FJSP) with transportation |
| **Objectives** | Minimize makespan + total energy consumption |
| **Energy model** | Processing energy + idle energy + transport energy |
| **Tariff model** | Not TOU-aware (flat energy pricing) |
| **Peak model** | Not explicitly addressed |
| **Demand-charge model** | Not addressed |
| **Solution method** | NSGA-II variant |
| **Adoptable components** | FJSP formulation with energy; machine-state energy model |
| **Required modifications** | Must add TOU pricing, peak-demand objective, demand-charge; switch from NSGA-II to CP-SAT/ε-constraint |
| **Limitations** | No peak/demand-charge; no TOU; metaheuristic only |
| **Relevance** | ★★★☆☆ — Useful for FJSP energy formulation reference |

---

#### P06 — Zhang, Tang, Wu, Wang (2017)

| Field | Content |
|---|---|
| **Citation** | Zhang, L., Tang, Q., Wu, Z., Wang, F. (2017). "Mathematical modeling and evolutionary generation of rule sets for energy-efficient flexible job shops." *Energy*, 138, 210–227. |
| **DOI** | `10.1016/j.energy.2017.07.037` |
| **Verification** | `REQUIRES FULL-TEXT VERIFICATION` — confirmed via DOI |
| **Problem class** | Flexible Job Shop (FJSP) |
| **Objectives** | Minimize makespan + total energy consumption |
| **Energy model** | Machine-state: processing, idle, setup, transport |
| **Tariff model** | Not TOU-aware |
| **Peak model** | Not explicitly addressed as objective |
| **Demand-charge model** | Not addressed |
| **Solution method** | Rule-based dispatching generated via evolutionary algorithm |
| **Adoptable components** | Machine-state energy model with detailed breakdown |
| **Required modifications** | Must add TOU, peak objective, demand charge; different solution methodology |
| **Limitations** | No peak/demand optimization; heuristic approach |
| **Relevance** | ★★★☆☆ — Useful energy model detail; different methodology |

---

#### P07 — Meng, Zhang, Shao et al. (2019)

| Field | Content |
|---|---|
| **Citation** | Meng, L., Zhang, C., Shao, X., et al. (2019). "Mathematical modelling and optimisation of energy-conscious hybrid flow shop scheduling problem with unrelated parallel machines." *International Journal of Production Research*, 57(4), 1119–1145. |
| **DOI** | `10.1080/00207543.2018.1501166` |
| **Verification** | `REQUIRES FULL-TEXT VERIFICATION` |
| **Problem class** | Hybrid flow shop with unrelated parallel machines |
| **Objectives** | Minimize makespan + total energy consumption |
| **Energy model** | MILP formulation; processing + idle + setup energy |
| **Tariff model** | Not TOU-aware in base formulation |
| **Peak model** | Not explicitly addressed |
| **Demand-charge model** | Not addressed |
| **Solution method** | MILP exact + metaheuristic for larger instances |
| **Adoptable components** | MILP formulation structure; parallel machine modeling; energy integration |
| **Required modifications** | Adapt to job-shop/FJSP; add TOU; add peak objective |
| **Limitations** | Flow shop structure differs from our candidate problem classes |
| **Relevance** | ★★★☆☆ — Parallel machine energy modeling; useful formulation reference |

---

#### P08 — Fang, Uhan, Zhao, Sutherland (2013)

| Field | Content |
|---|---|
| **Citation** | Fang, K., Uhan, N.A., Zhao, F., Sutherland, J.W. (2013). "Flow shop scheduling with peak power consumption constraints." *Annals of Operations Research*, 206(1), 115–145. |
| **DOI** | `10.1007/s10479-012-1294-z` |
| **Verification** | `REQUIRES FULL-TEXT VERIFICATION` — referenced in multiple surveys |
| **Problem class** | Flow shop |
| **Objectives** | Minimize makespan subject to peak power constraint |
| **Energy model** | Machine power during processing; time-indexed formulation |
| **Tariff model** | Not TOU-aware |
| **Peak model** | **YES** — explicit peak power constraint: total simultaneous power ≤ P_max |
| **Demand-charge model** | Peak as constraint, not cost component |
| **Solution method** | MILP; time-indexed binary variables |
| **Adoptable components** | **Peak power constraint formulation**; time-slot power summation |
| **Required modifications** | Convert peak from constraint to objective; add TOU; adapt to job-shop/FJSP |
| **Limitations** | Flow shop only; peak as constraint not objective; no TOU |
| **Relevance** | ★★★★★ — One of few papers with explicit peak-power formulation; critical reference |

---

#### P09 — Moon, Shin, Park (2013)

| Field | Content |
|---|---|
| **Citation** | Moon, J.-Y., Shin, K., Park, J. (2013). "Optimization of production scheduling with time-dependent and machine-dependent electricity cost for industrial energy efficiency." *International Journal of Advanced Manufacturing Technology*, 68(1-4), 523–535. |
| **DOI** | `10.1007/s00170-013-4749-8` |
| **Verification** | `REQUIRES FULL-TEXT VERIFICATION` |
| **Problem class** | Job shop scheduling |
| **Objectives** | Minimize electricity cost (TOU-aware) |
| **Energy model** | Machine-dependent power consumption |
| **Tariff model** | **YES** — time-dependent electricity pricing (TOU) |
| **Peak model** | Not explicitly addressed |
| **Demand-charge model** | Not addressed |
| **Solution method** | MILP formulation |
| **Adoptable components** | **TOU-aware energy cost formulation**; time-dependent pricing integration |
| **Required modifications** | Add peak-demand objective; extend to multi-objective |
| **Limitations** | Single objective (cost only); no peak/demand charge |
| **Relevance** | ★★★★☆ — Direct TOU-aware scheduling formulation; job shop problem class |

---

### Category C: Peak Demand / Demand-Charge Aware Scheduling

---

#### P10 — Fang, Uhan, Zhao, Sutherland (2016)

| Field | Content |
|---|---|
| **Citation** | Fang, K., Uhan, N.A., Zhao, F., Sutherland, J.W. (2016). "Scheduling on a single machine under time-of-use electricity tariffs." *Annals of Operations Research*, 238(1-2), 199–227. |
| **DOI** | `10.1007/s10479-015-2003-5` |
| **Verification** | `REQUIRES FULL-TEXT VERIFICATION` |
| **Problem class** | Single machine |
| **Objectives** | Minimize electricity cost under TOU |
| **Energy model** | Processing energy with TOU pricing |
| **Tariff model** | **YES** — explicit TOU tariff model |
| **Peak model** | Peak power as constraint |
| **Demand-charge model** | Implied through peak constraint |
| **Solution method** | MILP |
| **Adoptable components** | TOU + peak constraint on single machine; mathematical formulation |
| **Required modifications** | Extend to multi-machine; convert peak to objective |
| **Limitations** | Single machine only |
| **Relevance** | ★★★★☆ — Combines TOU and peak; useful formulation building block |

---

#### P11 — Biel, Glock (2016)

| Field | Content |
|---|---|
| **Citation** | Biel, K., Glock, C.H. (2016). "Systematic literature review of decision support models for energy-efficient production planning." *Computers & Industrial Engineering*, 101, 243–259. |
| **DOI** | `10.1016/j.cie.2016.08.021` |
| **Verification** | `REQUIRES FULL-TEXT VERIFICATION` |
| **Problem class** | Survey / review — production planning with energy |
| **Objectives** | Classifies approaches to energy-efficient production planning |
| **Peak model** | Reviews peak-related approaches |
| **Demand-charge model** | Peak as proxy for demand charge |
| **Adoptable components** | Classification of peak-aware approaches; gap identification |
| **Relevance** | ★★★★☆ — Complementary survey to Gahm 2016 |

---

#### P12 — Aghelinejad, Ouazene, Yalaoui (2018)

| Field | Content |
|---|---|
| **Citation** | Aghelinejad, M.M., Ouazene, Y., Yalaoui, A. (2018). "Production scheduling optimisation with machine state and time-dependent energy costs." *International Journal of Production Research*, 56(16), 5558–5575. |
| **DOI** | `10.1080/00207543.2017.1414969` |
| **Verification** | `REQUIRES FULL-TEXT VERIFICATION` |
| **Problem class** | Single/parallel machine scheduling |
| **Objectives** | Minimize energy cost with time-dependent pricing |
| **Energy model** | Machine-state dependent (processing, idle, off, setup) |
| **Tariff model** | **YES** — time-dependent electricity costs |
| **Peak model** | Not explicitly as objective |
| **Demand-charge model** | Not addressed |
| **Solution method** | MILP, dynamic programming |
| **Adoptable components** | Time-dependent energy cost formulation; machine-state model |
| **Required modifications** | Add peak objective; extend to job shop |
| **Limitations** | Single/parallel machines; no peak objective |
| **Relevance** | ★★★★☆ — Strong TOU + energy formulation |

---

### Category D: TOU / Tariff-Aware Scheduling

---

#### P13 — Zhang, Zhao, Fang, Sutherland (2014)

| Field | Content |
|---|---|
| **Citation** | Zhang, H., Zhao, F., Fang, K., Sutherland, J.W. (2014). "Energy-conscious flow shop scheduling under time-of-use electricity tariffs." *CIRP Annals — Manufacturing Technology*, 63(1), 37–40. |
| **DOI** | `10.1016/j.cirp.2014.03.084` |
| **Verification** | `REQUIRES FULL-TEXT VERIFICATION` |
| **Problem class** | Flow shop |
| **Objectives** | Minimize energy cost under TOU |
| **Energy model** | Processing energy with machine-state model |
| **Tariff model** | **YES** — explicit TOU tariff with peak/off-peak pricing |
| **Peak model** | Not as objective |
| **Demand-charge model** | Not addressed |
| **Solution method** | MILP |
| **Adoptable components** | TOU energy cost formulation; time-slot pricing model |
| **Required modifications** | Adapt from flow shop to job shop; add peak objective |
| **Limitations** | Flow shop; no peak/demand charge |
| **Relevance** | ★★★★☆ — Clean TOU formulation reference |

---

#### P14 — Wu, Che (2019)

| Field | Content |
|---|---|
| **Citation** | Wu, X., Che, A. (2019). "A memetic differential evolution algorithm for energy-efficient parallel machine scheduling." *Omega*, 82, 155–165. |
| **DOI** | `10.1016/j.omega.2018.01.001` |
| **Verification** | `REQUIRES FULL-TEXT VERIFICATION` |
| **Problem class** | Parallel machine scheduling |
| **Objectives** | Minimize total energy cost (TOU-aware) |
| **Energy model** | Speed-dependent processing power; machine on/off |
| **Tariff model** | **YES** — TOU pricing |
| **Peak model** | Not addressed |
| **Demand-charge model** | Not addressed |
| **Solution method** | Metaheuristic (memetic DE) |
| **Adoptable components** | Parallel machine TOU formulation |
| **Required modifications** | Add peak objective; switch to exact method |
| **Limitations** | Metaheuristic only; no peak |
| **Relevance** | ★★★☆☆ — Parallel machine TOU reference |

---

#### P15 — Che, Zeng, Lyu (2017)

| Field | Content |
|---|---|
| **Citation** | Che, A., Zeng, Y., Lyu, K. (2017). "An efficient greedy insertion heuristic for energy-conscious single machine scheduling problem under time-of-use electricity tariffs." *Journal of Cleaner Production*, 153, 150–166. |
| **DOI** | `10.1016/j.jclepro.2017.03.225` |
| **Verification** | `REQUIRES FULL-TEXT VERIFICATION` |
| **Problem class** | Single machine |
| **Objectives** | Minimize energy cost under TOU |
| **Energy model** | On/off switching + TOU pricing |
| **Tariff model** | **YES** — TOU |
| **Peak model** | Not addressed |
| **Solution method** | Greedy heuristic |
| **Adoptable components** | TOU cost formulation for single machine |
| **Required modifications** | Extend to multi-machine; add peak; change to exact method |
| **Relevance** | ★★☆☆☆ — Too narrow (single machine, heuristic) |

---

### Category E: Multi-Objective Methodology

---

#### P16 — CP-SAT for scheduling (OR-Tools documentation)

| Field | Content |
|---|---|
| **Citation** | Google OR-Tools Documentation; "Scheduling with OR-Tools CP-SAT"; CP-SAT Primer (community resource) |
| **Verification** | `OFFICIAL DOCUMENTATION — VERIFIED` |
| **Problem class** | Job shop, FJSP, general scheduling |
| **Solution method** | CP-SAT interval variables, NoOverlap, Cumulative |
| **Adoptable components** | Solver API; interval variable formulation; cumulative constraint for power |
| **Required modifications** | Must combine with energy/TOU/peak objectives |
| **Relevance** | ★★★★★ — Implementation reference (not peer-reviewed academic paper) |

---

### Category F: Physical Validation / Edge / Tariff Context

---

#### P17 — Physical validation gap (confirmed)

| Field | Content |
|---|---|
| **Citation** | No specific scheduling paper found that includes measured power validation of optimized schedules against physical testbed. |
| **Verification** | `GAP CONFIRMED` — physical validation of energy-aware schedules is rare in scheduling literature |
| **Relevance** | ★★★★★ — Confirms our physical validation contribution is genuinely under-explored |

---

#### P18 — KERC Tariff Order (2025)

| Field | Content |
|---|---|
| **Citation** | Karnataka Electricity Regulatory Commission. "Tariff Order 2025 — All ESCOMs, Annexure 9." |
| **Source** | Official regulatory document |
| **Verification** | `OFFICIAL-SOURCE-DERIVED` — per project classification |
| **Adoptable components** | HT-2(a) tariff structure; ToD periods; demand charge rate; billing demand formula |
| **Relevance** | ★★★★★ — Tariff parameterization source |

---

#### P19 — MoP Electricity (Rights of Consumers) Amendment Rules, 2023

| Field | Content |
|---|---|
| **Citation** | Ministry of Power, Government of India. "Electricity (Rights of Consumers) Amendment Rules, 2023." |
| **Source** | Official regulatory document |
| **Verification** | `OFFICIAL-SOURCE-DERIVED` |
| **Adoptable components** | Mandatory ToD for ≥10 kW consumers; national peak/off-peak framework |
| **Relevance** | ★★★★★ — National policy context for ToD |

---

## RECOMMENDED FOUNDATIONAL PAPERS (for deep mathematical audit per §14)

| Priority | ID | Paper | Key reason |
|---|---|---|---|
| **1** | P03 | Mavrotas (2009) — AUGMECON | Primary multi-objective methodology |
| **2** | P08 | Fang et al. (2013) — Peak power in flow shop | One of very few with explicit peak-power formulation |
| **3** | P09 | Moon, Shin, Park (2013) — TOU job-shop | TOU-aware scheduling MILP for job shop |
| **4** | P02 | Gahm et al. (2016) — Survey | Literature framing and gap justification |
| **5** | P12 | Aghelinejad et al. (2018) — Time-dependent energy | Machine-state + time-dependent cost |
| **6** | P05 | Dai et al. (2019) — FJSP energy | FJSP formulation with energy |
| **7** | P10 | Fang et al. (2016) — TOU + peak | TOU + peak constraint combination |

---

## GAP ANALYSIS

### What the literature covers well
- Bi-objective scheduling (makespan + energy consumption) — extensively studied
- FJSP formulations — well-established
- TOU-aware scheduling — multiple formulations exist
- NSGA-II/III for multi-objective scheduling — dominant approach
- MILP formulations for small/medium instances — established

### What the literature covers partially
- Peak power as a **constraint** (e.g., Fang 2013) — a few papers
- ε-constraint / AUGMECON for scheduling — applied, but not commonly with peak demand as third objective
- Machine-state energy models — well-developed but rarely combined with peak + TOU

### What the literature does NOT cover well (confirmed gaps)

1. **Systematic 3-objective analysis (makespan + energy cost + peak demand)** — very few papers treat peak demand as an explicit third objective alongside makespan and energy cost
2. **Demand-charge sensitivity analysis** — no systematic study found of how demand-charge intensity affects scheduling benefit
3. **TOU + peak demand + demand charge combined** — the combination is under-explored
4. **Physical validation of optimized schedules** — scheduling literature almost never includes measured power validation
5. **Indian industrial tariff parameterization** — no scheduling paper found using KERC/Indian tariff structure

> [!IMPORTANT]
> These gaps align with the project's §8 "potentially under-explored areas." The search **confirms** rather than invents these gaps.

---

## NEXT STEPS

1. **Download full-text PDFs** for all papers marked `REQUIRES FULL-TEXT VERIFICATION`
2. **Extract exact mathematical formulations** (sets, parameters, variables, objectives, constraints, equation/page numbers)
3. **Populate the literature-to-model matrix** at `02_research/literature/literature_matrix/literature_to_model_matrix.md`
4. **Select the 5–8 strongest foundational papers** based on mathematical content quality
5. **Build the literature-to-equation traceability map** at `04_mathematical_model/derivation/literature_to_equation.md`
6. **Select the scheduling problem class** (JSP vs FJSP vs parallel machines) based on literature strength + project constraints

> [!WARNING]
> All papers listed above require full-text verification. DOIs should be checked against the actual published versions. No equation numbers or page references are included yet — these must come from reading the actual papers.
