"""exp26 - a Gaussian competitor for the same target, information and level.

Protocol: docs/PROTOCOL_exp26_same_target.md (written before execution).

The comparator predicts the SAME object: theta_new = mu + u_new, the latent
value of a population with no direct estimate.  It is built from the same
structure confidence set and the same certified scale bound, so the two arms
differ only in how the remaining alpha_0 is spent: a conformal rank, or a normal
quantile plus a chi-square bound on A.  The competitor's budget split is scanned
and the narrowest valid choice given to it.

    python experiments/exp26_same_target.py
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2, norm, f as fdist
from scipy.special import polygamma

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from dac.bands import conformal_rank                        # noqa: E402

REPS, NULL_DRAWS = 10000, 200000
A_TRUE, GAMMA0 = 1.0, 1.0
ALPHA0, ETA_G, ETA_T = 0.05, 0.025, 0.025
SLACK = 1e-9
SPLITS = np.array([0.01, 0.02, 0.03, 0.04, 0.045])   # alpha_1; alpha_2 = a0 - a1


def seed_for(label):
    return np.random.default_rng(
        int.from_bytes(hashlib.sha256(label.encode()).digest()[:8], "little"))


def a_of(x, g):
    v = x ** (-g)
    return v / v.mean(axis=-1, keepdims=True)


def certified_d_lo(x, Dh, nu_c, nu, gL, gU):
    lx = np.log(x)
    def fdf(g):
        xg = x ** g[:, None]; xmg = x ** (-g[:, None])
        P = (nu_c * Dh * xg).sum(1); dP = (nu_c * Dh * xg * lx).sum(1)
        Q = xmg.mean(1); dQ = -(xmg * lx).mean(1)
        return P * Q / nu, (dP * Q + P * dQ) / nu
    fL, dL = fdf(gL); fU, dU = fdf(gU)
    a, b = gL.copy(), gU.copy()
    for _ in range(60):
        mid = 0.5 * (a + b); neg = fdf(mid)[1] < 0.0
        a = np.where(neg, mid, a); b = np.where(neg, b, mid)
    fa, da = fdf(a)
    return np.where(dL >= 0, fL, np.where(dU <= 0, fU,
                                          np.maximum(0.0, fa + da * (b - a))))


def run(K, d_over_A, nu0, sig_mis):
    rng = seed_for(f"exp26|{K}|{d_over_A}|{nu0}|{sig_mis}")
    x = rng.lognormal(0.0, 0.7, size=K)
    lx = np.log(x); lxc = lx - lx.mean(); Sxx = float((lxc ** 2).sum())
    nu_c = np.full(K, float(nu0)); nu = float(nu_c.sum())
    sig_e = float(np.sqrt(polygamma(1, nu0 / 2.0)))

    a_true = a_of(x, GAMMA0)
    if sig_mis > 0:
        a_true = a_true * rng.lognormal(0.0, sig_mis, size=K)
        a_true /= a_true.mean()
    d = A_TRUE * d_over_A
    D = d * a_true
    t0 = d / A_TRUE
    m = conformal_rank(K, ALPHA0)

    r2 = seed_for(f"exp26null|{K}|{nu0}")
    c = lxc / (sig_e * np.sqrt(Sxx))
    w = float(np.quantile(np.abs(
        np.log(r2.chisquare(nu_c, size=(NULL_DRAWS, K)) / nu_c) @ c), 1 - ETA_G))

    Y = rng.normal(0.0, np.sqrt(A_TRUE + D), size=(REPS, K))
    absY, Y2 = np.abs(Y), Y ** 2
    Dhat = D * rng.chisquare(nu_c, size=(REPS, K)) / nu_c
    u_new = rng.normal(0.0, np.sqrt(A_TRUE), size=REPS)     # the latent target

    ghat = -(np.log(Dhat) @ lxc) / Sxx
    half = w * sig_e / np.sqrt(Sxx)
    gL, gU = ghat - half, ghat + half

    # ---- the shared certified scale machinery ---------------------------
    t_start = time.perf_counter()
    q = float(fdist.ppf(1.0 - ETA_T, nu, K))
    a_lo = np.minimum(a_of(x, gL[:, None]), a_of(x, gU[:, None])) * (1 - SLACK)
    d_lo = certified_d_lo(x, Dhat, nu_c, nu, gL, gU) * (1 - SLACK)
    tgt = K * d_lo / q
    bad = (tgt <= 0) | (tgt > (Y2 / a_lo).sum(1))
    lo = np.full(REPS, 1e-14); hi = np.full(REPS, 1e14)
    for _ in range(120):
        mid = np.sqrt(lo * hi)
        below = (mid[:, None] * Y2 / (1.0 + mid[:, None] * a_lo)).sum(1) >= tgt
        hi = np.where(below, mid, hi); lo = np.where(below, lo, mid)
    t_cert = np.where(bad, 0.0, lo)
    t_scale = time.perf_counter() - t_start

    hit = lambda b: float((np.abs(u_new) <= b).mean())
    band = {"oracle": np.sort(absY / np.sqrt(1.0 + t0 * a_true), axis=1)[:, m - 1],
            "uncorrected": np.sort(absY, axis=1)[:, m - 1]}

    t0c = time.perf_counter()
    band["conformal"] = np.sort(
        absY / np.sqrt(1.0 + t_cert[:, None] * a_lo), axis=1)[:, m - 1]
    t_conf = time.perf_counter() - t0c

    # ---- the Gaussian competitor, same budget, best split given to it ----
    t0g = time.perf_counter()
    Sbar = (Y2 / (1.0 + t_cert[:, None] * a_lo)).sum(1)
    best = None
    for a1 in SPLITS:
        a2 = ALPHA0 - a1
        AU = Sbar / chi2.ppf(a2, K)
        b = norm.ppf(1 - a1 / 2.0) * np.sqrt(np.maximum(AU, 0.0))
        if best is None or b.mean() < best[0]:
            best = (float(b.mean()), b, float(a1), float(a2))
    t_gauss = time.perf_counter() - t0g
    band["gaussian"] = best[1]
    # a split fixed in advance, reported beside the data-chosen one
    a1f = a2f = ALPHA0 / 2.0
    band["gaussian_fixed"] = norm.ppf(1 - a1f / 2.0) * np.sqrt(
        np.maximum(Sbar / chi2.ppf(a2f, K), 0.0))
    band["gaussian_plugin"] = norm.ppf(1 - ALPHA0 / 2.0) * np.sqrt(
        np.maximum((Y2 - Dhat).mean(1), 0.0))

    vL_b = nu_c * Dhat / chi2.ppf(1.0 - 0.025 / K, nu_c)
    qb = float(chi2.ppf(0.025, K))
    lo2, hi2 = np.zeros(REPS), np.full(REPS, 1e4)
    for _ in range(70):
        mid = 0.5 * (lo2 + hi2)
        below = (Y2 / (mid[:, None] + vL_b)).sum(1) < qb
        hi2 = np.where(below, mid, hi2); lo2 = np.where(below, lo2, mid)
    band["sep_bonf"] = np.sort(
        absY / np.sqrt(1.0 + vL_b / np.maximum(0.5 * (lo2 + hi2), 1e-12)[:, None]),
        axis=1)[:, m - 1]

    out = dict(K=K, d_over_A=d_over_A, nu_per_pop=nu0, sig_mis=sig_mis, reps=REPS,
               m=m, nominal=m / (K + 1.0), guarantee=1 - ALPHA0 - ETA_G - ETA_T,
               alpha1=best[2], alpha2=best[3], fallback=float(bad.mean()),
               mc_se=float(np.sqrt(.95 * .05 / REPS)),
               ms_scale=1e3 * t_scale / REPS, ms_conformal=1e3 * t_conf / REPS,
               ms_gaussian=1e3 * t_gauss / REPS)
    for nm, b in band.items():
        out[f"{nm}_cov"] = hit(b)
        out[f"{nm}_w"] = float(b.mean())
        if nm != "oracle":
            out[f"{nm}_over_oracle"] = float(np.mean(b / band["oracle"]))
    out["gauss_over_conformal"] = float(np.mean(band["gaussian"]
                                                / band["conformal"]))
    out["gaussfix_over_conformal"] = float(np.mean(band["gaussian_fixed"]
                                                   / band["conformal"]))
    # reduction relative to the competitor, which is 1 - 1/ratio
    out["conformal_narrower_pct"] = float(
        100.0 * (1.0 - 1.0 / out["gauss_over_conformal"]))
    out["nominal_conformal"] = 1 - ALPHA0 - ETA_G - ETA_T
    out["nominal_gaussian"] = 1 - ALPHA0 - ETA_G - ETA_T
    out["nominal_plugin"] = 1 - ALPHA0
    return out


def main():
    rows = [run(K, da, nu0, sm) for K in (60, 200) for da in (0.5, 1.0)
            for nu0 in (8, 16) for sm in (0.0, 0.4)]
    df = pd.DataFrame(rows)
    out = ROOT / "results" / "exp26_same_target.csv"
    df.to_csv(out, index=False)
    ok, mis = df[df.sig_mis == 0], df[df.sig_mis > 0]
    (ROOT / "results" / "exp26_manifest.json").write_text(json.dumps(dict(
        experiment="exp26_same_target", reps=REPS, cells=len(df),
        alpha0=ALPHA0, eta_gamma=ETA_G, eta_t=ETA_T,
        guarantee=1 - ALPHA0 - ETA_G - ETA_T,
        g1_cov=[float(ok.conformal_cov.min()), float(ok.gaussian_cov.min())],
        g2_gauss_over_conformal=[float(df.gauss_over_conformal.min()),
                                 float(df.gauss_over_conformal.max())],
        splits_chosen=sorted(set(df.alpha1.round(3))),
        plugin_cov=[float(df.gaussian_plugin_cov.min()),
                    float(df.gaussian_plugin_cov.max())],
    ), indent=2) + "\n")
    pd.set_option("display.width", 240, "display.max_columns", 60)
    lab = ["K", "d_over_A", "nu_per_pop"]
    for tag, sub in (("CORRECTLY SPECIFIED", ok), ("MISSPECIFIED", mis)):
        print(f"\n########## {tag}   (guarantee {1-ALPHA0-ETA_G-ETA_T:.2f})")
        print("coverage and realised width first")
        print(sub.set_index(lab)[["oracle_cov", "conformal_cov", "gaussian_cov",
                                  "gaussian_plugin_cov", "sep_bonf_cov",
                                  "oracle_w", "conformal_w", "gaussian_w"]]
              .round(4).to_string())
        print("\npaired width ratio, chosen budget split, and cost per replicate (ms)")
        print(sub.set_index(lab)[["gauss_over_conformal", "gaussfix_over_conformal",
                                  "conformal_narrower_pct", "conformal_over_oracle",
                                  "gaussian_over_oracle", "alpha1", "alpha2",
                                  "ms_scale", "ms_conformal", "ms_gaussian"]]
              .round(4).to_string())
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
