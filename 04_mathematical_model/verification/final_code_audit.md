# Final Code-Level Audit of the Verified Benchmark (Model V1.0)

**Project:** Peak-Aware Energy-Cost Production Scheduling for Small Manufacturing Systems Under Industrial Tariff Structures: A Multi-Objective Optimization Study with Physical Validation  
**Phase:** Mathematical Foundation → Verification Audit Gate (Prompt 2D Deliverable)  
**Date:** 2026-11-05  
**Auditor:** Antigravity AI Pair Programmer (Independent Code-Level Auditor)  
**Target File:** `04_mathematical_model/verification/final_code_audit.md`  
**Audited Artifacts:**
- Verification Script: [`04_mathematical_model/verification/verify_benchmark.py`](file:///c:/Project/EL/04_mathematical_model/verification/verify_benchmark.py)
- Verification Results: [`04_mathematical_model/verification/benchmark_verification_results.md`](file:///c:/Project/EL/04_mathematical_model/verification/benchmark_verification_results.md)
- Mathematical Formulation: [`04_mathematical_model/formulation/mathematical_model_v1.md`](file:///c:/Project/EL/04_mathematical_model/formulation/mathematical_model_v1.md)
- Hand Calculations: [`04_mathematical_model/verification/test_instances/hand_calculations.md`](file:///c:/Project/EL/04_mathematical_model/verification/test_instances/hand_calculations.md)
- Project Status: [`PROJECT_STATUS.md`](file:///c:/Project/EL/PROJECT_STATUS.md)

---

## 1. Executive Summary & Audit Verdict

This audit performs an independent, code-level inspection of the benchmark verification artifacts prior to authorizing the computational implementation of Google OR-Tools CP-SAT.

Following the pre-implementation audit (Prompt 2B) and subsequent benchmark verification (Prompt 2C), this code-level audit evaluates the verification script `verify_benchmark.py` and its associated reports against six strict criteria:
1. **Enumeration Completeness:** Whether the recursive generator provably spans the complete combinatorial universe of feasible non-preemptive schedules without omission or duplication.
2. **Independent Objective Calculation:** Whether schedule evaluation independently derives machine occupancy, power profiles, energy, energy costs, maximum demand, demand charges, and total costs without circular logic or shared generator state.
3. **Lexicographic Optimization Hierarchy:** Whether multi-stage optimization strictly preserves the primary global optimum before tie-breaking.
4. **Strategy C Physical Validity:** Whether the 27 kW peak of Strategy C is an emergent property of optimal cost trade-off rather than an artificial hard constraint, and whether all operations remain strictly contiguous.
5. **Break-Even & Lower-Envelope Rigor:** Whether the ₹12.70/kW transition is the true lower convex envelope breakpoint across the entire solution space rather than a superficial two-schedule crossing.
6. **Dimensional and Regulatory Consistency:** Whether physical units, time discretization, and demand-charge conventions are mathematically coherent and insulated from real-world billing fallacies.

### Summary of Verdict:
```
====================================================================================
FINAL AUDIT VERDICT:
[ FINAL AUDIT PASSED — READY FOR CP-SAT IMPLEMENTATION AUTHORIZATION ]
====================================================================================
```
All six audit criteria have passed with zero unresolved mathematical or code discrepancies.

---

## 2. Audit Methodology

The code audit employed a five-stage verification pipeline:

```
+--------------------------------------------------------------------------------------------------+
|                                    CODE AUDIT PIPELINE                                           |
+--------------------------------------------------------------------------------------------------+
|                                                                                                  |
|   1. STATIC CODE INSPECTION                                                                      |
|      - Trace AST and call graph of `verify_benchmark.py` (lines 1–1024).                         |
|      - Verify variable naming, types, slot index conventions (1-based vs 0-based).               |
|      - Inspect assertion definitions, error messages, and exception boundaries.                  |
|                                                                                                  |
|   2. ANALYTICAL COMBINATORIAL DERIVATION                                                         |
|      - Derive closed-form stars-and-bars combinatorial formula for schedule space.               |
|      - Compute exact counts for all 16 machine assignment partitions.                            |
|      - Reconcile closed-form sum with script's enumeration count (7,530).                         |
|                                                                                                  |
|   3. INDEPENDENT MANUAL STEP-BY-STEP TRACING                                                     |
|      - Manually evaluate exemplary schedules for Strategies A, B, and C.                         |
|      - Verify slot-by-slot machine occupancy, power, energy, and ToU tariff arithmetic.          |
|                                                                                                  |
|   4. PARETO & LOWER-ENVELOPE SWEEP                                                               |
|      - Extract all 248 unique (P_max, EC) objective points from the 7,530 schedules.             |
|      - Identify the true non-dominated Pareto front.                                             |
|      - Sweep rho in [0, 50] with step 0.01 to verify uniqueness of the envelope breakpoint.      |
|                                                                                                  |
|   5. DIMENSIONAL & REGULATORY CROSS-EXAMINATION                                                  |
|      - Verify dimensional homogeneity of all equations.                                          |
|      - Cross-check Model A vs Model B boundaries against KERC Tariff Order 2025.                 |
|                                                                                                  |
+--------------------------------------------------------------------------------------------------+
```

---

## 3. Detailed File and Function References

The verification engine [`verify_benchmark.py`](file:///c:/Project/EL/04_mathematical_model/verification/verify_benchmark.py) is structured into clear, decoupled functional modules:

| Module / Function | Lines | Functional Role & Mathematical Implementation |
|---|---|---|
| **Constants & Instance Data** | 50–118 | Defines $\Delta t = 1.0\text{ h}$, $T = 8$, $D = 8$, $L = 1$, $P_1 = 10\text{ kW}$, $P_2 = 25\text{ kW}$, $P_{\text{base}} = 2\text{ kW}$, $C_t \in [5.60, 7.60, 6.60]$, $\rho = 15.00$. All parameters mirror `hand_calculations.md` Section 2. |
| **`Operation` NamedTuple** | 124–131 | `(job_id, machine_id, start_slot, end_slot)`. 1-based inclusive interval indexing. |
| **`generate_machine_placements`** | 137–183 | Recursive combinatorial generator for a single machine. Considers all permutations of assigned jobs and enumerates all non-negative integer idle gaps within deadline $D=8$. |
| **`enumerate_all_feasible_schedules`** | 186–219 | Generates all $2^4 = 16$ machine partitions, invokes `generate_machine_placements` per machine, and takes the Cartesian product across machines. |
| **`evaluate_schedule`** | 242–368 | Independent validator and metric evaluator. Checks single assignment, eligibility, duration, bounds, machine non-overlap, and computes Equations (7)–(17). Returns `ScheduleMetrics`. |
| **`solve_strategy_a`** | 375–402 | Implements sequential lexicographic optimization for Strategy A: Phase 1 $\min C_{\max}$; Phase 2 $\min \sum C_j$. |
| **`solve_strategy_b`** | 404–429 | Implements sequential lexicographic optimization for Strategy B: Phase 1 $\min EC$; Phase 2 $\min C_{\max}$. |
| **`solve_strategy_c`** | 431–461 | Implements sequential lexicographic optimization for Strategy C: Phase 1 $\min TEC = EC + \rho P_{\max}$; Phase 2 $\min C_{\max}$. |
| **`compute_breakeven`** | 467–539 | Calculates pairwise $\rho^*$, evaluates sensitivity grid $\rho \in [0, 30]$, and checks global lower envelope across all 7,530 schedules. |
| **`verify_contiguity`** | 546–570 | Explicit structural validator: checks single appearance, exact duration match, and absence of intra-job preemption. |
| **`main` Test Harness** | 643–1021 | Runs 24 formal assertions covering uniqueness, bounds, arithmetic, optimality, and regulatory consistency. |

---

## 4. Enumeration Completeness Argument

### 4.1. Mathematical Definition of the Feasible Solution Space
Let $\mathcal{J} = \{J1, J2, J3, J4\}$ be the set of 4 independent jobs, and $\mathcal{M} = \{M1, M2\}$ be the set of 2 parallel machines. The planning horizon consists of $D = 8$ discrete uniform time slots $\{1, 2, \dots, 8\}$.

Any feasible schedule $\sigma$ is uniquely defined by:
1. A machine assignment function $A: \mathcal{J} \to \mathcal{M}$, partitioning $\mathcal{J}$ into disjoint subsets $J_{M1} = A^{-1}(1)$ and $J_{M2} = A^{-1}(2)$.
2. For each machine $m \in \{1, 2\}$, a sequence of non-overlapping, non-preemptive operations executing the assigned jobs $J_m$.

Because jobs cannot overlap on a machine (Constraint 6: $\sum_j y_{jmt} \le 1$) and cannot be preempted (Constraint 5), the execution on machine $m$ with $k_m = |J_m|$ assigned jobs defines:
- A permutation $\pi_m = (j_{(1)}, j_{(2)}, \dots, j_{(k_m)})$ of the jobs in $J_m$.
- A sequence of non-negative integer idle gaps:
  - $g_0 \ge 0$: idle slots before the first job starts.
  - $g_i \ge 0$ ($1 \le i \le k_m - 1$): idle slots between job $j_{(i)}$ and job $j_{(i+1)}$.
  - $g_{k_m} \ge 0$: idle slots after the last job completes, up to deadline $D$.

The temporal duration of the jobs is $W_m = \sum_{i=1}^{k_m} p_{j_{(i)}, m}$. The sum of all idle gaps must satisfy:
$$\sum_{i=0}^{k_m} g_i = D - W_m$$

By the classical **Stars and Bars Theorem**, the number of distinct non-negative integer solutions to an equation of $k_m + 1$ variables summing to $G = D - W_m$ is:
$$\binom{G + (k_m + 1) - 1}{(k_m + 1) - 1} = \binom{(D - W_m) + k_m}{k_m}$$

Because all 4 jobs have distinct IDs, each permutation of jobs on a machine represents a physically distinct operational schedule. Furthermore, because there are no precedence constraints or machine-coupling constraints in the operational feasibility definition, the choices on Machine 1 and Machine 2 are completely independent.

Therefore, the total number of feasible schedules in the universe is given by the exact closed-form expression:
$$\mathcal{S}_{\text{total}} = \sum_{(J_{M1}, J_{M2}) \in \mathcal{P}_2(\mathcal{J})} \left( \sum_{\pi_1 \in \Pi(J_{M1})} \mathbb{I}(W_{1}(\pi_1) \le D) \binom{D - W_1 + |J_{M1}|}{|J_{M1}|} \right) \times \left( \sum_{\pi_2 \in \Pi(J_{M2})} \mathbb{I}(W_{2}(\pi_2) \le D) \binom{D - W_2 + |J_{M2}|}{|J_{M2}|} \right)$$

### 4.2. Partition-by-Partition Closed-Form Enumeration Table

Evaluating the closed-form combinatorial formula for all $2^4 = 16$ machine assignment partitions yields the exact breakdown below:

| Partition # | Assigned to $M1$ | Assigned to $M2$ | Workload $W_1$ (h) | Workload $W_2$ (h) | Valid $M1$ Placements: $\sum \binom{8-W_1+k_1}{k_1}$ | Valid $M2$ Placements: $\sum \binom{8-W_2+k_2}{k_2}$ | Total Joint Schedules ($M1 \times M2$) |
|---|---|---|---|---|---|---|---|
| **1** | $\{J1, J2, J3, J4\}$ | $\emptyset$ | $2+3+2+3 = 10 > 8$ | 0 | $0$ (Exceeds $D=8$) | $1$ (Empty machine) | **0** |
| **2** | $\{J1, J2, J3\}$ | $\{J4\}$ | $2+3+2 = 7$ | 2 | $3! \times \binom{8-7+3}{3} = 6 \times 4 = 24$ | $1! \times \binom{8-2+1}{1} = 7$ | $24 \times 7 = \mathbf{168}$ |
| **3** | $\{J1, J2, J4\}$ | $\{J3\}$ | $2+3+3 = 8$ | 1 | $3! \times \binom{8-8+3}{3} = 6 \times 1 = 6$ | $1! \times \binom{8-1+1}{1} = 8$ | $6 \times 8 = \mathbf{48}$ |
| **4** | $\{J1, J2\}$ | $\{J3, J4\}$ | $2+3 = 5$ | $1+2 = 3$ | $2! \times \binom{8-5+2}{2} = 2 \times 10 = 20$ | $2! \times \binom{8-3+2}{2} = 2 \times 21 = 42$ | $20 \times 42 = \mathbf{840}$ |
| **5** | $\{J1, J3, J4\}$ | $\{J2\}$ | $2+2+3 = 7$ | 2 | $3! \times \binom{8-7+3}{3} = 6 \times 4 = 24$ | $1! \times \binom{8-2+1}{1} = 7$ | $24 \times 7 = \mathbf{168}$ |
| **6** | $\{J1, J3\}$ | $\{J2, J4\}$ | $2+2 = 4$ | $2+2 = 4$ | $2! \times \binom{8-4+2}{2} = 2 \times 15 = 30$ | $2! \times \binom{8-4+2}{2} = 2 \times 15 = 30$ | $30 \times 30 = \mathbf{900}$ |
| **7** | $\{J1, J4\}$ | $\{J2, J3\}$ | $2+3 = 5$ | $2+1 = 3$ | $2! \times \binom{8-5+2}{2} = 2 \times 10 = 20$ | $2! \times \binom{8-3+2}{2} = 2 \times 21 = 42$ | $20 \times 42 = \mathbf{840}$ |
| **8** | $\{J1\}$ | $\{J2, J3, J4\}$ | 2 | $2+1+2 = 5$ | $1! \times \binom{8-2+1}{1} = 7$ | $3! \times \binom{8-5+3}{3} = 6 \times 20 = 120$ | $7 \times 120 = \mathbf{840}$ |
| **9** | $\{J2, J3, J4\}$ | $\{J1\}$ | $3+2+3 = 8$ | 2 | $3! \times \binom{8-8+3}{3} = 6 \times 1 = 6$ | $1! \times \binom{8-2+1}{1} = 7$ | $6 \times 7 = \mathbf{42}$ |
| **10** | $\{J2, J3\}$ | $\{J1, J4\}$ | $3+2 = 5$ | $2+2 = 4$ | $2! \times \binom{8-5+2}{2} = 2 \times 10 = 20$ | $2! \times \binom{8-4+2}{2} = 2 \times 15 = 30$ | $20 \times 30 = \mathbf{600}$ |
| **11** | $\{J2, J4\}$ | $\{J1, J3\}$ | $3+3 = 6$ | $2+1 = 3$ | $2! \times \binom{8-6+2}{2} = 2 \times 6 = 12$ | $2! \times \binom{8-3+2}{2} = 2 \times 21 = 42$ | $12 \times 42 = \mathbf{504}$ |
| **12** | $\{J2\}$ | $\{J1, J3, J4\}$ | 3 | $2+1+2 = 5$ | $1! \times \binom{8-3+1}{1} = 6$ | $3! \times \binom{8-5+3}{3} = 6 \times 20 = 120$ | $6 \times 120 = \mathbf{720}$ |
| **13** | $\{J3, J4\}$ | $\{J1, J2\}$ | $2+3 = 5$ | $2+2 = 4$ | $2! \times \binom{8-5+2}{2} = 2 \times 10 = 20$ | $2! \times \binom{8-4+2}{2} = 2 \times 15 = 30$ | $20 \times 30 = \mathbf{600}$ |
| **14** | $\{J3\}$ | $\{J1, J2, J4\}$ | 2 | $2+2+2 = 6$ | $1! \times \binom{8-2+1}{1} = 7$ | $3! \times \binom{8-6+3}{3} = 6 \times 10 = 60$ | $7 \times 60 = \mathbf{420}$ |
| **15** | $\{J4\}$ | $\{J1, J2, J3\}$ | 3 | $2+2+1 = 5$ | $1! \times \binom{8-3+1}{1} = 6$ | $3! \times \binom{8-5+3}{3} = 6 \times 20 = 120$ | $6 \times 120 = \mathbf{720}$ |
| **16** | $\emptyset$ | $\{J1, J2, J3, J4\}$ | 0 | $2+2+1+2 = 7$ | $1$ (Empty machine) | $4! \times \binom{8-7+4}{4} = 24 \times 5 = 120$ | $1 \times 120 = \mathbf{120}$ |
| **Total** | — | — | — | — | — | — | **7,530** |

$$\text{Analytical Sum} = 0 + 168 + 48 + 840 + 168 + 900 + 840 + 840 + 42 + 600 + 504 + 720 + 600 + 420 + 720 + 120 = \mathbf{7,530}$$

### 4.3. Proof of Completeness vs. Mere Uniqueness
- **Completeness:** The recursive generator `generate_machine_placements` visits every integer start time $s_i \in [\text{earliest\_start}, \text{latest\_start}]$, which bijectively maps to all non-negative integer partitions of $D - W_m$. Because the algorithm explores all permutations and all valid gap distributions, no feasible schedule can be skipped.
- **Non-Redundancy:** Each schedule is generated from a distinct permutation of distinct job objects and distinct start-time tuples. Testing the generated set against a canonical set of sorted 4-tuples `(job_id, machine_id, start_slot, end_slot)` yielded exactly 7,530 unique keys with 0 duplicates.
- **Conclusion:** The enumeration is **mathematically complete and non-redundant**.

---

## 5. Independent Objective Calculation & Separation of Concerns

### 5.1. Trace of Objective Calculations
The evaluator function `evaluate_schedule` (lines 242–368) receives only the list of operations `[(job_id, machine_id, start_slot, end_slot)]` and independently derives all metrics:

1. **Machine Occupancy ($y_{jmt}$):**
   A dedicated data structure `machine_slot_occupancy[m][t]` tracks machine allocation for every slot $t \in \{1..8\}$ and machine $m \in \{1, 2\}$. If an operation attempts to occupy a slot that is already filled, an `AssertionError` is raised immediately.
2. **Facility Aggregate Active Power ($P(t)$):**
   `power_profile_kw` is initialized to the baseline load $P_{\text{base}} = 2.0\text{ kW}$ for all 8 slots. For each slot $t \in [\text{start}_j, \text{end}_j]$, the machine power $P_{jm}$ ($10.0\text{ kW}$ for $M1$, $25.0\text{ kW}$ for $M2$) is added.
3. **Total Electrical Energy ($E_{\text{total}}$):**
   $$E_{\text{total}} = \sum_{t=1}^T P(t) \cdot \Delta t = \sum_{t=1}^8 P(t) \times 1.0\text{ h}$$
4. **Time-of-Use Energy Cost ($EC$):**
   $$EC = \sum_{t=1}^T C_t \cdot P(t) \cdot \Delta t = \sum_{t=1}^8 C_t \cdot P(t)$$
   Where $C_t$ is fetched via `tariff_at_slot(t)` implementing the exact step vector $[5.60, 5.60, 7.60, 7.60, 7.60, 6.60, 6.60, 6.60]$.
5. **Peak Billing Demand ($P_{\max}$):**
   Under $L = 1\text{ slot} = 1.0\text{ h}$, the average power $p_k^{\text{int}}$ over interval $k$ simplifies identically to $P(k)$. Thus:
   $$P_{\max} = \max_{k \in \{1..8\}} p_k^{\text{int}} = \max_{t \in \{1..8\}} P(t)$$
6. **Modeled Demand Charge ($DC$):**
   $$DC = \rho \cdot P_{\max} = 15.00 \cdot P_{\max}$$
7. **Total Modeled Electricity Cost ($TEC$):**
   $$TEC = EC + DC = EC + 15.00 \cdot P_{\max}$$

### 5.2. Audit of Shared Assumptions and Couplings
An audit was performed to identify any shared functions or cached assumptions between the schedule generator and the schedule evaluator:

| Item | Generator (`generate_machine_placements`) | Evaluator (`evaluate_schedule`) | Coupling Risk Analysis |
|---|---|---|---|
| **Instance Constants** | Reads `JOBS`, `D_SLOTS` | Reads `JOBS`, `MACHINE_POWER_KW`, `P_BASE_KW`, `TARIFF_INR_PER_KWH`, `DELTA_T_HOURS` | **Zero Risk:** Constants are immutable and verified against `hand_calculations.md`. |
| **Duration Enforcement** | Determines end slot: $\text{end} = \text{start} + p_{jm} - 1$ | Re-derives duration: $\text{actual} = \text{end} - \text{start} + 1$, asserts $\text{actual} == p_{jm}$ | **Decoupled:** Evaluator does not trust generator duration; independently re-verifies. |
| **Machine Non-Overlap** | Enforced by recursion step: $\text{earliest\_start} = \text{end} + 1$ | Enforced by 2D matrix: checks $\text{occupancy}[m][t] \text{ is None}$ | **Decoupled:** Generator uses linear forward sequencing; evaluator uses spatial grid collision detection. |
| **Non-Preemption** | Emits a single contiguous interval per job | Verifies that each job has exactly one operation with length $p_{jm}$ | **Decoupled:** Evaluator validates that no job is split into multiple sub-operations. |
| **State Sharing** | None | None | **Zero Risk:** Pure functions; no shared mutable state or cached metrics. |

---

## 6. Lexicographic Optimization Audit

The implementation of Sequential Lexicographic Optimization was audited across `solve_strategy_a`, `solve_strategy_b`, and `solve_strategy_c`:

```
====================================================================================================
LEXICOGRAPHIC OPTIMIZATION FILTER AUDIT
====================================================================================================

STRATEGY A:
  Step 1: min_makespan = min(m.makespan_slots for m in all_metrics)  --> min = 4 slots
  Step 2: phase1 = [m for m in all_metrics if m.makespan_slots == min_makespan]  --> len = 4
  Step 3: min_flow = min(m.sum_completion_slots for m in phase1)  --> min = 12 slots
  Step 4: phase2 = [m for m in phase1 if m.sum_completion_slots == min_flow]  --> len = 4
  VERDICT: Phase 2 is strictly evaluated on phase1. Makespan is guaranteed <= 4. Zero energy bias.

STRATEGY B:
  Step 1: min_ec = min(m.energy_cost_inr for m in all_metrics)  --> min = ₹785.60
  Step 2: phase1 = [m for m in all_metrics if abs(m.energy_cost_inr - min_ec) < 1e-4]  --> len = 12
  Step 3: min_makespan = min(m.makespan_slots for m in phase1)  --> min = 8 slots
  Step 4: phase2 = [m for m in phase1 if m.makespan_slots == min_makespan]  --> len = 12
  VERDICT: Phase 2 is strictly evaluated on phase1. EC is guaranteed <= ₹785.60. Zero peak bias (rho=0).

STRATEGY C:
  Step 1: min_tec = min(tec(m) for m in all_metrics) at rho=15.0  --> min = ₹1317.60
  Step 2: phase1 = [m for m in all_metrics if abs(tec(m) - min_tec) < 1e-4]  --> len = 6
  Step 3: min_makespan = min(m.makespan_slots for m in phase1)  --> min = 8 slots
  Step 4: phase2 = [m for m in phase1 if m.makespan_slots == min_makespan]  --> len = 6
  VERDICT: Phase 2 is strictly evaluated on phase1. TEC is guaranteed <= ₹1317.60.
====================================================================================================
```

**Audit Finding:** In all three strategies, secondary optimization is strictly restricted to candidate schedules attaining the proven global optimum of the primary objective. The primary optimum is never compromised.

---

## 7. Strategy C Schedule Recalculation & Physical Validity

### 7.1. Independent Step-by-Step Manual Trace
The exemplar schedule reported for Strategy C is:
- **$M1$:** $J1$ executes in slots 3–4 ($p_{1,1} = 2$); $J2$ executes in slots 5–7 ($p_{2,1} = 3$).
- **$M2$:** $J4$ executes in slots 1–2 ($p_{4,2} = 2$); $J3$ executes in slot 8 ($p_{3,2} = 1$).

We trace the operational profile slot by slot:

| Slot $t$ | Tariff $C_t$ (₹/kWh) | $M1$ Operation | $M1$ Power (kW) | $M2$ Operation | $M2$ Power (kW) | $P_{\text{base}}$ (kW) | Total Power $P(t)$ (kW) | Interval Energy (kWh) | Interval Cost (₹) |
|---|---|---|---|---|---|---|---|---|---|
| **1** | ₹ 5.60 (Off-Peak) | IDLE | 0.0 | **$J4$** | 25.0 | 2.0 | **27.0** | 27.0 | $27.0 \times 5.60 = \mathbf{151.20}$ |
| **2** | ₹ 5.60 (Off-Peak) | IDLE | 0.0 | **$J4$** | 25.0 | 2.0 | **27.0** | 27.0 | $27.0 \times 5.60 = \mathbf{151.20}$ |
| **3** | ₹ 7.60 (Peak) | **$J1$** | 10.0 | IDLE | 0.0 | 2.0 | **12.0** | 12.0 | $12.0 \times 7.60 = \mathbf{91.20}$ |
| **4** | ₹ 7.60 (Peak) | **$J1$** | 10.0 | IDLE | 0.0 | 2.0 | **12.0** | 12.0 | $12.0 \times 7.60 = \mathbf{91.20}$ |
| **5** | ₹ 7.60 (Peak) | **$J2$** | 10.0 | IDLE | 0.0 | 2.0 | **12.0** | 12.0 | $12.0 \times 7.60 = \mathbf{91.20}$ |
| **6** | ₹ 6.60 (Normal) | **$J2$** | 10.0 | IDLE | 0.0 | 2.0 | **12.0** | 12.0 | $12.0 \times 6.60 = \mathbf{79.20}$ |
| **7** | ₹ 6.60 (Normal) | **$J2$** | 10.0 | IDLE | 0.0 | 2.0 | **12.0** | 12.0 | $12.0 \times 6.60 = \mathbf{79.20}$ |
| **8** | ₹ 6.60 (Normal) | IDLE | 0.0 | **$J3$** | 25.0 | 2.0 | **27.0** | 27.0 | $27.0 \times 6.60 = \mathbf{178.20}$ |
| **Total** | — | — | — | — | — | — | **Peak = 27.0 kW** | **141.0 kWh** | **EC = ₹ 912.60** |

- **Demand Charge ($DC$):** $DC = \rho \cdot P_{\max} = 15.00 \times 27.0 = \mathbf{\text{₹ } 405.00}$.
- **Total Modeled Cost ($TEC$):** $TEC = EC + DC = 912.60 + 405.00 = \mathbf{\text{₹ } 1,317.60}$.
- **Contiguity Verification:**
  - $J4$ occupies slots $[1, 2]$ contiguously ($2\text{ slots}$).
  - $J1$ occupies slots $[3, 4]$ contiguously ($2\text{ slots}$).
  - $J2$ occupies slots $[5, 7]$ contiguously ($3\text{ slots}$).
  - $J3$ occupies slot $[8, 8]$ contiguously ($1\text{ slot}$).
  - **Zero preemption, zero intra-job idle gaps, zero machine overlap.**

### 7.2. Physical Nature of the 27 kW Peak (Constraint vs. Emergent Optimum)
> [!IMPORTANT]
> **Audit Confirmation:**
> The $27.0\text{ kW}$ peak demand is **NOT a hard constraint** in Mathematical Model V1.0.
> - The formulation does **not** include any constraint of the form $P_{\max} \le 27.0\text{ kW}$, nor does it forbid machines $M1$ and $M2$ from operating concurrently.
> - The model's constraint set allows $P(t)$ to reach $37.0\text{ kW}$ (as seen in Strategies A and B).
> - The complete de-synchronization of $M1$ and $M2$ in Strategy C is an **emergent, unconstrained cost-minimizing trade-off**: under $\rho = \text{₹ } 15.00/\text{kW}$, the marginal demand penalty of overlapping machines ($\Delta DC = 15.00 \times 10.0 = \text{₹ } 150.00$) outweighs the energy savings obtainable by concurrent off-peak execution ($\Delta EC = \text{₹ } 127.00$).

---

## 8. Break-Even and Lower-Envelope Verification

### 8.1. Lower Convex Envelope Analysis Across All 7,530 Schedules
To verify whether the reported break-even rate $\rho^* = 12.70\text{ ₹/kW}$ is a true global property or merely a local crossing of two arbitrary schedules, an exhaustive objective space sweep was conducted:
1. Every schedule in the 7,530 solution space was mapped to its 2D objective coordinate $(P_{\max}, EC)$.
2. Exactly **248 distinct $(P_{\max}, EC)$ objective points** exist in the solution space.
3. Filtering for Pareto dominance (minimizing both $P_{\max}$ and $EC$) reveals that the Pareto front consists of **EXACTLY TWO POINTS**:
   - Point 1: $(P_{\max} = 27.0\text{ kW}, EC = \text{₹ } 912.60)$
   - Point 2: $(P_{\max} = 37.0\text{ kW}, EC = \text{₹ } 785.60)$
   - **Zero intermediate non-dominated points exist.** (There are no feasible schedules with $P_{\max} \in (27.0, 37.0)$ that achieve lower energy cost).
4. Sweeping $\rho \in [0.00, 50.00]$ in increments of $0.01\text{ ₹/kW}$ across all 7,530 schedules confirms that the lower convex envelope consists of exactly two linear segments with **ONE UNIQUE TRANSITION**:

$$\min_{s \in \mathcal{S}} TEC(s, \rho) = \begin{cases} 
785.60 + 37.0 \cdot \rho & \text{if } 0.00 \le \rho \le 12.70 \quad (\text{Strategy B is globally optimal}) \\
912.60 + 27.0 \cdot \rho & \text{if } \rho \ge 12.70 \quad (\text{Strategy C is globally optimal})
\end{cases}$$

At $\rho = 12.70\text{ ₹/kW}$, both segments intersect at $TEC = \text{₹ } 1,255.50$.

**Audit Finding:** The reported break-even threshold $\rho^* = 12.70\text{ ₹/kW}$ is **rigorously and provably the global lower-envelope transition** for this benchmark instance.

---

## 9. Time Discretization, Units, and Regulatory Boundaries

### 9.1. Dimensional Homogeneity Audit

| Variable / Parameter | Formula | Canonical Units | Dimensions | Homogeneity Status |
|---|---|---|---|---|
| Active Power $P(t)$ | $\sum P_{jm} y_{jmt} + P_{\text{base}}$ | $\text{kW}$ | $[M L^2 T^{-3}]$ | **HOMOGENEOUS** |
| Energy Consumption $E_{\text{total}}$ | $\sum P(t) \cdot \Delta t$ | $\text{kWh}$ | $[M L^2 T^{-2}]$ | **HOMOGENEOUS** |
| Time Slot Duration $\Delta t$ | Defined parameter | $\text{hours } (\text{h})$ | $[T]$ | **HOMOGENEOUS** |
| Time-of-Use Tariff $C_t$ | Defined vector | $\text{₹} / \text{kWh}$ | $[\text{Currency}] \cdot [M L^2 T^{-2}]^{-1}$ | **HOMOGENEOUS** |
| Energy Cost $EC$ | $\sum C_t P(t) \Delta t$ | $\text{₹}$ | $[\text{Currency}]$ | **HOMOGENEOUS** |
| Demand Interval Average $p_k^{\text{int}}$ | $\frac{1}{L} \sum_{t \in \mathcal{T}_k} P(t)$ | $\text{kW}$ | $[M L^2 T^{-3}]$ | **HOMOGENEOUS** |
| Peak Demand $P_{\max}$ | $\max_k p_k^{\text{int}}$ | $\text{kW}$ | $[M L^2 T^{-3}]$ | **HOMOGENEOUS** |
| Demand Intensity $\rho$ | Parameterized rate | $\text{₹} / \text{kW}$ per horizon | $[\text{Currency}] \cdot [M L^2 T^{-3}]^{-1}$ | **HOMOGENEOUS** |
| Demand Charge $DC$ | $\rho \cdot P_{\max}$ | $\text{₹}$ per horizon | $[\text{Currency}]$ | **HOMOGENEOUS** |
| Total Modeled Cost $TEC$ | $EC + DC$ | $\text{₹}$ per horizon | $[\text{Currency}]$ | **HOMOGENEOUS** |

### 9.2. Regulatory Demarcation: Model A vs. Model B
The audit verified that the documentation maintains a strict, unbreached boundary between the optimization engine and real-world tariffs:
1. **Model A (Optimization Benchmark):** Uses peak active power ($\text{kW}$) over an 8-hour shift with parameterized rate $\rho = \text{₹ } 15.00/\text{kW}$. It does not pretend to be a utility invoice.
2. **Model B (Commercial Tariff Discussion):** Documents the true KERC HT-2(a) tariff: ₹350/kVA/month based on the monthly 15-minute maximum demand ratchet $BD = \max(MD, 0.90 \times CD)$.
3. **Absence of Proration Fallacies:** The documents explicitly forbid claiming that daily peak shaving yields prorated monthly demand savings ($\text{₹ } 350 / 25 = \text{₹ } 14/\text{kW/day}$), citing the extreme-value nature of monthly billing demand and the 90% contract demand floor.

---

## 10. Pass / Fail Audit Requirements Matrix

| # | Audit Requirement | Specific Verification Check | Evidence in Script / Documents | Audit Result |
|---|---|---|---|---|
| **1** | **Enumeration Completeness** | Covers all 16 machine assignments, all permutations, all idle gap distributions; no duplicates. | Closed-form stars-and-bars formula proves $\mathcal{S}_{\text{total}} = 7,530$. Script matches exactly with 7,530 unique canonical keys. | **PASS** |
| **2** | **Independent Objective Calculation** | Machine occupancy, power, energy, ToU cost, peak demand, demand charge, and total cost derived without circular generator logic. | `evaluate_schedule` independently reconstructs spatial grid, checks contiguity, validates non-overlap, and integrates power profile directly. | **PASS** |
| **3** | **Lexicographic Optimization** | Strict multi-stage priority (A: $C_{\max} \to \sum C_j$; B: $EC \to C_{\max}$; C: $TEC \to C_{\max}$). Secondary solves restricted to primary optima. | `solve_strategy_a/b/c` explicitly filter candidates on primary optimum before evaluating secondary objective. Primary value is invariant. | **PASS** |
| **4** | **Strategy C Physical Validity** | Exemplar schedule ($M1$: $J1, J2$; $M2$: $J4, J3$) achieves $P_{\max}=27\text{ kW}$, $EC=912.60$, $TEC=1317.60$. Strictly contiguous. 27 kW is emergent, not a constraint. | Manual trace verifies all numbers. Model V1 formulation contains no constraint on $P_{\max} \le 27$. Contiguity verified programmatically. | **PASS** |
| **5** | **Break-Even & Lower Envelope** | ₹12.70/kW is verified as the true global lower-envelope transition across all feasible schedules, not a local 2-schedule crossing. | Exhaustive sweep of 248 objective points confirms Pareto front has only 2 points. Transition at $\rho=12.70$ is unique on $[0, 50]$. | **PASS** |
| **6** | **Time Discretization & Units** | Dimensionally homogeneous. Coarse 1h slot ($L=1$) clearly separated from 15-min production model. No false industrial bill claims. | All physical dimensions match. Time discretization taxonomy in Section 3 of `model_v1_preimplementation_audit.md` explicitly documented. | **PASS** |

---

## 11. Final Recommendation and Authorization

The benchmark verification artifacts have been subjected to exhaustive code-level, mathematical, and regulatory audits. 
- The enumeration is proven complete by analytical combinatorics.
- The objective functions and lexicographic hierarchies are mathematically well-posed and correctly implemented.
- The global optima ($C_{\max}^{(A)} = 4.0\text{ h}$, $EC^{(B)} = \text{₹ } 785.60$, $TEC^{(C)} = \text{₹ } 1,317.60$) and the break-even threshold ($\rho^* = \text{₹ } 12.70/\text{kW}$) are reproducible ground truth.
- No further mathematical modifications or benchmark recalculations are required.

Implementation of **Phase 3: Computational Implementation (Google OR-Tools CP-SAT)** is fully authorized.

---

## 12. Formal Audit Verdict

```
====================================================================================
FINAL AUDIT PASSED — READY FOR CP-SAT IMPLEMENTATION AUTHORIZATION
====================================================================================
```

*End of Final Code-Level Audit Report.*

