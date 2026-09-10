# PRICSSA reporting items

The journal requires this checklist for analyses of complex sample survey data
(Seidenberg, Moser, and West 2023, *JSSAM* 11, 743). Item numbering follows the
published checklist. Entries marked **AUTHOR** cannot be filled from the data
files or this repository and must be completed before submission.

Survey: European Social Survey, integrated data files, rounds 9, 10 and 11.

## 1. Survey characteristics

**1.1 Data collection dates. — AUTHOR.** Country-specific and published per
round by ESS. They are also derivable from the interview-date variables in the
integrated files, which this analysis does not retain. Tabulate by country and
round in an appendix.

**1.2 Data collection mode(s). — AUTHOR to verify.** ESS core rounds are
face-to-face interviews. Rounds 10 and 11 include self-completion in some
countries; the country-by-mode allocation must be taken from the round
documentation rather than assumed.

**1.3 Target population.** All persons aged 15 and over resident within private
households in each participating country, regardless of nationality, citizenship
or language. Persons in institutions are out of scope.

**1.4 Sample design.** Country-specific strict probability samples. Designs
include stratification and, where no adequate person or household register
exists, multi-stage selection of primary sampling units. The analysis uses the
file's own design variables: `stratum`, `psu`, `region` and the inclusion
probability `prob`.

**1.5 Survey response rate(s). — AUTHOR.** Country-specific, published per round.
Report the rate together with its definition, and state the AAPOR formula used.

## 2. Analytic information

**2.1 Missingness rates.** Respondents are retained when the item response is in
0--10, the analysis weight is positive and the region identifier is present; all
other records are dropped, including the "don't know" and refusal codes. **The
resulting item-level missingness rate is not currently reported and should be**
(`experiments/exp27_ess_scalar.py`, selection at line 73). Design variables
(`region`, `stratum`, `psu`, `prob`, and the weights) have no missingness in
rounds 9--11, verified in `exp02`.

**2.2 Observation deletion.** Regions with fewer than two design degrees of
freedom are excluded and counted: 18 of 825 region-rounds. Regions whose design
variance estimate is exactly zero are retained but receive no shrinkage, which is
conservative; there are 13, 39 and 55 of them for the three items.

**2.3 Sample sizes.** 127,286 respondents; 75 country-rounds; 825 region-rounds
before exclusions; 31 countries; median 10 regions per country-round, range
1--28. The reported comparisons cover 45 item-by-round-by-country
configurations. Per-region sample sizes drive the design degrees of freedom,
whose median is 22 to 29 depending on the round.

**2.4 Confidence intervals and standard errors.** This paper reports interval
*widths* for a latent target, not point estimates with confidence intervals, and
**claims no coverage on these data**: the latent quantity is unobserved and a
held-out region's direct estimate is not a substitute for it. Every interval
reported is built on a design-based variance estimate, never on a
simple-random-sampling variance.

**2.5 Weighting.** The design weight `dweight` is used for the direct estimates.
`anweight`, `pspwght` and `pweight` are present in the extract and are not used
for the regional estimates; positivity of `anweight` is a selection condition.

**2.6 Variance estimation.** Ultimate-cluster Taylor linearisation over primary
sampling units within strata, aggregated over the whole country-round. For the
regional score $\widehat F_{cr}-\widehat F_c$ the linearised value is

    u_i = w_i 1{i in r} (z_i - Fhat_cr) / W_r  -  w_i (z_i - Fhat_c) / W_c

so that the variance estimated is that of the *difference*, not of
$\widehat F_{cr}$. Section 6.3 of the manuscript shows this choice changes the
conclusions. Degrees of freedom are clusters minus strata within the
country-round.

**A design-file limitation, disclosed.** `exp02` audited whether sampling units
nest inside regions. Nesting holds for 99.48% of respondents but fails in fifteen
country-rounds, and strata do not nest inside regions in 63 of 90 country-rounds.
Where nesting fails, treating regions as separable understates the dependence.

**2.7 Subpopulation analysis.** The analysis unit is the region within a
country-round, and the centring quantity $\widehat F_c$ is computed over the
whole country-round rather than on a subset, so the linearised values are formed
on the full country-round file.

**2.8 Suppression rules.** No estimate is suppressed. Exclusions are by design
degrees of freedom only, as in 2.2, and are counted in the manuscript.

**2.9 Software and code.** Python 3 with NumPy, SciPy and pandas; no
survey-specific package is used, and the linearisation is implemented directly
and tested. All code, protocols and result tables are in the replication
materials, including the retrieval script for the ESS files.

**2.10 Singleton problem.** Taylor linearisation requires at least two clusters
per stratum. `exp02` found twelve countries carrying degenerate primary sampling
unit identifiers, and regions with fewer than two design degrees of freedom are
excluded rather than given a singleton adjustment. **State this exclusion rule in
the paper**; it is in Section 6.

**2.11 Public/restricted data.** ESS integrated data files are freely available
after registration under the ESS End User Licence. They are not redistributed
with this work; a retrieval script obtains them through the portal's API and
caches them outside the replication materials. No user identifier is stored.

**2.12 Embedded experiments. — AUTHOR to verify.** Rounds 10 and 11 include
mode-related methodological work in some countries. Confirm against the round
documentation whether any affects the three items used here.

## Items this analysis cannot satisfy, stated plainly

The manuscript's guarantee is proved under a normal model with a known centre and
independent populations. On these data the centre is estimated, the scores carry
a measured dependence of about $-1/(n_r-1)$, two of the three items are badly
non-normal, and no $\chi^2$ law for a complex-design variance estimator is
established. The analysis is reported as an application under those stated
approximations, with the guarantee not attached to it.
