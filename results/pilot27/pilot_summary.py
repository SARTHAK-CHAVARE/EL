"""Detailed pilot summary (PRELIMINARY). Reads results/pilot27/results.csv + analysis/paired_instances.csv.
Usage: python results/pilot27/pilot_summary.py > results/pilot27/analysis/pilot_summary.txt"""
import sys
from pathlib import Path
import pandas as pd
pd.set_option("display.width", 220); pd.set_option("display.max_columns", 40); pd.set_option("display.float_format", "{:.2f}".format)
root = Path(__file__).resolve().parent
sys.path.insert(0, str(root.parents[1] / "07_src"))
from analysis.tables import load_results, paired_table, summary_by, rho_star_pair_table
df = load_results(root / "results.csv"); t = paired_table(df); rs = rho_star_pair_table(df)
opt = df[df.strategy.isin(["A","B","B_minpeak","B_maxpeak","P","C"])].copy()
opt["cell_w"] = opt.w_target
print("## 1 optimality by strategy (rows; OPTIMAL = all stages proven)")
g = opt.groupby("strategy").agg(n=("status","size"), optimal=("status", lambda s:(s=="OPTIMAL").sum()),
    stage1_proven=("proven_stages", lambda s:(s>=1).sum()), max_wall=("wall_time_s","max"))
g["optimal_pct"] = 100*g.optimal/g.n; g["stage1_pct"]=100*g.stage1_proven/g.n; print(g)
print("\n## 2 stage-wise completion: (strategy, proven_stages/n_stages) counts, unproven stage runtime")
print(opt.groupby(["strategy","proven_stages","n_stages","status"]).agg(n=("status","size"), wall_mean=("wall_time_s","mean"), wall_min=("wall_time_s","min"), wall_max=("wall_time_s","max")))
print("\n## 3 runtime (s) by strategy"); print(opt.groupby("strategy").wall_time_s.describe(percentiles=[.5,.95])[["count","mean","50%","95%","max"]])
print("\n## 3b runtime of proven vs unproven rows"); opt["proven"]=opt.status=="OPTIMAL"; print(opt.groupby(["strategy","proven"]).wall_time_s.agg(["count","mean","median","max"]))
print("\n## 4 runtime of C and P by gamma / W / CV (mean, median, max; share not fully OPTIMAL)")
for col in ["gamma","w_target","cv","rho_paise"]:
    s = opt[opt.strategy.isin(["C"]) | (opt.strategy=="P")].copy()
    s["notopt"]=(s.status!="OPTIMAL").astype(int)
    print(f"-- by {col}"); print(s.groupby(["strategy",col]).agg(n=("notopt","size"), mean_s=("wall_time_s","mean"), median_s=("wall_time_s","median"), max_s=("wall_time_s","max"), not_optimal=("notopt","sum")))
print("\n## 5 savings of C vs B (%), stratified cluster bootstrap, per rho (valid rows only)"); print(summary_by(t,["rho_inr"]).drop(columns=["n_cells"]))
print("\n## 5b raw saving_pct per instance x rho (valid)"); print(t[t.saving_valid].pivot_table(index=["gamma","w_target","cv"], columns="rho_inr", values="saving_pct"))
print("\n## 5c share of valid instance-rho rows with saving >= 1%, >0%"); v=t[t.saving_valid]; print(v.groupby("rho_inr").saving_pct.agg(lambda s:(s>=1).mean()), v.groupby("rho_inr").saving_pct.agg(lambda s:(s>0).mean()))
print("\n## 5d mean saving by gamma x rho"); print(v.pivot_table(index="gamma", columns="rho_inr", values="saving_pct", aggfunc="mean"))
print("\n## 5e mean saving by W x rho"); print(v.pivot_table(index="w_target", columns="rho_inr", values="saving_pct", aggfunc="mean"))
print("\n## 5f mean saving by CV x rho"); print(v.pivot_table(index="cv", columns="rho_inr", values="saving_pct", aggfunc="mean"))
print("\n## 6 trade-offs (full_valid rows): peak reduction %, energy increase %, makespan penalty %")
f=t[t.full_valid]; print(f.groupby("rho_inr")[["peak_reduction_pct","energy_increase_pct","makespan_penalty_pct"]].agg(["mean","median","min","max","count"]))
print("\n## 7 robustness band: saving % vs B, vs B_minpeak (best case for B), vs B_maxpeak (worst case)")
print(t.groupby("rho_inr").agg(n_valid_B=("saving_valid","sum"), n_valid_Bmin=("band_valid_Bmin","sum"), n_valid_Bmax=("band_valid_Bmax","sum"),
  vsB=("saving_pct","mean"), vsBmin=("saving_pct_vs_Bmin","mean"), vsBmax=("saving_pct_vs_Bmax","mean")))
b=t[t.saving_valid & t.band_valid_Bmin & t.band_valid_Bmax]; print("instances with all three valid:", len(b)); print("B peak (kW) vs Bmin/Bmax peak (kW), rho-independent, per instance:")
bp = df[df.strategy.isin(["B","B_minpeak","B_maxpeak","C"])&(df.rho_paise==0)|((df.strategy=="C"))]
pp = df[df.strategy.isin(["B","B_minpeak","B_maxpeak"])].pivot(index="instance_id", columns="strategy", values="peak_w")/1000
print((pp.assign(spread=pp.B_maxpeak-pp.B_minpeak)).describe().loc[["count","mean","min","max"]])
print("instances with spread>0:", int(((pp.B_maxpeak-pp.B_minpeak)>0).sum()), "of", len(pp))
print("\n## 7b rho*_ub (INR/kW) upper-bound break-even, states"); print(rs.state_B.value_counts()); print(rs.rho_star_ub_B.describe())
print(rs.groupby("w_target").rho_star_ub_B.describe())
print("\n## 8 heuristic feasibility")
h=df[df.strategy.isin(["FCFS","SPT"])]; h=h.assign(ok=h.status=="HEURISTIC")
print(h.groupby("strategy").ok.agg(["sum","count","mean"]))
for col in ["w_target","gamma","cv"]: print(h.pivot_table(index="strategy", columns=col, values="ok", aggfunc="mean"))
print("\n## 9 missing/excluded"); print(summary_by(t,["rho_inr"]).loc[:,["rho_inr","n_total","n_valid","n_missing","n_unproven"]])
for fl,rc in (("saving_valid","excl_reason_saving"),("full_valid","excl_reason_full"),("band_valid_Bmin","excl_reason_Bmin"),("band_valid_Bmax","excl_reason_Bmax")): print(fl, t[rc].value_counts().to_dict())
print("\n## 10 generator acceptance (one row per instance)")
i=df.drop_duplicates("instance_id"); gi=i.groupby("w_target").agg(instances=("instance_id","size"), mean_attempts=("gen_attempts","mean"), max_attempts=("gen_attempts","max"), mean_w_real=("w_real","mean"), min_w_real=("w_real","min"), max_w_real=("w_real","max"))
gi["acceptance_rate_pct"]=100*gi.instances/i.groupby("w_target").gen_attempts.sum(); print(gi)
print(i.groupby(["w_target","gamma"]).gen_attempts.mean().unstack())
print("\n## 11 hardest instances (any strategy), by total solve time"); tot=opt.groupby("instance_id").wall_time_s.sum().sort_values(ascending=False).head(8); print(tot)
print("\n## 12 totals: sum solver wall (s) =", round(df.wall_time_s.sum(),1), " per instance mean =", round(df.groupby("instance_id").wall_time_s.sum().mean(),1), " max =", round(df.groupby("instance_id").wall_time_s.sum().max(),1))
print("\n## 13 unproven rows detail"); print(opt[opt.status!="OPTIMAL"][["instance_id","gamma","w_target","cv","strategy","rho_paise","status","stage_statuses","stage_values","wall_time_s"]].to_string())
