# The two-axis boundary is a property of the problem

Companion to `docs/THEORY_certification.md` §1–2. Verified by `exp30`.

## 1. What was open

The condition recorded in `docs/CLAIMS.md`,

    1/(K-1) + 1/nu_tot  <=  2 eps^2 (1 - rho^2)^2 / rho^4,          (S)

is **sufficient**. It is the relative standard error of one estimator of
`kappa = sqrt(A/(A+D))`, set below `eps`. Nothing in that derivation rules out a
cleverer procedure clearing the same tolerance with fewer populations or fewer
design degrees of freedom. Until that is settled, the `rho^-4` saving is a claim
about our estimator, not about the problem — and §3's elasticity result inherits
the same doubt, since a referee may read the damping as an artefact of what the
derivative holds fixed.

## 2. The submodel

Equal design variances:

    Y_c ~ N(0, A + D)         iid,  c = 1..K
    nu Dhat_c / D ~ chi2_nu   iid,  independent of Y,   nu_tot = K nu

A lower bound proved over a submodel is valid for the full model, which is
harder. The sufficient condition (S) was derived in the same submodel, so the
two constants are comparable.

## 3. The argument

Take two parameter points whose `eps`-balls in `kappa` are disjoint:

    kappa_1 / kappa_0  >=  (1 + eps) / (1 - eps)  =:  tau                (D)

**solved exactly.** (Linearising this as `delta = 4 eps` places the points too
close together and inflates the bound by 11% at `eps = 0.05`; the error is in the
unsafe direction and an earlier draft of this memo made it.)

If an estimator satisfies `Pr(|kappahat/kappa - 1| > eps) <= eta` at both points,
the test "is `kappahat` in ball 0" has error sum `<= 2 eta`, so by Le Cam
`TV >= 1 - 2 eta`. With `TV <= sqrt(1 - aff^2)`,

    aff  <=  2 sqrt(eta (1 - eta)),     i.e.   -log aff  >=  L(eta).

Both affinities are closed form, so this is exact and finite-sample:

    scaled chi2, nu_tot df :  aff = (2 sqrt(D0 D1)/(D0+D1))^(nu_tot/2)
    normal N(0,V), K obs   :  aff = (2 sqrt(V0 V1)/(V0+V1))^(K/2)

**nu-axis** (hold `A+D`, move `A`): `D1/D0 = (1 - tau^2 kappa^2)/(1 - kappa^2)`.
**K-axis** (hold `D`, move `A`): `V1/V0 = (1 - kappa^2)/(1 - tau^2 kappa^2)`.

### Result N1 (necessary condition)

No procedure certifies `kappa` to tolerance `eps` at failure probability
`eta < 1/2` unless

    nu_tot  >=  L(eta) rho^4 / (eps^2 (1 - rho^2)^2),   L(eta) = -log(2 sqrt(eta(1-eta)))

and the same with `K` in place of `nu_tot`. Verified: `exp30` reproduces the
constant `L(0.05) = 0.8304` as `eps -> 0` (0.8098 at `eps = 0.005`).

### Result N2 (reciprocal duality — why the axes are harmonic)

The two perturbations are **exact reciprocals**, and the affinity
`(2 sqrt(r)/(1+r))^(n/2)` is invariant under `r -> 1/r`. Hence the two axes carry
the *same* constant. `exp30` confirms the identity to `8e-14` and the two bounds
agree to `9e-9` (bisection tolerance).

This is the reason `K` and `nu_tot` enter (S) harmonically rather than in some
other combination. Before this, the harmonic form was an observation from adding
two relative standard errors.

### Numbers

`eta = 0.05`; ratio of the sufficient constant to the necessary one:

| eps | rho2 = 0.2 | 0.4 | 0.6 | 0.8 |
|---|---|---|---|---|
| 0.05 | 14.52 | 4.17 | 3.32 | 3.01 |
| 0.02 | 3.69 | 2.86 | 2.65 | 2.56 |
| 0.005 | 2.57 | 2.43 | 2.39 | 2.37 |

The dependence on `rho`, `eps` matches exactly; the constants differ by a factor
approaching `z^2/(2 L) = 2.31`. One side is exact, the other a normal
approximation, so the residual gap is not all slack in the bound.

## 4. Registered predictions and what happened

| prediction | result |
|---|---|
| P-1 same `rho^4/(eps^2 (1-rho^2)^2)` dependence | **holds**, constant converges to `L(eta)` |
| P-2 necessary never exceeds sufficient | **holds**, no violation in 16 cells |
| P-3 the two axes differ | **refuted** — they are identical, by N2 |

P-3 was written down because the two channels carry different kinds of
information. They do; the reciprocal duality makes the *cost* the same anyway.

## 5. What this does NOT establish

1. **It is a bound on certifying `kappa`, not on interval width.** An interval
   can be valid without certifying `kappa`. No width lower bound is proved and
   **no optimality is claimed for the interval of §4.**
2. **Neither the technique nor the submodel problem is new.** Le Cam's two-point
   method is textbook. With equal design variances the model is the balanced
   one-way random-effects model, `kappa` is a monotone function of the intraclass
   correlation, exact intervals for it are classical, and trading groups against
   observations per group is an existing design literature (Donner 1986;
   Zou 2012; Shieh 2024). The SNR minimax theory (Verzelen & Gassiat 2018) has a
   different observation structure — no separate channel carrying the error scale
   on known degrees of freedom, which is what creates the second axis here.
3. **The heteroscedastic case is untouched.** The bound is for equal design
   variances; the paper's procedure operates under an estimated relative
   structure, where no matching bound is proved.
4. The bound loosens where the perturbation nears the parameter-space edge
   (`u -> 1`), by a factor 14 at `rho^2 = 0.2`, `eps = 0.05`.

## 6. What it is for

One sentence in the manuscript: (S) reflects the problem, not the estimator.
That closes the reading in which the `rho^2` damping of §3 is an artefact of the
bookkeeping, because `rho^2` appears in a lower bound that no bookkeeping choice
can move.
