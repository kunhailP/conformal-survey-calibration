"""exp14 - one procedure, from point estimate to band, with the guarantee named.

Protocol: docs/PROTOCOL_exp14_chain.md (written before execution).
Predecessors: exp12, exp13.

exp13 claimed a band whose containment is guaranteed by construction.  It did
not have one: the simultaneous lower limits were near-exact but the scale upper
limit was a normal approximation covering at 0.963-0.969 against 0.975.  This
experiment builds a scale limit that is valid by argument, and then follows one
procedure through all four links the review asks for -- point estimate, scale
limit, containment of the oracle band, latent-target coverage and width.

The valid limit uses a pivot rather than the point estimator, so whether the
weighting improvement of exp13 reaches the band is a question, not a corollary.

No microdata required.

    python experiments/exp14_chain.py
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

REPS = 20000
BOOT_REPS, B_BOOT = 1000, 200
NU = 10.0
A_TRUE = 1.0
ALPHA0 = ETA = 0.05
ETA1 = ETA2 = ETA / 2


def seed_for(label):
    return np.random.default_rng(
        int.from_bytes(hashlib.sha256(label.encode()).digest()[:8], "little"))


def make_D(rng, K, dbar, sigma_e, heavy=False):
    n = rng.lognormal(0.0, 1.8 if heavy else 0.8, size=K)
    e = rng.lognormal(0.0, sigma_e, size=K) if sigma_e > 0 else np.ones(K)
    D = e / n
    return D * A_TRUE * dbar / D.mean(), n


def opt_w(A, D, nu):
    return 1.0 / ((A + D) ** 2 + D ** 2 / nu)


def gvf_all(Dhat, n):
    """Ratio-form GVF fitted on every population, own estimate included."""
    return np.maximum((Dhat * n).mean(axis=-1, keepdims=True) / n, 1e-9)


def chi2_pivot_AU(Y2, vL2, q):
    """Root of sum_c Y_c^2 / (A + vL_c^2) = q, by vectorised bisection."""
    lo = np.zeros(Y2.shape[0])
    hi = np.full(Y2.shape[0], 1e4)
    f = lambda A: (Y2 / (A[:, None] + vL2)).sum(1) - q
    lo = np.where(f(lo) < 0, 0.0, lo)                # already below: A_U = 0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        hi = np.where(f(mid) < 0, mid, hi)
        lo = np.where(f(mid) < 0, lo, mid)
    return 0.5 * (lo + hi)


def gw_upper(S1, n1, S2, n2, eta):
    H1 = n1 / chi2.ppf(eta, n1) - 1.0
    G2 = 1.0 - n2 / chi2.ppf(1.0 - eta, n2)
    return S1 - S2 + np.sqrt((H1 * S1) ** 2 + (G2 * S2) ** 2)


def run(K, dbar, sigma_e, heavy=False, reps=REPS, with_boot=False):
    label = f"exp14|{K}|{dbar}|{sigma_e}|{heavy}"
    rng = seed_for(label)
    D, n = make_D(rng, K, dbar, sigma_e, heavy)
    nu = np.full(K, NU)
    sig2 = A_TRUE + D

    Y = rng.normal(0.0, np.sqrt(sig2), size=(reps, K))
    Y2 = Y ** 2
    Dhat = D * rng.chisquare(nu, size=(reps, K)) / nu
    Z = Y2 - Dhat

    A_unw = Z.mean(axis=1)
    Dsm = gvf_all(Dhat, n)
    A0 = np.maximum(A_unw, 1e-9)[:, None]
    w = opt_w(A0, Dsm, nu)
    A_gvf = (Z * w).sum(1) / w.sum(1)

    # --- scale upper limits, five arms ---------------------------------
    vL2 = nu * Dhat / chi2.ppf(1.0 - ETA2 / K, nu)          # simultaneous, eta2
    q = float(chi2.ppf(ETA1, K))
    lim = {"chi2_pivot": chi2_pivot_AU(Y2, vL2, q)}

    se_unw = np.sqrt((2 * (A0 + Dhat) ** 2 + 2 * Dhat ** 2 / nu).sum(1)) / K
    lim["normal_unw"] = A_unw + norm.ppf(1 - ETA1) * se_unw
    Ag = np.maximum(A_gvf, 1e-9)[:, None]
    vz = 2 * (Ag + Dsm) ** 2 + 2 * Dsm ** 2 / nu
    se_gvf = np.sqrt((w ** 2 * vz).sum(1)) / w.sum(1)
    lim["normal_gvf"] = A_gvf + norm.ppf(1 - ETA1) * se_gvf

    SY2 = Y2.mean(axis=1)                                    # mu known, so no -1
    Dbar_hat = Dhat.mean(axis=1)
    nu_n = K ** 2 * Dbar_hat ** 2 / (Dhat ** 2 / nu).sum(axis=1)
    lim["gw"] = gw_upper(SY2, float(K), Dbar_hat, nu_n, ETA1)

    if with_boot:
        idx0 = np.arange(min(reps, BOOT_REPS))
        bu = np.empty(len(idx0))
        for b in idx0:
            j = rng.integers(0, K, size=(B_BOOT, K))
            Zb, Dhb, nb = Z[b][j], Dhat[b][j], n[j]
            Dsb = gvf_all(Dhb, nb)
            A0b = np.maximum(Zb.mean(1), 1e-9)[:, None]
            wb = opt_w(A0b, Dsb, NU)
            Ab = (Zb * wb).sum(1) / wb.sum(1)
            bu[b] = 2 * A_gvf[b] - np.quantile(Ab, ETA1)     # basic upper
        lim["boot_gvf"] = np.r_[bu, np.full(reps - len(idx0), np.nan)]

    # --- band, from each limit ------------------------------------------
    m = conformal_rank(K, ALPHA0)
    absY = np.abs(Y)
    band_or = np.sort(absY / np.sqrt(1.0 + D / A_TRUE), axis=1)[:, m - 1]
    G = rng.normal(0.0, np.sqrt(A_TRUE), size=reps)
    ED = (vL2 <= D).all(axis=1)

    out = dict(K=K, Dbar_over_A=dbar, sigma_e=sigma_e, heavy=heavy, reps=reps,
               nu=NU, cv_D=float(D.std() / D.mean()),
               max_leverage=float(n.max() / np.median(n)),
               nominal=m / (K + 1.0), eta1=ETA1, eta2=ETA2,
               unw_bias=float(A_unw.mean() - A_TRUE),
               unw_rmse=float(np.sqrt(np.mean((A_unw - A_TRUE) ** 2))),
               gvf_bias=float(A_gvf.mean() - A_TRUE),
               gvf_rmse=float(np.sqrt(np.mean((A_gvf - A_TRUE) ** 2))),
               ED_prob=float(ED.mean()),
               cov_oracle=float((np.abs(G) <= band_or).mean()),
               mc_se=float(np.sqrt(0.95 * 0.05 / reps)))
    for name, AU in lim.items():
        ok = np.isfinite(AU)
        AUp = np.maximum(AU, 1e-9)
        band = np.sort(absY / np.sqrt(1.0 + vL2 / AUp[:, None]), axis=1)[:, m - 1]
        out[f"{name}_AU_cov"] = float((AU[ok] >= A_TRUE).mean())
        out[f"{name}_contain"] = float((band[ok] >= band_or[ok]).mean())
        out[f"{name}_cov"] = float((np.abs(G[ok]) <= band[ok]).mean())
        out[f"{name}_width"] = float(band[ok].mean())
        out[f"{name}_over_oracle"] = float((band[ok] / band_or[ok]).mean())
    return out


def main():
    rows = [run(K, db, se)
            for K in (60, 200) for db in (1.0, 4.0) for se in (0.0, 0.6)]
    boot = [run(K, 4.0, 0.3, reps=BOOT_REPS, with_boot=True) for K in (60, 200)]
    rate = [run(K, 4.0, 0.3) for K in (60, 120, 240, 480)]
    stress = [run(200, 4.0, 0.3, heavy=h) for h in (False, True)]

    df = pd.DataFrame(rows)
    dfb, dfr, dfs = pd.DataFrame(boot), pd.DataFrame(rate), pd.DataFrame(stress)
    for d, nm in ((df, "main"), (dfb, "boot"), (dfr, "rate"), (dfs, "stress")):
        d.insert(0, "block", nm)
    all_df = pd.concat([df, dfb, dfr, dfs], ignore_index=True)
    out = ROOT / "results" / "exp14_chain.csv"
    all_df.to_csv(out, index=False)

    slope = np.polyfit(np.log(dfr.K), np.log(np.abs(dfr.gvf_bias)), 1)[0]
    (ROOT / "results" / "exp14_manifest.json").write_text(json.dumps(dict(
        experiment="exp14_chain", reps=REPS, boot_reps=BOOT_REPS, B=B_BOOT,
        nu=NU, alpha0=ALPHA0, eta1=ETA1, eta2=ETA2,
        u1_chi2_AU_cov_min=float(df.chi2_pivot_AU_cov.min()),
        u2_normal_unw_AU_cov_min=float(df.normal_unw_AU_cov.min()),
        u3_normal_gvf_AU_cov_min=float(df.normal_gvf_AU_cov.min()),
        u4_chi2_contain_min=float(df.chi2_pivot_contain.min()),
        u5_bias_slope_in_logK=float(slope),
        u6_bias_heavy_vs_normal=[float(dfs.gvf_bias.iloc[0]),
                                 float(dfs.gvf_bias.iloc[1])],
    ), indent=2) + "\n")

    pd.set_option("display.width", 240, "display.max_columns", 80)
    lab = ["K", "Dbar_over_A", "sigma_e"]
    arms = ["chi2_pivot", "normal_unw", "normal_gvf", "gw"]
    print("=== U1-U3: coverage of the scale upper limit, nominal 0.975 (MC SE ~0.001)")
    print(df.set_index(lab)[[f"{a}_AU_cov" for a in arms]].round(4).to_string())
    print("\n=== U4: containment of the oracle half-width, requirement 0.95")
    print(df.set_index(lab)[["ED_prob"] + [f"{a}_contain" for a in arms]]
          .round(4).to_string())
    print("\n=== latent-target coverage (guaranteed 0.90) and width over the oracle band")
    print(df.set_index(lab)[["cov_oracle"] + [f"{a}_cov" for a in arms]
                            + [f"{a}_over_oracle" for a in arms]].round(4).to_string())
    print("\n=== the point estimators feeding them")
    print(df.set_index(lab)[["unw_bias", "unw_rmse", "gvf_bias", "gvf_rmse"]]
          .round(4).to_string())
    print("\n=== bootstrap arm (1,000 reps, B=200, full procedure refitted)")
    print(dfb.set_index(lab)[["boot_gvf_AU_cov", "boot_gvf_contain",
                              "boot_gvf_cov", "boot_gvf_over_oracle",
                              "chi2_pivot_AU_cov", "chi2_pivot_over_oracle"]]
          .round(4).to_string())
    print("\n=== U5: is the GVF bias O(1/K)?")
    print(dfr.set_index("K")[["gvf_bias", "unw_bias", "gvf_rmse"]].round(5).to_string())
    print(f"    slope of log|bias| on log K = {slope:.3f}  (-1 supports O(1/K))")
    print("\n=== U6: leverage stress")
    print(dfs.set_index("heavy")[["max_leverage", "cv_D", "gvf_bias", "gvf_rmse",
                                  "unw_rmse"]].round(4).to_string())
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
