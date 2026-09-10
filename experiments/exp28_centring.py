"""exp28 - the centring-variance mismatch on ESS, measured rather than noted.

Protocol: docs/PROTOCOL_exp28_centring.md (written before execution).
No new method.  exp27 scores Y_cr = Fhat_cr - Fhat_c but uses the design
variance of Fhat_cr alone.  Here the Taylor linearisation of the deviation is
used instead, and the dependence a common estimated centre induces across
regions is measured.

    ESS_CACHE=<dir> python experiments/exp28_centring.py
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments"))
import exp27_ess_scalar as E                                # noqa: E402

T0, ITEMS, ROUNDS, MIN_N = E.T0, E.ITEMS, E.ROUNDS, E.MIN_N


def country_round(gc: pd.DataFrame, item: str) -> list[dict]:
    """Deviation variances and the cross-region covariance they induce."""
    w = gc.anweight.to_numpy(float)
    z = (gc[item].to_numpy(float) <= T0).astype(float)
    Wc = w.sum()
    Fc = float((w * z).sum() / Wc)
    h = gc.stratum.to_numpy(); p = gc.psu.to_numpy()
    reg = gc.region.to_numpy()
    key = pd.MultiIndex.from_arrays([h, p])
    strata = pd.unique(h)
    regions = pd.unique(reg)

    # influence function of each region's deviation, aggregated to PSU totals
    U = {}
    meta = {}
    for r in regions:
        m = reg == r
        Wr = w[m].sum()
        if Wr <= 0:
            continue
        Fr = float((w[m] * z[m]).sum() / Wr)
        u = np.where(m, w * (z - Fr) / Wr, 0.0) - w * (z - Fc) / Wc
        tot = pd.Series(u, index=key).groupby(level=[0, 1], sort=False).sum()
        U[r] = tot
        n_psu_r = int(pd.unique(p[m]).size)
        n_str_r = int(pd.unique(h[m]).size)
        meta[r] = dict(F=Fr, Y=Fr - Fc, n=int(m.sum()), Wshare=float(Wr / Wc),
                       nu=n_psu_r - n_str_r, n_psu=n_psu_r, n_strata=n_str_r)
    if not U:
        return []
    idx = sorted(set().union(*[set(v.index) for v in U.values()]))
    M = pd.DataFrame({r: U[r].reindex(idx, fill_value=0.0) for r in U})
    hh = np.array([i[0] for i in idx])

    # stratified ultimate-cluster covariance of the PSU totals
    S = np.zeros((M.shape[1], M.shape[1]))
    for s in strata:
        V = M.to_numpy()[hh == s]
        m_ = V.shape[0]
        if m_ > 1:
            C = V - V.mean(0, keepdims=True)
            S += m_ / (m_ - 1.0) * (C.T @ C)
    cols = list(M.columns)
    out = []
    dg = np.diag(S)
    for i, r in enumerate(cols):
        out.append(dict(region=str(r), D_dev=float(dg[i]), **meta[r]))
    # induced within-country correlation among distinct regions
    if len(cols) > 1:
        sd = np.sqrt(np.maximum(dg, 1e-300))
        R = S / np.outer(sd, sd)
        off = R[~np.eye(len(cols), dtype=bool)]
        for o in out:
            o["mean_offdiag_corr"] = float(off.mean())
            o["n_regions"] = len(cols)
    else:
        for o in out:
            o["mean_offdiag_corr"] = np.nan
            o["n_regions"] = 1
    return out


def build(d: pd.DataFrame, item: str) -> pd.DataFrame:
    base = E.build(d, item)[["essround", "cntry", "region", "D", "nu", "n"]]
    base = base.rename(columns={"D": "D_region"})
    ok = d[item].between(0, 10) & d.anweight.gt(0) & d.region.notna()
    rows = []
    for (r, c), gc in d[ok].groupby(["essround", "cntry"], observed=True):
        for rec in country_round(gc, item):
            rec.update(essround=int(r), cntry=str(c))
            rows.append(rec)
    dev = pd.DataFrame(rows)
    m = base.merge(dev, on=["essround", "cntry", "region"],
                   suffixes=("", "_dev"))
    m["ratio"] = m.D_dev / m.D_region.replace(0, np.nan)
    return m


def main() -> None:
    cache = Path(os.environ.get("ESS_CACHE", str(Path.home() / "ess_cache"))) \
        / "ess_extract.pkl"
    d = pd.read_pickle(cache)
    tabs, rows = {}, []
    for item in ITEMS:
        t = build(d, item)
        tabs[item] = t
        for rnd in ROUNDS:
            sub = t[t.essround == rnd]
            for mn in MIN_N:
                s = sub[(sub.n >= mn) & (sub.nu >= 2)]
                if len(s) < 20:
                    continue
                # rerun exp27's configuration with the corrected variance
                sc = s.rename(columns={"D_dev": "D"}).copy()
                sc["Fc"] = np.nan
                r2 = E.run_config(sc, item, rnd, mn)
                if r2 is None:
                    continue
                r2 = {f"dev_{k}": v for k, v in r2.items()
                      if k not in ("item", "essround", "min_n")}
                r2.update(item=item, essround=rnd, min_n=mn,
                          ratio_med=float(s.ratio.median()),
                          ratio_q10=float(s.ratio.quantile(.10)),
                          ratio_q90=float(s.ratio.quantile(.90)),
                          Wshare_med=float(s.Wshare.median()),
                          corr_med=float(s.mean_offdiag_corr.median()),
                          nreg_med=float(s.n_regions.median()))
                rows.append(r2)
    dv = pd.DataFrame(rows)
    old = pd.read_csv(ROOT / "results" / "exp27_ess_scalar.csv")
    j = old.merge(dv, on=["item", "essround", "min_n"])
    out = ROOT / "results" / "exp28_centring.csv"
    j.to_csv(out, index=False)
    allrat = pd.concat(tabs.values())
    (ROOT / "results" / "exp28_manifest.json").write_text(json.dumps(dict(
        experiment="exp28_centring", configs=len(j),
        ratio_dev_over_region=[float(allrat.ratio.quantile(.1)),
                               float(allrat.ratio.median()),
                               float(allrat.ratio.quantile(.9))],
        corr_induced=[float(allrat.mean_offdiag_corr.min()),
                      float(allrat.mean_offdiag_corr.median()),
                      float(allrat.mean_offdiag_corr.max())],
        note="degrees of freedom kept at the region level, the conservative choice",
    ), indent=2) + "\n")

    pd.set_option("display.width", 240, "display.max_columns", 60)
    print("=== M1/M2: D_dev / D_region across all region cells")
    for it, t in tabs.items():
        v = t.ratio.dropna()
        print(f"  {it:8s} median {v.median():.3f}  q10 {v.quantile(.1):.3f}"
              f"  q90 {v.quantile(.9):.3f}  >1 in {100*(v>1).mean():.1f}% of cells")
        b = t.dropna(subset=["ratio"]).copy()
        b["q"] = pd.qcut(b.Wshare, 4, labels=["Q1", "Q2", "Q3", "Q4"])
        print("      by region weight share:",
              {str(k): round(float(g.ratio.median()), 3)
               for k, g in b.groupby("q", observed=True)})
    print("\n=== M3: correlation a common estimated centre induces across regions")
    for it, t in tabs.items():
        v = t.mean_offdiag_corr.dropna()
        print(f"  {it:8s} median {v.median():+.4f}  range {v.min():+.4f} to {v.max():+.4f}")
    c = pd.concat(tabs.values()).dropna(subset=["mean_offdiag_corr"])
    print("  by number of regions in the country-round:")
    c["nb"] = pd.cut(c.n_regions, [0, 5, 10, 20, 100])
    print("   ", {str(k): round(float(g.mean_offdiag_corr.median()), 4)
                  for k, g in c.groupby("nb", observed=True)})
    print("\n=== M4: does the correction move exp27's conclusions?")
    for col in ("cert_over_unc", "cert_over_sep", "cert_over_gauss",
                "struct_R2_on_Dhat", "rho2_hat"):
        a, b = j[col], j["dev_" + col]
        print(f"  {col:20s} exp27 {a.min():.3f}-{a.max():.3f} | corrected "
              f"{b.min():.3f}-{b.max():.3f} | median shift {np.median(b - a):+.4f}")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
