# Protocol exp30 — is the two-axis boundary a property of the problem?

Written before execution.

## Question

`docs/CLAIMS.md` records the two-axis condition
`1/(K-1) + 1/nu_tot <= 2 eps^2 (1-rho^2)^2 / rho^4`
as **sufficient**: it comes from the relative standard error of one estimator of
kappa. It does not follow that a different procedure could not do better. This
experiment asks whether a matching **necessary** condition holds.

## Method, fixed in advance

Restrict to the equal-design-variance submodel: `Y_c ~ N(0, A+D)` iid over
`c=1..K`, `nu Dhat_c / D ~ chi2_nu` iid and independent of `Y`, `nu_tot = K nu`.

Two-point (Le Cam). Choose two parameter points whose `eps`-balls in
`kappa = sqrt(A/(A+D))` are disjoint, i.e. `kappa_1/kappa_0 >= (1+eps)/(1-eps)`;
the separation is solved **exactly**, not linearised. If an estimator meets
`Pr(|kappahat/kappa - 1| > eps) <= eta` at both points then the induced test has
error sum `<= 2 eta`, so `TV >= 1 - 2 eta`; with `TV <= sqrt(1 - aff^2)` this
forces `aff <= 2 sqrt(eta (1-eta))`.

Hellinger affinities in closed form:
  scaled chi-square, n obs: `(2 sqrt(D0 D1)/(D0+D1))^(n nu/2)`
  normal N(0,V),   K obs:  `(2 sqrt(V0 V1)/(V0+V1))^(K/2)`

## Pre-registered predictions

- **P-1** The necessary condition carries the same `rho^4/(eps^2 (1-rho^2)^2)`
  dependence as the sufficient one. Tolerance: the ratio of the two constants is
  bounded and approaches a limit as `eps -> 0`.
- **P-2** The necessary bound never exceeds the sufficient one (a lower bound
  cannot exceed an achievable value). Any violation is a bug.
- **P-3** The nu-axis and K-axis bounds differ, because the two channels carry
  different information. *(Recorded as the prediction; see result.)*

## Reported

Exact affinity against numerical quadrature; the two bounds over
`rho^2 in {0.2,0.4,0.6,0.8}`, `eps in {0.05,0.02,0.01}`, `eta=0.05`; the ratio
to the sufficient condition; the limiting constant.

## Scope

The bound is for **certifying kappa**, not for the width of a valid interval, and
it is stated in the equal-variance submodel. A lower bound over a submodel is
valid for the full model. Nothing here is claimed as new: with equal design
variances the model is the balanced one-way random-effects model and the design
trade-off for the intraclass correlation is an existing literature.
