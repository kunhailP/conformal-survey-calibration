"""exp17 - the fixed procedure on a finite population and a complex sample.

Protocol: docs/PROTOCOL_exp17_complex_sample.md (written before execution).
Predecessor: exp16, which fixed the four constructions.  None is added here.

This does NOT test whether the chi-square pivot's guarantee holds under a
complex design; its conditions are not met there and a simulation cannot extend
a theorem's scope.  It measures how stably the fixed procedure behaves when the
conditions fail, and which violation moves which quantity.

Estimand: one pre-specified CDF point F_c(t0), the finite-population share below
t0.  Target: prediction of a NEWLY generated population's F_{K+1}(t0), not
design-based coverage for a fixed population.

    python experiments/exp17_complex_sample.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2, norm, kstest, skew, kurtosis

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from dac.bands import conformal_rank                        # noqa: E402

REPS, B_BOOT, CAL_DRAWS = 2000, 1000, 200000
H, M, M_SAMP, N_UNIT = 4, 20, 5, 10
NU = H * (M_SAMP - 1)                    # nominal design degrees of freedom = 16
SIGMA_EPS, TAU = 1.0, 0.45
ALPHA0 = ETA = 0.05
ETA1 = ETA2 = ETA / 2
FPC = 1.0 - M_SAMP / M


def seed_for(label):
    return np.random.default_rng(
        int.from_bytes(hashlib.sha256(label.encode()).digest()[:8], "little"))


def psu_means(rng, npop, t0, sigma_a):
    """PSU-level indicator means, shape (npop, H, M).  Exact, no unit loop."""
    mu = rng.normal(0.0, TAU, size=(npop, 1, 1))
    a = rng.normal(0.0, sigma_a, size=(npop, H, M))
    p = norm.cdf((t0 - mu - a) / SIGMA_EPS)
    return rng.binomial(N_UNIT, p) / N_UNIT


def finite_pop_F(z):
    return z.mean(axis=(1, 2))


def true_D(z):
    """Exact design variance of the stratified one-stage cluster estimator."""
    S2 = z.var(axis=2, ddof=1)                       # (npop, H)
    return (FPC / M_SAMP) * S2.sum(axis=1) / H ** 2


def draw_sample(rng, z):
    npop = z.shape[0]
    idx = np.argsort(rng.random((npop, H, M)), axis=2)[:, :, :M_SAMP]
    zs = np.take_along_axis(z, idx, axis=2)          # (npop, H, m)
    Fhat = zs.mean(axis=2).mean(axis=1)
    s2 = zs.var(axis=2, ddof=1)
    Dhat = (FPC / M_SAMP) * s2.sum(axis=1) / H ** 2
    return Fhat, Dhat


def calibrate(t0_q, sigma_a):
    """mu and A of the finite-population target, from an independent draw."""
    rng = seed_for(f"exp17cal|{t0_q}|{sigma_a}")
    t0 = norm.ppf(t0_q) * np.sqrt(TAU ** 2 + sigma_a ** 2 + SIGMA_EPS ** 2)
    F = np.concatenate([finite_pop_F(psu_means(rng, 20000, t0, sigma_a))
                        for _ in range(CAL_DRAWS // 20000)])
    return t0, float(F.mean()), float(F.var(ddof=1))


def pivot_AU(Y, vL2, df, fit_mean):
    """Root of Q(a) = chi2_{df, eta1}; Q refits the weighted mean when asked."""
    q = float(chi2.ppf(ETA1, df))
    lo, hi = np.zeros(Y.shape[0]), np.full(Y.shape[0], 10.0)

    def Q(a):
        w = 1.0 / (a[:, None] + vL2)
        r = Y - ((w * Y).sum(1) / w.sum(1))[:, None] if fit_mean else Y
        return (w * r ** 2).sum(1)

    for _ in range(90):
        mid = 0.5 * (lo + hi)
        below = Q(mid) < q
        hi = np.where(below, mid, hi)
        lo = np.where(below, lo, mid)
    return 0.5 * (lo + hi)


def opt_w(A, D):
    return 1.0 / ((A + D) ** 2 + D ** 2 / NU)


def gvf_prop(Dhat, Fhat):
    """Design relation for a proportion: D ~ c F(1-F).  Fitted on all populations."""
    v = np.maximum(Fhat * (1.0 - Fhat), 1e-9)
    c = (Dhat.sum(axis=-1, keepdims=True) / v.sum(axis=-1, keepdims=True))
    return np.maximum(c * v, 1e-12)


def run(K, t0_q, sigma_a):
    t0, mu, A = calibrate(t0_q, sigma_a)
    rng = seed_for(f"exp17|{K}|{t0_q}|{sigma_a}")

    z = psu_means(rng, REPS * (K + 1), t0, sigma_a).reshape(REPS, K + 1, H, M)
    Ftrue = finite_pop_F(z.reshape(-1, H, M)).reshape(REPS, K + 1)
    Dtrue = true_D(z.reshape(-1, H, M)).reshape(REPS, K + 1)
    Fhat, Dhat = draw_sample(rng, z.reshape(-1, H, M))
    Fhat = Fhat.reshape(REPS, K + 1)
    Dhat = Dhat.reshape(REPS, K + 1)

    Y = Fhat[:, :K] - mu                       # calibration deviations
    Dc, Dh = Dtrue[:, :K], np.maximum(Dhat[:, :K], 1e-12)
    Gnew = Ftrue[:, K] - mu                    # the latent target, finite population

    # --- assumption diagnostics -----------------------------------------
    std = Y / np.sqrt(A + Dc)
    ratio = NU * Dh / Dc
    diag = dict(
        skew_std=float(skew(std.ravel())), kurt_std=float(kurtosis(std.ravel())),
        ks_std_normal=float(kstest(std.ravel()[:5000], "norm").pvalue),
        chi2_ratio_mean=float(ratio.mean()), chi2_ratio_var=float(ratio.var()),
        chi2_mean_expected=float(NU), chi2_var_expected=float(2 * NU),
        ks_chi2=float(kstest(ratio.ravel()[:5000], "chi2", args=(NU,)).pvalue),
        corr_Dhat_Y=float(np.corrcoef(Dh.ravel(), Y.ravel())[0, 1]),
        deff=float((Dc.mean() * H * M_SAMP * N_UNIT)
                   / max(Ftrue.mean() * (1 - Ftrue.mean()), 1e-12)),
        Dbar_over_A=float(Dc.mean() / A))

    # --- the fixed constructions -----------------------------------------
    vL2 = NU * Dh / chi2.ppf(1.0 - ETA2 / K, NU)
    AU_piv = pivot_AU(Y, vL2, K, fit_mean=False)
    AU_piv_fit = pivot_AU(Y, vL2, K - 1, fit_mean=True)

    Dsm = gvf_prop(Dh, Fhat[:, :K])
    Z = Y ** 2 - Dh
    A0 = np.maximum(Z.mean(1), 1e-12)[:, None]
    w = opt_w(A0, Dsm)
    Ahat = (Z * w).sum(1) / w.sum(1)
    AU_pct = np.empty(REPS)
    rng2 = seed_for(f"exp17boot|{K}|{t0_q}|{sigma_a}")
    for b in range(REPS):
        j = rng2.integers(0, K, size=(B_BOOT, K))
        Zb, Dhb, Fb = Z[b][j], Dh[b][j], Fhat[b, :K][j]
        Dsb = gvf_prop(Dhb, Fb)
        A0b = np.maximum(Zb.mean(1), 1e-12)[:, None]
        wb = opt_w(A0b, Dsb)
        AU_pct[b] = np.quantile((Zb * wb).sum(1) / wb.sum(1), 1 - ETA1)

    m = conformal_rank(K, ALPHA0)
    absY = np.abs(Y)
    band = {}
    band["oracle"] = np.sort(absY / np.sqrt(1.0 + Dc / A), axis=1)[:, m - 1]
    for nm, AU in (("piv", AU_piv), ("piv_fit", AU_piv_fit), ("pct", AU_pct)):
        band[nm] = np.sort(absY / np.sqrt(1.0 + vL2 / np.maximum(AU, 1e-12)[:, None]),
                           axis=1)[:, m - 1]
    band["pct_normal"] = norm.ppf(1 - ALPHA0 / 2) * np.sqrt(np.maximum(AU_pct, 0))

    out = dict(K=K, t0_q=t0_q, sigma_a=sigma_a, reps=REPS, B=B_BOOT, nu=NU,
               t0=t0, mu=mu, A=A, m=m, nominal=m / (K + 1.0),
               mc_se=float(np.sqrt(.9 * .1 / REPS)), **diag,
               AU_piv_cov=float((AU_piv >= A).mean()),
               AU_piv_fit_cov=float((AU_piv_fit >= A).mean()),
               AU_pct_cov=float((AU_pct >= A).mean()),
               AU_piv_mean=float(AU_piv.mean()), AU_pct_mean=float(AU_pct.mean()))
    for nm, bd in band.items():
        out[f"{nm}_cov"] = float((np.abs(Gnew) <= bd).mean())
        out[f"{nm}_w"] = float(bd.mean())
        if nm != "oracle":
            out[f"{nm}_contain"] = float((bd >= band["oracle"]).mean())
            out[f"{nm}_over_oracle"] = float(np.mean(bd / band["oracle"]))
    return out


def main():
    rows = [run(K, q, sa) for K in (60, 200) for q in (0.50, 0.15)
            for sa in (0.2, 0.6)]
    df = pd.DataFrame(rows)
    out = ROOT / "results" / "exp17_complex_sample.csv"
    df.to_csv(out, index=False)
    (ROOT / "results" / "exp17_manifest.json").write_text(json.dumps(dict(
        experiment="exp17_complex_sample", reps=REPS, B=B_BOOT, cells=len(df),
        design=dict(H=H, M=M, m=M_SAMP, n=N_UNIT, nu_nominal=NU),
        eta1=ETA1, eta2=ETA2, alpha0=ALPHA0,
        x1_chi2_ratio_mean=[float(df.chi2_ratio_mean.min()),
                            float(df.chi2_ratio_mean.max())],
        x2_corr_Dhat_Y=[float(df.corr_Dhat_Y.min()), float(df.corr_Dhat_Y.max())],
        x3_oracle_cov=[float(df.oracle_cov.min()), float(df.oracle_cov.max())],
        x4_piv_cov=[float(df.piv_cov.min()), float(df.piv_cov.max())],
    ), indent=2) + "\n")

    pd.set_option("display.width", 250, "display.max_columns", 70)
    lab = ["K", "t0_q", "sigma_a"]
    print("=== the design, and how far the model's conditions are from holding")
    print(df.set_index(lab)[["deff", "Dbar_over_A", "A", "mu",
                             "skew_std", "kurt_std", "ks_std_normal"]]
          .round(4).to_string())
    print("\n=== X1/X2: the chi-square law for Dhat (nominal mean 16, var 32) and dependence")
    print(df.set_index(lab)[["chi2_ratio_mean", "chi2_ratio_var", "ks_chi2",
                             "corr_Dhat_Y"]].round(4).to_string())
    print("\n=== X3: does the ORACLE band cover?  (nominal m/(K+1), MC SE ~0.0067)")
    print(df.set_index(lab)[["nominal", "oracle_cov", "oracle_w"]].round(4).to_string())
    print("\n=== X4: scale limits and latent-target coverage, guaranteed 0.90 under the model")
    print(df.set_index(lab)[["AU_piv_cov", "AU_piv_fit_cov", "AU_pct_cov",
                             "piv_cov", "piv_fit_cov", "pct_cov", "pct_normal_cov"]]
          .round(4).to_string())
    print("\n=== X5: containment and width, ratios to the oracle band")
    print(df.set_index(lab)[["piv_contain", "pct_contain",
                             "piv_over_oracle", "pct_over_oracle",
                             "pct_normal_over_oracle"]].round(4).to_string())
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
