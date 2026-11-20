# SPEC-002 — Experiment design, generator and analysis rules (v1)

Status: **design documented and pipeline validated on a smoke design; the full factorial has NOT been run.**
Revision 2 (2026-11-15): correctness pass — W definition fixed, ρ clarified as repeated-measures, strict validity/bootstrap/runner rules.
Everything produced so far from the smoke design is **PRELIMINARY pipeline validation, not a research result.**
Code: `07_src/experiments/{design,generator,baselines,runner}.py`, `07_src/analysis/{tables,report}.py`.

## 1. Question
How much total energy cost (EC + ρ·Pmax, Model A) does the peak-aware strategy C save over the
energy-only strategy B, and how does that depend on tariff spread γ, workload W, machine-power
heterogeneity CV and demand-charge intensity ρ? What does it cost in makespan and energy cost?

## 2. Factors (`DESIGN_FULL`, version `SPEC-002/v1`)

**Two kinds of factor — this matters for the analysis.**
* **Instance-generation factors (between-instance): γ, W, CV.** Their 3×3×3 = 27 combinations are the
  *generation cells*; each cell gets 15 independently generated instances (seeds). Instances in different cells
  are different random draws.
* **ρ is a repeated-measures (within-instance) factor.** It is **not** a generation factor: every generated
  instance is solved at **all three ρ levels** (strategy C re-solved per ρ; A, B, B_minpeak, B_maxpeak, P, FCFS, SPT
  do not depend on ρ and are solved once). The three ρ results of one instance are therefore *paired and
  correlated*. Total = 27 cells × 15 instances = **405 instances**, evaluated at 3 ρ = 1215 (instance, ρ) comparisons,
  but only **405 independent replicates** (15 per cell). The analysis resamples instances, never individual ρ rows
  (§6).

| Factor | Role | Levels | Meaning |
|---|---|---|---|
| γ | generation cell | 1, 19/14, 7/4 | peak/off-peak price ratio; 19/14 = KERC HT-2(a) (₹7.60/₹5.60); 1 = flat-tariff control |
| W | generation cell | 0.40, 0.70, 0.90 | workload, **defined below** |
| CV | generation cell | 0, 0.35, 0.75 | coefficient of variation of machine power (mean preserved at 15 kW, floor 0.5 kW) |
| ρ | repeated measure | ₹5, ₹14, ₹50 per kW per horizon | evaluated on the *same* instance |
| seed | replicate | 15 per cell | independent instance within a cell |

**Workload definition (single definition, used by the generator, the metadata and the tests):**

    W = Σ_j min_m p_jm / (M·T)

p_jm in slots, M machines, T slots in the horizon (D = T). It is the fraction of the machines' time capacity that
is needed if every job ran on its fastest machine — a time-based utilisation lower bound, computed exactly by
`experiments.generator.workload_w`. It deliberately does **not** include machine power: W says how busy the shop
is, CV says how different the machines' powers are, and mixing power into W would confound the two factors.
`w_target` is the nominal level; the generator scales continuous processing times to hit it and then rounds to
integer slots (clamped to [1, D]), so the realised `w_real = workload_w(instance)` (stored in the CSV) differs by at
most about n/(2·M·T) ≈ 0.04. Analyses group by the nominal level.

Fixed: 8 jobs, 3 machines, T = 32 slots of 15 min, D = T, base load 2 kW, normal-tier ₹6.60,
shift starting 16:00 (KERC clock → off/normal/peak blocks), processing-time noise ×U(0.7,1.3).
**ρ levels are placeholders spanning below/around/above the benchmark ρ* = ₹12.70** — unresolved decision U2.

Tariff construction: normal = ₹6.60 fixed; off = 2·normal/(1+γ); peak = γ·off, so the mean of the
off/peak pair equals the normal price and γ is varied at constant average price (checked exactly:
γ=19/14 → ₹5.60/6.60/7.60).

## 3. Generator (`generate_instance`)
Deterministic: `random.Random("<base_seed>|<cell>|<seed_idx>")` (string seeding → independent of Python hash
randomisation and worker count). Draw base processing times and per-machine multipliers, scale to the target W (formula in §2),
round to integer slots, **accept only if FCFS or SPT produces a schedule within D** (guarantees a feasible
instance exists), retry up to `max_attempts`, else raise `GeneratorError`. Realised workload `w_real` and attempts
are recorded in the CSV. Selection bias: at W = 0.9 acceptance is ≈ 10 %, so instances are slightly easier than
the nominal cell; this is a stated limitation, not hidden.

## 4. Strategies and baselines per instance
A (min Cmax→ΣCj), B (min EC→Cmax) plus tie-break variants **B_minpeak / B_maxpeak** (best/worst peak among
EC-optimal schedules, quantifying the ambiguity of B), P (min Pmax→EC→Cmax), C at each ρ, and two non-optimising
baselines **FCFS** and **SPT** (non-delay list scheduling onto the machine with earliest completion; status
`HEURISTIC`, or `NO_SCHEDULE` if the deadline is missed — heuristic failure is data, not an error).

## 5. Runner
`python 07_src/scripts/run_experiment.py --design smoke|full --out DIR [--workers N] [--limit K] [--force]`
One atomic part file per instance (`parts/<id>.csv`, temp-file + rename), `manifest.json` carrying the design
digest, `results.csv` = sorted aggregate. **Design identity is enforced three ways:** (1) every row carries
`design_digest`; a part counts as done only if its digest equals the current design's; (2) a different design in
the same `--out` is refused, also when the manifest is missing or was hand-edited (foreign part files are detected
by their own digest); (3) `aggregate` refuses to merge parts of another digest. `--force` on a *changed* design
**archives** the old `parts/`, `results.csv`, `manifest.json` to `<out>/superseded/<old digest>/` (nothing is deleted)
and starts from scratch — old results are never reused; `--force` on an identical design is a no-op. The digest
covers all design fields (including solver budgets) and `DESIGN_VERSION`. Resume skips finished instances and
removes stale temp files. Columns include seeds, status per row, `proven_optimal`,
`primary_proven`, per-stage statuses/times, wall time, all metrics in integers (₹ = int/6·10⁶). Tests:
determinism (identical `results.csv` except `wall_time_s`, also across worker counts), resume after simulated kill,
manifest guard.

Solver budgets (full): stage 1 180 s wall / 60 s deterministic; tie-break stages 60 s / 15 s; 1 worker per solve,
parallelism across instances. Worst-case bound = 405 × 8 solves × (180 + 2·60) s ≈ 9.7·10⁵ CPU-s; the realistic
cost is **unmeasured** (smoke: median solve 0.6–4 s, worst 18 s at N=6). The recommended pilot **was executed on 2026-11-15** (`PILOT-RESULTS.md`: 50.8 s CPU per instance, effective limits are
the deterministic 60 s / 15 s ones); a revised calibration design is proposed in `SPEC-002-v2-proposal.md`. This v1 text is kept
unchanged otherwise.

## 6. Validity rules for analysis (`analysis/tables.py`)
**Flags are never interchangeable.** `status == OPTIMAL` / `proven_optimal = 1` means *every* lexicographic stage
was proven. `proven_stages` = number of leading stages proven; `primary_proven` (= `proven_stages ≥ 1`) is only the
first stage. The solver stops at the first stage that is not OPTIMAL (later stages never run, `n_stages` records how
many were defined).

| Output | Needs |
|---|---|
| saving % (TEC_B − TEC_C)/TEC_B | B `status == OPTIMAL` (B's peak, hence TEC_B at ρ, is fixed only by its makespan tie-break) **and** C `proven_stages ≥ 1` (TEC_C is the stage-1 optimum) → flag `saving_valid` |
| peak reduction, energy increase, makespan penalty | B **and** C `status == OPTIMAL` → `full_valid` |
| robustness band vs B_minpeak / vs B_maxpeak | that band strategy `status == OPTIMAL` (all 3 stages) and C `proven_stages ≥ 1`; **separate flags** `band_valid_Bmin`, `band_valid_Bmax`; band columns are NaN otherwise |
| ρ*_ub (break-even) | energy-only strategy (B or B_minpeak) `status == OPTIMAL` and P `proven_stages ≥ 2` |

* **Nothing is silently omitted.** Every summary table reports `n_total`, `n_valid`, `n_excluded` = `n_missing`
  (no result row) + `n_unproven` (row exists but a required stage is unproven); `coverage.csv` reports instances
  present vs expected; `status_counts.csv` lists every (strategy, status, proven_stages).
* TEC of ρ-independent strategies is recomputed exactly as `ec_int + 60·ρ_paise·peak_w`.
* **Intervals.** 95 % **stratified cluster bootstrap** (2000 resamples, deterministic seed): the resampling unit is
  the generated instance (all its ρ rows move together — ρ is repeated-measures), resampling happens *within* each
  γ×W×CV cell (cells are fixed design points), and the statistic is the **unweighted mean of cell means**, which is
  the estimand of the balanced design and is not re-weighted when exclusions unbalance the cells. Cells without any
  valid instance are omitted and counted (`n_cells_used` vs `n_cells`). `share_meaningful` is a pooled share and
  carries no interval.
* **Break-even is an upper bound.** `rho_star_ub = ΔEC/(6000·ΔPmax)` between an energy-only schedule and the
  min-peak extreme point P is an **upper bound on the smallest ρ at which peak-aware C strictly beats the
  energy-only schedule** (at that ρ the two tie, so the true optimum is ≤ the tie; intermediate efficient
  schedules can only lower the threshold). Columns/figures are named `rho_star_ub_*` and labelled "UPPER BOUND";
  it is not an estimate of the exact threshold.
* Every figure/table is stamped `PRELIMINARY` unless `--validated`, the design name is `full`, the digest matches
  the manifest, and **no instance is missing**.
* ρ-dependence is reported for Model A (normalised); Model B (real ₹/kVA/month) is not covered here.

## 7. Open decisions
U1 (resolved in rev. 2) W is the time-based Σ_j min_m p_jm/(M·T); power enters only through CV.
U2 ρ levels (₹5/14/50). U3 final time budgets and instance size after pilot. U4 whether 8×3×32 is large
enough to show differences between strategies on KERC γ (smoke at ρ=₹50: savings 0 on the 2 valid instances).
