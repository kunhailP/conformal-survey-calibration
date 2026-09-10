# Protocol — exp26: a Gaussian competitor for the same target, same information, same level

Written 2026-09-10, before executing `experiments/exp26_same_target.py`.
Completion criterion 3. **No new method for the proposal; the competitor is the
new construction and it is built to be strong.**

## The comparison that is actually needed

Applying an in-sample conformal interval to an out-of-sample target would be
comparing different questions. The direct comparator is a **Gaussian model-based
prediction interval for the same new population's latent value**, given the same
data and the same structure information.

Model R with $\mu$ known: $Y_c=u_c+e_c$, $u_c\sim N(0,A)$, $e_c\sim N(0,D_c)$,
$D_c=d\,a_c(\gamma)$, $\nu_c\widehat D_c/D_c\sim\chi^2_{\nu_c}$. The target is
$$\theta_{\mathrm{new}}=\mu+u_{\mathrm{new}},\qquad u_{\mathrm{new}}\sim N(0,A),$$
i.e. the **latent** value, not the new population's survey estimate. A Gaussian
interval that added a new sampling variance would be answering a different
question and is not used.

## The competitor, and why it is a fair one

$u_{\mathrm{new}}\sim N(0,A)$ exactly, so $\pm z_{1-\alpha_1/2}\sqrt{A_U}$ covers
it whenever $A\le A_U$. An upper limit for $A$ is built **from the same
quantities the proposal uses**:

1. the same structure confidence set $C_\gamma$ at $\eta_\gamma$;
2. the same certified $\underline t_{\mathrm{cert}}$ and $\underline a_c$ at $\eta_t$;
3. $\bar S=\sum_c Y_c^2/(1+\underline t_{\mathrm{cert}}\underline a_c)\ \ge\ S(t;\gamma)$
   on that event, and $S(t)/A\sim\chi^2_K$ at the truth, so
   $$A_U=\bar S\big/\chi^2_{K,\alpha_2}$$
   covers $A$ with probability at least $1-\eta_\gamma-\eta_t-\alpha_2$.

Total error $\alpha_1+\alpha_2+\eta_\gamma+\eta_t$. Setting
$\alpha_1+\alpha_2=\alpha_0$ makes the budget **identical** to the proposal's
$\alpha_0+\eta_\gamma+\eta_t$. The split $(\alpha_1,\alpha_2)$ is scanned and the
**narrowest valid choice is given to the competitor**, as was done for the
enlargement comparator earlier.

So the two differ in exactly one place: the proposal spends $\alpha_0$ on a
conformal rank and the competitor spends it on a normal quantile plus a $\chi^2$
bound. Everything else — data, structure model, structure uncertainty, centre,
nominal level — is held equal.

A **plug-in Gaussian** interval $\pm z_{1-\alpha_0/2}\sqrt{\widehat A}$ is carried
as an invalid reference, and `sep_bonf`, `oracle` and `uncorrected` as before.

## Reported

Latent-target coverage and realised width first; the ratio competitor/proposal
paired on the same replicates; the chosen budget split; and wall-clock cost per
replicate for both, since computational cost is one of the criteria.

Correctly specified and misspecified structure reported separately.

## Grid

$K\in\{60,200\}$, $d/A\in\{0.5,1\}$, $\nu_c\in\{8,16\}$,
$\sigma_{\mathrm{mis}}\in\{0,0.4\}$; 16 cells, 10,000 replicates.
$\alpha_0=0.05$, $\eta_\gamma=\eta_t=0.025$.

## Predictions

| # | prediction | falsified by |
|---|---|---|
| G1 | both arms cover at or above $1-\alpha_0-\eta$ when correctly specified | either failing |
| G2 | the Gaussian competitor is **narrower**, because it exploits a normal shape the conformal step does not | the proposal winning |
| G3 | the gap narrows as $K$ grows, since the conformal rank loses less at larger $K$ | no dependence on $K$ |
| G4 | under misspecified structure both degrade similarly, since they share the scale machinery | one degrading much more |

**G2 predicts the proposal loses on width.** That is the honest expectation under
Gaussian truth and it is written down before running. If it holds, the paper's
case rests on what the conformal step buys elsewhere — and that has to be
demonstrated, not asserted.

## Outcomes

1. **G2 holds.** The efficiency cost under Gaussian conditions is stated, and the
   manuscript must then show where the rank step earns it back — non-normal
   shape being the obvious candidate, which `exp01` already studies.
2. **G2 fails.** The proposal is narrower at equal information and level, and
   that is the efficiency claim.
3. **Widths are close.** Then the comparison is about guarantees, computation and
   assumptions, and the manuscript says so rather than claiming a width win.

No arm is added after seeing results.
