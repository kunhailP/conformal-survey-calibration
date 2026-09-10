# Protocol — exp11: does the correction-factor upper limit survive unequal design variances?

Written 2026-09-10, before executing `experiments/exp11_heteroscedastic.py`.
Derivations: `docs/THEORY_certification.md`. Predecessors: `exp09`, `exp10`.

## Why

`exp10` established the safe band $B_U=\pm q\,\kappa_U$ under **equal** design
variances, where the exact pivot $(\widehat D/S_Y^2)/\rho^2\sim F_{\nu,K-1}$
does the work. The applications are not homoscedastic. Proposition C is the
cleanest result in the project and the one least likely to survive a real
design, so it is tested before anything is built on it.

The scope is deliberately the **scalar** target with unequal $D_i$. Unequal
scales across *coordinates* is a separate difficulty — it changes the maximum
score, the per-coordinate correction and the simultaneity — and mixing the two
would make a failure uninterpretable.

## What is actually being approximated

With $D_i$ unequal, neither side of the pivot is chi-square.

- **Numerator.** $\overline{\widehat D}=K^{-1}\sum_i D_i\chi^2_{\nu_i}/\nu_i$
  has mean $\bar D$ and variance $2K^{-2}\sum_iD_i^2/\nu_i$, giving a
  Satterthwaite $\nu_{\mathrm{num}}=K^2\bar D^2/\sum_iD_i^2/\nu_i$.
- **Denominator.** $Y_i\sim N(\mu,\sigma_i^2)$ with $\sigma_i^2=A+D_i$ are
  independent but not identically distributed, so $S_Y^2$ is a quadratic form,
  not a scaled chi-square. With $s_1=\sum\sigma_i^2$, $s_2=\sum\sigma_i^4$,
  $\mathrm{Var}(S_Y^2)=2[s_2(1-2/K)+s_1^2/K^2]/(K-1)^2$ and
  $\nu_{\mathrm{den}}=(K-1)^2(s_1/K)^2/[s_2(1-2/K)+s_1^2/K^2]$, which equals
  $K-1$ exactly when the $\sigma_i^2$ are equal.
- **Independence.** Holds by construction in this model and is false in the
  application (`exp09` §7.1). Recorded, not tested here.

**Matching two moments on each side does not make the ratio an $F$.** The point
of this experiment is therefore *not* to confirm that Satterthwaite works. It
is to find the range of heteroscedasticity over which the one-sided upper limit
keeps its error control, and to say where it stops.

Both a feasible version (Satterthwaite degrees of freedom computed from
$\widehat D_i$ and a first-pass $\widehat A$) and an oracle version (computed
from the true $D_i$, $A$) are run, so that failure of the approximation is
separated from failure of the plug-in.

## One-sided, not two-sided

The safe band needs only $\Pr(\kappa>\kappa_U)\le\eta$. `exp10` spent a
two-sided interval on it. Here $\kappa_U=\sqrt{1-R/F_{1-\eta}}$ is one-sided,
which is the correct construction and strictly narrower. Certification, which
needs both ends, keeps the two-sided interval.

## Grid, fixed here

- $K\in\{30,100,300\}$
- $\bar D/A\in\{0.25,1,4\}$
- dispersion of $D_i$: lognormal with $\sigma_{\log}\in\{0,0.5,1.0,1.5\}$,
  mean held exactly, so $\sigma_{\log}=0$ is the `exp10` homoscedastic control
- $\nu_i=10$ per population; one side-set with $\nu_i$ dispersed lognormally
- 20,000 replicates; $\alpha_0=\eta=0.05$, target coverage 0.90, $\varepsilon=0.10$

## Comparators, on the same target and the same budget

The review is right that `noise_enlargement` reaches T2 under a *different*
assumption — a Gaussian tail bound on the target's sampling error rather than
the common-shape assumption (S) — so the comparison is of assumptions as well
as of widths, and must be labelled that way. Two changes to be fair to it:

1. **Its error budget is optimised, not split evenly.** The anchor/tail split
   is scanned and the narrowest valid choice is used per cell.
2. **A model-based competitor is added**: the Gaussian plug-in prediction
   interval $\pm z_{1-\alpha/2}\widehat s_G$, which is what an analyst who
   believes the model would actually compute. It carries no finite-sample
   guarantee and its realised coverage is the quantity of interest.

## Measured

Per cell: $\Pr(\kappa>\kappa_U)$ against $\eta$; realised T2 coverage of the
safe band against 0.90; realised coverage of oracle, enlargement and model
plug-in; mean widths of all four; realised Satterthwaite degrees of freedom
against nominal on both sides; two-sided certification rate and its error.

## Predictions

| # | prediction | falsified by |
|---|---|---|
| R1 | at $\sigma_{\log}=0$ the one-sided limit reproduces `exp10` exactly | any discrepancy |
| R2 | $\Pr(\kappa>\kappa_U)\le\eta$ holds up to moderate dispersion and degrades beyond it | control lost at $\sigma_{\log}=0.5$, or never lost |
| R3 | the denominator approximation degrades faster than the numerator | the reverse |
| R4 | safe band T2 coverage stays at or above 0.90 wherever R2 holds | undercoverage where the limit is valid |
| R5 | the safe band stays narrower than the optimised enlargement band | comparable or wider |

## Outcomes, all reported

1. **Control holds across the grid.** The scalar heteroscedastic case is
   closed and the next obstacle is coordinates, not populations.
2. **Control degrades past a dispersion threshold.** Then the paper states the
   threshold as an operating condition and must report where the ESS
   configurations sit relative to it — which requires the design variances, not
   more simulation.
3. **Control fails even at mild dispersion.** Then the $F$ pivot does not
   transfer, Proposition C is a homoscedastic curiosity, and the safe band needs
   a different interval — a bootstrap or a conservative bound — before anything
   else proceeds.

No cell is dropped after execution and no comparator is added after seeing results.
