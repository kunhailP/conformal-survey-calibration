"""exp18 - the regional design share, reached by two different routes.

Protocol: docs/PROTOCOL_exp18_regional_share.md (written before execution).
Predecessor: exp17.  Procedures and error budget unchanged.

exp17 sat at Dbar/A = 0.04-0.13, where the whole available narrowing is 2-6
percent, so a band close to the oracle proves little.  Here the design share is
raised to where the correction matters, by two routes that give the same D/A
but not the same difficulty:

    small_sample   fewer PSUs and smaller clusters -> D up, nu down, zeros up
    low_signal     smaller between-population spread -> A down, design untouched

An uncorrected band is carried as a reference, with no T2 guarantee claimed for
it, to separate "the correction works" from "the correction was not needed".

    python experiments/exp18_regional_share.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2, norm, skew, kurtosis

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from dac.bands import conformal_rank                        # noqa: E402

REPS, B_BOOT, CAL = 2000, 500, 120000
H, M = 4, 20
SIGMA_EPS, SIGMA_A = 1.0, 0.4
TAU0 = 0.45
ALPHA0 = ETA = 0.05
ETA1 = ETA2 = ETA / 2
FLOOR = 1e-12
SMALL = {"S1": (3, 4), "S2": (2, 2)}          # (PSUs sampled, units per PSU)
BASE = (5, 10)


def seed_for(label):
    return np.random.default_rng(
        int.from_bytes(hashlib.sha256(label.encode()).digest()[:8], "little"))


def psu_means(rng, npop, t0, tau, n_unit):
    mu = rng.normal(0.0, tau, size=(npop, 1, 1))
    a = rng.normal(0.0, SIGMA_A, size=(npop, H, M))
    p = norm.cdf((t0 - mu - a) / SIGMA_EPS)
    return rng.binomial(n_unit, p) / n_unit


def true_D(z, m_samp):
    return ((1.0 - m_samp / M) / m_samp) * z.var(axis=2, ddof=1).sum(axis=1) / H ** 2


def draw_sample(rng, z, m_samp):
    idx = np.argsort(rng.random(z.shape), axis=2)[:, :, :m_samp]
    zs = np.take_along_axis(z, idx, axis=2)
    Fhat = zs.mean(axis=2).mean(axis=1)
    Dhat = ((1.0 - m_samp / M) / m_samp) * zs.var(axis=2, ddof=1).sum(axis=1) / H ** 2
    return Fhat, Dhat


def calibrate(t0_q, tau, m_samp, n_unit, tag):
    """mu, A and the realised Dbar/A of a configuration."""
    rng = seed_for(f"exp18cal|{t0_q}|{tau:.6f}|{m_samp}|{n_unit}|{tag}")
    t0 = norm.ppf(t0_q) * np.sqrt(tau ** 2 + SIGMA_A ** 2 + SIGMA_EPS ** 2)
    F, D = [], []
    for _ in range(CAL // 20000):
        z = psu_means(rng, 20000, t0, tau, n_unit)
        F.append(z.mean(axis=(1, 2)))
        D.append(true_D(z, m_samp))
    F, D = np.concatenate(F), np.concatenate(D)
    A = float(F.var(ddof=1))
    return t0, float(F.mean()), A, float(D.mean() / A)


def tau_for(t0_q, target, m_samp, n_unit):
    """Find tau giving the requested Dbar/A on the base design."""
    lo, hi = 0.005, 1.5
    for _ in range(28):
        mid = 0.5 * (lo + hi)
        r = calibrate(t0_q, mid, m_samp, n_unit, "search")[3]
        if r > target:                     # too much noise relative to signal
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def opt_w(A, D, nu):
    return 1.0 / ((A + D) ** 2 + D ** 2 / nu)


def gvf_prop(Dhat, Fhat):
    v = np.maximum(Fhat * (1.0 - Fhat), 1e-9)
    c = Dhat.sum(axis=-1, keepdims=True) / v.sum(axis=-1, keepdims=True)
    return np.maximum(c * v, FLOOR)


def pivot_AU(Y, vL2, df, fit_mean):
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


def within_corr(rng, t0, tau, m_samp, n_unit, npop=200, nsamp=400):
    """Sampling dependence of Dhat and Fhat for FIXED populations."""
    z = psu_means(rng, npop, t0, tau, n_unit)
    D0, F0 = true_D(z, m_samp), z.mean(axis=(1, 2))
    eF, eD = [], []
    for _ in range(nsamp):
        Fh, Dh = draw_sample(rng, z, m_samp)
        eF.append(Fh - F0); eD.append(Dh - D0)
    eF, eD = np.array(eF), np.array(eD)
    cs = [np.corrcoef(eD[:, i], eF[:, i])[0, 1] for i in range(npop)
          if eD[:, i].std() > 0 and eF[:, i].std() > 0]
    return float(np.mean(cs)), float(np.corrcoef(D0, F0)[0, 1])


def run(route, level, t0_q, K):
    m_samp, n_unit = SMALL[level] if route == "small_sample" else BASE
    nu = H * (m_samp - 1)
    if route == "small_sample":
        tau = TAU0
        t0, mu, A, share = calibrate(t0_q, tau, m_samp, n_unit, "fix")
    else:
        target = SHARE_TARGET[(level, t0_q)]
        tau = tau_for(t0_q, target, m_samp, n_unit)
        t0, mu, A, share = calibrate(t0_q, tau, m_samp, n_unit, "fix")

    rng = seed_for(f"exp18|{route}|{level}|{t0_q}|{K}")
    z = psu_means(rng, REPS * (K + 1), t0, tau, n_unit)
    Ftrue = z.mean(axis=(1, 2)).reshape(REPS, K + 1)
    Dtrue = true_D(z, m_samp).reshape(REPS, K + 1)
    Fh, Dh_all = draw_sample(rng, z, m_samp)
    Fh, Dh_all = Fh.reshape(REPS, K + 1), Dh_all.reshape(REPS, K + 1)

    Y = Fh[:, :K] - mu
    Dc = Dtrue[:, :K]
    Dh = np.maximum(Dh_all[:, :K], FLOOR)
    Gnew = Ftrue[:, K] - mu

    vL2 = nu * Dh / chi2.ppf(1.0 - ETA2 / K, nu)
    AU_piv = pivot_AU(Y, vL2, K, False)
    AU_fit = pivot_AU(Y, vL2, K - 1, True)

    Dsm = gvf_prop(Dh, Fh[:, :K])
    Z = Y ** 2 - Dh
    A0 = np.maximum(Z.mean(1), FLOOR)[:, None]
    w = opt_w(A0, Dsm, nu)
    AU_pct = np.empty(REPS)
    rng2 = seed_for(f"exp18boot|{route}|{level}|{t0_q}|{K}")
    for b in range(REPS):
        j = rng2.integers(0, K, size=(B_BOOT, K))
        Zb, Dhb, Fb = Z[b][j], Dh[b][j], Fh[b, :K][j]
        Dsb = gvf_prop(Dhb, Fb)
        A0b = np.maximum(Zb.mean(1), FLOOR)[:, None]
        wb = opt_w(A0b, Dsb, nu)
        AU_pct[b] = np.quantile((Zb * wb).sum(1) / wb.sum(1), 1 - ETA1)

    m = conformal_rank(K, ALPHA0)
    absY = np.abs(Y)
    band = {"oracle": np.sort(absY / np.sqrt(1.0 + Dc / A), axis=1)[:, m - 1],
            "uncorrected": np.sort(absY, axis=1)[:, m - 1]}
    for nm, AU in (("piv", AU_piv), ("piv_fit", AU_fit), ("pct", AU_pct)):
        band[nm] = np.sort(absY / np.sqrt(1.0 + vL2 / np.maximum(AU, FLOOR)[:, None]),
                           axis=1)[:, m - 1]
    band["pct_normal"] = norm.ppf(1 - ALPHA0 / 2) * np.sqrt(np.maximum(AU_pct, 0))

    wc, bc = within_corr(seed_for(f"exp18wc|{route}|{level}|{t0_q}"),
                         t0, tau, m_samp, n_unit)
    std = Y / np.sqrt(A + Dc)
    out = dict(route=route, level=level, t0_q=t0_q, K=K, reps=REPS, B=B_BOOT,
               m_samp=m_samp, n_unit=n_unit, nu=nu, tau=tau, t0=t0, mu=mu, A=A,
               Dbar_over_A=share, m=m, nominal=m / (K + 1.0),
               oracle_scale_factor=float(1 / np.sqrt(1 + share)),
               mc_se=float(np.sqrt(.9 * .1 / REPS)),
               skew_std=float(skew(std.ravel())),
               kurt_std=float(kurtosis(std.ravel())),
               vL_simultaneous_cov=float((vL2 <= Dc).all(axis=1).mean()),
               pr_D_zero=float((Dc <= 0).mean()),
               pr_Dhat_zero=float((Dh_all[:, :K] <= 0).mean()),
               corr_within=wc, corr_between=bc,
               AU_piv_cov=float((AU_piv >= A).mean()),
               AU_fit_cov=float((AU_fit >= A).mean()),
               AU_pct_cov=float((AU_pct >= A).mean()))
    for nm, bd in band.items():
        out[f"{nm}_cov"] = float((np.abs(Gnew) <= bd).mean())
        out[f"{nm}_w"] = float(bd.mean())
        if nm not in ("oracle",):
            out[f"{nm}_over_oracle"] = float(np.mean(bd / band["oracle"]))
            out[f"{nm}_contain"] = float((bd >= band["oracle"]).mean())
        if nm not in ("oracle", "uncorrected"):
            out[f"{nm}_over_uncorr"] = float(np.mean(bd / band["uncorrected"]))
    return out


SHARE_TARGET = {}


def main():
    global SHARE_TARGET
    for lev, (ms, nu_) in SMALL.items():
        for q in (0.50, 0.15):
            SHARE_TARGET[(lev, q)] = calibrate(q, TAU0, ms, nu_, "fix")[3]
    print("realised Dbar/A of the small_sample designs, matched by low_signal:")
    for k, v in SHARE_TARGET.items():
        print(f"   {k}: {v:.4f}")

    rows = [run(r, lev, q, K)
            for r in ("small_sample", "low_signal")
            for lev in ("S1", "S2") for q in (0.50, 0.15) for K in (60, 200)]
    df = pd.DataFrame(rows)
    out = ROOT / "results" / "exp18_regional_share.csv"
    df.to_csv(out, index=False)
    (ROOT / "results" / "exp18_manifest.json").write_text(json.dumps(dict(
        experiment="exp18_regional_share", reps=REPS, B=B_BOOT, cells=len(df),
        eta1=ETA1, eta2=ETA2, alpha0=ALPHA0, sigma_alpha=SIGMA_A,
        share_targets={f"{k[0]}|{k[1]}": v for k, v in SHARE_TARGET.items()},
        y2_piv_cov=[float(df.piv_cov.min()), float(df.piv_cov.max())],
        y3_piv_over_uncorr=[float(df.piv_over_uncorr.min()),
                            float(df.piv_over_uncorr.max())],
        y4_oracle_cov=[float(df.oracle_cov.min()), float(df.oracle_cov.max())],
        y5_pct_AU_cov=[float(df.AU_pct_cov.min()), float(df.AU_pct_cov.max())],
        vL_cov=[float(df.vL_simultaneous_cov.min()),
                float(df.vL_simultaneous_cov.max())],
    ), indent=2) + "\n")

    pd.set_option("display.width", 250, "display.max_columns", 70)
    lab = ["route", "level", "t0_q", "K"]
    print("\n=== the two routes at matched design share")
    print(df.set_index(lab)[["nu", "tau", "Dbar_over_A", "oracle_scale_factor",
                             "A", "skew_std", "kurt_std", "pr_D_zero",
                             "pr_Dhat_zero"]].round(4).to_string())
    print("\n=== diagnostics corrected from exp17")
    print(df.set_index(lab)[["vL_simultaneous_cov", "corr_within", "corr_between"]]
          .round(4).to_string())
    print("\n=== Y4: the oracle band   (nominal m/(K+1), MC SE ~0.0067)")
    print(df.set_index(lab)[["nominal", "oracle_cov", "oracle_w"]].round(4).to_string())
    print("\n=== Y2/Y5: scale limits and latent-target coverage, guaranteed 0.90")
    print(df.set_index(lab)[["AU_piv_cov", "AU_fit_cov", "AU_pct_cov",
                             "piv_cov", "pct_cov", "pct_normal_cov",
                             "uncorrected_cov"]].round(4).to_string())
    print("\n=== Y3: is the correction worth doing here?")
    print(df.set_index(lab)[["uncorrected_over_oracle", "piv_over_oracle",
                             "pct_over_oracle", "piv_over_uncorr",
                             "pct_over_uncorr", "piv_contain"]].round(4).to_string())
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
