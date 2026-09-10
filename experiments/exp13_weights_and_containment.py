"""exp13 - what a feasible weighting recovers, and a band that is guaranteed.

Protocol: docs/PROTOCOL_exp13_weights_and_containment.md (written before execution).
Predecessors: exp09, exp12.

Two questions, deliberately not merged.

Part A  With D_i estimated, does a *feasible* weighting improve the MSE of A-hat
        at the same data budget?  Weights independent of the residual are one
        candidate among several, not the answer assumed in advance.
Part B  Does a band whose containment of the oracle band is guaranteed by
        construction actually contain it, and what does the guarantee cost?

An improvement in Part A is not evidence for Part B.

No microdata required.

    python experiments/exp13_weights_and_containment.py
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
K_GRID = (60, 200)
DBAR_GRID = (1.0, 4.0)
SIGMA_E_GRID = (0.0, 0.3, 0.6)
NU = 10.0
SIGMA_LOG_N = 0.8
A_TRUE = 1.0
ALPHA0 = ETA = 0.05
ETA1 = ETA2 = ETA / 2


def seed_for(label):
    return np.random.default_rng(
        int.from_bytes(hashlib.sha256(label.encode()).digest()[:8], "little"))


def opt_w(A, D, nu):
    """Optimal moment weight: the subtracted estimate's variance belongs in it."""
    return 1.0 / ((A + D) ** 2 + D ** 2 / nu)


def gvf(Dhat, n, idx):
    """Ratio-form generalised variance function D ~ c / n, fitted on idx."""
    c = (Dhat[:, idx] * n[idx]).mean(axis=1, keepdims=True)
    return c / n[None, :]


def summarise(a, A=A_TRUE):
    trunc = float((a <= 0).mean())
    at = np.maximum(a, 0.0)
    return dict(bias=float(a.mean() - A), sd=float(a.std(ddof=1)),
                rmse=float(np.sqrt(np.mean((a - A) ** 2))),
                rmse_trunc=float(np.sqrt(np.mean((at - A) ** 2))),
                at_zero=trunc)


def run(K, dbar, sigma_e):
    label = f"exp13|{K}|{dbar}|{sigma_e}"
    rng = seed_for(label)

    n = rng.lognormal(0.0, SIGMA_LOG_N, size=K)
    e = (rng.lognormal(0.0, sigma_e, size=K) if sigma_e > 0 else np.ones(K))
    D = e / n
    D *= A_TRUE * dbar / D.mean()
    nu = np.full(K, NU)
    sig2 = A_TRUE + D

    K_known = float(np.sum((A_TRUE / sig2) ** 2))
    K_eff = float(np.sum(A_TRUE ** 2 / (sig2 ** 2 + D ** 2 / nu)))
    tr = np.arange(K) % 2 == 0          # fixed split: even / odd populations
    ev = ~tr
    K_eff_ev = float(np.sum(A_TRUE ** 2 / (sig2[ev] ** 2 + D[ev] ** 2 / nu[ev])))

    Y = rng.normal(0.0, np.sqrt(sig2), size=(REPS, K))
    Dhat = D * rng.chisquare(nu, size=(REPS, K)) / nu
    Z = Y ** 2 - Dhat                                   # E Z_i = A

    wavg = lambda z, w: (z * w).sum(1) / w.sum(1)
    A_unw = Z.mean(axis=1)
    A_unw_ev = Z[:, ev].mean(axis=1)

    w_or = np.broadcast_to(opt_w(A_TRUE, D, nu), (REPS, K))
    A_or = wavg(Z, w_or)

    A0 = np.maximum(A_unw, 1e-9)[:, None]
    w_pl = opt_w(A0, Dhat, nu)
    A_pl = wavg(Z, w_pl)

    D_all = np.maximum(gvf(Dhat, n, np.arange(K)), 1e-9)
    w_ga = opt_w(A0, D_all, nu)
    A_ga = wavg(Z, w_ga)

    # split: everything entering the evaluation weights comes from the training half
    A_tr = np.maximum(Z[:, tr].mean(axis=1), 1e-9)[:, None]
    D_tr = np.maximum(gvf(Dhat, n, np.where(tr)[0]), 1e-9)
    w_sp = opt_w(A_tr, D_tr[:, ev], nu[ev])
    A_sp = wavg(Z[:, ev], w_sp)

    # two-fold cross-fitting: each half weighted from the other
    A_ev = np.maximum(Z[:, ev].mean(axis=1), 1e-9)[:, None]
    D_ev = np.maximum(gvf(Dhat, n, np.where(ev)[0]), 1e-9)
    num = ((Z[:, ev] * w_sp).sum(1)
           + (Z[:, tr] * opt_w(A_ev, D_ev[:, tr], nu[tr])).sum(1))
    den = w_sp.sum(1) + opt_w(A_ev, D_ev[:, tr], nu[tr]).sum(1)
    A_cv = num / den

    arms = dict(unweighted=A_unw, plugin=A_pl, gvf_all=A_ga, gvf_cv=A_cv,
                oracle=A_or, gvf_split=A_sp, unweighted_eval=A_unw_ev)
    out = dict(K=K, Dbar_over_A=dbar, sigma_e=sigma_e, reps=REPS,
               cv_D=float(D.std() / D.mean()),
               K_raw=float(K), K_known=K_known, K_eff=K_eff, K_eff_eval=K_eff_ev,
               rse_ideal=float(np.sqrt(2 / K_known)),
               rse_bound=float(np.sqrt(2 / K_eff)),
               rse_bound_eval=float(np.sqrt(2 / K_eff_ev)))
    for name, a in arms.items():
        s = summarise(a)
        base = out["rse_bound_eval"] if name.endswith("_eval") or name == "gvf_split" \
            else out["rse_bound"]
        for k, v in s.items():
            out[f"{name}_{k}"] = v
        out[f"{name}_eff"] = base / s["rmse"]
    for name, w in dict(plugin=w_pl, gvf_all=w_ga, oracle=w_or).items():
        out[f"{name}_maxshare"] = float(np.median(w.max(1) / w.sum(1)))

    # ---- Part B: a band whose containment is guaranteed by construction ----
    m = conformal_rank(K, ALPHA0)
    absY = np.abs(Y)
    band_oracle = np.sort(absY / np.sqrt(1.0 + D / A_TRUE), axis=1)[:, m - 1]
    G = rng.normal(0.0, np.sqrt(A_TRUE), size=REPS)

    # simultaneous lower limits on the design variances, Bonferroni over K
    vL2 = nu * Dhat / chi2.ppf(1.0 - ETA2 / K, nu)
    # one-sided upper limit on A from the unweighted moment estimator
    varZ = (2 * (A0 + Dhat) ** 2 + 2 * Dhat ** 2 / nu).sum(1) / K ** 2
    z1 = float(norm.ppf(1.0 - ETA1))
    sU2 = np.maximum(A_unw + z1 * np.sqrt(varZ), 1e-9)
    band_guard = np.sort(absY / np.sqrt(1.0 + vL2 / sU2[:, None]), axis=1)[:, m - 1]
    # exp12's band for reference: bound s_G only, substitute Dhat
    band_exp12 = np.sort(absY / np.sqrt(1.0 + Dhat / sU2[:, None]), axis=1)[:, m - 1]

    out.update(
        nominal=m / (K + 1.0),
        cov_oracle=float((np.abs(G) <= band_oracle).mean()),
        cov_guard=float((np.abs(G) <= band_guard).mean()),
        cov_exp12=float((np.abs(G) <= band_exp12).mean()),
        contain_guard=float((band_guard >= band_oracle).mean()),
        contain_exp12=float((band_exp12 >= band_oracle).mean()),
        sU_covers_A=float((sU2 >= A_TRUE).mean()),
        vL_covers_all=float((vL2 <= D).all(axis=1).mean()),
        w_oracle_band=float(band_oracle.mean()),
        w_guard=float(band_guard.mean()), w_exp12=float(band_exp12.mean()),
        guard_over_oracle=float((band_guard / band_oracle).mean()),
        exp12_over_oracle=float((band_exp12 / band_oracle).mean()),
        mc_se=float(np.sqrt(0.95 * 0.05 / REPS)),
    )
    return out


def main():
    rows = [run(K, db, se) for K in K_GRID for db in DBAR_GRID for se in SIGMA_E_GRID]
    df = pd.DataFrame(rows)
    out = ROOT / "results" / "exp13_weights_and_containment.csv"
    df.to_csv(out, index=False)
    (ROOT / "results" / "exp13_manifest.json").write_text(json.dumps(dict(
        experiment="exp13_weights_and_containment", reps=REPS, cells=len(df),
        alpha0=ALPHA0, eta=ETA, eta1=ETA1, eta2=ETA2, nu=NU,
        t3_split_beats_matched=float((df.gvf_split_rmse
                                      < df.unweighted_eval_rmse).mean()),
        t4_split_beats_full=float((df.gvf_split_rmse < df.unweighted_rmse).mean()),
        t6_min_contain_guard=float(df.contain_guard.min()),
        t6_min_contain_exp12=float(df.contain_exp12.min()),
        guard_width_range=[float(df.guard_over_oracle.min()),
                           float(df.guard_over_oracle.max())],
    ), indent=2) + "\n")

    pd.set_option("display.width", 240, "display.max_columns", 80)
    lab = ["K", "Dbar_over_A", "sigma_e"]
    print("=== decomposition: ideal (D known) -> bound (D estimated) -> procedure")
    print(df.set_index(lab)[["cv_D", "K_raw", "K_known", "K_eff",
                             "rse_ideal", "rse_bound", "unweighted_rmse"]]
          .round(4).to_string())
    print("\n=== Part A: RMSE by arm (full-sample arms scored on the full bound,")
    print("    split arms on the evaluation-half bound)")
    cols = [f"{a}_rmse" for a in ("unweighted", "plugin", "gvf_all", "gvf_cv",
                                  "oracle", "unweighted_eval", "gvf_split")]
    print(df.set_index(lab)[cols].round(4).to_string())
    print("\n=== Part A: efficiency against the appropriate bound")
    print(df.set_index(lab)[[c.replace("_rmse", "_eff") for c in cols]]
          .round(4).to_string())
    print("\n=== Part A: bias, truncation, extreme weights")
    print(df.set_index(lab)[["unweighted_bias", "plugin_bias", "gvf_all_bias",
                             "gvf_split_bias", "oracle_bias",
                             "unweighted_at_zero", "gvf_all_at_zero",
                             "plugin_maxshare", "gvf_all_maxshare",
                             "oracle_maxshare"]].round(4).to_string())
    print("\n=== Part B: containment and cost  (MC SE about 0.0015)")
    print(df.set_index(lab)[["nominal", "sU_covers_A", "vL_covers_all",
                             "contain_exp12", "contain_guard",
                             "cov_oracle", "cov_exp12", "cov_guard",
                             "exp12_over_oracle", "guard_over_oracle"]]
          .round(4).to_string())
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
