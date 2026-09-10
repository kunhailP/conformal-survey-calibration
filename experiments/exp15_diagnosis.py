"""exp15 - why the GVF upper limit undercovers, and the K-p extension.

Protocol: docs/PROTOCOL_exp15_diagnosis.md (written before execution).
Predecessor: exp14.

exp14 explained the GVF-based upper limit's undercoverage by "positive bias and
smaller variance".  For a ONE-SIDED upper limit that is backwards: failure is a
left-tail event and a positive bias raises coverage.  The cause was therefore
unidentified.  This is a diagnosis on the failing cells, not a new sweep.

    python experiments/exp15_diagnosis.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2, norm, kstest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from dac.bands import conformal_rank                        # noqa: E402

REPS, SUB_REPS, B_BOOT = 20000, 2000, 2000
NU, A_TRUE = 10.0, 1.0
ALPHA0 = ETA = 0.05
ETA1 = ETA2 = ETA / 2
Z1 = float(norm.ppf(1 - ETA1))


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


def varZ(A, D, nu):
    return 2 * (A + D) ** 2 + 2 * D ** 2 / nu


# ---------------------------------------------------------------- block 1

def block1(K, dbar, sigma_e):
    rng = seed_for(f"exp15b1|{K}|{dbar}|{sigma_e}")
    D, n = make_D(rng, K, dbar, sigma_e)
    nu = np.full(K, NU)
    Y = rng.normal(0.0, np.sqrt(A_TRUE + D), size=(REPS, K))
    Dhat = D * rng.chisquare(nu, size=(REPS, K)) / nu
    Z = Y ** 2 - Dhat

    Dsm = gvf(Dhat, n)
    A0 = np.maximum(Z.mean(1), 1e-9)[:, None]
    w = opt_w(A0, Dsm, nu)
    Ahat = (Z * w).sum(1) / w.sum(1)
    Ag = np.maximum(Ahat, 1e-9)[:, None]

    se = {}
    se["se_Dsm"] = np.sqrt((w ** 2 * varZ(Ag, Dsm, nu)).sum(1)) / w.sum(1)
    se["se_Dhat"] = np.sqrt((w ** 2 * varZ(Ag, Dhat, nu)).sum(1)) / w.sum(1)
    se["se_Dtrue"] = np.sqrt((w ** 2 * varZ(A_TRUE, D, nu)).sum(1)) / w.sum(1)

    # delete-one-population jackknife over the WHOLE procedure
    sub = slice(0, SUB_REPS)
    Zs, Dhs = Z[sub], Dhat[sub]
    cn = (Dhs * n).sum(1, keepdims=True)
    jk = np.empty((SUB_REPS, K))
    for j in range(K):
        keep = np.ones(K, bool); keep[j] = False
        c_j = (cn - (Dhs[:, [j]] * n[j])) / (K - 1)
        Dsm_j = np.maximum(c_j / n[keep], 1e-9)
        A0_j = np.maximum(Zs[:, keep].mean(1), 1e-9)[:, None]
        w_j = opt_w(A0_j, Dsm_j, nu[keep])
        jk[:, j] = (Zs[:, keep] * w_j).sum(1) / w_j.sum(1)
    se_jk = np.sqrt((K - 1) / K * ((jk - jk.mean(1, keepdims=True)) ** 2).sum(1))

    out = dict(K=K, Dbar_over_A=dbar, sigma_e=sigma_e, reps=REPS,
               bias=float(Ahat.mean() - A_TRUE), sd_realised=float(Ahat.std(ddof=1)))
    for name, s in se.items():
        t = (Ahat - A_TRUE) / s
        out[f"{name}_ratio"] = float(s.mean() / Ahat.std(ddof=1))
        out[f"{name}_cov"] = float((Ahat + Z1 * s >= A_TRUE).mean())
        out[f"{name}_t_mean"] = float(t.mean())
        out[f"{name}_t_sd"] = float(t.std(ddof=1))
        out[f"{name}_t_q025"] = float(np.quantile(t, ETA1))
    t_jk = (Ahat[sub] - A_TRUE) / se_jk
    out.update(se_jk_ratio=float(se_jk.mean() / Ahat[sub].std(ddof=1)),
               se_jk_cov=float((Ahat[sub] + Z1 * se_jk >= A_TRUE).mean()),
               se_jk_t_q025=float(np.quantile(t_jk, ETA1)),
               jk_reps=SUB_REPS, z_ref=-Z1,
               ks_normal_p=float(kstest(
                   ((Ahat - Ahat.mean()) / Ahat.std(ddof=1))[:5000], "norm").pvalue))

    # bootstrap forms, on the sub-block only
    rng2 = seed_for(f"exp15boot|{K}|{dbar}|{sigma_e}")
    nb = min(SUB_REPS, 400)
    bas = np.empty(nb); pct = np.empty(nb); stu = np.empty(nb)
    for b in range(nb):
        j = rng2.integers(0, K, size=(B_BOOT, K))
        Zb, Dhb, nbn = Z[b][j], Dhat[b][j], n[j]
        Dsb = gvf(Dhb, nbn)
        A0b = np.maximum(Zb.mean(1), 1e-9)[:, None]
        wb = opt_w(A0b, Dsb, NU)
        Ab = (Zb * wb).sum(1) / wb.sum(1)
        seb = np.sqrt((wb ** 2 * varZ(np.maximum(Ab, 1e-9)[:, None], Dsb, NU)
                       ).sum(1)) / wb.sum(1)
        bas[b] = 2 * Ahat[b] - np.quantile(Ab, ETA1)
        pct[b] = np.quantile(Ab, 1 - ETA1)
        tb = (Ab - Ahat[b]) / np.maximum(seb, 1e-12)
        stu[b] = Ahat[b] - np.quantile(tb, ETA1) * se["se_Dsm"][b]
    # the pivot limit on the same replicates, for a width comparison
    vL2 = nu * Dhat[:nb] / chi2.ppf(1.0 - ETA2 / K, nu)
    qp = float(chi2.ppf(ETA1, K))
    lo, hi = np.zeros(nb), np.full(nb, 1e4)
    Y2 = Y[:nb] ** 2
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        below = (Y2 / (mid[:, None] + vL2)).sum(1) < qp
        hi = np.where(below, mid, hi); lo = np.where(below, lo, mid)
    AU_piv = 0.5 * (lo + hi)
    out.update(boot_reps=nb, B=B_BOOT, boot_mc_se=float(np.sqrt(.975*.025/nb)),
               boot_basic_cov=float((bas >= A_TRUE).mean()),
               boot_pct_cov=float((pct >= A_TRUE).mean()),
               boot_stud_cov=float((stu >= A_TRUE).mean()),
               AU_pivot_mean=float(AU_piv.mean()),
               AU_boot_pct_mean=float(pct.mean()),
               AU_boot_stud_mean=float(stu.mean()),
               AU_normal_Dhat_mean=float((Ahat[:nb] + Z1 * se["se_Dhat"][:nb]).mean()),
               pct_over_pivot=float((pct / AU_piv).mean()),
               pivot_cov_here=float((AU_piv >= A_TRUE).mean()))
    return out


# ---------------------------------------------------------------- block 2

def Q_min(a, Y, X, Dv):
    """min_beta sum (Y - X beta)^2 / (a + D), by weighted least squares."""
    wgt = 1.0 / (a[:, None] + Dv)
    XtWX = np.einsum('rk,kp,kq->rpq', wgt, X, X)
    XtWY = np.einsum('rk,rk,kp->rp', wgt, Y, X)
    beta = np.linalg.solve(XtWX, XtWY[..., None])[..., 0]
    r = Y - beta @ X.T
    return (wgt * r ** 2).sum(1)


def block2(K, p):
    rng = seed_for(f"exp15b2|{K}|{p}")
    D, n = make_D(rng, K, 4.0, 0.3)
    nu = np.full(K, NU)
    X = np.column_stack([np.ones(K)] + [rng.normal(size=K) for _ in range(p - 1)])
    beta0 = np.arange(1.0, p + 1.0)
    Y = X @ beta0 + rng.normal(0.0, np.sqrt(A_TRUE + D), size=(REPS, K))
    Dhat = D * rng.chisquare(nu, size=(REPS, K)) / nu
    vL2 = nu * Dhat / chi2.ppf(1.0 - ETA2 / K, nu)

    Qtrue = Q_min(np.full(REPS, A_TRUE), Y, X, np.broadcast_to(D, (REPS, K)))
    q = float(chi2.ppf(ETA1, K - p))
    lo, hi = np.zeros(REPS), np.full(REPS, 1e4)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        below = Q_min(mid, Y, X, vL2) < q
        hi = np.where(below, mid, hi)
        lo = np.where(below, lo, mid)
    AU = 0.5 * (lo + hi)
    return dict(K=K, p=p, reps=REPS, df_nominal=K - p,
                Q_mean=float(Qtrue.mean()), Q_var=float(Qtrue.var(ddof=1)),
                Q_mean_expected=float(K - p), Q_var_expected=float(2 * (K - p)),
                ks_p=float(kstest(Qtrue[:5000], "chi2", args=(K - p,)).pvalue),
                AU_cov=float((AU >= A_TRUE).mean()),
                AU_mean=float(AU.mean()),
                guarantee=1 - ETA1 - ETA2)


# ---------------------------------------------------------------- block 3

def block3(K, dbar, sigma_e):
    rng = seed_for(f"exp15b3|{K}|{dbar}|{sigma_e}")
    D, n = make_D(rng, K, dbar, sigma_e)
    nu = np.full(K, NU)
    Y = rng.normal(0.0, np.sqrt(A_TRUE + D), size=(REPS, K))
    Dhat = D * rng.chisquare(nu, size=(REPS, K)) / nu
    vL2 = nu * Dhat / chi2.ppf(1.0 - ETA2 / K, nu)
    q = float(chi2.ppf(ETA1, K))
    lo, hi = np.zeros(REPS), np.full(REPS, 1e4)
    Y2 = Y ** 2
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        below = (Y2 / (mid[:, None] + vL2)).sum(1) < q
        hi = np.where(below, mid, hi)
        lo = np.where(below, lo, mid)
    AU = np.maximum(0.5 * (lo + hi), 1e-9)

    m = conformal_rank(K, ALPHA0)
    band_or = np.sort(np.abs(Y) / np.sqrt(1.0 + D / A_TRUE), axis=1)[:, m - 1]
    band_cf = np.sort(np.abs(Y) / np.sqrt(1.0 + vL2 / AU[:, None]), axis=1)[:, m - 1]
    band_nm = norm.ppf(1 - ALPHA0 / 2) * np.sqrt(AU)      # same A_U, same budget
    G = rng.normal(0.0, np.sqrt(A_TRUE), size=REPS)
    return dict(K=K, Dbar_over_A=dbar, sigma_e=sigma_e, reps=REPS,
                cov_oracle=float((np.abs(G) <= band_or).mean()),
                cov_conformal=float((np.abs(G) <= band_cf).mean()),
                cov_normal_model=float((np.abs(G) <= band_nm).mean()),
                w_conformal=float(band_cf.mean()), w_normal=float(band_nm.mean()),
                normal_over_conformal=float((band_nm / band_cf).mean()),
                guarantee=1 - ALPHA0 - ETA)


def main():
    b1 = pd.DataFrame([block1(K, 4.0, se) for K in (60, 200) for se in (0.0, 0.6)])
    b2 = pd.DataFrame([block2(K, p) for K in (60, 200) for p in (1, 3)])
    b3 = pd.DataFrame([block3(K, 4.0, se) for K in (60, 200) for se in (0.0, 0.6)])
    for d, nm in ((b1, "diagnosis"), (b2, "unknown_mean"), (b3, "normal_compare")):
        d.insert(0, "block", nm)
        d.to_csv(ROOT / "results" / f"exp15_{nm}.csv", index=False)
    (ROOT / "results" / "exp15_manifest.json").write_text(json.dumps(dict(
        experiment="exp15_diagnosis", reps=REPS, sub_reps=SUB_REPS, B=B_BOOT,
        eta1=ETA1, eta2=ETA2, alpha0=ALPHA0, nu=NU,
        v1_se_ratio_range=[float(b1.se_Dsm_ratio.min()), float(b1.se_Dsm_ratio.max())],
        v5_ks_p_min=float(b2.ks_p.min()),
        v5_AU_cov_min=float(b2.AU_cov.min()),
    ), indent=2) + "\n")

    pd.set_option("display.width", 240, "display.max_columns", 60)
    lab = ["K", "sigma_e"]
    print("=== V1/V2: is the standard error understated, and at which argument?")
    print("    ratio = mean(se) / realised SD;  cov = one-sided upper, nominal 0.975")
    print(b1.set_index(lab)[["bias", "sd_realised",
                             "se_Dsm_ratio", "se_Dhat_ratio", "se_Dtrue_ratio",
                             "se_Dsm_cov", "se_Dhat_cov", "se_Dtrue_cov"]]
          .round(4).to_string())
    print("\n=== V1: left tail of the standardised error against -1.96")
    print(b1.set_index(lab)[["se_Dsm_t_mean", "se_Dsm_t_sd", "se_Dsm_t_q025",
                             "se_Dtrue_t_q025", "se_jk_t_q025", "z_ref",
                             "ks_normal_p"]].round(4).to_string())
    print("\n=== V3/V4: jackknife over the whole procedure, and bootstrap forms")
    print(b1.set_index(lab)[["se_jk_ratio", "se_jk_cov", "boot_mc_se",
                             "boot_basic_cov", "boot_pct_cov", "boot_stud_cov",
                             "pivot_cov_here"]].round(4).to_string())
    print("\n=== width of the scale limit itself, same replicates")
    print(b1.set_index(lab)[["AU_pivot_mean", "AU_boot_pct_mean",
                             "AU_boot_stud_mean", "AU_normal_Dhat_mean",
                             "pct_over_pivot"]].round(4).to_string())
    print("\n=== V5: unknown mean, Q ~ chi2_{K-p}?  (guarantee 0.95)")
    print(b2.set_index(["K", "p"])[["df_nominal", "Q_mean", "Q_mean_expected",
                                    "Q_var", "Q_var_expected", "ks_p", "AU_cov"]]
          .round(4).to_string())
    print("\n=== Block 3: normal-model T2 interval on the same A_U and budget")
    print(b3.set_index(lab)[["cov_oracle", "cov_conformal", "cov_normal_model",
                             "w_conformal", "w_normal", "normal_over_conformal"]]
          .round(4).to_string())


if __name__ == "__main__":
    main()
