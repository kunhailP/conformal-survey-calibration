"""exp25 - the remaining high design-share cells, and a true-structure diagnostic.

Protocol: docs/PROTOCOL_exp25_high_share.md (written before execution).
Method, structure variable and error budget are those fixed in exp23/exp24 and
are not changed after seeing results.  This completes the agreed validation
range; it does not search for better conditions.

    python experiments/exp25_high_share.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2, norm, f as fdist

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from dac.bands import conformal_rank                        # noqa: E402

REPS, NULL_DRAWS = 2000, 100000
H, M = 4, 20
SIGMA_EPS, SIGMA_A = 1.0, 0.4
ALPHA0, ETA_G, ETA_T = 0.05, 0.025, 0.025
ETA_DIAG = 0.05
SLACK = 1e-9
ROUTES = {"small_sample": dict(m_lo=2, m_hi=3, n_unit=2),
          "low_signal":  dict(m_lo=4, m_hi=8, n_unit=10)}
TARGETS = (0.55, 0.75)


def seed_for(label):
    return np.random.default_rng(
        int.from_bytes(hashlib.sha256(label.encode()).digest()[:8], "little"))


def psu_means(rng, npop, t0, tau, n_unit):
    mu = rng.normal(0.0, tau, size=(npop, 1, 1))
    a = rng.normal(0.0, SIGMA_A, size=(npop, H, M))
    return rng.binomial(n_unit, norm.cdf((t0 - mu - a) / SIGMA_EPS)) / n_unit


def true_D(z, m_c):
    return (((1.0 - m_c / M) / m_c)[:, None] * z.var(axis=2, ddof=1)).sum(1) / H ** 2


def draw_sample(rng, z, m_c):
    order = np.argsort(rng.random(z.shape), axis=2)
    mask = np.arange(M)[None, None, :] < m_c[:, None, None]
    zs = np.where(mask, np.take_along_axis(z, order, axis=2), np.nan)
    Fh = np.nanmean(np.nanmean(zs, axis=2), axis=1)
    Dh = (((1.0 - m_c / M) / m_c)[:, None]
          * np.nanvar(zs, axis=2, ddof=1)).sum(1) / H ** 2
    return Fh, Dh


def calibrate(t0_q, tau, route, npop=45000):
    cfg = ROUTES[route]
    rng = seed_for(f"exp25cal|{t0_q}|{tau:.6f}|{route}")
    t0 = norm.ppf(t0_q) * np.sqrt(tau ** 2 + SIGMA_A ** 2 + SIGMA_EPS ** 2)
    F, D = [], []
    for _ in range(3):
        z = psu_means(rng, npop // 3, t0, tau, cfg["n_unit"])
        mc = rng.integers(cfg["m_lo"], cfg["m_hi"] + 1, size=z.shape[0]).astype(float)
        F.append(z.mean(axis=(1, 2))); D.append(true_D(z, mc))
    F, D = np.concatenate(F), np.concatenate(D)
    A = float(F.var(ddof=1))
    return t0, float(F.mean()), A, float(D.mean() / A)


def tau_for(t0_q, target, route):
    lo, hi = 0.003, 1.5
    for _ in range(24):
        mid = 0.5 * (lo + hi)
        if calibrate(t0_q, mid, route, 15000)[3] > target: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)


def invert(Y2, a_lo, tgt):
    lo = np.full(Y2.shape[0], 1e-14); hi = np.full(Y2.shape[0], 1e14)
    for _ in range(120):
        mid = np.sqrt(lo * hi)
        below = (mid[:, None] * Y2 / (1.0 + mid[:, None] * a_lo)).sum(1) >= tgt
        hi = np.where(below, mid, hi); lo = np.where(below, lo, mid)
    return lo


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


def A_upper(Y2, vL2, K, eta1):
    q = float(chi2.ppf(eta1, K))
    lo, hi = np.zeros(Y2.shape[0]), np.full(Y2.shape[0], 10.0)
    for _ in range(70):
        mid = 0.5 * (lo + hi)
        below = (Y2 / (mid[:, None] + vL2)).sum(1) < q
        hi = np.where(below, mid, hi); lo = np.where(below, lo, mid)
    return 0.5 * (lo + hi)


def run(route, target, t0_q, K):
    cfg = ROUTES[route]
    tau = tau_for(t0_q, target, route)
    t0, mu, A, share = calibrate(t0_q, tau, route)
    rng = seed_for(f"exp25|{route}|{target}|{t0_q}|{K}")
    m_c = rng.integers(cfg["m_lo"], cfg["m_hi"] + 1, size=K).astype(float)
    x = m_c.copy(); nu_c = H * (m_c - 1.0); nu = float(nu_c.sum())
    m_all = np.concatenate([m_c, [float(rng.integers(cfg["m_lo"], cfg["m_hi"] + 1))]])
    z = psu_means(rng, REPS * (K + 1), t0, tau, cfg["n_unit"])
    mrep = np.tile(m_all, REPS)
    Ftrue = z.mean(axis=(1, 2)).reshape(REPS, K + 1)
    Dtrue = true_D(z, mrep).reshape(REPS, K + 1)
    Fh, Dh_all = draw_sample(rng, z, mrep)
    Fh = Fh.reshape(REPS, K + 1); Dh_all = Dh_all.reshape(REPS, K + 1)

    Y = Fh[:, :K] - mu; absY, Y2 = np.abs(Y), Y ** 2
    Dc = Dtrue[:, :K]; Dh = np.maximum(Dh_all[:, :K], 1e-14)
    Gnew = Ftrue[:, K] - mu; mm = conformal_rank(K, ALPHA0)

    lx = np.log(x); lxc = lx - lx.mean(); Sxx = float((lxc ** 2).sum())
    lD = np.log(np.maximum(Dc, 1e-300))
    gamma_ls = -(lD @ lxc) / Sxx
    resid = lD - (lD.mean(1, keepdims=True) - gamma_ls[:, None] * lxc)
    r2 = 1.0 - resid.var(1) / np.maximum(lD.var(1), 1e-300)

    rr = seed_for(f"exp25null|{route}|{target}|{t0_q}|{K}")
    W0 = np.log(rr.chisquare(nu_c, size=(NULL_DRAWS, K)) / nu_c) @ lxc
    wq = float(np.quantile(np.abs(W0), 1 - ETA_G))
    ghat = -(np.log(Dh) @ lxc) / Sxx
    half = wq / Sxx; gL, gU = ghat - half, ghat + half

    band = {"oracle": np.sort(absY / np.sqrt(1.0 + Dc / A), axis=1)[:, mm - 1],
            "uncorrected": np.sort(absY, axis=1)[:, mm - 1]}
    vL_b = nu_c * Dh / chi2.ppf(1.0 - 0.025 / K, nu_c)
    AU_b = A_upper(Y2, vL_b, K, 0.025)
    band["sep_bonf"] = np.sort(
        absY / np.sqrt(1.0 + vL_b / np.maximum(AU_b, 1e-12)[:, None]), axis=1)[:, mm - 1]

    q = float(fdist.ppf(1.0 - ETA_T, nu, K))
    aL = x ** (-gL[:, None]); aL /= aL.mean(1, keepdims=True)
    aU = x ** (-gU[:, None]); aU /= aU.mean(1, keepdims=True)
    a_lo = np.minimum(aL, aU) * (1 - SLACK)
    d_lo = certified_d_lo(x, Dh, nu_c, nu, gL, gU) * (1 - SLACK)
    tgt = K * d_lo / q
    bad = (tgt <= 0) | (tgt > (Y2 / a_lo).sum(1))
    t = np.where(bad, 0.0, invert(Y2, a_lo, tgt))
    band["Cg_cert"] = np.sort(absY / np.sqrt(1.0 + t[:, None] * a_lo), axis=1)[:, mm - 1]

    # diagnostic: the TRUE structure supplied as known.  Infeasible on real data.
    has_zero = (Dc <= 0).any(axis=1)
    a_true = Dc / np.maximum(Dc.mean(1, keepdims=True), 1e-300)
    qd = float(fdist.ppf(1.0 - ETA_DIAG, nu, K))
    with np.errstate(divide="ignore", invalid="ignore"):
        dh_t = (nu_c * Dh / np.where(a_true > 0, a_true, np.nan)).sum(1) / nu
    ok = ~has_zero & np.isfinite(dh_t)
    tgt_t = K * dh_t / qd
    at = np.where(a_true > 0, a_true, 1.0)
    t_t = invert(Y2, at, np.where(ok, tgt_t, 0.0))
    band["ratio_true_a"] = np.where(
        ok, np.sort(absY / np.sqrt(1.0 + t_t[:, None] * at), axis=1)[:, mm - 1], np.nan)

    hit = lambda b: float(np.nanmean((np.abs(Gnew) <= b).astype(float)[np.isfinite(b)]))
    out = dict(route=route, target=target, t0_q=t0_q, K=K, reps=REPS, A=A,
               Dbar_over_A=share, rho2=share / (1.0 + share),
               nu_min=float(nu_c.min()), nu_max=float(nu_c.max()),
               m=mm, mc_se=float(np.sqrt(.9 * .1 / REPS)),
               struct_R2=float(r2.mean()), struct_gamma_ls=float(gamma_ls.mean()),
               struct_resid_sd=float(resid.std(1).mean()),
               Cg_contains_gamma_ls=float(((gL <= gamma_ls) & (gamma_ls <= gU)).mean()),
               fallback_rate=float(bad.mean()),
               pr_D_zero=float((Dc <= 0).mean()),
               pr_Dhat_zero=float((Dh_all[:, :K] <= 0).mean()),
               diag_excluded=float(has_zero.mean()),
               corr_Dhat_Y=float(np.corrcoef(Dh.ravel(), Y.ravel())[0, 1]))
    # like-for-like: every arm also scored on the subset the diagnostic can use
    common = np.isfinite(band["ratio_true_a"])
    for nm, b in band.items():
        if nm != "oracle":
            out[f"{nm}_contain_common"] = float(
                (b[common] >= band["oracle"][common]).mean())
            out[f"{nm}_over_oracle_common"] = float(
                np.mean(b[common] / band["oracle"][common]))
    for nm, b in band.items():
        f = np.isfinite(b)
        out[f"{nm}_cov"] = float((np.abs(Gnew[f]) <= b[f]).mean())
        out[f"{nm}_w"] = float(b[f].mean())
        if nm != "oracle":
            out[f"{nm}_contain"] = float((b[f] >= band["oracle"][f]).mean())
            out[f"{nm}_over_oracle"] = float(np.mean(b[f] / band["oracle"][f]))
    av = out["uncorrected_over_oracle"] - 1.0
    for nm in ("sep_bonf", "Cg_cert", "ratio_true_a"):
        out[f"captured_{nm}"] = float((av - (out[f"{nm}_over_oracle"] - 1)) / av) \
            if av > 1e-6 else float("nan")
    out["cert_over_sepbonf"] = float(np.mean(band["Cg_cert"] / band["sep_bonf"]))
    f = np.isfinite(band["ratio_true_a"])
    out["truea_over_sepbonf"] = float(np.mean(band["ratio_true_a"][f]
                                              / band["sep_bonf"][f]))
    return out


def main():
    rows = [run(r, tg, q, K) for r in ROUTES for tg in TARGETS
            for q in (0.50, 0.15) for K in (60, 200)]
    df = pd.DataFrame(rows)
    out = ROOT / "results" / "exp25_high_share.csv"
    df.to_csv(out, index=False)
    (ROOT / "results" / "exp25_manifest.json").write_text(json.dumps(dict(
        experiment="exp25_high_share", reps=REPS, cells=len(df),
        alpha0=ALPHA0, eta_gamma=ETA_G, eta_t=ETA_T, eta_diag=ETA_DIAG,
        structure_variable="x_c = m_c, fixed in exp24 and unchanged",
        realised_share=[float(df.Dbar_over_A.min()), float(df.Dbar_over_A.max())],
        r2_struct=[float(df.struct_R2.min()), float(df.struct_R2.max())],
        r2_cov=[float(df.Cg_cert_cov.min()), float(df.Cg_cert_cov.max())],
        r3_contain=[float(df.Cg_cert_contain.min()), float(df.Cg_cert_contain.max())],
        r4_truea_contain=[float(df.ratio_true_a_contain.min()),
                          float(df.ratio_true_a_contain.max())],
        r5_cert_over_sepbonf=[float(df.cert_over_sepbonf.min()),
                              float(df.cert_over_sepbonf.max())],
    ), indent=2) + "\n")
    pd.set_option("display.width", 250, "display.max_columns", 70)
    lab = ["route", "target", "t0_q", "K"]
    print("\n=== realised conditions")
    print(df.set_index(lab)[["Dbar_over_A", "rho2", "nu_min", "nu_max", "struct_R2",
                             "struct_gamma_ls", "struct_resid_sd", "pr_D_zero",
                             "pr_Dhat_zero", "diag_excluded", "corr_Dhat_Y"]]
          .round(4).to_string())
    print("\n=== coverage and realised width FIRST (guaranteed 0.90 in the restricted model)")
    print(df.set_index(lab)[["oracle_cov", "Cg_cert_cov", "ratio_true_a_cov",
                             "sep_bonf_cov", "uncorrected_cov",
                             "oracle_w", "Cg_cert_w", "ratio_true_a_w",
                             "sep_bonf_w", "uncorrected_w"]].round(4).to_string())
    print("\n=== containment (requirement 0.95 in the restricted model)")
    print(df.set_index(lab)[["Cg_cert_contain", "ratio_true_a_contain",
                             "sep_bonf_contain", "Cg_contains_gamma_ls",
                             "fallback_rate"]].round(4).to_string())
    print("\n=== containment on the subset the diagnostic can use (like-for-like)")
    print(df.set_index(lab)[["diag_excluded", "Cg_cert_contain_common",
                             "ratio_true_a_contain_common",
                             "sep_bonf_contain_common"]].round(4).to_string())
    print("\n=== width ratios; capture is secondary")
    print(df.set_index(lab)[["cert_over_sepbonf", "truea_over_sepbonf",
                             "Cg_cert_over_oracle", "ratio_true_a_over_oracle",
                             "sep_bonf_over_oracle", "captured_Cg_cert",
                             "captured_ratio_true_a", "captured_sep_bonf"]]
          .round(4).to_string())
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
