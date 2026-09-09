"""exp08 - can the boundary be outrun by refining the calibration unit?

Protocol: docs/PROTOCOL_exp08_domains.md (written before execution).
Requires licensed ESS microdata.

    python experiments/exp08_domains.py
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
import exp03_regional as E  # noqa: E402

OUT = ROOT / "results"
TAU = E.TAU_D

AGE4 = [(15, 29), (30, 44), (45, 59), (60, 200)]


def domain_key(g: pd.DataFrame, spec: str) -> np.ndarray:
    """Domain label per respondent.  Missing components become their own level
    rather than dropping the respondent, so the national curve stays whole."""
    n = len(g)
    parts = []
    if "sex" in spec:
        parts.append(g.gndr.fillna(-1).astype(int).astype(str).to_numpy())
    if "age" in spec:
        band = pd.cut(g.agea, bins=[14, 29, 44, 59, 200], labels=["a", "b", "c", "d"])
        parts.append(band.astype(object).fillna("na").astype(str).to_numpy())
    if "region" in spec:
        parts.append(g.region.fillna("na").astype(str).to_numpy())
    if not parts:
        return np.array(["all"] * n, dtype=object)
    out = parts[0].astype(object)
    for q in parts[1:]:
        out = np.char.add(np.char.add(out.astype(str), "|"), q.astype(str)).astype(object)
    return out


def departures(g: pd.DataFrame, spec: str, rng):
    """Domain departures from the country's own national curve, with design SDs."""
    y = g.trstprl.to_numpy()
    ind = (y[:, None] <= E.THRESHOLDS[None, :]).astype(np.float64)
    w = g.anweight.to_numpy(dtype=np.float64)
    dom, labels = pd.factorize(domain_key(g, spec))
    assert dom.min() >= 0
    nat = np.zeros(len(g), dtype=np.int64)

    dep = weighted_cdf(ind, w, dom, len(labels)) - weighted_cdf(ind, w, nat, 1)
    W, _ = replicate_weights(g.stratum.to_numpy(), g.psu.to_numpy(), w, E.B, rng)
    rep = weighted_cdf(ind, W, dom, len(labels)) - weighted_cdf(ind, W, nat, 1)
    v = np.nanstd(rep, axis=2, ddof=1)
    return dep, v, np.bincount(dom, minlength=len(labels))


# The country level is not a refinement of this estimand: a domain that is the
# country has zero departure from its own national curve by construction.  The
# national reference is exp04, which uses deviations from a cross-country centre.
SPECS = [("country x sex", "sex"), ("country x age", "age"),
         ("country x age x sex", "age+sex"), ("country x region", "region"),
         ("country x region x sex", "region+sex")]


def main() -> None:
    d = pd.read_pickle(E.CACHE)
    d = d[d.trstprl.between(0, 10) & d.anweight.gt(0) & d.agea.notna()].copy()
    d["region"] = d.region.astype(str)
    d = d[~d.region.isin(["nan", ""])]
    d = d[d.region.str.upper() != d.cntry.astype(str).str.upper()]

    rows = []
    for name, spec in SPECS:
        for rnd in (9, 10, 11):
            for min_n in (40, 60, 100):
                rng = np.random.default_rng(20260913)
                deps, vs = [], []
                for (r, c), g in d.groupby(["essround", "cntry"], observed=True):
                    if int(r) != rnd or len(g) < 200:
                        continue
                    dep, v, sizes = departures(g, spec, rng)
                    keep = sizes >= min_n
                    if keep.sum() < 2:      # a country needs two domains to differ
                        continue
                    deps.append(dep[keep]); vs.append(v[keep])
                if not deps:
                    continue
                dep = np.vstack(deps); v = np.vstack(vs)
                ok = np.isfinite(dep).all(1) & np.isfinite(v).all(1)
                dep, v = dep[ok], v[ok]
                if len(dep) < 5:
                    continue
                g_ = E.gates(dep, v)
                rho = g_["rho_hat"]
                req = 1 + 2 / (TAU ** 2 * (1 - rho ** 2) ** 2
                               * (1 - g_["hetero_share_of_D2"]))
                rows.append(dict(domain=name, essround=rnd, min_n=min_n,
                                 K=g_["K"], rho_hat=rho, D=g_["D"],
                                 K_required=req, supply_minus_need=g_["K"] - req,
                                 gate_A=g_["gate_A"], gate_B=g_["gate_B"],
                                 branch=g_["branch"]))

    out = pd.DataFrame(rows)
    out.to_csv(OUT / "exp08_domains.csv", index=False, float_format="%.6g")
    (OUT / "exp08_manifest.json").write_text(json.dumps({
        "protocol": "docs/PROTOCOL_exp08_domains.md", "tau": TAU,
        "specs": [s[0] for s in SPECS]}, indent=2) + "\n")

    pd.set_option("display.width", 200)
    piv = out[out.min_n == 60].pivot_table(index="domain", columns="essround",
                                           values=["K", "rho_hat", "K_required"])
    print("At minimum domain size 60, by round\n")
    print(piv.round(3).to_string())
    print("\nfull sweep, supply minus requirement (positive = gate reachable)\n")
    print(out[["domain", "essround", "min_n", "K", "rho_hat", "K_required",
               "supply_minus_need", "gate_B"]].round(2).to_string(index=False))
    print(f"\ngate B opens in {out.gate_B.sum()} of {len(out)} configurations")
    print(f"K exceeds its requirement in {(out.supply_minus_need > 0).sum()}")


if __name__ == "__main__":
    main()
