"""exp21 - matched information first, then paying for the structure.

Protocol: docs/PROTOCOL_exp21_estimated_structure.md (written before execution).
Specification: docs/THEORY_ratio_pivot.md section 3, route (b).

exp20's 9-20 percent mixed two effects: pooling (a known relative structure
removes the need for K simultaneous limits) and direct ratio inference (not
bounding A above and D below separately).  A third arm given the SAME known a_c
but still bounding components separately isolates the second.

Then the structure is estimated, and its uncertainty is paid for with a
confidence set rather than removed by substituting a_c(gamma-hat).

    python experiments/exp21_estimated_structure.py
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

REPS = 10000
A_TRUE, GAMMA0 = 1.0, 1.0
ALPHA0 = 0.05
ETA = 0.05                       # arms with a known structure
ETA_G = ETA_T = ETA / 2          # C_gamma arm: split the same total
GRID, GRID_FINE = 31, 61
NULL_DRAWS = 200000


def seed_for(label):
    return np.random.default_rng(
        int.from_bytes(hashlib.sha256(label.encode()).digest()[:8], "little"))


def a_of(x, gamma):
    """Relative structure, normalised to mean one so d and gamma do not confound."""
    v = x ** (-gamma)
    return v / v.mean(axis=-1, keepdims=True)


def band_at(absY, a, t, m):
    if np.ndim(t) == 0:
        t = np.full(absY.shape[0], t)
    return np.sort(absY / np.sqrt(1.0 + t[:, None] * a), axis=1)[:, m - 1]


def t_lower(Y2, a, dhat, K, nu, eta):
    """Exact one-sided lower bound for t = d/A; fallback t_L = 0 on an empty set."""
    q = float(fdist.ppf(1.0 - eta, nu, K))
    T = lambda t: K * dhat / np.maximum(
        t * (Y2 / (1.0 + t[:, None] * a)).sum(1), 1e-300)
    empty = (K * dhat / np.maximum((Y2 / a).sum(1), 1e-300)) > q
    lo, hi = np.full(Y2.shape[0], 1e-8), np.full(Y2.shape[0], 1e8)
    for _ in range(80):
        mid = np.sqrt(lo * hi)
        below = T(mid) <= q
        hi = np.where(below, mid, hi)
        lo = np.where(below, lo, mid)
    return np.where(empty, 0.0, np.sqrt(lo * hi)), empty


def A_upper(Y2, vL2, K, eta1):
    q = float(chi2.ppf(eta1, K))
    lo, hi = np.zeros(Y2.shape[0]), np.full(Y2.shape[0], 1e4)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        below = (Y2 / (mid[:, None] + vL2)).sum(1) < q
        hi = np.where(below, mid, hi)
        lo = np.where(below, lo, mid)
    return 0.5 * (lo + hi)


def null_w(x, nu_c, eta_g, rng):
    """Quantile of |W| under H0.  Its law depends on neither d nor gamma."""
    lx = np.log(x); lxc = lx - lx.mean()
    sig = np.sqrt(polygamma(1, nu_c[0] / 2.0))
    c = lxc / (sig * np.sqrt((lxc ** 2).sum()))
    eps = np.log(rng.chisquare(nu_c, size=(NULL_DRAWS, len(x))) / nu_c)
    return float(np.quantile(np.abs(eps @ c), 1.0 - eta_g)), sig, float((lxc ** 2).sum())


def run(K, d_over_A, nu0, sig_mis):
    rng = seed_for(f"exp21|{K}|{d_over_A}|{nu0}|{sig_mis}")
    x = rng.lognormal(0.0, 0.7, size=K)
    nu_c = np.full(K, float(nu0)); nu = float(nu_c.sum())
    a_true = a_of(x, GAMMA0)
    if sig_mis > 0:
        a_true = a_true * rng.lognormal(0.0, sig_mis, size=K)
        a_true = a_true / a_true.mean()
    d = A_TRUE * d_over_A
    D = d * a_true
    t0 = d / A_TRUE
    m = conformal_rank(K, ALPHA0)

    Y = rng.normal(0.0, np.sqrt(A_TRUE + D), size=(REPS, K))
    absY, Y2 = np.abs(Y), Y ** 2
    Dhat = D * rng.chisquare(nu_c, size=(REPS, K)) / nu_c
    G = rng.normal(0.0, np.sqrt(A_TRUE), size=REPS)

    band = {"oracle": band_at(absY, a_true, t0, m),
            "uncorrected": np.sort(absY, axis=1)[:, m - 1]}

    # incumbent: per-population lower limits with a Bonferroni correction
    vL_b = nu_c * Dhat / chi2.ppf(1.0 - (ETA / 2) / K, nu_c)
    AU_b = A_upper(Y2, vL_b, K, ETA / 2)
    band["sep_bonf"] = np.sort(
        absY / np.sqrt(1.0 + vL_b / np.maximum(AU_b, 1e-12)[:, None]), axis=1)[:, m - 1]

    # matched information: same known a_c, still bounding components separately
    dhat_k = (nu_c * Dhat / a_true).sum(1) / nu
    dL = nu * dhat_k / chi2.ppf(1.0 - ETA / 2, nu)
    vL_s = dL[:, None] * a_true
    AU_s = A_upper(Y2, vL_s, K, ETA / 2)
    band["sep_struct"] = np.sort(
        absY / np.sqrt(1.0 + vL_s / np.maximum(AU_s, 1e-12)[:, None]), axis=1)[:, m - 1]

    # ratio bound with the structure known
    tL_k, empty_k = t_lower(Y2, a_true, dhat_k, K, nu, ETA)
    band["ratio_known"] = band_at(absY, a_true, tL_k, m)

    # --- structure estimated -------------------------------------------
    lx = np.log(x); lxc = lx - lx.mean()
    w, sig_eps, Sxx = null_w(x, nu_c, ETA_G, seed_for(f"exp21null|{K}|{nu0}"))
    ghat = -(np.log(Dhat) @ lxc) / Sxx
    half = w * sig_eps / np.sqrt(Sxx)
    gL, gU = ghat - half, ghat + half

    def ratio_band_at_gamma(g):
        ag = a_of(x, g[:, None]) if np.ndim(g) else a_of(x, g)
        dh = (nu_c * Dhat / ag).sum(1) / nu
        tl, _ = t_lower(Y2, ag, dh, K, nu, ETA_T)
        return np.sort(absY / np.sqrt(1.0 + tl[:, None] * ag), axis=1)[:, m - 1]

    tL_p, empty_p = t_lower(Y2, a_of(x, ghat[:, None]), 
                            (nu_c * Dhat / a_of(x, ghat[:, None])).sum(1) / nu,
                            K, nu, ETA)
    ap = a_of(x, ghat[:, None])
    band["plugin_gamma"] = np.sort(
        absY / np.sqrt(1.0 + tL_p[:, None] * ap), axis=1)[:, m - 1]

    def sup_over_C(npts):
        u = np.linspace(0.0, 1.0, npts)
        best = np.zeros(REPS)
        for uu in u:
            best = np.maximum(best, ratio_band_at_gamma(gL + uu * (gU - gL)))
        return best
    band["Cgamma"] = sup_over_C(GRID)
    fine = sup_over_C(GRID_FINE)

    hit = lambda b: float((np.abs(G) <= b).mean())
    out = dict(K=K, d_over_A=d_over_A, nu_per_pop=nu0, sig_mis=sig_mis,
               reps=REPS, nu_total=nu, m=m, nominal=m / (K + 1.0), t_true=t0,
               w_crit=w, mc_se=float(np.sqrt(.95 * .05 / REPS)),
               Cgamma_set_cov=float(((gL <= GAMMA0) & (GAMMA0 <= gU)).mean()),
               Cgamma_halfwidth=float(half),
               empty_known=float(empty_k.mean()),
               empty_plugin=float(empty_p.mean()),
               grid_sensitivity=float(np.mean(fine / band["Cgamma"]) - 1.0))
    for nm, b in band.items():
        out[f"{nm}_cov"] = hit(b)
        out[f"{nm}_w"] = float(b.mean())
        if nm != "oracle":
            out[f"{nm}_contain"] = float((b >= band["oracle"]).mean())
            out[f"{nm}_over_oracle"] = float(np.mean(b / band["oracle"]))
    av = out["uncorrected_over_oracle"] - 1.0
    for nm in ("sep_bonf", "sep_struct", "ratio_known", "plugin_gamma", "Cgamma"):
        out[f"captured_{nm}"] = float((av - (out[f"{nm}_over_oracle"] - 1)) / av)
    out["ratio_over_sepstruct"] = float(out["ratio_known_w"] / out["sep_struct_w"])
    out["Cgamma_over_ratio"] = float(out["Cgamma_w"] / out["ratio_known_w"])
    out["Cgamma_over_sepbonf"] = float(out["Cgamma_w"] / out["sep_bonf_w"])
    return out


def main():
    rows = [run(K, da, nu0, sm) for K in (60, 200) for da in (0.5, 1.0)
            for nu0 in (8, 16) for sm in (0.0, 0.4)]
    df = pd.DataFrame(rows)
    out = ROOT / "results" / "exp21_estimated_structure.csv"
    df.to_csv(out, index=False)
    ok, mis = df[df.sig_mis == 0], df[df.sig_mis > 0]
    (ROOT / "results" / "exp21_manifest.json").write_text(json.dumps(dict(
        experiment="exp21_estimated_structure", reps=REPS, cells=len(df),
        alpha0=ALPHA0, eta=ETA, eta_gamma=ETA_G, eta_t=ETA_T,
        grid=GRID, grid_fine=GRID_FINE,
        u1_Cgamma_set_cov=[float(ok.Cgamma_set_cov.min()),
                           float(ok.Cgamma_set_cov.max())],
        u3_ratio_over_sepstruct=[float(ok.ratio_over_sepstruct.min()),
                                 float(ok.ratio_over_sepstruct.max())],
        u4_Cgamma_contain=[float(ok.Cgamma_contain.min()),
                           float(ok.Cgamma_contain.max())],
        u5_plugin_contain=[float(ok.plugin_gamma_contain.min()),
                           float(ok.plugin_gamma_contain.max())],
        u6_mis_Cgamma_contain=[float(mis.Cgamma_contain.min()),
                               float(mis.Cgamma_contain.max())],
        grid_sensitivity_max=float(df.grid_sensitivity.abs().max()),
    ), indent=2) + "\n")

    pd.set_option("display.width", 250, "display.max_columns", 70)
    lab = ["K", "d_over_A", "nu_per_pop"]
    for tag, sub in (("CORRECTLY SPECIFIED", ok), ("MISSPECIFIED structure", mis)):
        print(f"\n########## {tag}")
        print("1. C_gamma coverage (nominal 0.975) and its half-width")
        print(sub.set_index(lab)[["Cgamma_set_cov", "Cgamma_halfwidth", "w_crit",
                                  "empty_known", "empty_plugin",
                                  "grid_sensitivity"]].round(4).to_string())
        print("\n2. containment of the oracle half-width")
        print(sub.set_index(lab)[["sep_bonf_contain", "sep_struct_contain",
                                  "ratio_known_contain", "plugin_gamma_contain",
                                  "Cgamma_contain"]].round(4).to_string())
        print("\n3. latent-target coverage, guaranteed 0.90")
        print(sub.set_index(lab)[["oracle_cov", "sep_bonf_cov", "sep_struct_cov",
                                  "ratio_known_cov", "plugin_gamma_cov",
                                  "Cgamma_cov"]].round(4).to_string())
        print("\n4. width over the oracle band, and the isolating ratios")
        print(sub.set_index(lab)[["uncorrected_over_oracle", "sep_bonf_over_oracle",
                                  "sep_struct_over_oracle", "ratio_known_over_oracle",
                                  "plugin_gamma_over_oracle", "Cgamma_over_oracle",
                                  "ratio_over_sepstruct", "Cgamma_over_sepbonf"]]
              .round(4).to_string())
        print("\n5. share of the available narrowing captured")
        print(sub.set_index(lab)[["captured_sep_bonf", "captured_sep_struct",
                                  "captured_ratio_known", "captured_plugin_gamma",
                                  "captured_Cgamma"]].round(4).to_string())
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
