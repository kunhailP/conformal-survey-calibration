"""exp23 - the certified envelope, replacing exp22's endpoint claim.

Protocol: docs/PROTOCOL_exp23_certified.md (written before execution).

exp22 used a two-endpoint evaluation of inf_gamma t_L(gamma).  A counterexample
supplied in review reproduces exactly: the infimum can be interior, 16.9 percent
below the smaller endpoint.  The endpoint property is proved for a_c(gamma) and
does NOT transfer to t_L(gamma).

The certified bound needs no endpoint claim:
  a_lo_c = min{a_c(gL), a_c(gU)}          exact  (log a_c concave in gamma)
  d_lo   = min_gamma dhat(gamma)          certified (dhat convex in gamma:
                                           1/a_c = K^-1 sum_j (x_c/x_j)^gamma)
  Phibar(t) = sum_c t Y_c^2/(1 + t a_lo_c) >= Phi(t; gamma) for every gamma
  => t_cert = Phibar^{-1}(K d_lo / q) <= inf_gamma t_L(gamma).

    python experiments/exp23_certified.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2, f as fdist
from scipy.special import polygamma

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from dac.bands import conformal_rank                        # noqa: E402

REPS, GRID, NULL_DRAWS = 10000, 31, 200000
A_TRUE, GAMMA0 = 1.0, 1.0
ALPHA0, ETA = 0.05, 0.05
ETA_G = ETA_T = ETA / 2
ETA_1 = ETA_2 = (ETA - ETA_G) / 2


def seed_for(label):
    return np.random.default_rng(
        int.from_bytes(hashlib.sha256(label.encode()).digest()[:8], "little"))


def a_of(x, g):
    v = x ** (-g)
    return v / v.mean(axis=-1, keepdims=True)


def ord_m(z, m):
    return np.sort(z, axis=1)[:, m - 1]


def invert_increasing(f, tgt, n=90):
    """Vectorised geometric bisection of an increasing function."""
    lo = np.full(tgt.shape, 1e-12)
    hi = np.full(tgt.shape, 1e12)
    for _ in range(n):
        mid = np.sqrt(lo * hi)
        below = f(mid) >= tgt
        hi = np.where(below, mid, hi)
        lo = np.where(below, lo, mid)
    return np.sqrt(lo * hi)


def t_lower(Y2, a, dhat, K, nu, eta):
    q = float(fdist.ppf(1.0 - eta, nu, K))
    tgt = K * dhat / q
    empty = tgt > (Y2 / a).sum(1)
    t = invert_increasing(lambda t: (t[:, None] * Y2 / (1.0 + t[:, None] * a)).sum(1),
                          tgt)
    return np.where(empty, 0.0, t), empty


def certified_t(Y2, x, nu_c, Dhat, gL, gU, K, nu, eta):
    """t_cert <= inf_{gamma in [gL,gU]} t_L(gamma), by bound rather than search."""
    q = float(fdist.ppf(1.0 - eta, nu, K))
    a_lo = np.minimum(a_of(x, gL[:, None]), a_of(x, gU[:, None]))   # exact
    dh = lambda g: (nu_c * Dhat / a_of(x, g[:, None])).sum(1) / nu  # convex in g
    lo, hi = gL.copy(), gU.copy()
    for _ in range(120):                     # ternary search: convexity certifies
        m1 = lo + (hi - lo) / 3.0
        m2 = hi - (hi - lo) / 3.0
        take = dh(m1) < dh(m2)
        hi = np.where(take, m2, hi)
        lo = np.where(take, lo, m1)
    d_lo = np.minimum(np.minimum(dh(0.5 * (lo + hi)), dh(gL)), dh(gU))
    tgt = K * d_lo / q
    empty = tgt > (Y2 / a_lo).sum(1)         # no root: fall back to t = 0
    t = invert_increasing(
        lambda t: (t[:, None] * Y2 / (1.0 + t[:, None] * a_lo)).sum(1), tgt)
    return np.where(empty, 0.0, t), a_lo, empty


def A_upper(Y2, vL2, K, eta1):
    q = float(chi2.ppf(eta1, K))
    lo, hi = np.zeros(Y2.shape[0]), np.full(Y2.shape[0], 1e4)
    for _ in range(70):
        mid = 0.5 * (lo + hi)
        below = (Y2 / (mid[:, None] + vL2)).sum(1) < q
        hi = np.where(below, mid, hi)
        lo = np.where(below, lo, mid)
    return 0.5 * (lo + hi)


def run(K, d_over_A, nu0, sig_mis):
    rng = seed_for(f"exp22|{K}|{d_over_A}|{nu0}|{sig_mis}")   # same stream as exp22
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

    r2 = seed_for(f"exp22null|{K}|{nu0}")
    c = lxc / (sig_e * np.sqrt(Sxx))
    w = float(np.quantile(np.abs(
        np.log(r2.chisquare(nu_c, size=(NULL_DRAWS, K)) / nu_c) @ c), 1 - ETA_G))

    Y = rng.normal(0.0, np.sqrt(A_TRUE + D), size=(REPS, K))
    absY, Y2 = np.abs(Y), Y ** 2
    Dhat = D * rng.chisquare(nu_c, size=(REPS, K)) / nu_c
    G = rng.normal(0.0, np.sqrt(A_TRUE), size=REPS)

    ghat = -(np.log(Dhat) @ lxc) / Sxx
    half = w * sig_e / np.sqrt(Sxx)
    gL, gU = ghat - half, ghat + half

    band = {"oracle": ord_m(absY / np.sqrt(1.0 + t0 * a_true), m),
            "uncorrected": ord_m(absY, m)}
    vL_b = nu_c * Dhat / chi2.ppf(1.0 - 0.025 / K, nu_c)
    AU_b = A_upper(Y2, vL_b, K, 0.025)
    band["sep_bonf"] = ord_m(
        absY / np.sqrt(1.0 + vL_b / np.maximum(AU_b, 1e-12)[:, None]), m)

    sup_r = np.zeros(REPS); sup_c = np.zeros(REPS)
    for u in np.linspace(0.0, 1.0, GRID):
        g = gL + u * (gU - gL)
        ag = a_of(x, g[:, None])
        dhg = (nu_c * Dhat / ag).sum(1) / nu
        tl, _ = t_lower(Y2, ag, dhg, K, nu, ETA_T)
        sup_r = np.maximum(sup_r, ord_m(absY / np.sqrt(1.0 + tl[:, None] * ag), m))
        dLg = nu * dhg / chi2.ppf(1 - ETA_2, nu)
        vLg = dLg[:, None] * ag
        AUg = A_upper(Y2, vLg, K, ETA_1)
        sup_c = np.maximum(sup_c, ord_m(
            absY / np.sqrt(1.0 + vLg / np.maximum(AUg, 1e-12)[:, None]), m))
    band["Cg_ratio_grid"] = sup_r
    band["Cg_comp"] = sup_c

    t_cert, a_lo, fb = certified_t(Y2, x, nu_c, Dhat, gL, gU, K, nu, ETA_T)
    band["Cg_ratio_cert"] = ord_m(absY / np.sqrt(1.0 + t_cert[:, None] * a_lo), m)

    hit = lambda b: float((np.abs(G) <= b).mean())
    out = dict(K=K, d_over_A=d_over_A, nu_per_pop=nu0, sig_mis=sig_mis,
               reps=REPS, grid=GRID, m=m, nominal=m / (K + 1.0),
               Cg_set_cov=float(((gL <= GAMMA0) & (GAMMA0 <= gU)).mean()),
               fallback_rate=float(fb.mean()),
               cert_ge_grid=float((band["Cg_ratio_cert"] >= sup_r).mean()),
               cert_over_grid=float(np.mean(band["Cg_ratio_cert"] / sup_r)),
               mc_se=float(np.sqrt(.95 * .05 / REPS)))
    for nm, b in band.items():
        out[f"{nm}_cov"] = hit(b)
        out[f"{nm}_w"] = float(b.mean())
        if nm != "oracle":
            out[f"{nm}_contain"] = float((b >= band["oracle"]).mean())
            out[f"{nm}_over_oracle"] = float(np.mean(b / band["oracle"]))
    av = out["uncorrected_over_oracle"] - 1.0
    for nm in ("sep_bonf", "Cg_comp", "Cg_ratio_grid", "Cg_ratio_cert"):
        out[f"captured_{nm}"] = float((av - (out[f"{nm}_over_oracle"] - 1)) / av)
    out["cert_over_comp"] = float(np.mean(band["Cg_ratio_cert"] / sup_c))
    out["cert_over_sepbonf"] = float(np.mean(band["Cg_ratio_cert"] / band["sep_bonf"]))
    return out


def main():
    rows = [run(K, da, nu0, sm) for K in (60, 200) for da in (0.5, 1.0)
            for nu0 in (8, 16) for sm in (0.0, 0.4)]
    df = pd.DataFrame(rows)
    out = ROOT / "results" / "exp23_certified.csv"
    df.to_csv(out, index=False)
    ok, mis = df[df.sig_mis == 0], df[df.sig_mis > 0]
    (ROOT / "results" / "exp23_manifest.json").write_text(json.dumps(dict(
        experiment="exp23_certified", reps=REPS, cells=len(df),
        alpha0=ALPHA0, eta_gamma=ETA_G, eta_t=ETA_T,
        c1_cert_ge_grid=[float(df.cert_ge_grid.min()), float(df.cert_ge_grid.max())],
        c2_cert_over_grid=[float(df.cert_over_grid.min()),
                           float(df.cert_over_grid.max())],
        c3_contain_ok=[float(ok.Cg_ratio_cert_contain.min()),
                       float(ok.Cg_ratio_cert_contain.max())],
        c3_cov_ok=[float(ok.Cg_ratio_cert_cov.min()),
                   float(ok.Cg_ratio_cert_cov.max())],
        c4_captured=[float(ok.captured_Cg_ratio_cert.min()),
                     float(ok.captured_Cg_ratio_cert.max()),
                     float(ok.captured_sep_bonf.min()),
                     float(ok.captured_sep_bonf.max())],
        fallback=[float(df.fallback_rate.min()), float(df.fallback_rate.max())],
    ), indent=2) + "\n")

    pd.set_option("display.width", 250, "display.max_columns", 70)
    lab = ["K", "d_over_A", "nu_per_pop"]
    for tag, sub in (("CORRECTLY SPECIFIED", ok), ("MISSPECIFIED", mis)):
        print(f"\n########## {tag}")
        print("C1/C2: certified vs the retracted grid computation")
        print(sub.set_index(lab)[["cert_ge_grid", "cert_over_grid",
                                  "fallback_rate"]].round(4).to_string())
        print("\nthe three probabilities, side by side")
        print(sub.set_index(lab)[["Cg_set_cov", "Cg_ratio_cert_contain",
                                  "Cg_comp_contain", "sep_bonf_contain",
                                  "Cg_ratio_cert_cov", "Cg_comp_cov",
                                  "oracle_cov"]].round(4).to_string())
        print("\nwidth, paired")
        print(sub.set_index(lab)[["cert_over_comp", "cert_over_sepbonf",
                                  "Cg_ratio_cert_over_oracle", "Cg_comp_over_oracle",
                                  "sep_bonf_over_oracle", "captured_Cg_ratio_cert",
                                  "captured_Cg_comp", "captured_sep_bonf"]]
              .round(4).to_string())
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
