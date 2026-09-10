"""exp22 - completing route (b): the algorithm, and the matched comparison.

Protocol: docs/PROTOCOL_exp22_completion.md (written before execution).
Predecessor: exp21.  Route (a), general profiling, is NOT opened.

Job 1: replace the grid supremum by a certified envelope.  log a_c(gamma) is
concave in gamma, so inf over an interval is at an endpoint EXACTLY; combined
with monotonicity of R in each t a_c this bounds the supremum from above.  The
remaining gap is inf t_L(gamma), which is measured rather than assumed.

Job 2: compare against a component-wise bound that ALSO estimates the structure,
so both sides pay for it.

    python experiments/exp22_completion.py
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
ETA_G = 0.025                     # structure step, both arms
ETA_T = ETA - ETA_G               # ratio arm
ETA_1 = ETA_2 = (ETA - ETA_G) / 2  # component arm needs one more piece


def seed_for(label):
    return np.random.default_rng(
        int.from_bytes(hashlib.sha256(label.encode()).digest()[:8], "little"))


def a_of(x, g):
    v = x ** (-g)
    return v / v.mean(axis=-1, keepdims=True)


def ord_m(z, m):
    return np.sort(z, axis=1)[:, m - 1]


def t_lower(Y2, a, dhat, K, nu, eta):
    q = float(fdist.ppf(1.0 - eta, nu, K))
    T = lambda t: K * dhat / np.maximum(
        t * (Y2 / (1.0 + t[:, None] * a)).sum(1), 1e-300)
    empty = (K * dhat / np.maximum((Y2 / a).sum(1), 1e-300)) > q
    lo, hi = np.full(Y2.shape[0], 1e-8), np.full(Y2.shape[0], 1e8)
    for _ in range(70):
        mid = np.sqrt(lo * hi)
        below = T(mid) <= q
        hi = np.where(below, mid, hi)
        lo = np.where(below, lo, mid)
    return np.where(empty, 0.0, np.sqrt(lo * hi))


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
    rng = seed_for(f"exp22|{K}|{d_over_A}|{nu0}|{sig_mis}")
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
    logD = np.log(Dhat)

    ghat = -(logD @ lxc) / Sxx
    half = w * sig_e / np.sqrt(Sxx)
    gL, gU = ghat - half, ghat + half

    band = {"oracle": ord_m(absY / np.sqrt(1.0 + t0 * a_true), m),
            "uncorrected": ord_m(absY, m)}
    vL_b = nu_c * Dhat / chi2.ppf(1.0 - 0.025 / K, nu_c)
    AU_b = A_upper(Y2, vL_b, K, 0.025)
    band["sep_bonf"] = ord_m(absY / np.sqrt(1.0 + vL_b
                                            / np.maximum(AU_b, 1e-12)[:, None]), m)

    us = np.linspace(0.0, 1.0, GRID)
    sup_r = np.zeros(REPS); sup_c = np.zeros(REPS)
    tL_all = np.empty((GRID, REPS))
    for i, u in enumerate(us):
        g = gL + u * (gU - gL)
        ag = a_of(x, g[:, None])
        dh = (nu_c * Dhat / ag).sum(1) / nu
        tl = t_lower(Y2, ag, dh, K, nu, ETA_T)
        tL_all[i] = tl
        sup_r = np.maximum(sup_r, ord_m(absY / np.sqrt(1.0 + tl[:, None] * ag), m))
        dLg = nu * ((nu_c * Dhat / ag).sum(1) / nu) / chi2.ppf(1 - ETA_2, nu)
        vLg = dLg[:, None] * ag
        AUg = A_upper(Y2, vLg, K, ETA_1)
        sup_c = np.maximum(sup_c, ord_m(
            absY / np.sqrt(1.0 + vLg / np.maximum(AUg, 1e-12)[:, None]), m))
    band["Cg_ratio"] = sup_r
    band["Cg_comp"] = sup_c

    # certified envelope: endpoint minimum of a_c (exact) and grid minimum of t_L
    a_lo = np.minimum(a_of(x, gL[:, None]), a_of(x, gU[:, None]))
    t_lo = tL_all.min(axis=0)
    argmin_i = tL_all.argmin(axis=0)
    band["Cg_ratio_env"] = ord_m(absY / np.sqrt(1.0 + t_lo[:, None] * a_lo), m)

    hit = lambda b: float((np.abs(G) <= b).mean())
    out = dict(K=K, d_over_A=d_over_A, nu_per_pop=nu0, sig_mis=sig_mis,
               reps=REPS, grid=GRID, m=m, nominal=m / (K + 1.0), w_crit=w,
               Cg_set_cov=float(((gL <= GAMMA0) & (GAMMA0 <= gU)).mean()),
               Cg_halfwidth=float(half),
               tL_argmin_at_endpoint=float(
                   ((argmin_i == 0) | (argmin_i == GRID - 1)).mean()),
               env_ge_grid=float((band["Cg_ratio_env"] >= sup_r).mean()),
               mc_se=float(np.sqrt(.95 * .05 / REPS)))
    for nm, b in band.items():
        out[f"{nm}_cov"] = hit(b)
        out[f"{nm}_w"] = float(b.mean())
        if nm != "oracle":
            out[f"{nm}_contain"] = float((b >= band["oracle"]).mean())
            out[f"{nm}_over_oracle"] = float(np.mean(b / band["oracle"]))
    av = out["uncorrected_over_oracle"] - 1.0
    for nm in ("sep_bonf", "Cg_ratio", "Cg_ratio_env", "Cg_comp"):
        out[f"captured_{nm}"] = float((av - (out[f"{nm}_over_oracle"] - 1)) / av)
    out["env_over_grid"] = float(np.mean(band["Cg_ratio_env"] / sup_r))
    out["ratio_over_comp"] = float(np.mean(sup_r / sup_c))
    out["env_over_comp"] = float(np.mean(band["Cg_ratio_env"] / sup_c))
    return out


def main():
    rows = [run(K, da, nu0, sm) for K in (60, 200) for da in (0.5, 1.0)
            for nu0 in (8, 16) for sm in (0.0, 0.4)]
    df = pd.DataFrame(rows)
    out = ROOT / "results" / "exp22_completion.csv"
    df.to_csv(out, index=False)
    ok, mis = df[df.sig_mis == 0], df[df.sig_mis > 0]
    (ROOT / "results" / "exp22_manifest.json").write_text(json.dumps(dict(
        experiment="exp22_completion", reps=REPS, grid=GRID, cells=len(df),
        alpha0=ALPHA0, eta_gamma=ETA_G, eta_t=ETA_T, eta1=ETA_1, eta2=ETA_2,
        p1_tL_endpoint=[float(df.tL_argmin_at_endpoint.min()),
                        float(df.tL_argmin_at_endpoint.max())],
        p2_env_over_grid=[float(df.env_over_grid.min()),
                          float(df.env_over_grid.max())],
        p3_ratio_over_comp=[float(df.ratio_over_comp.min()),
                            float(df.ratio_over_comp.max())],
        p4_contain_ok=[float(ok.Cg_ratio_env_contain.min()),
                       float(ok.Cg_comp_contain.min())],
        p4_contain_mis=[float(mis.Cg_ratio_env_contain.min()),
                        float(mis.Cg_comp_contain.min())],
        set_cov_ok=[float(ok.Cg_set_cov.min()), float(ok.Cg_set_cov.max())],
    ), indent=2) + "\n")

    pd.set_option("display.width", 250, "display.max_columns", 70)
    lab = ["K", "d_over_A", "nu_per_pop"]
    for tag, sub in (("CORRECTLY SPECIFIED", ok), ("MISSPECIFIED", mis)):
        print(f"\n########## {tag}")
        print("Job 1: is the envelope justified, and what does it cost?")
        print(sub.set_index(lab)[["tL_argmin_at_endpoint", "env_ge_grid",
                                  "env_over_grid", "Cg_halfwidth"]]
              .round(4).to_string())
        print("\nthe three probabilities, side by side")
        print(sub.set_index(lab)[["Cg_set_cov", "Cg_ratio_env_contain",
                                  "Cg_comp_contain", "sep_bonf_contain",
                                  "Cg_ratio_env_cov", "Cg_comp_cov",
                                  "oracle_cov"]].round(4).to_string())
        print("\nJob 2: matched comparison, paired width ratios")
        print(sub.set_index(lab)[["ratio_over_comp", "env_over_comp",
                                  "Cg_ratio_over_oracle", "Cg_ratio_env_over_oracle",
                                  "Cg_comp_over_oracle", "sep_bonf_over_oracle",
                                  "captured_Cg_ratio_env", "captured_Cg_comp",
                                  "captured_sep_bonf"]].round(4).to_string())
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
