# Protocol — exp18: the regional design share, by two different routes

Written 2026-09-10, before executing `experiments/exp18_regional_share.py`.
Predecessor: `exp17`. **The procedures and the error budget are those already
fixed and are not changed after seeing results.**

## Why

`exp17` reached $\bar D/A=0.038$ to $0.126$, the manuscript's national regime.
There the correction has little to do: in the equal-variance idealisation the
oracle scale factor is $\{1+D/A\}^{-1/2}$, so the whole available narrowing is
1.8 percent at $D/A=0.038$ and 5.8 percent at $0.126$, against 18.4 percent at
$0.5$ and 29.3 percent at $1$. **A band that adds 1 to 8 percent over the oracle
is not a demanding test when a method that barely corrects at all would also sit
near the oracle.** This experiment moves to where the correction matters.

## Two routes to the same design share, deliberately kept apart

| route | knob | what also changes |
|---|---|---|
| `small_sample` | fewer PSUs sampled and smaller clusters | $D$ up, **and** design degrees of freedom down, zero-variance rate up, normal approximation worse |
| `low_signal` | smaller between-population spread $\tau$ | $A$ down only; the design and $\nu$ are untouched |

Equal $\bar D/A$ by the two routes is **not** equal difficulty, and reporting one
as if it stood for both would be the mistake this split exists to avoid. The
`small_sample` designs are fixed first — $(m,n)=(3,4)$ with $\nu=8$ and
$(2,2)$ with $\nu=4$ — their realised $\bar D/A$ recorded, and $\tau$ is then
tuned so that `low_signal` matches those same values on the original design
($m=5$, $n=10$, $\nu=16$). The comparison is therefore paired at equal design
share.

## Constructions — unchanged, plus one reference

`piv`, `piv_fit`, `pct`, `pct_normal`, `oracle` exactly as in `exp17`, plus:

**`uncorrected`** — the observed anchor radius $|Y|_{(m)}$ used for the latent
target with no scale correction at all. **No T2 guarantee is claimed for it.**
It is there to answer the question `exp17` could not: how much of the
correction's apparent success is the correction, and how much is that the
correction was barely needed. Its realised T2 coverage and width are reported
beside the others.

## Diagnostics corrected from `exp17`

1. **The simultaneous lower limits are judged directly, not inferred.** `exp17`
   argued from a smaller-than-$\chi^2$ variance that the Bonferroni limits must
   be conservative. That does not follow from a variance. What the argument
   needs is $\Pr\{v_{L,c}^2\le D_c\ \text{for all }c\}$ against $1-\eta_2$, and
   that is now computed directly.
2. **$D_c=0$ and $\widehat D_c=0$ are separated and their handling stated.**
   The first is a finite population with no within-stratum spread; the second is
   a sample that saw none. Both rates are reported. The rule used throughout is
   that $\widehat D_c$ is floored at $10^{-12}$, which sends $v_{L,c}\to0$ and so
   applies **no** shrinkage to that population — conservative for the band, and
   recorded rather than left implicit.
3. **The correlation is decomposed.** `exp17` pooled
   $\mathrm{corr}(\widehat D_c,Y_c)$ over populations and replicates, which mixes
   the between-population relation between the true $D_c$ and the true $F_c$
   with the within-population sampling dependence of $\widehat D_c$ and
   $\widehat F_c$. Both are computed separately, the second from repeated samples
   of fixed populations.

## Grid

Routes $\times$ two design-share levels $\times$ $t_0\in\{$median$, 0.15\}$
$\times$ $K\in\{60,200\}$ = 16 cells. 2,000 replicates, $B=500$ (`exp16` showed
the replicate count worth at most 0.9 points). $\sigma_\alpha=0.4$ throughout so
the route comparison is not confounded by the design effect.
$\eta_1=\eta_2=0.025$, $\alpha_0=0.05$, guaranteed 0.90.
Monte Carlo error about 0.0067 near 0.90 and 0.0035 near 0.975.

## The three questions this is meant to answer

1. Does the final T2 coverage hold **where the correction is actually needed**?
2. Is the corrected band **materially narrower than the uncorrected one**?
3. If the oracle fails, is the problem variance estimation or distributional
   shape? — separable because the oracle uses the true $A$ and true $D_c$, so its
   failure cannot be a variance-estimation failure.

## Predictions

| # | prediction | falsified by |
|---|---|---|
| Y1 | at equal $\bar D/A$, `small_sample` is harder than `low_signal` | the two routes behaving alike |
| Y2 | `piv` keeps T2 coverage at or above 0.90 on both routes | undercoverage |
| Y3 | the corrected band is materially narrower than `uncorrected` here, unlike `exp17` | no material narrowing |
| Y4 | the oracle band holds; if it fails it fails on the `small_sample` route | oracle failure on `low_signal` |
| Y5 | `pct` fails again at the tail quantile | it holding |

## Outcomes, all reported

1. **Y2 and Y3 hold on both routes.** The procedure has a demonstrated range
   that includes the regime the manuscript's regional configurations occupy.
2. **Y2 holds, Y3 fails.** The correction is valid and not worth doing at this
   design share, which is a finding about the method's usefulness and must be
   reported as prominently as a success.
3. **Y2 fails on `small_sample` only.** The range of application is stated in
   terms of design degrees of freedom, not design share.
4. **The oracle fails.** Then the binding problem is the shape assumption and
   the target definition, and no variance-limit work addresses it.

No construction is added and no cell dropped after execution.
