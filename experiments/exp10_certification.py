"""exp10 - certification with an error budget, against the frozen gate.

Protocol: docs/PROTOCOL_exp10_certification.md (written before execution).
Derivations: docs/THEORY_certification.md.

Closed model, the development plan's section 2:

    Y_i = mu + u_i + e_i,  u_i ~ N(0, A),  e_i ~ N(0, D),  i = 1..K,
    nu * Dhat / D ~ chi2_nu,   independent of the Y.

Two questions.  Does a confidence-interval certification reduce false
certification against the frozen gate, and does it abstain so often as to be
useless?  And which quantity should be certified: the latent scale s_G, or the
band's width factor kappa = s_G / s_Y?

No microdata required.

    python experiments/exp10_certification.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2, f as fdist

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

REPS = 20000
K_GRID = (30, 100, 300)
DA_GRID = (0.25, 1.0, 4.0)
NU_GRID = (4.0, 12.0, 40.0)
A_TRUE = 1.0
EPS = 0.10                      # tolerance on relative error
ETA = 0.05                      # budget for a wrong certification
TAU_FROZEN = 0.147              # the implementation's frozen threshold
ALPHA0 = 0.05                   # conformal miss budget; band target 1 - a0 - eta
K_FLOOR = 94                    # the implementation's stated population floor


def seed_for(label: str) -> np.random.Generator:
    digest = hashlib.sha256(label.encode()).digest()[:8]
    return np.random.default_rng(int.from_bytes(digest, "little"))


def minimax(L: np.ndarray, U: np.ndarray):
    """Point estimate minimising the worst relative error over [L, U],
    and that worst relative error.  Undefined, hence no certification, at L=0."""
    ok = L > 0
    star = np.where(ok, 2 * L * U / np.maximum(L + U, 1e-300), np.nan)
    r = np.where(ok, (U - L) / np.maximum(U + L, 1e-300), np.inf)
    return star, r


def gw_interval(S1: np.ndarray, n1: float, S2: np.ndarray, n2: float,
                eta: float):
    """Graybill-Wang modified large-sample interval for theta = sigma1 - sigma2,
    the standard interval for a difference of variance components."""
    a = eta / 2
    G1 = 1 - n1 / chi2.ppf(1 - a, n1)
    H1 = n1 / chi2.ppf(a, n1) - 1
    G2 = 1 - n2 / chi2.ppf(1 - a, n2)
    H2 = n2 / chi2.ppf(a, n2) - 1
    hat = S1 - S2
    lo = hat - np.sqrt((G1 * S1) ** 2 + (H2 * S2) ** 2)
    hi = hat + np.sqrt((H1 * S1) ** 2 + (G2 * S2) ** 2)
    return np.maximum(lo, 0.0), hi


def run(K: int, da: float, nu: float, pooled: bool = False) -> dict:
    """pooled=False: one variance estimate on nu total degrees of freedom.
    pooled=True: nu degrees of freedom *per population*, averaged over the K of
    them, which is what the manuscript's mean design variance actually is."""
    label = f"exp10|{K}|{da}|{nu}|{pooled}"
    rng = seed_for(label)
    D = A_TRUE * da
    T = A_TRUE + D
    rho2 = D / T
    kappa = np.sqrt(1.0 - rho2)          # the band's width factor
    s_true = np.sqrt(A_TRUE)             # the latent scale

    # --- data -----------------------------------------------------------
    Y = rng.normal(0.0, np.sqrt(T), size=(REPS, K))
    Y -= Y.mean(axis=1, keepdims=True)
    SY2 = (Y ** 2).sum(axis=1) / (K - 1)                 # ~ T chi2_{K-1}/(K-1)
    nu_tot = nu * K if pooled else nu
    Dhat = D * rng.chisquare(nu_tot, size=REPS) / nu_tot

    Ahat = np.maximum(SY2 - Dhat, 0.0)
    kap_plug = np.sqrt(np.maximum(1.0 - Dhat / SY2, 0.0))
    err_kap = np.abs(kap_plug / kappa - 1.0)             # the shared criterion
    err_s = np.abs(np.sqrt(Ahat) / s_true - 1.0)

    # --- rules ----------------------------------------------------------
    rules = {}
    rules["fixed_K"] = np.full(REPS, K >= K_FLOOR)

    diag = np.where(Ahat > 0, np.sqrt(2.0 / (K - 1)) * SY2
                    / np.maximum(Ahat, 1e-300), np.inf)
    rules["plug_frozen"] = diag <= TAU_FROZEN
    rules["plug_matched"] = diag <= 2 * EPS

    # the plan's section 3: two chi2 intervals, union bound, interval arithmetic
    a = ETA / 2
    TL = (K - 1) * SY2 / chi2.ppf(1 - a, K - 1)
    TU = (K - 1) * SY2 / chi2.ppf(a, K - 1)
    DL = nu_tot * Dhat / chi2.ppf(1 - a, nu_tot)
    DU = nu_tot * Dhat / chi2.ppf(a, nu_tot)
    AL_u, AU_u = np.maximum(TL - DU, 0.0), TU - DL
    valid_u = AU_u > 0
    _, r_u = minimax(np.sqrt(AL_u), np.sqrt(np.maximum(AU_u, 0.0)))
    rules["ci_union"] = valid_u & (r_u <= EPS)

    AL_g, AU_g = gw_interval(SY2, K - 1, Dhat, nu_tot, ETA)
    _, r_g = minimax(np.sqrt(AL_g), np.sqrt(np.maximum(AU_g, 0.0)))
    rules["ci_gw"] = (AU_g > 0) & (r_g <= EPS)

    # exact pivotal interval for rho^2, hence for kappa: (Dhat/SY2)/rho^2 ~ F
    R = Dhat / SY2
    rho2_L = np.clip(R / fdist.ppf(1 - a, nu_tot, K - 1), 0.0, 1.0)
    rho2_U = np.clip(R / fdist.ppf(a, nu_tot, K - 1), 0.0, 1.0)
    kapL, kapU = np.sqrt(1.0 - rho2_U), np.sqrt(1.0 - rho2_L)
    kap_star, r_k = minimax(kapL, kapU)
    rules["ci_kappa"] = r_k <= EPS

    # --- the safe band, plan section 6 -----------------------------------
    m = int(np.ceil((1 - ALPHA0) * (K + 1)))
    absY = np.sort(np.abs(Y), axis=1)
    qA = absY[:, m - 1] if m <= K else np.full(REPS, np.inf)
    G_new = rng.normal(0.0, np.sqrt(A_TRUE), size=REPS)
    cov_oracle = float((np.abs(G_new) <= qA * kappa).mean())
    cov_plug = float((np.abs(G_new) <= qA * kap_plug).mean())
    cov_safe = float((np.abs(G_new) <= qA * kapU).mean())

    out = dict(K=K, D_over_A=da, nu=nu, pooled=pooled, nu_tot=float(nu_tot),
               reps=REPS, rho=float(np.sqrt(rho2)),
               kappa=float(kappa), eps=EPS, eta=ETA,
               err_kap_rate=float((err_kap > EPS).mean()),
               err_s_rate=float((err_s > EPS).mean()),
               rse_kappa=float(kap_plug.std(ddof=1) / kappa),
               rse_s=float(np.sqrt(Ahat).std(ddof=1) / s_true),
               ci_kappa_cover=float(((kapL <= kappa) & (kappa <= kapU)).mean()),
               ci_union_cover=float(((np.sqrt(AL_u) <= s_true)
                                     & (s_true <= np.sqrt(np.maximum(AU_u, 0))))
                                    .mean()),
               ci_gw_cover=float(((np.sqrt(AL_g) <= s_true)
                                  & (s_true <= np.sqrt(np.maximum(AU_g, 0))))
                                 .mean()),
               cov_oracle=cov_oracle, cov_plug=cov_plug, cov_safe=cov_safe,
               width_safe_over_oracle=float((kapU / kappa).mean()),
               width_plug_over_oracle=float((kap_plug / kappa).mean()),
               width_safe_over_anchor=float((kapU).mean()),
               width_oracle_over_anchor=float(kappa))

    for name, cert in rules.items():
        out[f"cert_{name}"] = float(cert.mean())
        out[f"false_{name}"] = float((cert & (err_kap > EPS)).mean())
        out[f"falses_{name}"] = float((cert & (err_s > EPS)).mean())
    # ci_kappa scored on its own minimax estimate rather than the plug-in
    err_star = np.where(np.isfinite(kap_star),
                        np.abs(kap_star / kappa - 1.0), np.inf)
    out["false_ci_kappa_star"] = float((rules["ci_kappa"]
                                        & (err_star > EPS)).mean())
    return out


def main() -> None:
    rows = [run(K, da, nu, pooled)
            for pooled in (False, True)
            for K in K_GRID for da in DA_GRID for nu in NU_GRID]
    df = pd.DataFrame(rows)
    out = ROOT / "results" / "exp10_certification.csv"
    df.to_csv(out, index=False)

    rules = ["fixed_K", "plug_frozen", "plug_matched", "ci_union", "ci_gw",
             "ci_kappa"]
    manifest = dict(
        experiment="exp10_certification", reps=REPS, cells=len(df),
        eps=EPS, eta=ETA, tau_frozen=TAU_FROZEN, alpha0=ALPHA0,
        K_grid=list(K_GRID), D_over_A_grid=list(DA_GRID),
        nu_grid=list(NU_GRID),
        max_false_rate={r: float(df[f"false_{r}"].max()) for r in rules},
        mean_cert_rate={r: float(df[f"cert_{r}"].mean()) for r in rules},
        ci_kappa_coverage_range=[float(df.ci_kappa_cover.min()),
                                 float(df.ci_kappa_cover.max())],
        safe_band_coverage_min=float(df.cov_safe.min()),
        plug_band_coverage_min=float(df.cov_plug.min()),
    )
    (ROOT / "results" / "exp10_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n")

    pd.set_option("display.width", 220, "display.max_columns", 60)
    lab = ["pooled", "K", "rho", "nu"]
    print("=== false certification rate, budget eta = 0.05, criterion |kappa_hat/kappa - 1| > 0.10")
    print(df.set_index(lab)[[f"false_{r}" for r in rules]].round(4).to_string())
    print("\n=== certification rate (how often the rule says yes)")
    print(df.set_index(lab)[[f"cert_{r}" for r in rules]].round(4).to_string())
    print("\n=== interval coverage, nominal 0.95")
    print(df.set_index(lab)[["ci_union_cover", "ci_gw_cover",
                             "ci_kappa_cover"]].round(4).to_string())
    print("\n=== the two targets: realised relative SD")
    two = df.set_index(lab)[["rse_s", "rse_kappa"]].copy()
    two["ratio"] = two.rse_kappa / two.rse_s
    two["rho2"] = two.index.get_level_values("rho") ** 2
    print(two.round(4).to_string())
    print("\n=== safe band, target 1 - alpha0 - eta = 0.90")
    print(df.set_index(lab)[["cov_oracle", "cov_plug", "cov_safe",
                             "width_plug_over_oracle",
                             "width_safe_over_oracle"]].round(4).to_string())
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
