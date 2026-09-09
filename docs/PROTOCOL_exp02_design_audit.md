# Protocol — exp02: ESS design-file audit

Written 2026-09-09, before executing `experiments/exp02_design_audit.py`.
Status: **verification of a data property**, not an inferential experiment.
Licensed ESS microdata, rounds 9-11.

## Why

The regional construction estimates a region's departure from its own national
distribution and resamples primary sampling units to obtain the design variance
of that difference. `docs/DATA.md` records the outstanding condition:

> If a primary sampling unit spans more than one region, resampling must treat
> those regions jointly.

The predecessor analysis grouped by stratum, PSU and region. If PSUs nest
inside regions this is harmless. **If they do not, a resample can split one PSU
across regions, breaking the dependence it exists to represent, and the
regional design variances — hence every design share, every gate decision, and
the entire regional activation result — are computed under a false structure.**

The regional activation is the only place the correction fires on real data.
It rests on this condition. Nobody has checked it.

## Checks

Within each `(essround, cntry)`:

1. **Nesting.** Count PSUs mapping to more than one region; report the share of
   respondents in them, by country and round.
2. **Degeneracy.** Where a country's PSU identifier is constant, or equals the
   respondent identifier, the PSU is not an informative cluster and the
   bootstrap reduces to something else. Report which countries these are.
3. **Stratum-region relation.** Whether strata nest in regions, cross them, or
   are defined by them.
4. **Support.** PSUs per region and respondents per PSU, since a region carried
   by one or two PSUs cannot support a within-region resample.

## Outcomes and what each forces

- **PSUs nest in regions everywhere.** The inherited regional numbers stand as
  computed. Recorded and closed.
- **Nesting fails in a few countries.** Those countries are excluded, or the
  resampling unit is coarsened to the PSU with regions handled jointly, and the
  regional analysis is re-run. The activation result may not survive.
- **Nesting fails widely.** The regional activation cannot be reported in its
  current form. This is a result, and the manuscript reports it as one.

Every outcome, including the third, is reported. No country is dropped for
producing an inconvenient answer, and any exclusion is stated with its rule.
