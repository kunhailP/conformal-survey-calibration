# Protocol — exp25: the remaining high design-share cells, and a true-structure diagnostic

Written 2026-09-10, before executing `experiments/exp25_high_share.py`.
Predecessor: `exp24`. **The method, the structure variable and the error budget
are those already fixed and will not be changed after seeing results.** This
completes the validation range agreed earlier; it does not search for better
conditions.

## What is completed here

`exp24` reached $\bar D/A=0.053$ to $0.262$. The range set earlier also included
$\approx0.55$ and $\approx0.75$, which is where the correction has most to do and
where `exp18` found the incumbent capturing only 0.20–0.31. Both routes are
tuned to those two targets; the realised values are reported, and both
$\bar D/A$ and $\rho^2=\bar D/(A+\bar D)$ are printed, since "regional" is a
label and the numbers are the claim.

The routes keep their meaning: at matched $\bar D/A$, `small_sample` has
$m_c\in\{2,3\}$ and $n=2$, so $\nu_c\in\{4,8\}$ with frequent zero variance
estimates, while `low_signal` has $m_c\in\{4,\dots,8\}$ and $n=10$, so
$\nu_c\in\{12,\dots,28\}$ with none. $\tau$ is the knob in both.

## The diagnostic that separates two explanations

`exp24` showed containment failing while $C_\gamma$ contained the best-fitting
exponent, which rules out estimation error in $\gamma$ but does **not** identify
the cause: the structure residual and the sampling-distribution conditions
(normality, the $\chi^2$ law, $\widehat D_c\perp Y_c$) fail together in that
design.

A diagnostic arm separates them. In simulation the true $D_c$ is known, so
$$a_c^{\mathrm{true}}=D_c\big/\overline D$$
can be supplied as a *known* structure and the ratio procedure run on it at the
same total budget $\eta=0.05$, with no $C_\gamma$ step.

- **If containment and the width gain return with the true structure**, then
  approximating the variance structure is the binding step, and better structure
  modelling is the thing to work on.
- **If containment stays low even with the true structure**, then the $F$
  inference's own conditions are the problem and no structure model fixes it.

This is a diagnostic, not a method: it is infeasible on real data and is labelled
so everywhere.

**Zero-variance populations are recorded, not repaired.** Where $D_c=0$ the
positive-variance family does not apply and $a_c^{\mathrm{true}}$ is undefined.
Replicates containing any such population are counted and excluded **from the
diagnostic arm only**, with the excluded fraction reported beside it. No value is
substituted and nothing is dropped from the other arms.

## Arms

`oracle`, `uncorrected`, `sep_bonf` (structure-free incumbent), `Cg_cert` (the
fixed method), `ratio_true_a` (the diagnostic). Nothing else.

## Reporting order, corrected from `exp24`

**Latent-target coverage and realised width first**; the share of the oracle
narrowing captured is secondary and is flagged where the uncorrected and oracle
widths are close, since its denominator is then small. A band narrower than the
oracle is not by itself invalid — the oracle is a reference using the true scale
and has not been shown to be the narrowest valid band — so nothing is inferred
from a capture above 1 except that the statistic is uninformative there.

## Grid

Routes $\times$ targets $\{0.55,0.75\}$ $\times$ $t_0\in\{$median$,0.15\}$
$\times$ $K\in\{60,200\}$ = 16 cells, 2,000 replicates. $x_c=m_c$;
$\alpha_0=0.05$, $\eta_\gamma=\eta_t=0.025$ for `Cg_cert`, $\eta=0.05$ for the
diagnostic. Monte Carlo error about 0.0067 near 0.90.

## Predictions

| # | prediction | falsified by |
|---|---|---|
| R1 | the structure family explains less at high design share than in `exp24` | comparable or better $R^2$ |
| R2 | `Cg_cert` keeps latent-target coverage at or above 0.90 | undercoverage |
| R3 | its containment stays below 0.95 | containment recovering |
| R4 | the diagnostic arm with the true structure recovers containment | it staying low, which would move the problem to the $F$ conditions |
| R5 | the width gain over `sep_bonf` is larger than `exp24`'s 0.2–4.1 percent, because more is available | no larger gain |

## Outcomes, all reported

1. **R4 holds and R5 gives a material gain.** The applicable range is stated as
   a design-share and structure-quality condition, and better structure modelling
   is the identified next problem — for a later paper, not this one.
2. **R4 fails.** The $F$ inference does not transfer to this design regardless of
   the structure model, and that bounds the method to the restricted model.
3. **R5 fails.** The gain does not appear even where most is available, and the
   applicable range is empty on these designs.

After this experiment the applicable range is fixed. **No further conditions are
searched with this method.**
