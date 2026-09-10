"""exp29 - Proposition S4 as a pre-registered prediction on a fresh grid.

Protocol: docs/PROTOCOL_exp29_scale_law.md, whose predicted numbers were computed
before this was run.  Derivation: docs/THEORY_scale_sensitivity.md.

    python experiments/exp29_scale_law.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm, chi2

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments"))
import exp26_same_target as E                               # noqa: E402


def law(K, a1, a2, alpha0=E.ALPHA0):
    m = int(np.ceil((1 - alpha0) * (K + 1)))
    p = m / (K + 1)
    return norm.ppf(0.5 + p / 2) / norm.ppf(1 - a1 / 2) * np.sqrt(chi2.ppf(a2, K) / K)


def run(K, rho2, nu0, sig_mis, a1, a2):
    E.SPLITS = np.array([a1])                    # fixed split, no scanning
    d_over_A = rho2 / (1.0 - rho2)
    r = E.run(K, d_over_A, nu0, sig_mis)
    obs = 1.0 / r["gauss_over_conformal"]
    return dict(K=K, rho2=rho2, nu=nu0, sig_mis=sig_mis, alpha1=a1, alpha2=a2,
                obs_ratio=obs, predicted=law(K, a1, a2),
                err_pct=100 * (obs / law(K, a1, a2) - 1),
                conformal_cov=r["conformal_cov"], gaussian_cov=r["gaussian_cov"],
                w_conformal=r["conformal_w"], w_gaussian=r["gaussian_w"])


def main() -> None:
    rows = [run(K, r2, nu, sm, 0.025, 0.025)
            for K in (40, 120, 400) for r2 in (0.20, 0.45, 0.70)
            for nu in (6, 20) for sm in (0.0, 0.5)]
    split = [run(120, 0.45, 20, 0.0, a1, 0.05 - a1)
             for a1 in (0.005, 0.010, 0.020, 0.025, 0.035, 0.045)]
    df, ds = pd.DataFrame(rows), pd.DataFrame(split)
    df.to_csv(ROOT / "results" / "exp29_scale_law.csv", index=False)
    ds.to_csv(ROOT / "results" / "exp29_split_scan.csv", index=False)

    spread = df.groupby("K")["obs_ratio"].agg(lambda s: s.max() - s.min())
    (ROOT / "results" / "exp29_manifest.json").write_text(json.dumps(dict(
        experiment="exp29_scale_law", reps=E.REPS, cells=len(df) + len(ds),
        pA_max_abs_err_pct=float(df.err_pct.abs().max()),
        pB_within_K_spread={int(k): float(v) for k, v in spread.items()},
        pC_monotone=bool((ds.obs_ratio.diff().dropna() > 0).all()),
        pC_max_abs_err_pct=float(ds.err_pct.abs().max()),
        predictions_locked_in_protocol=True,
    ), indent=2) + "\n")

    pd.set_option("display.width", 200, "display.max_columns", 40)
    print("=== P-A / P-B: fresh grid, prediction locked before running")
    print(df.set_index(["K", "rho2", "nu", "sig_mis"])[
        ["predicted", "obs_ratio", "err_pct", "conformal_cov", "gaussian_cov"]]
        .round(4).to_string())
    print("\nP-A  max |error| = %.2f%%   (registered tolerance 5%%)"
          % df.err_pct.abs().max())
    print("P-B  within-K spread of the observed ratio  (tolerance 0.02):")
    for k, v in spread.items():
        print(f"       K={k:4d}: {v:.4f}")
    print("\n=== P-C: response to the budget split at K=120")
    print(ds.set_index("alpha1")[["alpha2", "predicted", "obs_ratio", "err_pct"]]
          .round(4).to_string())
    print("     monotone increasing:", bool((ds.obs_ratio.diff().dropna() > 0).all()),
          " | max |error| %.2f%%" % ds.err_pct.abs().max(),
          " | any crossing above 1:", bool((ds.obs_ratio >= 1).any()))


if __name__ == "__main__":
    main()
