"""exp12 - closing the scalar heteroscedastic case.

Protocol: docs/PROTOCOL_exp12_closing_scalar.md (written before execution).
Predecessors: exp09, exp10, exp11.

Three questions raised in review of exp11, none answered by more coordinates.

Q1  Which oracle band does the manuscript license under unequal design
    variances - per-population standardisation (a), or the common-denominator
    construction (b) that exp07 and exp11 actually use - and does the scalar
    kappa_U band contain the right one?
Q2  Is information destroyed by heteroscedasticity, or discarded by summarising
    with an unweighted variance?
Q3  How does the safe band compare with a model-based interval that is valid
    rather than a plug-in?

No microdata required.

    python experiments/exp12_closing_scalar.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm, chi2, f as fdist

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from dac.bands import conformal_rank                        # noqa: E402

REPS = 20000
K_GRID = (30, 100, 300)
DBAR_GRID = (1.0, 4.0)
SLOG_GRID = (0.0, 0.5, 1.0, 1.5)
NU_I = 10.0
A_TRUE = 1.0
ALPHA0 = ETA = 0.05
SPLITS = np.linspace(0.1, 0.9, 17)


def seed_for(label):
    return np.random.default_rng(
        int.from_bytes(hashlib.sha256(label.encode()).digest()[:8], "little"))


def sat_den(sig2):
    """Effective df of the unweighted S_Y^2 - a property of that statistic."""
    K = len(sig2)
    s1, s2 = sig2.sum(), (sig2 ** 2).sum()
    return float((K - 1) ** 2 * (s1 / K) ** 2
                 / (s2 * (1 - 2.0 / K) + s1 ** 2 / K ** 2))


def sat_num(D, nu):
    K = len(D)
    return float(K ** 2 * D.mean() ** 2 / np.sum(D ** 2 / nu))


def gw_upper(S1, n1, S2, n2, eta):
    """One-sided Graybill-Wang upper limit for sigma1 - sigma2."""
    H1 = n1 / chi2.ppf(eta, n1) - 1.0
    G2 = 1.0 - n2 / chi2.ppf(1.0 - eta, n2)
    return S1 - S2 + np.sqrt((H1 * S1) ** 2 + (G2 * S2) ** 2)


def order_stat(x, m):
    return np.sort(x, axis=1)[:, m - 1]


def run(K, dbar, slog, label_extra="", two_point=False):
    label = f"exp12|{K}|{dbar}|{slog}|{two_point}"
    rng = seed_for(label)

    if two_point:
        D = np.r_[np.full(K // 2, 0.1), np.full(K - K // 2, 7.9)]
        D = D * (A_TRUE * dbar) / D.mean()
    elif slog == 0.0:
        D = np.full(K, A_TRUE * dbar)
    else:
        D = rng.lognormal(0.0, slog, size=K)
        D *= A_TRUE * dbar / D.mean()
    nu = np.full(K, NU_I)
    sig2 = A_TRUE + D
    T = float(sig2.mean())
    kappa = float(np.sqrt(A_TRUE / T))

    nu_d, nu_n = sat_den(sig2), sat_num(D, nu)
    K_I = float(np.sum((A_TRUE / (A_TRUE + D)) ** 2))
    K_I_eff = float(np.sum(A_TRUE ** 2 / ((A_TRUE + D) ** 2 + D ** 2 / nu)))

    Y = rng.normal(0.0, np.sqrt(sig2), size=(REPS, K))
    Y -= Y.mean(axis=1, keepdims=True)
    SY2 = (Y ** 2).sum(axis=1) / (K - 1)
    Dhat = D * rng.chisquare(nu, size=(REPS, K)) / nu
    Dbar_hat = Dhat.mean(axis=1)

    # ---- Q2: lost or discarded -----------------------------------------
    A_unw = SY2 - Dbar_hat
    w_or = 1.0 / ((A_TRUE + D) ** 2 + D ** 2 / nu)
    A_wor = (Y ** 2 - Dhat) @ w_or / w_or.sum()
    A0 = np.maximum(A_unw, 1e-9)[:, None]
    w_fe = 1.0 / ((A0 + Dhat) ** 2 + Dhat ** 2 / nu)
    A_wfe = ((Y ** 2 - Dhat) * w_fe).sum(1) / w_fe.sum(1)
    rse = lambda a: float(np.sqrt(np.mean((a - A_TRUE) ** 2)) / A_TRUE)

    # ---- Q1: the two oracle constructions -------------------------------
    m = conformal_rank(K, ALPHA0)
    if m > K:
        return None
    Wn = rng.normal(size=REPS)
    G = np.sqrt(A_TRUE) * Wn                       # the latent target

    q_a = order_stat(np.abs(Y) / np.sqrt(sig2), m)          # (a) per-population
    band_a = np.sqrt(A_TRUE) * q_a
    q_raw = order_stat(np.abs(Y), m)
    band_b = q_raw * kappa                                   # (b) common scale

    # ---- safe bands ------------------------------------------------------
    R = Dbar_hat / SY2
    nu_n_fe = K ** 2 * Dbar_hat ** 2 / (Dhat ** 2 / nu).sum(axis=1)
    sg2 = np.maximum(A_unw, 1e-9)[:, None] + Dhat
    s1, s2 = sg2.sum(1), (sg2 ** 2).sum(1)
    nu_d_fe = (K - 1) ** 2 * (s1 / K) ** 2 / (s2 * (1 - 2.0 / K) + s1 ** 2 / K ** 2)
    kapU = np.sqrt(1.0 - np.clip(R / fdist.ppf(1 - ETA, nu_n_fe, nu_d_fe), 0, 1))
    safe_b = q_raw * kapU                                    # exp11's band

    A_U = np.maximum(gw_upper(SY2, nu_d_fe, Dbar_hat, nu_n_fe, ETA), 1e-9)
    # safe band for construction (a): m-th order statistic of h_c(s) at s^2 = A_U
    h = np.abs(Y) / np.sqrt(1.0 + Dhat / A_U[:, None])
    safe_a = order_stat(h, m)

    # ---- competitors, same total budget 0.10 ------------------------------
    D_new = D[rng.integers(0, K, size=REPS)]
    hit = lambda r: float((np.abs(G) <= r).mean())
    best = None
    for share in SPLITS:
        a0, beta = 0.10 * share, 0.10 * (1 - share)
        mm = conformal_rank(K, a0)
        if mm > K:
            continue
        r = order_stat(np.abs(Y), mm) + np.sqrt(D_new) * norm.ppf(1 - beta / 2)
        if best is None or r.mean() < best[0]:
            best = (float(r.mean()), hit(r), float(share))
    w_enl, cov_enl, enl_share = best

    r_mvalid = norm.ppf(1 - ALPHA0 / 2) * np.sqrt(A_U)       # valid, model-based
    r_mplug = norm.ppf(1 - 0.10 / 2) * np.sqrt(np.maximum(A_unw, 0.0))

    return dict(
        K=K, Dbar_over_A=dbar, slog=slog, two_point=two_point, reps=REPS,
        cv_D=float(D.std() / D.mean()), kappa=kappa,
        nu_den=nu_d, nu_num=nu_n, nu_den_over_K1=nu_d / (K - 1),
        K_I=K_I, K_I_eff=K_I_eff, K_raw=float(K),
        rse_bound=float(np.sqrt(2.0 / K_I_eff)),
        rse_unweighted=rse(A_unw), rse_w_oracle=rse(A_wor), rse_w_feasible=rse(A_wfe),
        eff_unweighted=float(np.sqrt(2.0 / K_I_eff)) / rse(A_unw),
        eff_w_oracle=float(np.sqrt(2.0 / K_I_eff)) / rse(A_wor),
        eff_w_feasible=float(np.sqrt(2.0 / K_I_eff)) / rse(A_wfe),
        nominal=m / (K + 1.0),
        cov_oracle_a=hit(band_a), cov_oracle_b=hit(band_b),
        cov_safe_a=hit(safe_a), cov_safe_b=hit(safe_b),
        cov_enlarge=cov_enl, cov_model_valid=hit(r_mvalid), cov_model_plug=hit(r_mplug),
        contain_b_over_a=float((safe_b >= band_a).mean()),
        contain_a_over_a=float((safe_a >= band_a).mean()),
        w_oracle_a=float(band_a.mean()), w_oracle_b=float(band_b.mean()),
        w_safe_a=float(safe_a.mean()), w_safe_b=float(safe_b.mean()),
        w_enlarge=w_enl, w_model_valid=float(r_mvalid.mean()),
        w_model_plug=float(r_mplug.mean()), enl_share=enl_share,
    )


def main():
    rows = [run(K, db, sl) for K in K_GRID for db in DBAR_GRID for sl in SLOG_GRID]
    rows += [run(K, 4.0, np.nan, two_point=True) for K in K_GRID]
    df = pd.DataFrame([r for r in rows if r])
    out = ROOT / "results" / "exp12_closing_scalar.csv"
    df.to_csv(out, index=False)
    (ROOT / "results" / "exp12_manifest.json").write_text(json.dumps(dict(
        experiment="exp12_closing_scalar", reps=REPS, cells=len(df),
        alpha0=ALPHA0, eta=ETA, nu_per_population=NU_I,
        s1_oracle_a_max_dev=float((df.cov_oracle_a - df.nominal).abs().max()),
        s2_oracle_b_max_dev=float((df.cov_oracle_b - df.nominal).abs().max()),
        s3_min_containment_b=float(df.contain_b_over_a.min()),
        s3_min_containment_a=float(df.contain_a_over_a.min()),
        s4_min_eff_unweighted=float(df.eff_unweighted.min()),
        s4_min_eff_w_oracle=float(df.eff_w_oracle.min()),
        s5_model_valid_narrower=float((df.w_model_valid < df.w_safe_a).mean()),
    ), indent=2) + "\n")

    pd.set_option("display.width", 230, "display.max_columns", 60)
    lab = ["K", "Dbar_over_A", "slog", "two_point"]
    print("=== Q1 / S1-S3: the two oracle constructions, and containment")
    print(df.set_index(lab)[["nominal", "cov_oracle_a", "cov_oracle_b",
                             "w_oracle_b", "w_oracle_a",
                             "contain_b_over_a", "contain_a_over_a",
                             "cov_safe_a", "cov_safe_b"]].round(4).to_string())
    print("\n=== Q2 / S4: lost or discarded?  (eff = bound / realised RSE)")
    print(df.set_index(lab)[["nu_den_over_K1", "K_raw", "K_I", "K_I_eff",
                             "rse_bound", "rse_unweighted", "rse_w_oracle",
                             "rse_w_feasible", "eff_unweighted", "eff_w_oracle",
                             "eff_w_feasible"]].round(4).to_string())
    print("\n=== Q3 / S5: competitors at the same guaranteed 0.90")
    print(df.set_index(lab)[["cov_safe_a", "cov_enlarge", "cov_model_valid",
                             "cov_model_plug", "w_safe_a", "w_enlarge",
                             "w_model_valid", "w_model_plug"]].round(4).to_string())
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
