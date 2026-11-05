# TWCI A4 - Step 2: Bayesian trend of reservoir area (OSF #1, H4; prior from OSF #2: Normal(0, 10) km2 per year)
# Run in Colab after Step 1 (upload the *_area_monthly.csv file). Install once: !pip install pymc arviz
#
# THE IDEA (simple): the reservoir breathes every year (full in spring, lower in autumn) = SEASON.
# We ask: after removing the season, is there a long-term TREND up or down, km2 per year?
# A Bayesian model starts with a PRIOR (what we believe before seeing data: "trend is probably small, around 0"),
# then looks at the data, and gives a POSTERIOR (updated belief) with an uncertainty range.
# We repeat with 3 different priors (a sceptical one, the registered one, a loose one). If the answer does not
# change, the result is robust.

# %% 1. Load
import sys
import numpy as np, pandas as pd, pymc as pm, arviz as az
FILE = "Iriklinskoye_area_monthly.csv"      # <- change for Shardara
d = pd.read_csv(FILE, parse_dates=["date"])
d = d[d["usable"] & d["water_km2"].notna()].copy()
d["t_years"] = (d["date"].dt.year - 2015) + (d["date"].dt.month - 1) / 12   # time in years since Jan 2015
m = (d["date"].dt.month - 1).values                                           # month index 0..11
y = d["water_km2"].values
t = d["t_years"].values
print("Months used in the model:", len(d))

# %% 2. The model, repeated for 3 priors on the trend (km2 per year)
PRIORS = {"sceptical sd=2": 2.0, "REGISTERED sd=10": 10.0, "loose sd=50": 50.0}
results = {}
for name, sd in PRIORS.items():
    with pm.Model():
        trend = pm.Normal("trend", mu=0.0, sigma=sd)                 # km2 per year
        # one typical level for each calendar month (this IS the season; no separate overall level needed)
        season = pm.Normal("season", mu=y.mean(), sigma=max(y.std() * 3, 1.0), shape=12)
        noise = pm.HalfNormal("noise", sigma=max(y.std(), 1.0))
        pm.Normal("obs", mu=trend * t + season[m], sigma=noise, observed=y)
        idata = pm.sample(2000, tune=2000, chains=4, random_seed=2026, target_accept=0.95, progressbar=False)
    rhat = float(az.rhat(idata, var_names=["trend"])["trend"])
    div = int(idata.sample_stats["diverging"].sum())
    post = idata.posterior["trend"].values.ravel()
    results[name] = dict(mean=post.mean(), lo=np.percentile(post, 2.5), hi=np.percentile(post, 97.5), rhat=rhat, divergences=div)

# %% 3. Result table (this is what goes into the paper)
out = pd.DataFrame(results).T.round(3)
out["converged (R-hat<1.01, 0 divergences)"] = (out["rhat"] < 1.01) & (out["divergences"] == 0)
print(out.to_string())
out.to_csv("trend_3priors.csv")
print("\nREAD IT LIKE THIS: 'trend' = change of water area, km2 per year, with a 95% credible interval [lo, hi].")
print("If the interval contains 0, we cannot say the area is going up or down.")
print("If the three rows tell the same story, the result does not depend on our starting belief.")
