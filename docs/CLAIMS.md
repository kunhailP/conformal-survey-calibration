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

## From exp03 / exp03b (verified, `results/exp03_regional.csv`, `exp03b_verification.csv`)

Regional departures from own national distribution, `trstprl`, low-trust core
`t in {1,2,3,4}` (d = 4, the grid of the implementation under study), ESS rounds
9-11, B = 400, resampling unit `(stratum, psu)`. Diagnostic formulas reproduce
`pcb.inference.design_aware` of the archive exactly.

**Reproduction.** Under the archive's own settings (m-of-m, unit split by
region) the diagnostic reproduces the archive's reported values to four decimal
places: 0.1423 / 0.1380 / 0.1241 / 0.1307 against a reported 0.1415 / 0.1382 /
0.1249 / 0.1312. The reimplementation is therefore characterising the same
statistic.

| finding | value |
|---|---|
| Activations under Rao-Wu-Yue with `(stratum, psu)` | **4 of 30 configurations** |
| Need gate A opens | 22 of 30 |
| Reliability gate B opens | 6 of 30 |
| Regional design share `rho_hat` | **0.49 - 0.66** |
| Bootstrap: gate B opens under m-of-m | **8 of 8 arms** |
| Bootstrap: gate B opens under Rao-Wu-Yue | **2 of 8 arms** |
| Resampling unit `(stratum,psu)` vs `(stratum,psu,region)`: effect on D | **< 1%, never flips a gate** |
| Seed stability (4 seeds) | D within 0.001 |
| Replicate count (B = 200 to 2000) | D within 0.002 |

**The bootstrap choice, not the resampling unit, is what moves the result.**
`exp02` found only 0.52% of respondents in a region-splitting PSU, and the
correction accordingly changes nothing. The m-of-m scheme biases design
variance downward, and `tau_D = 0.147` sits inside the gap it opens.

**The two gates are structurally coupled.** The ratio of the realised
diagnostic to its K-floor is predicted by scale shrinkage times a heterogeneity
factor with correlation 0.984 and mean error 3.2%, and scale shrinkage is the
dominant term.

| | |
|---|---|
| `corr(rho_hat, D / K-floor)` | **0.964** |
| K-floor cleared | 27 of 30 configurations |
| Gate B opened | 6 of 30 |

The more design noise there is to remove, the more the deconvolution shrinks the
target scale, and the diagnostic is inflated by exactly that shrinkage. The
need gate and the reliability gate therefore read the same quantity in opposite
directions. Activation survives only in a narrow band where the design share
clears `rho_0 = 0.47` without inflating `D` past `tau_D`, which is why the four
activations sit at the smallest region size and, three of four, in round 11,
the round with the lowest design share.

This supersedes the `K >= 94` floor as the operative account. The floor is
cleared in 27 of 30 configurations and is not what binds.

## From exp04 (verified, `results/exp04_national.csv`)

National unit, same machinery. Full samples and a subgroup scan matching the
construction behind the inherited figure.

| finding | value |
|---|---|
| `rho_hat`, full samples, per round and trajectory | **0.095 - 0.101** |
| `rho_hat`, subgroup scan, 33 cells | 0.093 - **0.369** |
| Inherited maximum, from a scan of this kind | 0.29 |
| Need gate opened | **0 of 37** |
| Reliability gate opened | 0 of 37 |
| Heterogeneity share of `D^2` at the national unit | **0.1% - 4.4%** |

Protocol outcome 1. The national cell of the characterisation stands, now
verified. Its diagnostic has a different structure from the regional one: at
`K <= 33` the K-floor term dominates and heterogeneity is negligible, the
reverse of the regional unit.

## From exp05 (verified, `results/exp05_information.csv`)

Fay-Herriot with known sampling variances, REML, 40 conditions x 2,000 replicates. Protocol outcome 1.

| finding | value |
|---|---|
| Fisher information for the model variance | `I(A) = (1/2) sum_c (A + D_c)^-2` |
| Closed form vs exact bound, equal `D` | agree to **3e-16** relative |
| REML realised / bound, `K >= 100` | median **1.002**, range 0.952-1.035 |
| REML returns `A_hat = 0`, `rho <= 0.5`, any `K` | **0.0%** |
| REML returns `A_hat = 0`, `rho = 0.9` | **25.3%** at K=30, 8.3% at K=100, 1.3% at K=250, 0.0% at K=500 |
| Dispersed `D_c` at the same mean | exact bound falls below the closed form; the closed form is conservative |

**Reading.** The `(1 - rho^2)^-1` inflation is an information bound, not an
artefact of a moment estimator, and REML attains it. This closes the scope gap
the predecessor left open, which excluded biased, shrinkage and prior-informed
estimators and left a minimax version unproved: the restriction to unbiased
estimation is not what carries the result, since the estimator small-area
practice actually uses sits on the bound.

It also connects the boundary to a recognised failure mode. Zero and negative
estimates of a between-area variance appear in exactly the regime the boundary
calls infeasible, and are absent at design shares up to 0.5 at every `K`
examined.

**Not claimed as novel.** Equation~(9) is the standard asymptotic variance of
the model-variance estimator in this model. What the manuscript claims is
overlooked is its consequence for feasibility criteria, and the empirical
demonstration in exp03.

## From exp06 (verified, `results/exp06_claims.csv`)

Trust in parliament, ESS rounds 9-11, 30 countries, low-trust core, `alpha = 0.10`,
B = 2000, one-sided studentised sup-t over the contrast surface.

**Reproduction gate cleared.** Under the archive's m-of-m bootstrap this
implementation returns 20 / 12 / 6 / 1 and the net set {AT, BE, EE, GB, GR, NL},
exactly as the archive reports.

| claim | point estimate | pointwise | simultaneous |
|---|---|---|---|
| some adjacent pair declines | **20** | **15** | **11** |
| the span declines | 10 | 7 | **6** |
| every adjacent pair declines | 4 | 2 | **1** |

Net certified: AT, BE, EE, GB, GR, NL.

**Reading.** Two reductions compound and answer different questions. Design-based
uncertainty applied one contrast at a time removes 5 of 20; simultaneity over the
whole surface removes a further 4. The claim rung compounds again, 11 to 6 to 1.

**Correction to the predecessor's presentation.** It reported the first and third
entries of the first row as a contrast between a "marginal reading" and a
simultaneous band. The first column is not a marginal statistical reading: it is
the sign of the point estimate, with no uncertainty attached. The three-column
decomposition is the honest form of the same comparison and remains a large
effect. Reported in the manuscript as such.

**Not claimed.** Nothing here is a statement about political change. The window
contains a pandemic round and a mode transition in several countries, and
measurement comparability across rounds is assumed rather than shown.

## From exp07 (verified, `results/exp07_widths.csv`, `exp07_anchor_coverage.csv`)

Same target, same level, same calibration set. 15 regional configurations.

| finding | value |
|---|---|
| Correction radius / anchor radius, median | **0.805** (range 0.780-0.895) |
| Where the gates open | **0.805-0.849**, a 15-20% reduction |
| Oracle ceiling `1 - sqrt(1-rho^2)` in those cells | 17-22% |
| Conservative envelope / anchor | **1.63** |
| Anchor leave-one-country-out marginal coverage | **0.896** median, 0.891-0.906 |
| Nominal | 0.900 |
| Largest deviation vs one SE at the smallest evaluation count | within 0.018 |
| Worst held-out country, conditional | 0.10-0.60 |

**Reading.** The correction buys 15 to 20 percent against the anchor where it
activates, inside the oracle ceiling. It is worth having where reachable, so the
boundary is a search instruction rather than a discouragement.

The anchor's finite-sample guarantee for the observed target survives a real
complex design. Conditional coverage does not and is not claimed.

**Correction to the predecessor's comparator.** It reported the gain against the
conservative envelope, which is 1.63 times the anchor here, and reported a scale
ratio rather than a realised radius. Against the anchor the gain is smaller than
the headline it replaced but is measured on the band an analyst would otherwise
use.

**No external head-to-head is run,** because the available benchmarks cover
scalar parameters of observed areas rather than a simultaneous band for a
held-out population. Argued in the manuscript rather than dodged.

## From exp08 (verified, `results/exp08_domains.csv`)

Estimand held fixed as a domain's departure from its own national curve;
only the domain definition varies. 45 configurations: five definitions x three
rounds x three minimum sizes. Protocol: `docs/PROTOCOL_exp08_domains.md`.

| domains cut by | K | design share | required by the boundary |
|---|---|---|---|
| sex | **60** | **0.85** | **2006** |
| age band | 119 | 0.52 | 189 |
| region | **236** | **0.60** | **256** |
| age band and sex | 232 | 0.65 | 330 |
| region and sex | 292 | 0.68 | 393 |

| | |
|---|---|
| Boundary predicts the gate correctly | **44 of 45** |
| Gate opens | 6 of 45, five of them in round 11 |

**Reading.** Refinement raises the supply and the requirement together, and the
dimension decides which wins. Cutting by sex yields 60 populations against a
requirement of 2,006; cutting by region yields 236 against 256. The domain
counts differ only fourfold, so the count is not what separates them: sex adds
sampling variance without adding between-domain dispersion, because men and
women have nearly the same trust distribution, and the design share reaches
0.85. Regions genuinely differ, so dispersion grows with the noise and the share
stays at 0.60.

The design instruction is to refine along a dimension on which the domains
actually differ. A cut that only subdivides a homogeneous population cannot
reach the correction at any depth.

**A level dropped after the first run.** The country level was included
initially and is degenerate for this estimand: a domain that is the country has
zero departure from its own national curve by construction. It was removed and
the sweep re-run; the national reference is `exp04`, which uses deviations from
a cross-country centre instead.

## Claims deliberately not made

- No universal width-optimality for any latent-target band.
- `K >= 94` is the intercept of one diagnostic at one frozen constant, not a
  limit on inference. It does not cover biased, shrinkage, or
  structured-covariance estimators.
- Activation of the selector is not evidence that assumption (S) holds.
- An empirically calibrated operational level is not a theorem-backed level.
- Coverage measured against survey estimates does not validate latent coverage.
