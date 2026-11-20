# OVERNIGHT-STATUS

_Last updated: 2026-11-20 ~18:25 UTC (23:55 IST), after P4 (SPEC-003 and smoke run). Branch `phase3-experiments`. GitHub has
`5d363fa`; newer commits are local until pushed (bundle provided)._

## Stage status
| Stage | Status | Evidence |
|---|---|---|
| P0: branch, pins, reproducibility | Done | Clean-env reproduction |
| P1: front, guard, gaps, billing | Done; Gate 1 passed | `FRONT-AND-BILLING.md`, `results/front_validation/` |
| P2: energy-greedy and peak-capped rules | Done | `BASELINES-AND-SCALING.md` §P2 (denominators corrected: 89 FCFS chains) |
| P3: scaling probe | Done; Gate 2 → M₂ = 12 × 4 (narrow) | `BASELINES-AND-SCALING.md` §P3; probe parts now digest-checked, missing parts accounted |
| P4: SPEC-003 and smoke run | **Done: GO recommended, awaiting your approval** | `SPEC-003-main-study.md`, `P4-SMOKE-RESULTS.md`, `results/main_smoke/` |
| P5: main run (540 + 60) | **Not started** (Gate 4: your approval) | — |
| P6–P10 | Pending | — |

## P4 in brief
* **Fixes:**
  1. P2 decomposition: the chain columns are over 89 (59) complete FCFS chains; numbers unchanged, labels and `n_chain` columns
     added.
  2. Probe docs: the guard was evaluated at ρ = 14 only, not at ρ_eq.
  3. Probe part files now carry a design-and-budget digest. Stale parts are refused; the 32 older parts are accepted via a verified
     manifest entry.
  4. Probe aggregation lists missing instances and never passes an incomplete size.

  Six regression tests were added.
* **SPEC-003 frozen:**
  * M3: 540 instances (W 0.40–0.625, γ 1 / 19/14 / 7/4, CV 0 / 0.35 / 0.75 stress, 15 seeds);
  * M4: 60 instances (12 × 4, γ 19/14, W 0.40 / 0.55 / 0.70, CV 0 / 0.35, 10 seeds);
  * pre-registered rules for break-even labels, dominance, completeness and gaps, rules vs optimiser, pairing, intervals,
    exclusions, and separate M3 / M4 interpretation;
  * digests: M3 `56e0f2f2f3455ffd`, M4 `e5bfe31d5230171c`.
* **Smoke run (36 + 12 instances):**
  * 0 missing instances and rows;
  * fronts complete 36/36 and 11/12;
  * direct C@14 = front 42/42;
  * guard ≤ B everywhere;
  * rules 100 % successful;
  * one M4 instance (W 0.70, CV 0.35) incomplete, labelled upper bound, gap ≤ 3.7 %.
* **Projection:** **2.8 h wall** (90 % interval 1.7–4.0 h): M3 1.9 h, M4 0.9 h.

## Checks (actual)
* 752 tests passed; benchmark reproduced.
* Model V1.0 and the verification scripts: zero diff.
* No earlier result file modified (`git diff -- results` empty).
* Raw data hashes unchanged: pilot `516ee522…`, cal2 `857b9f1c…`.

## Open issues
1. **Push:** the commits after `5d363fa` are in `EL-phase3-p4.bundle`. In your EL folder:
   `git fetch <bundle> phase3-experiments && git merge --ff-only FETCH_HEAD && git push origin phase3-experiments`.
2. **Gate 4 (your decision):** approve the main run, and say who runs it: me, watched within one session of about 3 h; or you,
   locally, with the commands in SPEC-003 §13.
3. **Hardware gate (D5):** answer needed by 23 Nov evening.

## Next task (after approval)
P5 main run, then P6 analysis (`analysis/` extension per SPEC-003 §§5–11) in parallel with P7 (CLI and Streamlit).
