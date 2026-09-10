# Protocol — exp16: does the tighter scale limit survive into the band?

Written 2026-09-10, before executing `experiments/exp16_band_comparison.py`.
Predecessor: `exp15`. Scope fixed by the review: **no new estimator is added.**

## Why, and why the answer is not already known

`exp15` found the percentile bootstrap upper limit for $A$ to be 2.1 to 2.6
times tighter than the $\chi^2$ pivot on identical replicates. **That is a
statement about $A_U$, not about a band, and the two are not proportional.**
The conformal half-width is
$$h_c(A)=|Y_c|\sqrt{\frac{A}{A+L_c}},\qquad
\frac{\partial\log h_c}{\partial\log A}=\frac{L_c}{2(A+L_c)}\in[0,\tfrac12],$$
so a 2.6-fold reduction in $A_U$ can produce at most a $\sqrt{2.6}=1.62$-fold
reduction in half-width, and much less when $L_c$ is small relative to $A_U$: at
$A_U=4.7$, $L_c=1$ the elasticity is 0.088. **A ratio of mean limits must not be
used to estimate a ratio of mean widths**, which is why this experiment exists.

## What is compared, on identical replicates and one error budget

| construction | scale limit | band | status |
|---|---|---|---|
| `piv_conformal` | $\chi^2$ pivot | correction band | derivable guarantee under the normal model |
| `pct_conformal` | percentile bootstrap | correction band | approximation, no derived guarantee |
| `pct_normal` | the **same** percentile limit | normal-model T2 interval | isolates the band construction from the limit |
| `oracle` | true $A$, true $D_c$ | correction band | infeasible width reference |

Budget throughout: $\eta_1=\eta_2=0.025$, $\alpha_0=0.05$, guaranteed level
0.90 for the constructions that have one.

## Reported, linked, per cell

1. coverage of $A_U$ itself;
2. containment of the oracle half-width;
3. final latent-target coverage;
4. mean half-widths and their **paired** ratios on the same replicates.

**(2) and (3) are reported separately and neither is read from the other.**
Containment of the oracle band is sufficient for coverage, not necessary: a
construction can miss the oracle band often and still cover, and other
conservatisms can mask a failure. `exp13` and `exp14` already showed that
happening.

## The cells that failed are kept

$K\in\{60,200\}$, $\bar D/A\in\{1,4\}$, $\sigma_e\in\{0,0.6\}$, $\nu=10$.
$K=60$ is where the percentile limit undercovered in `exp15` (0.953, 0.960) and
it stays in, because a candidate procedure's range of application cannot be
judged from the conditions where it worked.

2,000 outer replicates, $B=2{,}000$; Monte Carlo error about 0.0035 on a
coverage near 0.975 and 0.0067 near 0.90.

## Block 2 — separating the two changes made in `exp15`

`exp15` changed the bootstrap form and the replicate count together, so the
improvement cannot be attributed to either. Here both are computed **from the
same resampling draws**, the $B=200$ arms using the first 200 of the 2,000:

| | $B=200$ | $B=2{,}000$ |
|---|---|---|
| basic | `exp14`'s choice | form held, count raised |
| percentile | count held, form changed | `exp15`'s candidate |

A small attribution check, not a research programme.

## Predictions

| # | prediction | falsified by |
|---|---|---|
| W1 | the width gain in the band is far smaller than the 2.6-fold gain in $A_U$, and bounded by $\sqrt{\cdot}$ | a band gain near the limit gain |
| W2 | `pct_conformal` still covers at or above the 0.90 target everywhere | undercoverage of the latent target |
| W3 | `pct_conformal` containment falls below `piv_conformal`'s, most at $K=60$ | containment holding at the pivot's level |
| W4 | the form change contributes more than the count change | the reverse, or neither |
| W5 | `pct_normal` is wider than `pct_conformal` on the same limit | the normal band winning |

## Outcomes, all reported

1. **W1 and W2 hold with a material gain.** The percentile limit becomes the
   main candidate, the pivot stays as the guaranteed baseline, and the pair goes
   to a complex-sample experiment.
2. **The band gain is negligible.** Then the scale limit is not what governs the
   width, the pivot is kept for its guarantee, and effort moves to whatever does
   govern it.
3. **W2 fails at $K=60$.** The candidate has a stated range of application and
   the small-$K$ failure is reported as a limit on it, not dropped.

No construction is added after seeing results and no cell is dropped.
