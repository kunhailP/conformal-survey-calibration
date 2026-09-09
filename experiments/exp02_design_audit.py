"""exp02 - ESS design-file audit: do primary sampling units nest in regions?

Protocol: docs/PROTOCOL_exp02_design_audit.md (written before execution).
Requires licensed ESS microdata; see docs/DATA.md.  Reads the cached extract
produced by scripts in this repository, never redistributed.

    python experiments/exp02_design_audit.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

CACHE = ROOT / "data" / "ess_r9_11.pkl"
OUT = ROOT / "results"


def main() -> None:
    d = pd.read_pickle(CACHE)
    d = d[d.region.notna() & d.psu.notna()].copy()
    d["region"] = d.region.astype(str)
    d["psu"] = d.psu.astype(str)
    d["stratum"] = d.stratum.astype(str)

    rows = []
    for (rnd, cty), g in d.groupby(["essround", "cntry"], observed=True):
        per_psu = g.groupby("psu").region.nunique()
        split = per_psu[per_psu > 1].index
        n_split_resp = int(g.psu.isin(split).sum())
        per_stratum = g.groupby("stratum").region.nunique()
        psus_per_region = g.groupby("region").psu.nunique()
        rows.append(dict(
            essround=int(rnd), cntry=str(cty), n=len(g),
            n_regions=g.region.nunique(), n_psu=g.psu.nunique(),
            n_stratum=g.stratum.nunique(),
            psu_equals_idno=bool((g.psu.nunique() == len(g))),
            psu_constant=bool(g.psu.nunique() == 1),
            psu_split_across_regions=int(len(split)),
            share_resp_in_split_psu=n_split_resp / len(g),
            stratum_split_across_regions=int((per_stratum > 1).sum()),
            median_psu_per_region=float(psus_per_region.median()),
            regions_with_lt3_psu=int((psus_per_region < 3).sum()),
            median_resp_per_psu=float(g.groupby("psu").size().median()),
        ))
    a = pd.DataFrame(rows).sort_values(["essround", "cntry"])
    OUT.mkdir(exist_ok=True)
    a.to_csv(OUT / "exp02_design_audit.csv", index=False)

    print(f"country-rounds audited: {len(a)}   respondents: {a.n.sum():,}\n")
    deg = a[a.psu_equals_idno | a.psu_constant]
    print(f"[1] PSU is degenerate (equals respondent, or constant): "
          f"{len(deg)} of {len(a)} country-rounds")
    if len(deg):
        print("    ", sorted(deg.cntry.unique()))
    ok = a[~(a.psu_equals_idno | a.psu_constant)]
    bad = ok[ok.psu_split_across_regions > 0]
    print(f"\n[2] Among {len(ok)} country-rounds with informative PSUs, "
          f"{len(bad)} have PSUs spanning >1 region")
    if len(bad):
        print(bad[["essround", "cntry", "n", "n_regions", "n_psu",
                   "psu_split_across_regions", "share_resp_in_split_psu"]]
              .to_string(index=False))
        print(f"\n    respondents in split PSUs: {(bad.share_resp_in_split_psu*bad.n).sum():,.0f}"
              f" ({(bad.share_resp_in_split_psu*bad.n).sum()/a.n.sum():.2%} of all)")
    thin = ok[ok.regions_with_lt3_psu > 0]
    print(f"\n[3] country-rounds with a region carried by <3 PSUs: {len(thin)}")
    print(f"\n[4] strata spanning >1 region: "
          f"{int((a.stratum_split_across_regions > 0).sum())} of {len(a)} country-rounds")
    print(f"\nwritten: {OUT/'exp02_design_audit.csv'}")


if __name__ == "__main__":
    main()
