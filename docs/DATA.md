# Data

No microdata are stored in this repository, and none are required to reproduce
`exp01`.

## Licensed sources used by the inherited analyses

| source | edition | access |
|---|---|---|
| European Social Survey, integrated file rounds 1-11 | 2024 release | free registration, ESS End User Licence |
| AmericasBarometer / LAPOP Grand Merge 2004-2023 | 2023 release | free registration |

Redistribution is prohibited; access is not restricted. Obtain from the
providers, then follow the predecessor repository's instructions at
`github.com/kunhailP/design-aware-conformal` (snapshot `ea592e9`).

### ESS retrieval, scripted (added 2026-09-10)

The ESS data portal at `https://ess.sikt.no` exposes a beta REST API with a
single endpoint, which makes the ESS half of this reproducible without manual
downloads:

```
GET https://api.ess.sikt.no/v1/data/dataFile/{doiPrefix}/{doiSuffix}
      ?userId=<your ESS user id>&fileFormat=csv
```

`userId` is **not** authentication — the API's own documentation says it is for
usage statistics — so an ESS End User Licence registration is still required and
each user supplies their own id, obtained from `https://ess.sikt.no/en/api`
after logging in. **No user id is stored in this repository.** The endpoint
returns a 307 redirect to a generated file URL; follow redirects.

Data-file DOIs used, all under prefix `10.21338`:

| round | suffix | respondents |
|---|---|---|
| 9 | `ess9e03_2` | 49,519 |
| 10 | `ess10e03_2` | 37,611 |
| 11 | `ess11e02_0` | 40,156 |

These integrated files carry `region`, `stratum`, `psu`, `prob`, `domain` and
the weights `anweight`, `pspwght`, `dweight`, `pweight` with **no missingness**
in rounds 9--11, so the design-file condition `exp02` checked is met by the API
files as well. Combined: 127,286 respondents, 75 country-rounds, 31 countries,
825 region-rounds, median 10 regions per country-round (range 1--28).

`experiments/fetch_ess.py` performs the download and writes a column subset to a
local cache **outside this repository**. The cache is not committed and the raw
files are not redistributed.

## Re-execution status

`exp01` runs from source in this repository. The survey diagnostics quoted in
`docs/CLAIMS.md` are read from archived result tables and have **not** been
re-executed here. Reproducing a saved number and justifying its assumptions are
separate tasks, and the manuscript distinguishes them.

## Design-file verification: closed 2026-09-09

The regional analysis groups by stratum, primary sampling unit, and region. If
a primary sampling unit spans more than one region, resampling must treat those
regions jointly. `experiments/exp02_design_audit.py` checked this against the
licensed files. Result in `docs/CLAIMS.md`: nesting holds for 99.48% of
respondents, fails in fifteen country-rounds, and strata do not nest in regions
in 63 of 90 country-rounds. Twelve countries carry degenerate PSU identifiers.
The consequences for the regional analysis are recorded with the finding.

Rounds 9-11 carry complete `psu`, `stratum`, `region`, `prob` and weight
variables for all 33 countries, so no country is lost to missing design
metadata.
