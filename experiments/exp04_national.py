"""exp04 - national unit design shares, recomputed under correct resampling.

Protocol: docs/PROTOCOL_exp04_national.md (written before execution).
Requires licensed ESS microdata; see docs/DATA.md.

    python experiments/exp04_national.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments"))

from dac.survey import replicate_weights, weighted_cdf  # noqa: E402
from exp03_regional import THRESHOLDS, B, gates  # noqa: E402

CACHE = ROOT / "data" / "ess_r9_11.pkl"
OUT = ROOT / "results"
#: Subgroup scan.  The inherited national maximum of 0.29 came from a scan of
#: this kind, not from full samples: smaller subsamples carry larger design
#: variance, so the two numbers are not comparable unless the scan is repeated.
SUBGROUPS = {
    "all": lambda g: g,
    "age 15-29": lambda g: g[g.agea.between(15, 29)],
    "age 30-44": lambda g: g[g.agea.between(30, 44)],
    "age 45-59": lambda g: g[g.agea.between(45, 59)],
    "age 60+": lambda g: g[g.agea >= 60],
}
MIN_N_SCAN = (200, 400, 800)


def country_curve(g: pd.DataFrame, rng):
    """National CDF and its design SD for one country-round."""
    y = g.trstprl.to_numpy()
    ind = (y[:, None] <= THRESHOLDS[None, :]).astype(np.float64)
    w = g.anweight.to_numpy(dtype=np.float64)
    one = np.zeros(len(g), dtype=np.int64)
    point = weighted_cdf(ind, w, one, 1)[0]
    W, _ = replicate_weights(g.stratum.to_numpy(), g.psu.to_numpy(), w, B, rng)
    rep = weighted_cdf(ind, W, one, 1)[0]          # (T, B)
    return point, rep.std(axis=1, ddof=1)


def main() -> None:
    d = pd.read_pickle(CACHE)
    d = d[d.trstprl.between(0, 10) & d.anweight.gt(0)].copy()

    rng = np.random.default_rng(20260910)
    curves: dict[tuple[int, str], tuple[np.ndarray, np.ndarray]] = {}
    for (rnd, cty), g in d.groupby(["essround", "cntry"], observed=True):
        if len(g) < 200:
            continue
        curves[(int(rnd), str(cty))] = country_curve(g, rng)

    rows = []
    # per-round, d = 10
    for rnd in (9, 10, 11):
        sel = {c: v for (r, c), v in curves.items() if r == rnd}
        if len(sel) < 5:
            continue
        F = np.vstack([v[0] for v in sel.values()])
        V = np.vstack([v[1] for v in sel.values()])
        dev = F - F.mean(axis=0, keepdims=True)
        res = gates(dev, V)
        res.update(unit="national", structure="per-round", essround=rnd,
                   d=len(THRESHOLDS), n_countries=len(sel))
        rows.append(res)

    # trajectory, rounds 9-11 stacked, d = 30
    common = sorted({c for (r, c) in curves} &
                    {c for (r, c) in curves if r == 9} &
                    {c for (r, c) in curves if r == 10} &
                    {c for (r, c) in curves if r == 11})
    if len(common) >= 5:
        F = np.vstack([np.concatenate([curves[(r, c)][0] for r in (9, 10, 11)])
                       for c in common])
        V = np.vstack([np.concatenate([curves[(r, c)][1] for r in (9, 10, 11)])
                       for c in common])
        dev = F - F.mean(axis=0, keepdims=True)
        res = gates(dev, V)
        res.update(unit="national", structure="trajectory 9-11", essround=0,
                   d=3 * len(THRESHOLDS), n_countries=len(common))
        rows.append(res)

    # subgroup scan, matching the construction behind the inherited maximum
    for name, sub in SUBGROUPS.items():
        for min_n in MIN_N_SCAN:
            for rnd in (9, 10, 11):
                sel = {}
                for (r, cty), g in d.groupby(["essround", "cntry"], observed=True):
                    if int(r) != rnd:
                        continue
                    gg = sub(g)
                    if len(gg) < min_n or gg.psu.nunique() < 5:
                        continue
                    sel[str(cty)] = country_curve(gg, rng)
                if len(sel) < 5:
                    continue
                F = np.vstack([v[0] for v in sel.values()])
                V = np.vstack([v[1] for v in sel.values()])
                res = gates(F - F.mean(axis=0, keepdims=True), V)
                res.update(unit="national", structure=f"scan {name} min_n={min_n}",
                           essround=rnd, d=len(THRESHOLDS), n_countries=len(sel))
                rows.append(res)

    out = pd.DataFrame(rows)[["unit", "structure", "essround", "d", "n_countries",
                              "K", "rho_hat", "rho_lcb", "D", "delta_ucb",
                              "gate_A", "gate_B", "branch", "K_floor",
                              "D_sampling_only", "hetero_share_of_D2",
                              "design_var_spread"]]
    OUT.mkdir(exist_ok=True)
    out.to_csv(OUT / "exp04_national.csv", index=False, float_format="%.6g")
    (OUT / "exp04_manifest.json").write_text(json.dumps({
        "protocol": "docs/PROTOCOL_exp04_national.md",
        "bootstrap": "Rao-Wu-Yue rescaled", "resample_unit": "(stratum, psu)",
        "B": B, "estimand": "country deviation from cross-country mean, trstprl",
    }, indent=2) + "\n")

    pd.set_option("display.width", 220)
    print(out.to_string(index=False))
    full = out[~out.structure.str.startswith("scan")]
    scan = out[out.structure.str.startswith("scan")]
    print(f"\ninherited national maximum was rho_hat <= 0.29, from a subgroup scan")
    print(f"recomputed, full samples : rho_hat {full.rho_hat.min():.3f} - {full.rho_hat.max():.3f}")
    print(f"recomputed, subgroup scan: rho_hat {scan.rho_hat.min():.3f} - "
          f"{scan.rho_hat.max():.3f}  ({len(scan)} cells)")
    worst = scan.loc[scan.rho_hat.idxmax()]
    print(f"  worst scan cell: {worst.structure}, round {worst.essround}, "
          f"K={worst.K}, rho_hat={worst.rho_hat:.3f}, rho_LCB={worst.rho_lcb:.3f}")
    print(f"  its D = {worst.D:.3f} vs K-floor {worst.K_floor:.3f}; "
          f"heterogeneity share of D^2 = {worst.hetero_share_of_D2:.1%}")
    print(f"need gate (rho_0 = 0.47) opened: {out.gate_A.sum()} of {len(out)}")
    print(f"reliability gate opened:         {out.gate_B.sum()} of {len(out)}")


if __name__ == "__main__":
    main()
