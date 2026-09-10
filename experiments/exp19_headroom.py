"""exp19 - is there headroom for a joint-inference candidate, and where?

Protocol: docs/PROTOCOL_exp19_headroom.md (written before execution).
NO method is proposed or added.  The same band function is evaluated at mixed
arguments to locate where the width is lost.

    python experiments/exp19_headroom.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments"))
from dac.bands import conformal_rank                        # noqa: E402
import exp18_regional_share as E                            # noqa: E402

REPS = 2000


def band(absY, D, A, m):
    """R(A, D) = ord_m { |Y_c| / sqrt(1 + D_c / A) }, the shared band function."""
    return np.sort(absY / np.sqrt(1.0 + D / np.maximum(A, E.FLOOR)[:, None]),
                   axis=1)[:, m - 1]


def run(route, level, t0_q, K):
    m_samp, n_unit = E.SMALL[level] if route == "small_sample" else E.BASE
    nu = E.H * (m_samp - 1)
    tau = E.TAU0 if route == "small_sample" else E.tau_for(
        t0_q, E.calibrate(t0_q, E.TAU0, *E.SMALL[level], "fix")[3], *E.BASE)
    t0, mu, A, share = E.calibrate(t0_q, tau, m_samp, n_unit, "fix")

    rng = E.seed_for(f"exp18|{route}|{level}|{t0_q}|{K}")   # same stream as exp18
    z = E.psu_means(rng, REPS * (K + 1), t0, tau, n_unit)
    Ftrue = z.mean(axis=(1, 2)).reshape(REPS, K + 1)
    Dtrue = E.true_D(z, m_samp).reshape(REPS, K + 1)
    Fh, Dh_all = E.draw_sample(rng, z, m_samp)
    Fh, Dh_all = Fh.reshape(REPS, K + 1), Dh_all.reshape(REPS, K + 1)

    Y = Fh[:, :K] - mu
    absY, Dc = np.abs(Y), Dtrue[:, :K]
    Dh = np.maximum(Dh_all[:, :K], E.FLOOR)
    Gnew = Ftrue[:, K] - mu
    m = conformal_rank(K, E.ALPHA0)

    # the two lower-limit variants: with and without the Bonferroni factor
    vL_bonf = nu * Dh / chi2.ppf(1.0 - E.ETA2 / K, nu)
    vL_marg = nu * Dh / chi2.ppf(1.0 - E.ETA2, nu)
    AU_bonf = E.pivot_AU(Y, vL_bonf, K, False)
    AU_marg = E.pivot_AU(Y, vL_marg, K, False)

    ev = {
        "oracle":        band(absY, Dc, np.full(REPS, A), m),
        "boundA_only":   band(absY, Dc, AU_bonf, m),
        "boundD_only":   band(absY, vL_bonf, np.full(REPS, A), m),
        "current":       band(absY, vL_bonf, AU_bonf, m),
        "no_multiplicity": band(absY, vL_marg, AU_marg, m),
        "uncorrected":   np.sort(absY, axis=1)[:, m - 1],
    }
    out = dict(route=route, level=level, t0_q=t0_q, K=K, reps=REPS, nu=nu,
               Dbar_over_A=share, A=A, m=m, nominal=m / (K + 1.0),
               vL_bonf_cov=float((vL_bonf <= Dc).all(axis=1).mean()),
               vL_marg_cov=float((vL_marg <= Dc).all(axis=1).mean()),
               mc_se=float(np.sqrt(.9 * .1 / REPS)))
    for nm, bd in ev.items():
        out[f"{nm}_over_oracle"] = float(np.mean(bd / ev["oracle"]))
        out[f"{nm}_cov"] = float((np.abs(Gnew) <= bd).mean())
    tot = out["uncorrected_over_oracle"] - 1.0
    out["loss_boundA"] = out["boundA_only_over_oracle"] - 1.0
    out["loss_boundD"] = out["boundD_only_over_oracle"] - 1.0
    out["loss_current"] = out["current_over_oracle"] - 1.0
    out["loss_no_mult"] = out["no_multiplicity_over_oracle"] - 1.0
    out["available"] = tot
    out["mult_share_of_current_loss"] = (
        (out["loss_current"] - out["loss_no_mult"]) / out["loss_current"]
        if out["loss_current"] > 0 else float("nan"))
    out["captured_now"] = (tot - out["loss_current"]) / tot if tot > 0 else float("nan")
    out["captured_no_mult"] = (tot - out["loss_no_mult"]) / tot if tot > 0 else float("nan")
    return out


def main():
    rows = [run(r, "S2", q, K) for r in ("low_signal", "small_sample")
            for q in (0.50, 0.15) for K in (60, 200)]
    df = pd.DataFrame(rows)
    out = ROOT / "results" / "exp19_headroom.csv"
    df.to_csv(out, index=False)
    (ROOT / "results" / "exp19_manifest.json").write_text(json.dumps(dict(
        experiment="exp19_headroom", reps=REPS, cells=len(df),
        z1_loss_boundA=[float(df.loss_boundA.min()), float(df.loss_boundA.max())],
        z1_loss_boundD=[float(df.loss_boundD.min()), float(df.loss_boundD.max())],
        z2_mult_share=[float(df.mult_share_of_current_loss.min()),
                       float(df.mult_share_of_current_loss.max())],
        z3_captured_now=[float(df.captured_now.min()), float(df.captured_now.max())],
        z3_captured_no_mult=[float(df.captured_no_mult.min()),
                             float(df.captured_no_mult.max())],
    ), indent=2) + "\n")

    pd.set_option("display.width", 240, "display.max_columns", 60)
    lab = ["route", "t0_q", "K"]
    print("=== where the width is lost: same band function, mixed arguments")
    print("    (all as width over the oracle band)")
    print(df.set_index(lab)[["Dbar_over_A", "uncorrected_over_oracle",
                             "boundA_only_over_oracle", "boundD_only_over_oracle",
                             "current_over_oracle", "no_multiplicity_over_oracle"]]
          .round(4).to_string())
    print("\n=== Z1/Z2/Z3")
    print(df.set_index(lab)[["loss_boundA", "loss_boundD", "loss_current",
                             "loss_no_mult", "mult_share_of_current_loss",
                             "captured_now", "captured_no_mult"]].round(4).to_string())
    print("\n=== validity of the two lower-limit variants (requirement 0.975)")
    print(df.set_index(lab)[["vL_bonf_cov", "vL_marg_cov", "oracle_cov",
                             "current_cov", "no_multiplicity_cov"]].round(4).to_string())
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
