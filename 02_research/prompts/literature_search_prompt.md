# Literature Search Prompt — Energy-Aware Production Scheduling

I am developing an undergraduate engineering research project under:

**SDG 9: Industry, Innovation and Infrastructure**

Project working title:

**Peak-Aware Energy-Cost Production Scheduling for Small Manufacturing Systems Under Industrial Tariff Structures: A Multi-Objective Optimization Study with Physical Validation**

## Project context

The project studies production scheduling for a small manufacturing-system abstraction where electricity cost can depend on:

1. energy consumed (kWh),
2. time-of-use/time-of-day electricity pricing,
3. peak electrical demand / demand charges,
4. production constraints such as machine availability, operation precedence and makespan.

The intended research question is:

> Under what combinations of demand-charge intensity, time-of-use tariff variation, workload intensity, and machine power heterogeneity does peak-aware production scheduling provide a statistically significant economic benefit over energy-cost-only scheduling?

The project is NOT intended to claim a new optimization algorithm or new mathematical optimization theory.

The intended contribution is an empirical and engineering study involving:

- established production-scheduling mathematics,
- energy-cost-aware scheduling,
- peak-demand-aware scheduling,
- systematic sensitivity analysis,
- Pareto analysis,
- physical validation using a low-voltage DC machine-load emulation testbed,
- Raspberry Pi edge deployment.

## IMPORTANT HARDWARE CONTEXT

The current physical testbed uses:

- Raspberry Pi 5
- ESP32
- INA226 DC power-monitoring modules
- low-voltage 12V DC machine-load emulators
- relay/MOSFET switching

**PZEM-004T is a superseded design and is NOT the current measurement device for the 12V DC testbed.**

Do not use the old PZEM design as the current hardware architecture.

---

# PRIMARY TASK

Do NOT create our final mathematical model yet.

Instead, conduct a rigorous literature search to determine:

> **What mathematical formulations already exist in peer-reviewed research that can legitimately form the foundation of our production scheduling + energy cost + peak demand model?**

The objective is to move from:

```text
peer-reviewed literature
        ↓
established mathematical formulations
        ↓
comparison of formulations
        ↓
selection of foundation
        ↓
adaptation to our project