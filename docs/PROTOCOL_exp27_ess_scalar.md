# Protocol — exp27: the fixed procedure on ESS, scalar target

Written 2026-09-10, **before any estimate is computed from the microdata**.
Everything below — target, threshold, populations, structure variable, variance
estimator, comparators, error budget — is fixed here and will not be changed
after seeing results.

## What the real data can and cannot show

The latent $\theta_{K+1}$ is unobserved in ESS. **No latent-target coverage is
claimed or computed here.** A held-out region's direct estimate carries its own
sampling error and is *not* the latent truth; treating it as such would be
measuring the anchor, not the correction. Latent coverage is the simulations'
job (`exp20`–`exp26`).

The real data answer three questions:

1. what survey information the structure model is built from, and how well it
   describes the observed design variances;
2. how far the proposed interval and its comparators differ **on the same data**;
3. how far the model's assumptions can be supported or checked here.

## Data

ESS rounds 9, 10, 11 integrated files, retrieved through the portal API
documented in `docs/DATA.md`; 127,286 respondents, 75 country-rounds, 31
countries, 825 region-rounds, no missingness in `region`, `stratum`, `psu`,
`prob`, `anweight`.

## Target — scalar, and pre-specified

For region $r$ in country-round $c$, the estimand is a **single CDF point**
$$F_{cr}(t_0)=\Pr\{\text{item}\le t_0\},$$
estimated by the `anweight`-weighted share. **Threshold fixed by rule, not by
inspection:** the items are 0–10 scales, and $t_0=4$ — one below the scale
midpoint — is used for all of them. No other threshold is examined.

**Items, three, chosen in advance for differing between-region heterogeneity**
and not for their results: `trstprl` (trust in parliament; the manuscript's
existing item), `stflife` (life satisfaction), `happy`. All three are reported
whatever they show.

Populations are regions, and the deviation is from the country-round estimate,
as in `exp03`/`exp07`. **The centre is therefore estimated**, where the theory of
§17–§20 assumes it known; that gap is stated with every number and is a limit on
what the guarantee covers here, not a detail.

## Design variance and its degrees of freedom

$\widehat D_{cr}$ is the stratified ultimate-cluster estimator of the weighted
CDF ordinate within the region, with $\nu_{cr}=(\#\text{PSUs})-(\#\text{strata})$
in that region. Regions with $\nu_{cr}<2$ are **reported and excluded with their
count**, not silently dropped. `exp02` found PSUs nesting in regions for 99.48
percent of respondents and failing in fifteen country-rounds; those country-rounds
are flagged in the output rather than removed.

## Structure variable — fixed now

$x_{cr}=$ **the number of sampled PSUs in the region**, a design quantity known
before any estimate is seen. This is the same choice as `exp24`/`exp25`, kept
deliberately so the simulation evidence applies to what is run here.
$a_{cr}(\gamma)\propto x_{cr}^{-\gamma}$, normalised to mean one.

## Comparators, at one budget

$\alpha_0=0.05$, $\eta_\gamma=\eta_t=0.025$; total 0.10 for every arm.

| arm | construction |
|---|---|
| `certified` | the fixed method: $C_\gamma$, certified $\underline t$, band at $\underline t,\underline a$ |
| `gaussian` | the matched competitor of `exp26`, same $C_\gamma$ and $\underline t$, split fixed at $(0.025,0.025)$ |
| `sep_bonf` | structure-free: $A_U$ plus Bonferroni lower limits |
| `uncorrected` | the observed anchor radius; **T1, no T2 claim** |

**The Gaussian split is fixed in advance here**, not scanned, because on real
data there is no criterion to scan against that is not the outcome.

## Reported

Per country-round configuration and per item: $K$, the design-degrees-of-freedom
distribution, the share of zero variance estimates, $\widehat\gamma$ and
$C_\gamma$, the $R^2$ of $\log\widehat D_{cr}$ on $\log x_{cr}$ **with the
caveat that this is a fit to the estimate and not to the true $D_{cr}$**, the
realised radius of each arm, and their ratios.

Also reported, as assumption checks that ESS can actually support: the skewness
and kurtosis of the standardised regional deviations, and the dispersion of
$\nu_{cr}\widehat D_{cr}$ against $\chi^2_{\nu_{cr}}$ pooled across regions.

## What would count as a useful result

Not a width record. **That a reader can see which input each arm needs, how much
the intervals differ on their own data, and which assumptions the data support
or contradict.** A finding that the structure model fits poorly in ESS, or that
the arms barely differ, is reported as prominently as the reverse — and, given
`exp24`, is a live possibility.

## Fixed before execution

No threshold, item, structure variable, budget or comparator is changed after
results are seen. Any region or country-round removed is counted in the output.
