# Protocol — exp13: what a feasible weighting recovers, and a band that is guaranteed

Written 2026-09-10, before executing `experiments/exp13_weights_and_containment.py`.
Predecessors: `exp09`, `exp12`.

Two questions that must not be merged, and are not merged here. Part A is about
estimating $A$. Part B is about whether a band contains the oracle band. **An
improvement in Part A is not evidence for Part B**, and the experiment is built
so that neither result can be read as the other.

## Standing correction to how efficiency is reported

`exp12` measured efficiency against $\sqrt{2/K_{I,\mathrm{eff}}}$, the bound for
*estimated* design variances, using root mean squared error, so bias is already
inside it. That is the right benchmark and it stays. What was missing is the
decomposition, which is added here and reported for every cell:

$$\underbrace{\sqrt{2/K_{I,\mathrm{known}}}}_{\text{ideal, }D_i\text{ known}}
\ \longrightarrow\
\underbrace{\sqrt{2/K_{I,\mathrm{eff}}}}_{\text{cost of estimating }D_i}
\ \longrightarrow\
\underbrace{\mathrm{RMSE}(\widehat A)}_{\text{cost of the procedure}} .$$

Only the third gap is recoverable by a better estimator. **"Three quarters of
the information is discarded" is restated as a statement about that third gap
only**, in the closed Gaussian--$\chi^2$ model, and not as a claim about survey
data.

## Part A — does a feasible weighting improve MSE at the same data budget?

### Generation, built so that a realistic independent weight exists

$D_i=c\,e_i/n_i$ where $n_i$ is a **design variable known without error** — a
sample size — and $e_i$ is lognormal model error with dispersion $\sigma_e$.
$\sigma_e=0$ is an exact generalised variance function; larger $\sigma_e$ is a
GVF that does not fit. $Y_i\sim N(0,A+D_i)$, $\nu\widehat D_i/D_i\sim\chi^2_\nu$,
$\mu_i$ known, populations independent.

The optimal moment weight is **not** $(A+D_i)^{-2}$. From
$Z_i=(Y_i-\mu_i)^2-\widehat D_i$ with
$\mathrm{Var}(Z_i)=2(A+D_i)^2+2D_i^2/\nu_i$ it is
$$w_i\propto\big\{(A+D_i)^2+D_i^2/\nu_i\big\}^{-1},$$
so the uncertainty of the subtracted variance estimate belongs in the weight.
That is what every weighted arm below targets.

### Arms, all evaluated on identical replicates

| arm | weights from | data used for the estimate |
|---|---|---|
| `unweighted` | none | all $K$ |
| `plugin` | own $\widehat D_i$ | all $K$ |
| `gvf_all` | GVF fitted on **all** populations, own $\widehat D_i$ included | all $K$ |
| `gvf_split` | GVF fitted on a training half only | evaluation half only |
| `gvf_cv` | two-fold cross-fitting | all $K$ |
| `oracle` | true $(A,D_i)$ | all $K$ |
| `unweighted_eval` | none | evaluation half only |

`gvf_all` is included because smoothing does **not** automatically produce
independence: fitting on a set containing population $i$ leaves $\widehat D_i$
in its own weight. `unweighted_eval` is the matched baseline for `gvf_split`,
so that halving the data cannot be mistaken for an improvement.
`gvf_cv` is reported with the caveat that combining folds needs its own
variance justification, which is not attempted here.

### Reported per arm

Bias, standard deviation, RMSE, efficiency against both bounds, the share of
replicates truncated at $\widehat A=0$ (before and after truncation), and the
largest single weight share $\max_i w_i/\sum_j w_j$ as an extreme-weight
diagnostic.

## Part B — a band whose containment is guaranteed by construction

The half-width $h_c(s,v_c)=|Y_c|/\sqrt{1+v_c^2/s^2}$ is increasing in $s$ and
**decreasing in $v_c$**. `exp12` bounded only $s_G$ and substituted
$\widehat v_c$, which is why its containment of the oracle band was 0.944 —
3.9 Monte Carlo standard errors below $1-\eta$ at 20,000 replicates, so a real
shortfall rather than noise.

The reference construction bounds both directions. With $\eta_1+\eta_2=\eta$,
take $s_U$ a one-sided upper limit for $s_G$ at $\eta_1$ and $v_{L,c}$
**simultaneous** lower limits at $\eta_2$, by Bonferroni
$v_{L,c}^2=\nu_c\widehat D_c/\chi^2_{\nu_c,\,1-\eta_2/K}$. Then
$$R_U=\operatorname{ord}_m\Big\{|Y_c|\big/\sqrt{1+v_{L,c}^2/s_U^2}\Big\}$$
contains the oracle half-width on the event $\{s_G\le s_U\}\cap\bigcap_c\{v_c\ge
v_{L,c}\}$, of probability at least $1-\eta$, by monotonicity in each argument.

This is expected to be wide. That is the point: **a procedure whose guarantee
holds gives the reference against which a narrower approximation can be judged.**

## Grid, fixed here

$K\in\{60,200\}$; $\bar D/A\in\{1,4\}$; $\sigma_e\in\{0,0.3,0.6\}$; $\nu_i=10$;
$n_i$ lognormal with $\sigma_{\log n}=0.8$; 20,000 replicates; $A=1$;
$\alpha_0=\eta=0.05$ with $\eta_1=\eta_2=0.025$; guaranteed level 0.90.

## Predictions

| # | prediction | falsified by |
|---|---|---|
| T1 | `plugin` fails, reproducing `exp12` | plug-in weighting performing well |
| T2 | `gvf_all` inherits part of that failure | `gvf_all` matching `gvf_split` |
| T3 | `gvf_split` beats `unweighted_eval` on RMSE at the same half-sample | no improvement on the matched baseline |
| T4 | `gvf_split` does **not** beat full-sample `unweighted` once the split cost is paid, except at high dispersion | beating it everywhere, or nowhere |
| T5 | the improvement degrades as $\sigma_e$ grows | insensitivity to GVF misfit |
| T6 | Part B containment is at least $1-\eta$; Part B is wider than `exp12`'s band | containment still short, or no width cost |

## Outcomes, all reported

1. **T3 and T4 both hold.** A feasible weighting recovers part of the gap but
   the split pays for it; cross-fitting is then the thing to justify properly,
   and that is the next task rather than a claim.
2. **T3 holds, T4 fails in the good direction.** A feasible weighting beats the
   standard construction outright on the same data. That would be the paper's
   estimation result and it needs the survey-design check before being claimed.
3. **T3 fails.** Independence of the weights is not sufficient, the diagnosis in
   `exp12` is incomplete, and joint modelling or an estimating-equation route is
   where to go instead. This outcome is expected to be reported as prominently
   as the others.
4. **T6 fails.** Then even the Bonferroni reference does not contain the oracle
   band, the monotonicity argument has a hole, and Part B is the blocking
   problem for the whole latent-target claim.

No arm is added after seeing results and no cell is dropped.
