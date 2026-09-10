"""exp09 - what does estimating the sampling variance cost?

Protocol: docs/PROTOCOL_exp09_estimated_variance.md (written before execution).
Derivations: docs/THEORY_estimated_variance.md.

Model M1, independently over i = 1..m:

    Y_i ~ N(0, A + D_i),   nu * Dhat_i / D_i ~ chi2_nu,   Y_i _||_ Dhat_i.

Two questions, pointing opposite ways.  The *information* about A lost by
estimating D_i is fourth order in the design share (memo section 2).  The
*plug-in bias* incurred by substituting Dhat_i into a known-D procedure is
first order in 1/nu, does not vanish as populations accumulate, and moves the
manuscript's reliability gate in the anti-conservative direction (memo
section 4).  This experiment checks both.

No microdata required.

    python experiments/exp09_estimated_variance.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

REPS = 2000
M_GRID = (30, 100, 250, 500, 1000)
RHO_GRID = (0.3, 0.5, 0.66, 0.9)
NU_GRID = (5.0, 10.0, 25.0, 100.0, np.inf)
A_TRUE = 1.0
TAU = 0.147                     # the frozen reliability threshold, eq. (14)


def seed_for(label: str) -> np.random.Generator:
    """Cell seeds derive from the cell label, as everywhere else here."""
    digest = hashlib.sha256(label.encode()).digest()[:8]
    return np.random.default_rng(int.from_bytes(digest, "little"))


# ---------------------------------------------------------------- information

def info_eff(A: float, D: np.ndarray, nu: float) -> float:
    """Proposition 1: effective Fisher information for A, D_i profiled out."""
    pen = 0.0 if not np.isfinite(nu) else D ** 2 / nu
    return float(0.5 * np.sum(1.0 / ((A + D) ** 2 + pen)))


def info_known(A: float, D: np.ndarray) -> float:
    """The manuscript's eq. (12): the same with D_i known."""
    return float(0.5 * np.sum((A + D) ** -2.0))


def k_eff(A: float, D: np.ndarray, nu: float) -> float:
    """K_{I,eff} = 2 A^2 I_eff, the information in units of populations."""
    return 2.0 * A ** 2 * info_eff(A, D, nu)


def eff_score_var(A: float, D: np.ndarray, nu: float) -> float:
    """Var of the analytic effective score.  Equals info_eff if Prop. 1 holds."""
    V = A + D
    if not np.isfinite(nu):
        return float(np.sum(1.0 / (2 * V ** 2)))
    c = D ** 2 / (D ** 2 + nu * V ** 2)          # I_AD / I_DD
    return float(np.sum((1 - c) ** 2 / (2 * V ** 2) + c ** 2 * nu / (2 * D ** 2)))


# ----------------------------------------------------------------- estimators

def est_oracle_w(Z: np.ndarray, Dhat: np.ndarray, A: float, D: np.ndarray,
                 nu: float) -> np.ndarray:
    """Proposition 2 with the oracle weights.  Attains 1 / info_eff exactly."""
    pen = 0.0 if not np.isfinite(nu) else D ** 2 / nu
    w = 1.0 / ((A + D) ** 2 + pen)
    return (Z - Dhat) @ w / w.sum()


def est_equal_w(Z: np.ndarray, Dhat: np.ndarray) -> np.ndarray:
    """Prasad-Rao / Fay-Herriot moment estimator: equal weights, unbiased."""
    return (Z - Dhat).mean(axis=1)


def _plug_ml_one(z: np.ndarray, d: np.ndarray, hi: float = 1e6) -> float:
    """Known-D ML profile in A with d substituted for the true variances."""
    def g(A):
        v = A + d
        return float(np.sum((z - v) / v ** 2))
    if g(0.0) <= 0.0:
        return 0.0
    if g(hi) > 0.0:
        return hi
    return float(brentq(g, 0.0, hi, xtol=1e-10, rtol=1e-12))


def est_plug_ml(Z: np.ndarray, Dvar: np.ndarray) -> np.ndarray:
    """Standard practice: substitute the estimated variances and proceed."""
    if Dvar.ndim == 1:                            # true D, shared by all reps
        Dvar = np.broadcast_to(Dvar, Z.shape)
    return np.array([_plug_ml_one(Z[b], Dvar[b]) for b in range(Z.shape[0])])


# ------------------------------------------------------------------ diagnostic

def gate_open(Y: np.ndarray, Dhat: np.ndarray, sG2: np.ndarray) -> np.ndarray:
    """Reliability diagnostic of eq. (14), one coordinate, per replicate."""
    m = Y.shape[1]
    sY2 = Y.var(axis=1, ddof=1)
    sd_v = Dhat.std(axis=1, ddof=1)
    se = np.sqrt(2 * sY2 ** 2 / (m - 1) + (sd_v / np.sqrt(m)) ** 2)
    with np.errstate(divide="ignore", invalid="ignore"):
        diag = np.where(sG2 > 0, se / np.maximum(sG2, 1e-12), np.inf)
    return diag <= TAU, diag


# ------------------------------------------------------------------- one cell

def run(m: int, rho: float, nu: float) -> dict:
    label = f"exp09|{m}|{rho}|{nu}"
    rng = seed_for(label)
    D = np.full(m, A_TRUE * rho ** 2 / (1 - rho ** 2))

    Y = rng.normal(0.0, np.sqrt(A_TRUE + D), size=(REPS, m))
    Z = Y ** 2
    if np.isfinite(nu):
        Dhat = D * rng.chisquare(nu, size=(REPS, m)) / nu
    else:
        Dhat = np.broadcast_to(D, (REPS, m)).copy()

    a_oracle = est_oracle_w(Z, Dhat, A_TRUE, D, nu)
    a_equal = est_equal_w(Z, Dhat)
    a_plug = est_plug_ml(Z, Dhat)

    bound_var = 1.0 / info_eff(A_TRUE, D, nu)
    bias_pred = (4 * rho ** 4 / (nu * (1 - rho ** 2))) if np.isfinite(nu) else 0.0

    open_plug, _ = gate_open(Y, Dhat, np.maximum(a_plug, 0.0))
    open_equal, _ = gate_open(Y, Dhat, np.maximum(a_equal, 0.0))
    open_true, _ = gate_open(Y, Dhat, np.full(REPS, A_TRUE))

    mc = lambda x: float(x.std(ddof=1) / np.sqrt(REPS))
    return dict(
        m=m, rho=rho, nu=(nu if np.isfinite(nu) else -1.0), reps=REPS,
        D=float(D[0]),
        K_naive=float(m),
        K_known=2 * A_TRUE ** 2 * info_known(A_TRUE, D),
        K_eff=k_eff(A_TRUE, D, nu),
        rse_bound=float(np.sqrt(bound_var) / A_TRUE),
        rse_bound_known=float(np.sqrt(1.0 / info_known(A_TRUE, D)) / A_TRUE),
        score_var_check=eff_score_var(A_TRUE, D, nu) / info_eff(A_TRUE, D, nu),
        oracle_bias=float(a_oracle.mean() - A_TRUE), oracle_bias_mc=mc(a_oracle),
        oracle_var_ratio=float(a_oracle.var(ddof=1) / bound_var),
        equal_bias=float(a_equal.mean() - A_TRUE), equal_bias_mc=mc(a_equal),
        equal_var_ratio=float(a_equal.var(ddof=1) / bound_var),
        plug_bias=float(a_plug.mean() - A_TRUE), plug_bias_mc=mc(a_plug),
        plug_bias_pred=bias_pred,
        plug_var_ratio=float(a_plug.var(ddof=1) / bound_var),
        plug_rmse=float(np.sqrt(np.mean((a_plug - A_TRUE) ** 2))),
        equal_rmse=float(np.sqrt(np.mean((a_equal - A_TRUE) ** 2))),
        oracle_rmse=float(np.sqrt(np.mean((a_oracle - A_TRUE) ** 2))),
        plug_at_zero=float((a_plug <= 1e-8).mean()),
        equal_at_zero=float((a_equal <= 0).mean()),
        gate_open_plug=float(open_plug.mean()),
        gate_open_equal=float(open_equal.mean()),
        gate_open_true=float(open_true.mean()),
    )


# ------------------------------------------- replicates are not degrees of freedom

def nu_ceiling(nu_des: float = 20.0) -> pd.DataFrame:
    """Memo section 5: raising B lifts nu_eff to the design ceiling, no further."""
    rows = []
    for B in (10, 25, 50, 100, 250, 1000, 10000, np.inf):
        if np.isinf(B):
            var_ratio = 2.0 / nu_des
        else:
            var_ratio = (1 + 2 / nu_des) * (1 + 2 / B) - 1
        rows.append(dict(nu_des=nu_des, B=(B if np.isfinite(B) else -1),
                         var_Dhat_over_D2=var_ratio, nu_eff=2.0 / var_ratio))
    return pd.DataFrame(rows)


def main() -> None:
    rows = [run(m, rho, nu)
            for m in M_GRID for rho in RHO_GRID for nu in NU_GRID]
    df = pd.DataFrame(rows)
    out = ROOT / "results" / "exp09_estimated_variance.csv"
    df.to_csv(out, index=False)

    ceil = nu_ceiling()
    ceil.to_csv(ROOT / "results" / "exp09_nu_ceiling.csv", index=False)

    fin = df[df.nu > 0]
    manifest = dict(
        experiment="exp09_estimated_variance", reps=REPS,
        m_grid=list(M_GRID), rho_grid=list(RHO_GRID),
        nu_grid=[float(x) for x in NU_GRID[:-1]] + ["inf"],
        cells=len(df),
        p1_score_var_max_dev=float(np.abs(df.score_var_check - 1).max()),
        p2_oracle_var_ratio_range=[float(df.oracle_var_ratio.min()),
                                   float(df.oracle_var_ratio.max())],
        p6_equal_bias_max_z=float((df.equal_bias.abs()
                                   / df.equal_bias_mc).max()),
        p3_plug_bias_positive_share=float((fin.plug_bias > 0).mean()),
        p5_gate_plug_minus_true_max=float((fin.gate_open_plug
                                           - fin.gate_open_true).max()),
    )
    (ROOT / "results" / "exp09_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n")

    pd.set_option("display.width", 200, "display.max_columns", 50)
    print("P1  max |Var(effective score)/I_eff - 1| :",
          f"{manifest['p1_score_var_max_dev']:.2e}")
    print("P2  oracle Var / bound, range           :",
          " to ".join(f"{v:.4f}" for v in manifest["p2_oracle_var_ratio_range"]))
    print("P6  equal-weight bias, max |z|          :",
          f"{manifest['p6_equal_bias_max_z']:.2f}")
    print()
    print("P3/P4  relative bias of the plug-in estimator (A = 1)")
    piv = fin.pivot_table(index=["rho", "nu"], columns="m", values="plug_bias")
    pred = fin.groupby(["rho", "nu"]).plug_bias_pred.first()
    print(piv.assign(predicted=pred).round(4))
    print()
    print("P5  share of replicates with the reliability gate open")
    print(fin.pivot_table(index=["rho", "nu"], columns="m",
                          values=["gate_open_true", "gate_open_plug"])
          .round(3))
    print()
    print("nu_eff ceiling at nu_des = 20")
    print(ceil.round(3).to_string(index=False))
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
