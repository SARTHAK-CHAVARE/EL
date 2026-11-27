# EL – Tariff Opti: demo script (1 Dec 2026, about 8 minutes + Q&A)

Software-only demonstration (decision D5): the hardware testbed is a design and is presented as such. Every number below
was printed by `07_src/app/cli.py` on 27 Nov 2026 (this machine). Times on your laptop will be roughly 2× longer. The
main-study slide is filled from `MAIN-RESULTS.md` once P6 is done; until then, **do not quote study-level numbers**.

## Before the demo (15 minutes earlier)
1. Open PowerShell in the EL folder, activate the environment, check, and start the app:
   ```powershell
   .venv\Scripts\Activate.ps1
   python -m pytest -q tests/test_app.py          # expect: 8 passed
   streamlit run 07_src/app/ui.py
   ```
2. **Pre-warm the cache.** Select each example once in the sidebar (Example → each name) and wait for it to solve. Afterwards,
   switching examples and moving sliders is instant.
3. **Fallback files** (in case the browser or Streamlit fails):
   ```powershell
   python 07_src/app/cli.py solve --instance examples/shop_8x3_three_options.json --out out/three_options
   python 07_src/app/cli.py solve --instance examples/shop_8x3_kerc.json --out out/kerc
   ```
   Keep the `out/` PNGs open in a viewer. The CLI prints the same tables as the app.
4. Set the sidebar to the defaults: 26 shift-days, PF 1.00, "KERC-equivalent", contract demand "renegotiated".

## 1. The problem (45 s, no screen needed)
* Karnataka HT industrial tariff (KERC HT-2(a)) has two parts:
  * a **time-of-day energy charge**: ₹6.60/kWh normal, ₹1 more in the evening peak, ₹1 less at night;
  * a **demand charge** of ₹350 per kVA per month on the month's maximum demand (at least 90 % of the contract demand).
* A scheduler that only minimises energy cost packs jobs into cheap hours, often running machines together. The energy bill
  falls, but the peak (and the demand charge) can rise.
* Our question: **when is it worth giving up some energy saving to cut the peak, and by how much?** We answer it exactly,
  with proven-optimal schedules, not rules of thumb.

## 2. Example: "8 jobs x 3 machines ... three trade-off options" (3 min)
**Schedules tab.**
* Three Gantt charts: FCFS (today's practice proxy), energy-only optimum, recommended peak-aware.
* Point out: the energy-only schedule stacks machines; the recommended one staggers them.

**Power over the shift tab.**
* The tariff bands are shaded. Peaks: FCFS and energy-only **47 kW**, recommended **25.57 kW**.

**Comparison tab** (₹ per shift at the KERC-equivalent ₹13.46/kW):

| Approach | Total |
|---|---|
| FCFS | 2,140.42 |
| Energy rule | 1,724.42 |
| Peak-capped rule | 1,516.32 |
| Energy-only optimum (B) | 1,544.42 |
| **Recommended** | **1,309.33** |

* The recommended schedule is **38.8 % below FCFS**, and it is **proven optimal**.
* It is also about 14 % below the best simple rule, so here the optimiser clearly earns its place.

**Trade-off tab.**
* The front has three proven options:
  * 47 kW at ₹911.80 energy;
  * 32 kW at ₹938.80;
  * 25.57 kW at ₹965.15.
* Each option is best over a range of demand charge: up to ₹1.80/kW, then ₹1.80–4.10, then above ₹4.10.

**Live interaction (the key moment).** In the sidebar choose "Custom" and move the slider:

| Slider (₹/kW per shift) | Recommended peak |
|---|---|
| 1.5 | 47 kW (same as energy-only) |
| 2.0 | 32 kW |
| 4.5 | 25.57 kW |

* The schedule switches exactly at the break-even values, and it is instant, because the whole front was solved once.
* Return the setting to "KERC-equivalent".

## 3. Same idea, the bill (1.5 min). Example: "8 jobs x 3 identical 15 kW machines, KERC ... workload 0.625"
**KPIs.**
* Peak demand **47 → 32 kW**.
* Break-even **₹6.00/kW per shift (exact)**, below the KERC-equivalent ₹13.46, so the peak cut pays at KERC rates.
* Here the peak-capped rule happens to match the optimum. Say so: the optimiser also tells you *when* a simple rule is
  already good enough.

**Monthly bill tab** (26 days, PF 1; partial bill):

| Contract demand | Saving vs energy-only |
|---|---|
| Renegotiated | **₹2,910 per month** |
| Fixed | **−₹695 per month** (the bill goes up) |

* **Key insight.** KERC bills at least 90 % of the contract demand.
* If the plant cuts its peak but keeps its old contract, the demand charge cannot fall below that floor, while energy
  costs a little more.
* So peak shaving only pays once the contract demand is renegotiated.
* Say clearly: "partial monthly bill estimate: demand charge plus this shift's energy; no fixed charges or taxes."

## 4. When nothing can be gained (45 s). Example: "8 jobs x 3 machines where no peak reduction is possible"
* The app says: **"No peak reduction is possible (proven)."** The energy-only schedule is optimal at every demand charge.
* Why: the minimum peak (18.222 kW) equals our **structural lower bound**. The total work forces at least that much
  machine overlap, so the solver can certify there is nothing left to shave.
* At its extreme this becomes the workload theorem: if work exceeds (M−1)/M of machine capacity, no peak reduction is possible
  at all. A plant can tell in advance when peak-aware scheduling is pointless.

## 5. Bigger shop and any instance (1 min)
**Example "12 jobs x 4 identical 15 kW machines".**
* The front has three options: 62 → 47 → 32 kW.
* Break-even ₹2.00/kW. Renegotiated saving **₹7,672.50 per month**; fixed −₹657.50.
* Solved in about 10 s here.

**Generate.**
* Pick a size and seed and press Solve to show it works on an unseen instance.
* The tool never returns anything worse than the energy-only schedule. This "guard" is checked by an independent evaluator.

**Upload JSON.** Instances are plain JSON (see `examples/`), so a plant's own jobs and machines can be entered.

## 6. Main study (1 min): 540 instances of 8 × 3 plus 60 of 12 × 4 (MAIN-RESULTS.md)
Show figures F1 and F4 from `results/main_analysis/figures/`. Speak to four numbers (CV ≤ 0.35, KERC ρ ₹13.46, all exact):
* **A lower peak is possible in 79 % of instances.** In almost all of them it already pays at KERC rates; the exact
  break-even median is ₹3.18/kW per shift.
* **Shift cost falls 7.2 % [6.8, 7.6] vs the energy-only optimum,** worth **₹3,345 per month** on the partial bill
  **if contract demand is renegotiated**.
* **With a fixed contract demand only ₹127 per month remains.** KERC's 90 % floor eats it, and at high workload the
  result is negative.
* **Simple rules are near-optimal only when all jobs draw the same power.** Otherwise the optimiser is 13–21 % cheaper on
  average.
* **The 12 × 4 shop shows the same picture:** a 9.3 % saving, ₹5,491 per month renegotiated vs ₹242 fixed.

## 7. Honest scope (say it before they ask)
* **Hardware:** a 12 V testbed was designed but not built. Nothing was physically measured; this is a software demonstration.
* **Bills:** partial estimates (demand charge + scheduled energy), assuming the same schedule every shift-day.
* **Instances:** synthetic, from a documented generator. They are not a specific plant's data; we do not claim plant-level
  savings.
* **Model:** 15-minute slots, unrelated parallel machines, no setups or breakdowns; the KERC tariff as published.

## Likely questions (short answers)
* **"Is it really optimal?"**
  * CP-SAT proves optimality; the app shows "proven" per row.
  * Unproven results are labelled FEASIBLE and never reported as optimal.
  * The front is cross-checked against direct solves.
* **"How long does it take?"** Seconds for these sizes (here 2–10 s per instance; laptop about 2× that). Main-study runtime
  statistics will be in MAIN-RESULTS.md.
* **"Why not just use a rule?"**
  * Sometimes a rule is enough (the KERC example).
  * Sometimes it is not: on the three-options example the optimum is about 14 % cheaper than the best rule.
  * The tool tells you which case you are in.
* **"What if the contract demand can't change?"** Then use the "fixed" view. The tool shows the real effect, including when
  peak cutting costs money.
* **"Does it scale?"**
  * 12 × 4 is solved exactly in seconds.
  * Larger shops will need time limits; the tool then reports bounds, not false optimality.
