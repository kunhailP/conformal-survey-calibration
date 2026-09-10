# Protocol — exp14: one procedure, from point estimate to band, with the guarantee named

Written 2026-09-10, before executing `experiments/exp14_chain.py`.
Predecessors: `exp12`, `exp13`.

## Retraction that motivates this experiment

`exp13` said a band whose containment is guaranteed by construction had been
obtained. **It had not.** The containment argument needs
$\Pr(A>A_U)\le\eta_1$ and $\Pr(\exists c: v_c<v_{L,c})\le\eta_2$. The simultaneous
lower limits were near-exact (0.974--0.977 against 0.975), but the scale limit
was a normal approximation with an estimated variance and covered at
**0.963--0.969** against 0.975. So what `exp13` established is that the
construction *behaved conservatively in the conditions examined* — the two
conservatisms compensating — not that the stated guarantee holds.

## A scale limit that is valid, and uses the bound already needed

With $\mu_i$ known, $Y_c^2/(A+D_c)$ are independent $\chi^2_1$, so
$U(A)=\sum_c Y_c^2/(A+D_c)\sim\chi^2_K$ exactly. Replacing $D_c$ by a lower
bound raises the sum: on $E_D=\{v_c\ge v_{L,c}\ \forall c\}$,
$$\widetilde U(A)=\sum_c\frac{Y_c^2}{A+v_{L,c}^2}\ \ge\ U(A).$$
Define $A_U$ as the root of $\widetilde U(A)=\chi^2_{K,\eta_1}$; $\widetilde U$ is
decreasing in $A$, so $\{A>A_U\}=\{\widetilde U(A)<\chi^2_{K,\eta_1}\}$ and
$$\Pr(E_D\cap\{A>A_U\})\le\Pr\{U(A)<\chi^2_{K,\eta_1}\}=\eta_1 .$$
Hence $\Pr(E_A^c\cup E_D^c)=\Pr(E_D^c)+\Pr(E_D\cap E_A^c)\le\eta_2+\eta_1$, and
the band $R(\sqrt{A_U},\mathbf v_L)$ contains the oracle half-width with
probability at least $1-\eta$. **The same simultaneous lower limits serve both
the scale limit and the band, so the budget is $\eta_1+\eta_2$ and not more.**

Note what this implies and why it is the point of the experiment: **the valid
limit is built from a pivot and does not use the point estimator at all.** So
`exp13`'s estimation improvement has no automatic route into the band, and
whether it has any route is exactly what is tested here.

## Arms for the scale limit, all on identical replicates

| arm | construction | expected |
|---|---|---|
| `chi2_pivot` | the above | valid by the argument, possibly wide |
| `normal_unw` | $\widehat A_{\mathrm{unw}}+z_{1-\eta_1}\widehat{\mathrm{SE}}$ | `exp13`'s; expected to undercover |
| `normal_gvf` | same from the GVF-weighted estimator | does a better point estimate give a better limit? |
| `gw` | one-sided Graybill--Wang, Satterthwaite dfs | the standard variance-component limit |
| `boot_gvf` | population bootstrap **refitting GVF, weights and subtraction** | reduced replicate count; validity not claimed |

For each arm, the same four quantities in sequence, which is the connection the
review asks for:

1. bias and RMSE of the underlying point estimator;
2. coverage of $A_U$ against $1-\eta_1$;
3. containment of the oracle half-width by $R(\sqrt{A_U},\mathbf v_L)$ against $1-\eta$;
4. latent-target coverage against $1-\alpha_0-\eta$, and width.

## Also settled here

**The $O(1/K)$ bias rate is tested, not asserted.** `exp13` inferred it from two
values of $K$. Here $K\in\{60,120,240,480\}$ at one setting, with the fitted
slope of $\log|\mathrm{bias}|$ on $\log K$ reported. A slope near $-1$ supports
the claim; anything else refutes the rate while leaving the direction intact.

**A leverage stress cell.** The dilution argument fails if a few populations
dominate the smoother. One cell uses heavy-tailed $n_i$ so that the largest
leverage is an order of magnitude above the median, and the bias is compared.

## Grid

$K\in\{60,200\}$; $\bar D/A\in\{1,4\}$; $\sigma_e\in\{0,0.6\}$; $\nu=10$;
20,000 replicates. Bootstrap arm: 1,000 replicates, $B=200$, two cells.
Rate check: $K\in\{60,120,240,480\}$ at $\bar D/A=4$, $\sigma_e=0.3$.
$\alpha_0=\eta=0.05$, $\eta_1=\eta_2=0.025$, guaranteed 0.90.

**$\nu$ is reported beside every information-gap figure**, because the gap is
bounded by $\sqrt{1+\rho^4/\nu}$ and a result at $\nu=10$ does not transfer to a
small area with four degrees of freedom.

## Predictions

| # | prediction | falsified by |
|---|---|---|
| U1 | `chi2_pivot` covers at or above $1-\eta_1$ at every cell | undercoverage |
| U2 | `normal_unw` undercovers, reproducing `exp13` | it covering |
| U3 | `normal_gvf` does **not** inherit the point estimator's advantage as coverage | it covering better *and* narrower |
| U4 | containment reaches $1-\eta$ for `chi2_pivot` and not for the normal arms | either failing |
| U5 | the bias slope in $\log K$ is near $-1$ | a slope far from $-1$ |
| U6 | leverage stress raises the GVF bias materially | no change |

## Outcomes, all reported

1. **U1 and U4 hold, U3 holds.** The chain is closed with a named guarantee, and
   the honest finding is that the estimation improvement of `exp13` does **not**
   propagate to the band. The paper then has two separate results, not one.
2. **U3 fails in the good direction.** The weighted estimator yields a limit that
   is both valid and narrower; then the chain is a single result and that is the
   stronger paper.
3. **U1 fails.** The pivot argument has an error and nothing downstream stands.
4. **U5 or U6 fail.** The dilution explanation is wrong or conditional; the GVF
   result is restricted to the regimes where it holds and said so.

No arm is added after seeing results and no cell is dropped.
