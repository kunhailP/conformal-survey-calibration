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
| Regional activations, common coding level, either bootstrap | **0 of 21** | both of the above |
| Leave-one-country-out anchor coverage | 0.893-0.903 vs 0.900 | `small_area_exchangeability.csv` |
| Worst held-out country conditional coverage | 0.53-0.63 | `small_area_loco_by_country.csv` |

The common-coding-level row is a fact about the archive that the predecessor
manuscript stated in prose but never tabulated. It belongs in a table: the
correction has never activated on a homogeneous unit definition.

## Claims deliberately not made

- No universal width-optimality for any latent-target band.
- `K >= 94` is the intercept of one diagnostic at one frozen constant, not a
  limit on inference. It does not cover biased, shrinkage, or
  structured-covariance estimators.
- Activation of the selector is not evidence that assumption (S) holds.
- An empirically calibrated operational level is not a theorem-backed level.
- Coverage measured against survey estimates does not validate latent coverage.
