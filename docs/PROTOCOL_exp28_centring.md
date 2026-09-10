# Protocol — exp28: the centring–variance mismatch, measured

Written 2026-09-10, before execution. Predecessor: `exp27`. **No new method.**
This closes the last connection between the score the paper defines and the
uncertainty the analysis actually computes.

## The mismatch

`exp27` scores regions by $Y_{cr}=\widehat F_{cr}-\widehat F_c$ but uses
$\widehat D_{cr}$, the design variance of $\widehat F_{cr}$ **alone**. The
quantity the score needs is
$$\mathrm{Var}_d(\widehat F_{cr}-\widehat F_c)=\mathrm{Var}_d(\widehat F_{cr})
+\mathrm{Var}_d(\widehat F_c)-2\,\mathrm{Cov}_d(\widehat F_{cr},\widehat F_c),$$
and a centre estimated from the same sample also makes the $Y_{cr}$ **dependent
across regions of a country**. Recording that as a limitation does not connect
the theory to the application; ESS carries the design information to evaluate
it, so it is evaluated.

## What is computed

For each country-round, the Taylor linearisation of the deviation is
$$u_i=\frac{w_i\mathbf 1\{i\in r\}(z_i-\widehat F_{cr})}{W_r}
-\frac{w_i(z_i-\widehat F_c)}{W_c},$$
aggregated to PSU totals **over the whole country-round**, and
$\widehat D^{\mathrm{dev}}_{cr}$ is the stratified ultimate-cluster variance of
those totals. This is the same estimator `exp27` uses, applied to the correct
influence function.

**Degrees of freedom stay at the region level**, $\nu_{cr}=\#\mathrm{PSU}_r-
\#\mathrm{strata}_r$, rather than the country's larger count. That is the
conservative choice and it is stated rather than optimised: the deviation's
variance is dominated by the region term whenever the region is a small share of
its country, but no claim is made that this is the exact effective degrees of
freedom.

**And the induced cross-region dependence is measured too**, from the same
influence functions: for regions $r\ne r'$ of a country-round,
$\mathrm{Cov}_d(Y_{cr},Y_{cr'})$ and the implied correlation. The scalar theory
assumes independent populations, so its size is the thing to know.

## Reported

1. the distribution of $\widehat D^{\mathrm{dev}}_{cr}/\widehat D_{cr}$;
2. the mean and range of the induced within-country correlation, and how it
   varies with the number of regions in the country;
3. every `exp27` number recomputed with $\widehat D^{\mathrm{dev}}$ — the
   structure fit, $\widehat\gamma$, and the four arms' radii — so the size of the
   correction to the reported conclusions is visible.

## What this cannot do, stated in advance

**Correcting the variance does not restore exchangeability.** A common estimated
centre makes the scores dependent, and the conformal rank argument assumes they
are not. Nothing in this experiment repairs that, and no coverage claim follows
from it.

If the corrected variance leaves the `exp27` conclusions materially unchanged,
the manuscript reports ESS as an application under a **stated approximation** —
estimated centre, dependence unaddressed — **without the theorem's guarantee
attached**. If it changes them, the corrected numbers replace the earlier ones.

## Predictions

| # | prediction | falsified by |
|---|---|---|
| M1 | $\widehat D^{\mathrm{dev}}<\widehat D$ typically, since the region contributes to the centre | the ratio exceeding 1 on average |
| M2 | the reduction grows as the region's weight share grows | no relation |
| M3 | the induced within-region-pair correlation is negative and $O(1/\#\text{regions})$ | positive, or not shrinking with the region count |
| M4 | the `exp27` width comparisons move by less than their spread across configurations | a change large enough to overturn them |

No arm, item, threshold or budget is changed.
