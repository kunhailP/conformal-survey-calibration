"""exp07 - realised widths against the anchor, and whether the anchor holds.

Protocol: docs/PROTOCOL_exp07_widths.md (written before execution).
Requires licensed ESS microdata.

    python experiments/exp07_widths.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments"))

from dac.bands import conformal_quantile  # noqa: E402
import exp03_regional as E  # noqa: E402

OUT = ROOT / "results"
ALPHA, Z = 0.10, 1.645


def radii(dep, v):
    """Realised radii of the three constructions on one calibration set."""
    obs = np.max(np.abs(dep), axis=1)
    anchor = float(conformal_quantile(obs[None, :], ALPHA)[0])
    cons = float(conformal_quantile(
        np.max(np.abs(dep) + Z * v, axis=1)[None, :], ALPHA)[0])
    g = E.gates(dep, v)
    # scale correction: studentise by the guarded scale, place on that scale
    s = dep.std(axis=0)
    s_plug = np.maximum(s, E.FLOOR_FRAC * max(s.max(), 1e-12))
    v2 = v ** 2
    guard = np.maximum(v2.mean(0) - Z * v2.std(0) / np.sqrt(len(dep)), 0.0)
    sT = np.sqrt(np.maximum(s_plug ** 2 - guard, (E.FLOOR_FRAC * s_plug.max()) ** 2))
    q = float(conformal_quantile(
        np.max(np.abs(dep) / s_plug, axis=1)[None, :], ALPHA)[0])
    dec = q * float(sT.mean())
    return anchor, cons, dec, g


def main() -> None:
    d = pd.read_pickle(E.CACHE)
    d = d[d.trstprl.between(0, 10) & d.anweight.gt(0)].copy()
    d["region"] = d.region.astype(str)
    d = d[~d.region.isin(["nan", ""])]
    d = d[d.region.str.upper() != d.cntry.astype(str).str.upper()]

    rng = np.random.default_rng(20260912)
    store = {}
    for (r, c), g in d.groupby(["essround", "cntry"], observed=True):
        if g.region.nunique() < 2:
            continue
        store[(int(r), str(c))] = E.country_departures(g, rng)

    rows, cov_rows = [], []
    for rnd in (9, 10, 11):
        for min_n in (40, 60, 80, 100, 150):
            deps, vs, ctry = [], [], []
            for (r, c), (regions, dep, v, sizes, _) in store.items():
                if r != rnd:
                    continue
                keep = sizes >= min_n
                if keep.sum() >= 2:
                    deps.append(dep[keep]); vs.append(v[keep])
                    ctry += [c] * int(keep.sum())
            if not deps:
                continue
            dep = np.vstack(deps); v = np.vstack(vs); ctry = np.array(ctry)
            ok = np.isfinite(dep).all(1) & np.isfinite(v).all(1)
            dep, v, ctry = dep[ok], v[ok], ctry[ok]
            if len(dep) < 20:
                continue
            a, cn, dc, g = radii(dep, v)
            rows.append(dict(essround=rnd, min_n=min_n, K=len(dep),
                             rho_hat=g["rho_hat"], branch=g["branch"],
                             r_anchor=a, r_conservative=cn, r_correction=dc,
                             corr_over_anchor=dc / a, cons_over_anchor=cn / a,
                             ceiling=1 - np.sqrt(max(1 - g["rho_hat"] ** 2, 0))))

            # leave-one-country-out coverage of the anchor, observed target
            hits, per = [], {}
            for c in np.unique(ctry):
                tr, te = ctry != c, ctry == c
                if tr.sum() < 20 or te.sum() == 0:
                    continue
                q = float(conformal_quantile(
                    np.max(np.abs(dep[tr]), axis=1)[None, :], ALPHA)[0])
                h = (np.max(np.abs(dep[te]), axis=1) <= q)
                hits.append(h); per[c] = float(h.mean())
            if hits:
                allh = np.concatenate(hits)
                cov_rows.append(dict(
                    essround=rnd, min_n=min_n, K=len(dep), n_eval=len(allh),
                    marginal_coverage=float(allh.mean()), nominal=1 - ALPHA,
                    worst_country=float(min(per.values())),
                    p10_country=float(np.percentile(list(per.values()), 10))))

    w = pd.DataFrame(rows); cov = pd.DataFrame(cov_rows)
    w.to_csv(OUT / "exp07_widths.csv", index=False, float_format="%.6g")
    cov.to_csv(OUT / "exp07_anchor_coverage.csv", index=False, float_format="%.6g")
    (OUT / "exp07_manifest.json").write_text(json.dumps({
        "protocol": "docs/PROTOCOL_exp07_widths.md", "alpha": ALPHA}, indent=2) + "\n")

    pd.set_option("display.width", 200)
    print("(a) REALISED RADII, ratios to the observed anchor\n")
    print(w[["essround", "min_n", "K", "rho_hat", "branch", "corr_over_anchor",
             "cons_over_anchor", "ceiling"]].round(4).to_string(index=False))
    print(f"\n  correction / anchor: median {w.corr_over_anchor.median():.3f}, "
          f"range {w.corr_over_anchor.min():.3f}-{w.corr_over_anchor.max():.3f}")
    print(f"  conservative / anchor: median {w.cons_over_anchor.median():.3f}")
    act = w[w.branch == "deconvolution"]
    if len(act):
        print(f"  where the correction activates: "
              f"{act.corr_over_anchor.min():.3f}-{act.corr_over_anchor.max():.3f} "
              f"of the anchor")

    print("\n(b) ANCHOR, leave-one-country-out coverage of the OBSERVED target\n")
    print(cov.round(4).to_string(index=False))
    print(f"\n  marginal coverage: median {cov.marginal_coverage.median():.4f} "
          f"against nominal {1-ALPHA}")
    print(f"  below nominal in {(cov.marginal_coverage < 0.9).sum()} of {len(cov)}")


if __name__ == "__main__":
    main()
