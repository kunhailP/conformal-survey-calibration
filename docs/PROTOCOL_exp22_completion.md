# Protocol — exp22: completing route (b) — the algorithm, and the matched estimated-structure comparison

Written 2026-09-10, before executing `experiments/exp22_completion.py`.
Predecessor: `exp21`. **Route (a), general profiling, is not opened.**

## Two jobs, both closing work rather than opening it

### Job 1 — make the supremum a computation, not a grid

`exp21` took $\sup_{\gamma\in C_\gamma}R(t_L(\gamma),\gamma)$ on a 31-point grid
and showed insensitivity to 61 points. **Insensitivity is evidence of numerical
stability, not a proof that the maximum over a continuous interval was not
missed.** Half of that gap closes exactly:

> **Lemma.** $\log a_c(\gamma)=-\gamma\log x_c-\log\overline{x^{-\gamma}}$ has
> $\partial_\gamma\log a_c(\gamma)=\bar\ell(\gamma)-\log x_c$ where
> $\bar\ell(\gamma)$ is the mean of $\log x$ under weights $\propto x^{-\gamma}$,
> and $\bar\ell'(\gamma)=-\mathrm{Var}_w(\log x)\le0$. So $\log a_c$ is **concave**
> in $\gamma$ for every $c$, and
> $\inf_{\gamma\in[\gamma_L,\gamma_U]}a_c(\gamma)=\min\{a_c(\gamma_L),a_c(\gamma_U)\}$
> **exactly**, at an endpoint.

Since $R$ is decreasing coordinatewise in $t\,a_c$, that gives a **certified
envelope**
$$\bar R=\operatorname{ord}_m\Big\{|Y_c|\big/\sqrt{1+\underline t\,\underline a_c}\Big\},
\qquad \underline a_c=\min\{a_c(\gamma_L),a_c(\gamma_U)\},\quad
\underline t=\inf_{\gamma\in C_\gamma}t_L(\gamma),$$
with $\bar R\ge R(t_L(\gamma),\gamma)$ for every $\gamma\in C_\gamma$. The
remaining gap is $\underline t$, for which no monotonicity is proved. This
experiment records whether the grid minimiser of $t_L$ lands at an endpoint, and
reports the envelope's width cost against the grid maximum, so that the price of
certification is measured rather than assumed. **The envelope is reported as the
defensible construction and the grid maximum as the reference.**

### Job 2 — the comparison the previous review asked for

`exp21` compared a ratio bound that estimates the structure against a
component-wise bound that was **given** it. The matched comparison estimates the
structure on both sides:

| arm | budget split of $\eta=0.05$ | construction |
|---|---|---|
| `Cg_ratio` | $\eta_\gamma=0.025$, $\eta_t=0.025$ | $\sup_{\gamma\in C_\gamma}R(t_L(\gamma),\gamma)$ |
| `Cg_ratio_env` | same | the certified envelope above |
| `Cg_comp` | $\eta_\gamma=0.025$, $\eta_1=\eta_2=0.0125$ | $\sup_{\gamma\in C_\gamma}R$ built from $d_L(\gamma)$ and $A_U(\gamma)$ separately |
| `sep_bonf` | $\eta_1=\eta_2=0.025$ | the structure-free incumbent, reference only |
| `oracle`, `uncorrected` | — | references |

The component-wise arm needs one more budget piece, and paying for that is part
of what is being compared. **The ratio arm does not have to win.** If the
difference is small, the simplest construction to state and prove becomes the
main method.

## Reported, three probabilities side by side, always

After the key collision found in `exp21`, these are printed together in every
table and never inferred from one another:

| quantity | stage it checks |
|---|---|
| $\Pr\{\gamma_0\in C_\gamma\}$ | structure estimation |
| $\Pr\{R_{\text{method}}\ge R_{\text{oracle}}\}$ | uncertainty propagation |
| $\Pr\{\theta_{K+1}\in B\}$ | what the user receives |

Widths are compared **paired on the same replicates**, since equal ranges across
cells do not mean equal performance within them.

## Misspecification is reported as model error, not estimation error

When the true $\mathbf D$ lies outside $\{d\,a_c(\gamma)\}$ there is no $\gamma_0$
to cover, so a correct confidence set for $\gamma$ gives no protection. The
misspecified block therefore reports $\Pr\{\gamma_0\in C_\gamma\}$ as
uninterpretable and reads only containment and coverage. **A confidence set for a
structure parameter does not protect against the structure family being wrong**,
and that sentence is the finding, not a caveat.

## Grid

$K\in\{60,200\}$, $d/A\in\{0.5,1\}$, $\nu_c\in\{8,16\}$,
$\sigma_{\text{mis}}\in\{0,0.4\}$; 16 cells, 10,000 replicates, $\gamma_0=1$,
$\alpha_0=0.05$, total $\eta=0.05$, guaranteed 0.90. Monte Carlo error 0.0016
near 0.975 and 0.0030 near 0.90.

## Predictions

| # | prediction | falsified by |
|---|---|---|
| P1 | the grid minimiser of $t_L(\gamma)$ is at an endpoint on nearly every replicate | interior minima being common, which would leave the envelope unjustified |
| P2 | the certified envelope costs little against the grid maximum | a large certification cost |
| P3 | `Cg_ratio` and `Cg_comp` are close, both far better than `sep_bonf` | a large gap either way |
| P4 | both keep containment when correctly specified and lose it under misspecification | one of them surviving misspecification |

## Outcomes

1. **P3 holds with a small gap.** The main method is chosen for provability, not
   width, and that choice is stated.
2. **`Cg_comp` is materially better.** Then the ratio construction is dropped as
   the main method and kept as the exact reference case of §17.
3. **P1 fails.** The envelope is not justified and the supremum needs a different
   treatment before anything is claimed about it.

No arm is added and no cell dropped after execution. The complex-survey
application follows once the main method is fixed here.
