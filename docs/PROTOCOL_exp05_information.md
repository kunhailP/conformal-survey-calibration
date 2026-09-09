# Protocol — exp05: is the coupling a property of the problem?

Written 2026-09-09, before executing `experiments/exp05_information.py`.

## Why

The coupling identity as currently stated is about one implementation's
diagnostic, built on the moment estimator of a variance component. A referee is
entitled to ask why the constants of an uncited procedure should interest them.
If the same inflation is a property of the *estimation problem* rather than of
that estimator, the result applies to any workflow that subtracts sampling
variance from between-population dispersion, and the paper is about survey
practice rather than about one selector.

## The claim to test

Write the Fay-Herriot model, the standard small-area formulation
\citep{fay1979estimates}: for area `c`, a direct estimate `y_c = theta_c + e_c`
with known sampling variance `D_c`, and `theta_c = x_c' beta + u_c` with
`u_c ~ N(0, A)`. Estimating the model variance `A` is exactly the operation of
subtracting sampling variance from observed dispersion.

The Fisher information for `A` with known `D_c` is
`I(A) = (1/2) sum_c (A + D_c)^{-2}`, so any unbiased estimator satisfies

    Var(A_hat) >= 2 / sum_c (A + D_c)^{-2},

and with common `D` and design share `rho^2 = D / (A + D)`,

    RSE(A_hat) >= sqrt(2/K) / (1 - rho^2).

**Prediction: the `(1 - rho^2)^{-1}` inflation is an information bound, not an
artefact of the moment estimator.** If so, requiring relative precision `tau`
forces `K >= 2 / [tau^2 (1 - rho^2)^2]`, the same boundary, now for any
estimator of the component rather than one diagnostic.

This would also close a gap the predecessor left open. Its floor was proved by
Lehmann-Scheffe for unbiased estimation of a variance from `K` summaries, and
explicitly excluded biased, shrinkage and prior-informed estimators, with a
minimax version left open. Shrinkage estimators are what small-area practice is
built on, so that exclusion removed the result from its own application.

## Checks

1. **Information identity.** Verify `I(A) = (1/2) sum_c (A + D_c)^{-2}`
   numerically against the observed information from simulated likelihoods.
2. **REML attains it.** Simulate Fay-Herriot data over `K` in {30, 100, 250,
   500} and `rho` in {0.1, 0.3, 0.5, 0.7, 0.9}, estimate `A` by REML, and
   compare the realised relative standard error with `sqrt(2/K)/(1-rho^2)`.
   REML is consistent and asymptotically efficient here, so agreement is the
   expected outcome and disagreement would refute the claim.
3. **Unequal sampling variances.** Repeat with `D_c` dispersed across areas, to
   check the equal-`D` simplification is not carrying the result.
4. **Negative estimates.** Record how often REML returns the boundary estimate
   `A_hat = 0`, by `rho` and `K`. If the boundary is the operative constraint,
   truncation at zero should become common in exactly the regime the bound
   calls infeasible, which would connect the result to a failure mode small-area
   practitioners already recognise.

## Outcomes

1. **REML tracks the bound.** The coupling is a property of the problem. The
   manuscript states it for the estimation problem and treats the selector's
   diagnostic as one instance.
2. **REML beats the bound at small `K`.** Then bias is buying precision, the
   unbiased-estimation framing is too narrow, and the claim must be restricted
   to unbiased estimators with that stated explicitly.
3. **The equal-`D` simplification carries the result and dispersed `D_c`
   breaks it.** Then the boundary is stated with the harmonic-type sum rather
   than in closed form, and the closed form is labelled an equal-variance
   special case.

All outcomes are reported. The simulation grid is fixed here and no cell is
dropped after execution.
