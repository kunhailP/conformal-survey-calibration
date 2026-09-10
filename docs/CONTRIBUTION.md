# Contribution and positioning

Written 2026-09-10. Completion criterion 1 of the fixed plan: state, against the
closest prior work and at the level of targets and assumptions, what this paper
adds. Nothing here is a result; it is the claim the manuscript must support.

---

## 1. The question the paper answers

> **To remove the sampling error from survey estimates and predict a latent
> population summary, what information is required, how is the uncertainty in
> that information carried into the prediction interval, and when is the result
> worth using on real survey data?**

The contribution sentence, at the width the evidence supports:

> This paper gives a procedure for predicting the latent summary of a population
> with no direct estimate, which carries into the prediction interval the
> uncertainty of a relative design-variance structure estimated from the observed
> populations' survey and design-variance estimates; states what it guarantees
> and under which assumptions; makes the interval computable with a conservative
> bound rather than an optimisation; and reports the survey conditions under
> which it improves on comparators and those under which it does not.

**And one scope limit on the motivation.** That an unobserved population forces a
deconvolution is true *of a correction that rescales by the latent scale*, which
is the construction studied here. It is not a claim that every possible interval
for a latent target must separate the components.

Three claims answer it, and the manuscript is organised around them rather than
around the experiments that produced them.

**Claim 1 — the information.** The precision with which sampling variance can be
subtracted from between-population dispersion depends jointly on the number of
populations, the design share, and the degrees of freedom behind the variance
estimates; and **the quantity that governs the band is not the variance
component.** Stated for named models and estimator classes.

**Claim 2 — the procedure.** Under a relative design-variance structure, a
latent-target prediction interval can be built that carries the **estimation
uncertainty of that structure** into the final band rather than substituting a
fitted value, with a conservative computational bound so the interval is an
algorithm and not an optimisation.

**Claim 3 — the operating conditions.** In complex-sample simulation the gain
survives in some survey regimes and the intermediate guarantee fails in others,
and **the same $\bar D/A$ does not imply the same inference problem.**

---

## 2. The target, which is what separates this from the nearest work

Write $\theta_c$ for population $c$'s latent summary and $y_c$ for its survey
estimate. The literature divides sharply by which object the interval covers.

| work | target | sampling-variance uncertainty | deconvolution |
|---|---|---|---|
| **This paper** | **$\theta_{K+1}$ of a population never observed**, marginal over populations | carried into the band via a structure confidence set | **the object of study** |
| Zhang & Tuoto, [arXiv:2608.02766](https://arxiv.org/abs/2608.02766) (3 Aug 2026) |  expectations of the **in-sample** outcomes, conditional on the realised sample — verified from the abstract | **not estimated at all** for the split-CSI (verified, their §3.4) | none — an in-sample target does not require it |
| [Bersson & Hoff](https://arxiv.org/abs/2204.08122) | a **future observation within** an area | — | none |
| Fay–Herriot EBLUP with second-order EB intervals | $\theta_i$, in-sample, area-conditional, asymptotic | sampling variances assumed **known** | implicit in $\widehat A$, not analysed |
| Wang–Fuller (2003); Rivest–Vandal; You–Chapman; Maiti et al.; Sugasawa et al. | MSE of the **in-sample** area predictor | modelled, and the MSE corrected for it | not the object |
| Variance smoothing / GVF: Gao–Wakefield; Erciulescu et al.; Parker et al.; [McGovern–Fuglstad–Wakefield](https://arxiv.org/abs/2604.23029) | in-sample area estimates | smoothed, sometimes jointly modelled | not the object |
| [Acero–Molina–Marín](https://arxiv.org/abs/2403.15384) | in-sample area predictor | bootstrap MSE reflecting it | not the object |

**The target difference with Zhang & Tuoto is verified and it is the sharpest
contrast.** Their abstract states the aim as confidence intervals for "the
unknown expectations of the **in-sample** outcomes ... conditional on the
realised sample". Ours is a population never observed, marginal over
populations. The two are different inference problems and the manuscript will
present them as complementary.

> **Verification note — closed 2026-09-10.** The full text was retrieved
> (arXiv PDF, 19 pp.) and the sentence located. In §3.4 (Conclusion of the
> Italian permanent-census application): *"the split-CSI is easier to implement
> than the direct or EBLUP interval, because there is no need at all to estimate
> the sampling variances $\psi_i$."* Premises: it is said of the **split-CSI**
> specifically (a design-based split-sampling conformal construction), for
> **in-sample** area expectations, and it is a practical-implementation
> statement — the surrounding text notes that the FH model assumes the $\psi_i$
> known and that smoothing them biases the EBLUP interval. The earlier reading
> that "both variance components are absorbed into a shrinkage score" is **not**
> supported by any sentence in the paper and is withdrawn.
>
> Two further facts from the same section, both relevant to us: they state that
> for their application the exchangeability of $\{(y_i,x_i)\}$ **likely does not
> hold** (95 of the areas sampled with probability $<1$), and that the
> split-CSI's coverage remained valid on restricted reference sets; and their
> Table 6 shows the split-CSI half-width **growing with the design share** $w$
> (2.3\% to 4.6\%) while the direct interval's stays near 3.5\%. Not estimating
> the sampling variances is therefore not a free lunch in width — it is a
> different trade, made for a different target.

**And a difference in target is not by itself a demonstration of originality.**
It shows that paper does not subsume this one; it does not show this one adds
something.

**The gap must also be stated narrowly.** Prediction for an out-of-sample area is
standard through synthetic estimation (Rao & Molina 2015), and the linear
mixed-model literature does treat prediction intervals for a target containing a
new random effect — the parametric-bootstrap approximation to the EBLUP
prediction interval of [Chatterjee, Lahiri & Li](https://arxiv.org/abs/0806.2931)
is the reference point. **It is therefore false to say the literature offers no
interval for an out-of-sample latent target**, and the manuscript will not say
it. What those constructions do is Gaussian and model-based with the sampling
variances treated as known; what is not offered is an interval that carries the
uncertainty of an **estimated relative design-variance structure** into the
band. That is the narrow claim, and §7 tests it against exactly such a Gaussian
competitor rather than asserting it.

---

## 3. What is *not* claimed as new

Stated plainly so that a referee does not have to find it:

- Fisher information for a variance component, and the $\chi^2$/$F$ distribution
  theory that the pivots rest on. Classical.
- The conformal rank argument.
- Variance smoothing or generalised variance functions as an idea. A large and
  active literature.
- Taking a supremum of a band over a confidence set. A standard device.
- Any claim of superiority over methods that answer a different question,
  including the in-sample conformal interval above.
- **Robustness from the use of conformal prediction.** The exact ratio inference
  here rests on a normal--$\chi^2$ model, so "conformal, therefore
  distribution-free" is not available as an argument and will not be made. The
  rank step is finite-sample; the scale step is not model-free.

**The contribution is a result about the problem, and a construction that
exploits it.**

*The result* is the scale-sensitivity calculus of `docs/THEORY_scale_sensitivity.md`.
What separates interval constructions here is not how well they estimate the
scale — they can be given the same estimate — but **how hard the band reacts to
being wrong about it**. That reaction is an elasticity, and for a deconvolution
band it is $\rho^2/2$, damped by the design share, against exactly $1/2$ for any
band proportional to $\sqrt A$. From that follow, and are verified: the
population requirement being $\rho^{-4}$ smaller than a variance-component
criterion implies; the crossings between constructions across settings that were
first reported as separate surprises; and a formula for the width ratio of two
named constructions that was **pre-registered and tested on a fresh grid**,
reproducing the dependence on the error-budget split to six decimal places while
its constant needed a $1+1.9/K$ correction that the test located.

*The construction* of §17–§20 is then an instance built to exploit the damping,
with its uncertainty carried by a confidence set and a conservative computational
bound — not the contribution by itself.

**Why this matters for the objection a referee will raise.** Each ingredient —
variance smoothing, confidence sets, pivots, conformal ranks — is standard, and
against a component-wise construction given the same structure the assembled gain
is one to two percent. If the paper's claim were the assembly, that objection
would land. The claim is instead the calculus: it says *which* quantity's
uncertainty the interval is sensitive to, and predicts which construction is
narrowest for a given survey configuration without running it.

---

## 4. Where each claim's evidence sits, and what is still owed

| claim | established | owed |
|---|---|---|
| 1: the band depends on the scales only through a ratio, whose relative error is $\rho^2$ times that of the variance component | derived and verified; matches the repository's own band implementation | statement for coordinate-varying scales |
| 1: the requirement has two axes, $(K-1)^{-1}+\nu_{\mathrm{tot}}^{-1}$ | derived and verified | — |
| 1: plug-in estimation of the variance component is biased upward and does not average away | derived and verified | theoretical account of the $O(1/K)$ smoother bias |
| 2: exact pivot and one-sided limit under a known relative structure | proved; verified exactly | — |
| 2: closed-form confidence set for the structure parameter | proved; verified at nominal | — |
| 2: conservative computational bound for the supremum | proved for $a_c$; bounded for $\widehat d$ by convexity; verified with zero violations | — |
| 2: guarantee $\alpha_0+\eta_\gamma+\eta_t$ | proved **in the restricted normal model** | nothing under a complex design, and none is claimed |
| 3: gain and failure regimes | measured in finite-population complex-sample simulation | real-data analysis on the scalar target |

**The line between claim 2 and claim 3 is the one the manuscript must never
blur.** Claim 2's guarantee is a theorem about a restricted model. Claim 3 is a
set of simulation observations under designs where that model's conditions
demonstrably fail. A simulation cannot extend a theorem's scope, and high
observed coverage where an intermediate confidence event fails is empirical
conservatism, not a guarantee.

---

## 5. Scope, fixed

**The new procedure's target is a scalar population summary.** The manuscript
will not place the inherited full-CDF simultaneous band and the new scalar
result under one guarantee. The CDF work stands as the setting and the
motivation, with its own targets and its own assumption (S); the new theorem
covers a scalar functional and says so. The real-data analysis is chosen to
match the scalar target.

---

## 6. Completion criteria, and current status

| criterion | status |
|---|---|
| **Originality** — additional contribution over the nearest prior work | the scale-sensitivity calculus, pre-registered and tested; needs the comparison written into the manuscript at equation level |
| **Mathematical completeness** — guarantee for the implemented algorithm | done for the restricted model, including the computational bound |
| **Persuasive comparison** — same target and information | done against a structure-free construction and against a component-wise construction given the same structure; **owed**: a comparison against a method that shares the target |
| **Survey usefulness** — real-data analysis and stated limits | **owed** |

The two owed items are the manuscript's remaining work. Neither is a new method.
