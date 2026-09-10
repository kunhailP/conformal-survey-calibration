# Protocol — exp12: closing the scalar heteroscedastic case

Written 2026-09-10, before executing `experiments/exp12_closing_scalar.py`.
Predecessors: `exp09`, `exp10`, `exp11`. Responds to three objections raised in
review of `exp11`, none of which is answered by more coordinates.

## Why, and a retraction

`exp11` reported that unequal design variances reduce the effective population
count to as few as 14 of 100 and called the scalar case closed. **The second
claim was premature and the first conflated two quantities.** Recomputed
directly, at $K=100$, $A=1$, mean $D=4$:

| $D_i$ | $\nu_{\mathrm{den}}$ | $K_I=\sum_i(A/(A+D_i))^2$ | RSE of unweighted $\widehat A$ | information bound |
|---|---|---|---|---|
| all $4$ | 99.0 | 4.00 | 0.711 | 0.707 |
| 50 at $0.1$, 50 at $7.9$ | 61.8 | **41.95** | 0.900 | **0.218** |

Heteroscedasticity **raises** the Fisher information by a factor of ten while
**lowering** the precision of the unweighted sample variance. The two move in
opposite directions. So $\nu_{\mathrm{den}}$ is the effective degrees of freedom
of one statistic, not the information in the data, and the two must never be
reported as a single $K_{\mathrm{eff}}$.

That turns the interesting question around:

> **Is information destroyed by unequal design variances, or discarded by
> summarising them with an unweighted variance?**

## Three questions, in order

### Q1. Which oracle band is the manuscript's, and is it the one being widened?

Under (S) with unequal $v_c$, the manuscript's Section 3 standardises **per
population**, $M_c=|Y_c|/\sqrt{s_G^2+v_c^2}$, and places the band at $s_G$.
Call this construction (a); its coverage is exactly $m/(K+1)$ by exchangeability
of the $W_c$.

`exp07_widths.py` does something else. `s_plug = dep.std(axis=0)` is common
across populations, so the scores are $|Y_c|/\widehat s_Y$ and the band is
$|Y|_{(m)}\widehat\kappa$. Call this construction (b). `exp11` used (b) as its
"oracle" and reported empirical coverage near nominal; **that is not a
guarantee, and (b) is not what the manuscript's theory licenses.**

The two coincide under homoscedasticity. This experiment measures how far apart
they are, and whether the scalar $\kappa_U$ band of `exp11` contains the
*correct* oracle band (a).

A safe band for (a) exists: the half-width is the $m$-th order statistic of
$h_c(s)=|Y_c|\big/\sqrt{1+v_c^2/s^2}$, each $h_c$ increasing in $s$, so the
band is increasing in $s_G$ and the union over an interval is the band at its
upper endpoint. That needs an upper limit on $s_G$, not on $\kappa$. It is
built here and its coverage measured. **The substitution of $\widehat v_c$ for
$v_c$ is not covered by that argument** — $h_c$ is decreasing in $v_c$, so
plugging in an estimate is not conservative — and the size of that gap is
recorded rather than assumed away.

### Q2. Lost or discarded?

Per cell, all of: $\nu_{\mathrm{den}}$; $K_I$; $K_{I,\mathrm{eff}}$ of `exp09`;
the realised RSE of the unweighted $\widehat A=S_Y^2-\overline{\widehat D}$; the
realised RSE of the optimally weighted estimator of `exp09` Proposition 2 at
oracle weights; the same at feasible plug-in weights; and the information bound.

### Q3. A model-based competitor that is actually valid

The Gaussian plug-in interval of `exp11` fails because it ignores parameter
uncertainty, which is not news. The fair competitor uses the same Gaussian
model **and** an error budget: $\pm z_{1-\alpha_0/2}\sqrt{A_U}$ with $A_U$ a
one-sided Graybill–Wang upper limit at $\eta$, guaranteed at $1-\alpha_0-\eta$,
the same 0.90 as everything else. It exploits a known shape where the conformal
route does not, so it **should** be narrower, and if it is that is the honest
result.

## Grid, fixed here

$K\in\{30,100,300\}$; $\bar D/A\in\{1,4\}$; $\sigma_{\log}\in\{0,0.5,1.0,1.5\}$
lognormal with the mean held exactly; $\nu_i=10$; 20,000 replicates;
$\alpha_0=\eta=0.05$, guaranteed level 0.90. Plus the two-point cell above as a
named extreme.

## Predictions

| # | prediction | falsified by |
|---|---|---|
| S1 | oracle (a) covers at exactly $m/(K+1)$ at every dispersion | any departure beyond Monte Carlo error |
| S2 | oracle (b) departs from nominal as dispersion grows | (b) staying exact |
| S3 | the scalar $\kappa_U$ band fails to contain oracle (a) at high dispersion | containment holding throughout |
| S4 | the unweighted RSE falls far short of the bound as dispersion grows, and oracle weighting recovers most of it | the gap not opening, or weighting not closing it |
| S5 | the valid model-based interval is narrower than the safe conformal band under Gaussian truth | the conformal band winning |

## Outcomes, all reported

1. **S3 holds.** `exp11`'s construction is not the one the manuscript licenses,
   the scalar case is *not* closed, and the heteroscedastic safe band must be
   built on $s_G$ as here.
2. **S3 fails, containment holds.** Then (b) is defensible as a conservative
   approximation and the reason must be given, not observed.
3. **S4 holds.** The paper gains a second result: standard practice discards
   most of the information under realistic heteroscedasticity, and a weighted
   construction recovers it. This is larger than the band result.
4. **S5 holds.** Then the conformal route's case rests on robustness to shape,
   which is `exp01`, and the comparison table must say so plainly rather than
   claiming a width advantage it does not have.

No cell is dropped after execution and no construction is added after results.
