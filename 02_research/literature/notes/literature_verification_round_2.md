# EL Project — Round 2 Literature Verification (Initial Audit)

**Prepared:** 2026-10-18  
**Status:** Initial bibliographic/abstract audit; full-text equation verification remains pending.  
**Purpose:** Continue from `literature_search_round_1.md` without prematurely freezing the model or claiming a verified research gap.

## 1. Current phase

The project is in **Literature-to-Mathematical-Foundation**. Do not begin full optimizer implementation or freeze the final equations until the core source papers and modeling assumptions have been checked.

## 2. Important Round-2 findings

### F01 — Add the 2023 ToU scheduling survey

**Catanzaro, Pesenti & Ronco (2023), “Job scheduling under Time-of-Use energy tariffs for sustainable manufacturing: a survey,” European Journal of Operational Research, 308(3), 1091–1109. DOI: 10.1016/j.ejor.2023.01.029.**

Publisher and institutional records identify this as a review focused specifically on job scheduling under ToU tariffs, including mathematical models and computational approaches. Add it to the literature matrix as a high-priority survey and use its reference list to expand citation chasing.

Source: https://doi.org/10.1016/j.ejor.2023.01.029
Publisher page: https://www.sciencedirect.com/science/article/pii/S0377221723000474
Institutional record with an open-access PDF listing: https://research.dial.uclouvain.be/entities/publication/f0f21003-c424-4d8a-9378-9b6dcc3527de

### F02 — Add and prioritize the 2026 demand-charge paper

**Sung & Kwon (2026), “Demand charge determination for managing peak demand in energy-aware production scheduling,” Applied Energy, 415, article 127953. DOI: 10.1016/j.apenergy.2026.127953. Published 15 July 2026.**

The publisher abstract describes production scheduling under time-varying energy prices and demand charges, a peak–energy curve, and estimating demand-charge rates to target peak demand. This is directly relevant to our research framing.

**Consequence:** Round-1 statements that demand-charge sensitivity or the combination of ToU and peak-demand scheduling is a “confirmed gap” are not defensible as written. This paper does not automatically invalidate our precise empirical question, but we must read it and compare its research question, model and experiments before defining any gap.

Source: https://doi.org/10.1016/j.apenergy.2026.127953
Publisher page: https://www.sciencedirect.com/science/article/pii/S0306261926006057

### F03 — Correct Moon et al. (2013) scheduling-class label

Round 1 describes Moon, Shin & Park (2013) as job-shop scheduling. The accessible article abstract/author copy describes an **unrelated parallel-machine scheduling problem**, with time- and machine-dependent electricity costs and a weighted objective involving makespan and electricity cost.

**Action:** Change the matrix classification to “unrelated parallel-machine scheduling” unless full-text verification reveals that the current record refers to a different formulation. Do not use it as the primary job-shop reference without resolving this discrepancy.

Publisher DOI: https://doi.org/10.1007/s00170-013-4749-8
Accessible author copy/discovery record: https://www.researchgate.net/publication/257337356_Optimization_of_production_scheduling_with_time-dependent_and_machine-dependent_electricity_cost_for_industrial_energy_efficiency

### F04 — Correct Dai et al. (2019) page range

For **“Multi-objective optimization for energy-efficient flexible job shop scheduling problem with transportation constraints”**, the publisher listing gives *Robotics and Computer-Integrated Manufacturing*, volume 59, pages **143–157**, DOI **10.1016/j.rcim.2019.04.006**. Round 1 recorded pages 263–276, which appears inconsistent with the publisher record.

The publisher abstract describes a multi-objective flexible job-shop formulation minimizing energy consumption and makespan, with transportation constraints and an enhanced genetic algorithm.

**Action:** Correct the citation metadata and verify exact equations from the paper before adopting any formulation.

Publisher page: https://www.sciencedirect.com/science/article/pii/S0736584518305222
DOI: https://doi.org/10.1016/j.rcim.2019.04.006

### F05 — Correct Zhang et al. (2014) DOI

For **“Energy-conscious flow shop scheduling under time-of-use electricity tariffs”**, the publisher record identifies DOI **10.1016/j.cirp.2014.03.011**, not **10.1016/j.cirp.2014.03.084** as recorded in Round 1.

The publisher abstract describes a time-indexed integer-programming formulation for electricity cost and carbon-footprint minimization under ToU pricing in a flow shop.

**Action:** Correct DOI metadata, then verify publication details and equation references against the paper.

Publisher page: https://www.sciencedirect.com/science/article/abs/pii/S0007850614000146
Correct DOI: https://doi.org/10.1016/j.cirp.2014.03.011

### F06 — Correct Aghelinejad et al. (2018) problem-class label

The publisher abstract says this paper studies a **non-preemptive single-machine** manufacturing environment with time-dependent energy costs. Round 1 labels the problem “single/parallel machine scheduling,” which is broader than the abstract supports.

**Action:** Label it “single-machine scheduling” unless full text supports a broader class.

Publisher page: https://www.tandfonline.com/doi/full/10.1080/00207543.2017.1414969
DOI: https://doi.org/10.1080/00207543.2017.1414969

### F07 — Separate peak constraints from demand-charge cost

A paper that constrains peak power does not necessarily formulate an explicit demand-charge cost. Record these as separate fields:

- peak power as a constraint;
- peak power as an objective;
- explicit demand-charge term in the economic objective;
- utility billing-demand rules, including billing interval and kW/kVA treatment.

Do not classify one as another without evidence in the paper.

### F08 — Keep solver documentation out of the academic-paper count

OR-Tools / CP-SAT documentation is useful for implementation, but it is not one of the 15–20 peer-reviewed candidate papers or 5–8 foundational academic papers. Maintain a separate “implementation documentation” category.

## 3. Initial verification matrix

| ID | Candidate | Metadata/abstract status from publisher or authoritative record | What remains before adopting equations |
|---|---|---|---|
| P01 | Mouzon et al. (2007) | Publisher metadata and abstract located | Read full text; extract state-energy and objective equations with page numbers |
| P02 | Gahm et al. (2016) | Publisher metadata and abstract located | Review full paper and citation network; use as survey, not equation source unless justified |
| P03 | Mavrotas (2009) | Publisher DOI record and abstract located | Read exact AUGMECON formulation, assumptions, and implementation details |
| P05 | Dai et al. (2019) | Publisher metadata/abstract located; page-range correction needed | Full-text extraction; confirm objective, constraints, energy model, problem assumptions |
| P08 | Fang et al. (2013) | Author repository record and DOI located | Full-text equation/page extraction; confirm peak-power constraint structure |
| P09 | Moon et al. (2013) | DOI and article record located; problem-class discrepancy found | Resolve exact problem class and extract ToU-cost equations from article |
| P10 | Fang et al. (2016) | Bibliographic record located | Verify whether it models a peak constraint and/or an explicit demand-charge cost; do not infer |
| P12 | Aghelinejad et al. (2018) | Publisher metadata and abstract located; single-machine classification supported | Extract equations and machine-state assumptions |
| NEW | Catanzaro et al. (2023) | Publisher/institutional metadata and survey scope located | Read review, follow references, classify coverage of peak/demand charge |
| NEW | Sung & Kwon (2026) | Publisher metadata and abstract located | Obtain/read full text; compare directly against project RQs and factor sensitivity design |

**Important:** “Metadata/abstract located” does not mean full mathematical verification is complete. No equation from these papers is marked fully verified in this report.

## 4. Updated gap discipline

Until systematic full-text screening is finished, use wording such as:

> “The preliminary search identified a potential empirical question concerning the conditions under which peak-aware scheduling improves economic outcomes. This question will be refined after full-text comparison with existing ToU and demand-charge scheduling studies.”

Do not use “no studies exist,” “gap confirmed,” or “first ever” unless a documented search and full-text comparison actually support that claim.

The 2026 Sung & Kwon paper is particularly important: its scope overlaps with peak-demand management under time-varying energy prices and demand charges. The project may still have a defensible angle in its **factorial sensitivity analysis, workload/power heterogeneity study, or physical validation**, but that must be established from the full text rather than presumed.

## 5. Immediate tasks in the repository

1. Preserve `literature_search_round_1.md` as the historical Round-1 result; do not silently overwrite it.
2. Create `02_research/literature/notes/literature_verification_round_2.md` from this report.
3. Add Catanzaro et al. (2023) and Sung & Kwon (2026) to `literature_to_model_matrix.md` with status `PENDING FULL-TEXT REVIEW`.
4. Correct the preliminary metadata errors: Moon problem class; Dai page range; Zhang DOI; Aghelinejad problem class.
5. Obtain the actual PDFs for the top 5–8 papers and record verified equation/page references.
6. Only after this work, decide the scheduling class and mathematical formulation.

## 6. Next milestone

**Round-2 milestone:** a verified 5–8 paper foundation, an equation-level traceability table, and a conservatively justified research question.

Do not start full implementation until the mathematical formulation is drafted and checked on small hand-solvable instances.
