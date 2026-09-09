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

## Re-execution status

`exp01` runs from source in this repository. The survey diagnostics quoted in
`docs/CLAIMS.md` are read from archived result tables and have **not** been
re-executed here. Reproducing a saved number and justifying its assumptions are
separate tasks, and the manuscript distinguishes them.

## Open verification item

The regional analysis groups by stratum, primary sampling unit, and region. If
a primary sampling unit spans more than one region, resampling must treat those
regions jointly. This has not been confirmed against the ESS design files and
is the first check to perform on obtaining the data.
