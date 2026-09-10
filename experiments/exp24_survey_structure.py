"""exp24 - the fixed certified method on the two complex-survey routes.

Protocol: docs/PROTOCOL_exp24_survey_structure.md (written before execution).
Predecessors: exp18 (routes) and exp23 (the fixed method).  No method chosen or
changed here; no comparator added.

Populations are given different numbers of sampled PSUs so that an exogenous
structure variable exists: x_c = m_c, known before any estimate is seen.  The
structure family d x_c^{-gamma} is misspecified by construction, since the true
design variance of a proportion also carries p(1-p) and the cluster structure.

    python experiments/exp24_survey_structure.py
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
TAU0 = 0.45
ALPHA0 = 0.05
ETA_G = ETA_T = 0.025
SLACK = 1e-9
ROUTES = {"S1": dict(m_lo=4, m_hi=8, n_unit=10),      # richer designs
          "S2": dict(m_lo=2, m_hi=5, n_unit=4)}       # small-sample route


def seed_for(label):
    return np.random.default_rng(
        int.from_bytes(hashlib.sha256(label.encode()).digest()[:8], "little"))


def psu_means(rng, npop, t0, tau, n_unit):
    mu = rng.normal(0.0, tau, size=(npop, 1, 1))
    a = rng.normal(0.0, SIGMA_A, size=(npop, H, M))
    p = norm.cdf((t0 - mu - a) / SIGMA_EPS)
    return rng.binomial(n_unit, p) / n_unit


def design_stats(z, m_c):
    """Exact design variance and its ultimate-cluster estimator, per population."""
    npop = z.shape[0]
    S2 = z.var(axis=2, ddof=1)                                   # (npop, H)
    D = ((1.0 - m_c / M) / m_c)[:, None] * S2
    return D.sum(axis=1) / H ** 2


def draw_sample(rng, z, m_c):
    npop = z.shape[0]
    order = np.argsort(rng.random((npop, H, M)), axis=2)
    mask = np.arange(M)[None, None, :] < m_c[:, None, None]
    zs = np.take_along_axis(z, order, axis=2)
    zs = np.where(mask, zs, np.nan)
    Fh = np.nanmean(np.nanmean(zs, axis=2), axis=1)
    s2 = np.nanvar(zs, axis=2, ddof=1)
    Dh = (((1.0 - m_c / M) / m_c)[:, None] * s2).sum(axis=1) / H ** 2
    return Fh, Dh


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
        mid = 0.5 * (a + b)
        neg = fdf(mid)[1] < 0.0
        a = np.where(neg, mid, a); b = np.where(neg, b, mid)
    fa, da = fdf(a)
    interior = np.maximum(0.0, fa + da * (b - a))
    return np.where(dL >= 0, fL, np.where(dU <= 0, fU, interior))


def cert_band(absY, Y2, x, Dh, nu_c, nu, gL, gU, K, m):
    q = float(fdist.ppf(1.0 - ETA_T, nu, K))
    aL = x ** (-gL[:, None]); aL /= aL.mean(1, keepdims=True)
    aU = x ** (-gU[:, None]); aU /= aU.mean(1, keepdims=True)
    a_lo = np.minimum(aL, aU) * (1 - SLACK)
    d_lo = certified_d_lo(x, Dh, nu_c, nu, gL, gU) * (1 - SLACK)
    tgt = K * d_lo / q
    bad = (tgt <= 0) | (tgt > (Y2 / a_lo).sum(1))
    lo = np.full(K if False else absY.shape[0], 1e-14)
    hi = np.full(absY.shape[0], 1e14)
    for _ in range(120):
        mid = np.sqrt(lo * hi)
        below = (mid[:, None] * Y2 / (1.0 + mid[:, None] * a_lo)).sum(1) >= tgt
        hi = np.where(below, mid, hi); lo = np.where(below, lo, mid)
    t = np.where(bad, 0.0, lo)
    return np.sort(absY / np.sqrt(1.0 + t[:, None] * a_lo), axis=1)[:, m - 1], \
        float(bad.mean())


def A_upper(Y2, vL2, K, eta1):
    q = float(chi2.ppf(eta1, K))
    lo, hi = np.zeros(Y2.shape[0]), np.full(Y2.shape[0], 10.0)
    for _ in range(70):
        mid = 0.5 * (lo + hi)
        below = (Y2 / (mid[:, None] + vL2)).sum(1) < q
        hi = np.where(below, mid, hi); lo = np.where(below, lo, mid)
    return 0.5 * (lo + hi)


def calibrate(t0_q, tau, route, npop=60000):
    cfg = ROUTES[route]
    rng = seed_for(f"exp24cal|{t0_q}|{tau:.6f}|{route}")
    t0 = norm.ppf(t0_q) * np.sqrt(tau ** 2 + SIGMA_A ** 2 + SIGMA_EPS ** 2)
    F, D = [], []
    for _ in range(3):
        z = psu_means(rng, npop // 3, t0, tau, cfg["n_unit"])
        mc = rng.integers(cfg["m_lo"], cfg["m_hi"] + 1, size=z.shape[0])
        F.append(z.mean(axis=(1, 2))); D.append(design_stats(z, mc))
    F, D = np.concatenate(F), np.concatenate(D)
    A = float(F.var(ddof=1))
    return t0, float(F.mean()), A, float(D.mean() / A)


def tau_for(t0_q, target, route):
    lo, hi = 0.005, 1.5
    for _ in range(22):
        mid = 0.5 * (lo + hi)
        if calibrate(t0_q, mid, route, 20000)[3] > target: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)


SHARE = {}


def run(route, level, t0_q, K):
    cfg = ROUTES[level]
    if route == "small_sample":
        tau = TAU0
    else:
        tau = tau_for(t0_q, SHARE[(level, t0_q)], level)
    t0, mu, A, share = calibrate(t0_q, tau, level)
    rng = seed_for(f"exp24|{route}|{level}|{t0_q}|{K}")

    m_c = rng.integers(cfg["m_lo"], cfg["m_hi"] + 1, size=K).astype(float)
    x = m_c.copy()
    nu_c = H * (m_c - 1.0); nu = float(nu_c.sum())
    m_all = np.concatenate([m_c, [float(rng.integers(cfg["m_lo"], cfg["m_hi"] + 1))]])

    z = psu_means(rng, REPS * (K + 1), t0, tau, cfg["n_unit"])
    mrep = np.tile(m_all, REPS)
    Ftrue = z.mean(axis=(1, 2)).reshape(REPS, K + 1)
    Dtrue = design_stats(z, mrep).reshape(REPS, K + 1)
    Fh, Dh_all = draw_sample(rng, z, mrep)
    Fh = Fh.reshape(REPS, K + 1); Dh_all = Dh_all.reshape(REPS, K + 1)

    Y = Fh[:, :K] - mu
    absY, Y2 = np.abs(Y), Y ** 2
    Dc = Dtrue[:, :K]
    Dh = np.maximum(Dh_all[:, :K], 1e-14)
    Gnew = Ftrue[:, K] - mu
    mm = conformal_rank(K, ALPHA0)

    # block 1: how well does the structure family describe the true D_c?
    lx = np.log(x); lxc = lx - lx.mean(); Sxx = float((lxc ** 2).sum())
    lD = np.log(np.maximum(Dc, 1e-300))
    slope = (lD @ lxc) / Sxx            # regression of log D_c on log x_c
    gamma_ls = -slope                    # the gamma the family would need
    resid = lD - (lD.mean(1, keepdims=True) + slope[:, None] * lxc)
    r2 = 1.0 - resid.var(1) / np.maximum(lD.var(1), 1e-300)

    # C_gamma with heterogeneous nu_c: null law simulated with the actual nu_c
    r2rng = seed_for(f"exp24null|{route}|{level}|{t0_q}|{K}")
    eps = np.log(r2rng.chisquare(nu_c, size=(NULL_DRAWS, K)) / nu_c)
    W0 = eps @ lxc
    wq = float(np.quantile(np.abs(W0), 1 - ETA_G))
    ghat = -(np.log(Dh) @ lxc) / Sxx
    half = wq / Sxx
    gL, gU = ghat - half, ghat + half

    band = {"oracle": np.sort(absY / np.sqrt(1.0 + Dc / A), axis=1)[:, mm - 1],
            "uncorrected": np.sort(absY, axis=1)[:, mm - 1]}
    vL_b = nu_c * Dh / chi2.ppf(1.0 - 0.025 / K, nu_c)
    AU_b = A_upper(Y2, vL_b, K, 0.025)
    band["sep_bonf"] = np.sort(
        absY / np.sqrt(1.0 + vL_b / np.maximum(AU_b, 1e-12)[:, None]), axis=1)[:, mm - 1]
    band["Cg_cert"], fb = cert_band(absY, Y2, x, Dh, nu_c, nu, gL, gU, K, mm)

    hit = lambda b: float((np.abs(Gnew) <= b).mean())
    out = dict(route=route, level=level, t0_q=t0_q, K=K, reps=REPS, A=A, mu=mu,
               Dbar_over_A=share, nu_min=float(nu_c.min()), nu_max=float(nu_c.max()),
               m=mm, nominal=mm / (K + 1.0), mc_se=float(np.sqrt(.9 * .1 / REPS)),
               struct_R2=float(r2.mean()), struct_gamma_ls=float(gamma_ls.mean()),
               struct_gamma_ls_sd=float(gamma_ls.std()),
               struct_resid_sd=float(resid.std(1).mean()),
               Cg_halfwidth=float(half),
               Cg_contains_gamma_ls=float(((gL <= gamma_ls)
                                           & (gamma_ls <= gU)).mean()),
               fallback_rate=fb,
               pr_Dhat_zero=float((Dh_all[:, :K] <= 0).mean()),
               corr_Dhat_Y=float(np.corrcoef(Dh.ravel(), Y.ravel())[0, 1]))
    for nm, b in band.items():
        out[f"{nm}_cov"] = hit(b)
        out[f"{nm}_w"] = float(b.mean())
        if nm != "oracle":
            out[f"{nm}_contain"] = float((b >= band["oracle"]).mean())
            out[f"{nm}_over_oracle"] = float(np.mean(b / band["oracle"]))
    av = out["uncorrected_over_oracle"] - 1.0
    for nm in ("sep_bonf", "Cg_cert"):
        out[f"captured_{nm}"] = float((av - (out[f"{nm}_over_oracle"] - 1)) / av) \
            if av > 0 else float("nan")
    out["cert_over_sepbonf"] = float(np.mean(band["Cg_cert"] / band["sep_bonf"]))
    return out


def main():
    global SHARE
    for lev in ROUTES:
        for q in (0.50, 0.15):
            SHARE[(lev, q)] = calibrate(q, TAU0, lev)[3]
    print("matched design shares (small_sample route):",
          {f"{k[0]}|{k[1]}": round(v, 4) for k, v in SHARE.items()})
    rows = [run(r, lev, q, K) for r in ("small_sample", "low_signal")
            for lev in ("S1", "S2") for q in (0.50, 0.15) for K in (60, 200)]
    df = pd.DataFrame(rows)
    out = ROOT / "results" / "exp24_survey_structure.csv"
    df.to_csv(out, index=False)
    (ROOT / "results" / "exp24_manifest.json").write_text(json.dumps(dict(
        experiment="exp24_survey_structure", reps=REPS, cells=len(df),
        alpha0=ALPHA0, eta_gamma=ETA_G, eta_t=ETA_T,
        structure_variable="x_c = sampled PSU count m_c, fixed before running",
        s1_struct_R2=[float(df.struct_R2.min()), float(df.struct_R2.max())],
        s2_cov=[float(df.Cg_cert_cov.min()), float(df.Cg_cert_cov.max())],
        s3_contain=[float(df.Cg_cert_contain.min()), float(df.Cg_cert_contain.max())],
        s4_over_sepbonf=[float(df.cert_over_sepbonf.min()),
                         float(df.cert_over_sepbonf.max())],
    ), indent=2) + "\n")
    pd.set_option("display.width", 250, "display.max_columns", 70)
    lab = ["route", "level", "t0_q", "K"]
    print("\n=== 1. structure explanatory power (x_c = sampled PSUs, fixed in advance)")
    print(df.set_index(lab)[["Dbar_over_A", "nu_min", "nu_max", "struct_R2",
                             "struct_gamma_ls", "struct_gamma_ls_sd", "struct_resid_sd", "pr_Dhat_zero",
                             "corr_Dhat_Y"]].round(4).to_string())
    print("\n=== 2. inference stage")
    print(df.set_index(lab)[["Cg_halfwidth", "Cg_contains_gamma_ls",
                             "Cg_cert_contain", "sep_bonf_contain",
                             "fallback_rate"]].round(4).to_string())
    print("\n=== 3. final performance, guaranteed 0.90 in the restricted model")
    print(df.set_index(lab)[["oracle_cov", "Cg_cert_cov", "sep_bonf_cov",
                             "uncorrected_cov", "Cg_cert_over_oracle",
                             "sep_bonf_over_oracle", "cert_over_sepbonf",
                             "captured_Cg_cert", "captured_sep_bonf"]]
          .round(4).to_string())
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
