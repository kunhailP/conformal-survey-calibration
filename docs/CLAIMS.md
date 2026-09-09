# Claims ledger

Every numeric claim intended for the manuscript, with the artefact that
produces it. A claim without a row here does not go in the paper.

Status: `verified` = regenerated in this repository. `inherited` = read from an
archived table produced by the predecessor analysis on licensed microdata,
**not** re-executed here.

## From exp01 (verified, `results/exp01_shape_audit.csv`)

180 cells, 4,000 replicates each, nominal 0.90, exact coordinate variances
throughout. Protocol: `docs/PROTOCOL_exp01_shape_audit.md`.

| claim | structure | rho | d | latent coverage | MC SE |
|---|---|---|---|---|---|
| Control: (S) holds, coverage is nominal | `matched` | 0.80 | 48 | **0.9002** | 0.0047 |
| Realistic national share, worst mismatch | `noise_far_more_correlated` | 0.29 | 48 | **0.9028** | 0.0047 |
| Realistic regional share, worst mismatch | `noise_far_more_correlated` | 0.52 | 48 | **0.8852** | 0.0050 |
| High share, 8 coordinates | `noise_far_more_correlated` | 0.80 | 8 | **0.8592** | 0.0055 |
| High share, 48 coordinates | `noise_far_more_correlated` | 0.80 | 48 | **0.7548** | 0.0068 |
| Reverse mismatch is conservative | `latent_more_correlated` | 0.80 | 48 | **0.9828** | 0.0021 |

**More calibration populations do not repair the mismatch.** At `rho = 0.80`,
`d = 48`, `noise_far_more_correlated`: K=30 gives 0.7765, K=100 gives 0.7823,
K=250 gives 0.7548. The cost does not shrink in K.

**The direction is predictable, and the survey-realistic direction is the
damaging one.** Every structure in which sampling error is more correlated
across coordinates than population differences undercovers; the reverse
overcovers. For a cumulative distribution function, sampling errors at adjacent
thresholds are partial sums over one sample, so the damaging configuration is
the expected one.

**The honest magnitude at the operating point.** At `rho = 0.29`, the national
maximum in the applications, no mismatch structure departs from nominal by more
than Monte Carlo error. At `rho = 0.52`, the regional maximum, the cost is
about one to two percentage points. The large failures require design shares
above anything these surveys exhibit. This must be stated in the manuscript;
it bounds the practical claim to a warning about direction and mechanism, not a
demonstration of failure in the presented applications.

## Inherited from the predecessor archive (NOT re-executed here)

Source: `github.com/kunhailP/design-aware-conformal` at `ea592e9`, licensed
microdata not redistributed. See `docs/DATA.md`.

| claim | value | archived table |
|---|---|---|
| National design share, AmericasBarometer (rescaled) | <= 0.222 | `lapop_change_candidate_b_by_rho_rescaled.csv` |
| National design share, ESS subgroup scan (rescaled) | <= 0.28 | `ess_subgroup_rho_scan_rescaled.csv` |
| National activations | 0 | both of the above |
| Regional activations, original bootstrap | 4 of 23 unit-rounds | `small_area_transport.csv` |
| Regional activations, Rao-Wu-Yue rescaled | 1 of 23 unit-rounds | `small_area_transport_rescaled.csv` |
| Regional activations, common coding level, either bootstrap | 0 of 21 | both of the above |

The three regional rows above are **superseded by exp03**, which recomputes them
under correct joint resampling and finds no activation anywhere. They are kept
here as the record of what the inherited analysis reported.
| Leave-one-country-out anchor coverage | 0.893-0.903 vs 0.900 | `small_area_exchangeability.csv` |
| Worst held-out country conditional coverage | 0.53-0.63 | `small_area_loco_by_country.csv` |

The common-coding-level row is a fact about the archive that the predecessor
manuscript stated in prose but never tabulated. It belongs in a table: the
correction has never activated on a homogeneous unit definition.

## From exp02 (verified, `results/exp02_design_audit.csv`)

ESS rounds 9-11, 90 country-rounds, 159,320 respondents. Protocol:
`docs/PROTOCOL_exp02_design_audit.md`. This closes the outstanding design-file
condition recorded in `docs/DATA.md`; it had never been checked.

| finding | value |
|---|---|
| Country-rounds where the PSU identifier is degenerate (equals respondent, or constant) | **25 of 90** |
| Countries affected | AT, CH, CY, DK, EE, FI, IL, LV, NL, NO, RS, SE |
| Country-rounds with informative PSUs | 65 |
| Of those, country-rounds where a PSU spans more than one region | **15** |
| Respondents in a region-splitting PSU | **822, 0.52% of all** |
| Worst country-rounds | FR r11 15.0%, BE r10 8.7%, HR r11 6.3%, SK r9 5.5% |
| Country-rounds with a region carried by fewer than three PSUs | 8 |
| Country-rounds where a stratum spans more than one region | **63 of 90** |

**Reading.** Nesting holds for the overwhelming majority of the sample, so the
inherited regional design variances are not built on a wholly false structure.
But the violation is not empty, it concentrates in identifiable country-rounds,
and strata almost never nest in regions. Two consequences follow.

1. The regional analysis must either exclude the fifteen country-rounds with
   region-splitting PSUs or resample their affected regions jointly, and the
   activation result must be shown to survive that change rather than assumed
   to. The activation is the only place the correction fires on real data.
2. For the twelve countries with degenerate PSUs the design variance carries no
   clustering component at all. This is a property of those samples, several of
   which are individual-level register samples, not a data defect. It must be
   stated, because a design share estimated without a clustering component is
   not comparable to one estimated with it, and the regional pool mixes both.

## From exp03 (verified, `results/exp03_regional.csv`)

Regional departures from own national distribution, `trstprl`, ESS rounds 9-11,
d = 10 thresholds, B = 400 Rao-Wu-Yue rescaled replicates, resampling unit
`(stratum, psu)` so region-splitting PSUs are carried whole. 30 configurations:
two pools x three rounds x five minimum region sizes. Protocol:
`docs/PROTOCOL_exp03_regional.md`, outcome 3 of the three written before running.

| finding | value |
|---|---|
| Configurations where the correction activates | **0 of 30** |
| Need gate A opens (design noise is real at this unit) | **27 of 30** |
| Reliability gate B opens | **0 of 30** |
| Regional design share `rho_hat` | **0.49 - 0.66** |
| Reliability diagnostic `D` | 0.16 - 0.59, against `tau_D = 0.147` |

**The reported `K >= 94` floor is not what blocks the correction.**

| | |
|---|---|
| Configurations clearing the K-floor `sqrt(2/(K-1)) <= tau_D` | **27 of 30** |
| Of those, configurations where gate B opens | **0** |
| Median share of `D^2` from design-variance heterogeneity | **30.1%** |
| Round 10, min_n 40: K = 290, K-floor 0.0832, realised D | **0.2438** |
| Same cell, heterogeneity share of `D^2` | **60.2%** |
| Configurations passing even with homogeneous design variances | **1 of 30** |
| Ratio of largest to smallest regional design variance | **1,143x - 16,386x** |

**Reading.** At the national unit the correction is unnecessary: the design
share is small. At the regional unit it is needed — gate A opens in 27 of 30
configurations — and it remains unreachable, at population counts up to 290,
three times the reported floor. What blocks it is not the sampling error of a
variance estimate, which more populations would cure, but the *dispersion* of
design variances across units, which they would not. Small areas have wildly
unequal design variances because they have wildly unequal sizes, and the same
refinement of the unit that raises the population count raises that dispersion.
The barrier is therefore structural rather than a sample-size threshold.

This supersedes the inherited regional activation, which was obtained under an
`m`-of-`m` bootstrap that biases design variance downward and under resampling
that could split a PSU across regions. Both corrections push the diagnostic the
same way.

## Claims deliberately not made

- No universal width-optimality for any latent-target band.
- `K >= 94` is the intercept of one diagnostic at one frozen constant, not a
  limit on inference. It does not cover biased, shrinkage, or
  structured-covariance estimators.
- Activation of the selector is not evidence that assumption (S) holds.
- An empirically calibrated operational level is not a theorem-backed level.
- Coverage measured against survey estimates does not validate latent coverage.
