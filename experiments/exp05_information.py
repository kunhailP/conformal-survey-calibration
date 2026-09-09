"""exp05 - is the coupling a property of the problem or of one estimator?

Protocol: docs/PROTOCOL_exp05_information.md (written before execution).

Fay-Herriot with known sampling variances.  Estimating the model variance is
exactly the operation of subtracting sampling variance from between-area
dispersion, so the Fisher information for it bounds any workflow that does so.
No microdata required.

    python experiments/exp05_information.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

REPS = 2000
K_GRID = (30, 100, 250, 500)
RHO_GRID = (0.1, 0.3, 0.5, 0.7, 0.9)
A_TRUE = 1.0


def fisher_rse(A: float, D: np.ndarray) -> float:
    """Cramer-Rao relative standard error for the model variance."""
    return float(np.sqrt(2.0 / np.sum((A + D) ** -2.0)) / A)


def reml_A(y: np.ndarray, D: np.ndarray, hi: float = 1e4) -> float:
    """REML estimate of the model variance, intercept only, known D."""
    def neg(A):
        w = 1.0 / (A + D)
        mu = np.sum(w * y) / np.sum(w)
        return 0.5 * (np.sum(np.log(A + D)) + np.log(np.sum(w))
                      + np.sum(w * (y - mu) ** 2))
    r = minimize_scalar(neg, bounds=(0.0, hi), method="bounded",
                        options={"xatol": 1e-10})
    return float(max(r.x, 0.0))


def run(K: int, rho: float, dispersed: bool) -> dict:
    label = f"exp05|{K}|{rho}|{dispersed}"
    rng = np.random.default_rng(
        int.from_bytes(hashlib.sha256(label.encode()).digest()[:8], "little"))
    # rho^2 = mean(D) / (A + mean(D))  ->  mean(D) = A rho^2 / (1 - rho^2)
    Dbar = A_TRUE * rho ** 2 / (1 - rho ** 2)
    D = (Dbar * rng.lognormal(0, 0.8, size=K) if dispersed
         else np.full(K, Dbar))
    D = D * Dbar / D.mean()                      # hold the mean exactly
    est = np.empty(REPS)
    for b in range(REPS):
        u = rng.normal(0, np.sqrt(A_TRUE), size=K)
        y = 5.0 + u + rng.normal(0, np.sqrt(D))
        est[b] = reml_A(y, D)
    realised = est.std(ddof=1) / A_TRUE
    return dict(K=K, rho=rho, dispersed=dispersed, reps=REPS,
                mean_D=float(D.mean()), sd_D=float(D.std()),
                A_hat_mean=float(est.mean()),
                share_at_zero=float((est <= 1e-8).mean()),
                rse_realised=realised,
                rse_bound=fisher_rse(A_TRUE, D),
                rse_closed_form=float(np.sqrt(2 / K) / (1 - rho ** 2)),
                ratio=realised / fisher_rse(A_TRUE, D))


def main() -> None:
    rows = [run(K, rho, disp)
            for disp in (False, True) for K in K_GRID for rho in RHO_GRID]
    df = pd.DataFrame(rows)
    out = ROOT / "results"
    df.to_csv(out / "exp05_information.csv", index=False, float_format="%.6g")
    (out / "exp05_manifest.json").write_text(json.dumps({
        "protocol": "docs/PROTOCOL_exp05_information.md",
        "model": "Fay-Herriot, known sampling variances, intercept only",
        "estimator": "REML", "reps_per_cell": REPS, "A_true": A_TRUE,
        "K": list(K_GRID), "rho": list(RHO_GRID),
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }, indent=2) + "\n")

    pd.set_option("display.width", 200)
    eq = df[~df.dispersed]
    print("EQUAL sampling variances: does REML attain the information bound?")
    print(eq[["K", "rho", "rse_realised", "rse_bound", "rse_closed_form",
              "ratio", "share_at_zero"]].round(4).to_string(index=False))
    dp = df[df.dispersed]
    print("\nDISPERSED sampling variances (lognormal, same mean)")
    print(dp[["K", "rho", "rse_realised", "rse_bound", "rse_closed_form",
              "ratio", "share_at_zero"]].round(4).to_string(index=False))
    big = df[df.K >= 100]
    print(f"\nrealised / bound, K >= 100: median {big.ratio.median():.3f}, "
          f"range {big.ratio.min():.3f}-{big.ratio.max():.3f}")
    print(f"closed form vs exact bound, equal D: max rel. diff "
          f"{(abs(eq.rse_closed_form - eq.rse_bound) / eq.rse_bound).max():.2e}")


if __name__ == "__main__":
    main()
