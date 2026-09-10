"""exp20 - bounding the correction ratio directly, against separate bounds.

Protocol: docs/PROTOCOL_exp20_ratio_pivot.md (written before execution).
Specification: docs/THEORY_ratio_pivot.md.

Model R: Y_c ~ N(0, A + d a_c) with a_c a KNOWN relative variance structure,
nu_c Dhat_c / (d a_c) ~ chi2_{nu_c} independent of Y.  This is the
heteroscedastic model in which reduction to one ratio parameter t = d/A is
genuinely true.  a_c is a design quantity and is not fitted to Dhat.

    python experiments/exp20_ratio_pivot.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2, f as fdist

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from dac.bands import conformal_rank                        # noqa: E402

REPS = 20000
A_TRUE = 1.0
ALPHA0 = ETA = 0.05
ETA1 = ETA2 = ETA / 2


def seed_for(label):
    return np.random.default_rng(
        int.from_bytes(hashlib.sha256(label.encode()).digest()[:8], "little"))


def band_at_t(absY, a, t, m):
    """R(t) = ord_m { |Y_c| / sqrt(1 + a_c t) }, decreasing in t."""
    return np.sort(absY / np.sqrt(1.0 + np.outer(t, a)), axis=1)[:, m - 1]


def t_lower(Y2, a, dhat, K, nu, eta):
    """Exact one-sided lower bound for t by inverting T(t) = K dhat/(t S(t))."""
    q = float(fdist.ppf(1.0 - eta, nu, K))
    T = lambda t: K * dhat / np.maximum(t * (Y2 / (1.0 + np.outer(t, a))).sum(1),
                                        1e-300)
    # T decreases from +inf to K dhat / sum(Y2/a); empty set when that exceeds q
    T_inf = K * dhat / np.maximum((Y2 / a).sum(1), 1e-300)
    empty = T_inf > q
    lo, hi = np.full(Y2.shape[0], 1e-8), np.full(Y2.shape[0], 1e8)
    for _ in range(90):
        mid = np.sqrt(lo * hi)                       # geometric bisection
        below = T(mid) <= q
        hi = np.where(below, mid, hi)
        lo = np.where(below, lo, mid)
    return np.sqrt(lo * hi), empty


def separate_bounds(Y2, Dhat, nu_c, K, m, absY):
    """The incumbent: chi2_K pivot for A at eta1, Bonferroni v_L at eta2."""
    vL2 = nu_c * Dhat / chi2.ppf(1.0 - ETA2 / K, nu_c)
    q = float(chi2.ppf(ETA1, K))
    lo, hi = np.zeros(Y2.shape[0]), np.full(Y2.shape[0], 1e4)
    for _ in range(90):
        mid = 0.5 * (lo + hi)
        below = (Y2 / (mid[:, None] + vL2)).sum(1) < q
        hi = np.where(below, mid, hi)
        lo = np.where(below, lo, mid)
    AU = 0.5 * (lo + hi)
    bd = np.sort(absY / np.sqrt(1.0 + vL2 / np.maximum(AU, 1e-12)[:, None]),
                 axis=1)[:, m - 1]
    return AU, vL2, bd


def run(K, d_over_A, nu0, slog_a):
    rng = seed_for(f"exp20|{K}|{d_over_A}|{nu0}|{slog_a}")
    a = rng.lognormal(0.0, slog_a, size=K)
    a /= a.mean()                                    # known structure, mean 1
    d = A_TRUE * d_over_A
    t = d / A_TRUE
    D = d * a
    nu_c = np.full(K, float(nu0))
    nu = float(nu_c.sum())

    Y = rng.normal(0.0, np.sqrt(A_TRUE + D), size=(REPS, K))
    absY, Y2 = np.abs(Y), Y ** 2
    Dhat = D * rng.chisquare(nu_c, size=(REPS, K)) / nu_c
    dhat = (nu_c * Dhat / a).sum(1) / nu

    m = conformal_rank(K, ALPHA0)
    tL, empty = t_lower(Y2, a, dhat, K, nu, ETA)
    band_ratio = band_at_t(absY, a, tL, m)
    band_ratio = np.where(empty, np.inf, band_ratio)
    band_oracle = band_at_t(absY, a, np.full(REPS, t), m)
    band_unc = np.sort(absY, axis=1)[:, m - 1]
    AU, vL2, band_sep = separate_bounds(Y2, Dhat, nu_c, K, m, absY)

    G = rng.normal(0.0, np.sqrt(A_TRUE), size=REPS)
    fin = np.isfinite(band_ratio)
    hit = lambda b: float((np.abs(G) <= b).mean())
    out = dict(K=K, d_over_A=d_over_A, nu_per_pop=nu0, slog_a=slog_a, reps=REPS,
               nu_total=nu, t_true=t, m=m, nominal=m / (K + 1.0),
               cv_a=float(a.std() / a.mean()),
               mc_se_95=float(np.sqrt(.95 * .05 / REPS)),
               # 1. level
               ratio_level=float((tL <= t).mean()),
               sep_AU_level=float((AU >= A_TRUE).mean()),
               sep_vL_level=float((vL2 <= D).all(axis=1).mean()),
               # 2. containment
               ratio_contain=float((band_ratio >= band_oracle).mean()),
               sep_contain=float((band_sep >= band_oracle).mean()),
               # 4. boundary
               empty_rate=float(empty.mean()),
               Dhat_zero_rate=float((Dhat <= 0).mean()),
               # 3. width and coverage
               cov_oracle=hit(band_oracle), cov_ratio=hit(band_ratio),
               cov_sep=hit(band_sep), cov_unc=hit(band_unc),
               w_oracle=float(band_oracle.mean()),
               w_ratio=float(band_ratio[fin].mean()),
               w_sep=float(band_sep.mean()), w_unc=float(band_unc.mean()),
               ratio_over_oracle=float(np.mean(band_ratio[fin]
                                               / band_oracle[fin])),
               sep_over_oracle=float(np.mean(band_sep / band_oracle)),
               ratio_over_sep=float(np.mean(band_ratio[fin] / band_sep[fin])),
               ratio_over_unc=float(np.mean(band_ratio[fin] / band_unc[fin])),
               sep_over_unc=float(np.mean(band_sep / band_unc)))
    avail = out["sep_over_unc"] and (out["w_unc"] / out["w_oracle"] - 1.0)
    out["available"] = float(out["w_unc"] / out["w_oracle"] - 1.0)
    out["captured_ratio"] = float(
        (out["available"] - (out["ratio_over_oracle"] - 1)) / out["available"])
    out["captured_sep"] = float(
        (out["available"] - (out["sep_over_oracle"] - 1)) / out["available"])
    return out


def main():
    rows = [run(K, da, nu0, sa) for K in (60, 200) for da in (0.5, 1.0)
            for nu0 in (8, 16) for sa in (0.5, 1.2)]
    df = pd.DataFrame(rows)
    out = ROOT / "results" / "exp20_ratio_pivot.csv"
    df.to_csv(out, index=False)
    (ROOT / "results" / "exp20_manifest.json").write_text(json.dumps(dict(
        experiment="exp20_ratio_pivot", reps=REPS, cells=len(df),
        eta=ETA, alpha0=ALPHA0, model="R: D_c = d a_c, a_c known",
        v1_ratio_level=[float(df.ratio_level.min()), float(df.ratio_level.max())],
        v2_ratio_contain=[float(df.ratio_contain.min()),
                          float(df.ratio_contain.max())],
        v3_ratio_over_sep=[float(df.ratio_over_sep.min()),
                           float(df.ratio_over_sep.max())],
        v5_cov=[float(df.cov_ratio.min()), float(df.cov_sep.min())],
        captured=[float(df.captured_ratio.min()), float(df.captured_ratio.max()),
                  float(df.captured_sep.min()), float(df.captured_sep.max())],
    ), indent=2) + "\n")

    pd.set_option("display.width", 240, "display.max_columns", 60)
    lab = ["K", "d_over_A", "nu_per_pop", "slog_a"]
    print("=== 1. LEVEL first  (ratio: nominal 0.95; separate: 0.975 each)")
    print(df.set_index(lab)[["ratio_level", "sep_AU_level", "sep_vL_level",
                             "empty_rate", "Dhat_zero_rate"]].round(4).to_string())
    print("\n=== 2. CONTAINMENT of the oracle half-width")
    print(df.set_index(lab)[["ratio_contain", "sep_contain"]].round(4).to_string())
    print("\n=== 3. WIDTH, with realised coverage beside it (guaranteed 0.90)")
    print(df.set_index(lab)[["cov_oracle", "cov_ratio", "cov_sep", "cov_unc",
                             "ratio_over_oracle", "sep_over_oracle",
                             "ratio_over_sep", "captured_ratio", "captured_sep"]]
          .round(4).to_string())
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
