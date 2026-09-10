# Protocol — exp24: the fixed certified method on the two complex-survey routes

Written 2026-09-10, before executing `experiments/exp24_survey_structure.py`.
Predecessors: `exp18` (the two routes) and `exp23` (the fixed method).
**No method is chosen or changed here. No comparator is added.**

## The one design change, fixed before running

`exp18`'s populations all had the same design, so no exogenous variable
predicted $D_c$. The structure model needs one. **Populations are therefore given
different sample sizes**: the number of sampled PSUs $m_c$ varies, so
$\nu_c=H(m_c-1)$ varies with it, and
$$x_c=m_c\quad\text{(sampled PSUs, known exactly before any estimate is seen)}$$
is the structure variable. It is fixed here and **will not be changed after
seeing results** — reselecting it on the outcome would turn the validation data
back into development data.

Heterogeneous $\nu_c$ requires the null law of $W(\gamma)$ to be simulated with
the actual $\nu_c$; it still depends on neither $d$ nor $\gamma$, and $W$ is
still linear in $\gamma$, so $C_\gamma$ stays closed-form.

**The structure is misspecified by construction and that is the point.** The true
design variance of a proportion carries $p_c(1-p_c)$ and the cluster structure as
well as the sample size, and $d\,x_c^{-\gamma}$ captures only the last. How much
it captures is the first thing measured.

## Budget, fixed

$\alpha_0=0.05$, $\eta_\gamma=\eta_t=0.025$, guaranteed 0.90 in the restricted
model. Not changed after results.

## Three things separated in the report

1. **Structure explanatory power.** $R^2$ of $\log D_c$ on $\log x_c$ across
   populations, the residual standard deviation, and the least-squares slope —
   the quantity $\gamma$ would have to be if the family were right.
2. **The inference stage.** The width of $C_\gamma$; whether it contains that
   least-squares slope (**a diagnostic, not a coverage statement** — with the
   family misspecified there is no $\gamma_0$ to cover); oracle-band containment;
   the fallback rate.
3. **Final performance.** Latent-target coverage and band width against the
   structure-free incumbent, the uncorrected band and the oracle.

**If intermediate confidence events fail while the final coverage holds, that is
reported as empirical conservatism**, not as the restricted-model guarantee
extending to a complex design. The $F$ pivot's conditions do not hold here and a
simulation cannot make them hold.

## Arms

`oracle`, `uncorrected`, `sep_bonf` (structure-free incumbent), `Cg_cert` (the
method fixed in `exp23`). Nothing else.

## Grid — `exp18`'s two routes preserved

`small_sample` (fewer sampled PSUs and smaller clusters) and `low_signal`
(smaller between-population spread), matched on $\bar D/A$ so that the routes
differ in degrees of freedom, zero-variance rate and estimate–variance
dependence rather than in design share. $t_0$ at the population median and at
the 0.15 quantile; $K\in\{60,200\}$. 16 cells, 2,000 replicates. Monte Carlo
error about 0.0067 near 0.90.

## Predictions

| # | prediction | falsified by |
|---|---|---|
| S1 | the sample-size structure explains much but not all of $\log D_c$; $R^2$ well below 1 at the tail quantile | $R^2$ near 1, which would make the test uninformative |
| S2 | `Cg_cert` keeps latent-target coverage at or above 0.90 on both routes | undercoverage |
| S3 | its oracle containment falls below the restricted-model requirement, most on the small-sample route | containment holding at 0.95 throughout |
| S4 | it is still narrower than `sep_bonf`, but by less than the 6.5–16.5 percent of the closed model | no narrowing, or the closed-model figure surviving intact |

## Outcomes, all reported

1. **S2 and S4 hold.** The method transfers with a stated operating range and
   the empirical gain is quoted at its complex-survey value.
2. **S4 fails.** Using a variance structure does not pay under a real design,
   and that is the result — reported as prominently as a gain would have been.
3. **S2 fails.** The method has a boundary in survey conditions, located by the
   diagnostics of block 1 and 2, and stated as a restriction.

No cell dropped, no comparator added, no structure variable reselected.
