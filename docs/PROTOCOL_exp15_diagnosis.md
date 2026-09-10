# Protocol — exp15: why the GVF upper limit undercovers, and the K-p extension

Written 2026-09-10, before executing `experiments/exp15_diagnosis.py`.
Deliberately small. Predecessor: `exp14`.

## The error being corrected

`exp14` explained the GVF-based upper limit's undercoverage as "smaller variance
and positive bias, a tighter interval around a displaced centre". **For a
one-sided upper limit that reasoning is backwards.** Failure of
$A_U=\widehat A+z_{1-\eta}\widehat{\mathrm{se}}$ is
$(\widehat A-A)/\widehat{\mathrm{se}}<-z_{1-\eta}$, a left-tail event, and with
$\widehat A=A+b+\sigma Z$ at known $\sigma$ the coverage is
$\Phi(z_{1-\eta}+b/\sigma)$, which a positive $b$ **increases**. So the observed
0.900 is not explained by the bias and the cause is unidentified.

This is a diagnosis on the two cells that failed, not a new sweep.

## Block 1 — candidate causes, on $K=60$, $\bar D/A=4$, $\sigma_e\in\{0,0.6\}$

Recorded in this order, because the first split settles most of it:

1. **Is the standard error understated?** Mean $\widehat{\mathrm{se}}$ against
   the realised standard deviation of $\widehat A_{\mathrm{GVF}}$.
2. **Is the left tail non-normal?** Mean, standard deviation and 2.5 percent
   quantile of $(\widehat A-A)/\widehat{\mathrm{se}}$ against $-1.96$.
3. **Is the variance formula evaluated at the wrong argument?**
   `exp14` used $\mathrm{Var}(Z_i)=2(A+\widetilde D_i)^2+2\widetilde D_i^2/\nu$
   at the **smoothed** $\widetilde D_i$. Since the true $D_i$ scatters around it
   and the variance is convex in $D$, this is a candidate for understatement,
   and it should worsen with $\sigma_e$. Compared against the same formula at
   $\widehat D_i$, and at the true $D_i$.
4. **Is the weight-estimation uncertainty missing?** `exp14` treated $w$ as
   fixed. Compared against a delete-one-population jackknife over the **whole**
   procedure — GVF refit, weights recomputed, subtraction redone.
5. **Is it the bootstrap form?** `exp14` used a basic upper limit at $B=200$,
   where the 2.5 percent tail rests on about five replicates. Compared against
   percentile and studentized forms at $B=2{,}000$ on these two cells only.

## Block 2 — the extension to an unknown mean

With $Y\sim N(X\beta,\,AI+\mathrm{diag}(\mathbf D))$ and $\mathrm{rank}(X)=p<K$,
$$Q(a,\mathbf D)=\min_\beta\sum_c\frac{(Y_c-x_c^\top\beta)^2}{a+D_c}
\quad\Longrightarrow\quad Q(A,\mathbf D)\sim\chi^2_{K-p},$$
because standardising and projecting off a rank-$p$ space leaves $K-p$ degrees
of freedom; and $Q(a,\mathbf L)\ge Q(a,\mathbf D)$ on $E_D$ for every $\beta$,
so the minimum inherits it. The upper limit therefore extends **provided the
weighted regression is refitted at each candidate $a$** — reusing residuals
fitted at one $a$ and changing only the degrees of freedom is not the same
construction and is not tested as if it were.

Verified at $p\in\{1,3\}$: the null distribution of $Q(A,\mathbf D)$ against
$\chi^2_{K-p}$, and the coverage of the resulting $A_U$.

**This bounds the variance component only.** It says nothing about the error
from centring the band on an estimated mean, or about exchangeability of the
conformal scores under an estimated centre. Those stay open.

## Block 3 — the comparison the normality assumption now obliges

The pivot uses normality explicitly, not merely the common-shape assumption (S):
standardised curves sharing a law does not give $\sum_cW_c^2\sim\chi^2_K$ unless
that law is normal. Since normality is now an assumption of the method, a
normal-model T2 interval must be given the same information: same $A_U$, same
$\eta_1,\eta_2$, same $\alpha_0$. Reported beside the conformal band.

## Grid

Blocks 1 and 3: $K=60$ and $200$, $\bar D/A=4$, $\sigma_e\in\{0,0.6\}$,
$\nu=10$, 20,000 replicates; jackknife and bootstrap sub-blocks at 2,000.
Block 2: $K=60,200$, $p\in\{1,3\}$, 20,000 replicates.
$\eta_1=\eta_2=0.025$, $\alpha_0=0.05$.

## Predictions

| # | prediction | falsified by |
|---|---|---|
| V1 | the standard error is understated, ratio below 1 | ratio at 1, making it a tail-shape problem |
| V2 | evaluating the variance at $\widetilde D_i$ is a material part of it, worsening with $\sigma_e$ | no difference between the $\widetilde D$ and $\widehat D$ forms |
| V3 | the jackknife standard error is larger and its limit covers better | no improvement |
| V4 | a studentized bootstrap at $B=2{,}000$ covers better than basic at $B=200$ | no improvement |
| V5 | $Q(A,\mathbf D)\sim\chi^2_{K-p}$ and the $A_U$ from it covers | departure from $\chi^2_{K-p}$ |

## Outcomes

1. **V1--V3 hold and a corrected standard error restores coverage.** Then
   `exp14`'s negative reading is withdrawn: the GVF route was failing on an
   implementation of its uncertainty, not on principle, and the comparison must
   be redone with the corrected limit.
2. **Coverage is restored but the corrected limit is no narrower than the
   pivot.** Then the GVF route becomes a secondary result and the pivot carries
   the paper, but for a measured reason rather than a mistaken one.
3. **Coverage is not restored by any of the four repairs.** Only then is there
   evidence for something stronger than an implementation failure, and even then
   it is about these constructions, not about the possibility of a good one.

No cell is added after execution.
