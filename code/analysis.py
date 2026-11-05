"""TWCI analysis (OSF #1 h3wgn, OSF #2 z4vde). Seed 2026, 10,000 bootstrap resamples.
Reads ural.csv and syrdarya.csv; prints results. No other analyses are run."""
import csv, math
import numpy as np

SEED, B = 2026, 10_000

def load(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))

ural = load("ural.csv")
syr = load("syrdarya.csv")

def score(r):                       # obligation score 0-6
    return int(r["access"]) + int(r["clarity"]) + int(r["time"])

def cvi(scores):                    # CVI in %
    return 100 * np.sum(scores) / (6 * len(scores))

def pct_ci(samples):
    return np.percentile(samples, [2.5, 97.5])

def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z**2 / n
    c = (p + z**2 / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / d
    return c - h, c + h

rng = np.random.default_rng(SEED)
u = np.array([score(r) for r in ural])
s = np.array([score(r) for r in syr])

print("=== Basic ===")
print(f"Ural      n={len(u)}  sum={u.sum()}  CVI={cvi(u):.2f}%")
print(f"Syr Darya n={len(s)}  sum={s.sum()}  CVI={cvi(s):.2f}%")
for dim in ("access", "clarity", "time"):
    a = np.array([int(r[dim]) for r in ural]); b = np.array([int(r[dim]) for r in syr])
    print(f"  {dim:8s} Ural mean={a.mean():.2f}  Syr mean={b.mean():.2f}")

# H1: Ural CVI < 50%
boot = np.array([cvi(rng.choice(u, len(u), replace=True)) for _ in range(B)])
lo, hi = pct_ci(boot)
print("\n=== H1 (Ural CVI below 50%) ===")
print(f"CVI={cvi(u):.2f}%  95% CI [{lo:.2f}, {hi:.2f}]  ->",
      "SUPPORTED" if cvi(u) < 50 and hi < 50 else "inconclusive/not supported")

# H2: mean Accessibility, data exchange minus water quantity
de = np.array([int(r["access"]) for r in ural if r["type"] == "Дерек алмасу"])
wq = np.array([int(r["access"]) for r in ural if r["type"] == "Су мөлшері"])
d2 = de.mean() - wq.mean()
b2 = np.array([rng.choice(de, len(de)).mean() - rng.choice(wq, len(wq)).mean() for _ in range(B)])
lo, hi = pct_ci(b2)
print("\n=== H2 (data-exchange vs water-quantity Accessibility, descriptive) ===")
print(f"data exchange n={len(de)} mean={de.mean():.2f};  water quantity n={len(wq)} mean={wq.mean():.2f}")
print(f"difference={d2:.2f}  95% CI [{lo:.2f}, {hi:.2f}]  (a group has <5 obligations -> descriptive only)"
      if min(len(de), len(wq)) < 5 else f"difference={d2:.2f}  95% CI [{lo:.2f}, {hi:.2f}]")

# H3: share of obligations requiring public disclosure; Wilson CI; threshold 10%
k3 = sum(r["h3"] == "yes" for r in ural)
lo, hi = wilson(k3, len(ural))
print("\n=== H3 (share requiring public disclosure, threshold 10%) ===")
print(f"{k3}/{len(ural)} = {100*k3/len(ural):.1f}%  95% Wilson [{100*lo:.1f}, {100*hi:.1f}]%  ->",
      "SUPPORTED" if hi < 0.10 else "inconclusive")

# H7: CVI(Syr Darya) - CVI(Ural), bootstrap within each treaty
d7 = cvi(s) - cvi(u)
b7 = np.array([cvi(rng.choice(s, len(s))) - cvi(rng.choice(u, len(u))) for _ in range(B)])
lo, hi = pct_ci(b7)
print("\n=== H7 (CVI Syr Darya minus CVI Ural; confirmatory) ===")
print(f"difference={d7:.2f} percentage points  95% CI [{lo:.2f}, {hi:.2f}]")
print("->", "SUPPORTED" if lo > 0 else "NOT SUPPORTED (opposite direction)" if hi < 0 else "INCONCLUSIVE (interval contains 0)")

# H8: joint commission vs both states
com = np.array([score(r) for r in ural if r["group"] == "Комиссия"])
both = np.array([score(r) for r in ural if r["group"] == "Екі мемлекет"])
one = np.array([score(r) for r in ural if r["group"].startswith("Бір тарап")])
d8 = cvi(com) - cvi(both)
b8 = np.array([cvi(rng.choice(com, len(com))) - cvi(rng.choice(both, len(both))) for _ in range(B)])
lo, hi = pct_ci(b8)
print("\n=== H8 (joint commission minus both states, descriptive) ===")
print(f"commission n={len(com)} CVI={cvi(com):.2f}%;  both states n={len(both)} CVI={cvi(both):.2f}%;  single party n={len(one)} CVI={cvi(one):.2f}% (descriptive)")
print(f"difference={d8:.2f} pp  95% CI [{lo:.2f}, {hi:.2f}]")

# H9: confidentiality flag share
k9 = sum(r["h9"] == "yes" for r in ural)
lo, hi = wilson(k9, len(ural))
print("\n=== H9 (confidentiality / third-party restriction share, descriptive) ===")
print(f"{k9}/{len(ural)} = {100*k9/len(ural):.1f}%  95% Wilson [{100*lo:.1f}, {100*hi:.1f}]%")
