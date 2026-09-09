"""exp03 - regional transport under corrected resampling.

Protocol: docs/PROTOCOL_exp03_regional.md (written before execution).
Requires licensed ESS microdata; see docs/DATA.md.

The resampling unit is (stratum, psu), so a PSU straddling regions is carried
whole into every replicate.  Rao-Wu-Yue rescaling is the default.

    python experiments/exp03_regional.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from dac.survey import replicate_weights, weighted_cdf  # noqa: E402

CACHE = ROOT / "data" / "ess_r9_11.pkl"
OUT = ROOT / "results"

B = 400
THRESHOLDS = np.arange(0, 10)          # F(t) = P(trstprl <= t), d = 10
MIN_N_GRID = (40, 60, 80, 100, 150)
ROUNDS = (9, 10, 11)
Z = 1.645
RHO_0, DELTA_MAX, A_UCB, B_UCB = 0.47, 0.02, 0.0061, 0.0943
TAU_D = (DELTA_MAX - A_UCB) / B_UCB


def country_departures(g: pd.DataFrame, rng, rescaled=True):
    """Regional departures and their design SDs for one country-round."""
    y = g.trstprl.to_numpy()
    ind = (y[:, None] <= THRESHOLDS[None, :]).astype(np.float64)
    w = g.anweight.to_numpy(dtype=np.float64)
    reg, regions = pd.factorize(g.region.to_numpy())
    nat = np.zeros(len(g), dtype=np.int64)

    point_g = weighted_cdf(ind, w, reg, len(regions))
    point_n = weighted_cdf(ind, w, nat, 1)[0]
    dep = point_g - point_n[None, :]

    W, n_single = replicate_weights(g.stratum.to_numpy(), g.psu.to_numpy(),
                                    w, B, rng, rescaled=rescaled)
    rep_g = weighted_cdf(ind, W, reg, len(regions))       # (G, T, B)
    rep_n = weighted_cdf(ind, W, nat, 1)                  # (1, T, B)
    rep_dep = rep_g - rep_n
    v = np.nanstd(rep_dep, axis=2, ddof=1)                # (G, T)
    sizes = np.bincount(reg, minlength=len(regions))
    return regions, dep, v, sizes, n_single


def gates(dep: np.ndarray, v: np.ndarray):
    """Diagnostics and gate decisions for a pooled set of regional departures."""
    K = dep.shape[0]
    s_plug2 = dep.var(axis=0, ddof=1)                     # between-region
    v2 = v ** 2
    vbar2 = v2.mean(axis=0)
    se_vbar2 = v2.std(axis=0, ddof=1) / np.sqrt(K)

    # rho: t-averaged LCB on mean design variance over t-averaged UCB on total
    lcb_v = max(vbar2.mean() - Z * se_vbar2.mean() / np.sqrt(len(vbar2)), 0.0)
    ucb_s = s_plug2.mean() * (1.0 + Z * np.sqrt(2.0 / (K - 1)))
    rho_hat = float(np.sqrt(vbar2.mean() / s_plug2.mean()))
    rho_lcb = float(np.sqrt(lcb_v / ucb_s))

    guard = np.maximum(vbar2 - Z * se_vbar2, 0.0)
    floor = 0.01 * s_plug2
    sT2 = np.maximum(s_plug2 - guard, floor)
    term_sampling = np.sqrt(2 * s_plug2 ** 2 / (K - 1))   # the K-floor term
    term_hetero = se_vbar2                                # dispersion of design variances
    se_sT2 = np.sqrt(term_sampling ** 2 + term_hetero ** 2)
    D = float(np.max(se_sT2 / sT2))
    j = int(np.argmax(se_sT2 / sT2))
    delta = A_UCB + B_UCB * D

    gate_a = rho_lcb > RHO_0
    gate_b = delta <= DELTA_MAX
    return dict(K=K, rho_hat=rho_hat, rho_lcb=rho_lcb, D=D, delta_ucb=delta,
                gate_A=bool(gate_a), gate_B=bool(gate_b),
                K_floor=float(np.sqrt(2.0 / (K - 1))),
                D_sampling_only=float(np.max(term_sampling / sT2)),
                hetero_share_of_D2=float(term_hetero[j] ** 2 / se_sT2[j] ** 2),
                design_var_spread=float(np.max(v2.max(axis=0) / np.maximum(v2.min(axis=0), 1e-30))),
                branch="deconvolution" if (gate_a and gate_b)
                else ("conservative" if gate_a else "anchor"),
                scale_ratio=float(np.sqrt(sT2.mean() / s_plug2.mean())))


def main() -> None:
    d = pd.read_pickle(CACHE)
    d = d[d.trstprl.between(0, 10) & d.anweight.gt(0)].copy()
    d["region"] = d.region.astype(str)
    d = d[~d.region.isin(["nan", ""])]
    # a country whose region code equals its country code has no regional variation
    d = d[d.region.str.upper() != d.cntry.astype(str).str.upper()]

    audit = pd.read_csv(OUT / "exp02_design_audit.csv")
    degenerate = set(map(tuple, audit.loc[audit.psu_equals_idno | audit.psu_constant,
                                          ["essround", "cntry"]].to_numpy()))
    splitting = set(map(tuple, audit.loc[audit.psu_split_across_regions > 0,
                                         ["essround", "cntry"]].to_numpy()))

    rng = np.random.default_rng(20260909)
    store = {}
    for (rnd, cty), g in d.groupby(["essround", "cntry"], observed=True):
        if g.region.nunique() < 2:
            continue
        regions, dep, v, sizes, ns = country_departures(g, rng)
        store[(int(rnd), str(cty))] = (regions, dep, v, sizes, ns)

    rows = []
    for pool in ("all countries", "clustered PSU only"):
        for rnd in ROUNDS:
            for min_n in MIN_N_GRID:
                deps, vs, ncty, nsplit = [], [], 0, 0
                for (r, c), (regions, dep, v, sizes, ns) in store.items():
                    if r != rnd:
                        continue
                    if pool == "clustered PSU only" and (r, c) in degenerate:
                        continue
                    keep = sizes >= min_n
                    if keep.sum() < 2:
                        continue
                    deps.append(dep[keep]); vs.append(v[keep])
                    ncty += 1
                    nsplit += int((r, c) in splitting)
                if not deps:
                    continue
                dep_all = np.vstack(deps); v_all = np.vstack(vs)
                ok = np.isfinite(dep_all).all(1) & np.isfinite(v_all).all(1)
                dep_all, v_all = dep_all[ok], v_all[ok]
                if dep_all.shape[0] < 3:
                    continue
                res = gates(dep_all, v_all)
                res.update(pool=pool, essround=rnd, min_n=min_n,
                           n_countries=ncty, n_split_countries=nsplit)
                rows.append(res)

    out = pd.DataFrame(rows)[["pool", "essround", "min_n", "K", "n_countries",
                              "n_split_countries", "rho_hat", "rho_lcb", "D",
                              "delta_ucb", "gate_A", "gate_B", "branch",
                              "K_floor", "D_sampling_only", "hetero_share_of_D2",
                              "design_var_spread", "scale_ratio"]]
    OUT.mkdir(exist_ok=True)
    out.to_csv(OUT / "exp03_regional.csv", index=False, float_format="%.6g")
    (OUT / "exp03_manifest.json").write_text(json.dumps({
        "protocol": "docs/PROTOCOL_exp03_regional.md",
        "resample_unit": "(stratum, psu)", "bootstrap": "Rao-Wu-Yue rescaled",
        "B": B, "d": len(THRESHOLDS), "estimand": "region minus own nation, trstprl",
        "frozen": {"rho_0": RHO_0, "delta_max": DELTA_MAX, "tau_D": round(TAU_D, 4),
                   "K_floor": int(np.ceil(1 + 2 / TAU_D ** 2))},
    }, indent=2) + "\n")

    pd.set_option("display.width", 200)
    print(out.to_string(index=False))
    print(f"\nactivations (deconvolution): {(out.branch == 'deconvolution').sum()} "
          f"of {len(out)} configurations")
    print(f"gate A opened: {out.gate_A.sum()}   gate B opened: {out.gate_B.sum()}")
    print(f"\nK-floor cleared in {(out.K_floor <= TAU_D).sum()} of {len(out)} configurations,"
          f" yet gate B opened in {out.gate_B.sum()}.")
    print(f"median share of D^2 from design-variance heterogeneity: "
          f"{out.hetero_share_of_D2.median():.1%}")
    print(f"configurations that would pass with homogeneous design variances: "
          f"{(out.D_sampling_only <= TAU_D).sum()} of {len(out)}")


if __name__ == "__main__":
    main()
