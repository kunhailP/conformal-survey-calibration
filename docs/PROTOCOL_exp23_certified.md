# Protocol — exp23: the certified envelope, replacing the endpoint claim

Written 2026-09-10, before executing `experiments/exp23_certified.py`.
Predecessor: `exp22`. **Retraction first.**

## What is being retracted

`exp22` reported that the grid minimiser of $t_L(\gamma)$ lands at an endpoint on
0.9999–1.0000 of replicates, and used a two-endpoint evaluation. **A
counterexample supplied in review reproduces exactly**: with $K=6$, $\nu_c=8$,
$C_\gamma=[-0.59651,0.34495]$ and the tabulated $(x_c,Y_c^2,\widehat D_c)$,
$t_L(\gamma_L)=0.10974$, $t_L(\gamma_U)=0.12106$, and an interior minimum
$t_L(-0.18321)=0.09121$ — **16.9 percent below the smaller endpoint.** The
endpoint property holds for $a_c(\gamma)$, which is proved, and **does not
transfer to $t_L(\gamma)$**, which is a different function. The rate of 0.9999
was never a theorem and the remaining 0.0001 is exactly what a universal claim
needs.

## The certified global lower bound, which needs no endpoint claim

$\Phi(t;\gamma)=t\,S(t;\gamma)=\sum_c\frac{t\,Y_c^2}{1+t\,a_c(\gamma)}$ is
increasing in $t$ and decreasing in each $a_c$, and $t_L(\gamma)$ solves
$\Phi(t;\gamma)=K\widehat d(\gamma)/q$.

1. **$\underline a_c=\min\{a_c(\gamma_L),a_c(\gamma_U)\}$ is exact**, by the
   concavity of $\log a_c$ in $\gamma$ already proved. Hence
   $\bar\Phi(t)=\sum_c t Y_c^2/(1+t\underline a_c)\ \ge\ \Phi(t;\gamma)$ for every
   $\gamma\in C_\gamma$.
2. **$\widehat d(\gamma)$ is convex in $\gamma$**: $1/a_c(\gamma)=K^{-1}\sum_j
   (x_c/x_j)^{\gamma}$ is a positive sum of exponentials, and $\widehat d$ is a
   positive combination of those. A one-dimensional convex minimisation therefore
   *certifies* $\underline d=\min_{\gamma\in C_\gamma}\widehat d(\gamma)$ — a
   ternary search returns the global minimum because the function is convex, not
   because the search was fine.
3. Then for every $\gamma\in C_\gamma$,
   $\bar\Phi(t_L(\gamma))\ge\Phi(t_L(\gamma);\gamma)=K\widehat d(\gamma)/q\ge
   K\underline d/q$, and $\bar\Phi$ increasing gives
   $$t_L(\gamma)\ \ge\ \underline t_{\mathrm{cert}}:=\bar\Phi^{-1}\!\big(K\underline d/q\big).$$

The envelope $\bar R=\operatorname{ord}_m\{|Y_c|/\sqrt{1+\underline t_{\mathrm{cert}}
\underline a_c}\}$ then dominates $R(t_L(\gamma),\gamma)$ for **every** $\gamma$ in
the set, by a bound rather than by a search. It is also **cheaper** than the grid:
two structure evaluations, one convex minimisation, one monotone inversion.

**Fallback.** If $K\underline d/q$ exceeds $\lim_{t\to\infty}\bar\Phi(t)=\sum_c
Y_c^2/\underline a_c$ there is no root; the conservative choice
$\underline t_{\mathrm{cert}}=0$ gives $\bar R=\operatorname{ord}_m|Y_c|$. The rate
is reported.

**Verification before use.** On the review's counterexample the bound gives
0.08924 against a true infimum of 0.09121. Over 300 randomly generated
configurations with a 401-point reference grid and a relative tolerance of
$10^{-9}$: **zero violations**; tightness $\underline t_{\mathrm{cert}}/\inf t_L$
has median 0.941 and 5th–95th percentiles 0.796–0.990. (A first pass at 3,000
cases showed one apparent violation, which did not survive a finer reference
grid and is recorded as a numerical artefact of the reference, not of the bound.)

## What this changes about the main method choice

The component-wise arm's supremum over $C_\gamma$ has **the same unproved
status** and no analogous certification: its band depends on $\gamma$ through
$d_L(\gamma)$, $a_c(\gamma)$ and $A_U(\gamma)$ at once. So the ratio form is now
preferred for a reason stronger than the 0.7–2.3 percent of width — **it is the
form that admits a certified computation.** The component arm is carried here
as it was computed in `exp22`, on a grid, and is labelled uncertified.

## Arms and reporting

Same generation and seeds as `exp22`. Arms: `oracle`, `uncorrected`,
`sep_bonf`, `Cg_comp` (grid, uncertified), `Cg_ratio_grid` (the retracted
computation, kept for the cost comparison), `Cg_ratio_cert` (this construction).

Reported: the three probabilities side by side — structure-set coverage, oracle
containment, latent-target coverage — then width, then the fallback rate and the
certification cost against the grid version. Correct and misspecified blocks
separately.

## Grid

$K\in\{60,200\}$, $d/A\in\{0.5,1\}$, $\nu_c\in\{8,16\}$,
$\sigma_{\mathrm{mis}}\in\{0,0.4\}$; 16 cells, 10,000 replicates;
$\alpha_0=0.05$, $\eta_\gamma=\eta_t=0.025$, guaranteed 0.90.

## Predictions

| # | prediction | falsified by |
|---|---|---|
| C1 | `Cg_ratio_cert` dominates `Cg_ratio_grid` on every replicate | any replicate where it does not |
| C2 | the certification costs more than `exp22`'s 0.5–1.9 percent, since $\underline t_{\mathrm{cert}}$ is below the true infimum | a cost at or under the earlier figure |
| C3 | containment and coverage stay at or above requirement when correctly specified | either failing |
| C4 | the certified arm still beats `sep_bonf` and stays near `Cg_comp` | losing to either |

## Outcomes

1. **C1–C4 hold.** The construction is a certified algorithm and the earlier
   width figures are restated at the certified cost.
2. **C2 shows a large cost.** Then the gain over the structure-free incumbent is
   restated at that cost, and whether it is still worth reporting is decided on
   the corrected numbers, not the retracted ones.
