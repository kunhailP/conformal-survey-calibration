# Protocol — exp09: what does estimating the sampling variance cost?

Written 2026-09-10, before executing `experiments/exp09_estimated_variance.py`.
Derivations and predictions: `docs/THEORY_estimated_variance.md`.

## Why

Section 4.2 states the information bound for the model variance with the design
variances $D_i$ **known**. In every survey application in this paper they are
estimated, from a replication variance estimator with limited design degrees of
freedom. The manuscript's boundary (eq. 15) inherits that assumption, so the
boundary is currently stated for a quantity nobody observes.

The theory memo derives two things and they point in opposite directions. The
*information* cost of estimating $D_i$ is fourth order in the design share and
negligible at survey-realistic values. The *plug-in bias* is first order in
$1/\nu$, does not vanish as populations accumulate, and moves the reliability
gate in the anti-conservative direction. If the second holds, the paper has a
result. If it does not, the extension is a two-percent correction and should be
a remark, not a section.

## Model

Independently over $i=1,\dots,m$: $Y_i\sim N(0,A+D_i)$ and
$\nu\widehat D_i/D_i\sim\chi^2_\nu$, with $Y_i$ and $\widehat D_i$ independent,
$\nu$ known, $A=1$ throughout, and $D$ set from the design share
$\rho^2=D/(A+D)$.

## Grid, fixed here

- $m\in\{30,100,250,500,1000\}$
- $\rho\in\{0.3,0.5,0.66,0.9\}$ — 0.66 is the largest share in the applications
- $\nu\in\{5,10,25,100,\infty\}$ — $\infty$ is the known-$D$ control
- 2,000 replicates per cell; cell seeds by SHA-256 of the cell label, as elsewhere

## Estimators compared, on identical data

1. `oracle_w` — Prop. 2 with $w_i^\star$ at the true $(A,D_i)$. Attains the bound.
2. `equal_w` — Prasad–Rao moment estimator, $m^{-1}\sum_i(Y_i^2-\widehat D_i)$.
3. `plug_ml` — known-$D$ ML/REML profile in $A$ with $\widehat D_i$ substituted.
   This is standard practice and the subject of P3–P5.
4. `plug_ml_known` — the same on the true $D_i$, as the $\nu=\infty$ reference.

All truncated at zero where the estimator is; the truncation share is recorded
separately so it cannot be confused with bias.

## Checks

1. **P1, information identity.** Compare $I_{\mathrm{eff}}$ of Prop. 1 with the
   Monte Carlo variance of the profile score and with the observed information
   of the simulated joint log-likelihood.
2. **P2, sharpness.** `oracle_w` bias and variance against $1/I_{\mathrm{eff}}$.
   This is an exact finite-sample claim, so agreement should be to Monte Carlo
   error at every cell, not asymptotically.
3. **P3, plug-in bias.** Realised relative bias of `plug_ml` against the
   prediction $4\rho^4/[\nu(1-\rho^2)]$.
4. **P4, persistence in $m$.** The same relative bias across $m$ at fixed $\nu$.
   The prediction is a flat line. A falling line refutes the claim that this is
   the operative problem.
5. **P5, gate direction.** Compute the reliability diagnostic of eq. (14) on
   each replicate using $\widehat s_G^2$ from `plug_ml` and from `equal_w`, and
   record the share of replicates on which $D\le\tau$ at $\tau=0.147$. The
   prediction is that the plug-in opens the gate strictly more often, at fixed
   truth.
6. **P6, equal weights.** `equal_w` unbiased at every $\nu$.
7. **Degrees of freedom versus replicates.** A separate small cell: hold
   $\nu^{\mathrm{des}}$ fixed, vary the Monte Carlo replicate count $B$ entering
   $\widehat D_i$, and confirm the $\nu^{\mathrm{eff}}$ ceiling of memo §5.

## Outcomes, all reported

1. **P3–P5 hold.** The plug-in practice is anti-conservative for the gate the
   manuscript characterises, the effect does not average away, and Section 4
   gains a subsection with a correction and a revised boundary.
2. **P3 holds but P5 does not** — the bias is real but the gate does not move,
   because the diagnostic's numerator is biased in the same direction. Then the
   result is about $\widehat A$ and small-area practice, not about this
   paper's gate, and it belongs in the small-area discussion instead.
3. **P4 fails, the bias shrinks in $m$.** Then the derivation in memo §4 is
   wrong, the extension is the two-percent information correction of memo §2,
   and it becomes a remark. The memo's own §2 says this outcome is a real
   possibility and it is not a disappointing one to report.
4. **P1, P2 or P6 fail.** Arithmetic error upstream. Fix before anything else.

No cell is dropped after execution, and the estimator set is fixed here.
