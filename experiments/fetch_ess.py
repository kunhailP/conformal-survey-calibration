"""Fetch the ESS rounds 9-11 integrated files and cache the columns we use.

The ESS data portal exposes a beta REST API with one endpoint.  `userId` is not
authentication - the API documentation states it is for usage statistics - so an
ESS End User Licence registration is required and each user supplies their own
id from https://ess.sikt.no/en/api.

    ESS_USER_ID=<your id> python experiments/fetch_ess.py [--outdir DIR]

Nothing is written into this repository: the default cache directory is outside
it, and the raw files are not redistributed.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import pandas as pd
import urllib.request

API = "https://api.ess.sikt.no/v1/data/dataFile/10.21338/{suffix}"
FILES = {9: "ess9e03_2", 10: "ess10e03_2", 11: "ess11e02_0"}
KEEP = ["essround", "cntry", "region", "stratum", "psu", "prob", "domain",
        "anweight", "pspwght", "dweight", "pweight",
        "trstprl", "stflife", "happy"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default=os.environ.get(
        "ESS_CACHE", str(Path.home() / "ess_cache")))
    args = ap.parse_args()
    uid = os.environ.get("ESS_USER_ID")
    if not uid:
        sys.exit("set ESS_USER_ID (see https://ess.sikt.no/en/api)")
    out = Path(args.outdir); out.mkdir(parents=True, exist_ok=True)

    frames = []
    for rnd, suffix in FILES.items():
        raw = out / f"{suffix}.csv"
        if not raw.exists():
            url = f"{API.format(suffix=suffix)}?userId={uid}&fileFormat=csv"
            print(f"round {rnd}: downloading {suffix} ...", flush=True)
            urllib.request.urlretrieve(url, raw)
        d = pd.read_csv(raw, usecols=lambda c: c in KEEP, low_memory=False)
        print(f"round {rnd}: {d.shape[0]:,} respondents, {d.shape[1]} columns")
        frames.append(d)

    d = pd.concat(frames, ignore_index=True)
    cache = out / "ess_extract.pkl"
    d.to_pickle(cache)
    print(f"\ncached {d.shape[0]:,} respondents to {cache}")
    print(f"country-rounds {d.groupby(['essround','cntry']).ngroups}, "
          f"countries {d.cntry.nunique()}, "
          f"region-rounds {d[d.region.notna()].groupby(['essround','cntry']).region.nunique().sum()}")
    miss = d[["region", "stratum", "psu", "prob", "anweight"]].isna().mean()
    print("design-variable missingness:", dict(miss.round(4)))


if __name__ == "__main__":
    main()
