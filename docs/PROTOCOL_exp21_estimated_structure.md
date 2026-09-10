# Protocol — exp21: matched information first, then paying for the structure

Written 2026-09-10, before executing `experiments/exp21_estimated_structure.py`.
Specification: `docs/THEORY_ratio_pivot.md` §3 route (b). Predecessor: `exp20`.

## Why the matched comparison comes first

`exp20` gave the ratio construction a **known** $a_c$ and compared it against an
incumbent that bounds each $D_c$ separately with a Bonferroni correction. The
observed 9–20 percent therefore mixes two effects:

1. **pooling** — knowing the relative structure lets one common $d$ carry the
   information from all $K$ variance estimates, so no simultaneity correction is
   needed at all;
2. **direct ratio inference** — not bounding $A$ above and $D$ below separately.

Both are useful and only the second is the idea under test. So a third arm is
added that is **given the same known $a_c$** and still bounds the components
separately: one lower limit for the common $d$ at $\eta_2$ (exact, from
$\nu\widehat d/d\sim\chi^2_\nu$, no Bonferroni) and an upper limit for $A$ at
$\eta_1$. The gap between that arm and the ratio arm is the effect being
claimed.

## The structure model, and how its uncertainty is paid for

$D_c=d\,a_c(\gamma)$ with $a_c(\gamma)=x_c^{-\gamma}/\overline{x^{-\gamma}}$ and
$x_c$ a known design variable. The normalisation $\overline{a_c}=1$ fixes the
$d$–$\gamma$ confounding.

**$a_c(\widehat\gamma)$ is not treated as known.** With
$\epsilon_c=\log(\chi^2_{\nu_c}/\nu_c)$, whose law is completely known and whose
variance is $\psi'(\nu_c/2)$,
$$W(\gamma)=\frac{\sum_c(\log x_c-\overline{\log x})\{\log\widehat D_c+\gamma\log x_c\}}
{\sqrt{\psi'(\nu/2)\sum_c(\log x_c-\overline{\log x})^2}}$$
has, at the true $\gamma$, a null law that depends on neither $d$ nor $\gamma$;
it is a fixed linear functional of independent variables with a known
distribution, and its quantiles are computed once by simulation. $W$ is linear
and increasing in $\gamma$, so
$$C_\gamma=\Big[\widehat\gamma-\tfrac{w\sigma_\epsilon}{\sqrt{S_{xx}}},\;
\widehat\gamma+\tfrac{w\sigma_\epsilon}{\sqrt{S_{xx}}}\Big],
\qquad \widehat\gamma=-S_{xD}/S_{xx},$$
in closed form, with no search. Then
$$R_U=\sup_{\gamma\in C_\gamma}R\big(t_L(\gamma),\gamma\big),$$
and on $\{\gamma_0\in C_\gamma\}\cap\{t_0\ge t_L(\gamma_0)\}$,
$R_U\ge R(t_L(\gamma_0),\gamma_0)\ge R(t_0,\gamma_0)$, giving
$\Pr\{\theta_{K+1}\notin B_U\}\le\alpha_0+\eta_\gamma+\eta_t$ by a union of the
three events. **No independence between the two confidence events is needed.**

The supremum is over a one-dimensional interval and is computed on a grid of 31
points; a sensitivity check at 61 points is reported. **A grid maximum is not
declared to be the supremum**, and the check is what stands behind the number.

## Boundary handling, corrected from `exp20`

`exp20` reported $R_U=\infty$ when the inversion set was empty. Since
$R(t,\gamma)\le R(0)=\operatorname{ord}_m|Y_c|$ for every $t\ge0$, falling back to
$t_L=0$ is also safe for containment and keeps the width finite. **That is the
rule here**, and the fallback rate is reported. (In `exp20` the set was never
empty, so no width statistic there was affected; that is recorded rather than
assumed.)

## Arms, at one total budget of $\alpha_0+0.05=0.10$

| arm | information | construction |
|---|---|---|
| `oracle` | true $A$, true $D_c$ | width reference |
| `uncorrected` | none | $\operatorname{ord}_m|Y_c|$; no T2 guarantee claimed |
| `sep_bonf` | $\widehat D_c$ only | $A_U$ at $\eta_1$ + Bonferroni $v_{L,c}$ at $\eta_2$ — the `exp18` incumbent |
| `sep_struct` | **known $a_c$** | $d_L$ at $\eta_2$ (one exact limit) + $A_U$ at $\eta_1$ |
| `ratio_known` | **known $a_c$** | $t_L$ at $\eta=0.05$ — `exp20`'s |
| `plugin_gamma` | $x_c$, $\widehat\gamma$ | $t_L$ at $\eta=0.05$ treating $a_c(\widehat\gamma)$ as known |
| `Cgamma` | $x_c$ | $\sup_{\gamma\in C_\gamma}R(t_L(\gamma),\gamma)$, $\eta_\gamma=\eta_t=0.025$ |

`sep_struct` minus `ratio_known` isolates the claim. `plugin_gamma` shows what
ignoring the structure uncertainty costs. `Cgamma` is the proposal.

## Reported, in this order

1. coverage of $C_\gamma$ against $1-\eta_\gamma$;
2. containment of the oracle half-width, every arm;
3. latent-target coverage against the guaranteed 0.90;
4. width, paired, with coverage printed beside it;
5. fallback rate, and the grid sensitivity of the supremum.

## Grid

$K\in\{60,200\}$, $d/A\in\{0.5,1\}$, $\nu_c\in\{8,16\}$, and structure
misspecification $\sigma_{\text{mis}}\in\{0,0.4\}$ — at $0$ the model is exactly
$D_c=d\,a_c(\gamma_0)$ and the guarantees above apply; at $0.4$ a lognormal
factor is applied to $a_c$ so **no** $\gamma$ is correct and only empirical
stability is being observed. 16 cells, 10,000 replicates. $\gamma_0=1$.
Monte Carlo error 0.0022 near 0.95 and 0.0030 near 0.90.

**The two regimes are reported separately and never averaged.**

## Predictions

| # | prediction | falsified by |
|---|---|---|
| U1 | $C_\gamma$ covers at $1-\eta_\gamma$ when correctly specified | departure |
| U2 | `sep_struct` recovers much of `sep_bonf`'s gap, so the pooling effect is large | no improvement from pooling |
| U3 | `ratio_known` is still materially narrower than `sep_struct` | no gap, which would relocate the contribution to pooling |
| U4 | `Cgamma` keeps containment and coverage when correctly specified, at a width between `ratio_known` and `sep_struct` | undercoverage, or a width worse than `sep_bonf` |
| U5 | `plugin_gamma` undercovers, most at small $K$ and small $\nu$ | it covering |
| U6 | under misspecification `Cgamma` loses containment; `sep_bonf` may not | both failing equally, or neither |

## Outcomes, all reported

1. **U3 and U4 hold.** Direct ratio inference is the effect, and it survives
   paying for the structure. This is the result the line was built for.
2. **U3 fails.** The gain is pooling, not direct inference. The contribution is
   restated around using a known variance structure, which is a smaller and
   different claim, and said so.
3. **U4 fails.** Paying for the structure costs more than the idea earns; route
   (b) closes and route (a) is the remaining option.
4. **U6 shows failure under misspecification.** Then the method's stated range
   requires a correctly specified variance structure, and that condition is
   reported with the gain, not after it.

No arm is added and no cell dropped after execution.
