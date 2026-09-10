"""exp16 - does the tighter scale limit survive into the band?

Protocol: docs/PROTOCOL_exp16_band_comparison.md (written before execution).
Predecessor: exp15.  No new estimator is added.

exp15 found the percentile bootstrap limit for A to be 2.1-2.6 times tighter
than the chi-square pivot.  That is a statement about A_U.  The half-width is
h_c(A) = |Y_c| sqrt(A / (A + L_c)) with elasticity L_c / (2(A+L_c)) in [0, 1/2],
so the band cannot gain more than the square root of the limit gain and will
usually gain much less.  This measures what actually survives.

    python experiments/exp16_band_comparison.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2, norm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from dac.bands import conformal_rank                        # noqa: E402

REPS, B_BOOT, B_SMALL = 2000, 2000, 200
NU, A_TRUE = 10.0, 1.0
ALPHA0 = ETA = 0.05
ETA1 = ETA2 = ETA / 2


def seed_for(label):
    return np.random.default_rng(
        int.from_bytes(hashlib.sha256(label.encode()).digest()[:8], "little"))


def make_D(rng, K, dbar, sigma_e):
    n = rng.lognormal(0.0, 0.8, size=K)
    e = rng.lognormal(0.0, sigma_e, size=K) if sigma_e > 0 else np.ones(K)
    D = e / n
    return D * A_TRUE * dbar / D.mean(), n


def opt_w(A, D, nu):
    return 1.0 / ((A + D) ** 2 + D ** 2 / nu)


def gvf(Dhat, n):
    return np.maximum((Dhat * n).mean(axis=-1, keepdims=True) / n, 1e-9)


def pivot_AU(Y2, vL2, q):
    lo, hi = np.zeros(Y2.shape[0]), np.full(Y2.shape[0], 1e4)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        below = (Y2 / (mid[:, None] + vL2)).sum(1) < q
        hi = np.where(below, mid, hi)
        lo = np.where(below, lo, mid)
    return 0.5 * (lo + hi)


def band_from(absY, vL2, AU, m):
    return np.sort(absY / np.sqrt(1.0 + vL2 / np.maximum(AU, 1e-9)[:, None]),
                   axis=1)[:, m - 1]


def run(K, dbar, sigma_e):
    rng = seed_for(f"exp16|{K}|{dbar}|{sigma_e}")
    D, n = make_D(rng, K, dbar, sigma_e)
    nu = np.full(K, NU)
    Y = rng.normal(0.0, np.sqrt(A_TRUE + D), size=(REPS, K))
    absY, Y2 = np.abs(Y), Y ** 2
    Dhat = D * rng.chisquare(nu, size=(REPS, K)) / nu
    Z = Y2 - Dhat

    Dsm = gvf(Dhat, n)
    A0 = np.maximum(Z.mean(1), 1e-9)[:, None]
    w = opt_w(A0, Dsm, nu)
    Ahat = (Z * w).sum(1) / w.sum(1)

    vL2 = nu * Dhat / chi2.ppf(1.0 - ETA2 / K, nu)
    AU_piv = pivot_AU(Y2, vL2, float(chi2.ppf(ETA1, K)))

    # one set of resampling draws; both forms and both counts read off it
    AU = {k: np.empty(REPS) for k in
          ("pct_B2000", "pct_B200", "basic_B2000", "basic_B200")}
    rng2 = seed_for(f"exp16boot|{K}|{dbar}|{sigma_e}")
    for b in range(REPS):
        j = rng2.integers(0, K, size=(B_BOOT, K))
        Zb, Dhb, nb = Z[b][j], Dhat[b][j], n[j]
        Dsb = gvf(Dhb, nb)
        A0b = np.maximum(Zb.mean(1), 1e-9)[:, None]
        wb = opt_w(A0b, Dsb, NU)
        Ab = (Zb * wb).sum(1) / wb.sum(1)
        AU["pct_B2000"][b] = np.quantile(Ab, 1 - ETA1)
        AU["pct_B200"][b] = np.quantile(Ab[:B_SMALL], 1 - ETA1)
        AU["basic_B2000"][b] = 2 * Ahat[b] - np.quantile(Ab, ETA1)
        AU["basic_B200"][b] = 2 * Ahat[b] - np.quantile(Ab[:B_SMALL], ETA1)

    m = conformal_rank(K, ALPHA0)
    band_or = np.sort(absY / np.sqrt(1.0 + D / A_TRUE), axis=1)[:, m - 1]
    G = rng.normal(0.0, np.sqrt(A_TRUE), size=REPS)

    bands = {"piv_conformal": band_from(absY, vL2, AU_piv, m),
             "pct_conformal": band_from(absY, vL2, AU["pct_B2000"], m),
             "pct_normal": norm.ppf(1 - ALPHA0 / 2)
             * np.sqrt(np.maximum(AU["pct_B2000"], 1e-9))}

    out = dict(K=K, Dbar_over_A=dbar, sigma_e=sigma_e, reps=REPS, B=B_BOOT,
               nu=NU, m=m, nominal=m / (K + 1.0),
               mc_se_975=float(np.sqrt(.975 * .025 / REPS)),
               mc_se_90=float(np.sqrt(.90 * .10 / REPS)),
               gvf_bias=float(Ahat.mean() - A_TRUE),
               elasticity=float(np.mean(D / (2 * (A_TRUE + D)))),
               AU_piv_cov=float((AU_piv >= A_TRUE).mean()),
               AU_piv_mean=float(AU_piv.mean()),
               cov_oracle=float((np.abs(G) <= band_or).mean()),
               w_oracle=float(band_or.mean()))
    for k, v in AU.items():
        out[f"AU_{k}_cov"] = float((v >= A_TRUE).mean())
        out[f"AU_{k}_mean"] = float(v.mean())
    out["AU_ratio_pct_over_piv"] = float(np.mean(AU["pct_B2000"] / AU_piv))
    for name, bd in bands.items():
        out[f"{name}_contain"] = float((bd >= band_or).mean())
        out[f"{name}_cov"] = float((np.abs(G) <= bd).mean())
        out[f"{name}_w"] = float(bd.mean())
        out[f"{name}_over_oracle"] = float(np.mean(bd / band_or))
    out["band_ratio_pct_over_piv"] = float(
        np.mean(bands["pct_conformal"] / bands["piv_conformal"]))
    out["sqrt_bound_on_band_gain"] = float(
        np.sqrt(out["AU_ratio_pct_over_piv"]))
    out["normal_over_conformal"] = float(
        np.mean(bands["pct_normal"] / bands["pct_conformal"]))
    return out


def main():
    rows = [run(K, db, se) for K in (60, 200) for db in (1.0, 4.0)
            for se in (0.0, 0.6)]
    df = pd.DataFrame(rows)
    out = ROOT / "results" / "exp16_band_comparison.csv"
    df.to_csv(out, index=False)
    (ROOT / "results" / "exp16_manifest.json").write_text(json.dumps(dict(
        experiment="exp16_band_comparison", reps=REPS, B=B_BOOT, nu=NU,
        eta1=ETA1, eta2=ETA2, alpha0=ALPHA0, cells=len(df),
        w1_AU_ratio=[float(df.AU_ratio_pct_over_piv.min()),
                     float(df.AU_ratio_pct_over_piv.max())],
        w1_band_ratio=[float(df.band_ratio_pct_over_piv.min()),
                       float(df.band_ratio_pct_over_piv.max())],
        w2_pct_cov_min=float(df.pct_conformal_cov.min()),
        w3_pct_contain_min=float(df.pct_conformal_contain.min()),
        w5_normal_over_conformal=[float(df.normal_over_conformal.min()),
                                  float(df.normal_over_conformal.max())],
    ), indent=2) + "\n")

    pd.set_option("display.width", 240, "display.max_columns", 60)
    lab = ["K", "Dbar_over_A", "sigma_e"]
    print("=== the four linked quantities  (MC SE ~0.0035 near 0.975, ~0.0067 near 0.90)")
    print("(1) coverage of A_U itself, and its size (true A = 1)")
    print(df.set_index(lab)[["AU_piv_cov", "AU_pct_B2000_cov",
                             "AU_piv_mean", "AU_pct_B2000_mean",
                             "AU_ratio_pct_over_piv"]].round(4).to_string())
    print("\n(2) containment of the oracle half-width   (3) latent-target coverage, target 0.90")
    print(df.set_index(lab)[["piv_conformal_contain", "pct_conformal_contain",
                             "pct_normal_contain", "cov_oracle",
                             "piv_conformal_cov", "pct_conformal_cov",
                             "pct_normal_cov"]].round(4).to_string())
    print("\n(4) half-widths, paired on the same replicates")
    print(df.set_index(lab)[["w_oracle", "piv_conformal_w", "pct_conformal_w",
                             "pct_normal_w", "band_ratio_pct_over_piv",
                             "sqrt_bound_on_band_gain", "elasticity",
                             "normal_over_conformal"]].round(4).to_string())
    print("\n=== block 2: form and count separated, from the same draws")
    print(df.set_index(lab)[["AU_basic_B200_cov", "AU_basic_B2000_cov",
                             "AU_pct_B200_cov", "AU_pct_B2000_cov"]]
          .round(4).to_string())
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
