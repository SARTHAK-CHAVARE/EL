"""Build analysis tables from ``results.csv`` (no plotting here, so it is unit-testable).

Validity rules (SPEC-002 section 6) -- every flag says WHICH proven stages the reported quantity needs:

* ``proven_stages`` = number of leading lexicographic stages proven OPTIMAL; ``status == OPTIMAL`` means ALL stages
  were proven (``proven_optimal``). ``primary_proven`` (= proven_stages >= 1) is weaker and is only enough for a
  quantity fixed by stage 1 alone (TEC of strategy C, EC of B, Pmax of P).
* ``saving_valid``  : B status OPTIMAL (B's peak, hence its TEC at rho, is defined only after its tie-break stage)
                      AND C proven_stages >= 1 (TEC_C is the stage-1 optimum).
* ``full_valid``    : B and C both status OPTIMAL (needed for peak / energy / makespan comparisons, which depend on
                      the tie-break stages).
* ``band_valid_Bmin`` / ``band_valid_Bmax``: B_minpeak / B_maxpeak status OPTIMAL (all three stages: EC, Cmax, then
                      min/max Pmax) AND C proven_stages >= 1. Robustness-band columns are NaN otherwise.
* Rows that are missing or unproven are COUNTED (``n_missing`` / ``n_unproven`` / ``n_excluded``), never dropped silently.
* TEC of rho-independent strategies is recomputed exactly as ``ec_int + 60 * rho_paise * peak_w``.
* ``rho_star_ub_*`` is an UPPER BOUND on the smallest rho at which peak-aware C beats the energy-only schedule.
* Everything produced from a design other than the validated full design is PRELIMINARY.
"""
from __future__ import annotations

import random
from typing import Dict, List, Optional, Sequence, Tuple

import pandas as pd

SCALE = 6_000_000
INSTANCE_COLS = ["instance_id", "gamma", "w_target", "w_real", "cv", "seed_idx"]
#: generation cells (strata); rho is NOT among them (repeated-measures factor evaluated on the same instances)
STRATA_COLS = ["gamma", "w_target", "cv"]
#: A percentile bootstrap resamples instances within cells; with fewer than this many instances per cell it is not a
#: meaningful interval, so summaries are then DESCRIPTIVE ONLY (no ci_lo / ci_hi columns are produced).
MIN_SEEDS_FOR_INTERVALS = 10


class AnalysisError(RuntimeError):
    pass


def load_results(path, expected_digest: Optional[str] = None) -> pd.DataFrame:
    df = pd.read_csv(path, dtype={"gamma": str, "w_target": str, "cv": str, "design_digest": str})
    digests = set(df["design_digest"].dropna().unique())
    if len(digests) != 1:
        raise AnalysisError(f"{path} mixes designs or has no digest: {sorted(digests)}")
    if expected_digest is not None and digests != {expected_digest}:
        raise AnalysisError(f"{path} digest {sorted(digests)} != manifest digest {expected_digest}")
    for c in ("makespan", "sum_completion", "peak_w", "ec_int", "dc_int", "tec_int", "energy_w_min",
              "proven_stages", "n_stages"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def _strategy_frame(df: pd.DataFrame, strategy: str, suffix: str, rho_paise: Optional[int] = None) -> pd.DataFrame:
    s = df[df.strategy == strategy]
    if rho_paise is not None:
        s = s[s.rho_paise == rho_paise]
    keep = ["instance_id", "status", "proven_stages", "n_stages", "makespan", "sum_completion", "peak_w", "ec_int",
            "wall_time_s"]
    return s[keep].rename(columns={c: f"{c}_{suffix}" for c in keep if c != "instance_id"})


def _optimal(t: pd.DataFrame, suf: str) -> pd.Series:
    """All stages proven (status OPTIMAL). NaN/missing -> False."""
    return (t[f"status_{suf}"] == "OPTIMAL") & (t[f"proven_stages_{suf}"] == t[f"n_stages_{suf}"])


def _stage1(t: pd.DataFrame, suf: str) -> pd.Series:
    return t[f"proven_stages_{suf}"] >= 1


def _reason(t: pd.DataFrame, ok: pd.Series, a: str, b: Optional[str]) -> pd.Series:
    """Why a row is excluded: 'missing' (no result row) beats 'unproven' (row exists, not proven)."""
    sufs = [a] + ([b] if b else [])
    missing = pd.Series(False, index=t.index)
    for suf in sufs:
        missing |= t[f"status_{suf}"].isna()
    return pd.Series("ok", index=t.index).mask(~ok, "unproven").mask(missing & ~ok, "missing")


def paired_table(df: pd.DataFrame) -> pd.DataFrame:
    """One row per (instance, rho): strategies side by side + validity flags + comparison metrics."""
    inst = df[INSTANCE_COLS].drop_duplicates("instance_id")
    base = inst
    for strat, suf in (("A", "A"), ("B", "B"), ("B_minpeak", "Bmin"), ("B_maxpeak", "Bmax"), ("P", "P"),
                       ("FCFS", "FCFS"), ("SPT", "SPT")):
        base = base.merge(_strategy_frame(df, strat, suf), on="instance_id", how="left")
    rhos = sorted(df[df.strategy == "C"].rho_paise.unique())
    parts = []
    for r in rhos:
        t = base.merge(_strategy_frame(df, "C", "C", r), on="instance_id", how="left")
        t["rho_paise"] = r
        parts.append(t)
    t = pd.concat(parts, ignore_index=True)

    for suf in ("A", "B", "Bmin", "Bmax", "P", "FCFS", "SPT", "C"):
        t[f"tec_{suf}"] = t[f"ec_int_{suf}"] + 60 * t["rho_paise"] * t[f"peak_w_{suf}"]

    # --- validity flags (see module docstring) ---
    t["saving_valid"] = _optimal(t, "B") & _stage1(t, "C")
    t["full_valid"] = _optimal(t, "B") & _optimal(t, "C")
    t["band_valid_Bmin"] = _optimal(t, "Bmin") & _stage1(t, "C")
    t["band_valid_Bmax"] = _optimal(t, "Bmax") & _stage1(t, "C")
    t["cost_valid"] = t["saving_valid"]                     # backwards-compatible alias
    t["excl_reason_saving"] = _reason(t, t.saving_valid, "B", "C")
    t["excl_reason_full"] = _reason(t, t.full_valid, "B", "C")
    t["excl_reason_Bmin"] = _reason(t, t.band_valid_Bmin, "Bmin", "C")
    t["excl_reason_Bmax"] = _reason(t, t.band_valid_Bmax, "Bmax", "C")

    nan = float("nan")
    t["saving_pct"] = (100.0 * (t.tec_B - t.tec_C) / t.tec_B).where(t.saving_valid, nan)
    t["saving_inr"] = ((t.tec_B - t.tec_C) / SCALE).where(t.saving_valid, nan)
    # peak / energy / makespan of B and C depend on the tie-break stages -> need BOTH fully proven
    t["peak_reduction_pct"] = (100.0 * (t.peak_w_B - t.peak_w_C) / t.peak_w_B).where(t.full_valid, nan)
    t["energy_increase_pct"] = (100.0 * (t.ec_int_C - t.ec_int_B) / t.ec_int_B).where(t.full_valid, nan)
    t["makespan_penalty_pct"] = (100.0 * (t.makespan_C - t.makespan_B) / t.makespan_B).where(t.full_valid, nan)
    # robustness band: only where the band strategy itself is fully proven (separately for min / max)
    t["tec_Bmin_valid"] = t.tec_Bmin.where(t.band_valid_Bmin, nan)
    t["tec_Bmax_valid"] = t.tec_Bmax.where(t.band_valid_Bmax, nan)
    t["saving_pct_vs_Bmin"] = (100.0 * (t.tec_Bmin - t.tec_C) / t.tec_Bmin).where(t.band_valid_Bmin, nan)
    t["saving_pct_vs_Bmax"] = (100.0 * (t.tec_Bmax - t.tec_C) / t.tec_Bmax).where(t.band_valid_Bmax, nan)
    t["rho_inr"] = t.rho_paise / 100.0
    return t


def rho_star_pair_table(df: pd.DataFrame) -> pd.DataFrame:
    """Per-instance break-even rho between an energy-only schedule (B or B_minpeak) and the min-peak extreme P.

    ``rho_star_ub_*`` = DeltaEC / (6000 * DeltaPmax) [INR/kW] is an UPPER BOUND on the smallest rho at which the
    peak-aware optimum strictly beats the energy-only schedule: at that rho the two schedules tie, so the true
    optimum there is <= the tie value, and intermediate efficient schedules can only lower the threshold.
    Needs: energy-only strategy status OPTIMAL (all stages) and P with >= 2 proven stages (Pmax and EC are fixed by
    stages 1-2; its Cmax tie-break stage is irrelevant). States: ok | unproven | missing | no_peak_reduction_possible.
    """
    base = df[INSTANCE_COLS].drop_duplicates("instance_id")
    for strat, suf in (("B", "B"), ("B_minpeak", "Bmin"), ("P", "P")):
        base = base.merge(_strategy_frame(df, strat, suf), on="instance_id", how="left")
    out = base[INSTANCE_COLS].copy()
    p_ok = base.proven_stages_P >= 2
    for suf, name in (("B", "B"), ("Bmin", "Bminpeak")):
        ok = _optimal(base, suf) & p_ok
        missing = base[f"status_{suf}"].isna() | base["status_P"].isna()
        d_ec = base.ec_int_P - base[f"ec_int_{suf}"]
        d_pk = base[f"peak_w_{suf}"] - base.peak_w_P
        val = (d_ec / (6000.0 * d_pk)).clip(lower=0.0)
        state = pd.Series("ok", index=base.index)
        state = state.mask(~ok, "unproven").mask(missing, "missing")
        state = state.mask(ok & (d_pk <= 0), "no_peak_reduction_possible")
        out[f"rho_star_ub_{name}"] = val.where(state == "ok", float("nan"))
        out[f"state_{name}"] = state
    return out


# --------------------------------------------------------------------------------- bootstrap
def bootstrap_ci(values: Sequence[float], n_boot: int = 2000, alpha: float = 0.05, seed: int = 12345
                 ) -> Tuple[float, float, float]:
    """Simple i.i.d. percentile bootstrap of a mean (generic helper; NOT used for the factorial summaries)."""
    v = [x for x in values if x == x]
    if not v:
        return (float("nan"),) * 3
    rng = random.Random(seed)
    n = len(v)
    means = sorted(sum(v[rng.randrange(n)] for _ in range(n)) / n for _ in range(n_boot))
    return sum(v) / n, means[int(alpha / 2 * n_boot)], means[int((1 - alpha / 2) * n_boot) - 1]


def stratified_cluster_bootstrap(data: pd.DataFrame, value: str, strata: Sequence[str] = tuple(STRATA_COLS),
                                 n_boot: int = 2000, alpha: float = 0.05, seed_key: str = ""
                                 ) -> Tuple[float, float, float, int]:
    """Bootstrap for the balanced, repeated-measures factorial design.

    * Resampling unit = the generated INSTANCE (cluster). All rho-rows of one instance move together, so repeated
      measures are never treated as independent replicates.
    * Resampling is done WITHIN each generation cell (gamma, W, CV), keeping every cell's size (stratified), because
      cells are fixed design points, not draws from a population of cells.
    * Statistic = unweighted mean of the cell means (every cell weighs the same, as in the balanced design), so
      that excluded/unproven instances do not re-weight the cells. Cells with no valid instance are omitted
      from the statistic and reported (4th return value = number of cells used).
    Returns (estimate, ci_lo, ci_hi, n_cells). Deterministic given ``seed_key``.
    """
    d = data[data[value].notna()]
    if d.empty:
        return float("nan"), float("nan"), float("nan"), 0
    cells: List[List[Tuple[float, int]]] = []
    for _, g in d.groupby(list(strata)):
        per_inst = g.groupby("instance_id")[value].agg(["sum", "count"])
        cells.append([(float(r["sum"]), int(r["count"])) for _, r in per_inst.iterrows()])

    def stat(cs: List[List[Tuple[float, int]]]) -> float:
        return sum(sum(s for s, _ in c) / sum(n for _, n in c) for c in cs) / len(cs)

    est = stat(cells)
    rng = random.Random(f"{seed_key}|{value}")
    boots = []
    for _ in range(n_boot):
        boots.append(stat([[c[rng.randrange(len(c))] for _ in range(len(c))] for c in cells]))
    boots.sort()
    return est, boots[int(alpha / 2 * n_boot)], boots[int((1 - alpha / 2) * n_boot) - 1], len(cells)


def summary_by(t: pd.DataFrame, by: Sequence[str], value: str = "saving_pct", valid: str = "saving_valid",
               threshold_pct: float = 1.0, n_boot: int = 2000, intervals: bool = True) -> pd.DataFrame:
    """Per group: mean of cell means (see ``stratified_cluster_bootstrap``) plus explicit exclusion accounting.

    n_total = all (instance, rho) rows in the group; n_valid = rows passing ``valid``;
    n_missing / n_unproven = excluded rows split by reason (n_excluded = their sum).
    ``intervals=False`` (used when a design has < MIN_SEEDS_FOR_INTERVALS seeds per cell) skips the bootstrap and
    emits NO ci_lo / ci_hi columns: the table is then descriptive only.
    When grouping by workload, nominal ``w_target`` and the realised ``w_real`` (mean/min/max over the group's
    instances) are both reported.
    """
    reason_col = {"saving_valid": "excl_reason_saving", "full_valid": "excl_reason_full",
                  "band_valid_Bmin": "excl_reason_Bmin", "band_valid_Bmax": "excl_reason_Bmax"}[valid]
    out = []
    for key, g in t.groupby(list(by)):
        key = key if isinstance(key, tuple) else (key,)
        gv = g[g[valid]]
        rec = dict(zip(by, key), n_total=len(g), n_valid=len(gv), n_excluded=len(g) - len(gv),
                   n_missing=int((g[reason_col] == "missing").sum()),
                   n_unproven=int((g[reason_col] == "unproven").sum()),
                   n_cells=g.groupby(STRATA_COLS).ngroups)
        if "w_target" in by:
            wi = g.drop_duplicates("instance_id")
            rec.update(w_real_mean=float(wi.w_real.mean()), w_real_min=float(wi.w_real.min()),
                       w_real_max=float(wi.w_real.max()))
        if intervals:
            est, lo, hi, ncell = stratified_cluster_bootstrap(
                gv, value, [c for c in STRATA_COLS], n_boot=n_boot, seed_key="|".join(map(str, key)))
            rec.update(n_cells_used=ncell, mean=est, ci_lo=lo, ci_hi=hi)
        else:
            d = gv[gv[value].notna()]
            cells = [c[value].mean() for _, c in d.groupby(STRATA_COLS)]
            rec.update(n_cells_used=len(cells), mean=(sum(cells) / len(cells)) if cells else float("nan"))
        rec["share_meaningful"] = float((gv[value] >= threshold_pct).mean()) if len(gv) else float("nan")
        out.append(rec)
    return pd.DataFrame(out)


def coverage_table(df: pd.DataFrame, expected_instances: Optional[int] = None) -> pd.DataFrame:
    """Instances present vs expected (a run can be partial); makes missing results visible."""
    present = df.instance_id.nunique()
    return pd.DataFrame([dict(expected_instances=expected_instances if expected_instances is not None else present,
                              present_instances=present,
                              missing_instances=(expected_instances - present) if expected_instances is not None
                              else 0)])


def runtime_table(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby("strategy").wall_time_s
    return pd.DataFrame(dict(n=g.count(), mean_s=g.mean(), median_s=g.median(), p95_s=g.quantile(0.95), max_s=g.max()))


def status_table(df: pd.DataFrame) -> pd.DataFrame:
    """Status counts per strategy, plus how many stages were proven (nothing omitted)."""
    t = df.groupby(["strategy", "status", "proven_stages", "n_stages"], dropna=False).size().rename("n")
    return t.reset_index()
