# Protocol — exp10: certification against the frozen gate, in the closed model

Written 2026-09-10, before executing `experiments/exp10_certification.py`.
Derivations: `docs/THEORY_certification.md`. Predecessor: `exp09`.

## Why

The manuscript certifies with a frozen threshold on a plug-in diagnostic and
has no statement about how often that certification is wrong. The development
plan asks for a confidence-interval certification with a stated error budget,
and for the two checks that decide whether it is worth anything: does it reduce
false certification, and does it abstain so often as to be useless.

It also asks which quantity to certify. The plan proposes the latent scale
$s=\sqrt A$. This protocol tests a competing answer — that the quantity
governing the band is the **width factor** $\kappa=s_G/s_Y=\sqrt{1-\rho^2}$,
not $s_G$ — because the two differ by a factor $\rho^2$ in relative precision
and therefore by $\rho^{-4}$ in the population requirement. If that is right it
changes the manuscript's central number, so it is tested before anything is
written.

## Model, the plan's section 2 exactly

$Y_i=\mu+u_i+e_i$, $u_i\sim N(0,A)$, $e_i\sim N(0,D)$, independent,
$i=1,\dots,K$; $T=A+D$; a separate estimator with
$\nu\widehat D/D\sim\chi^2_\nu$ independent of the $Y$. $A=1$ throughout,
$\mu$ unknown and estimated, so $(K-1)S_Y^2/T\sim\chi^2_{K-1}$ exactly.

## Grid, fixed here

- $K\in\{30,100,300\}$
- $D/A\in\{0.25,1,4\}$, i.e. $\rho\in\{0.447,0.707,0.894\}$
- $\nu\in\{4,12,40\}$
- 20,000 replicates per cell. At a 5 percent event this is a Monte Carlo
  standard error of 0.15 percentage points.
- tolerance $\varepsilon=0.10$ on relative error; error budget $\eta=0.05$

## Certification rules compared, on identical data

1. `fixed_K` — $K\ge94$, the implementation's stated floor.
2. `plug_gate` — the manuscript's diagnostic, $\sqrt{2/(K-1)}\,S_Y^2/\widehat A
   \le\tau$, at the frozen $\tau=0.147$ and at $\tau=2\varepsilon$.
3. `ci_union` — the plan's section 3: separate $\chi^2$ intervals for $T$ and
   $D$ at $\eta/2$ each, $A_L=\max(0,T_L-D_U)$, $A_U=T_U-D_L$, certify when
   $(U-L)/(U+L)\le\varepsilon$ on $[\sqrt{A_L},\sqrt{A_U}]$.
4. `ci_gw` — the same target by the Graybill–Wang modified large-sample
   interval, the standard interval for a difference of variance components.
   Included because a referee will ask why the union bound was used instead.
5. `ci_kappa` — an exact interval for $\kappa$. Since
   $(\widehat D/S_Y^2)/\rho^2\sim F_{\nu,K-1}$, the interval is pivotal and
   exact, with no union bound anywhere.

## Evaluation

Every rule is judged on the **same** downstream criterion, the relative error
of the band's width factor $\kappa$, using a common plug-in $\widehat\kappa$ so
that the gate is compared and not the estimator. `ci_kappa`'s own minimax point
estimate $\widehat\kappa_\star=2LU/(L+U)$ is reported separately so the two
effects stay separable. Each rule is additionally judged on its own declared
target, so that no rule is scored against a quantity it never claimed.

Recorded per cell: certification rate; false certification rate
$\Pr(\text{certify}\cap|\widehat\kappa/\kappa-1|>\varepsilon)$; the same
conditional on certifying; and, for the safe band of the plan's section 6,
realised T2 coverage and width relative to the oracle band.

## Predictions

| # | prediction | falsified by |
|---|---|---|
| Q1 | `plug_gate` false certification exceeds $\eta$, badly, at high $\rho$ | rate at or below $\eta$ |
| Q2 | `ci_union` and `ci_gw` hold the budget but abstain almost always | budget violated, or certification rate comparable to `ci_kappa` |
| Q3 | `ci_kappa` holds the budget **and** certifies at a useful rate | either half failing |
| Q4 | the requirement on $K$ falls by about $\rho^4$ when the target is $\kappa$ rather than $s_G$ | certification rates not separating in that ratio |
| Q5 | the safe band covers at $1-\alpha_0-\eta$ or better, at a width penalty that shrinks with $K$ | undercoverage, or a penalty not shrinking |

## Outcomes, all reported

1. **Q3 and Q4 hold.** The certification target changes, the boundary is
   restated on $\kappa$, and the manuscript's central requirement falls by
   roughly $\rho^{-4}$. This is the outcome that would reorganise the paper.
2. **Q3 holds, Q4 fails.** Certification is worth having but the two targets
   are equivalent in practice; the boundary stands and only the gate changes.
3. **Q2 fails in the direction of adequacy** — the union bound is not
   materially worse than the exact interval. Then the plan's section 3 is
   sufficient, `ci_kappa` is a refinement, and the contribution is smaller.
4. **Q3 fails on the abstention half.** Every honest rule abstains almost
   always, which is itself the paper's answer, and it must be reported as such
   rather than tuned around.

No cell is dropped after execution and no rule is added after seeing results.
