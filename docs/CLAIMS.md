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

## From exp05, shrinkage-weight corollary (verified)

| finding | value |
|---|---|
| Elasticity of the shrinkage weight to the model variance | `rho^2` |
| Closed form | `RSE(gamma) = (D/A) sqrt(2/K)` |
| REML realised / predicted, `K >= 100`, `rho <= 0.7` | median **1.015**, range 0.847-1.064 |
| Areas for a 10% tolerance at `D/A = 1` | **200** |
| Areas for a 10% tolerance at `D/A = 4` | **3,200** |
| Areas for a 5% tolerance at `D/A = 1` | **800** |

Breaks down at `rho = 0.9`, where the delta-method step fails as the weight
approaches its boundary, and runs about a tenth high at `K = 30`. Reported.

**Why this matters for placement.** The boundary as first stated needs a
relative-precision tolerance, which a gated procedure supplies and ordinary
small-area analysis does not. Through the shrinkage weight it needs none: the
tolerance is on a quantity the analyst already reports. The result is therefore
about area-level modelling generally, not about one conformal selector.

## From exp01, survey-realistic correlation structure (verified)

The manuscript argues that sampling error in an estimated distribution function
is more correlated across thresholds than differences between populations are,
because the former are partial sums over one sample. That argument is now
instantiated rather than asserted: `R(j,k) = sqrt(p_j(1-p_k)/p_k(1-p_j))`
evaluated at the survey's own core threshold values `(0.177, 0.262, 0.370,
0.463)`, whose mean off-diagonal entry is **0.688** and which decays with the
distance between CDF values.

| condition | rho = 0.29 | rho = 0.52 | rho = 0.80 |
|---|---|---|---|
| survey-realistic, d = 48 | 0.898 | 0.883 | **0.797** |

It behaves like the mild stylised condition, which is the reassuring outcome:
the stylised grid was not carrying the result.

## Claims deliberately not made

- No universal width-optimality for any latent-target band.
- `K >= 94` is the intercept of one diagnostic at one frozen constant, not a
  limit on inference. It does not cover biased, shrinkage, or
  structured-covariance estimators.
- Activation of the selector is not evidence that assumption (S) holds.
- An empirically calibrated operational level is not a theorem-backed level.
- Coverage measured against survey estimates does not validate latent coverage.

## From exp09 (verified, `results/exp09_estimated_variance.csv`)

100 cells, 2,000 replicates each, $A=1$, Gaussian--$\chi^2$ model M1 of
`docs/THEORY_estimated_variance.md`. Protocol:
`docs/PROTOCOL_exp09_estimated_variance.md`. Nothing here is in the manuscript
yet; the rows exist so that nothing enters it without one.

| claim | cell | value | note |
|---|---|---|---|
| Effective information identity is exact | all | max deviation **9e-16** | Prop. 1 |
| Bound attained by oracle-weighted moment estimator | all | mean ratio **0.9989** | Prop. 2, MC SE 0.032 |
| Equal-weight moment estimator unbiased under estimated D | all | max \|z\| **3.25** | 100 cells |
| Information cost of estimated variances at the regional share | rho=0.66, nu=5, m=250 | K_eff/K_known = **0.963** | under 4 percent |
| Plug-in relative bias, regional operating point | rho=0.66, nu=10 | **0.111** at m=250 | predicted 0.134 |
| That bias does not shrink in m | rho=0.66, nu=10 | 0.097 / 0.105 / 0.111 / 0.111 / 0.109 | m = 30 to 1,000 |
| Reliability gate opens too often under plug-in | rho=0.66, nu=10, m=250 | **0.585** vs 0.179 correctly scaled | equal-weight 0.087 |
| Direction reverses at low share and small m | rho=0.30, nu=5, m=100 | 0.015 vs 0.366 | variance beats bias there |
| Plug-in ML loses to the moment estimator on RMSE | rho=0.66, nu=10, m=250 | **1.223** vs 1.006 times the bound | reverses exp05's ranking |
| Replicate count cannot buy design degrees of freedom | nu_des=20 | nu_eff **16.4** at B=100, **19.6** at B=1,000 | `results/exp09_nu_ceiling.csv` |

## From exp10 (verified, `results/exp10_certification.csv`)

54 cells, 20,000 replicates each, closed Gaussian--$\chi^2$ model of
`docs/THEORY_certification.md`. $\varepsilon=0.10$, $\eta=0.05$,
$\alpha_0=0.05$. Protocol: `docs/PROTOCOL_exp10_certification.md`. Nothing here
is in the manuscript yet.

| claim | cell | value | note |
|---|---|---|---|
| The K>=94 floor is not error-controlled | K=100, rho=0.894, nu=4 | false certification **0.944** | budget 0.05 |
| The frozen gate is not error-controlled | K=300, rho=0.707, nu=4 | certifies 0.527, wrong on **0.466** | budget 0.05 |
| Exact interval on kappa holds the budget | all 54 cells | max **0.049** | nominal 0.05 |
| Its coverage is exact | all 54 cells | **0.946--0.952** | nominal 0.95 |
| Union-bound interval is over-covered | all 54 cells | 0.970--0.994 | nominal 0.95 |
| Union-bound interval almost never certifies | K=300, nu=40, rho=0.707 | **0.000** vs 0.856 exact | Graybill-Wang also 0.000 |
| RSE ratio of the two targets equals rho^2 | rho^2=0.2 / 0.5 / 0.8 | **0.21--0.27 / 0.52--0.71 / 0.85--0.90** | predicted 0.2 / 0.5 / 0.8 |
| Gain in required populations | rho^2=0.2 / 0.5 | **14--24x / 2.0--3.8x** | predicted rho^-4 = 25 / 4 |
| Plug-in band undercovers | K=30, rho=0.894 | **0.704** | oracle 0.965 |
| Safe band covers | all 54 cells | min **0.951** | target 0.90 |
| Safe band width over oracle | worst / best cell | **1.61 / 1.02** | shrinks in K |
| Safe band still narrower than the anchor | worst cell | **0.72** | secondary, across targets |

## Correction to the exp10 rows (2026-09-10)

The claim "gain in required populations 14--24x / 2.0--3.8x" is a **relative
standard error** comparison and must not be read as a reduction in the
certification requirement. On matched criteria at $\tau=0.147$, $\eta=0.05$:

| claim | rho | value | note |
|---|---|---|---|
| Required K, RSE on s_G (manuscript's criterion) | 0.47 / 0.60 / 0.66 | 153 / 226 / 291 | with exp09's estimated-variance correction |
| Required K, RSE on kappa | 0.47 / 0.60 / 0.66 | 9--10 / 31--37 / 58--70 | gain matches rho^-4 = 20.5 / 7.7 / 5.3 |
| Required K, **certified** on kappa, median | 0.47 / 0.60 / 0.66 | **33--41 / 122--149 / 226--276** | costs a further z^2 = 3.84 |
| Gain vs the manuscript's own number | 0.47 / 0.60 / 0.66 | **3.7--4.6x / 1.5--1.9x / 1.1--1.3x** | not reachability at the regional point |

## Same-target T2 comparison (verified, scratch reproduction of exp10 cells)

40,000 replicates, nu = 10 per population, alpha0 = eta = 0.05, target 0.90.
The comparator is `dac.bands.noise_enlargement`, the only other valid T2
construction in the repository.

| claim | cell | value | note |
|---|---|---|---|
| Safe band narrower than the enlargement band | K=300, rho=0.894 | **0.301** | 0.42--0.68 elsewhere |
| Enlargement band coverage | all cells | **0.999--1.000** | valid, wastes its budget |
| Safe band coverage | all cells | **0.955--0.986** | target 0.90 |
| Conservatism: conformal granularity | K=30 / K>=100 | 0.014 / 0.001 | only K+1 levels exist |
| Conservatism: the union step | all cells | 0.004--0.035 | of an eta of 0.05 |

## From exp11 (verified, `results/exp11_heteroscedastic.csv`)

45 cells, 20,000 replicates, scalar target, unequal $D_i$, $\nu_i=10$ per
population, $\alpha_0=\eta=0.05$, guaranteed level 0.90. Protocol:
`docs/PROTOCOL_exp11_heteroscedastic.md`. Nothing here is in the manuscript yet.

| claim | cell | value | note |
|---|---|---|---|
| One-sided limit keeps its budget, oracle df | max over 45 cells | **0.0514** | eta = 0.05, MC SE 0.0015 |
| One-sided limit keeps its budget, feasible df | max over 45 cells | **0.0481** | never exceeded |
| Homoscedastic control reproduces exp10 | slog = 0 | 0.047--0.051 | oracle df |
| Feasible df are conservative at high dispersion | K=100, Dbar/A=4, slog=1.5 | **0.0008** | oracle df 0.0124 there |
| Denominator is the binding channel | K=100, Dbar/A=4, slog=1.5 | nu_den/(K-1) = **0.144** | 100 populations carry 14 |
| Numerator is not | same cell | nu_num = **96** | never below 75 |
| Safe band coverage | min over 45 cells | **0.950** | guaranteed 0.90 |
| Gaussian model plug-in never reaches nominal | max over 45 cells | **0.899** | min 0.547; nominal 0.90 |
| Safe band vs optimised enlargement | best / worst cell | **0.295 / 0.825** | split scanned, optimum 0.5--0.8 on the anchor |
| Safe band width over the infeasible oracle | best / worst cell | **1.017 / 1.873** | shrinks in K |
| Dispersed nu side-set holds too | 9 cells | fail 0.002--0.041 | cov_safe 0.952--0.997 |

## From exp12 (verified, `results/exp12_closing_scalar.csv`)

27 cells, 20,000 replicates, scalar target, unequal $D_i$, $\nu_i=10$,
$\alpha_0=\eta=0.05$, guaranteed 0.90. Protocol:
`docs/PROTOCOL_exp12_closing_scalar.md`.

| claim | cell | value | note |
|---|---|---|---|
| nu_den and K_I move in opposite directions | K=100, mean D=4, 50 at 0.1 / 50 at 7.9 | nu_den **61.8**, K_I **41.95** | equal-D: 99.0 and 4.00 |
| Licensed oracle (a) is exact at every dispersion | max over 27 cells | deviation **0.003** | MC SE 0.0015 |
| Common-denominator oracle (b) is not | two-point, K=300 | **+0.021**, width **+12%** | -0.003 elsewhere |
| Scalar kappa_U band misses the licensed oracle | K=30, Dbar/A=1, slog=1.0 | containment **0.835** | retracts exp11's closure |
| Heteroscedastic safe band on s_G covers | min over 27 cells | **0.964** | guaranteed 0.90 |
| Its containment falls short of 1 - eta | min over 27 cells | **0.944** | Dhat substitution not conservative |
| Unweighted deconvolution efficiency | K=300, Dbar/A=4, slog=1.5 | **0.232** | 0.996 at equal variances |
| Oracle weighting recovers it | all 27 cells | **0.939--1.013** | exp09 Prop. 2 under heteroscedasticity |
| Plug-in weighting backfires | K=300, Dbar/A=4, slog=0 | **0.341** vs unweighted 0.996 | never above 0.69 |
| Valid model-based interval is wider, not narrower | all 27 cells | **1.03--1.14x** the safe band | S5 falsified |
| Gaussian plug-in never reaches nominal | max over 27 cells | **0.897** | min 0.539, nominal 0.90 |

## From exp13 (verified, `results/exp13_weights_and_containment.csv`)

12 cells, 20,000 replicates, $D_i = c\,e_i/n_i$ with $n_i$ a known design
variable, $\nu=10$, $\alpha_0=\eta=0.05$ ($\eta_1=\eta_2=0.025$), guaranteed 0.90.
Protocol: `docs/PROTOCOL_exp13_weights_and_containment.md`.

### Part A — estimating A

| claim | cell | value | note |
|---|---|---|---|
| Cost of estimating the design variances | all 12 cells | **1.005--1.019** | ratio to the known-D ideal |
| Cost of the unweighted procedure | all 12 cells | **1.28--3.02** | this is the whole gap |
| Cost of a feasible GVF weighting | all 12 cells | **1.00--1.41** | recovers most of it |
| Plug-in weights: bias | K=60, Dbar/A=4 | **+0.58** on A=1 | exp09 section 4 again |
| GVF-on-all weights: bias | K=60 / K=200, Dbar/A=4 | **+0.075 / +0.030** | O(1/K) dilution |
| GVF-on-all beats unweighted | 12 cells | **12/12** | efficiency 0.71--1.00 vs 0.33--0.78 |
| GVF-on-all beats cross-fitting | 12 cells | **12/12** | splitting is not what pays |
| Split beats its matched half-sample baseline | 12 cells | **12/12** | the weighting works |
| Split beats full-sample unweighted | 12 cells | **6/12** | all six at Dbar/A=4 |
| Gain degrades with GVF misfit | K=200, Dbar/A=4 | **0.963 / 0.893 / 0.707** | sigma_e = 0 / 0.3 / 0.6 |
| Weighting removes boundary estimates | K=60, Dbar/A=4 | at-zero **0.198--0.237 -> 0.017--0.057** | unweighted -> gvf_all |
| No extreme-weight pathology | all arms | max share **0.012--0.081** | oracle comparable |

### Part B — containment of the oracle band

| claim | cell | value | note |
|---|---|---|---|
| Bonferroni reference contains the oracle band | 12 cells | **0.9998--1.0000** | requirement 1 - eta = 0.95 |
| exp12-style band does not | 12 cells | **0.940--0.994** | 0.940 is 3.9 MC SE below 0.95 |
| Price of the guarantee | 12 cells | **1.28--1.89** vs **1.10--1.53** | width over the oracle band |
| Simultaneous lower limits are near-exact | 12 cells | **0.974--0.977** | nominal 0.975 |
| The scale upper limit is not | Dbar/A=1 | **0.963--0.969** | nominal 0.975; second cause of the shortfall |
| Coverage, guaranteed 0.90 | 12 cells | guard **0.984--0.999**, exp12 **0.965--0.992** | oracle 0.949--0.953 |

## From exp14 (verified, `results/exp14_chain.csv`)

8 main cells at 20,000 replicates plus bootstrap, rate and leverage blocks.
$\nu=10$, $\eta_1=\eta_2=0.025$, $\alpha_0=0.05$, guaranteed 0.90. Protocol:
`docs/PROTOCOL_exp14_chain.md`. **Supersedes the exp13 Part B claim that a
guaranteed construction had been obtained.**

| claim | cell | value | note |
|---|---|---|---|
| chi-square pivot limit covers | 8 cells | **0.9998--1.0000** | nominal 0.975, MC SE 0.0011 |
| Normal limit on the unweighted estimator undercovers | 8 cells | **0.962--0.992** | reproduces exp13's 0.963--0.969 |
| **Normal limit on the GVF estimator is the worst** | K=60, Dbar/A=4, sigma_e=0.6 | **0.8998** | best RMSE, worst coverage |
| Graybill-Wang undercovers here too | 8 cells | **0.940--0.967** | Satterthwaite dfs, mu known |
| Full-procedure bootstrap undercovers | K=60 / K=200 | **0.901 / 0.920** | B=200, 1,000 reps |
| Containment holds for every arm using v_L | 8 cells | **0.989--1.000** | requirement 0.95 |
| The exp13 containment failure was the Dhat substitution | vs exp13's 0.940 | attribution | not the scale limit |
| Price of validity in band width | 8 cells | **4--20%** | chi2_pivot vs narrowest invalid |
| Latent-target coverage, all arms | 8 cells | **0.985--1.000** | guaranteed 0.90 |
| GVF bias slope in log K | K = 60/120/240/480 | **-0.966** | bias 0.0874/0.0518/0.0227/0.0123 |
| Leverage stress did not stress the smoother | max leverage 10.8 -> 95.0 | bias **0.033 -> 0.018** | ratio GVF has uniform leverage in n |
| Information gap bound, by degrees of freedom | rho^2=0.8 | **3.15% / 7.7% / 14.9%** | nu = 10 / 4 / 2 |

## From exp15 (verified, `results/exp15_diagnosis.csv`, `_unknown_mean.csv`, `_normal_compare.csv`)

$K\in\{60,200\}$, $\bar D/A=4$, $\sigma_e\in\{0,0.6\}$, $\nu=10$, 20,000
replicates; jackknife 2,000; bootstrap 400 outer $\times$ $B=2{,}000$
(MC SE 0.0078). Protocol: `docs/PROTOCOL_exp15_diagnosis.md`.
**Supersedes the exp14 reading that estimation improvements cannot reach an interval.**

| claim | cell | value | note |
|---|---|---|---|
| Standardised error has a heavy left tail | K=60, sigma_e=0.6 | 2.5% quantile **-3.25** | reference -1.96 |
| A fixed denominator removes it | same cell | **-1.54**, coverage 0.996 | variance at true D_i |
| SE at the smoothed D is understated | K=60, sigma_e=0.6 | ratio **0.891** | at Dhat: 1.012 |
| Correcting the argument alone is not enough | K=60, sigma_e=0.6 | coverage 0.911 -> **0.952** | nominal 0.975 |
| Whole-procedure jackknife fixes magnitude, not tail | 4 cells | ratio 0.972--1.038, coverage **0.919--0.959** | tail -2.35 to -3.18 |
| Basic bootstrap at B=200 was most of the defect | 4 cells | **0.895--0.953** | exp14's choice |
| Percentile bootstrap at B=2,000 | 4 cells | **0.953 / 0.960 / 0.973 / 0.988** | nominal 0.975 |
| The corrected limit is much tighter than the pivot | 4 cells | mean A_U **1.79--2.73 vs 4.39--5.66** | true A = 1 |
| Pivot spends almost none of its budget | 4 cells | coverage **1.000** | guarantee 0.95 |
| Q ~ chi2_{K-p} under an unknown mean | K=60,200, p=1,3 | KS p **0.10--0.55** | mean/var match |
| Its limit covers | same | **1.000** | guarantee 0.95 |
| Conformal narrower than normal model on the same A_U | K=60 / K=200 | **1.145 / 1.069** | normal over conformal |

## From exp16 (verified, `results/exp16_band_comparison.csv`)

8 cells, 2,000 outer replicates, $B=2{,}000$, $\nu=10$, $\eta_1=\eta_2=0.025$,
$\alpha_0=0.05$, guaranteed 0.90. MC SE 0.0035 near 0.975, 0.0067 near 0.90.
Protocol: `docs/PROTOCOL_exp16_band_comparison.md`.
**Supersedes exp15's readings on bootstrap validity and on the normal comparison.**

| claim | cell | value | note |
|---|---|---|---|
| Scale-limit gain | 8 cells | A_U ratio **0.40--0.66** | percentile over pivot |
| **Band gain is far smaller** | 8 cells | band ratio **0.861--0.967** | 3--14 percent |
| Realised gain is below the sqrt bound | K=200, Dbar/A=4 | 0.861 vs bound 0.632 | elasticity 0.351, max 0.5 |
| Gain tracks the design share, not K | Dbar/A = 4 / 1 | **12--14% / 3.3%** | elasticity 0.35 / 0.22 |
| Latent-target coverage, pivot band | 8 cells | **0.986--1.000** | guaranteed 0.90 |
| Latent-target coverage, percentile band | 8 cells | **0.983--0.999** | guaranteed 0.90 |
| Containment does not degrade | 8 cells | **0.9965--1.0000** | requirement 0.95 |
| Bootstrap form is worth | 8 cells | **3--8 points** | basic vs percentile, same draws |
| Bootstrap count is worth | 8 cells | **0.1--0.9 points** | B = 200 vs 2,000, same draws |
| Percentile limit undercovers everywhere | 8 cells | **0.939--0.968** | nominal 0.975; exp15's 0.973/0.988 not replicated |
| Normal band narrower on a tight limit | 8 cells | **0.776--0.981** | exp15 found the reverse on the loose pivot limit |

## From exp17 (verified, `results/exp17_complex_sample.csv`)

8 cells, 2,000 replicates, $B=1{,}000$. Finite populations, 4 strata $\times$ 20
PSUs $\times$ 10 units, SRSWOR of 5 PSUs per stratum, $\nu=16$. Estimand
$F_c(t_0)$; target a newly generated population. $\eta_1=\eta_2=0.025$,
$\alpha_0=0.05$, guaranteed 0.90. MC SE 0.0067. Protocol:
`docs/PROTOCOL_exp17_complex_sample.md`.

| claim | cell | value | note |
|---|---|---|---|
| Design share reached | 8 cells | Dbar/A **0.038--0.126** | national-like, not regional |
| Design effect | sigma_alpha = 0.2 / 0.6 | **0.81 / 1.71** | one-stage cluster |
| Normality fails at the tail quantile | t0 = 0.15 | skew **0.92--1.10**, kurt **0.93--1.40** | KS p = 0 |
| Chi-square law rejected, conservative direction | 8 cells | var **20.5--23.1** vs 32 | mean 15.98--16.00 vs 16 |
| Design variance is sometimes exactly zero | t0 = 0.15 | Pr(D=0) **2e-5**, Pr(Dhat=0) **0.0013--0.0021** | no variance model covers it |
| Dhat and Y correlated at the tail | t0 = 0.15 / median | **0.80--0.84 / 0.00** | exp09 sec.7.1 realised |
| **Oracle band covers** | 8 cells | **0.942--0.959** | nominal 0.950; (S) holds to +-0.008 |
| Pivot scale limit holds its guarantee | 8 cells | **0.953--0.998** | guarantee 0.95 |
| Fitting the mean costs almost nothing | 8 cells | 0.001--0.007 on A_U | band unchanged to 3 dp |
| **Percentile limit fails at the tail** | t0 = 0.15 | **0.852--0.908** | nominal 0.975; 0.952--0.984 at the median |
| All bands cover the latent target | 8 cells | **0.947--0.965** | guaranteed 0.90 |
| Containment of the oracle half-width | 8 cells | piv **1.000**, pct **0.9995--1.000** | requirement 0.95 |
| Pivot band over the oracle band | 8 cells | **1.009--1.078** | exp16 gave 1.31--2.03 at higher design share |
| Normal interval wider here | 8 cells | **1.114--1.198** | reverses exp16; elasticity 0.02--0.06 |

## From exp18 (verified, `results/exp18_regional_share.csv`)

16 cells, 2,000 replicates, $B=500$, $\sigma_\alpha=0.4$, procedures fixed by
exp16. $\eta_1=\eta_2=0.025$, $\alpha_0=0.05$, guaranteed 0.90. MC SE 0.0067
near 0.90. Protocol: `docs/PROTOCOL_exp18_regional_share.md`.

| claim | cell | value | note |
|---|---|---|---|
| Design shares reached | 16 cells | Dbar/A **0.20--0.75** (rho 0.41--0.66) | the manuscript's regional range |
| Oracle correction is worth | 16 cells | **8.8--24.5%** of width | so the test is real |
| Two routes differ at matched share | small_sample / low_signal | nu **4--8 / 16**, skew **0.7--0.9 / 0.2--0.5** | Pr(Dhat=0) **20.9% / 0%** |
| **Simultaneous lower limits fail at the tail** | small_sample, t0=0.15 | **0.445--0.834** | requirement 0.975; exp17's inference was wrong |
| That failure worsens with K | S2 tail, K=60 / 200 | **0.718 / 0.445** | Bonferroni at eta2/K reaches further into a wrong tail |
| Correlation decomposes | tail cells | between **0.78--0.95**, within **0.52--0.67** | exp17 pooled them |
| Pivot band coverage | 16 cells | **0.9615--0.9860** | guaranteed 0.90 |
| **Oracle band undercovers at the tail** | small_sample S2, t0=0.15, K=200 | **0.9315** | nominal 0.950, 2.8 MC SE; not a variance problem |
| **Corrected band vs not correcting** | 16 cells | **0.934--0.991** | 0.9--6.6 percent narrower |
| **Share of the oracle narrowing captured** | 16 cells | **6--31%** | mechanism: A bounded up and v bounded down compound |
| Against the manuscript's 15--19% | low_signal S2, median | oracle **19.5%**, feasible **4.9%** | same figure, a quarter delivered |

## From exp19 (verified, `results/exp19_headroom.csv`)

8 cells, 2,000 replicates, same generation and seeds as exp18, largest design
shares only. **No method proposed**; the same band function at mixed arguments.
Protocol: `docs/PROTOCOL_exp19_headroom.md`.

| claim | cell | value | note |
|---|---|---|---|
| Bounding D costs more than bounding A | 8 cells | **0.136--0.332 vs 0.074--0.204** | width loss over oracle |
| Bounding A alone, with TRUE D_c | 8 cells | **7--20%** | a joint set over D does not touch this |
| Multiplicity share of the current loss | 8 cells | **6--22%** | grows with K, but minor |
| Captured share of the oracle narrowing, now | 8 cells | **6--27%** | |
| Captured share with multiplicity removed | 8 cells | **12--42%** | invalid procedure; a ceiling, not an option |
| Marginal lower limits are wildly invalid | K=200, t0=0.15 | coverage **0.0005--0.0085** | requirement 0.975 |
| Band coverage barely moves when they fail | same cells | **0.970--0.976** | guaranteed 0.90 |

## From exp20 (verified, `results/exp20_ratio_pivot.csv`)

Model R: $Y_c\sim N(0,A+d a_c)$, $a_c$ **known**, $\nu_c\widehat D_c/(d a_c)\sim
\chi^2_{\nu_c}$. 16 cells, 20,000 replicates, $\eta=\alpha_0=0.05$, guaranteed
0.90. MC SE 0.0015 near 0.95. Protocol:
`docs/PROTOCOL_exp20_ratio_pivot.md`; specification `docs/THEORY_ratio_pivot.md`.

| claim | cell | value | note |
|---|---|---|---|
| Ratio pivot is exact | 16 cells | level mean **0.9498**, range 0.9465--0.9538 | nominal 0.95 |
| Containment equals the level | 16 cells | max difference **0.00e+00** | R monotone in t |
| Incumbent's A-limit wastes its budget | 16 cells | **0.998--1.000** | nominal 0.975 |
| Incumbent's Bonferroni limits | 16 cells | 0.973--0.978 | nominal 0.975 |
| **Ratio band narrower than the incumbent** | 16 cells | **0.797--0.907** | 9--20 percent |
| Ratio band over the oracle | 16 cells | **1.026--1.116** | incumbent 1.150--1.348 |
| **Share of available narrowing captured** | 16 cells | ratio **73--89%**, incumbent **18--38%** | exp18 gave 6--31% under a complex design |
| Coverage, all arms | 16 cells | **0.955--0.990** | guaranteed 0.90 |
| Gain grows with design share | d/A = 0.5 / 1.0 | width ratio **0.894 / 0.826** | mean over cells |
| Gain grows with K | K = 60 / 200 | **0.870 / 0.850** | Bonferroni charges per limit |
| Gain is flat in the dispersion of a_c | slog_a = 0.5 / 1.2 | **0.859 / 0.861** | prediction V4 was wrong |
| Scope | -- | a_c **known** | not a survey-ready method; route (b) decides the line |

## From exp21 (verified, `results/exp21_estimated_structure.csv`)

16 cells, 10,000 replicates, $\gamma_0=1$, one total budget $\alpha_0+0.05=0.10$
for every arm. Correctly specified and misspecified blocks reported separately.
Protocol: `docs/PROTOCOL_exp21_estimated_structure.md`.
**A key collision that overwrote the $C_\gamma$ coverage column was fixed and the
experiment rerun before any number here was read.**

| claim | cell | value | note |
|---|---|---|---|
| C_gamma is exact | 8 correctly specified cells | mean **0.9752**, range 0.9716--0.9777 | nominal 0.975, MC SE 0.0016 |
| Supremum is grid-insensitive | all cells | **0.0000** | 31 vs 61 points |
| Inversion fallback never used | all cells | **0.0** | corrected rule t_L = 0 |
| **Pooling: captured share** | 8 cells | **0.20--0.31 -> 0.63--0.80** | incumbent -> same with known a_c |
| **Direct ratio adds only** | 8 cells | width ratio **0.958--0.987** | 1.3--4.2 percent, captured +0.06--0.11 |
| C_gamma containment | 8 cells | **0.983--0.986** | requirement 0.95 |
| C_gamma captured share | 8 cells | **0.63--0.80** | back to where sep_struct was |
| C_gamma vs the incumbent | 8 cells | **0.817--0.926** | 7--18 percent narrower |
| Plug-in gamma is fine when correct | 8 cells | containment **0.944--0.949** | prediction U5 was wrong |
| **Plug-in fails under misspecification** | 8 cells | **0.821--0.898** | requirement 0.95 |
| **C_gamma also fails under misspecification** | 8 cells | **0.899--0.964** | below 0.95 in half the cells |
| The incumbent does not | 8 cells | **1.000** | it assumes no structure |

## From exp22 (verified, `results/exp22_completion.csv`)

16 cells, 10,000 replicates, total budget $\alpha_0+\eta=0.10$ every arm; ratio
arm splits $\eta$ two ways, component arm three. Protocol:
`docs/PROTOCOL_exp22_completion.md`.

| claim | cell | value | note |
|---|---|---|---|
| Endpoint lemma for the structure minimum | -- | **exact** | log a_c concave in gamma; verified numerically |
| Envelope dominates the grid maximum | 16 cells | **1.000** | as the lemma requires |
| Cost of certification | 16 cells | **1.005--1.019** | width over the grid maximum |
| Grid minimiser of t_L at an endpoint | 16 cells | **0.9999--1.0000** | evidence, not a theorem; the item still owed |
| Structure-set coverage | 8 correct cells | **0.9718--0.9775** | nominal 0.975 |
| Envelope containment, correct structure | 8 cells | **0.9931--0.9973** | requirement 0.95 |
| Component containment, correct structure | 8 cells | **0.9975--0.9988** | requirement 0.95 |
| Latent-target coverage, both | 8 cells | **0.960--0.978** | guaranteed 0.90; oracle 0.947--0.952 |
| **Ratio envelope vs matched component-wise** | 8 cells | **0.977--0.993** | 0.7--2.3 percent narrower |
| Captured share | 8 cells | envelope **0.53--0.78**, component **0.53--0.75**, incumbent **0.20--0.31** | |
| **Envelope loses containment under misspecification** | 8 cells | **0.930--0.981** | below 0.95 in three cells |
| Component-wise degrades more gracefully | 8 cells | **0.958--0.992** | a reason to keep it |
| The structure-free incumbent does not degrade | 8 cells | **1.000** | it assumes no structure |

## From exp23 (verified, `results/exp23_certified.csv`)

Same generation and seeds as exp22. 16 cells, 10,000 replicates,
$\eta_\gamma=\eta_t=0.025$, $\alpha_0=0.05$, guaranteed 0.90. Protocol:
`docs/PROTOCOL_exp23_certified.md`.
**Supersedes exp22's endpoint evaluation, which is retracted.**

| claim | cell | value | note |
|---|---|---|---|
| **Endpoint claim for t_L is false** | review's counterexample, K=6 | endpoints 0.10974 / 0.12106, **interior 0.09121** | smaller endpoint 20.3% above the infimum |
| Certified bound on the counterexample | same | **0.08924** vs true inf 0.09121 | valid |
| Certified bound, stress test | 300 random configurations | **0 violations** | 401-point reference, rel. tol. 1e-9 |
| Its tightness | 300 configurations | median **0.941**, 5--95% 0.796--0.990 | below the infimum by design |
| Certified envelope dominates the grid | 16 cells | **1.000** | on every replicate |
| Cost of certification | 16 cells | **1.007--1.029** | exp22 claimed 0.5--1.9 percent |
| Fallback t = 0 used | 16 cells | **0.0** | |
| Structure-set coverage | 8 correct cells | **0.972--0.978** | nominal 0.975, MC SE 0.0016 |
| Certified containment | 8 correct cells | **0.9953--0.9988** | requirement 0.95 |
| Latent-target coverage | 8 correct cells | **0.961--0.977** | guaranteed 0.90; oracle 0.947--0.952 |
| **Captured share, certified** | 8 correct cells | **0.574--0.768** | incumbent 0.205--0.306 |
| **Band vs the structure-free incumbent** | 8 correct cells | **0.835--0.935** | 6.5--16.5 percent narrower |
| Band vs the component-wise arm | 8 correct cells | **0.985--0.996** | that arm is **not** certified |
| Containment under misspecification | 8 cells | **0.941--0.989** | below requirement in one cell |

## From exp24 (verified, `results/exp24_survey_structure.csv`)

16 cells, 2,000 replicates, finite populations with varying sampled-PSU counts;
structure variable $x_c=m_c$ fixed before running; $\alpha_0=0.05$,
$\eta_\gamma=\eta_t=0.025$. Protocol:
`docs/PROTOCOL_exp24_survey_structure.md`. A sign error in one diagnostic was
fixed and the experiment rerun before any number here was read.

| claim | cell | value | note |
|---|---|---|---|
| Structure explains, median | 8 cells | R2 **0.63--0.79** | sample size only |
| Structure explains, tail quantile | 8 cells | R2 **0.17--0.26** | p(1-p) and clustering not carried |
| Best-fitting exponent and its spread | tail cells | gamma_ls 1.14--1.56, **sd up to 5.5** | |
| Dhat--Y dependence at the tail | 8 cells | **0.57--0.71** | 0.00 at the median |
| **Certified containment fails** | 16 cells | **0.366--0.989** | requirement 0.95 |
| Worst containment where C_gamma is best | S1 median, K=200 | contains gamma_ls **0.991**, containment **0.368** | the failure is model error |
| Fallback never fired | 16 cells | **0.0** | not a computational failure |
| Latent-target coverage holds | 16 cells | **0.943--0.963** | guaranteed 0.90; empirical conservatism only |
| **Width gain collapses** | 16 cells | **0.959--0.998** vs incumbent | 6.5--16.5 percent in the closed model |
| Design shares reached | 16 cells | **0.05--0.26** | available narrowing only 1.2--15.5 percent |
| Two cells report captured > 1 | S1 median | band below the oracle where containment is 0.37 | the statistic stops meaning anything there |

## From exp25 (verified, `results/exp25_high_share.csv`)

16 cells, 2,000 replicates, method/structure variable/budget unchanged from
exp24. Realised $\bar D/A=0.541$--$0.752$ ($\rho^2=0.351$--$0.429$). Protocol:
`docs/PROTOCOL_exp25_high_share.md`. **Completes the agreed validation range.**

| claim | route / cell | value | note |
|---|---|---|---|
| Design shares reached | 16 cells | Dbar/A **0.541--0.752**, rho2 **0.351--0.429** | the agreed targets |
| Structure explanatory power | low_signal / small_sample | R2 **0.59--0.85 / 0.05--0.71** | worst at the tail quantile |
| Zero variance estimates | small_sample | Pr(Dhat=0) up to **0.171** | Pr(D=0) up to 0.0033 |
| **Containment holds on low_signal** | 8 cells | **0.955--0.992** | requirement 0.95 |
| **Containment fails on small_sample** | tail cells | **0.681--0.780** | width there is not usable |
| Latent-target coverage | 16 cells | **0.944--0.975** | guaranteed 0.90 |
| **Band vs the structure-free incumbent** | low_signal / all | **0.883--0.937 / 0.836--0.937** | 6.3--16.4 percent narrower |
| Captured share | low_signal | **0.56--0.74** vs incumbent **0.23--0.30** | |
| **Corrects exp24** | -- | exp24 sat at Dbar/A 0.053--0.262 | available narrowing was only 1.2--15.5 percent there |
| True structure recovers part of containment | small_sample tail | **0.682 -> 0.815**, **0.770 -> 0.888** | does not reach 0.95 |
| So the cause is structure **and** the F conditions | small_sample | both | better structure modelling alone insufficient |
| True-structure arm on low_signal | 8 cells | 0.937--0.952 | below the certified arm, which pays for C_gamma |
| Diagnostic exclusions recorded | small_sample tail K=200 | **0.483** of replicates | that arm only; nothing substituted |
| Fallback t = 0 | 16 cells | **0.000** | |

### exp25 addendum — like-for-like subset check

Every arm rescored on the subset the diagnostic can use (all $D_c>0$), since
excluding replicates from one arm only is not a comparison.

| claim | cell | value | note |
|---|---|---|---|
| Certified containment, all replicates vs common subset | small_sample tail, K=200 | **0.6815 / 0.6763** | exclusion 0.483 |
| Certified vs true-structure on the common subset | small_sample tail, K=200 | **0.676 vs 0.815** | contrast unchanged |
| Same, K=60 target 0.75 | small_sample tail | **0.771 vs 0.908** | contrast unchanged |
| The exclusion does not carry the finding | 4 affected cells | confirmed | |

## From exp26 (verified, `results/exp26_same_target.csv`)

16 cells, 10,000 replicates, Model R with estimated structure. Both arms target
$\theta_{\mathrm{new}}=\mu+u_{\mathrm{new}}$ and spend the identical budget
$\alpha_0+\eta_\gamma+\eta_t=0.10$; the competitor's split was scanned and the
narrowest valid choice given to it. Protocol:
`docs/PROTOCOL_exp26_same_target.md`.

| claim | cell | value | note |
|---|---|---|---|
| All valid arms cover | 16 cells | conformal **0.957--0.978**, Gaussian **0.982--0.996** | guaranteed 0.90 |
| **Conformal narrower than the Gaussian baseline** | K=60 / K=200 | **22.2% / 13.9%** | ratio 1.285 / 1.162; reduction is 1 - 1/r |
| Same with a split fixed in advance at (0.025, 0.025) | K=60 / K=200 | **25.9% / 20.4%** | the data-chosen split favours the competitor |
| Nominal levels differ and are stated | -- | conformal and Gaussian **0.90**; plug-in **0.95** | plug-in's 0.925--0.948 is short of its own 0.95 |
| Part of the width gap is conservatism | 16 cells | Gaussian realises 0.982--0.996 vs conformal 0.957--0.978 | not calibrated to the same realised level |
| Scope | -- | one constructed Gaussian baseline | not Gaussian methods or SAE methods in general |
| Gap narrows with K | K = 60 -> 200 | 1.285 -> 1.162 | G3 |
| Misspecification does not change it | 8 cells | 1.157--1.282 | they share the scale machinery |
| Budget split chosen by the competitor | K=60 / K=200 | (0.040, 0.010) / (0.045, 0.005) | scanned, best given to it |
| Plug-in Gaussian is narrower and not valid | 16 cells | coverage **0.925--0.948** | its own nominal is 0.95 |
| Computation does not distinguish them | 16 cells | shared scale 0.27--0.80 ms; band step 0.0005--0.003 ms | per replicate |
| Qualification | -- | one valid Gaussian construction, not the best possible | claim is about this comparator |

## From exp27 (verified, `results/exp27_ess_scalar.csv`, `exp27_ess_exclusions.csv`)

ESS rounds 9--11 via the portal API, 127,286 respondents, 825 region-rounds,
45 configurations (3 items $\times$ 3 rounds $\times$ 5 minimum region sizes).
Target $F_{cr}(4)$; structure variable = sampled PSU count; $\alpha_0=0.05$,
$\eta_\gamma=\eta_t=0.025$; Gaussian split fixed at (0.025, 0.025). Protocol:
`docs/PROTOCOL_exp27_ess_scalar.md`. **No latent-target coverage is claimed.**

| claim | value | note |
|---|---|---|
| Regional design share on ESS | rho2-hat **0.25--0.68** | the regime the correction is for |
| Design df per region | median **22--29**, q10 8, q90 180--339 | ample |
| Excluded: nu < 2 | **18 of 825** cells | every item |
| Dhat = 0 cells | **13 / 39 / 55** | trstprl / stflife / happy; given v_L = 0 |
| Fallback t = 0 | **0 of 45** configurations | |
| Normality support, `trstprl` | skew **-0.47..0.62**, excess kurt **0.3--4.4** | best supported |
| Normality support, `stflife` / `happy` | skew up to **2.30 / 2.81**, kurt up to **12.6 / 17.6** | clearly not supported |
| Structure fit, R2 of log Dhat on log x | `trstprl` **0.12--0.65**, `stflife` 0.001--0.57, `happy` 0.0002--0.47 | understates the fit to true D by psi'(nu/2) ~ 0.074--0.098 |
| Implausible structure fit flagged | `happy`, round 9, n>=150: gamma-hat **-0.33**, C_gamma excludes 0 | family does not fit |
| **Certified vs matched Gaussian** | **0.686--0.964, narrower in 45 of 45**, median 0.854 | 3.6--31.4 percent; reproduces exp26 |
| Certified vs uncorrected | **0.647--0.953** | narrows by 4.7--35.3 percent |
| **Certified vs structure-free: mixed** | **0.695--1.125** | sometimes 30% narrower, sometimes 12% wider |
| **The payoff tracks an observable diagnostic** | corr(R2, cert/sep) = **-0.54** | R2 < 0.20: median **1.048**; R2 >= 0.40: median **0.908** |
| That association was **not** pre-specified | -- | found post hoc in these 45 configurations; needs a second survey system |

## From exp28 (verified, `results/exp28_centring.csv`) — supersedes part of exp27

Same data, configurations and row sets as exp27 ($K$ identical, uncorrected radii
identical to machine zero). Design variance recomputed from the Taylor
linearisation of the deviation $\widehat F_{cr}-\widehat F_c$. Protocol:
`docs/PROTOCOL_exp28_centring.md`.

| claim | value | note |
|---|---|---|
| D_dev / D_region | median **0.952--0.963**, q10 0.80, q90 1.16--1.28 | exceeds 1 in 26--33% of cells |
| Reduction grows with the region's weight share | quartiles **0.99 / 0.97 / 0.94 / 0.84** | M2 |
| **Structure exponent becomes physical** | median gamma-hat **0.531 -> 1.140** | gamma = 1 is D ~ 1/n |
| **C_gamma contains gamma = 1** | **0 of 45 -> 17 of 45** | with the wrong variance, never |
| Implausible negative gamma-hat disappears | `happy` round 9 | was -0.33 with C_gamma excluding 0 |
| Structure R2 falls and compresses | 0.000--0.653 -> **0.091--0.225** | log D_dev is the noisier quantity |
| **Certified vs matched Gaussian survives** | 0.729--1.014, **44/45 narrower**, median **0.821** | exp27 gave 0.854; both arms share the variance |
| Certified vs structure-free becomes favourable | mixed -> **0.459--1.034, 43/45 narrower**, median 0.830 | the exp27 version is withdrawn |
| Certified vs uncorrected | **0.422--0.867**, median 0.730 | |
| Design share, corrected | rho2-hat **0.219--0.612** | |
| **The R2--payoff association weakens** | corr **-0.54 -> -0.30** | downgraded to an exploratory diagnostic, not a criterion |
| **Induced within-country correlation** | **-0.232 / -0.116 / -0.046 / -0.029** by region count | matches -1/(n_r - 1) almost exactly |
| Fixing the variance does not fix exchangeability | -- | ESS carries no theorem guarantee |

## From exp29 (verified, `results/exp29_scale_law.csv`, `exp29_split_scan.csv`)

Fresh grid: $K\in\{40,120,400\}$, $\rho^2\in\{0.20,0.45,0.70\}$,
$\nu\in\{6,20\}$, $\sigma_{\mathrm{mis}}\in\{0,0.5\}$; 10,000 replicates.
**Predicted values were written into `docs/PROTOCOL_exp29_scale_law.md` before
the run.** Derivation: `docs/THEORY_scale_sensitivity.md`.

| claim | value | note |
|---|---|---|
| Exchange identity S1 | **0 violations in 200,000 random cases** | exact, no approximation |
| **P-C: dependence on the budget split** | error **identical to 6 decimals (1.2774%)** across six splits | predicted ratio spans 0.6225--0.8188 |
| P-C monotone, no crossing | **both hold** | as registered |
| **P-A: level — FAILS as registered** | worst cell **7.07%** against a 5% tolerance | K=40, rho2=0.70, misspecified |
| Failure located: one constant per K | c = **1.0496 / 1.0171 / 1.0066** at K = 40 / 120 / 400 | (c-1)K = 1.98 / 2.06 / 2.66 |
| Refined law (1 + 1.92/K) | max error **2.17%** (was 7.07%), mean +0.15% | constant fitted, not derived |
| **P-B: invariance — asymptotic, not exact** | within-K spread **0.0200 / 0.0110 / 0.0089** | registered tolerance 0.02 |
| Residual is systematic in rho2 | 0.7171 / 0.7194 / 0.7270 at rho2 = 0.20/0.45/0.70, K=40 | strong invariance claim refuted |
| Coverage, both arms, all 42 cells | conformal **0.954--0.990**, Gaussian **0.985--0.999** | guaranteed 0.90 |


---

## exp30 — a necessary condition matching the two-axis boundary (2026-09-10)

Protocol: `docs/PROTOCOL_exp30_necessary_condition.md`. Theory:
`docs/THEORY_optimality.md`. Deterministic; no Monte Carlo error.
Equal-design-variance submodel, `eta = 0.05`, exact separation of the two points.

| claim | cells | value | note |
|---|---|---|---|
| Closed-form Hellinger affinities correct | 2 | max error **2.4e-12** | vs numerical quadrature |
| **Necessary condition, same dependence as (S)** | 16 | `nu_tot >= L(eta) rho^4 / (eps^2 (1-rho^2)^2)` | constant -> **L(0.05)=0.8304** |
| Sufficient never below necessary (P-2) | 16 | **no violation** | a violation would be a bug |
| Constant gap, sufficient / necessary | 16 | **2.37--14.5**, -> **2.44** at eps=0.005 | predicted limit `z^2/(2L) = 2.31` |
| **Reciprocal duality of the two axes (N2)** | 16 | identity error **8e-14** | axes agree to 9e-9 |
| P-3 (the two axes differ) | 16 | **refuted** | they are identical |

**Scope, and it is narrow.** The bound is on **certifying kappa**, not on the
width of a valid interval: no width lower bound is proved and **no optimality is
claimed for the interval**. Le Cam's two-point method is textbook; with equal
design variances the model is the balanced one-way random-effects model and the
group-versus-replicate design trade-off for the intraclass correlation is an
existing literature (Donner 1986; Zou 2012; Shieh 2024). Nothing here is claimed
as new. The heteroscedastic case is untouched.

**Correction recorded.** The first version of this argument linearised the
separation as `delta = 4 eps` rather than solving `((1+eps)/(1-eps))^2 - 1`. That
places the two points too close together and **inflates the lower bound** — by
11% at `eps = 0.05`. The error was in the unsafe direction. All numbers above use
the exact solve.
