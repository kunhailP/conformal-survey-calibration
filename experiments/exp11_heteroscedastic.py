"""exp11 - does the correction-factor upper limit survive unequal design variances?

Protocol: docs/PROTOCOL_exp11_heteroscedastic.md (written before execution).
Derivations: docs/THEORY_certification.md.  Predecessors: exp09, exp10.

Scalar target, unequal design variances across populations:

    Y_i ~ N(mu, A + D_i),   nu_i * Dhat_i / D_i ~ chi2_{nu_i},   independent,

with the correction factor kappa = sqrt(A / (A + mean(D_i))).  Neither side of
the exp10 pivot is chi-square here, so the F interval is an approximation and
this experiment asks over what range of dispersion its one-sided upper limit
keeps its error control.

No microdata required.

    python experiments/exp11_heteroscedastic.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm, f as fdist

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from dac.bands import conformal_rank                       # noqa: E402

REPS = 20000
K_GRID = (30, 100, 300)
DBAR_GRID = (0.25, 1.0, 4.0)
SLOG_GRID = (0.0, 0.5, 1.0, 1.5)
NU_I = 10.0
A_TRUE = 1.0
ALPHA0 = 0.05
ETA = 0.05
EPS = 0.10
SPLITS = np.linspace(0.1, 0.9, 17)     # anchor share scanned for the enlargement


def seed_for(label: str) -> np.random.Generator:
    return np.random.default_rng(
        int.from_bytes(hashlib.sha256(label.encode()).digest()[:8], "little"))


def satterthwaite_num(D: np.ndarray, nu: np.ndarray) -> float:
    """df of the averaged variance estimator, matching its first two moments."""
    K = len(D)
    return float(K ** 2 * D.mean() ** 2 / np.sum(D ** 2 / nu))


def satterthwaite_den(sig2: np.ndarray) -> float:
    """df of S_Y^2 when the Y_i are independent but not identically distributed.

    Var(S_Y^2) = 2 tr((P Sigma)^2) / (K-1)^2 with P = I - J/K, which reduces to
    s2 (1 - 2/K) + s1^2 / K^2.  Equals K-1 exactly when the sig2 are equal.
    """
    K = len(sig2)
    s1, s2 = sig2.sum(), (sig2 ** 2).sum()
    tr = s2 * (1 - 2.0 / K) + s1 ** 2 / K ** 2
    return float((K - 1) ** 2 * (s1 / K) ** 2 / tr)


def kappa_upper(R: np.ndarray, nu_n, nu_d, eta: float) -> np.ndarray:
    """One-sided upper limit for kappa from the (approximate) F pivot."""
    rho2_L = np.clip(R / fdist.ppf(1.0 - eta, nu_n, nu_d), 0.0, 1.0)
    return np.sqrt(1.0 - rho2_L)


def run(K: int, dbar: float, slog: float, disperse_nu: bool = False) -> dict:
    label = f"exp11|{K}|{dbar}|{slog}|{disperse_nu}"
    rng = seed_for(label)

    Dbar = A_TRUE * dbar
    if slog == 0.0:
        D = np.full(K, Dbar)
    else:
        D = rng.lognormal(0.0, slog, size=K)
        D *= Dbar / D.mean()                       # hold the mean exactly
    nu = (np.maximum(rng.lognormal(np.log(NU_I), 0.6, size=K), 2.0)
          if disperse_nu else np.full(K, NU_I))
    sig2 = A_TRUE + D
    T = float(sig2.mean())                          # = A + mean(D)
    kappa = float(np.sqrt(A_TRUE / T))

    nu_n_or = satterthwaite_num(D, nu)
    nu_d_or = satterthwaite_den(sig2)

    Y = rng.normal(0.0, np.sqrt(sig2), size=(REPS, K))
    Y -= Y.mean(axis=1, keepdims=True)
    SY2 = (Y ** 2).sum(axis=1) / (K - 1)
    Dhat = D * rng.chisquare(nu, size=(REPS, K)) / nu
    Dbar_hat = Dhat.mean(axis=1)
    R = Dbar_hat / SY2

    # feasible Satterthwaite: everything from the data
    A0 = np.maximum(SY2 - Dbar_hat, 1e-9)
    nu_n_fe = K ** 2 * Dbar_hat ** 2 / (Dhat ** 2 / nu).sum(axis=1)
    sg2 = A0[:, None] + Dhat
    s1, s2 = sg2.sum(axis=1), (sg2 ** 2).sum(axis=1)
    tr = s2 * (1 - 2.0 / K) + s1 ** 2 / K ** 2
    nu_d_fe = (K - 1) ** 2 * (s1 / K) ** 2 / tr

    kapU_or = kappa_upper(R, nu_n_or, nu_d_or, ETA)
    kapU_fe = kappa_upper(R, nu_n_fe, nu_d_fe, ETA)
    kap_plug = np.sqrt(np.maximum(1.0 - R, 0.0))

    # two-sided interval, for certification only
    a = ETA / 2
    rL = np.clip(R / fdist.ppf(1 - a, nu_n_fe, nu_d_fe), 0, 1)
    rU = np.clip(R / fdist.ppf(a, nu_n_fe, nu_d_fe), 0, 1)
    kL, kU = np.sqrt(1 - rU), np.sqrt(1 - rL)
    r_star = np.where(kL > 0, (kU - kL) / (kU + kL), np.inf)
    kstar = np.where(kL > 0, 2 * kL * kU / np.maximum(kL + kU, 1e-300), np.nan)
    cert = r_star <= EPS

    # bands, all on the latent target, all at total budget alpha0 + eta = 0.10
    m = conformal_rank(K, ALPHA0)
    qa = np.sort(np.abs(Y), axis=1)[:, m - 1] if m <= K else np.full(REPS, np.inf)
    G = rng.normal(0.0, np.sqrt(A_TRUE), size=REPS)
    D_new = D[rng.integers(0, K, size=REPS)]        # the target's own design variance

    hit = lambda r: float((np.abs(G) <= r).mean())
    cov_oracle, w_oracle = hit(qa * kappa), float((qa * kappa).mean())
    cov_safe, w_safe = hit(qa * kapU_fe), float((qa * kapU_fe).mean())
    cov_safe_or = hit(qa * kapU_or)
    cov_plug, w_plug = hit(qa * kap_plug), float((qa * kap_plug).mean())

    # enlargement with its budget split optimised, given the same total
    best = None
    for share in SPLITS:
        a0, beta = 0.10 * share, 0.10 * (1 - share)
        mm = conformal_rank(K, a0)
        if mm > K:
            continue
        q0 = np.sort(np.abs(Y), axis=1)[:, mm - 1]
        r = q0 + np.sqrt(D_new) * norm.ppf(1.0 - beta / 2.0)
        w = float(r.mean())
        if best is None or w < best[0]:
            best = (w, hit(r), float(share))
    w_enl, cov_enl, enl_share = best

    # Gaussian model-based plug-in prediction interval, no guarantee
    r_mod = norm.ppf(1 - 0.10 / 2) * kap_plug * np.sqrt(SY2)
    cov_mod, w_mod = hit(r_mod), float(r_mod.mean())

    return dict(
        K=K, Dbar_over_A=dbar, slog=slog, disperse_nu=disperse_nu, reps=REPS,
        kappa=kappa, cv_D=float(D.std() / D.mean()),
        nu_num_oracle=nu_n_or, nu_den_oracle=nu_d_or, nu_den_ratio=nu_d_or / (K - 1),
        nu_num_feas_med=float(np.median(nu_n_fe)),
        nu_den_feas_med=float(np.median(nu_d_fe)),
        fail_upper_feas=float((kappa > kapU_fe).mean()),
        fail_upper_oracle=float((kappa > kapU_or).mean()),
        fail_mc=float(np.sqrt(ETA * (1 - ETA) / REPS)),
        cov_oracle=cov_oracle, cov_safe=cov_safe, cov_safe_oracle_df=cov_safe_or,
        cov_plug=cov_plug, cov_enlarge=cov_enl, cov_model=cov_mod,
        w_oracle=w_oracle, w_safe=w_safe, w_plug=w_plug,
        w_enlarge=w_enl, w_model=w_mod, enl_share=enl_share,
        safe_over_oracle=w_safe / w_oracle, safe_over_enlarge=w_safe / w_enl,
        safe_over_model=w_safe / w_mod,
        cert_rate=float(cert.mean()),
        cert_error=float((cert & (np.abs(kstar / kappa - 1) > EPS)).mean()),
    )


def main() -> None:
    rows = [run(K, db, sl) for K in K_GRID for db in DBAR_GRID for sl in SLOG_GRID]
    rows += [run(K, db, 1.0, disperse_nu=True) for K in K_GRID for db in DBAR_GRID]
    df = pd.DataFrame(rows)
    out = ROOT / "results" / "exp11_heteroscedastic.csv"
    df.to_csv(out, index=False)

    main_grid = df[~df.disperse_nu]
    (ROOT / "results" / "exp11_manifest.json").write_text(json.dumps(dict(
        experiment="exp11_heteroscedastic", reps=REPS, cells=len(df),
        alpha0=ALPHA0, eta=ETA, eps=EPS, nu_per_population=NU_I,
        K_grid=list(K_GRID), Dbar_grid=list(DBAR_GRID), slog_grid=list(SLOG_GRID),
        max_fail_upper_feasible=float(df.fail_upper_feas.max()),
        max_fail_upper_oracle=float(df.fail_upper_oracle.max()),
        homoscedastic_control_fail=float(
            main_grid[main_grid.slog == 0].fail_upper_feas.max()),
        min_cov_safe=float(df.cov_safe.min()),
        safe_over_enlarge_range=[float(df.safe_over_enlarge.min()),
                                 float(df.safe_over_enlarge.max())],
    ), indent=2) + "\n")

    pd.set_option("display.width", 220, "display.max_columns", 60)
    lab = ["K", "Dbar_over_A", "slog"]
    print("=== R2/R3: one-sided upper limit, Pr(kappa > kappa_U), budget eta = 0.05")
    print("    (Monte Carlo SE about 0.0015)")
    print(main_grid.set_index(lab)[["cv_D", "nu_den_ratio", "fail_upper_oracle",
                                    "fail_upper_feas"]].round(4).to_string())
    print("\n=== R4: latent-target coverage, guaranteed level 0.90")
    print(main_grid.set_index(lab)[["cov_oracle", "cov_safe", "cov_plug",
                                    "cov_enlarge", "cov_model"]].round(4).to_string())
    print("\n=== R5: mean widths, same total budget")
    print(main_grid.set_index(lab)[["safe_over_oracle", "safe_over_enlarge",
                                    "safe_over_model", "enl_share"]]
          .round(4).to_string())
    print("\n=== dispersed nu side-set")
    print(df[df.disperse_nu].set_index(["K", "Dbar_over_A"])[
        ["fail_upper_feas", "cov_safe", "safe_over_enlarge"]].round(4).to_string())
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
