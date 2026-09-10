# A scale-sensitivity calculus for latent-target survey prediction

Written 2026-09-10. This is the piece of the work that is a **result about the
problem** rather than a procedure, and it unifies a set of findings that were
reported as separate surprises across `exp13`, `exp14`, `exp16`, `exp17`, `exp23`
and `exp26`.

---

## 1. The object

Every construction here predicts an unobserved population's latent summary by
some half-width $R$ that depends on a scale nobody knows. Nobody evaluates $R$ at
the truth: each evaluates it at a bound. **What separates the constructions is
not how well they estimate the scale — they can be given the same estimate — but
how hard the band reacts to being wrong about it.**

Define the **scale elasticity**
$$e(\theta)=\frac{\partial\log R}{\partial\log\theta}.$$

For a latent scale $A$ and a design variance $L$ (so the design share is
$\rho^2=L/(A+L)$):

| construction | half-width | **elasticity in $A$** |
|---|---|---|
| deconvolution band | $q\sqrt{A/(A+L)}$ | $\dfrac{L}{2(A+L)}=\boxed{\rho^2/2}$ |
| any band $\propto\sqrt A$ (model-based) | $z\sqrt A$ | $\boxed{1/2}$ |
| uncorrected anchor | $q$ | $0$ |
| anchor $+$ sampling-error enlargement | $q+z\sqrt{L}$ | between the two |

The deconvolution band's elasticity is **damped by the design share**, and this
is the whole of what follows. It is not a property of conformal prediction; it is
a property of dividing by $\sqrt{A+L}$ and multiplying by $\sqrt A$.

---

## 2. The exchange identity

> **Proposition S1.** For the deconvolution band $R_c$ and any band
> $R_g\propto\sqrt A$, evaluated at a common upper bound $A_U\ge A$,
> $$\frac{R_c(A_U)/R_g(A_U)}{R_c(A)/R_g(A)}
> \;=\;\sqrt{\frac{A+L}{A_U+L}}\;=:\;\Lambda ,$$
> **exactly**, with no approximation.

*Proof.* $R_c(A_U)/R_c(A)=\sqrt{A_U(A+L)/\{A(A_U+L)\}}$ and
$R_g(A_U)/R_g(A)=\sqrt{A_U/A}$; divide. $\square$

Verified numerically: zero violations in 200,000 random $(A,L,A_U)$.

$\Lambda\to1$ as $L\to0$ — with no design noise there is nothing to deconvolve
and no advantage — and $\Lambda\to\sqrt{A/A_U}$ as $L/A\to\infty$. **So the
deconvolution form's advantage is bought entirely by design noise, and it is
largest exactly when the scale bound is loosest.**

### Corollary S2 — the requirement is $\rho^{-4}$ smaller than it looks

Certifying the variance component to relative precision $\tau$ and certifying the
band's own scale factor to the same precision differ by the elasticity ratio, and
the population requirement by its square: $\rho^{4}$. This is §13, where it was
found empirically and verified at 14–24 times at $\rho^2=0.2$.

### Corollary S3 — the ranking crosses, and where

Two forms with elasticities $e_1<e_2$ and oracle width ratio $r_0=R_1/R_2$ at the
truth realise $r_0\lambda^{e_1-e_2}$ at a bound loose by $\lambda=A_U/A$. They
cross at
$$\lambda^\star=r_0^{-1/(e_2-e_1)} .$$
Below $\lambda^\star$ the higher-elasticity form is narrower; above it the lower
one is. **Every reversal reported in this project is one crossing.** §13 (tight
limit, normal wins), §14 and §17 (loose pivot and low design share, conformal
wins by 11–20 percent), §23 and §26 (matched budget, conformal wins) are the same
statement at different $\lambda$ and $\rho^2$.

---

## 3. The sharp case: when the bound cancels

The comparison of `exp26` is not two forms at an arbitrary common bound. There
the Gaussian arm's bound is built from the conformal arm's own statistic:
$A_U=\bar S/\chi^2_{K,\alpha_2}$ with
$\bar S=\sum_cY_c^2/(1+\underline t)$, while the conformal band is
$\operatorname{ord}_m|Y_c|/\sqrt{1+\underline t}$.

> **Proposition S4.** In the scalar homoscedastic case, with
> $p=m/(K+1)$ and $z_p$ the $p$-quantile of $|N(0,1)|$,
> $$\frac{R_{\text{conformal}}}{R_{\text{gaussian}}}\;\approx\;
> \frac{z_p}{z_{1-\alpha_1/2}}\sqrt{\frac{\chi^2_{K,\alpha_2}}{K}} .$$
> **The certified bound $\underline t$ cancels, and so do $A$, $L$, $\rho$ and
> $\nu$: the ratio depends only on $K$ and the split of the error budget.**

*Sketch.* $\operatorname{ord}_m|Y_c|\approx\sqrt{A+L}\,z_p$ and
$\bar S\approx K(A+L)/(1+\underline t)$; the factors $\sqrt{A+L}$ and
$(1+\underline t)^{-1/2}$ appear in both and divide out. $\square$

**Tested against `exp26` with no free parameters**: predicted 0.757 at $K=60$ and
0.854 at $K=200$ against observed 0.778–0.784 and 0.860–0.864 — errors of 0.8 to
3.6 percent. And the prediction that the ratio is **invariant** in $\rho$, $\nu$
and structure misspecification is what `exp26` shows: the observed ratio moves by
0.6 percent across all of them within each $K$.

That invariance was reported in `exp26` as an unexplained regularity. It is a
consequence of S4.

---

## 4. What this is, and what it is not

**It is** a statement about the problem: which interval form is narrowest for a
given survey configuration is decided by the design share and by how loose the
achievable scale bound is, both of which are known before any interval is
computed. It gives a practitioner a reason to choose a construction that does not
depend on trusting a simulation, and it explains why the same two constructions
change places between settings.

**It is not** an optimality theorem. Nothing here says the deconvolution band is
the best possible; it says how two named forms trade off, and the trade-off is
exact for that pair. Extending it to a class would require defining the class.

**It is not** a property of conformal prediction. The rank step contributes only
$z_p$ in S4. A parametric band built on $\sqrt{A/(A+L)}$ would inherit the same
elasticity, and saying otherwise would be the "conformal is robust" claim already
disclaimed in `docs/CONTRIBUTION.md`.

**And S4 is asymptotic in $K$ and exact only in the scalar homoscedastic case.**
S1 is exact; S4 uses $\operatorname{ord}_m|Y|\approx\sqrt{A+L}z_p$ and
$\bar S\approx K(A+L)/(1+\underline t)$, which is where its 1–4 percent error
comes from.

---

## 5. Why this changes the paper's contribution claim

`docs/CONTRIBUTION.md` currently rests the paper on connecting known tools. The
weakness a referee will press is that each tool is standard and the assembled
gain over a component-wise method with the same information is one to two
percent.

**This section is the answer.** The contribution is not the assembly: it is
identifying *which quantity's uncertainty the interval is actually sensitive to*,
showing that sensitivity is damped by the design share, and deriving from that a
prediction — verified without free parameters — of which construction is
narrowest and by how much. The procedure of §17–§20 is then an instance built to
exploit the damping, rather than the contribution itself.

`exp29` tests S4 as a **pre-registered prediction on a fresh grid** rather than a
retrodiction, which is what the claim needs.

---

## 6. The pre-registered test, and what it refuted

`exp29`, protocol `docs/PROTOCOL_exp29_scale_law.md`, whose predicted numbers
were computed and written down before the experiment ran. Fresh grid:
$K\in\{40,120,400\}$, $\rho^2\in\{0.20,0.45,0.70\}$, $\nu\in\{6,20\}$,
$\sigma_{\mathrm{mis}}\in\{0,0.5\}$ — none of these values appears in `exp26`.
10,000 replicates.

### P-C passes decisively, and it is the sharpest test

Varying the budget split at $K=120$ with $\alpha_1+\alpha_2=0.05$:

| $\alpha_1$ | 0.005 | 0.010 | 0.020 | 0.025 | 0.035 | 0.045 |
|---|---|---|---|---|---|---|
| predicted | 0.6225 | 0.6758 | 0.7414 | 0.7653 | 0.8015 | 0.8188 |
| observed | 0.6304 | 0.6844 | 0.7509 | 0.7750 | 0.8118 | 0.8292 |
| error | **1.2774%** | **1.2774%** | **1.2774%** | **1.2774%** | **1.2774%** | **1.2774%** |

**The error is identical to six decimal places across all six splits.** The
law's dependence on $(\alpha_1,\alpha_2)$ — a factor of 1.32 between the extreme
splits — is reproduced exactly. Monotone as predicted, no crossing, as predicted.

### P-A fails as registered, and the failure is located

Registered tolerance 5 percent; the worst cell is **7.07 percent**
($K=40$, $\rho^2=0.70$, misspecified). P-A **fails**.

The failure is a single multiplicative constant per $K$, which is what P-C
already implied:

| $K$ | observed / predicted | $(c-1)K$ |
|---|---|---|
| 40 | 1.0496 | 1.98 |
| 120 | 1.0171 | 2.06 |
| 400 | 1.0066 | 2.66 |

Fitting $(c-1)$ on $1/K$ across the 36 cells gives a slope of **1.92**, so

> **Refined S4.**
> $$\frac{R_{\text{conformal}}}{R_{\text{gaussian}}}
> =\frac{z_p}{z_{1-\alpha_1/2}}\sqrt{\frac{\chi^2_{K,\alpha_2}}{K}}
> \Big(1+\frac{\approx1.9}{K}\Big)+O(K^{-2}).$$

Maximum error falls from 7.07 to **2.17 percent**, mean $+0.15$ percent.

**The source is identified**: S4 replaces $E[\operatorname{ord}_m|Y_c|]$ by the
$p$-quantile of $|N(0,1)|$, and the gap between an order statistic's expectation
and the corresponding quantile is $O(1/K)$. The constant is fitted here, not
derived; the standard order-statistic expansion would supply it and that is
recorded as owed rather than claimed.

### P-B holds asymptotically, not exactly

Within-$K$ spread of the observed ratio, against a registered tolerance of 0.02:

| $K$ | 40 | 120 | 400 |
|---|---|---|---|
| spread | **0.0200** | 0.0110 | 0.0089 |

At the tolerance boundary at $K=40$ and inside it above. But the residual is
**systematic in the design share**, not noise: mean ratio 0.7171, 0.7194, 0.7270
at $\rho^2=0.20,0.45,0.70$ for $K=40$, and 0.8180, 0.8193, 0.8217 at $K=400$.

So the invariance claimed in S4 is **asymptotic**: a residual dependence on
$\rho^2$ of about 1.4 percent at $K=40$, 0.7 at $K=120$ and 0.45 at $K=400$
survives. **The strong form of the claim — that the ratio does not depend on the
design share at all — is refuted**; what stands is that the dependence is an
order of magnitude smaller than one would expect of a quantity built entirely out
of design variances, and vanishing in $K$.

### What the test leaves standing

| claim | status |
|---|---|
| S1, the exchange identity | exact; 0 violations in 200,000 cases |
| the elasticity table | algebra |
| S4's dependence on the budget split | **exact** (P-C, to six decimals) |
| S4's constant | **wrong by $1+1.9/K$**; refined form errs by $\le2.2$ percent |
| S4's invariance in $\rho^2$, $\nu$ | **asymptotic, not exact**; residual 1.4 percent at $K=40$ falling to 0.45 at $K=400$ |

This is protocol outcome 3: the structure is right, the constant was not, and the
error is located rather than absorbed. **A law stated in advance, tested on a
fresh grid, and refuted in one of its three registered predictions is a stronger
object than one fitted to the data that produced it** — and the refined form is
now itself a prediction, untested on new conditions.
