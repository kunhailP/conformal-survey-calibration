# Design specification — bounding the correction ratio directly

Written 2026-09-10. Step 2 of the fixed plan. Supersedes the design sketch in
the previous report, which contained an error identified in review and corrected
in §0.

---

## 0. The error being corrected

The sketch said that under heteroscedasticity the ratios
$r_c=D_c/A$ are determined by $A$ together with the observed $\widehat D_c$, so
the confidence set could be built on a single axis. **That is false in a general
heteroscedastic model.** $\widehat D_c/A$ is a plug-in, not the parameter:
observing $\widehat D\approx(1,1)$ leaves $\mathbf D=(1,1)$ and
$\mathbf D=(0.5,2)$ both compatible with the data. Fixing $\widehat D_c$ and
moving only $A$ excludes most of the admissible ratio vectors, and reintroduces
the exact fault the whole construction exists to avoid — **treating the design
variance estimate as the design variance.**

Three things must stay distinct in everything below:

| construction | what it means |
|---|---|
| $D_c=d\,a_c$ with $a_c$ **known** | genuinely a low-dimensional model |
| general $D_c$, profiled or jointly inferred | nuisance uncertainty retained while computing |
| $D_c$ set to $\widehat D_c$ | uncertainty removed by substitution |

The third is not joint inference and will not be called that.

---

## 1. The restricted model, exactly

> **Model R.** Independently across $c=1,\dots,K$, with $\mu$ known and
> subtracted,
> $$Y_c\sim N(0,\;A+d\,a_c),\qquad
> \frac{\nu_c\widehat D_c}{d\,a_c}\sim\chi^2_{\nu_c},\qquad Y\perp\widehat D,$$
> where $a_c>0$ is a **known** relative variance structure, $d>0$ an unknown
> common scale, and $A>0$ the between-population variance.

**$a_c$ must be known from the design, not built from the same $\widehat D_c$.**
A relative structure fitted to the observed variance estimates and then declared
known is the plug-in fault in another costume. Admissible sources: sampling
fractions, PSU counts, published design effects — quantities fixed before the
survey estimates are seen.

Write $t=d/A$, so $r_c=D_c/A=a_c t$: **one unknown ratio parameter**.

### The pivot

With $\nu=\sum_c\nu_c$ and
$$\widehat d=\frac1\nu\sum_c\frac{\nu_c\widehat D_c}{a_c},
\qquad S(t)=\sum_c\frac{Y_c^2}{1+t\,a_c},$$
we have $\nu\widehat d/d\sim\chi^2_\nu$ and, at the true $t$,
$S(t)/A\sim\chi^2_K$, independently. Therefore
$$\boxed{\;T(t)=\frac{K\,\widehat d}{t\,S(t)}\ \sim\ F_{\nu,K}\;}$$
**exactly**, with no approximation and no multiplicity correction.

### Monotonicity, and the inversion

$$\frac{\partial}{\partial t}\big[t\,S(t)\big]=\sum_c\frac{Y_c^2}{(1+t\,a_c)^2}>0,$$
so $t\,S(t)$ is strictly increasing and $T(t)$ strictly decreasing in $t$. With
$q=F_{1-\eta;\,\nu,K}$, the set $\{t:T(t)\le q\}$ is a half-line $[t_L,\infty)$
and
$$\Pr\{t\ge t_L\}=\Pr\{T(t)\le q\}=1-\eta .$$
$t_L$ is an **exact one-sided lower confidence bound**, obtained by one
monotone root-find.

### The half-width bound

The oracle half-width is a function of $t$ alone:
$$R(t)=\operatorname{ord}_m\Big\{|Y_c|\big/\sqrt{1+a_c t}\Big\},$$
strictly decreasing in $t$, so $t\ge t_L$ gives $R(t)\le R(t_L)$ and
$$\Pr\{\theta_{K+1}\in B(t_L)\}\ \ge\ 1-\alpha_0-\eta$$
by the same union of the rank event and $\{t\ge t_L\}$ used throughout.

**One parameter, one budget, one bound.** The separate-bounds construction spends
$\eta_1$ on an upper limit for $A$ and $\eta_2$ on $K$ simultaneous lower limits
for the $D_c$, and both bounds push the correction toward zero; here the same
total $\eta$ buys a single limit on the only quantity the band depends on.

### Boundary handling, stated rather than left to the code

- $T(t)\to\infty$ as $t\downarrow0$ and $T(t)\to K\widehat d\big/\sum_cY_c^2/a_c$
  as $t\to\infty$. If that limit exceeds $q$, $\{T\le q\}$ is **empty**: no $t$
  is compatible at this level. The rule is to report $R_U=\infty$, an
  uninformative band, matching `dac.bands.conformal_quantile`'s treatment of a
  rank that does not exist. The rate is recorded per cell. This event is
  contained in the $\eta$-probability failure event, so it costs nothing in the
  guarantee.
- If $m>K$ the conformal radius is infinite, as elsewhere.
- $\widehat D_c=0$ makes $\widehat d$ smaller and $t_L$ smaller, hence the band
  wider. Conservative, and recorded.

### What this step is and is not

It is an exact reference case in which the ratio idea can be verified — the
heteroscedastic model in which one-axis reduction is genuinely true, not assumed.
**It is not by itself a novel contribution or a survey-ready method**, and it
does not establish anything about a general $\mathbf D$.

---

## 2. What the comparison must establish, in order

1. the realised confidence level of $t_L$ against $1-\eta$;
2. containment of the oracle half-width, $\Pr\{R(t_L)\ge R(t)\}$;
3. **only then** width, against the separate-bounds construction at the same
   total budget, with realised coverage printed beside it.

A narrower band from a construction whose level is wrong is not an improvement.

---

## 3. The general heteroscedastic extension — specification, not yet a result

The target stays
$$R_U=\sup_{(A,\mathbf D)\in\mathcal C}R(A,\mathbf D),$$
and the design question is what $\mathcal C$ is. Three routes, with what each owes:

**(a) Profile the nuisance.** Invert a test of $H_0:R=r$ profiling over
$(A,\mathbf D)$ subject to $R(A,\mathbf D)=r$. Retains the nuisance uncertainty
rather than substituting it. **Owes:** a null distribution for the profiled
statistic — exact if one exists, otherwise an asymptotic regime in which $K$ and
the $\nu_c$ both grow, stated explicitly.

**(b) A structured $\mathcal C$ from a working variance model.** Impose
$D_c=d\,a_c(\gamma)$ with $\gamma$ estimated, and carry the uncertainty in
$\gamma$ into $\mathcal C$. This is Model R with the relative structure no longer
known. **Owes:** the level under a misspecified $a_c(\gamma)$, which is the
question `exp13` §T5 already showed matters — GVF misfit gave back most of the
gain there.

**(c) Design-preserving joint resampling.** Resample so that the survey
estimate, the design variance, the mean model and the correction factor are all
recomputed together, preserving their dependence. **Owes, before any
implementation:** what is resampled, at what level of the design, and in what
asymptotic regime it is justified. `exp14`–`exp16` are the standing warning —
a bootstrap that refits the whole procedure covered at 0.901, and the *form* of
the limit mattered more than anything else. **Resampling is not a validity
argument.**

The order is (a) or (b) first, since each can be checked in the closed model
against the exact Model R answer, and (c) last.

---

## 4. Success criterion for this line

Not another formula. **Does bounding the ratio directly reduce conservatism
under correct error control, and does the gain survive beyond a known variance
structure?** If the answer to the first is no, the line stops at Model R as a
negative result about the separate-bounds construction. If the first is yes and
the second no, the paper's scope is a stated variance structure, and that
condition must be reported as prominently as the gain.
