# Protocol — exp20: the ratio construction against separate bounds, in Model R

Written 2026-09-10, before executing `experiments/exp20_ratio_pivot.py`.
Design specification: `docs/THEORY_ratio_pivot.md`.

## Model, and why this one

Model R of the specification: $Y_c\sim N(0,A+d\,a_c)$ with $a_c$ a **known**
relative variance structure, $\nu_c\widehat D_c/(d a_c)\sim\chi^2_{\nu_c}$
independent of $Y$. This is the heteroscedastic model in which reduction to one
ratio parameter $t=d/A$ is genuinely true rather than assumed — the error the
previous design sketch made and that this protocol exists to avoid repeating.

$a_c$ is generated as a design quantity and used as known. It is **not** fitted
to $\widehat D_c$.

## What is compared, at the same total budget $\alpha_0+\eta$

| arm | construction |
|---|---|
| `ratio` | one-sided $t_L$ from $T(t)=K\widehat d/\{tS(t)\}\sim F_{\nu,K}$ at $\eta$; band $R(t_L)$ |
| `separate` | the current procedure: $A_U$ from the $\chi^2_K$ pivot at $\eta_1$, Bonferroni $v_{L,c}$ at $\eta_2$, $\eta_1=\eta_2=\eta/2$ |
| `oracle` | $R(t)$ at the true $t$ — width reference and containment target |
| `uncorrected` | $\operatorname{ord}_m|Y_c|$ — no T2 guarantee claimed |

## Reported in this order, and the order is the point

1. **Level.** $\Pr\{t\ge t_L\}$ against $1-\eta$, and $\Pr\{A\le A_U\}$,
   $\Pr\{v_{L,c}^2\le D_c\ \forall c\}$ for the incumbent.
2. **Containment.** $\Pr\{R(\cdot)\ge R(t)\}$ for both.
3. **Width**, with realised latent-target coverage printed beside it.
4. Boundary rates: empty inversion set, $\widehat D_c=0$, infinite radius.

A narrower band from a construction whose level is wrong is not an improvement,
so width is not read before the first two rows.

## Grid

$K\in\{60,200\}$; $d/A\in\{0.5,1\}$ (the regional range `exp18` reached);
$\nu_c\in\{8,16\}$ common across populations; dispersion of the known structure
$\sigma_{\log a}\in\{0.5,1.2\}$. 16 cells, 20,000 replicates. $A=1$.
$\eta=0.05$, $\alpha_0=0.05$, guaranteed $1-\alpha_0-\eta=0.90$.
Monte Carlo error 0.0015 near 0.95 and 0.0021 near 0.90.

## Predictions

| # | prediction | falsified by |
|---|---|---|
| V1 | $\Pr\{t\ge t_L\}=1-\eta$ to Monte Carlo error, at every cell | any departure — the pivot is exact, so a departure is an implementation error |
| V2 | containment for `ratio` equals its level exactly, since $R$ is monotone in $t$ | containment differing from the level |
| V3 | `ratio` is narrower than `separate` | no narrowing, which stops this line at Model R |
| V4 | the gain grows with the dispersion of $a_c$ and with $K$, because those are what the Bonferroni step charges for | no dependence on either |
| V5 | both cover the latent target at or above 0.90 | undercoverage |

## Outcomes, all reported

1. **V1–V3 hold.** Bounding the ratio directly reduces conservatism under
   correct error control in the exact case. The line proceeds to route (a) or (b)
   of the specification, and the size of the gain sets expectations for it.
2. **V1–V2 hold, V3 fails.** The separate-bounds conservatism is not where the
   width goes even in the exact case. The line stops here and the result is
   reported as a negative one about the construction, not about the idea.
3. **V1 fails.** Implementation error; nothing downstream is read.

No arm is added and no cell dropped after execution. The general-$\mathbf D$
routes are specified in `docs/THEORY_ratio_pivot.md` §3 and are **not** run here.
