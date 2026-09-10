# Protocol — exp17: the fixed procedure on a finite population and a complex sample

Written 2026-09-10, before executing `experiments/exp17_complex_sample.py`.
Predecessors: `exp16` (which fixed the procedures) and `exp01` (shape).

## What this experiment is and is not

It does **not** test whether the $\chi^2$ pivot's guarantee holds under a complex
design. That guarantee assumes normality of the population-level deviations and
a $\chi^2$ law for the design-variance estimator, and a stratified cluster sample
of a proportion satisfies neither. A simulation cannot extend a theorem's scope.

What it measures is **how stably the fixed procedure behaves when its conditions
are not met, and which violation moves which quantity.** No direction is
predicted for the coverage margin; predicting one and then designing around it
would be designing toward a result.

**No method is added.** The four constructions are those `exp16` settled on.

## Target, and the distinction that must not blur

The estimand is a **single pre-specified point of the CDF**,
$$F_c(t_0)=\frac{1}{N_c}\sum_{u=1}^{N_c}\mathbf 1\{Y_{cu}\le t_0\},$$
the finite-population share below $t_0$ in population $c$. This keeps the scalar
procedure intact while moving to the manuscript's actual estimand.

The guarantee evaluated is **prediction of a newly generated population**: each
replicate draws $K+1$ finite populations, builds the band from the $K$ observed
survey estimates, and asks whether it covers the *true finite-population*
$F_{K+1}(t_0)$. It is **not** design-based coverage for a fixed population under
repeated sampling, and the results must not be described as such.

## Generation

Population $c$: $H=4$ strata $\times$ $M=20$ primary sampling units $\times$
$n=10$ units. Unit indicator means are generated at the PSU level, which is
exact and avoids simulating units:
$$\mu_c\sim N(0,\tau^2),\quad \alpha_{chi}\sim N(0,\sigma_\alpha^2),\quad
p_{chi}=\Phi\!\Big(\frac{t_0-\mu_c-\alpha_{chi}}{\sigma_\epsilon}\Big),\quad
n\bar z_{chi}\sim\mathrm{Bin}(n,p_{chi}).$$
$\sigma_\alpha$ controls the intra-cluster correlation and hence the design
effect; $\tau$ controls the between-population variance $A$.

**Sample.** SRSWOR of $m=5$ PSUs per stratum, all units in a sampled PSU. Then
$\widehat F_c=H^{-1}\sum_h m^{-1}\sum_{i\in s_h}\bar z_{chi}$, and the design
variance is available **exactly** for this design:
$$D_c=\frac{1}{H^2}\sum_h\frac{1-m/M}{m}S^2_{ch},\qquad
S^2_{ch}=\frac{1}{M-1}\sum_i(\bar z_{chi}-\bar z_{ch})^2,$$
with the ultimate-cluster estimator $\widehat D_c$ replacing $S^2_{ch}$ by the
within-sample variance and nominal degrees of freedom $\nu=H(m-1)=16$.

$A=\mathrm{Var}\{F_c(t_0)\}$ and $\mu=E\{F_c(t_0)\}$ are computed to high
precision from an independent draw of 200,000 populations, so they are known
constants in the experiment rather than estimated within it.

## Constructions, fixed by `exp16`

| construction | role |
|---|---|
| `piv` | $\chi^2$ pivot limit, correction band — the baseline with a guarantee under the model |
| `pct` | percentile bootstrap limit, correction band — the recorded approximation |
| `pct_normal` | normal T2 interval on the **same** percentile limit |
| `oracle` | true $A$ and true $D_c$ — a diagnostic, not a competitor |

The oracle matters most here. **If the oracle band already miscovers, the problem
is not variance estimation** and no improvement to the limit will fix it; the
place to look is then the common-shape assumption or the match between the
prediction target and the construction.

Both a $\mu$-known form ($\chi^2_K$) and a $\mu$-fitted form ($\chi^2_{K-1}$,
refitting the weighted mean at each candidate $A$) are run, since a real analysis
does not know the centre.

The GVF used by `pct` regresses $\widehat D_c$ on $\widehat F_c(1-\widehat F_c)$,
which is the natural design relation for a proportion. **Note that this predictor
is a function of the estimate itself**, so the independence assumed throughout
the scalar work is violated here by construction, deliberately.

## Assumption diagnostics, recorded alongside

- skewness and excess kurtosis of $Y_c/\sqrt{A+D_c}$, whose normality the pivot needs;
- mean, variance and a Kolmogorov--Smirnov statistic for $\nu\widehat D_c/D_c$
  against $\chi^2_\nu$;
- realised correlation between $\widehat D_c$ and $Y_c$;
- realised design effect and $\bar D/A$.

These are what make a failure interpretable.

## Grid, fixed here

$K\in\{60,200\}$; $t_0$ at the population median and at the 0.15 quantile;
$\sigma_\alpha\in\{0.2,0.6\}$. 8 cells, 2,000 replicates, $B=1{,}000$.
$\eta_1=\eta_2=0.025$, $\alpha_0=0.05$, guaranteed level 0.90 for `piv` under
the model. Monte Carlo error about 0.0067 near 0.90.

## Predictions

| # | prediction | falsified by |
|---|---|---|
| X1 | the $\chi^2$ law for $\widehat D_c$ is violated measurably at $\nu=16$ | agreement with $\chi^2_{16}$ |
| X2 | $\widehat D_c$ and $Y_c$ are correlated, most at the 0.15 quantile | no correlation |
| X3 | the oracle band covers at about $m/(K+1)$ | oracle miscoverage, which relocates the whole problem |
| X4 | `piv` covers at or above 0.90 | undercoverage |
| X5 | the width ordering of `piv`, `pct`, `pct_normal` is as in `exp16` | a different ordering |

No direction is predicted for the size of the coverage margin.

## Outcomes, all reported

1. **X3 holds and X4 holds.** The procedure transfers to this design; the paper
   can state the operating conditions under which it was checked.
2. **X3 fails.** The binding problem is not the variance limit and the project
   returns to the shape assumption and the target definition, with `exp01` as the
   starting point.
3. **X3 holds, X4 fails.** The violation is located by the diagnostics, and the
   procedure gets a stated range of application rather than a repair.

No cell is dropped and no construction is added after execution.
