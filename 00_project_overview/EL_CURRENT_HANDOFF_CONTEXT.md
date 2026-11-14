# EL Project — Current Handoff Context

> **Last updated:** 2026-10-18  
> **Use:** Give this file to a new AI/chat at the beginning of a continuation.  
> **Authority:** This is a compact handoff summary. The project's canonical master context and execution plan take precedence if details conflict.

## Project

**Title:** Peak-Aware Energy-Cost Production Scheduling for Small Manufacturing Systems Under Industrial Tariff Structures: A Multi-Objective Optimization Study with Physical Validation.

**SDG:** SDG 9 — Industry, Innovation and Infrastructure.

**Central research question:** Under what combinations of demand-charge intensity, time-of-use tariff variation, workload intensity, and machine-power heterogeneity does peak-aware production scheduling provide a statistically significant economic benefit over energy-cost-only scheduling?

## The core idea in plain language

Different schedules can finish the same jobs but create different power profiles. The project will compare production-only, energy-cost-only, and peak-aware scheduling to determine when accounting for peak demand is economically useful. Do not assume in advance that peak-aware scheduling always wins.

## Current status

- Project definition and scope established.
- Project folder organization completed.
- KERC tariff reference documented.
- Old PZEM-004T proposal superseded; current 12V DC testbed direction uses INA226.
- Literature search Round 1 completed as a candidate list.
- Full-text verification of foundational papers still pending.
- Phase-I PPT content, diagrams, and mentor-pitch explanations drafted.
- Final mathematical model is **not frozen**.
- No experimental savings results should be claimed yet.

## Research workflow

`Literature discovery → DOI/source verification → full-text equation extraction → literature-to-model matrix → literature-to-equation map → select scheduling class → construct Model V1 → hand-verify → implement → baselines → sensitivity experiments → physical validation`.

The existing prompt `02_research/prompts/literature_search_prompt.md` should be retained and used as the literature task specification. Do not redesign the model before the literature audit. Do not rely on a report's “gap confirmed” label until full-text screening supports it.

## Literature Round 1

Artifact: `literature_search_round_1.md` (uploaded file; 455 lines). Its declared status is candidate list requiring full-text PDF verification. Candidate papers cover machine-state energy modeling, energy-aware scheduling surveys, ToU scheduling, peak-power constraints, multi-objective scheduling, and epsilon-constraint/AUGMECON methods.

Cautions:
- Peak-power constraint ≠ demand-charge cost model automatically.
- CP-SAT is constraint programming/SAT-based, not a MILP solver.
- OR-Tools documentation is an implementation source, not a peer-reviewed foundational paper.
- Research gaps are preliminary until verified against full papers and broader search.

## Tariff facts recorded in project reference

From the official KERC Tariff Order 2025 — All ESCOMs, Annexure 9, HT-2(a) Industrial, FY2026–27 (effective 1 April 2026):
- Energy charge: ₹6.60/kWh.
- Demand charge: ₹350/kVA/month of billing demand.
- Billing-demand rule: `BD = max(MD, 0.90 × CD)`, subject to the order's rounding and excess-demand rules.
- ToU schedule and applicability must be read from the project tariff reference, not improvised.

Do not equate short-run lab peak kW with monthly billing demand kVA. Keep actual tariff billing separate from a normalized research demand parameter.

## Active hardware architecture

`12V DC load emulators → INA226 measurement → ESP32 sensing/control → Wi-Fi/MQTT → Raspberry Pi 5 optimizer/experiment controller`.

- INA226: DC voltage/current/power measurement.
- ESP32: sensing, timestamps, load switching/control, communications.
- Raspberry Pi 5: OR-Tools CP-SAT optimization and experiment workflow; can be benchmarked against a laptop.
- Candidate loads: 12V motor, resistive/heater load, LED, fan/pump, subject to actual rating checks.
- No mains voltage on a breadboard; the physical testbed emulates machine loads, not an industrial factory.
- PZEM-004T is historical/superseded only.

## Experimental approach

Data layers:
1. **Measured:** voltage, current, power, energy, load state and timing from the physical testbed.
2. **Designed/synthetic:** jobs, machines, processing times, precedence, machine assignment, workload and instance size.
3. **Official-source-derived:** KERC tariff values and time periods.

Compare scheduling baselines such as FCFS, SPT, makespan-only, energy-cost-only, and the proposed peak-aware strategy as supported by the final formulation. Primary metrics: makespan, energy consumption/cost, peak power, solver time; predicted-versus-measured error for physical validation.

Vary four factors: demand-charge intensity, ToU price differential, workload intensity, machine-power heterogeneity. Choose parameter values based on verified design and sensitivity methodology; do not assert arbitrary thresholds or expected percentage savings.

## Presentation guidance

Phase-I PPT template requires title, methodology/outline, intro, literature review, problem definition, objectives, methodology, a methodology flowchart, proposed outcomes, timeline, conclusion, references, and expected first-year outcomes.

State what is **completed**, **preliminary**, and **planned** accurately. Literature findings are preliminary until full-text verified. No fabricated result or claim of novel algorithm. Use concise visual diagrams:
- Slide 4: production vs energy-cost vs peak-demand motivation/trade-off.
- Slide 8: data inputs (physical measurements, synthetic scheduling data, KERC tariff).
- Slide 9: main methodology flowchart.
- Slide 10 or 8: current hardware/software architecture, only if space permits.

Mentor pitch core: “We are not trying to prove peak-aware scheduling is always better; we are trying to determine when it is actually worth doing.”

## Key files in project repository

- `00_project_overview/energy_scheduling_project_master_context.md` — authoritative project context in repo.
- `05_planning/master_execution_plan.md` — execution plan.
- `03_tariff/tariff_reference.md` — current KERC parameterization reference.
- `09_hardware/current_hardware_spec.md` — current INA226/DC-testbed specification.
- `02_research/prompts/literature_search_prompt.md` — existing literature prompt.
- `02_research/literature/notes/literature_search_round_1.md` — expected Round 1 output location (check actual repo copy).
- `02_research/literature/literature_matrix/literature_to_model_matrix.md` — literature matrix target.
- `04_mathematical_model/derivation/literature_to_equation.md` — equation traceability target.
- `PROJECT_STATUS.md` — status summary.

## How a new AI should proceed

1. Read this handoff first.
2. Read the repo master context and execution plan; they override conflicting summary details.
3. Use actual file contents where provided; don't claim a file is empty just because it wasn't ingested into context. Don't rewrite files unless explicitly requested.
4. Ask for or inspect `EL_CONVERSATION_LOG.md` for history; it is a curated summary, not a verbatim transcript.
5. Continue from the current phase: full-text literature verification and preparation of the Phase-I presentation.
6. Do not start final modeling before the literature-to-equation audit.
7. Be direct, precise, step-by-step, and PowerShell-friendly when giving local Windows commands.
