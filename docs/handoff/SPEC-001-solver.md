# SPEC-001 — CP-SAT Solver Implementation Specification

| | |
|---|---|
| **Status** | FINAL for Phase 3 implementation (decisions D1–D8 adopted, see §10) |
| **Date** | 2026-11-15 |
| **Source model** | `04_mathematical_model/formulation/mathematical_model_v1.md` (Model V1.0, **unchanged**) |
| **Cross-checked against** | `verify_benchmark.py`, `hand_calculations.md`, `assumptions.md`, `tariff_reference.md`, `model_v1_preimplementation_audit.md` |
| **Implementation** | `07_src/model/` · tests in `tests/` |

This document specifies *how Model V1.0 is implemented*. It does not change the research model.
Where Model V1.0 text is ambiguous or inconsistent, this spec states the implemented
interpretation (§9 lists every such case). Model V1.0 itself is left untouched.

---

## 1. Conventions

* **Slots are 1-based**: slot `t ∈ {1..T}`. A job starting at slot `s` with duration `p` occupies
  slots `s … s+p-1`; its completion time is `C_j = s + p − 1` (the last occupied slot). This matches
  Model V1.0 Eq. (7) and `verify_benchmark.py`. No 0-based indexing exists anywhere in the code.
* `D ≤ T` is the global deadline (last usable slot). `r_j` (release) is 1-based, `d_j ≤ D` is the
  job due slot (default `D`).
* **All optimisation arithmetic is integer.** Floating point never enters a CP-SAT expression.
  Inputs given in kW / ₹ are converted once, exactly, with `decimal.Decimal` (§4).
* Power inside the engine is integer **watts**; tariffs are integer **paise/kWh**;
  `Δt` is integer **minutes**.

## 2. Decision variables (D1: time-indexed formulation)

| Symbol | CP-SAT object | Domain | Meaning |
|---|---|---|---|
| `x[j,m,t]` | `BoolVar`, created **only** for valid triples | `m ∈ M_j`, `r_j ≤ t ≤ min(D,d_j) − p_jm + 1` | job `j` **starts** on machine `m` in slot `t` |
| `y[j,m,t]` | *linear expression* (no variable) | `Σ_{t'=max(t−p_jm+1, r_j)}^{t} x[j,m,t']` ∈ {0,1} | job `j` is processing on `m` in slot `t` (Eq. 5) |
| `z[j,m]` | derived `Σ_t x[j,m,t]` | {0,1} | assignment (Eqs. 1–2 merged) |
| `C_j` | `IntVar` | `[r_j + min_m p_jm − 1, min(D,d_j)]` | completion slot (Eq. 7) |
| `C_max` | `IntVar` | `[max_j (r_j+min_m p_jm−1), D]` | makespan, **equality** with `max_j C_j` |
| `P_t` | `IntVar` per slot, `= P̃_base + Σ P̃_jm·y[j,m,t]` | `[P̃_base, P̃_base + Σ_m max_j P̃_jm]` | aggregate power in slot `t`, W (Eq. 11) |
| `P_max` | `IntVar`, `AddMaxEquality(P_max, [P_1..P_T, P̃_base])` | same range | peak demand, W (Eq. 14, **exact**; D3) |

Eqs. (3), (4), (8) are satisfied *by construction*: an `x` that would violate them is never created.
If a job has **no** valid `(m,t)`, the instance is infeasible and is reported as such without calling
CP-SAT (§7).

## 3. Constraints (all linear, no big-M)

| Model eq. | Implementation |
|---|---|
| (1)–(2) | `∀j: AddExactlyOne({x[j,m,t]})` |
| (5) | `y` expression above (non-preemption by construction) |
| (6) | `∀m,t: AddAtMostOne({x[j,m,t'] : slot t covered by (j,m,t')})` |
| (7) | `C_j == Σ_{m,t} (t+p_jm−1)·x[j,m,t]` |
| (9)–(10) | `AddMaxEquality(C_max, {C_j})`, domain `≤ D` |
| (11) | `P_t == P̃_base + Σ P̃_jm·y[j,m,t]` |
| (12)–(14) | **`L = 1` only** (D5): window = one slot, `P_max == max_t P_t` |

**Redundant constraints (implemented, `build_formulation(redundant=True)`, default).** To speed up
proofs on low-workload instances, the formulation adds, *without changing the feasible set*: per machine a
`NoOverlap` over optional fixed-size intervals (start `s_jm`, size `p_jm`, presence `z_jm`), and a
`Cumulative` over all optional intervals with demand `P_jm` and capacity `P_max − base`. The oracle and
benchmark tests run with the default. Setting `redundant=False` gives the pure linear model and is covered
by tests to give identical optima.

## 4. Integer scaling (D2) — supersedes Model V1.0 §8.2

Model V1.0 §8.2 scales EC without `Δt` and DC without a matching factor, so EC and DC cannot be added
when `Δt ≠ 1 h`. SPEC-001 uses one common scale:

| Quantity | Integer form |
|---|---|
| power | `P̃ = round(1000·P_kW)` W (input must be exact at 1 W) |
| tariff | `C̃_t = round(100·C_t)` paise/kWh (input must be exact at 1 paise) |
| demand-charge intensity | `ρ̃ = round(100·ρ)` paise/kW |
| slot length | `Δt_min` minutes (integer) |
| **energy cost** | `EC_int = Σ_t C̃_t · Δt_min · P_t` |
| **demand charge** | `DC_int = 60 · ρ̃ · P_max` |
| **total** | `TEC_int = EC_int + DC_int` |
| **conversion** | `₹ = int / 6 000 000` (= 100·1000·60) |

Derivation: `EC[₹] = Σ C_t[₹/kWh]·P_t[kW]·Δt[h] = Σ (C̃/100)(P̃/1000)(Δt_min/60)`, hence
`EC_int/6e6`. `DC[₹] = ρ[₹/kW]·P_max[kW] = (ρ̃/100)(P̃_max/1000)`, hence `60·ρ̃·P̃_max/6e6`.
Worked check (benchmark, slot 1 of Schedule B): `560·60·37000/6e6 = ₹207.20 = 5.60×37`.

**Overflow guard:** `validate_instance` bounds `TEC_int` from above (all slots at the highest tariff and
the maximum possible power, plus `DC_int` at the maximum peak) and rejects instances whose bound exceeds
`10^17` (CP-SAT int64 safety margin). The benchmark's bound (ρ=₹15/kW) is ≈ 1.68·10^10 (`tec_upper_bound`).

## 5. Objective hierarchy and optimisation sequence

All strategies share the identical feasible set (§2–3). A strategy is an ordered list of stages.
Stage *k* minimises (or maximises) an expression subject to every earlier stage being fixed at its
achieved value (`≤` for min stages, `≥` for max stages — exact integers, no ε-weights).
Each stage is a **fresh model** (no stale state); the previous stage's solution is passed as a hint.

| Strategy | Stage 1 | Stage 2 | optional Stage 3 (D4) |
|---|---|---|---|
| **A** production baseline | min `C_max` | min `ΣC_j` | — |
| **B** energy-cost-only (ρ ≡ 0) | min `EC_int` | min `C_max` | `B_minpeak`: min `P_max` · `B_maxpeak`: max `P_max` |
| **C** peak-aware (ρ>0) | min `TEC_int(ρ)` | min `C_max` | — |
| **P** min-peak extreme point (analysis only) | min `P_max` | min `EC_int` | min `C_max` |

* Strategy **B is exactly Strategy C with ρ = 0** (same definition of stages). Test: `C(ρ=0)` and `B`
  agree on every metric.
* **A, B, C contain no information from each other** (A has no cost term; B has no peak term).

### Why B's tie-break matters (D4)
B's stage 2 minimises `C_max` only. Among EC- and makespan-optimal schedules the peak is *not*
determined, so a plain B run returns an arbitrary member of that set. To keep the comparison defensible
the runner also computes `B_minpeak` (best case for B) and `B_maxpeak` (worst case). The headline
"peak-aware benefit over energy-cost-only" is reported against **plain B (the documented definition)**,
with the `B_minpeak … B_maxpeak` band reported as the tie-break robustness check. On the canonical
benchmark all three coincide (12 tied B optima, all `P_max = 37 kW`).

## 6. Solver status and optimality policy (D7)

Per stage the CP-SAT status is mapped to `OPTIMAL | FEASIBLE | INFEASIBLE | UNKNOWN | MODEL_INVALID`.
Strategy-level status:

| Condition | Strategy status | `proven_optimal` |
|---|---|---|
| all stages `OPTIMAL` | `OPTIMAL` | **True** |
| a stage is `INFEASIBLE` at stage 1 | `INFEASIBLE` | False |
| stage 1 `UNKNOWN` (timeout, no solution) | `UNKNOWN` (no schedule) | False |
| a solution exists but some stage is not proven | `FEASIBLE` (schedule returned, lexicographic guarantee void) | **False** |
| `MODEL_INVALID` | `MODEL_INVALID` | False |

A `FEASIBLE` result is **never** reported as `OPTIMAL`.

**Stop rule (correctness pass, 2026-11-15).** The lexicographic hierarchy advances to stage k+1 only if stage k
returned `OPTIMAL`; only proven values are frozen as bounds (`expr ≤ v` for min stages, `≥ v` for max stages).
If a stage returns `FEASIBLE` (or `UNKNOWN`/anything else), later stages are **not run**, the best schedule found so
far is returned with status `FEASIBLE`, and `reason` says which stage stopped the hierarchy. Before this rule a
non-proven stage value could be frozen as an exact bound and a later stage optimised over it, silently mixing
proven and unproven values. `StrategyResult.proven_stages` counts the leading proven stages; `n_stages` the defined
ones; `proven_optimal ⇔ status == OPTIMAL ⇔ proven_stages == n_stages`. Experiment statistics must filter
`status == OPTIMAL`; non-optimal rows are kept in the CSV with their status and best bound.

**`primary_proven` (added in Stage 4).** `StrategyResult.primary_proven` is true iff stage 1 (the strategy's
primary objective: min Cmax for A, min EC for B, min TEC for C, min Pmax for P) was `OPTIMAL`. It is *not* an
optimality claim for the strategy (that remains `status`/`proven_optimal`); it only records that the
**cost** value is proven although a later compactness tie-break stage (min Cmax) may not be. Cost-based
analyses use `primary_proven`; makespan-based analyses require `status == OPTIMAL`.
`SolverConfig.tiebreak_time_limit_s / tiebreak_deterministic_time_limit` bound stages ≥ 2 separately.

Defaults (`SolverConfig`): `num_workers = 1` (reproducible, parallelism is at process level),
`random_seed = 0`, per-stage `max_time_in_seconds = 60` plus a `max_deterministic_time` limit so that
results do not depend on machine load. With a single worker and no limit hit, results are deterministic.

## 7. Independent metric evaluation

After solving, the schedule (list of `(job, machine, start, end)`) is passed to
`evaluate_schedule`, which **does not import the formulation or CP-SAT**. It:
1. checks feasibility (every job exactly once, eligible machine, duration `p_jm`, release/due/deadline,
   no machine overlap, slot bounds) and returns the list of violations;
2. rebuilds the power profile, `C_max`, `ΣC_j`, `P_max`, energy (Wh exact), `EC_int`, `DC_int`, `TEC_int`
   with integer arithmetic.

The solver then compares its own stage expressions with the evaluator for the final schedule; any
mismatch raises `InternalConsistencyError`. **Reported metrics always come from the evaluator.**

Infeasible/degenerate instances: a job with no valid placement, or a CP-SAT `INFEASIBLE` stage 1, yields
`INFEASIBLE` with an explanatory `reason`; malformed input raises `InstanceError` with all problems
listed.

## 8. Benchmark reproduction (acceptance criteria)

Instance (`tests/benchmark_instance.py`, **not** in the solver): `T = D = 8`, `Δt = 60 min`, `L = 1`,
`P_base = 2 kW`; machines `M1 = 10 kW`, `M2 = 25 kW`; jobs `J1..J4` with `p` on (M1, M2) =
(2,2), (3,2), (2,1), (3,2); tariff slots 1–8 = 5.60, 5.60, 7.60, 7.60, 7.60, 6.60, 6.60, 6.60 ₹/kWh
(illustrative block sequence, ISS-08); `ρ = 15 ₹/kW`.

| Strategy | Required metrics (tested as metrics, not schedules) |
|---|---|
| A | `C_max = 4`, `ΣC_j = 12`, `EC = ₹1031.60`, `P_max = 37 kW`, `TEC = ₹1586.60` |
| B | `EC = ₹785.60` (`4 713 600 000`), `C_max = 8`, `P_max = 37 kW`, `TEC = ₹1340.60` |
| C | `TEC = ₹1317.60` (`7 905 600 000`), `EC = ₹912.60`, `P_max = 27 kW` |
| ρ*(pair) | `(912.60 − 785.60)/(37 − 27) = ₹12.70/kW` |

Additional checks: `TEC*` equals the enumerated global minimum at ρ ∈ {0, 5, 10, 12, 14, 15, 20, 30};
the min-peak solve gives `(27 kW, ₹912.60)` (same ρ*); every solver schedule belongs to the verifier's
set of optimal schedules. (Do not test at ρ = 12.70 exactly: B and C tie.)

## 9. Ambiguities / inconsistencies found and how they are resolved

| # | Finding | Resolution in this spec |
|---|---|---|
| 1 | Model V1.0 §8.1 sketch uses 0-based `NewIntVar(r_j, D−p)` while §5 is 1-based (off-by-one if `r_j` is 1-based) | 1-based everywhere (§1). §8.1 is treated as illustrative only. |
| 2 | §8.1 time-slot indicator uses one-directional `OnlyEnforceIf` (a minimiser could switch it off and hide power) | exact time-indexed `x/y` formulation (D1) |
| 3 | Equation numbers (20) and (22) do not exist; `hand_calculations.md` cites "(1)–(22)" | spec refers to Eqs. (1)–(19), (21) only |
| 4 | §8.2 scaling omits `Δt` / mismatched EC–DC scales | §4 common-scale fix |
| 5 | B's tie-break is makespan only | §5 band (D4) |
| 6 | `L > 1` gives fractional averages; sliding windows undefined | `L = 1` only (D5); `L>1` out of scope |
| 7 | Base load is billed over the whole horizon `T` (not up to `C_max`) | implemented as in the verifier (constant offset; affects % savings, not argmin) — must be stated in reports |
| 8 | Generator parameters (p_jm, P_jm, N, M, γ, ρ levels, W) not defined in V1.0 | SPEC-002 |
| 9 | `tariff_reference.md`: ToD adjustments apply **Dec–June only** (July–Nov zero); V1.0 / README use ±₹1.00 year-round; master plan says ±20 % and ₹365/kVA | `tariff_reference.md` is authoritative for values; experiments are the *normalised research model (Model A)*, not a bill |
| 10 | `W = Σ min_m p_jm /(M·D)` assumes every job on its fastest machine | defined explicitly in SPEC-002 and the *realised* value is recorded |
| 11 | README says H3 "±5 %" and H2 "monotonic" more strongly than the plan (H4: error bound determined by experiment) | not changed here; flagged for the report |

### Demand charge and monthly tariff interpretation
`DC = ρ · P_max` is **Model A (normalised research benchmark)**: `ρ` in ₹/kW *per scheduling horizon*,
`P_max` = peak active power (kW) over `L = 1` windows. It is **not** a monthly KERC bill (Model B:
₹350/kVA/month, `BD = max(MD, 0.9·CD)`, kVA ≠ kW unless PF = 1). A daily schedule only moves the
monthly bill if that day sets the monthly maximum, and nothing is saved if `MD ≤ 0.9·CD`. Reports
must therefore express ρ as a sweep (e.g. `350/N_shifts`) and not claim monthly savings.

## 10. Decisions (D1–D8) — adopted under delegated authority, all reversible

| ID | Decision |
|---|---|
| D1 | time-indexed formulation (literal Eqs. 1–17) |
| D2 | Δt-aware common scale `6 000 000` |
| D3 | `AddMaxEquality` for `P_max` and `C_max`; reported metrics always recomputed independently |
| D4 | B = documented two-stage definition; `B_minpeak`/`B_maxpeak` reported as a robustness band |
| D5 | demand window `L = 1` only |
| D6 | two time profiles: `benchmark` (T = 8, Δt = 60 min) and `experiment` (Δt = 15 min, T = D = 32; SPEC-002) |
| D7 | status policy §6; workers = 1; deterministic time limit; FEASIBLE ≠ OPTIMAL |
| D8 | ρ* from two schedules is named `rho_star_pair`: an **upper bound** on the true switching ρ when intermediate efficient schedules exist; `rho_star_exact` (peak-cap sweep) is a stretch item |

### Still unresolved (documented, not blocking)
* Final ρ levels for the factorial (SPEC-002 proposes {5, 14, 50} ₹/kW) — confirm with mentor.
* Which clock window / season the 32-slot experiment tariff should represent (SPEC-002 proposes the
  16:00–24:00 evening shift in a Dec–June ToD day, the only 8-hour window that contains all three
  tiers).
* Whether the report should present ρ in ₹/kW/horizon or ₹/kVA/month equivalents (or both).
