# EL Project — Conversation Log

> **Purpose:** Portable chronological record of decisions, explanations, tasks, and artifacts discussed with AI assistants.
>
> **Important:** Entries in this file are curated summaries, not verbatim transcripts, unless a section is explicitly marked **VERBATIM**. Do not treat summaries as exact quotations.
>
> **Project:** Peak-Aware Energy-Cost Production Scheduling for Small Manufacturing Systems Under Industrial Tariff Structures: A Multi-Objective Optimization Study with Physical Validation.

## How to maintain this log

After each meaningful work session, append a new dated entry using the template at the bottom. Record:
- what the user asked for;
- what was decided or explained;
- assumptions and limitations stated;
- files/artifacts created or reviewed;
- unresolved questions and next actions.

Keep old entries. Correct mistakes with a dated correction note rather than silently rewriting history. For the authoritative current state, consult `EL_CURRENT_HANDOFF_CONTEXT.md` and the project's canonical master context. The canonical project documents take precedence over any conflicting historical log entry.

For exact message-by-message history, save/export the raw conversation separately. This file alone is not a complete verbatim transcript.

---

# Chronological Entries

## Entry 001 — Project direction and research framing

**Period:** Earlier project planning conversations; exact individual timestamps not available in this summary.

**User goal:** Develop a technically defensible undergraduate Experiential Learning project under SDG 9 (Industry, Innovation and Infrastructure). The user explicitly rejected generic, unnecessary combinations of AI, IoT, blockchain, dashboards, chatbots, and basic prediction models.

**Working project title:**

> Peak-Aware Energy-Cost Production Scheduling for Small Manufacturing Systems Under Industrial Tariff Structures: A Multi-Objective Optimization Study with Physical Validation.

**Central research question:**

> Under what combinations of demand-charge intensity, time-of-use (ToU) tariff variation, workload intensity, and machine-power heterogeneity does peak-aware production scheduling provide a statistically significant economic benefit over energy-cost-only scheduling?

**Research stance:** The goal is not to claim a new optimization algorithm. The intended contribution is primarily empirical/engineering integration: systematic evaluation of when peak-awareness is economically useful, comparison of scheduling baselines, and physical validation.

**Key rule:** A positive, negligible, or null result can all be valid. Do not assume peak-aware scheduling always wins or promise a savings percentage before experiments.

## Entry 002 — Mathematical and experimental scope

The project plan establishes the following core direction:

- Compare production-oriented, energy-cost-oriented, and peak-aware scheduling strategies.
- Evaluate makespan, energy consumption/cost, and maximum simultaneous power.
- Vary four experimental factors: demand-charge intensity, ToU price differential, workload intensity, and machine-power heterogeneity.
- Use deterministic, known scheduling instances for the core work.
- Use synthetic scheduling instances for systematic computational experiments.
- Use OR-Tools CP-SAT as the planned optimization solver, with a systematic multi-objective approach such as an epsilon-constraint/AUGMECON-style method only after the formulation and method are verified.
- Compare against appropriate baselines such as FCFS, SPT, makespan-only, and energy-cost-only scheduling.
- Perform statistical analysis and Pareto/trade-off evaluation.
- Keep uncertainty analysis, advanced evolutionary methods, and rolling-horizon rescheduling as stretch work rather than allowing them to block the core project.

**Important methodological rule:** Do not freeze the final equations before completing the literature-to-mathematical-foundation audit. Do not label CP-SAT as a MILP solver.

## Entry 003 — Tariff interpretation and official source

The project uses the uploaded KERC Tariff Order 2025 — All ESCOMs, particularly Annexure 9, as the official tariff parameterization source. The project notes record the following HT-2(a) Industrial values for FY2026–27, effective 1 April 2026:

- Energy charge: ₹6.60/kWh.
- Demand charge: ₹350/kVA/month of billing demand.
- Billing demand: `BD = max(MD, 0.90 × CD)`, subject to the order's rounding and excess-demand provisions.
- Time-of-day adjustments vary by period and season; use the project's official tariff reference for exact periods and applicability.

**Non-negotiable distinctions:**
- kW and kVA are not interchangeable without an explicit power-factor assumption.
- A peak-power constraint is not automatically a demand-charge cost model.
- Real utility demand billing is monthly; a short laboratory test does not reproduce a real monthly industrial bill.
- Keep the real tariff layer separate from any normalized research demand parameter (such as `rho`).
- Use the official order for exact tariff details; don't rely on stale copied values.

## Entry 004 — Hardware correction

**Superseded component:** PZEM-004T was proposed in an older design but is an AC measurement solution and is unsuitable for the planned 12V DC load-emulation testbed.

**Current hardware direction:**

`12V DC loads → INA226 measurement → ESP32 sensing/control → Wi-Fi/MQTT → Raspberry Pi 5 optimization/experiment platform`

- INA226 measures DC bus voltage and shunt current; power is derived/recorded.
- ESP32 handles measurement collection, timestamps/load states, and load switching.
- Raspberry Pi 5 runs the optimization/experiment workflow and may benchmark solver runtime against a laptop.
- Test loads are emulators (candidate motor, heater/resistive load, LED, fan/pump); they do not represent actual industrial machines.
- No mains voltage on a breadboard. Verify exact component and supply ratings before wiring.

**Do not remove all mentions of PZEM from historical files.** Retain references when clearly marked as superseded/historical.

## Entry 005 — Repository organization and cleanup

The project repository is organized under `C:\Project\EL`, including:

```text
EL/
├── 00_project_overview/
├── 01_rubric/
├── 02_research/
│   ├── literature/
│   │   ├── papers/
│   │   ├── literature_matrix/
│   │   └── notes/
│   ├── prompts/
│   └── validation/
├── 03_tariff/
│   ├── official/
│   ├── supporting/
│   ├── extracted/
│   └── tariff_reference.md
├── 04_mathematical_model/
│   ├── derivation/
│   ├── formulation/
│   └── verification/
├── 05_planning/
├── 06_data/
├── 07_src/
├── 08_experiments/
├── 09_hardware/
├── 10_results/
├── 11_report/
├── 12_tools/
├── tests/
└── PROJECT_STATUS.md
```

Old validation documents were moved under `historical` folders. A PowerShell scan confirmed that remaining PZEM references are retained in historical/superseded notes, correction notes, or current hardware documentation that explicitly describes the old design. The `PROJECT_STATUS.md` line was updated to state that PZEM-004T was an earlier proposed device and was superseded by INA226.

## Entry 006 — Literature-review workflow

The user has an existing literature prompt at:

`02_research/prompts/literature_search_prompt.md`

and tariff reference at:

`03_tariff/tariff_reference.md`.

There was an access/context issue where Opus reported these documents as empty in its ingested view; the user clarified that the files contain data. Do not let an AI overwrite or reconstruct them merely because its context viewer reports them empty. First confirm actual workspace access and, if needed, explicitly attach the files or create a context packet from their actual contents.

**Existing literature prompt should be retained.** It asks for verified peer-reviewed papers, explicit mathematical formulation extraction, equation/page references, a literature-to-model matrix, and careful research-gap analysis. It says not to design the final model yet.

**Research process:**

`Paper discovery → DOI/source verification → full-text PDF screening → extract equations/assumptions → literature-to-model matrix → literature-to-equation traceability → choose scheduling class → formulate Model V1 → hand-verify → implement`.

Target from the current plan: approximately 15–20 candidate papers and 5–8 foundational papers, subject to quality rather than padding the count.

## Entry 007 — Literature Round 1 file reviewed

**Artifact:** `literature_search_round_1.md` (uploaded and reviewed in this conversation; 455 lines).

**Its own status:** Candidate list requiring verification against full-text PDFs.

Candidate papers include:
- Mouzon, Yildirim & Twomey (2007), machine-state energy modeling.
- Gahm et al. (2016), energy-efficient scheduling review.
- Mavrotas (2009), epsilon-constraint method.
- Mavrotas & Florios (2013), AUGMECON2.
- Dai et al. (2019), multi-objective energy-efficient FJSP.
- Zhang et al. (2017), energy-efficient FJSP.
- Fang et al. (2013), flow-shop peak-power constraints.
- Moon, Shin & Park (2013), job-shop scheduling with time-dependent electricity costs.
- Fang et al. (2016), single-machine scheduling under ToU tariffs.
- Aghelinejad et al. (2018), machine-state and time-dependent energy costs.

**Review cautions recorded:**
1. Round 1 is useful for discovery, not yet a verified review.
2. Do not call a gap “confirmed” while key papers remain unverified.
3. A peak-power constraint is not automatically an economic demand-charge model.
4. OR-Tools documentation is useful implementation documentation, not a peer-reviewed foundational paper.
5. KERC is a tariff parameterization source, not an academic scheduling paper.
6. No final mathematical formulation should be frozen until equations and assumptions are extracted from the actual papers.

**Next literature step:** Round 2 full-text verification, DOI checks, equation/page extraction, and updating the literature-to-model and literature-to-equation matrices.

## Entry 008 — Phase-I presentation content

The user supplied the Experiential Learning Phase-I PowerPoint template. It requires:
1. Title
2. Experiential Learning outline / tentative methodology
3. Presentation outline
4. Introduction
5. Literature review
6. Problem definition
7. Objectives
8. Methodology
9. Methodology flowchart
10. Proposed outcomes
11. Timeline
12. Conclusion
13. References
14. Expected outcomes by end of first year

Slide content was drafted concisely, with the following rules:
- Present the work as proposed/planned unless results exist.
- Describe the literature review as preliminary until full-text verification is complete.
- Do not claim known savings percentages or algorithmic novelty.
- State clearly that synthetic instances are used for larger computational experiments and the physical testbed is a low-voltage DC machine-load emulator, not a real factory.

A compact literature-review table was made for Mouzon, Moon, Fang, Gahm, and Aghelinejad. The table must be updated if full-text verification changes a paper's contribution or bibliographic details.

## Entry 009 — Data collection explanation

Data sources were clarified as three categories:

1. **Real physical measurements:** INA226 voltage/current/power readings, timestamps, machine ON/OFF state, measured energy and peak power from the low-voltage testbed.
2. **Designed/synthetic scheduling inputs:** jobs, machines, processing times, precedence, assignments, workload levels, instance sizes.
3. **Official tariff parameters:** KERC energy charges, demand-charge rate, ToU time periods and applicable tariff rules.

Optimization produces schedules evaluated for makespan, energy cost, and peak demand. Sensitivity experiments vary demand-charge intensity, ToU price differential, workload intensity, and machine-power heterogeneity. Larger computational runs are simulated; do not present synthetic results as physical measurements.

## Entry 010 — Flowcharts and diagrams

Diagrams/images were generated for presentation use covering:
- introduction: conventional scheduling versus a production + energy-cost + peak-aware approach;
- trade-off between makespan, energy cost and peak demand;
- data collection from physical measurements, synthetic scheduling instances, and KERC tariff data;
- methodology flowchart from data inputs through optimization, schedule generation, performance evaluation, sensitivity analysis, and physical validation;
- hardware/software architecture using 12V DC loads, INA226, ESP32, Wi-Fi/MQTT and Raspberry Pi 5;
- a feedback/model-refinement loop.

**Slide placement guidance:**
- Slide 4 (Introduction): motivation/trade-off diagram on the right, explanatory text on left.
- Slide 8 (Methodology/data collection): data-source diagram under/alongside concise bullets.
- Slide 9 (Methodology flowchart): main research process, centered and large; the template explicitly asks for a flowchart here.
- Slide 10 (Proposed Outcomes) or Slide 8: current hardware/software architecture, only if the slide has room.
- Avoid using several detailed diagrams on one slide. Generated images should be checked for text accuracy and legibility before final presentation.

## Entry 011 — Pitching the project to a mentor

The mentor pitch should emphasize the research question, not market the project as a generic IoT or AI system.

**Core pitch:**

> Two schedules can complete the same production workload but have different electrical profiles. Our study investigates when adding peak-demand awareness to production scheduling provides meaningful economic benefit, compared with energy-cost-only scheduling. We will use verified literature to construct the model, controlled computational experiments to compare strategies under varying tariff/workload conditions, and a low-voltage physical testbed to validate modeled electrical behavior.

**Honest contribution:** Systematic empirical characterization and physical validation, not a claimed new optimization algorithm.

**Important limitations to mention:** no real factory deployment; short testbed runs do not reproduce monthly industrial bills; DC testbed does not reproduce AC power factor behavior.

## Entry 012 — Current status as of 2026-10-18

**Current phase:** Preparing Phase-I presentation while literature Round 1 is complete and Round 2 full-text verification remains the research next step.

**Known project state:**
- Project direction and research question established.
- KERC tariff values and billing-demand distinction documented in project files.
- Active testbed architecture uses INA226 + ESP32 + low-voltage 12V DC loads; Raspberry Pi 5 is the optimization/experiment platform.
- Existing literature prompt should be reused, not replaced without reason.
- Literature Round 1 is a candidate list, not a verified final review.
- Presentation content and explanation/pitch have been drafted.
- The model is not frozen and experimental results have not yet been established.

**Immediate research next actions:**
1. Complete Round 2 full-text verification of candidate papers.
2. Verify metadata/DOIs and extract actual equation/page references.
3. Populate `02_research/literature/literature_matrix/literature_to_model_matrix.md`.
4. Create/complete `04_mathematical_model/derivation/literature_to_equation.md`.
5. Choose the scheduling problem class from evidence and scope.
6. Draft and hand-verify Model V1.
7. Only then proceed to implementation and planned experiments.

**Immediate presentation next actions:**
1. Check the slide content against the actual PPT template.
2. Verify every preliminary literature citation before final submission.
3. Check generated diagrams for correct labels and readable text.
4. Ensure all slides distinguish completed work from proposed work.

---

# Append-only entry template

## Entry NNN — [Short topic]

**Date:** YYYY-MM-DD

**User request:** [What was requested]

**Work done / response summary:** [What was provided]

**Decisions made:**
- [Decision]

**Corrections / caveats:**
- [Correction or limitation]

**Files / artifacts:**
- [Path or filename; indicate created/reviewed/updated]

**Open questions:**
- [Unresolved question]

**Next actions:**
1. [Next action]
