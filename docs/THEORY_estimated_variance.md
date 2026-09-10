# Theory memo — what estimating the sampling variance costs

Written 2026-09-10. Scope item (2) of the development plan: extend the
information statement of Section 4.2 from *known* $D_i$ to *estimated*
$\widehat D_i$, and check the result against the literature before any
simulation programme is designed around it.

This memo is deliberately narrow. It closes one model completely rather than
gesturing at the general one. What it does **not** cover is listed in §7, and
the list is the agenda for the next memos.

---

## 1. What is observed, and what separates $A$ from $D_i$

The manuscript's information statement (eq. 12) assumes the design variances
$D_i$ are known. They never are. Write the minimal model that makes the
distinction visible and nothing else:

> **Model M1.** Independently across populations $i=1,\dots,m$,
> $$Y_i\sim N(\mu_i,\;A+D_i),\qquad \frac{\nu_i\widehat D_i}{D_i}\sim\chi^2_{\nu_i},
> \qquad Y_i\perp\widehat D_i,$$
> with $\mu_i$ and $\nu_i$ known, $A>0$ the parameter of interest, and
> $D_1,\dots,D_m>0$ unknown nuisance parameters.

Three modelling decisions carry the whole memo and each is a real assumption:

- **$D_i$ is a free parameter per population, not a known constant.** The
  observation $\widehat D_i$ is the *only* information about it. This is the
  point of departure from Section 4.2.
- **$\nu_i$ is known.** For a replication variance estimator this is the design
  degrees of freedom — PSUs minus strata — not the number of replicates. §5
  makes that distinction exact, because it is the one a practitioner is most
  likely to get wrong.
- **$Y_i\perp\widehat D_i$.** True for a Gaussian mean; **false for a CDF
  ordinate**, which is this paper's actual estimand. §7.1 states why, and it is
  the single most important limitation of M1.

The identification is then transparent. There are $2m$ observations and $m+1$
parameters. $\widehat D_i$ identifies $D_i$; $Y_i^2$ identifies $A+D_i$; $A$ is
identified by the difference, population by population, and pooled across $m$.
Nothing else in the model informs $A$. That is what makes the information
calculation below the complete answer for M1 rather than a bound of convenience.

---

## 2. The effective information

> **Proposition 1.** Under M1, the effective Fisher information for $A$, after
> profiling out $D_1,\dots,D_m$, is
> $$I_{\mathrm{eff}}(A)=\frac12\sum_{i=1}^m\frac{1}{(A+D_i)^2+D_i^2/\nu_i}.$$

*Proof.* Write $V_i=A+D_i$ and $\ell_i=\ell_i^{Y}(V_i)+\ell_i^{V}(D_i)$, the
two summands being the Gaussian and $\chi^2$ log-likelihoods. Since
$\partial V_i/\partial A=\partial V_i/\partial D_i=1$ and $\ell^V_i$ does not
involve $A$,
$$I_{AA,i}=E\big[(\partial_V\ell^Y_i)^2\big]=\frac{1}{2V_i^2},\qquad
I_{AD_i}=\frac{1}{2V_i^2},\qquad
I_{D_iD_i}=\frac{1}{2V_i^2}+\frac{\nu_i}{2D_i^2},$$
the cross term using $E[\partial_V\ell^Y_i\,\partial_{D}\ell^V_i]=0$ by
independence and zero score means, and $I_{D_iD_i}$ using the standard
$\chi^2$ information $\nu_i/(2D_i^2)$. The full information matrix is an
arrowhead: $A$ couples to every $D_i$, and the $D_i$ do not couple to each
other. Its Schur complement in the $A$ entry is therefore additive over $i$,
$$I_{\mathrm{eff}}(A)=\sum_i\left[\frac{1}{2V_i^2}
-\frac{(2V_i^2)^{-2}}{(2V_i^2)^{-1}+\nu_i(2D_i^2)^{-1}}\right]
=\sum_i\frac{1}{2V_i^2}\cdot\frac{\nu_iV_i^2}{D_i^2+\nu_iV_i^2}
=\sum_i\frac{1}{2\big(V_i^2+D_i^2/\nu_i\big)} .\qquad\square$$

Setting $\nu_i\to\infty$ recovers $\tfrac12\sum_i(A+D_i)^{-2}$, the
manuscript's eq. (12). The estimated-variance problem differs from the known
one by the single additive term $D_i^2/\nu_i$ in each denominator.

**In the paper's units.** With $K_I:=2A^2I$,
$$K_{I,\mathrm{eff}}=\sum_{i=1}^m\frac{A^2}{(A+D_i)^2+D_i^2/\nu_i},
\qquad\text{and}\qquad \mathrm{RSE}(\widehat A)\ \ge\ \sqrt{2/K_{I,\mathrm{eff}}}.$$
In the equal-variance case $D_i\equiv D$, $\nu_i\equiv\nu$, with the design
share $\rho^2=D/(A+D)$ as in eq. (7),
$$\boxed{\;K_{I,\mathrm{eff}}=m\,\frac{(1-\rho^2)^2}{1+\rho^4/\nu},\qquad
\mathrm{RSE}(\widehat A)\ \ge\ \sqrt{\frac{2}{m}}\;
\frac{\sqrt{1+\rho^4/\nu}}{1-\rho^2}\;}$$
and the manuscript's feasibility boundary (eq. 15, at $h=0$) becomes
$$m\ \ge\ \frac{2\,(1+\rho^4/\nu)}{\tau^2\,(1-\rho^2)^2}.$$

**Reading.** The penalty factor is $1+\rho^4/\nu$, and it is *fourth* order in
the design share. Both ingredients are needed for it to bite: the sampling
error must dominate ($\rho\to1$) **and** be itself poorly measured ($\nu$
small). At the largest design share in our applications, $\rho=0.66$, and a
plausible regional $\nu=10$, the requirement rises by 1.9 percent. At
$\rho=0.9,\ \nu=5$ it rises by 13 percent.

> **This is the memo's first substantive finding, and it is negative.** In M1,
> estimating the sampling variance costs almost no information about $A$ at
> survey-realistic design shares. The boundary of Section 4 is close to correct
> as written. A paper whose contribution was "we account for estimated
> sampling variances in the information bound" would be a paper about a
> two-percent correction.

§4 is where the real cost is.

---

## 3. The bound is sharp, and by a computable estimator

A Cramér–Rao statement alone would be open to the objection the plan raises:
a lower bound for unbiased estimators does not tell us what is achievable. In
M1 the gap closes exactly, in finite samples.

> **Proposition 2.** Let $Z_i=(Y_i-\mu_i)^2$ and, for fixed weights $w_i>0$,
> $$\widehat A_w=\frac{\sum_i w_i\,(Z_i-\widehat D_i)}{\sum_i w_i}.$$
> Then $\widehat A_w$ is exactly unbiased for $A$ for every $m$ and every $w$,
> with
> $$\mathrm{Var}(\widehat A_w)=\frac{2\sum_i w_i^2\big[(A+D_i)^2+D_i^2/\nu_i\big]}
> {\big(\sum_i w_i\big)^2},$$
> minimised at $w_i^\star\propto\big[(A+D_i)^2+D_i^2/\nu_i\big]^{-1}$, where it
> equals $1/I_{\mathrm{eff}}(A)$ exactly.

*Proof.* $E Z_i=A+D_i$ and $E\widehat D_i=D_i$ give unbiasedness.
$\mathrm{Var}(Z_i)=2(A+D_i)^2$, $\mathrm{Var}(\widehat D_i)=2D_i^2/\nu_i$, and
the two are independent, so the variance is as stated. Minimising a ratio of
quadratic forms (equivalently, Cauchy–Schwarz) gives $w_i^\star$ and the value
$2/\sum_i[(A+D_i)^2+D_i^2/\nu_i]^{-1}=1/I_{\mathrm{eff}}$. $\square$

So the information bound of Proposition 1 is attained, not merely approached,
and by a moment estimator rather than by a likelihood argument. Three
consequences:

1. **The bound is the right object.** It is not slack, and the "necessary but
   not sufficient" caveat that applies to a generic Cramér–Rao argument does
   not apply here: in M1 the necessary condition is also achieved.
2. **The oracle is the weights, not the estimator.** $w^\star$ depends on the
   unknown $(A,D_i)$. A two-step version substitutes consistent estimates and
   loses only second-order terms — with one caveat, which is §4.
3. **Equal weights are the Prasad–Rao / Fay–Herriot moment estimator**,
   $\widehat A=m^{-1}\sum_i(Z_i-\widehat D_i)$. It is unbiased under estimated
   $D_i$ too, and its efficiency loss relative to the bound is exactly the
   Cauchy–Schwarz gap, i.e. the dispersion of $(A+D_i)^2+D_i^2/\nu_i$.

---

## 4. Where the cost actually is: plug-in bias that does not vanish in $m$

Standard practice is not $\widehat A_{w^\star}$. It is to substitute
$\widehat D_i$ for $D_i$ wherever $D_i$ appears in a known-variance procedure —
ML, REML, or the iterated Fay–Herriot equation — and proceed as though the
substitution were free. The information calculation of §2 says nothing about
this, because that estimator is not unbiased.

Take the known-$D$ ML score with $\widehat D_i$ plugged in:
$$g(A)=\sum_i\frac{Z_i-A-\widehat D_i}{(A+\widehat D_i)^2}.$$
At the true $A$, writing $\delta_i=\widehat D_i-D_i$ and expanding
$f(x)=(A+x)^{-2}$ about $D_i$,
$$E\,g(A)=\sum_iE\big[-\delta_i f(D_i+\delta_i)\big]
\approx-\sum_i f'(D_i)\,\mathrm{Var}(\widehat D_i)
=\sum_i\frac{4D_i^2}{\nu_i(A+D_i)^3}\;>\;0 .$$
The plug-in estimating function is **positively** biased at the truth. With
$-E\,g'(A)\approx\sum_i(A+D_i)^{-2}$,
$$\mathrm{Bias}(\widehat A_{\mathrm{plug}})\;\approx\;
\frac{\sum_i 4D_i^2\big/\big[\nu_i(A+D_i)^3\big]}{\sum_i(A+D_i)^{-2}},
\qquad\text{and with }D_i\equiv D,\ \nu_i\equiv\nu:\qquad
\boxed{\;\frac{\mathrm{Bias}}{A}\;\approx\;\frac{4\rho^4}{\nu\,(1-\rho^2)}\;}$$

Three properties, and each of them matters more than §2 did.

**(a) It does not shrink with the number of populations.** The bias is
$O(1/\nu)$, and $\nu$ is a property of each survey's design, not of how many
surveys are stacked. The standard deviation is $O(m^{-1/2})$. Bias therefore
overtakes noise once
$$m\;\gtrsim\;\frac{\nu^2\,(1+\rho^4/\nu)}{8\rho^8}\;\approx\;\frac{\nu^2}{8\rho^8}.$$
At $\rho=0.9,\ \nu=10$ this is $m\approx29$. At $\rho=0.66,\ \nu=10$,
$m\approx350$. **Refining the calibration unit — the paper's own prescription
in Section 6.6 — raises $m$ and lowers $\nu$ simultaneously, and so moves an
analyst into the bias-dominated regime from both sides.**

**(b) The sign is the dangerous one.** $\widehat A$ is biased **upward**, so
the deconvolved scale $\widehat s_G^2$ is overstated, so the reliability
diagnostic $D=\mathrm{SE}/\widehat s_G^2$ of eq. (14) is **understated**, so
the reliability gate opens more readily than it should. (§9 qualifies this:
the sampling variability of $\widehat A$ pushes the other way through
$E[1/\widehat A]>1/A$, and which effect wins is regime-dependent. Bias wins at
the design shares the applications exhibit.) The one gate the
manuscript characterises is anti-conservative under estimated design
variances, in the direction that admits corrections that are not in fact
determined. Simultaneously $\widehat\rho^2=\widehat D/(\widehat A+\widehat D)$
is understated, so the *need* gate opens less readily. The two gates are moved
in opposite directions by the same error.

**(c) It is a property of the weights, not of estimating $A$.** Equal weights
(Prasad–Rao) are unbiased; the bias is generated entirely by the correlation
between $\widehat D_i$ in the weight and $\widehat D_i$ in the residual. This
converts the choice among variance-component estimators from an efficiency
question — where REML wins, as exp05 showed — into a **bias** question, where
REML loses. It also supplies a principled reading of what smoothed design
variances (GVF, or the variance-smoothing models of the small-area literature)
buy: weights built from a smoothed $\widetilde D_i$ are nearly independent of
the residual, which removes the leading bias term. That is a stronger argument
for smoothing than "the estimates are noisy".

> **This is the memo's central claim.** The consequential effect of estimating
> $D_i$ is not information loss, which is $O(\rho^4/\nu)$ and negligible here.
> It is a plug-in bias of order $\rho^4/\nu$ **relative to a small $A$**, which
> does not average away over populations and which moves the manuscript's
> feasibility gate in the anti-conservative direction.

---

## 5. Degrees of freedom are not replicates

$\nu_i$ enters everything above, so it must be pinned down. Suppose
$\widehat D_i$ is computed from $B$ resampling replicates. Then
$$\mathrm{Var}(\widehat D_i)\;=\;\underbrace{\frac{2D_i^2}{\nu_i^{\mathrm{des}}}}
_{\text{design}}\;+\;\underbrace{\frac{\kappa_iD_i^2}{B}}_{\text{Monte Carlo}}
\;\Longrightarrow\;
\nu_i^{\mathrm{eff}}:=\frac{2D_i^2}{\mathrm{Var}(\widehat D_i)}
=\frac{\nu_i^{\mathrm{des}}}{1+\kappa_i\nu_i^{\mathrm{des}}/(2B)} .$$
Raising $B$ drives $\nu^{\mathrm{eff}}$ up to the ceiling
$\nu^{\mathrm{des}}$ and no further. The ceiling is set by the design — PSUs
minus strata — and no amount of computation raises it. Every quantity in §2
and §4 saturates at that ceiling.

This is directly relevant to `exp03b`, which found the reliability gate opening
in a different number of arms under an $m$-of-$m$ resample than under
Rao–Wu–Yue. Both estimate the same $D_i$; they differ in $\nu^{\mathrm{eff}}$
and in bias. The framework above says which direction that difference should
push the gate, which is a prediction `exp03b` can be re-read against.

---

## 6. Literature check

Searched 2026-09-10. The relevant body of work is Fay–Herriot with estimated
sampling variances.

| line of work | what it does | overlap |
|---|---|---|
| Rivest & Vandal (2002), Wang & Fuller (2003, *JASA* 98:716) | MSE of the small-area predictor when $D_i$ is estimated; extra MSE term; moment estimators | Same model M1. **They target the MSE of the predictor**, not the information about $A$. |
| You & Chapman (2006); Maiti, Ren & Sinha (2014); Sugasawa, Tamae & Kubokawa (2017); Dass et al. | Hierarchical/EB models placing a prior on $D_i$ and shrinking variances as well as means | Same $\chi^2$ sampling model. **Construct better estimators**; no information or feasibility statement. |
| Gao & Wakefield (2022, arXiv:2209.02602); Erciulescu et al. (2019); Parker et al. (2024) | Spatial variance-smoothing area-level models | Smoothing as method. Motivates §4(c) but does not quantify it. |
| Wakefield group (arXiv:2604.23029, 2026) | Derives sampling distributions for complex-design variance estimators in FH; shows known-$D$ FH undercovers | Closest recent work. Explicitly **does not** derive Fisher information, effective sample size, or a precision criterion; the case is made by simulation. |
| Acero, Molina & Marín (arXiv:2403.15384) | Bootstrap MSE reflecting estimated-variance uncertainty | Computational route to the same uncertainty; no analytic bound. |
| Partlett & Riley (2017); DerSimonian–Laird | Meta-analytic $\tau^2$ with estimated within-study variances | The same coupling empirically; within-study variances usually treated as known. |

**Provisional gap statement, to be confirmed by a proper reference check
before anything is written for the manuscript.** The literature *models* the
uncertainty in $\widehat D_i$ and *corrects* the MSE for it. What appears
absent is:

1. the effective information $I_{\mathrm{eff}}$ of Proposition 1 stated as
   such, and its use as a planning quantity ($K_{I,\mathrm{eff}}$, the revised
   boundary of §2);
2. the closed-form plug-in bias $4\rho^4/[\nu(1-\rho^2)]$ of §4, and in
   particular its **non-vanishing in $m$** and its **direction relative to a
   feasibility gate**;
3. the $\nu^{\mathrm{eff}}$ ceiling of §5 as an explicit statement that
   replicate count cannot substitute for design degrees of freedom.

Item 1 alone is a re-expression and, by its own magnitude (§2), a small one.
**Items 2 and 3 are what would justify the section.** The honest framing is
therefore: the information extension is a corollary, not the contribution; the
contribution is that the standard plug-in practice fails in a way the
information calculation does not detect.

---

## 7. What M1 assumes away, in priority order

**7.1 $Y_i\perp\widehat D_i$ is false for the paper's estimand.** M1 is written
for a mean. This paper's $Y_i(j)$ is a *CDF ordinate*, whose design variance is
approximately $p_i(j)\{1-p_i(j)\}/n_i^{\mathrm{eff}}$ — a deterministic
function of the same quantity being estimated, to first order. So $\widehat D_i$
and $Y_i$ are strongly dependent, the cross-information $I_{AD_i}$ acquires a
term M1 omits, and the plug-in bias of §4 acquires a second source. This is the
first extension to derive, and it is the one that is specific to this paper's
setting rather than inherited from small-area estimation. It is also where a
distinctive contribution is most likely to be.

**7.2 Independence across populations.** Plan item (3). Regions within a
country share a common national estimate and an aggregation constraint. Under
M1, $m$ regions supply $m$ independent contributions; that is precisely what
the block structure denies. **No presumption is made here that dependence
must reduce information** — the correct statement depends on what is being
estimated and what covariance is known, and deriving it is the work.

**7.3 $\nu_i$ known.** In practice $\nu_i$ is itself approximated
(Satterthwaite). Misspecifying $\nu$ propagates into §4's bias correction.

**7.4 Gaussianity, and $A$ near zero.** The $\chi^2$ model for $\widehat D_i$
is exact only for a normal linear statistic under simple designs. Separately,
when $A\to0$ every *relative* criterion in this memo degenerates — and $A\to0$
is a real operating regime, not a corner case. A criterion stated on the
relative-error scale is the wrong criterion there; the plan's point that a
small $A$ can still support a good shrunken prediction is the reason, and it
argues for restating the feasibility target on a decision or risk scale rather
than as $\mathrm{RSE}(\widehat A)\le\tau$. That restatement is plan item (4)
and this memo does not attempt it.

**7.5 Estimation of $\mu_i$.** With $\mu_i=x_i'\beta$ estimated, $Z_i$ becomes
a squared residual, the moment estimator carries the usual $m-p$ divisor, and
the information for $A$ is reduced by an $O(p)$ term. This changes constants,
not conclusions.

---

## 8. Predictions to check numerically

Stated before execution; the protocol is `docs/PROTOCOL_exp09_estimated_variance.md`.

| # | prediction | falsified by |
|---|---|---|
| P1 | $I_{\mathrm{eff}}$ of Prop. 1 matches the observed information of simulated joint likelihoods | disagreement beyond Monte Carlo error |
| P2 | $\widehat A_{w^\star}$ is unbiased and its variance equals $1/I_{\mathrm{eff}}$ exactly | any systematic departure |
| P3 | naive plug-in REML/ML is biased upward by $\approx4\rho^4/[\nu(1-\rho^2)]$ | wrong sign, or bias shrinking in $m$ |
| P4 | that bias does not shrink as $m$ grows at fixed $\nu$ | bias falling with $m$ |
| P5 | the naive reliability diagnostic $D$ of eq. (14) is understated, so the gate opens too often | gate opening less often, or unchanged |
| P6 | equal-weight (Prasad–Rao) moment estimation is unbiased under estimated $D_i$ at all $\nu$ | any bias beyond Monte Carlo error |

P3–P5 are the ones that carry the section. P1–P2, P6 are arithmetic checks:
if they fail, the derivations above are wrong.

---

## 9. Verification

`experiments/exp09_estimated_variance.py`, protocol
`docs/PROTOCOL_exp09_estimated_variance.md`, results
`results/exp09_estimated_variance.csv`. 100 cells,
$m\in\{30,100,250,500,1000\}$, $\rho\in\{0.3,0.5,0.66,0.9\}$,
$\nu\in\{5,10,25,100,\infty\}$, 2,000 replicates each, $A=1$.

**P1 — the information identity holds exactly.** The variance of the analytic
effective score matches $I_{\mathrm{eff}}$ to $9\times10^{-16}$ across all
cells. Proposition 1 is arithmetic and it is right.

**P2 — the bound is attained, exactly.** The ratio of the realised variance of
$\widehat A_{w^\star}$ to $1/I_{\mathrm{eff}}$ has mean 0.9989 and median
0.9986 over the 100 cells, against a Monte Carlo standard error of 0.0316 for
a variance ratio at 2,000 replicates. Proposition 2 holds in finite samples,
not asymptotically.

**P6 — equal weights are unbiased under estimated $D_i$**, at every $\nu$ and
every $\rho$; the largest standardised bias over 100 cells is $|z|=3.25$, the
expected maximum for 100 draws.

**§2 confirmed, and it is as small as claimed.** $K_{I,\mathrm{eff}}$ relative
to the known-$D$ $K_I$, at $m=250$:

| $\rho$ | $\nu=5$ | 10 | 25 | 100 |
|---|---|---|---|---|
| 0.30 | 0.998 | 0.999 | 1.000 | 1.000 |
| 0.50 | 0.988 | 0.994 | 0.998 | 0.999 |
| **0.66** | **0.963** | **0.981** | 0.993 | 0.998 |
| 0.90 | 0.884 | 0.938 | 0.974 | 0.994 |

At the largest design share in the applications the information cost of
estimating the sampling variances is under 4 percent even at 5 degrees of
freedom. **The information extension is a footnote to the boundary, and the
memo's §2 was right to say so.**

**P3 and P4 — the plug-in bias is real, positive, and flat in $m$.** Relative
bias of the plug-in ML estimator, $A=1$:

| $\rho$, $\nu$ | $m{=}30$ | 100 | 250 | 500 | 1000 | first-order prediction |
|---|---|---|---|---|---|---|
| 0.50, 10 | 0.025 | 0.027 | 0.020 | 0.031 | 0.031 | 0.033 |
| 0.66, 25 | 0.054 | 0.038 | 0.052 | 0.048 | 0.050 | 0.054 |
| **0.66, 10** | **0.097** | **0.105** | **0.111** | **0.111** | **0.109** | 0.134 |
| 0.66, 5 | 0.158 | 0.170 | 0.189 | 0.185 | 0.186 | 0.269 |
| 0.90, 10 | 0.937 | 0.964 | 0.991 | 1.002 | 0.998 | 1.381 |

Thirty-three-fold growth in the number of populations does not reduce the bias
at all. The closed form of §4 is accurate while $\rho^4/\nu$ is small and
**overstates** the bias when it is not — at $\rho=0.9$ the first-order
expansion is not valid, though the bias it fails to quantify is a 100 percent
overstatement of $A$. Using the formula for planning is therefore conservative
about the bias in the same way the equal-variance closed form is conservative
about the requirement.

At $\rho=0.66,\nu=10$ the realised bias equals the bound's standard deviation
at $m\approx530$. The regional configurations of Section 6 sit at $m$ between
100 and 290, i.e. one refinement step below that crossover.

**P5 — the gate moves, and at the operating point it opens far too often.**
Share of replicates on which the reliability diagnostic of eq. (14) passes
$\tau=0.147$, at $\rho=0.66$, $m=250$, which is the regional operating point of
Section 6:

| $\nu$ | correctly scaled | plug-in $\widehat A$ | equal-weight $\widehat A$ |
|---|---|---|---|
| 5 | 0.137 | **0.849** | 0.084 |
| 10 | 0.179 | **0.585** | 0.087 |
| 25 | 0.190 | 0.297 | 0.112 |
| 100 | 0.218 | 0.144 | 0.104 |

At ten design degrees of freedom the standard practice opens the reliability
gate on 59 percent of replicates where the correct scale opens it on 18. **The
one gate this manuscript characterises is anti-conservative under estimated
design variances, by a factor of three at the design share the regional
applications actually exhibit.**

**One honest qualification, which the prediction did not anticipate.** The
plug-in does not always open the gate more often. At low design shares and
small $m$ it opens it *less* often — at $\rho=0.3$, $m=100$ the plug-in passes
on 1 percent against 37 percent correctly scaled. Two effects compete:
the bias in $\widehat A$ inflates the denominator and opens the gate, while the
*variance* of $\widehat A$ acts through $E[1/\widehat A]>1/A$ and closes it.
Bias wins where $\rho^4/\nu$ is large; variance wins near the threshold where
the diagnostic is poised. The claim that survives is directional and
regime-specific, not universal, and it must be stated that way.

**An unplanned finding, and the sharpest one.** RMSE relative to the
information bound at $m=250$:

| $\rho$, $\nu$ | plug-in ML | equal-weight moment |
|---|---|---|
| 0.50, 10 | 1.007 | 0.990 |
| 0.66, 10 | **1.223** | 1.006 |
| 0.90, 10 | **2.274** | 1.007 |
| 0.66, 100 | 0.999 | 1.006 |

`exp05` established that REML attains the information bound when $D_i$ is
known, and concluded that the inflation cannot be evaded by a better estimator.
That conclusion is correct and its scope is narrower than it reads. Once $D_i$
is estimated, the likelihood-weighted estimator is 1.22 times the bound at the
regional operating point and 2.27 times at $\rho=0.9$, while the unweighted
moment estimator — dominated in the known-$D$ setting — sits on the bound.
**Estimating the sampling variances reverses the ranking of the two standard
variance-component estimators.** That is a statement about survey practice, it
is checkable, and it is the kind of consequence that would justify the section.

**§5, replicates against degrees of freedom.** With $\nu^{\mathrm{des}}=20$ and
Monte Carlo replication entering multiplicatively, $\nu^{\mathrm{eff}}$ is 6.3
at $B=10$, 13.9 at $B=50$, 16.4 at $B=100$, 19.6 at $B=1{,}000$ and 20.0 in the
limit. Raising $B$ from 100 to 10,000 buys 3.6 degrees of freedom; the design
supplies the rest and computation cannot.

**Outcome, against the protocol.** Outcome 1: P3, P4 and P5 hold at the
operating point, with the qualification above. The extension is not a
two-percent information correction; it is a bias result with a consequence for
the gate. What it is *not* yet is a statement about dependent populations, and
memo §7.1–7.2 remain the binding limitations.
