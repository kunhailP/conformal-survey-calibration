"""exp03b - verification of exp03: seed, replicate count, and mechanism.

Three checks.

(1) Seed stability.   Does the conclusion depend on the bootstrap draw?
(2) Replicate count.  Does B = 400 resolve the diagnostic?
(3) Mechanism.        exp03 claims the inherited activation was produced by two
                      choices: an m-of-m bootstrap that biases design variance
                      downward, and a resampling unit of (stratum, psu, region)
                      that splits a PSU straddling regions.  This runs the 2x2
                      and tests that claim directly, on the cells the archive
                      reported as activating.

    python experiments/exp03b_verification.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments"))

from dac.survey import replicate_weights, weighted_cdf  # noqa: E402
import exp03_regional as E  # noqa: E402

TAU_D = E.TAU_D
ARCHIVE_CELLS = ((9, 60), (10, 60), (9, 40), (10, 40))   # activated in the archive


def departures(g, rng, *, rescaled, split_by_region, n_rep):
    y = g.trstprl.to_numpy()
    ind = (y[:, None] <= E.THRESHOLDS[None, :]).astype(np.float64)
    w = g.anweight.to_numpy(dtype=np.float64)
    reg, regions = pd.factorize(g.region.to_numpy())
    nat = np.zeros(len(g), dtype=np.int64)
    dep = E.weighted_cdf(ind, w, reg, len(regions)) - E.weighted_cdf(ind, w, nat, 1)
    psu = g.psu.astype(str).to_numpy()
    if split_by_region:                       # the inherited grouping
        psu = np.char.add(np.char.add(psu, "|"), g.region.astype(str).to_numpy())
    W, _ = replicate_weights(g.stratum.to_numpy(), psu, w, n_rep, rng, rescaled=rescaled)
    rep = weighted_cdf(ind, W, reg, len(regions)) - weighted_cdf(ind, W, nat, 1)
    return dep, np.nanstd(rep, axis=2, ddof=1), np.bincount(reg, minlength=len(regions))


def pool(d, rnd, min_n, rng, **kw):
    deps, vs = [], []
    for (r, c), g in d.groupby(["essround", "cntry"], observed=True):
        if int(r) != rnd or g.region.nunique() < 2:
            continue
        dep, v, sizes = departures(g, rng, **kw)
        keep = sizes >= min_n
        if keep.sum() >= 2:
            deps.append(dep[keep]); vs.append(v[keep])
    dep = np.vstack(deps); v = np.vstack(vs)
    ok = np.isfinite(dep).all(1) & np.isfinite(v).all(1)
    return E.gates(dep[ok], v[ok])


def main() -> None:
    d = pd.read_pickle(E.CACHE)
    d = d[d.trstprl.between(0, 10) & d.anweight.gt(0)].copy()
    d["region"] = d.region.astype(str)
    d = d[~d.region.isin(["nan", ""])]
    d = d[d.region.str.upper() != d.cntry.astype(str).str.upper()]

    base = dict(rescaled=True, split_by_region=False, n_rep=E.B)

    print("(1) SEED STABILITY  round 10, min_n 40, deployed settings")
    for seed in (20260909, 1, 77, 12345):
        r = pool(d, 10, 40, np.random.default_rng(seed), **base)
        print(f"    seed {seed:>8}  K={r['K']}  rho={r['rho_hat']:.4f}  "
              f"D={r['D']:.4f}  gate_B={r['gate_B']}")

    print("\n(2) REPLICATE COUNT  round 10, min_n 40, deployed settings")
    for nb in (200, 400, 1000, 2000):
        r = pool(d, 10, 40, np.random.default_rng(20260909),
                 rescaled=True, split_by_region=False, n_rep=nb)
        print(f"    B={nb:>5}  rho={r['rho_hat']:.4f}  D={r['D']:.4f}  "
              f"gate_B={r['gate_B']}")

    print(f"\n(3) MECHANISM  does the inherited setup reopen gate B?  (tau_D = {TAU_D:.3f})")
    print(f"    {'round':>5} {'min_n':>6} {'bootstrap':>10} {'unit':>18} "
          f"{'K':>5} {'rho':>7} {'D':>7}  gate_B")
    rows = []
    for rnd, min_n in ARCHIVE_CELLS:
        for rescaled in (True, False):
            for split in (False, True):
                r = pool(d, rnd, min_n, np.random.default_rng(20260909),
                         rescaled=rescaled, split_by_region=split, n_rep=E.B)
                boot = "Rao-Wu-Yue" if rescaled else "m-of-m"
                unit = "(stratum,psu,region)" if split else "(stratum,psu)"
                rows.append(dict(essround=rnd, min_n=min_n, bootstrap=boot,
                                 resample_unit=unit, **r))
                print(f"    {rnd:>5} {min_n:>6} {boot:>10} {unit:>18} "
                      f"{r['K']:>5} {r['rho_hat']:>7.4f} {r['D']:>7.4f}  {r['gate_B']}")
    out = pd.DataFrame(rows)
    out.to_csv(ROOT / "results" / "exp03b_verification.csv", index=False,
               float_format="%.6g")
    print(f"\n    gate B opens in {out.gate_B.sum()} of {len(out)} arms")
    infer = out[(out.bootstrap == "m-of-m") & (out.resample_unit == "(stratum,psu,region)")]
    ours = out[(out.bootstrap == "Rao-Wu-Yue") & (out.resample_unit == "(stratum,psu)")]
    print(f"    mean D, inherited setup : {infer.D.mean():.4f}")
    print(f"    mean D, corrected setup : {ours.D.mean():.4f}  "
          f"({ours.D.mean()/infer.D.mean():.2f}x)")


if __name__ == "__main__":
    main()
