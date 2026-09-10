# Theory memo — certifying the right quantity

Written 2026-09-10, after `exp09`. Responds to development-plan items (1), (2),
(3) and (6). Verification: `experiments/exp10_certification.py`, protocol
`docs/PROTOCOL_exp10_certification.md`, results
`results/exp10_certification.csv`.

The plan asks: define the paper's success mathematically, build a
confidence-interval certification with an error budget, and connect it to a
prediction band. This memo does all three, and in doing so **disagrees with the
plan on which quantity to certify.** That disagreement is the memo's main
content, because it changes the manuscript's central number by a factor
$\rho^{-4}$.

---

## 1. The plan proposes certifying the latent scale. It should not.

The plan's target is $s=\sqrt A$, with success defined as
$\Pr_\theta(\text{certify}\cap|\widehat s/s-1|>\varepsilon)\le\eta$. The error
statement is exactly right and the choice of $s$ is not.

Work out what the band actually depends on. In the equal-design-variance case
$v_c^2\equiv v^2$, the calibration scores of Section 3 are
$M_c=\max_j|Y_c(j)|/\widehat s_Y(j)$ — they involve $\widehat s_Y$ and **not**
$\widehat s_G$ — and the band placed on the latent scale has half-width
$M_{(m)}\widehat s_G(j)$.

> **Proposition A.** With $d=1$, the estimated-scale band is
> $$\widehat B=\Big[-\,|Y|_{(m)}\,\widehat\kappa,\ \ |Y|_{(m)}\,\widehat\kappa\Big],
> \qquad \widehat\kappa:=\frac{\widehat s_G}{\widehat s_Y}=\sqrt{1-\widehat\rho^2},$$
> and the oracle band is the same with $\kappa$ in place of $\widehat\kappa$.
> Coverage and width therefore depend on the estimated scales only through the
> **ratio** $\widehat\kappa$. The band does not stop depending on
> $\widehat s_G$; it depends on it only in that ratio, which is a different and
> weaker requirement.

*Proof.* $M_c=|Y_c|/\widehat s_Y$ so $M_{(m)}=|Y|_{(m)}/\widehat s_Y$, and the
half-width is $M_{(m)}\widehat s_G=|Y|_{(m)}\widehat s_G/\widehat s_Y$. $\square$

For $d>1$ the half-width is $M_{(m)}\widehat s_Y(j)\widehat\kappa(j)$, and a
*common* multiplicative error in $\widehat s_Y$ cancels exactly between
$M_{(m)}$ and the width. What does not cancel is an error in the **shape** of
$\widehat s_Y$ across coordinates, which is a separate problem from the one
this memo treats and should not be folded into it.

The consequence is that $\widehat s_G$ is the wrong certification target: it is
the numerator of the quantity that matters, and its error is partly cancelled
by the denominator because both are built from the same $S_Y^2$.

> **Proposition B.** Writing $\sigma_T^2=\mathrm{Var}(\widehat T)=2T^2/(K-1)$
> and $\sigma_D^2=\mathrm{Var}(\widehat D)$, to first order
> $$\frac{\mathrm{RSE}(\widehat\kappa)}{\mathrm{RSE}(\widehat s_G)}
> =\sqrt{\frac{\rho^4\sigma_T^2+\sigma_D^2}{\sigma_T^2+\sigma_D^2}}
> \ \longrightarrow\ \rho^2\quad\text{as }\sigma_D^2/\sigma_T^2\to0 .$$

*Proof.* $\log\widehat\kappa=\tfrac12(\log\widehat A-\log\widehat T)$ with
$\widehat A=\widehat T-\widehat D$, so
$\mathrm{Var}(\log\widehat\kappa)=\tfrac14[\sigma_T^2D^2/(A^2T^2)+\sigma_D^2/A^2]$,
while $\mathrm{Var}(\log\widehat s_G)=\tfrac14[\sigma_T^2+\sigma_D^2]/A^2$.
Divide, and use $D/T=\rho^2$. $\square$

The cancellation is not an approximation trick: it is the same $S_Y^2$ appearing
in both places. And it is worth exactly $\rho^4$ in the population requirement.

> **Corollary (the boundary, restated on the right quantity).** With
> $\sigma_D^2=2D^2/\nu_{\mathrm{tot}}$, the requirement
> $\mathrm{RSE}(\widehat\kappa)\le\varepsilon$ is
> $$\boxed{\ \frac{1}{K-1}+\frac{1}{\nu_{\mathrm{tot}}}
> \ \le\ \frac{2\varepsilon^2(1-\rho^2)^2}{\rho^4}\ }$$
> against the manuscript's $K\ge2/[\tau^2(1-\rho^2)^2]$ at $\tau=2\varepsilon$.
> The requirement on populations falls by the factor $\rho^4$.

Two things follow, and both matter more than the algebra.

**The boundary has two axes, not one.** Populations and design degrees of
freedom enter harmonically: $K_{\mathrm{eff}}^{-1}=(K-1)^{-1}+\nu_{\mathrm{tot}}^{-1}$.
Neither substitutes for the other, and $\nu_{\mathrm{tot}}$ imposes a floor no
number of populations can clear. `exp09` §5 already showed $\nu$ cannot be
bought with computation; this says what it costs when you cannot.

**The requirement on populations falls by $\rho^{-4}$ — on a matched relative
standard error criterion, and only there.** §7 recomputes this properly and
corrects an overstatement made when this memo was first written. The
manuscript's 291 populations at $\rho=0.66$ is an RSE criterion; the same
criterion on $\kappa$ gives 58 to 70. But a *certified* guarantee at the same
tolerance is a high-probability statement, not an RSE, and costs a further
factor of about $z_{1-\eta/2}^2\approx3.8$. The honest comparison is in §7 and
the gain at $\rho=0.66$ is a factor of 1.1 to 1.3, not 5.

---

## 2. The certification interval: exact, not a union bound

The plan builds separate $\chi^2$ intervals for $T$ and $D$, splits $\eta$
between them, and takes $A\in[\max(0,T_L-D_U),\,T_U-D_L]$. That is valid and it
is doubly wasteful: it pays a union bound, and it pays it on the wrong target.
It is also not the standard interval — a difference of variance components from
independent mean squares is the subject of a literature
(Graybill–Wang 1980; Ting et al. 1990; Burdick & Graybill 1992), and a referee
will ask why the modified large-sample interval was not used.

For $\kappa$ no approximation is needed at all.

> **Proposition C.** Under the model of plan §2, with $\widehat D$ independent
> of $S_Y^2$,
> $$\frac{\widehat D/S_Y^2}{\rho^2}\ \sim\ F_{\nu_{\mathrm{tot}},\,K-1},$$
> so $[\rho^2_L,\rho^2_U]=[R/F_{1-\eta/2},\ R/F_{\eta/2}]$ with
> $R=\widehat D/S_Y^2$ is an **exact** $1-\eta$ interval for $\rho^2$, and
> $[L,U]=[\sqrt{1-\rho^2_U},\ \sqrt{1-\rho^2_L}]$ is an exact interval for
> $\kappa$.

*Proof.* $\nu_{\mathrm{tot}}\widehat D/D$ and $(K-1)S_Y^2/T$ are independent
$\chi^2$, so their scaled ratio is $F$; $\rho^2=D/T$; monotone transformation.
$\square$

The pivot exists because $\kappa$ is a *ratio* of the two variance components,
which is what made it the right target in §1. Certifying the difference $A$
forfeits it.

> **Proposition D (certification).** Let $\widehat\kappa_\star=2LU/(L+U)$ and
> $r_\star=(U-L)/(U+L)$; certify iff $L>0$ and $r_\star\le\varepsilon$. Then
> $$\Pr_\theta\big(\text{certify}\cap|\widehat\kappa_\star/\kappa-1|>\varepsilon\big)\le\eta .$$

*Proof.* On $\{\kappa\in[L,U]\}$, $\widehat\kappa_\star$ is the minimax point of
$[L,U]$ so $|\widehat\kappa_\star/\kappa-1|\le r_\star$; if additionally
$r_\star\le\varepsilon$ the bad event is empty. So the bad event is contained in
$\{\kappa\notin[L,U]\}$, of probability at most $\eta$. $\square$

The plan's own caution applies and should be printed: this controls the
*joint* event over repeated samples, not the error rate conditional on having
certified. §5 shows the two differ substantially, and the paper must not blur
them.

**The point estimate is part of the guarantee.** Proposition D holds for
$\widehat\kappa_\star$ and not for the plug-in $\widehat\kappa$: §5 measures
false certification at 0.003 for the former and 0.045 for the latter, at
$\eta=0.05$. Reporting the certified interval while shipping the plug-in point
estimate breaks the theorem.

---

## 3. The band: a closed-form union, and certification becomes optional

The plan's §6 constructs $B_{\mathrm{safe}}=\bigcup_{\vartheta\in\mathcal C}B_\vartheta$
and warns, correctly, that a grid maximum is not a union. Here no grid is
needed.

> **Proposition E.** The half-width $|Y|_{(m)}\vartheta$ is increasing in
> $\vartheta$, so $\bigcup_{\vartheta\in[L,U]}B_\vartheta=B_U$, and
> $$\Pr\{F_{K+1}\notin B_U\}\ \le\ \alpha_0+\eta ,$$
> at width $U/\kappa$ times the oracle band.

*Proof.* Monotone nesting gives the union. On $\{\kappa\in[L,U]\}$,
$B_\kappa\subseteq B_U$, and $\Pr\{F_{K+1}\notin B_\kappa\}\le\alpha_0$ by the
oracle argument of Section 3. Union the two failure events. $\square$

This is the reframing the paper needs, and it is larger than the algebra.

> **Certification is not a gate. It is a report.** The safe band is available
> at every $(K,\nu,\rho)$, valid at $\alpha_0+\eta$, with no threshold to pass.
> What certification adds is the statement that the honest widening is small.
> A procedure that refuses to act when it cannot certify is throwing away a
> valid band.

That replaces the manuscript's current prescription — clear the gate or fall
back to the anchor — with: always widen to $U$, and report $U/\kappa$ as the
price of not knowing the scale.

---

## 4. What this memo assumes

**Homoscedasticity, and a correction about what is implemented.** Propositions
A and C are exact only for $v_c^2\equiv v^2$. An earlier version of this memo
said the coordinate-varying case was implemented nowhere; that was read off
`src/dac/bands.py` alone and is **wrong**. `experiments/exp07_widths.py` already
standardises coordinate by coordinate: `s_plug` and `sT` are per-coordinate
vectors, the scores are $\max_j|Y_c(j)|/\widehat s_Y(j)$, and the reported
radius is $q\cdot\overline{sT}$ — the **mean half-width** across coordinates, not
a common radius. So the accurate statement is: the closed-model experiments use
a scalar scale, the ESS analysis uses per-coordinate standardisation and a
per-coordinate correction scale, and **the theory connecting the two paths does
not yet exist.** Concretely, the safe band at $d>1$ needs
$\kappa_U(j)\ge\kappa(j)$ *simultaneously* over coordinates, which is a
simultaneous band on $\kappa(\cdot)$ and carries a multiplicity cost that
Proposition E does not pay. That cost is unmeasured.
The ESS configurations are heteroscedastic and $\overline{v^2}$ is an average.
Proposition B survives with $\sigma_D^2=\mathrm{Var}(\overline{\widehat v^2})$;
Proposition C does not, and needs either a Satterthwaite $\nu_{\mathrm{tot}}$ or
a different pivot. **This is the gap between the memo and the application, and
it is the first thing to close.**

**$\widehat D\perp S_Y^2$.** Same limitation as `exp09` §7.1: false for a CDF
ordinate. Unresolved.

**Independence across populations.** Plan item (3), untouched here. The
country–region block structure would enter through the effective $K-1$ in the
$\chi^2$ for $S_Y^2$, which is where the plan's centring matrix $H_c$ does its
damage: country-centred deviations lose one contrast per country, so
$K-1\rightsquigarrow K-n_{\text{countries}}$ before any correlation is
accounted for. That is a first-order bound worth stating precisely, and it is
small — 236 regions in 30 countries gives 206, not 235.

**Assumption (S).** Orthogonal to all of the above and untouched. A certified
$\kappa$ says nothing about whether the standardised shapes share a law.
Section 5 of the manuscript stands as it is.

---

## 5. Verification

`exp10`: 54 cells, $K\in\{30,100,300\}$, $D/A\in\{0.25,1,4\}$
($\rho\in\{0.447,0.707,0.894\}$), $\nu\in\{4,12,40\}$ as a single pooled
estimate and as per-population degrees of freedom, 20,000 replicates,
$\varepsilon=0.10$, $\eta=0.05$, $\alpha_0=0.05$.

**Q1 — the frozen gate is not an error-controlled rule, and the population
floor is worse.** Maximum false-certification rate over cells, against a budget
of 0.05:

| rule | single estimate | per-population df |
|---|---|---|
| $K\ge94$ | **0.945** | **0.750** |
| plug-in diagnostic at $\tau=0.147$ | **0.466** | 0.005 |
| plug-in diagnostic at $\tau=2\varepsilon$ | **0.466** | 0.005 |
| union-bound interval on $s$ | 0.017 | 0.000 |
| Graybill–Wang interval on $s$ | 0.017 | 0.000 |
| exact interval on $\kappa$ | 0.045 | 0.049 |

At $K=300$, $\rho=0.707$, $\nu=4$ the frozen gate certifies on 53 percent of
replicates and is wrong on 47 of those 53. The population floor certifies
always and is wrong up to 94 percent of the time. Neither is a rule with an
error rate.

**Q2 — the plan's interval is valid and abstains almost always.** Realised
coverage of the union-bound interval is 0.970 to 0.994 against a nominal 0.95;
Graybill–Wang is 0.947 to 0.961; the $F$ interval on $\kappa$ is 0.946 to 0.952,
i.e. exact. Certification rates at $K=300$, $\nu=40$, per-population df:

| $\rho$ | union bound | Graybill–Wang | exact on $\kappa$ |
|---|---|---|---|
| 0.447 | 0.065 | 0.475 | **1.000** |
| 0.707 | 0.000 | 0.000 | **0.856** |
| 0.894 | 0.000 | 0.000 | 0.000 |

The gap decomposes: union bound against Graybill–Wang isolates the cost of the
union (a factor of about seven), Graybill–Wang against the $F$ interval isolates
the cost of the wrong target (the rest, and at $\rho=0.707$ it is the whole
difference between never and usually).

**Q3 — the exact rule holds the budget and is useful over a real range.**
Never above $\eta$; certification rates of 0.73 to 1.00 at $\rho=0.447$ and 0.68
to 0.86 at $\rho=0.707$, $K\ge300$. At $\rho=0.894$ it certifies essentially
never, and that is correct rather than a failure: the requirement at
$\varepsilon=0.10$ is not met at any $K$ in the grid.

**Q4 — the $\rho^4$ prediction holds for the RSE, which is not the same as a
gain in the certification requirement; see §7.** Ratio of realised relative SDs and the
implied gain in required populations, per-population df:

| $\rho^2$ | $\mathrm{RSE}(\widehat\kappa)/\mathrm{RSE}(\widehat s_G)$ | predicted $\rho^2$ | gain in required $K$ | predicted $\rho^{-4}$ |
|---|---|---|---|---|
| 0.2 | 0.206–0.265 | 0.2 | **14–24** | 25 |
| 0.5 | 0.516–0.710 | 0.5 | **2.0–3.8** | 4 |
| 0.8 | 0.852–0.904 | 0.8 | 1.22–1.38 | 1.56 |

The attenuation at small $K$ and at $\rho^2=0.8$ is the $\sigma_D^2$ term of
Proposition B, and it is in the predicted direction. With a single pooled
estimate on few degrees of freedom the gain disappears entirely, as Proposition
B says it must.

**Q5 — the safe band covers, and it is still much narrower than the anchor.**
Per-population df, target $1-\alpha_0-\eta=0.90$:

| $K$ | $\rho$ | oracle cov. | plug-in cov. | **safe cov.** | safe/oracle width | **safe/anchor width** |
|---|---|---|---|---|---|---|
| 30 | 0.447 | 0.965 | 0.959 | 0.971 | 1.050 | 0.939 |
| 30 | 0.707 | 0.965 | 0.921 | 0.981 | 1.186 | 0.839 |
| 30 | 0.894 | 0.965 | **0.704** | 0.986 | 1.611 | 0.720 |
| 300 | 0.707 | 0.949 | 0.945 | 0.964 | 1.074 | 0.759 |
| 300 | 0.894 | 0.950 | **0.918** | 0.983 | 1.264 | 0.565 |

The plug-in band undercovers by up to 25 percentage points. The safe band never
falls below 0.951. Its width penalty over the infeasible oracle is 2 to 61
percent and shrinks in $K$ — **and even at its worst it is 28 percent narrower
than the uncorrected anchor radius.** The comparison to the anchor is across
targets and is reported as secondary; the same-target comparison is the first
three columns, where the safe band is the only valid construction of the three.

**Outcome, against the protocol.** Outcome 1: Q3 and Q4 hold. The certification
target changes to $\kappa$, the boundary is restated on two axes, and the
population requirement falls by $\rho^4$ in the closed model. What is not yet
established is that any of this survives heteroscedastic designs and dependent
populations, which §4 lists and §6 schedules.

---

## 6. What would establish the claim on the application

Not more simulation. Three specific things, in order.

1. **Recompute the manuscript's regional configurations on $\kappa$.** `exp03`
   and `exp07` hold everything needed; the question is whether the $\rho^4$
   reduction in the requirement is realised at the actual heteroscedastic
   $\widehat v^2(j)$ profiles. If it is, the count of configurations where the
   correction is reachable changes, and that is the paper's new headline.
2. **A pivot, or an honest Satterthwaite, for the heteroscedastic case.**
   Proposition C is the memo's cleanest result and the one least likely to
   survive contact with a real design. Establishing what replaces it is the
   main remaining theoretical task.
3. **The block structure**, entering as the effective degrees of freedom of
   $S_Y^2$. The centring bound $K-n_{\text{countries}}$ is a first-order
   statement available now; the covariance correction is plan item (3).

Only after (1) is the manuscript's central number known to change. Everything
above is a statement about a model.

---

## 7. Correction after review: the requirement, on matched criteria

The first version of this memo reported the population requirement at
$\rho=0.66$ falling from 291 to about 55. **That comparison mixed two
criteria and the improvement it claims is not available.** The correction is
recorded here rather than silently applied.

The manuscript's 291 comes from a *relative standard error* criterion on the
**variance**, $\mathrm{RSE}(\widehat A)\le\tau$ — the diagnostic of eq. (14) is
$\mathrm{SE}(\widehat s_G^2)/\widehat s_G^2$, not a statement about
$\widehat s_G$. The $\kappa$ column is therefore computed at $\varepsilon=\tau/2$,
the delta-method equivalent on a standard deviation, so the two columns are on
the same footing. Earlier drafts of this table labelled the first column "RSE on
$s_G$", which named the wrong quantity even though the number was right. The certification of §2 is a *high
probability* statement, $\Pr(\text{certify}\cap|\cdot|>\varepsilon)\le\eta$.
For an approximately log-symmetric interval the certification condition is
$r_\star=\tanh(z_{1-\eta/2}\sigma)\le\varepsilon$, so it demands
$\sigma\lesssim\varepsilon/z_{1-\eta/2}$ where the RSE criterion demands
$\sigma\le\varepsilon$. The requirement on populations is therefore about
$z_{1-\eta/2}^2\approx3.84$ times larger for the same $\varepsilon$. Three
separate mismatches, all noted in review, are folded into this: variance versus
standard deviation (handled by $\tau=2\varepsilon$), RSE versus high-probability
guarantee (the factor above), and finite versus infinite $\nu$.

Required populations at $\tau=0.147$, i.e. $\varepsilon=0.0735$ on a standard
deviation, $\eta=0.05$, with $\nu$ degrees of freedom per population pooled
over the $K$ of them. `K_cert` is the count at which the exact rule of
Proposition D certifies with probability one half, and in brackets four fifths.

| $\rho$ | $\nu$/pop. | RSE on $A$ at $\tau$ (manuscript) | RSE on $\kappa$ at $\tau/2$ | **certify on $\kappa$** | gain on RSE | **gain vs. manuscript** |
|---|---|---|---|---|---|---|
| 0.47 | 4 | 153 | 10 | **41** (63) | 15.1 | **3.7** |
| 0.47 | 40 | 153 | 9 | **33** (51) | 17.7 | **4.6** |
| 0.60 | 4 | 226 | 37 | **149** (201) | 6.0 | **1.5** |
| 0.60 | 40 | 226 | 31 | **122** (164) | 7.3 | **1.9** |
| 0.66 | 4 | 291 | 70 | **276** (357) | 4.2 | **1.1** |
| 0.66 | 40 | 291 | 58 | **226** (292) | 5.1 | **1.3** |

**What survives.** The $\rho^{-4}$ mechanism is real and the RSE column
confirms it against $\rho^{-4}=20.5,\ 7.7,\ 5.3$. So does the two-axis
structure.

**What does not.** The claim that this makes the ESS regional configurations
reachable. At $\rho=0.66$ a certified guarantee needs 226 to 276 populations
for a coin-flip chance and 292 to 357 for four chances in five, against the
manuscript's 291 and against regional counts of 100 to 290. **At the operating
point that matters most the certification requirement is barely below the
manuscript's own, and above it if one wants to certify reliably.** The gain is
real only at lower design shares — a factor of 3.7 to 4.6 at the need cutoff
$\rho=0.47$.

### Why this does not sink the result

Because the deliverable should not be certification. §3 already argued it:
$B_U$ is valid at $\alpha_0+\eta$ whether or not $r_\star\le\varepsilon$. The
certification requirement being high is a statement about how often one can
*announce* a small widening, not about whether the band works.

The review asks for the comparison that settles this: against a valid
alternative on the same target, not against the T1 anchor. The repository
contains exactly one other valid T2 construction, `noise_enlargement` — the
anchor widened by a tail bound on the target's sampling error, shape-free.
Same budget, $\alpha_0=\eta=0.05$, target 0.90, $\nu=10$ per population,
40,000 replicates:

| $K$ | $\rho$ | oracle cov. | **safe cov.** | enlargement cov. | safe/oracle width | **safe/enlargement width** |
|---|---|---|---|---|---|---|
| 30 | 0.447 | 0.964 | 0.970 | 0.999 | 1.053 | **0.680** |
| 30 | 0.894 | 0.965 | 0.986 | 1.000 | 1.644 | **0.416** |
| 100 | 0.707 | 0.950 | 0.968 | 1.000 | 1.122 | **0.468** |
| 300 | 0.707 | 0.951 | 0.964 | 1.000 | 1.075 | **0.446** |
| 300 | 0.894 | 0.947 | 0.981 | 1.000 | 1.270 | **0.301** |

The safe band is **30 to 68 percent narrower than the only other valid latent
target construction available**, at coverage that never falls below 0.955
against a 0.90 target. The enlargement band covers at 0.999 or above
everywhere: valid, and wasting almost its whole budget. This is the comparison
the paper should lead with, and it does not depend on certifying anything.

### Where the observed conservatism comes from

The review is right that a realised 0.95 and a proven 0.90 are different
statements, and that this memo must not blur them. The budget was declared in
advance as $\alpha_0=\eta=0.05$ and the guarantee claimed is 0.90; 0.955 is
realised conservatism. It decomposes:

- **conformal granularity**, $m/(K+1)-(1-\alpha_0)$: 0.014 at $K=30$, 0.001 at
  $K\ge100$. Only $K+1$ levels are achievable, so at small $K$ the anchor
  overshoots. This is also what the review's point about small $K$ refers to:
  at $K=30$ the radius is finite only for $\alpha_0\ge1/(K+1)=0.032$, so the
  split of a total budget between $\alpha_0$ and $\eta$ is constrained, not
  free.
- **the union step**, realised safe coverage minus oracle coverage: 0.004 to
  0.035 against an $\eta$ of 0.05.

So the union argument spends between a tenth and seven tenths of its budget.
It is loose, but not the main source of the gap, and a sharper joint argument
would recover at most about three percentage points.

### Standing conditions on every statement above

Under the equal-design-variance model of §1, assumption (S), and exchangeability
of the observed curves. None of the three is verified here and (S) is not even
addressed. "Valid at every $(K,\nu,\rho)$" in §3 means within that model, and
the sentence should carry the qualifier wherever it appears.

---

## 8. Unequal design variances: the scalar case, closed

`exp11`, protocol `docs/PROTOCOL_exp11_heteroscedastic.md`, results
`results/exp11_heteroscedastic.csv`. 45 cells, 20,000 replicates,
$\nu_i=10$ per population, $\alpha_0=\eta=0.05$, guaranteed level 0.90.
Scalar target throughout; coordinates are **not** touched here.

With $D_i$ unequal, neither side of Proposition C's pivot is chi-square. The
numerator $\overline{\widehat D}$ is a weighted sum of chi-squares; the
denominator $S_Y^2$ is a quadratic form in independent but non-identically
distributed normals, with
$$\mathrm{Var}(S_Y^2)=\frac{2\big[s_2(1-2/K)+s_1^2/K^2\big]}{(K-1)^2},
\qquad s_1=\sum_i\sigma_i^2,\ s_2=\sum_i\sigma_i^4,\ \sigma_i^2=A+D_i,$$
which reduces to $2T^2/(K-1)$ exactly when the $\sigma_i^2$ are equal. Matching
two moments on each side does not make the ratio an $F$, so the question is
empirical: over what range does the one-sided upper limit keep its budget?

**R1, R2 — control is never lost.** $\Pr(\kappa>\kappa_U)$ against $\eta=0.05$,
Monte Carlo standard error 0.0015: maximum over all 45 cells is **0.0514** with
oracle degrees of freedom and **0.0481** with feasible ones. At
$\sigma_{\log}=0$ the oracle version returns 0.047–0.051, reproducing `exp10`.
This is protocol outcome 1: **the scalar heteroscedastic case is closed.**

**But the feasible version pays for it in conservatism, and the cost grows.**
$\Pr(\kappa>\kappa_U)$, feasible degrees of freedom:

| $K$ | $\bar D/A$ | $\sigma_{\log}=0$ | 0.5 | 1.0 | 1.5 |
|---|---|---|---|---|---|
| 30 | 1 | 0.039 | 0.030 | 0.009 | **0.002** |
| 100 | 4 | 0.035 | 0.025 | 0.012 | **0.001** |
| 300 | 4 | 0.038 | 0.030 | 0.016 | **0.004** |

The oracle version stays near 0.05 over the same cells (0.012 at the worst).
So the approximation is not what degrades — **plugging $\widehat D_i$ into the
Satterthwaite formula is.** That is the same plug-in mechanism `exp09` §4 found
in the variance component, appearing again in the degrees of freedom.

**R3 — the denominator is the binding channel, and it defines an effective
population count.** $\nu_{\mathrm{den}}/(K-1)$:

| $K$ | $\bar D/A$ | $\sigma_{\log}=0$ | 0.5 | 1.0 | 1.5 |
|---|---|---|---|---|---|
| 100 | 0.25 | 1.000 | 0.991 | 0.959 | 0.879 |
| 100 | 1 | 1.000 | 0.936 | 0.755 | 0.592 |
| 100 | 4 | 1.000 | 0.817 | 0.498 | **0.144** |

Against $\nu_{\mathrm{num}}$, which never falls below 75 and is usually in the
hundreds or thousands. **Unequal design variances cost information through the
observed spread, not through the variance estimator.** At the worst cell 100
populations carry the information of 14.

This is the effective population count the project has been looking for, and it
is not an assumption: it is $\mathrm{tr}((P\Sigma)^2)$, computable from the
data, degrading with the dispersion of $A+D_i$. It composes with the other two
losses already identified — the $\rho^4$ factor of §1 and the one-contrast-per-
country cost of §4 — and none of them is the raw count $K$.

**R4 — coverage, and the model-based competitor fails.** Guaranteed 0.90:

| $K$ | $\bar D/A$ | $\sigma_{\log}$ | oracle | **safe** | plug-in $\kappa$ | enlargement | Gaussian model |
|---|---|---|---|---|---|---|---|
| 30 | 4 | 0.0 | 0.969 | 0.984 | 0.713 | 1.000 | **0.667** |
| 30 | 4 | 1.5 | 0.974 | 0.995 | 0.594 | 1.000 | **0.547** |
| 300 | 4 | 1.5 | 0.945 | 0.992 | 0.776 | 1.000 | **0.733** |
| 300 | 0.25 | 1.5 | 0.951 | 0.955 | 0.950 | 0.988 | 0.899 |

Minimum safe-band coverage over all 45 cells is **0.950**. The Gaussian
plug-in prediction interval — the review's requested model-based comparator,
and what an analyst who believes the model would actually compute — **never
reaches its nominal 0.90 in any cell**, and falls to 0.547. It is narrow and
invalid, which is the useful contrast.

**R5 — width, against a comparator given every advantage.** The enlargement's
anchor/tail budget split was scanned and the narrowest valid choice used per
cell; the optimum is 0.5 to 0.8 on the anchor, so the even split used earlier
was handicapping it. Even so, safe / enlargement:

| $K$ | $\bar D/A$ | $\sigma_{\log}=0$ | 1.0 | 1.5 |
|---|---|---|---|---|
| 30 | 0.25 | 0.750 | 0.808 | 0.825 |
| 100 | 1 | 0.464 | 0.503 | 0.547 |
| 300 | 4 | 0.295 | 0.338 | 0.413 |

**The safe band is 18 to 71 percent narrower than the optimised enlargement
band, at every cell in the grid**, and its own width penalty over the
infeasible oracle runs 1.02 to 1.87. Dispersion narrows the gap but does not
close it anywhere.

**The comparison is of assumptions as well as of widths, and must be labelled
so.** The enlargement reaches T2 through a Gaussian tail bound on the target's
sampling error; the safe correction reaches it through assumption (S) plus a
bound on the correction factor. These simulations are generated under (S). The
defensible statement is: *where the common-shape assumption holds, the safe
correction is substantially narrower than the sampling-error enlargement at the
same guaranteed level.* Nothing here says what happens when (S) fails — that is
`exp01`, and it is a separate axis.

**What is still assumed.** $\overline{\widehat D}\perp S_Y^2$ holds by
construction in this model and is false for a CDF ordinate (`exp09` §7.1).
Populations are independent. And the whole experiment is scalar: the ESS path
standardises coordinate by coordinate (§4), and the simultaneity cost of a
$\kappa_U(\cdot)$ band across coordinates remains unmeasured.

---

## 9. Closing the scalar case, and two retractions

`exp12`, protocol `docs/PROTOCOL_exp12_closing_scalar.md`, results
`results/exp12_closing_scalar.csv`. 27 cells, 20,000 replicates,
$\nu_i=10$, $\alpha_0=\eta=0.05$, guaranteed 0.90.

### Retraction 1: $\nu_{\mathrm{den}}$ is not the information

§8 reported that unequal design variances reduce 100 populations to 14 and
called this the effective population count. **That conflated the precision of
one statistic with the information in the data, and the two move in opposite
directions.** At $K=100$, $A=1$, mean $D=4$:

| $D_i$ | $\nu_{\mathrm{den}}$ | $K_I=\sum_i(A/(A+D_i))^2$ |
|---|---|---|
| all $4$ | 99.0 | 4.00 |
| 50 at $0.1$, 50 at $7.9$ | 61.8 | **41.95** |

Dispersion **multiplies** the Fisher information by ten — the manuscript's own
Jensen argument in §4.2 says so — while lowering the precision of the unweighted
sample variance. $\nu_{\mathrm{den}}$ is the effective degrees of freedom of
$S_Y^2$, a property of that estimator. It must never be reported as
$K_{\mathrm{eff}}$.

### Retraction 2: the scalar case was not closed

§8 called it closed on the strength of `exp11`, which used the
common-denominator construction (b), $|Y|_{(m)}\widehat\kappa$. **That is not
the construction the manuscript's Section 3 licenses.** Under (S) with unequal
$v_c$ the licensed oracle standardises per population,
$M_c=|Y_c|/\sqrt{s_G^2+v_c^2}$, band $s_G M_{(m)}$ — construction (a). The two
coincide only when the $v_c$ are equal, and `exp07_widths.py` uses (b).

`exp12` measures the difference. Construction (a) covers at exactly $m/(K+1)$
at every dispersion (largest deviation 0.003, Monte Carlo error 0.0015), as
exchangeability requires. Construction (b) departs — up to **+0.021** at the
two-point cell, at a width **12 percent** above (a), and by $-0.003$ in the
other direction elsewhere. It is not exact and it is not uniformly conservative.

**And the scalar $\kappa_U$ band does not contain the licensed oracle band.**
$\Pr(B_{\mathrm{safe}}^{(b)}\supseteq B_{\mathrm{oracle}}^{(a)})$ falls to
**0.835**. Protocol outcome 1: `exp11`'s band is not the object Proposition E
covers under heteroscedasticity.

A correct heteroscedastic safe band exists and is built here. The half-width is
the $m$-th order statistic of $h_c(s)=|Y_c|/\sqrt{1+v_c^2/s^2}$; each $h_c$ is
increasing in $s$, so the band is increasing in $s_G$ and the union over an
interval is the band at its upper endpoint — an upper limit on $s_G$, not on
$\kappa$. Its realised coverage is 0.964 to 0.996 against a guaranteed 0.90.
**Its containment of the oracle band is 0.944 to 0.997, marginally short of
$1-\eta$ in the low-dispersion cells**, because $h_c$ is *decreasing* in $v_c$,
so substituting $\widehat v_c$ is not conservative and the monotonicity argument
does not cover it. That gap is real, it is small, and it is not yet closed.

### The finding worth the section: information is discarded, not destroyed

Efficiency, defined as the information bound divided by the realised root mean
squared error of $\widehat A$:

| $K$ | $\bar D/A$ | $\sigma_{\log}$ | $K_I$ | unweighted | oracle weights | plug-in weights |
|---|---|---|---|---|---|---|
| 300 | 4 | 0.0 | 12.0 | 0.996 | 0.998 | **0.341** |
| 300 | 4 | 1.0 | 44.7 | 0.334 | 1.003 | 0.502 |
| 300 | 4 | 1.5 | 72.5 | **0.232** | 0.999 | 0.437 |
| 300 | 4 | two-point | 125.9 | **0.234** | 0.993 | 0.689 |
| 300 | 1 | 1.5 | 157.4 | 0.459 | 1.000 | 0.889 |

Three readings, in order of how much they matter.

**The unweighted deconvolution throws away three quarters of the available
precision at realistic dispersion.** It is efficient only when the design
variances are equal, which is the one case surveys never present.

**Optimal weighting recovers essentially all of it**, at every cell, which is
`exp09` Proposition 2 holding under heteroscedasticity. So the answer to the
question the review posed is: **discarded, not destroyed.** The manuscript's
whole construction — $s_Y^2$ minus a mean design variance — is the discarding
step.

**But naive weighting backfires**, and this is the practical sting. Plug-in
weights built from $\widehat D_i$ reach 0.341 where the *unweighted* estimator
reaches 0.996. Weighting helps only once dispersion is large enough to
outweigh the plug-in damage, and even then reaches 0.44 to 0.69, not 1. This is
`exp09` §4 again: the correlation between $\widehat D_i$ in the weight and in
the residual. A usable weighted construction needs weights that are independent
of the residual — smoothed design variances, or sample splitting — and building
one is a real task, not a corollary.

### The model-based comparator: prediction S5 was wrong

The review asked for a Gaussian competitor that carries an error budget rather
than a plug-in. Built as $\pm z_{1-\alpha_0/2}\sqrt{A_U}$ with $A_U$ a one-sided
Graybill–Wang upper limit at $\eta$, guaranteed at the same 0.90. **It is wider
than the safe conformal band in every cell** — by 3 to 14 percent — which is the
opposite of what the protocol predicted.

The mechanism is the one from §1 and it is worth stating because it is not about
conformal prediction at all. Both constructions use the same $A_U$. The
model-based band is proportional to $\sqrt{A_U}$, so its sensitivity to the
scale limit is one. The conformal band has
$\partial\log h_c/\partial\log s=\rho_c^2$, so its sensitivity is $\rho^2$.
**The advantage is the $\rho^2$ damping, not the rank argument.** A parametric
interval that exploited the same damping would match it, and the honest
comparison should say so rather than claim a win for conformal prediction.

The plug-in Gaussian interval remains the useful negative control: narrowest of
all and covering 0.539 to 0.897 against a nominal 0.90, never reaching it.

### Downgrading the Satterthwaite claim

§8 said unequal design variances do not break the upper limit. The defensible
statement is narrower and is adopted: **across the 45 conditions of `exp11` and
the 27 of `exp12`, no evidence was found of the nominal level being exceeded.**
Satterthwaite approximates a heteroscedastic quadratic form by a single
chi-square; oracle degrees of freedom do not make the ratio exactly $F$, and
nothing here proves finite-sample control. Claiming it would need an
approximation-error bound or a construction that is conservative by design.

One point of fact, since it was raised: the oracle-versus-feasible comparison in
`exp11` already changes **only** the degrees of freedom. Both limits are
computed from the same $R=\overline{\widehat D}/S_Y^2$ on the same replicates,
through the same function; nothing else varies. The collapse of the feasible
failure rate to 0.001–0.004 is therefore attributable to the substitution, and
it is excess conservatism rather than loss of control.

---

## 10. What a feasible weighting recovers, and a band that is guaranteed

`exp13`, protocol `docs/PROTOCOL_exp13_weights_and_containment.md`, results
`results/exp13_weights_and_containment.csv`. 12 cells, 20,000 replicates,
$\nu=10$, design variances generated as $D_i=c\,e_i/n_i$ with $n_i$ a design
variable known without error and $e_i$ lognormal GVF misfit of dispersion
$\sigma_e$.

Two questions kept apart throughout: Part A estimates $A$, Part B asks whether a
band contains the oracle band. **Neither result licenses the other.**

### The three-way decomposition, and a properly scoped restatement

| $K$ | $\bar D/A$ | $\sigma_e$ | cost of estimating $D_i$ | unweighted procedure | feasible weighting |
|---|---|---|---|---|---|
| 60 | 1 | 0.0 | 1.007 | 1.319 | **0.999** |
| 60 | 4 | 0.3 | 1.016 | **2.640** | 1.124 |
| 200 | 1 | 0.6 | 1.006 | 1.458 | 1.098 |
| 200 | 4 | 0.0 | 1.018 | **1.999** | 1.038 |
| 200 | 4 | 0.6 | 1.012 | **3.017** | 1.414 |

Each column is the ratio to the previous stage:
$\sqrt{2/K_{I,\mathrm{known}}}\to\sqrt{2/K_{I,\mathrm{eff}}}\to\mathrm{RMSE}$.

**Estimating the design variances costs 0.5 to 1.9 percent — at
$\nu=10$ degrees of freedom per population, which must be quoted with the
figure.** The ratio of information-based standard-error bounds is at most
$\sqrt{1+\rho^4/\nu_{\min}}$ (and at most $\sqrt{1+1/\nu_{\min}}$ without the
$\rho$ refinement), so the observed range is what this $\nu$ permits: 3.15
percent at $\rho^2=0.8,\nu=10$, but 7.7 percent at $\nu=4$ and 14.9 percent at
$\nu=2$. **A result at $\nu=10$ does not transfer to a small area with four
PSUs**, and the defensible sentence is: at the degrees of freedom examined, the
loss from the design variances being unknown was smaller than the loss from the
estimating procedure.

**The unweighted procedure costs 28 to 202 percent**, and that is the entire
loss. §9's "three quarters of the information is discarded" is restated: it is
the third gap only, in this closed Gaussian--$\chi^2$ model, and it is a
statement about the estimator rather than about survey data.

### T2 was wrong, and the reason is the useful finding

The protocol predicted that a GVF fitted on all populations — including the
population whose weight it forms — would inherit the plug-in failure.
**It does not.** Efficiency against the estimated-$D$ bound:

| arm | range over 12 cells | bias range |
|---|---|---|
| `unweighted` | 0.33–0.78 | $-0.013$ to $+0.015$ |
| `plugin` (own $\widehat D_i$) | 0.49–0.91 | $+0.09$ to $\mathbf{+0.58}$ |
| `gvf_all` (fitted on all, own included) | **0.71–1.00** | $+0.004$ to $+0.075$ |
| `gvf_cv` (two-fold cross-fitting) | 0.58–0.92 | — |
| `oracle` | 0.99–1.01 | $\approx0$ |

`gvf_all` beats `unweighted` in 12 of 12 cells and beats `gvf_cv` in 12 of 12.

The proposed mechanism is dilution: a GVF fit averages $\widehat D_i$ over all
$K$ populations, so population $i$'s own estimate enters its own weight with
coefficient $O(1/K)$. The dependence is not removed, it is diluted. **Two values
of $K$ do not establish a rate**, and the final estimator is a ratio with a
random denominator, so the order of the bias does not follow from the influence
of one weight. §11 tests the rate over four values of $K$ rather than asserting
it.

So the review's objection stands and the memo adopts it. **"A valid method must
use weights independent of the residual" was too strong.** What the evidence
supports is: weights formed from a single population's own estimate fail badly;
weights formed from a smooth over many populations do not, with a residual
$O(1/K)$ bias that should be quantified rather than assumed away.

### Sample splitting costs more than it buys, except at high design share

`gvf_split` beats its matched half-sample baseline in **12 of 12** cells — the
weighting works. Against the *full-sample* unweighted estimator it wins in
**6 of 12**, and those six are exactly the $\bar D/A=4$ cells. At $\bar D/A=1$
the half of the data given up exceeds what the weighting recovers.

Cross-fitting was meant to recover the split cost and is worse than `gvf_all`
in all 12 cells **of this model and grid**. That is evidence about these
conditions, not a general statement that cross-fitting is unnecessary; the
comparison would have to be redone wherever the smoother's own-observation
influence is larger.

### T5 holds: the gain depends on the design variable actually predicting $D_i$

`gvf_all` efficiency at $K=200$, $\bar D/A=4$: 0.963 at $\sigma_e=0$, 0.893 at
0.3, 0.707 at 0.6. A generalised variance function that does not fit gives back
most of the gain. This is the condition under which the result transfers to a
survey and it should be stated as such, not buried.

### An unplanned side effect worth reporting

The share of replicates returning $\widehat A\le0$ falls from **0.198–0.237**
(unweighted, $K=60$, $\bar D/A=4$) to **0.017–0.057** (`gvf_all`). The manuscript
§4.2 already reads zero estimates as the symptom of an infeasible regime; part
of that symptom is the estimator, not the regime.

Largest single weight share is 0.012–0.081 across all feasible arms and
comparable to the oracle's, so none of this is driven by extreme weights.

### Part B — a band whose containment holds

$h_c(s,v_c)=|Y_c|/\sqrt{1+v_c^2/s^2}$ increases in $s$ and **decreases in
$v_c$**, so bounding $s_G$ above while substituting $\widehat v_c$ is not
enough. With $\eta_1+\eta_2=\eta$, take $s_U$ an upper limit at $\eta_1$ and
$v_{L,c}^2=\nu_c\widehat D_c/\chi^2_{\nu_c,1-\eta_2/K}$ simultaneous lower
limits at $\eta_2$ by Bonferroni; then
$R_U=\operatorname{ord}_m\{|Y_c|/\sqrt{1+v_{L,c}^2/s_U^2}\}$ contains the oracle
half-width on an event of probability at least $1-\eta$.

| quantity | `exp12`-style band | Bonferroni reference |
|---|---|---|
| containment of the oracle band | **0.940–0.994** | **0.9998–1.0000** |
| latent-target coverage (guaranteed 0.90) | 0.965–0.992 | 0.984–0.999 |
| width over the oracle band | 1.10–1.53 | 1.28–1.89 |

**Containment is achieved empirically — but the guarantee was claimed too
early, and §11 retracts it.** The construction contains the oracle band
essentially always and costs 17 to 36 percentage points of extra width over the
band that does not. What that establishes is conservative *behaviour in the
conditions examined*, with two conservatisms compensating. The stated
$\eta_1+\eta_2$ guarantee needs $\Pr(A>A_U)\le\eta_1$, and the $s_U$ used here
covers at 0.963--0.969 against 0.975. §11 builds a limit for which the argument
goes through.

The shortfall of the `exp12`-style band decomposes into two causes, and only one
was identified before. $\Pr(v_c\ge v_{L,c}\ \forall c)$ is 0.974–0.977 against a
nominal 0.975, so Bonferroni is essentially exact here. But $\Pr(s_G\le s_U)$ is
**0.963–0.969** against a nominal 0.975 at $\bar D/A=1$: the normal-approximation
upper limit for $A$ is itself mildly anti-conservative. So part of the 0.940
containment is the $\widehat v_c$ substitution and part is the scale limit. The
second is fixable with an exact or Graybill–Wang limit; the first is not, and
needs the two-sided bounding above.

### Standing limitations, unchanged

Scalar target. Populations independent. $Y_i\perp\widehat D_i$, false for a CDF
ordinate. The $\chi^2$ model for $\widehat D_i$ is not established for complex
designs. And nothing here has been through a finite-population sampling
experiment, which is the step that decides whether any of it transfers.

---

## 11. The chain, with the guarantee named

`exp14`, protocol `docs/PROTOCOL_exp14_chain.md`, results
`results/exp14_chain.csv`. 8 main cells at 20,000 replicates, plus a bootstrap
block, a rate block and a leverage block. $\nu=10$, $\eta_1=\eta_2=0.025$,
$\alpha_0=0.05$, guaranteed 0.90.

### A scale limit for which the argument goes through

With $\mu_i$ known, $U(A)=\sum_cY_c^2/(A+D_c)\sim\chi^2_K$ exactly. On
$E_D=\{v_c\ge v_{L,c}\ \forall c\}$ the feasible
$\widetilde U(A)=\sum_cY_c^2/(A+v_{L,c}^2)$ dominates it, so with $A_U$ the root
of $\widetilde U(A)=\chi^2_{K,\eta_1}$,
$$\Pr(E_D\cap\{A>A_U\})\le\Pr\{U(A)<\chi^2_{K,\eta_1}\}=\eta_1,
\qquad\Pr(E_A^c\cup E_D^c)\le\eta_1+\eta_2 .$$
The same simultaneous lower limits serve the scale limit and the band, so the
budget is $\eta_1+\eta_2$ and not $\eta_1+2\eta_2$. **What is derivable is
therefore an unconditional guarantee of $1-\eta_1-\eta_2=0.95$**; the
0.975 quoted in the table below is each arm's own nominal target, not this
procedure's guarantee, and the two must not be conflated.

**And the pivot needs normality, not assumption (S).** Standardised curves
sharing a common law does not give $\sum_cW_c^2\sim\chi^2_K$ unless that law
is normal. So what is established is: *under an independent normal population
model with valid simultaneous lower limits on the design variances, a
conservative procedure containing the oracle band can be constructed.* That is
narrower than a statement about survey CDF bands.

**The limit is a pivot and does not use the point estimator.** That is why the
connection the review asked for is a question rather than a corollary.

### The answer to that question is negative, and clean

Coverage of the scale upper limit, nominal 0.975, Monte Carlo error 0.0011:

| $K$ | $\bar D/A$ | $\sigma_e$ | `chi2_pivot` | `normal_unw` | **`normal_gvf`** | `gw` | `boot_gvf` |
|---|---|---|---|---|---|---|---|
| 60 | 1 | 0.0 | **0.9998** | 0.9678 | 0.9397 | 0.9654 | — |
| 60 | 4 | 0.6 | **1.0000** | 0.9920 | **0.8998** | 0.9496 | — |
| 200 | 1 | 0.6 | **1.0000** | 0.9747 | 0.9518 | 0.9604 | — |
| 200 | 4 | 0.6 | **1.0000** | 0.9895 | 0.9414 | 0.9395 | — |
| 60 | 4 | 0.3 | **1.0000** | — | — | — | 0.901 |
| 200 | 4 | 0.3 | **1.0000** | — | — | — | 0.920 |

The arm built on the best point estimator covers at 0.900 to 0.956 against a
nominal 0.975. **The explanation offered here — "smaller variance and positive
bias, a tighter interval around a displaced centre" — is wrong, and §12
retracts it.** For a one-sided upper limit, failure is a left-tail event and a
positive bias *raises* coverage. §12 diagnoses the real cause and, correcting
it, largely restores coverage. **The reading that an estimation improvement
cannot reach an interval is withdrawn.**

Graybill--Wang with Satterthwaite degrees of freedom also undercovers
(0.940--0.967). The bootstrap here covers at 0.901 and 0.920 — but it is a
*basic* upper limit at $B=200$, where the 2.5 percent tail rests on about five
replicates, and §12 shows that choice was most of the defect.

### What validity costs

Band width over the oracle band: `chi2_pivot` 1.31--2.03, `normal_gvf`
1.26--1.74, `gw` 1.27--1.87, `boot_gvf` 1.68--1.72 — **observed width
differences between the constructions compared, 4 to 20 percent, and not a
minimum price of validity.** §12 shows a valid-enough construction that is much
tighter. Latent-target coverage is
0.985--1.000 for every arm against a guaranteed 0.90, so all of them are
conservative on the band even when the scale limit is not.

That decoupling is itself the finding. Containment of the oracle half-width is
0.989--1.000 for **every** arm, including those whose scale limit undercovers,
because all of them substitute the simultaneous lower limits $v_{L,c}$ in the
band. Comparing with §10, where substituting $\widehat v_c$ gave containment 0.940:
in the conditions examined, **the conservatism of the simultaneous lower limits
compensated for the scale limit's undercoverage**, producing high final
containment. That is not the same as showing the scale limit was blameless —
a conservative $v_L$ can mask a failing $s_U$, and both can be at work.

### U5: the rate is tested now

$|$bias$|$ of `gvf_all` at $\bar D/A=4$, $\sigma_e=0.3$: 0.0874 at $K=60$,
0.0518 at 120, 0.0227 at 240, 0.0123 at 480. Slope of $\log|$bias$|$ on
$\log K$ is $\mathbf{-0.966}$. Four points, consistent with $O(1/K)$. The
theoretical justification is still owed; the rate is no longer only asserted.

### U6 failed, and the test was the wrong test

Heavy-tailed $n_i$ raised the largest leverage from 10.8 to 95.0 times the
median and the GVF bias **fell**, 0.033 to 0.018. The reason is specific and
worth recording: with $D_i=c\,e_i/n_i$ and the ratio smoother
$\widehat c=\overline{\widehat D_jn_j}$, the product $\widehat D_jn_j=c\,e_j
\chi^2_{\nu}/\nu$ is free of $n_j$, so **leverage is uniform in $n$ by
construction** however dispersed $n$ is. The cell stressed the design variable
and not the smoother. A real leverage stress needs a misspecified GVF form, or a
smoother whose influence is genuinely uneven, and the review's concern is
therefore still open rather than answered.

---

## 12. Diagnosis: the explanation in §11 was wrong, and the GVF route is not dead

`exp15`, protocol `docs/PROTOCOL_exp15_diagnosis.md`, results
`results/exp15_*.csv`. $K\in\{60,200\}$, $\bar D/A=4$, $\sigma_e\in\{0,0.6\}$,
$\nu=10$, 20,000 replicates (jackknife 2,000, bootstrap 400 outer $\times$
$B=2{,}000$).

### The error

§11 attributed the GVF limit's undercoverage to a positive bias with a small
variance. For a one-sided upper limit $A_U=\widehat A+z_{1-\eta_1}\widehat{se}$
the failure event is
$$A>A_U\iff\frac{\widehat A-A}{\widehat{se}}<-z_{1-\eta_1},$$
a **left**-tail event, and with $\widehat A=A+b+\sigma Z$ at known $\sigma$ the
coverage is $\Phi(z_{1-\eta_1}+b/\sigma)$, which a positive $b$ *increases*. The
explanation was directionally wrong and the cause was unidentified.

### The actual cause: a random denominator correlated with the numerator

Standardised error $t=(\widehat A-A)/\widehat{se}$, against $-1.96$:

| $K$ | $\sigma_e$ | $t$ mean | $t$ sd | $t$ 2.5% | with a **fixed** denominator |
|---|---|---|---|---|---|
| 60 | 0.0 | $-0.146$ | 1.12 | $\mathbf{-2.91}$ | $-1.62$ |
| 60 | 0.6 | $-0.158$ | 1.22 | $\mathbf{-3.25}$ | $-1.54$ |
| 200 | 0.6 | $-0.005$ | 1.10 | $\mathbf{-2.49}$ | $-1.59$ |

With the variance evaluated at the *true* $D_i$ — a denominator that neither
varies nor depends on the numerator — the left tail is **lighter** than normal
($-1.54$ to $-1.72$) and coverage is 0.989–0.996. With the estimated denominator
the tail is far heavier. The fixed-denominator comparison removes the
denominator's variability *and* its dependence on the numerator at once, so it
identifies **using an estimated denominator as the main failure path** without
separating the two mechanisms. A plausible reading is that $\widehat{se}$ and
$\widehat A$ are built from the same $\widehat D_i$ so the interval contracts
where $\widehat A$ is low; that reading is not isolated by this experiment.
Either way it is a studentisation problem, not a bias problem.

A second, smaller contribution is V2, and it is real: the variance was evaluated
at the *smoothed* $\widetilde D_i$. Ratio of mean $\widehat{se}$ to realised
standard deviation — 0.891 to 1.004 at $\widetilde D_i$, **1.007 to 1.040 at
$\widehat D_i$**, and the gap widens with $\sigma_e$ exactly as predicted.
Correcting the argument alone lifts coverage from 0.911 to 0.952; it does not
reach nominal, because the tail problem remains.

A delete-one-population jackknife over the whole procedure gets the *magnitude*
right (ratio 0.972–1.038) and does **not** fix the tail (2.5% quantile $-2.35$
to $-3.18$), so its coverage is 0.919–0.959. V3 is falsified: the missing
weight-estimation uncertainty was not the binding defect either.

### The bootstrap form was most of the defect

| $K$ | $\sigma_e$ | basic, $B=200$ (§11) | **percentile, $B=2{,}000$** | studentised |
|---|---|---|---|---|
| 60 | 0.0 | 0.895 | **0.953** | 0.933 |
| 60 | 0.6 | 0.905 | **0.960** | 0.930 |
| 200 | 0.0 | 0.953 | **0.973** | 0.968 |
| 200 | 0.6 | 0.933 | **0.988** | 0.980 |

Monte Carlo error 0.0078 on only 400 outer replicates. **Two things changed at
once here — the form and the replicate count — so neither can be credited, and
§13 separates them from a single set of draws: the form is worth 3 to 8
percentage points and the count 0.1 to 0.9.** §13 also re-measures the coverage
at 2,000 outer replicates and finds 0.939–0.968, so the reading that the
percentile limit reaches nominal at $K=200$ **does not survive the more precise
measurement**. What stands is that §11 compared a badly chosen resampling form
against a pivot and read the result as a property of the estimator.

### And the corrected limit is far tighter than the pivot

Mean $A_U$ on identical replicates, true $A=1$:

| $K$ | $\sigma_e$ | pivot | percentile bootstrap | ratio |
|---|---|---|---|---|
| 60 | 0.0 | 5.46 | 2.41 | 0.44 |
| 60 | 0.6 | 5.66 | 2.73 | 0.47 |
| 200 | 0.0 | 4.70 | 1.79 | **0.38** |
| 200 | 0.6 | 4.39 | 1.85 | 0.42 |

The pivot covers at 1.000 — it spends almost none of its budget — and its limit
is four to six times the truth. **So §11's reading is withdrawn.** The finding
is not that estimation improvements cannot reach an interval; it is that the
particular constructions tried in §11 were poor, and a correctly formed one is
1.5 to 2.5 times tighter than the pivot while still undercovering its nominal
level by 0.7 to 3.6 points (§13). **It is a promising approximation, not a
procedure with a guarantee**, and §13 measures what its tightness is worth in
the band.

**Not yet measured, and it is the next thing:** the *band* built on the
percentile-bootstrap $A_U$. §11 reported band widths for the pivot only. Given a
2.5-fold tighter scale limit the band should be markedly narrower, but that has
not been run and is not claimed.

### V5: the unknown-mean extension holds

With $Y\sim N(X\beta,AI+\mathrm{diag}(\mathbf D))$, $\mathrm{rank}(X)=p$, and
$Q(a,\mathbf D)=\min_\beta\sum_c(Y_c-x_c^\top\beta)^2/(a+D_c)$ refitted at each
candidate $a$:

| $K$ | $p$ | mean $Q$ | expected | var $Q$ | expected | KS $p$ | $A_U$ coverage |
|---|---|---|---|---|---|---|---|
| 60 | 1 | 59.04 | 59 | 117.4 | 118 | 0.10 | 1.000 |
| 60 | 3 | 56.96 | 57 | 114.4 | 114 | 0.55 | 1.000 |
| 200 | 3 | 197.00 | 197 | 397.7 | 394 | 0.21 | 1.000 |

$Q(A,\mathbf D)\sim\chi^2_{K-p}$ confirmed and the limit is valid at the 0.95
guarantee. **This bounds the variance component only** — it says nothing about
the error from centring the band on an estimated mean, or about exchangeability
of the conformal scores under an estimated centre.

### Block 3: the normal-model comparison the pivot now obliges

Since normality is an explicit assumption, a normal-model interval is given the
same $A_U$, the same $\eta_1,\eta_2$ and the same $\alpha_0$:

| $K$ | $\sigma_e$ | oracle | conformal | normal model | normal / conformal width |
|---|---|---|---|---|---|
| 60 | 0.0 | 0.953 | 0.999 | 1.000 | **1.145** |
| 200 | 0.6 | 0.949 | 1.000 | 1.000 | **1.069** |

The conformal band is 7 to 14 percent narrower on the same information, which is
the $\rho^2$ damping of §1 once more. Both are grossly conservative here
(0.999–1.000 against a guaranteed 0.90) because the pivot $A_U$ is loose; the
comparison should be repeated on the corrected limit before it is used.

---

## 13. What the tighter limit is worth in the band: 3 to 14 percent

`exp16`, protocol `docs/PROTOCOL_exp16_band_comparison.md`, results
`results/exp16_band_comparison.csv`. 8 cells, $K\in\{60,200\}$,
$\bar D/A\in\{1,4\}$, $\sigma_e\in\{0,0.6\}$, $\nu=10$, 2,000 outer replicates,
$B=2{,}000$. Monte Carlo error 0.0035 near 0.975 and 0.0067 near 0.90. No new
estimator; the cells where the percentile limit failed are kept.

### W1 — the limit gain does not carry into the band

All ratios below are **percentile over pivot**, so a ratio $r$ means the
percentile band is $100(1-r)$ percent narrower and the pivot band is
$100(1/r-1)$ percent wider; the two are not the same number and only the first
is quoted in the text.

| $K$ | $\bar D/A$ | $A_U$ ratio | $\sqrt{\cdot}$ lower bound on the width ratio | **band ratio** | elasticity |
|---|---|---|---|---|---|
| 60 | 1 | 0.656 | 0.810 | **0.967** | 0.217 |
| 60 | 4 | 0.434 | 0.659 | **0.876** | 0.363 |
| 200 | 1 | 0.643 | 0.802 | **0.966** | 0.215 |
| 200 | 4 | 0.400 | 0.632 | **0.861** | 0.351 |

**A scale limit 1.5 to 2.5 times tighter makes the band 3 to 14 percent
narrower.** The direction of the square-root relation matters and the earlier
label was ambiguous: for $A_1\le A_2$,
$$\sqrt{A_1/A_2}\ \le\ \frac{h_c(A_1)}{h_c(A_2)}=\sqrt{\frac{A_1(A_2+L_c)}{A_2(A_1+L_c)}}\ \le\ 1,$$
and an order statistic preserves a common positive factor, so
$R(A_1)/R(A_2)\ge\sqrt{A_1/A_2}$ **per replicate**. The square root is a
*lower* bound on the width ratio, i.e. an upper bound on the achievable
narrowing. The column above applies it to the *mean* limit ratio, which is a
useful reference point and **not** a bound on the mean width ratio; the
per-replicate statement is the one that is proved.

The realised narrowing is well short of even that reference, because the
elasticity $L_c/\{2(A+L_c)\}$ runs 0.20 to 0.36 rather than its maximum of
$1/2$. The review's warning against reading a width ratio off a limit ratio was
exactly right: the mean-limit ratio would have overstated the narrowing about
twofold.

The gain is largest where the design share is largest — 12 to 14 percent at
$\bar D/A=4$, 3.3 percent at $\bar D/A=1$ — which is the elasticity, not the
sample size.

### W2, W3 — both bands cover, and by a wide margin

Latent-target coverage against a guaranteed 0.90: `piv_conformal` 0.986–1.000,
`pct_conformal` **0.983–0.999**, `pct_normal` 0.972–0.991, oracle 0.939–0.958.
Containment of the oracle half-width: pivot 1.000, percentile **0.9965–1.0000**
against a 0.95 requirement.

So W2 holds and W3 is falsified — containment does not degrade under the tighter
limit. **And the margin over the target is so large in every arm that the scale
limit is not what governs coverage here.** The binding conservatism is elsewhere:
the oracle band itself covers at 0.939–0.958 against $\alpha_0=0.05$, and the
$v_{L,c}$ inflation supplies the rest.

### W4 — the bootstrap form, not the replicate count

Computed from **one** set of draws, the $B=200$ arms reading the first 200:

| $K$ | $\bar D/A$ | basic $B{=}200$ | basic $B{=}2000$ | pct $B{=}200$ | pct $B{=}2000$ |
|---|---|---|---|---|---|
| 60 | 1 | 0.911 | 0.916 | 0.957 | 0.958 |
| 60 | 4 | 0.890 | 0.893 | 0.948 | 0.949 |
| 200 | 1 | 0.935 | 0.941 | 0.957 | 0.961 |
| 200 | 4 | 0.918 | 0.924 | 0.966 | 0.968 |

**The form is worth 3 to 8 percentage points; the count is worth 0.1 to 0.9.**
§12 attributed the improvement partly to the 2.5 percent tail resting on five
replicates. That attribution is withdrawn: raising $B$ tenfold moves the coverage
by less than one point.

And with 2,000 outer replicates rather than 400, the percentile limit covers at
**0.939 to 0.968** against a nominal 0.975 — below nominal in every cell,
including $K=200$. §12's reading that it reaches nominal at $K=200$ does not
survive the more precise measurement. **The correct description is a promising
approximation that undercovers by 0.7 to 3.6 points, not a valid limit.**

### W5 — falsified, and the reason is the same elasticity

On the *same* percentile limit, the normal-model interval is **narrower** than
the conformal band: ratio 0.776 to 0.981, most at $\bar D/A=4$. §12 reported the
opposite (conformal 7 to 14 percent narrower) — but that was measured on the
*pivot* limit, and §12 flagged that it should be repeated. It has been, and the
ranking flips.

The mechanism: the normal band is $z\sqrt{A_U}$, elasticity exactly $1/2$ in
$A_U$; the conformal band's elasticity is $L_c/\{2(A+L_c)\}\le1/2$, here 0.20 to
0.36. **The conformal band is less sensitive to the scale limit**, which is
consistent with it winning on a loose limit and losing on a tight one. The
elasticity difference does not by itself force a reversal at any particular
limit — the realised ranking also carries the conformal quantile, the
standardisation and the data distribution — so the statement is made within the
range measured here. Neither construction dominates; any width claim must name
the limit it was measured on, **and be read beside the realised coverage**,
since equal nominal budgets did not produce equal coverage (0.972--0.991 for the
normal interval against 0.983--0.999 for the conformal band).

### The decision this supports

Protocol outcome 2. The pivot's guarantee costs 3 to 14 percent of band width
against an approximation that undercovers its own nominal level. **On this
evidence the $\chi^2$ pivot should be the paper's method and the bootstrap a
reported alternative**, which is the opposite of what §12 pointed toward and is
the result of measuring the band rather than the limit.

Two caveats that keep this provisional. All of it is the independent normal
population model with a scalar target; the coverage margins are so wide that
they may not discriminate between constructions in a harder setting; and nothing
has been through a finite-population complex-sample experiment.

**And the decision is narrower than "the paper's method".** What has been chosen
is *the baseline procedure to carry into the next experiment*. The complex-sample
experiment does **not** test whether the pivot's guarantee holds there: its
conditions — normality of the population-level deviations, a $\chi^2$ law for the
design-variance estimator — are not satisfied by a complex design, and a
simulation cannot extend a theorem's scope. What it measures is **how stably the
procedure behaves when its conditions are not met**, and which violation moves
which quantity.

---

## 14. The fixed procedure on a finite population and a complex sample

`exp17`, protocol `docs/PROTOCOL_exp17_complex_sample.md`, results
`results/exp17_complex_sample.csv`. 8 cells, 2,000 replicates, $B=1{,}000$.
Design: 4 strata $\times$ 20 PSUs $\times$ 10 units, SRSWOR of 5 PSUs per
stratum, nominal design degrees of freedom $\nu=16$. Estimand: one
pre-specified CDF point $F_c(t_0)$ of a finite population. Target: prediction
of a **newly generated** population's $F_{K+1}(t_0)$ — not design-based coverage
for a fixed population.

**This does not extend the pivot's guarantee.** Its conditions fail here,
measurably, and are shown failing below. What is measured is stability.

### How far the conditions are from holding

| $t_0$ | $\sigma_\alpha$ | deff | $\bar D/A$ | skew | kurtosis | KS vs normal | $\mathrm{corr}(\widehat D_c,Y_c)$ | $\nu\widehat D/D$: mean, var |
|---|---|---|---|---|---|---|---|---|
| median | 0.2 | 0.81 | 0.038 | 0.00 | $-0.51$ | 0.016 | 0.003 | 15.98, **23.1** |
| median | 0.6 | 1.71 | 0.100 | 0.01 | $-0.39$ | 0.114 | $-0.006$ | 16.00, **20.5** |
| 0.15 | 0.2 | 0.80 | 0.052 | **1.09** | **1.37** | **0.0000** | **0.800** | undefined |
| 0.15 | 0.6 | 1.55 | 0.126 | **0.92** | **0.93** | **0.0000** | **0.835** | undefined |

Three violations, all real.

**Normality fails at the tail quantile**, decisively: skewness 0.92–1.10 and
excess kurtosis 0.93–1.40, Kolmogorov–Smirnov $p=0$. At the median it holds to
a mild platykurtosis.

**The $\chi^2$ law for $\widehat D_c$ is rejected everywhere**: the mean matches
(15.98–16.00 against 16) but the variance is **20.5–23.1 against a nominal 32**.
An earlier version of this section inferred from the smaller variance that the
Bonferroni lower limits must be conservative. **That does not follow from a
variance**, and §15 computes the quantity the argument actually needs,
$\Pr\{v_{L,c}^2\le D_c\ \forall c\}$, directly — where it holds at the median
and **fails badly at a tail quantile**.

At the tail quantile the ratio $\nu\widehat D_c/D_c$ is undefined because the
exact design variance is occasionally **zero**: $\Pr(D_c=0)=2\times10^{-5}$ and
$\Pr(\widehat D_c=0)=0.13$–$0.21$ percent. A proportion in the tail of a small
finite population with ten-unit clusters genuinely has zero within-stratum
spread sometimes. No variance model covers that case.

**And $\widehat D_c$ is correlated with $Y_c$ at 0.80 to 0.84** at the tail
quantile, against 0.00 at the median. This is the violation `exp09` §7.1 flagged
as the one specific to a CDF ordinate, now realised: the design variance of a
proportion is a function of the proportion, and near the median that function is
flat while in the tail it is not.

### X3 — the oracle band covers, so the problem is not variance estimation

| $K$ | $t_0$ | nominal | oracle coverage |
|---|---|---|---|
| 60 | median | 0.9508 | 0.9495–0.9590 |
| 60 | 0.15 | 0.9508 | 0.9490–0.9515 |
| 200 | median | 0.9502 | 0.9490–0.9495 |
| 200 | 0.15 | 0.9502 | 0.9420–0.9425 |

Monte Carlo error 0.0067. The oracle band — true $A$, true $D_c$,
per-population standardisation — reproduces the rank guarantee to within about
one standard error, the two $K=200$ tail cells running 1.2 standard errors low.
**No detectable undercoverage of the oracle band at this nominal level, in these
conditions.** That is not a check of assumption (S): coverage at one nominal
level does not verify a common standardised shape, since different laws can
agree at one quantile, and here the sampling error is small enough that observed
and latent are close in any case. What it does establish is that in these
conditions the shape problem is not distorting coverage, so the machinery
downstream is not being asked to repair a broken target.

### X4 — the pivot holds; the bootstrap fails exactly where the dependence is

| $K$ | $t_0$ | $\sigma_\alpha$ | $A_U$ pivot | $A_U$ pivot, mean fitted | **$A_U$ percentile** | band: piv | band: pct | band: pct-normal |
|---|---|---|---|---|---|---|---|---|
| 60 | median | 0.2 | 0.990 | 0.990 | 0.952 | 0.952 | 0.952 | 0.985 |
| 60 | 0.15 | 0.2 | 0.953 | 0.946 | **0.852** | 0.955 | 0.955 | 0.966 |
| 200 | median | 0.6 | 0.998 | 0.999 | 0.984 | 0.962 | 0.962 | 0.978 |
| 200 | 0.15 | 0.6 | 0.978 | 0.973 | **0.866** | 0.949 | 0.949 | 0.961 |

The pivot limit's realised coverage is **0.953–0.998**, and the mean-fitted form
gives 0.946–0.999; the guaranteed level is 0.95 and the Monte Carlo error is
about 0.005 at these rates, so a point estimate of 0.953 or 0.946 is evidence of
behaviour near the target, **not evidence that the true coverage is at or above
it**. What is defensible: no clear undercoverage was observed, including in the
cells where normality is decisively rejected. Fitting the mean costs 0.001–0.007
and leaves the band unchanged to three decimals.

**The percentile bootstrap limit fails at the tail quantile**, 0.852–0.908
against a nominal 0.975, while holding at 0.952–0.984 at the median. A strong
estimate--variance-estimate association and the undercoverage were observed
**together**; a GVF built from $\widehat F_c(1-\widehat F_c)$, a function of the
estimate itself, is a plausible failure path. It is not an established cause:
the tail cells also change the skewness, the rate of boundary values and the
distribution of the variance estimator at once. The reported correlation was
also pooled over populations and replicates, mixing the between-population
relation between the true $D_c$ and the true $F_c$ with the within-population
sampling dependence; §15 separates them.

Every band covers at 0.947 or above against the guaranteed 0.90. Containment of
the oracle half-width is 1.000 for the pivot and 0.9995–1.0000 for the
percentile band.

### X5 — the width ordering reverses again, and the elasticity says why

Width over the oracle band: pivot **1.009–1.078**, percentile 1.009–1.073,
normal on the same limit **1.114–1.198**. So the conformal band is 10 to 12
percent narrower than the normal interval here — the reverse of §13, where the
normal interval won.

The reason is the operating point. $\bar D/A$ is **0.038 to 0.126** in this
design, so the elasticity $L_c/\{2(A+L_c)\}$ is 0.02 to 0.06 rather than the
0.20–0.36 of §13. The conformal band barely moves with the scale limit while the
normal interval moves at elasticity $1/2$. **Which construction is narrower is
decided by the design share, and neither dominates** — the third time this has
come up and the first time it has been seen at both ends.

### The limitation that matters most for the manuscript

**This design sits at a low design share.** $\rho^2=\bar D/(A+\bar D)$ is 0.037
to 0.112, which is the manuscript's *national* ESS regime ($\rho\approx0.1$) and
**not** its regional one ($\rho\approx0.5$ to $0.66$, i.e. $\rho^2$ from 0.25 to
0.44). Where the correction is nearly inactive, a band that adds 1 to 8 percent
over the oracle is not a demanding test. Reaching a regional-like design share
needs the between-population spread reduced or the sample cut, and that has not
been run.

So the defensible statement is: **in a stratified cluster design at a national-
like design share, with normality and the $\chi^2$ variance law both measurably
violated, the fixed procedure's scale limit held its guaranteed level and its
band covered, at 1 to 8 percent over the infeasible oracle.** The regional
regime is the next cell, and the alternative construction already has a located
failure to carry into it.

---

## 15. The regional design share: the procedure holds, and recovers a quarter of what it is for

`exp18`, protocol `docs/PROTOCOL_exp18_regional_share.md`, results
`results/exp18_regional_share.csv`. 16 cells, 2,000 replicates, $B=500$,
$\sigma_\alpha=0.4$ throughout. Procedures and budget unchanged from `exp16`.

### Two routes to the same design share, and they are not the same problem

| route | $(m,n)$ | $\nu$ | $\bar D/A$ | oracle scale factor | skew (tail) | $\Pr(\widehat D_c=0)$ (tail) |
|---|---|---|---|---|---|---|
| `small_sample` S1 | (3,4) | 8 | 0.203 / 0.274 | 0.912 / 0.886 | 0.88 | 3.6% |
| `small_sample` S2 | (2,2) | 4 | 0.549 / 0.754 | 0.804 / 0.755 | 0.71 | **20.9%** |
| `low_signal` S1 | (5,10) | 16 | 0.204 / 0.272 | 0.911 / 0.887 | 0.46 | 0% |
| `low_signal` S2 | (5,10) | 16 | 0.544 / 0.757 | 0.805 / 0.755 | 0.20 | 0% |

These design shares are $\rho=0.41$ to $0.66$, **the manuscript's regional
range**. The oracle correction is worth 8.8 to 24.5 percent of width here, so
the test is now a real one.

**Y1 holds.** At matched $\bar D/A$ the routes differ in everything that is not
the design share: degrees of freedom 4 or 8 against 16, tail skewness 0.7–0.9
against 0.2–0.5, and a fifth of all variance estimates exactly zero against
none. Reporting one route as if it stood for the other would have been the error
this split exists to prevent.

### The diagnostic `exp17` got wrong

$\Pr\{v_{L,c}^2\le D_c\ \text{for all }c\}$, against the $1-\eta_2=0.975$ the
containment argument requires:

| route | $t_0$ | $K=60$ | $K=200$ |
|---|---|---|---|
| `small_sample` S1 | median | 1.0000 | 0.9990 |
| `small_sample` S1 | 0.15 | **0.8340** | **0.7205** |
| `small_sample` S2 | 0.15 | **0.7175** | **0.4450** |
| `low_signal` S2 | 0.15 | 0.9955 | 0.9980 |

**The simultaneous lower limits fail at a tail quantile on the small-sample
route**, on more than half of replicates in the worst cell. `exp17` inferred
their conservatism from a variance smaller than $\chi^2$; that inference was
wrong in exactly the cells that matter. The mechanism is visible in the $K$
dependence: Bonferroni sets each limit at $\eta_2/K$, so a larger $K$ pushes
further into a $\chi^2$ tail that does not describe the estimator, and coverage
**falls** as $K$ grows — 0.72 at $K=200$ against 0.83 at $K=60$.

The correlation decomposes as the review said it must: the pooled figure of 0.8
in `exp17` is a **between-population** relation of 0.78–0.95 between the true
$D_c$ and the true $F_c$, plus a **within-population** sampling dependence of
0.52–0.67. Both are real and they are different objects.

### Y2 holds, Y4 nearly

Latent-target coverage of the pivot band is **0.9615–0.9860** against a
guaranteed 0.90, on both routes, including the cells where the containment
argument's premise fails on half the replicates. Again: stability, not validity.

The oracle band covers at 0.9315–0.9605 against a nominal 0.950. The worst is
`small_sample` S2 at the tail quantile with $K=200$: **0.9315, 2.8 Monte Carlo
standard errors low.** That is a detectable shortfall, it is on the harsh route
at the tail, and **no variance-limit work can address it** — the oracle uses the
true $A$ and the true $D_c$. It is the first sign in this project of the target
itself failing, and it belongs with `exp01` rather than here.

### Y3 fails, and this is the finding

| route | level | $t_0$ | uncorrected / oracle | pivot / oracle | **pivot / uncorrected** | share of the available narrowing captured |
|---|---|---|---|---|---|---|
| `small_sample` | S1 | median | 1.072 | 1.061 | **0.990** | 15% |
| `small_sample` | S2 | median | 1.195 | 1.181 | **0.988** | **7%** |
| `small_sample` | S2 | 0.15 | 1.495 | 1.404 | **0.940** | 19% |
| `low_signal` | S1 | 0.15 | 1.139 | 1.097 | **0.963** | 31% |
| `low_signal` | S2 | median | 1.237 | 1.177 | **0.951** | 25% |
| `low_signal` | S2 | 0.15 | 1.326 | 1.238 | **0.934** | 27% |

**The valid corrected band is 0.9 to 6.6 percent narrower than not correcting at
all**, and captures **6 to 31 percent** of the narrowing the oracle achieves.

The mechanism is the guarantee itself. The band factor is
$\{1+v_{L,c}^2/A_U\}^{-1/2}$: the argument needs $A$ bounded **above** and each
$v_c$ bounded **below**, and both bounds drive that factor toward 1, which is no
correction at all. The two conservatisms do not offset — they compound in the
same direction.

This bears directly on the manuscript. Section 6.5 reports the correction
narrowing the band by 15 to 19 percent where it activates. At `low_signal` S2,
median, the oracle narrowing is 19.5 percent — the same figure — and **the
feasible, honestly-bounded band achieves 4.9 percent of width, a quarter of it.**
The manuscript's number is an oracle-like quantity computed with plug-in scales;
the price of making it a statement with an error budget is most of the gain.

Protocol outcome 2, and it must be reported as prominently as a success would
have been: **at the design share where the correction is needed, the valid
procedure is valid and worth little.** Whether a construction exists that keeps
the guarantee and recovers more of the 6 to 31 percent is now the open question,
and it is a better question than the one this project started with.

### What is still not established

The pivot's guarantee is not shown to hold here and cannot be — its conditions
fail measurably, and one of them, $E_D$, fails on up to 56 percent of replicates
while the procedure nonetheless behaves. Coverage point estimates near the
target are not proof of coverage at the target. The oracle shortfall at the tail
on the harsh route is unexplained. And nothing here is the multi-coordinate
simultaneous problem the manuscript's actual band requires.

---

## 16. Headroom: where the width is lost, and what a joint set could buy

`exp19`, protocol `docs/PROTOCOL_exp19_headroom.md`, results
`results/exp19_headroom.csv`. **No method proposed.** The same band function
$R(A,\mathbf D)$ evaluated at mixed arguments on the `exp18` cells with the
largest design share ($\bar D/A=0.54$ and $0.75$), 2,000 replicates, same seeds.

| route | $t_0$ | $K$ | uncorrected | bound $A$ only | bound $\mathbf D$ only | current | no multiplicity |
|---|---|---|---|---|---|---|---|
| `low_signal` | median | 200 | 1.237 | 1.079 | 1.141 | 1.177 | 1.142 |
| `low_signal` | 0.15 | 200 | 1.326 | 1.115 | 1.179 | 1.238 | 1.189 |
| `small_sample` | median | 200 | 1.195 | 1.074 | 1.170 | 1.181 | 1.165 |
| `small_sample` | 0.15 | 200 | 1.495 | 1.169 | 1.332 | 1.404 | 1.315 |

All as width over the oracle band.

**Z1 holds.** Bounding the design variances costs more than bounding $A$ —
0.136–0.332 against 0.074–0.204 — in every cell.

**Z2 fails in its important half.** The multiplicity is only **6 to 22 percent**
of the current loss. It does grow with $K$ as predicted (0.14 to 0.20, 0.15 to
0.21, 0.06 to 0.08, 0.16 to 0.22 from $K=60$ to $200$), but it is a minor part
of the total.

**Z3 holds, and it is the answer.** Removing the simultaneity correction
entirely — an invalid procedure whose lower limits then cover on 0.0005 to 0.76
of replicates — raises the captured share of the oracle narrowing only from
**6–27 percent to 12–42 percent**. Most of the gap survives.

**What this decides about the joint-inference candidate.** Replacing the
simultaneity treatment alone, in the constructions compared here, roughly doubles
the captured fraction and leaves more than half the gap; and bounding $A$ alone,
*with the true $D_c$ supplied*, already costs 7 to 20 percent. **So a candidate
that only replaces the simultaneity treatment is not the one to build.** This is
a diagnostic that orders the design options, **not an upper bound on what any
valid joint inference could achieve**: the components interact, and an invalid
procedure with the multiplicity removed is not guaranteed to be narrower than
every valid joint construction. One that bounds the band factor $v_c^2/A$ as a single object — the
structure the scalar $\kappa$ pivot of §2 had, and which the separate-bounds
construction destroys — addresses both losses at once and is the version worth
designing.

### The observation that reframes the design target

The band's realised coverage is 0.974 to 0.986 against a guaranteed 0.90 **even
when the lower limits cover on 0.05 percent of replicates.** The chain of
sufficient conditions is so slack that violating one of them almost surely
leaves the coverage essentially unchanged.

So the width is not being spent on the coverage the construction achieves. It is
being spent on a sufficient-condition argument each link of which is loose:
oracle rank slack, the $A_U$ bound, the $v_L$ bounds, and their composition.
**The design target for the next step should therefore be a construction that
spends its error budget on one direct statement rather than reaching the same
coverage through a chain of separately conservative bounds.** Two things must
not be confused here: *reducing theoretical conservatism*, by a more direct test
or joint inference that uses the budget efficiently, is a validity argument;
*tuning the width down until the realised coverage sits at 0.90* on a particular
generative model is not. Only the first is a contribution. Over-coverage in some
conditions is acceptable and expected — the aim is to remove unnecessary width
while keeping validity, not to hit 0.90 everywhere.

---

## 17. Bounding the ratio directly: the exact case

`exp20`, protocol `docs/PROTOCOL_exp20_ratio_pivot.md`, specification
`docs/THEORY_ratio_pivot.md`. Model R — $Y_c\sim N(0,A+d\,a_c)$ with $a_c$ a
**known** relative variance structure — 16 cells, 20,000 replicates,
$\eta=\alpha_0=0.05$, guaranteed 0.90.

The design sketch that preceded this contained an error, corrected in the
specification §0: it proposed reducing a general heteroscedastic model to one
axis by holding $\widehat D_c$ fixed, which is substituting the estimate for the
parameter. Model R is the heteroscedastic model in which the reduction is
**true** rather than assumed, and $a_c$ is generated as a design quantity, never
fitted to $\widehat D_c$.

### 1. Level, read first

$T(t)=K\widehat d/\{t\,S(t)\}\sim F_{\nu,K}$ exactly, and inverting it gives
$\Pr\{t\ge t_L\}$ of **mean 0.9498, range 0.9465–0.9538** against a nominal 0.95
at a Monte Carlo error of 0.0015. The inversion set was never empty and no
$\widehat D_c$ was zero in this model.

The incumbent's two components: $\Pr\{A\le A_U\}=0.998$–$1.000$ against 0.975,
and $\Pr\{v_{L,c}^2\le D_c\ \forall c\}=0.973$–$0.978$ against 0.975. So the
incumbent's $A$-limit spends almost none of its budget while the ratio limit
spends all of it — on the only quantity the band depends on.

### 2. Containment

$\Pr\{R(t_L)\ge R(t)\}$ equals $\Pr\{t\ge t_L\}$ to **machine zero** in every
cell, which is the monotonicity of $R$ in $t$ made visible: for this
construction, containment and level are the same event, and there is nothing
lost between them. The incumbent's containment is 1.000, which is not an
advantage — it is the same over-conservatism showing up as a wasted budget.

### 3. Width, with coverage beside it

| $K$ | $d/A$ | $\nu$ | $\sigma_{\log a}$ | oracle cov. | ratio cov. | sep. cov. | ratio/oracle | sep/oracle | **ratio/sep** |
|---|---|---|---|---|---|---|---|---|---|
| 60 | 0.5 | 8 | 0.5 | 0.952 | 0.961 | 0.978 | 1.063 | 1.187 | **0.897** |
| 60 | 1.0 | 8 | 0.5 | 0.953 | 0.968 | 0.990 | 1.116 | 1.348 | **0.831** |
| 200 | 0.5 | 16 | 1.2 | 0.950 | 0.955 | 0.973 | 1.027 | 1.150 | **0.895** |
| 200 | 1.0 | 16 | 1.2 | 0.952 | 0.960 | 0.986 | 1.047 | 1.262 | **0.832** |

Every arm covers the latent target at 0.955 or above against a guaranteed 0.90.

**The ratio band is 9 to 20 percent narrower than the incumbent**, and sits 2.6
to 11.6 percent over the infeasible oracle where the incumbent sits 15.0 to 34.8
percent over it.

In the units that matter — the share of the available narrowing actually
captured:

| construction | captured |
|---|---|
| separate bounds (the incumbent) | **18–38 %** |
| **ratio bound** | **73–89 %** |

That is protocol outcome 1. `exp18` found the incumbent valid and worth little
at the regional design share; **in the exact case, bounding the ratio directly
recovers most of what was being lost, under correct error control.**

### 4. Where the gain comes from

Mean ratio-to-incumbent width by factor: $K=60$ 0.870 against $K=200$ 0.850;
$d/A=0.5$ 0.894 against $d/A=1.0$ 0.826; $\nu=8$ 0.851 against $\nu=16$ 0.869;
dispersion of $a_c$ 0.859 against 0.861.

So the gain grows with $K$ and, much more, with the **design share** — the two
things that make the incumbent's two-sided conservatism expensive. It is
essentially **flat in the dispersion of $a_c$**, which prediction V4 had wrong:
the Bonferroni step is not charging for heterogeneity so much as for the
existence of $K$ separate limits at all.

### 5. What this does not establish

$a_c$ is known. **That is the whole reduction**, and the specification says so:
this is an exact reference case and a verification of the construction, not a
survey-ready method and not, by itself, a contribution. Whether the gain
survives when the relative structure must be estimated — specification §3, route
(b), where `exp13`'s finding that GVF misfit returns most of the gain is the
standing warning — is the question that decides this line. Nothing here is a
general heteroscedastic result, and $\mathbf D$ was never profiled.

---

## 18. Matched information, and paying for the structure

`exp21`, protocol `docs/PROTOCOL_exp21_estimated_structure.md`. 16 cells,
10,000 replicates, $\gamma_0=1$, total budget $\alpha_0+0.05=0.10$ for every arm.
Correctly specified and misspecified blocks are reported separately and never
averaged.

**An implementation error found and fixed before reading anything.** A dictionary
key collision overwrote the confidence-set coverage of $C_\gamma$ with the
latent-target coverage of the band built from it. The first run's "$C_\gamma$
coverage of 0.956–0.972" was therefore not that quantity at all. Corrected, and
the interval was verified in isolation at 200,000 draws (0.9746 against 0.975)
before the rerun.

### The confidence set for the structure

$W(\gamma)$ is linear and increasing in $\gamma$, so
$C_\gamma=[\widehat\gamma\pm w\sigma_\epsilon/\sqrt{S_{xx}}]$ in closed form,
$\widehat\gamma=-S_{xD}/S_{xx}$, with $w$ the quantile of a null law that depends
on neither $d$ nor $\gamma$. **U1 holds:** realised coverage 0.9716–0.9777, mean
**0.9752**, against a nominal 0.975 at Monte Carlo error 0.0016. The
supremum over $C_\gamma$ was insensitive to the grid — 31 against 61 points gave
a mean width ratio differing by $0.0000$ — and the inversion set was never empty,
so the corrected fallback $t_L=0$ was never exercised.

### U2 and U3: the gain is pooling, not direct ratio inference

Share of the available narrowing captured, correctly specified:

| $K$ | $d/A$ | $\nu$ | incumbent | **+ known structure** | **+ direct ratio** | plug-in $\widehat\gamma$ | **$C_\gamma$** |
|---|---|---|---|---|---|---|---|
| 60 | 0.5 | 8 | 0.210 | **0.640** | 0.751 | 0.750 | 0.633 |
| 60 | 1.0 | 16 | 0.283 | **0.662** | 0.757 | 0.756 | 0.669 |
| 200 | 0.5 | 16 | 0.308 | **0.797** | 0.856 | 0.856 | 0.799 |
| 200 | 1.0 | 8 | 0.221 | **0.782** | 0.852 | 0.852 | 0.791 |

**U2 holds decisively and U3 largely fails.** Giving the incumbent the same known
$a_c$ — one exact lower limit for the common $d$, no Bonferroni — moves it from
capturing 0.20–0.31 to **0.63–0.80**. The last row of the table should also be
read the other way: **the method that must estimate the structure lands where the
method given it already sat.** Equal ranges across cells are not equality within
them, so §19 repeats the comparison paired on the same replicates. Bounding the ratio directly then adds
0.06–0.11 more, a width ratio of **0.958–0.987**: between 1.3 and 4.2 percent.

So the 9–20 percent of §17 decomposes into **pooling, which is nearly all of it,
and direct ratio inference, which is a few percent.** The review asked for this
separation before the contribution was named, and it changes what the
contribution is.

### U4: paying for the structure costs back the ratio step

$C_\gamma$ containment is **0.983–0.986** against its $1-\eta_\gamma-\eta_t=0.95$
requirement — valid and conservative — and its captured share is **0.63–0.80**,
which is where `sep_struct` already sits and below `ratio_known`'s 0.74–0.86.
Against the incumbent its band is **0.817–0.926**, i.e. 7 to 18 percent narrower.

**The direct-ratio gain and the price of estimating the structure are of the same
size**, so the deliverable improvement over the incumbent is, to a good
approximation, the value of exploiting a variance structure at all.

### U5, U6: what the structure assumption costs when it is wrong

Under correct specification the plug-in $a_c(\widehat\gamma)$ departs little
from its requirement — containment 0.944–0.949 against 0.95, which is below it
and by more than Monte Carlo error at 10,000 replicates, so "fine" would be too
strong; U5's prediction that it undercovers *generally* is nonetheless wrong.
Under misspecification it fails outright: containment falls to **0.821–0.898**.
The $C_\gamma$ construction degrades more gracefully but still fails,
**0.899–0.964**, below its 0.95 requirement in half the cells, while
`ratio_known` (given the true $a_c$) holds at 0.948–0.955 and the incumbent, which
assumes no structure at all, stays at 1.000.

**U6 holds, and the reason must be stated as model error rather than estimation
error.** $C_\gamma$ answers "how precisely was $\gamma$ estimated". When the true
$\mathbf D$ lies outside the family $\{d\,a_c(\gamma)\}$ there is no $\gamma_0$
to cover, so a correct confidence set for $\gamma$ confers no protection at all.
**Reflecting the estimation uncertainty of a structure parameter does not protect
against the structure model being wrong.** That is the condition to report with
the gain rather than after it: the improvement is conditional on a correctly
specified relative variance structure, and where that fails the construction
loses containment while the incumbent, which assumes no structure, does not.

### Where this leaves the line

Protocol outcome 2. The contribution is not "bounding the ratio directly";
measured against a construction given the same information, that is worth a few
percent. It is **using a relative variance structure, with its estimation
uncertainty paid for by a confidence set rather than removed by substitution,
which takes the captured share from 0.20–0.31 to 0.63–0.80 and the band to 7–18
percent narrower than the incumbent — conditional on the structure being right.**

That is a smaller and different claim than the one §17 pointed toward, it is
stated in the terms the evidence supports, and the failure mode is measured
rather than assumed. What it is not yet: anything under a complex design, where
neither the $\chi^2$ law for $\widehat D_c$ nor the normality of $Y_c$ holds, and
where `exp18` found the incumbent's own lower limits failing at 0.445.

---

## 19. Completing route (b): the algorithm, and the matched comparison

`exp22`, protocol `docs/PROTOCOL_exp22_completion.md`. 16 cells, 10,000
replicates, total budget $\alpha_0+\eta=0.10$ for every arm; the component-wise
arm splits its $\eta$ three ways and the ratio arm two. Route (a) not opened.

### Job 1 — the supremum becomes two evaluations

> **Lemma.** $\partial_\gamma\log a_c(\gamma)=\bar\ell(\gamma)-\log x_c$ where
> $\bar\ell(\gamma)$ is the mean of $\log x$ under weights $\propto x^{-\gamma}$,
> and $\bar\ell'(\gamma)=-\mathrm{Var}_w(\log x)\le0$. So $\log a_c$ is concave
> in $\gamma$ for every $c$, and its minimum over $[\gamma_L,\gamma_U]$ is
> attained **at an endpoint, exactly.**

With $R$ decreasing coordinatewise in $t\,a_c$, that gives the certified envelope
$\bar R=\operatorname{ord}_m\{|Y_c|/\sqrt{1+\underline t\,\underline a_c}\}$ with
$\underline a_c=\min\{a_c(\gamma_L),a_c(\gamma_U)\}$, which dominates
$R(t_L(\gamma),\gamma)$ for **every** $\gamma\in C_\gamma$ and not only for the
grid points. Measured: $\bar R\ge$ the grid maximum on **100 percent** of
replicates, at a width cost of **0.5 to 1.9 percent**.

The one step not proved was $\underline t=\inf_\gamma t_L(\gamma)$. Its grid
minimiser landed at an endpoint on 0.9999 to 1.0000 of replicates, and this
section originally used a two-endpoint evaluation on that basis. **That is
retracted: §20 reproduces a counterexample in which the infimum is interior and
16.9 percent below the smaller endpoint.** The endpoint property is proved for
$a_c(\gamma)$ and does not transfer to $t_L(\gamma)$. §20 replaces the endpoint
evaluation with a certified global lower bound and restates every width figure
in this section at the certified cost.

### The three probabilities, side by side

Correctly specified, printed together after the `exp21` key collision:

| $K$ | $d/A$ | $\nu$ | $\Pr\{\gamma_0\in C_\gamma\}$ | envelope containment | component containment | envelope T2 | component T2 | oracle T2 |
|---|---|---|---|---|---|---|---|---|
| 60 | 0.5 | 8 | 0.9775 | 0.9954 | 0.9988 | 0.9640 | 0.9655 | 0.9470 |
| 60 | 1.0 | 16 | 0.9750 | 0.9936 | 0.9981 | 0.9750 | 0.9784 | 0.9517 |
| 200 | 0.5 | 16 | 0.9727 | 0.9931 | 0.9975 | 0.9601 | 0.9620 | 0.9505 |
| 200 | 1.0 | 8 | 0.9742 | 0.9948 | 0.9985 | 0.9672 | 0.9705 | 0.9502 |

Requirements: 0.975, 0.95, 0.95, 0.90, 0.90, 0.95. All met.

### Job 2 — matched, with both sides estimating the structure

Paired on the same replicates:

| $K$ | $d/A$ | $\nu$ | ratio / component | **envelope / component** | envelope captured | component captured | incumbent captured |
|---|---|---|---|---|---|---|---|
| 60 | 0.5 | 8 | 0.978 | **0.988** | 0.590 | 0.530 | 0.205 |
| 60 | 1.0 | 8 | 0.963 | **0.981** | 0.609 | 0.555 | 0.227 |
| 200 | 0.5 | 16 | 0.987 | **0.992** | 0.778 | 0.741 | 0.303 |
| 200 | 1.0 | 16 | 0.977 | **0.987** | 0.780 | 0.745 | 0.306 |

**P3 holds with a small gap.** After certification the ratio construction is
**0.7 to 2.3 percent** narrower than the component-wise construction given the
same information and the same total budget. Both capture 0.53 to 0.78 of the
available narrowing where the structure-free incumbent captures 0.20 to 0.31.

So the matched comparison confirms what `exp21` implied: **the substance is
using a variance structure and paying for it; the ratio formulation is a
refinement worth one or two percent.**

### Choosing the main method, on provability rather than width

| | ratio envelope | component-wise |
|---|---|---|
| budget pieces | **2** ($\eta_\gamma,\eta_t$) | 3 ($\eta_\gamma,\eta_1,\eta_2$) |
| bounds to justify | $C_\gamma$, one $F$ pivot, endpoint lemma | $C_\gamma$, $\chi^2$ for $d$, $\chi^2_K$ for $A$ |
| unproved step | $\inf_\gamma t_L$ | the same $\sup_\gamma$ |
| width | **best** | 0.7–2.3% wider |
| **containment under misspecification** | 0.930–0.981 | **0.958–0.992** |

**The ratio envelope is fixed as the main method**: fewer budget pieces, a
shorter chain, and — as §20 establishes — the form for which a conservative
computational bound has been obtained; none has been built for the
component-wise form, which is not the same as none existing. The component-wise version
is retained and reported, because it degrades more gracefully when the structure
family is wrong — a real reason to prefer it that the width comparison does not
show.

### Misspecification: model error, not estimation error

Containment under a structure outside the family: envelope **0.930–0.981**,
below its 0.95 requirement in three of eight cells; component-wise 0.958–0.992;
incumbent 1.000. Latent-target coverage nonetheless stays at 0.960–0.977 for
both against the guaranteed 0.90, so the failure is in the propagation step and
is absorbed by slack downstream — which is not something to rely on.

$C_\gamma$ answers how precisely $\gamma$ was estimated. If no $\gamma$ describes
the truth there is nothing for it to cover. **A confidence set for a structure
parameter is not protection against the structure family being wrong**, and the
gain is conditional on that family, stated with the gain.

### Next

The main method is fixed. It goes to the two complex-survey routes of `exp18` —
the small-sample route and the low-signal route, which differ at matched $D/A$
in degrees of freedom, zero-variance rate and estimate–variance dependence — to
answer whether the structure model describes real design-variance patterns and
whether the gain survives in T2 coverage and width.

---

## 20. The certified envelope, and a retracted endpoint claim

`exp23`, protocol `docs/PROTOCOL_exp23_certified.md`. Same generation and seeds
as `exp22`, 16 cells, 10,000 replicates.

### The retraction

§19 evaluated $\inf_{\gamma\in C_\gamma}t_L(\gamma)$ at the two endpoints,
because the grid minimiser landed there on 0.9999–1.0000 of replicates. **A
counterexample supplied in review reproduces exactly.** With $K=6$, $\nu_c=8$,
$C_\gamma=[-0.59651,\,0.34495]$ and the tabulated $(x_c,Y_c^2,\widehat D_c)$:

| evaluation | $\gamma$ | $t_L(\gamma)$ |
|---|---|---|
| left endpoint | $-0.59651$ | 0.10974 |
| **interior** | $\mathbf{-0.18321}$ | **0.09121** |
| right endpoint | $0.34495$ | 0.12106 |

The smaller endpoint is **20.3 percent above** the interior minimum. The
endpoint property is proved for $a_c(\gamma)$, whose logarithm is concave in
$\gamma$; $t_L(\gamma)$ is a different function — the solution of an $F$
inversion in which the variance estimates and the observations both enter — and
the property does not transfer. A rate of 0.9999 was never a theorem, and the
remaining $10^{-4}$ is precisely what a universal claim needs.

### The certified bound, which needs no endpoint claim

$\Phi(t;\gamma)=\sum_c t Y_c^2/\{1+t\,a_c(\gamma)\}$ is increasing in $t$ and
decreasing in each $a_c$, and $t_L(\gamma)$ solves $\Phi=K\widehat d(\gamma)/q$.

1. $\underline a_c=\min\{a_c(\gamma_L),a_c(\gamma_U)\}$ is **exact** by the
   concavity lemma, so $\bar\Phi(t)=\sum_c tY_c^2/(1+t\underline a_c)\ge
   \Phi(t;\gamma)$ for every $\gamma\in C_\gamma$.
2. $1/a_c(\gamma)=K^{-1}\sum_j(x_c/x_j)^{\gamma}$ is a positive sum of
   exponentials, hence **convex in $\gamma$**, and so is $\widehat d(\gamma)$.
   **A value returned by an optimiser is not a lower bound**, so the
   implementation does not use one: $\widehat d'$ is increasing by convexity, so
   its sign at the endpoints decides whether the minimum is at $\gamma_L$ or
   $\gamma_U$ — in which case $\underline d$ is *exact* — and otherwise a
   bisection on $\widehat d'$ brackets the minimiser, with the supporting line at
   the bracket's left end giving
   $\underline d\ \ge\ \widehat d(b_L)+\widehat d'(b_L)(b_U-b_L)$. Every
   returned quantity is shrunk by a relative $10^{-9}$ for rounding, and the
   monotone inversion returns its **lower** bracket end rather than the midpoint.
   Verified: zero violations over 400 stress configurations, tightness median
   0.941 and 5th–95th percentiles 0.797–0.990 — the same tightness the
   uncertified ternary version had.
3. Hence for every $\gamma\in C_\gamma$,
   $\bar\Phi(t_L(\gamma))\ge\Phi(t_L(\gamma);\gamma)=K\widehat d(\gamma)/q\ge
   K\underline d/q$, and $\bar\Phi$ increasing gives
   $$t_L(\gamma)\ \ge\ \underline t_{\mathrm{cert}}=\bar\Phi^{-1}\!\big(K\underline d/q\big).$$

**Verified before use.** On the counterexample the bound gives 0.08924 against a
true infimum of 0.09121. Over 300 random configurations with a 401-point
reference grid at relative tolerance $10^{-9}$: **zero violations**; tightness
$\underline t_{\mathrm{cert}}/\inf t_L$ has median 0.941 and 5th–95th percentiles
0.796–0.990. (A coarser first pass at 3,000 cases showed one apparent violation
that did not survive a finer reference grid; recorded as an artefact of the
reference, not of the bound.)

It is also **cheaper** than the retracted grid: two structure evaluations, one
convex minimisation, one monotone inversion, against 31 $F$ inversions.

### The numbers, restated at the certified cost

**C1.** The certified envelope dominates the retracted grid computation on
**100 percent** of replicates in every cell. **C2.** It costs
**0.7 to 2.9 percent** of width against that grid computation — more than §19's
0.5–1.9 percent, as it must, since $\underline t_{\mathrm{cert}}$ lies below the
true infimum. The $\underline t=0$ fallback was never used.

Correctly specified, the three probabilities side by side:

| $K$ | $d/A$ | $\nu$ | $\Pr\{\gamma_0\in C_\gamma\}$ | certified containment | latent-target coverage | oracle |
|---|---|---|---|---|---|---|
| 60 | 0.5 | 8 | 0.9775 | 0.9978 | 0.9645 | 0.9470 |
| 60 | 1.0 | 16 | 0.9750 | 0.9974 | 0.9767 | 0.9517 |
| 200 | 0.5 | 16 | 0.9727 | 0.9955 | 0.9608 | 0.9505 |
| 200 | 1.0 | 8 | 0.9742 | 0.9983 | 0.9686 | 0.9502 |

Levels were derived in the restricted model; the simulated values agree with
them within Monte Carlo uncertainty (0.0016 near 0.975, 0.0021 near 0.96). The
containment at 0.995–0.999 against a 0.95 requirement, with latent-target
coverage at 0.96 against a guaranteed 0.90, shows conservatism still remaining
in the chain.

Width, paired on the same replicates:

| $K$ | $d/A$ | $\nu$ | certified / component | certified / incumbent | **captured: certified** | component | incumbent |
|---|---|---|---|---|---|---|---|
| 60 | 0.5 | 8 | 0.991 | 0.928 | **0.574** | 0.530 | 0.205 |
| 60 | 1.0 | 16 | 0.987 | 0.894 | **0.615** | 0.578 | 0.290 |
| 200 | 0.5 | 16 | 0.994 | 0.908 | **0.768** | 0.741 | 0.303 |
| 200 | 1.0 | 8 | 0.994 | 0.835 | **0.740** | 0.723 | 0.226 |

**C3 and C4 hold.** The certified construction captures **0.574 to 0.768** of the
available narrowing where the structure-free incumbent captures **0.205 to
0.306**, and its band is **6.5 to 16.5 percent narrower** than the incumbent. It
remains 0.4 to 1.5 percent narrower than the component-wise construction —
which is itself still computed on a grid and is **not certified**, since its band
depends on $\gamma$ through $d_L(\gamma)$, $a_c(\gamma)$ and $A_U(\gamma)$ at
once and admits no analogous bound.

**That is now the stronger reason for the main-method choice**, stated at the
right scope: among the constructions implemented and examined here, the ratio
form is the one for which a conservative computational bound over a continuous
structure confidence set has been obtained. **That no such bound has been built
for the component-wise form is not evidence that none exists**, and the sentence
must not be read that way.

### Misspecification, unchanged in direction

Containment under a structure outside the family: certified **0.941–0.989**,
below its requirement in one of eight cells; component-wise 0.958–0.992;
structure-free incumbent 1.000. Latent-target coverage holds at 0.961–0.976
against the guaranteed 0.90. The conclusion stands as stated in §19 — a
confidence set for $\gamma$ is not protection against the family being wrong.

### What is now owed

Nothing on the computation: the supremum is bounded rather than searched. What
remains is the complex-survey step, which `exp18`'s two routes are already built
for.

---

## 21. The fixed method under a complex design

`exp24`, protocol `docs/PROTOCOL_exp24_survey_structure.md`. 16 cells, 2,000
replicates, `exp18`'s two routes preserved. Populations were given different
numbers of sampled PSUs so that an exogenous structure variable exists:
$x_c=m_c$, **fixed before running and not reselected afterwards**. Budget
$\alpha_0=0.05$, $\eta_\gamma=\eta_t=0.025$, fixed in advance.

A sign error in one diagnostic — comparing $[\gamma_L,\gamma_U]$ against the
regression *slope* rather than against $\gamma_{\mathrm{ls}}=-\text{slope}$ —
was found and fixed before any of this was read. It affected only that
diagnostic.

### 1. How much does the structure family explain?

| route | $t_0$ | $\bar D/A$ | $\nu_c$ | $R^2$ of $\log D_c$ on $\log x_c$ | $\gamma_{\mathrm{ls}}$ (sd) | residual sd | $\mathrm{corr}(\widehat D_c,Y_c)$ |
|---|---|---|---|---|---|---|---|
| S1 | median | 0.053 | 12–28 | **0.63–0.67** | 1.41 (0.07–0.15) | 0.24 | 0.00 |
| S1 | 0.15 | 0.067 | 12–28 | **0.17–0.21** | 1.39–1.56 (1.2–3.2) | 0.84–1.09 | **0.68–0.71** |
| S2 | median | 0.195 | 4–16 | **0.78–0.79** | 1.20 (0.05–0.08) | 0.22 | 0.00 |
| S2 | 0.15 | 0.262 | 4–16 | **0.25–0.26** | 1.14–1.23 (2.3–5.5) | 2.50–4.06 | **0.57–0.58** |

**S1 holds.** Sample size explains 63 to 79 percent of $\log D_c$ at the median
and **17 to 26 percent at a tail quantile**, where the design variance of a
proportion is dominated by $p_c(1-p_c)$ and the cluster structure that
$d\,x_c^{-\gamma}$ does not carry. The exponent that would fit best is 1.14 to
1.56, and at the tail its replicate-to-replicate standard deviation reaches 5.5.

### 2. The inference stage, and where it fails

| route | $t_0$ | $K$ | $C_\gamma$ contains $\gamma_{\mathrm{ls}}$ | **certified containment** | incumbent containment |
|---|---|---|---|---|---|
| S1 | median | 60 | 0.989 | **0.716** | 1.000 |
| S1 | median | 200 | 0.991 | **0.368** | 1.000 |
| S1 | 0.15 | 200 | 0.767 | 0.989 | 1.000 |
| S2 | median | 200 | 0.718 | 0.885 | 1.000 |
| S2 | 0.15 | 200 | **0.053** | 0.964 | 1.000 |

**S3 holds and is worse than predicted.** Certified containment runs 0.366 to
0.989 against a restricted-model requirement of 0.95, and is worst — 0.37 at
$K=200$ — in exactly the cells where $C_\gamma$ *does* contain the best-fitting
exponent on 99 percent of replicates.

**That contrast is the finding, stated at the scope it supports.** Containing the
best-fitting exponent did not restore containment, so **estimation error in
$\gamma$ cannot explain the failure**. It does not follow that the structure
residual is the sole cause: when the family is wrong, $\gamma_{\mathrm{ls}}$ is
the best projection rather than a parameter of the truth, and this design also
breaks normality, the $\chi^2$ law for $\widehat D_c$ and the independence of
$\widehat D_c$ from $Y_c$ at the same time. **Whether the structure confidence
set covers the best-fitting exponent does not diagnose whether the structure
model is adequate**; separating the structure residual from the
sampling-distribution conditions needs the true-structure diagnostic of §22. The
fallback $\underline t=0$ was never triggered, so it is not a computational
failure.

### 3. Final performance

Latent-target coverage: certified **0.943–0.963**, incumbent 0.944–0.968,
oracle 0.935–0.958, against a guaranteed 0.90. **S2 holds** — but this is
**empirical conservatism, not the restricted-model guarantee transferring.** The
$F$ pivot's conditions do not hold under this design and a simulation cannot make
them hold; the intermediate containment event fails on up to 63 percent of
replicates while the final coverage does not, because the chain has slack
downstream.

Width against the structure-free incumbent: **0.959 to 0.998** — a narrowing of
**0.2 to 4.1 percent**, against 6.5 to 16.5 percent in the closed model.
**S4 fails.**

Two of the sixteen cells report a "captured share" above 1 — the band falling
below the oracle width. **That alone does not make the band invalid**: the oracle
uses the true scale as a reference and has not been shown to be the narrowest
valid band. What forbids reading it as an improvement is the containment of 0.37
observed in the same cells. The capture statistic is also unstable where the
uncorrected and oracle widths are close, since its denominator is then small, so
**coverage and realised width are reported first and capture is secondary**.

### What this establishes

> Under a stratified cluster design with an exogenous sample-size structure
> variable fixed in advance, the certified construction keeps latent-target
> coverage but **loses its containment guarantee**, and the width advantage over
> a structure-free construction falls from 6.5–16.5 percent to **0.2–4.1
> percent**. Estimation error in the structure parameter does not account for it;
> the structure family explains only 0.63 to 0.79 of $\log D_c$ at the median and
> 0.17 to 0.26 in the tail, and the same design breaks three of the model's other
> conditions at once. Which of these binds is not settled by this experiment.

Protocol outcome 2, reported as prominently as a gain would have been: **on this
design, using a variance structure does not pay.** One limitation bounds the
reading in the other direction: the design shares reached here are 0.05 to 0.26,
so the *available* narrowing is only 1.2 to 15.5 percent to begin with, and a
regional-share version of this design has not been built.

---

## 22. The remaining high design-share cells, and what the true-structure diagnostic separates

`exp25`, protocol `docs/PROTOCOL_exp25_high_share.md`. 16 cells, 2,000
replicates. Method, structure variable ($x_c=m_c$) and budget unchanged from
`exp24`. **Realised $\bar D/A=0.541$ to $0.752$, i.e. $\rho^2=0.351$ to
$0.429$** — the agreed targets, and the regional range `exp18` reached. The
fallback $\underline t=0$ fired on no replicate in any cell.

### The applicable range splits by route, and that is the result

| | `low_signal` ($\nu_c$ 12–28) | `small_sample` ($\nu_c$ 4–8) |
|---|---|---|
| structure $R^2$ of $\log D_c$ on $\log x_c$ | **0.59–0.85** | **0.05–0.71** |
| $\Pr(\widehat D_c=0)$ | 0.000 | up to **0.171** |
| $\mathrm{corr}(\widehat D_c,Y_c)$, tail | 0.48–0.50 | 0.68 |
| **containment, certified** | **0.955–0.992** | **0.681–0.987** |
| latent-target coverage | 0.958–0.971 | 0.944–0.975 |
| **band / structure-free incumbent** | **0.883–0.937** | 0.836–0.928 |
| captured share | **0.56–0.74** | 0.48–0.77 |
| incumbent captured | 0.23–0.30 | 0.09–0.23 |

**On the `low_signal` route the method works.** Containment holds at or above
its 0.95 requirement in every cell, coverage is 0.958 to 0.971 against a
guaranteed 0.90, and the band is **6.3 to 11.7 percent narrower** than the
structure-free construction, capturing 0.56 to 0.74 of the available narrowing
where that construction captures 0.23 to 0.30.

**On the `small_sample` route it does not.** Containment falls to 0.681–0.780 at
the tail quantile, where the structure explains 5 to 13 percent of $\log D_c$,
a sixth of the variance estimates are exactly zero, and $\widehat D_c$ correlates
with $Y_c$ at 0.68. The width figures there are not usable, because the band is
not containing what it is supposed to contain.

**R5 holds and this corrects the reading of `exp24`.** The width advantage over
the incumbent is 6.3 to 16.4 percent here against 0.2 to 4.1 percent in `exp24`.
The difference is the design share: `exp24` sat at $\bar D/A=0.053$ to $0.262$,
where the whole available narrowing was 1.2 to 15.5 percent to begin with.
**`exp24` was measuring a regime with little to win, not a method that does not
work**, and reporting it alone would have been the wrong conclusion.

### The diagnostic, and the answer is "both"

Supplying the true structure $a_c^{\mathrm{true}}=D_c/\overline D$ as known —
infeasible on real data, a diagnostic only:

| route | $t_0$ | $K$ | certified containment | **true-structure containment** |
|---|---|---|---|---|
| `small_sample` | 0.15 | 60 | 0.770 | **0.888** |
| `small_sample` | 0.15 | 200 | 0.682 | **0.815** |
| `small_sample` | 0.15 | 200 (target 0.75) | 0.769 | **0.868** |
| `low_signal` | 0.15 | 200 | 0.955 | 0.937 |

**On the harsh route the true structure recovers much of the containment — 0.68
to 0.82, 0.77 to 0.89 — and does not reach 0.95.** Two conclusions, and only
two: approximating and estimating the variance structure **does** affect the
outcome, and improving that step alone **would not** repair the procedure there.
The residue is not apportioned among normality, the $\chi^2$ law and
independence; this experiment does not identify their separate contributions and
no percentage is assigned to any of them.

On the well-behaved route the true-structure arm sits at 0.937–0.952, slightly
*below* the certified arm's 0.955–0.992. This is **consistent with** the
conservatism introduced by carrying the structure's estimation uncertainty
masking other approximation error, and it is consistent with the structure step
not being what binds there. Neither reading is established without a containment
argument or further analysis, and the observation is reported as an ordering,
not as a cause.

**Zero-variance populations are recorded, not repaired.** $\Pr(D_c=0)$ reaches
0.0033 and $\Pr(\widehat D_c=0)$ reaches 0.171 on the small-sample route. The
diagnostic arm is undefined when any $D_c=0$, so replicates containing one are
excluded **from that arm only**; the excluded fraction is 0.000 on `low_signal`
and up to **0.483** at `small_sample`, tail, $K=200$. Nothing was substituted.

**And the comparison was rerun with every arm scored on that same subset**, since
excluding half the replicates from one arm and not the others is not a
comparison. On the common subset the certified arm's containment is 0.676 to
0.992 against 0.682 to 0.992 on all replicates, and the contrast with the
true-structure arm is unchanged: 0.676 against 0.815, and 0.771 against 0.868, in
the two worst cells. **The exclusion does not carry the finding.**

### The verified scenario range — not a usage threshold

The temptation here is to write "degrees of freedom of 12 or more and a
structure $R^2$ above 0.6" as an operating rule. **That would be wrong on three
counts**, and the manuscript will not say it. Those numbers are characteristics
that happened to co-occur in these scenarios, not thresholds derived or tested
as such; the structure $R^2$ is computed from the *true* $D_c$ and is therefore
not available in real data; and nothing here proves that normality or the
$\chi^2$ law hold under any complex design. The two routes also vary degrees of
freedom, the sampling distributions and the structure fit together, so their
separate contributions are not identified.

What the experiment supports is a statement about the scenarios examined:

> In the high-noise, signal-reduction scenarios examined ($\bar D/A=0.55$ and
> $0.75$, $\nu_c$ between 12 and 28), the proposed procedure showed oracle
> containment of 0.955–0.992 against a nominal 0.95, latent-target coverage of
> 0.958–0.971 against a target of 0.90, and bands **6.3 to 11.7 percent
> narrower** than the structure-free comparator, at a Monte Carlo error of about
> 0.005 on these rates. In the small-sample scenarios ($\nu_c$ between 4 and 8,
> up to 17 percent of variance estimates exactly zero) oracle containment fell to
> 0.681–0.780 at a tail quantile and the width figures there are not usable.

**Reporting the simulation accurately does not require inventing a threshold for
general use.**

**This is the end of the validation range agreed earlier.** No further conditions
are searched with this method.

---

## 23. A Gaussian competitor for the same target, information and level

`exp26`, protocol `docs/PROTOCOL_exp26_same_target.md`. 16 cells, 10,000
replicates, Model R with an estimated structure. Both arms predict
$\theta_{\mathrm{new}}=\mu+u_{\mathrm{new}}$ — the **latent** value of a
population with no direct estimate — and both spend the identical budget
$\alpha_0+\eta_\gamma+\eta_t=0.10$.

### The competitor, built to be strong

$u_{\mathrm{new}}\sim N(0,A)$ exactly, so $\pm z_{1-\alpha_1/2}\sqrt{A_U}$ covers
it whenever $A\le A_U$. The upper limit is built from the **same** structure
confidence set and the **same** certified $\underline t_{\mathrm{cert}}$,
$\underline a_c$: on that event
$\bar S=\sum_cY_c^2/(1+\underline t_{\mathrm{cert}}\underline a_c)\ge S(t;\gamma)$,
and $S(t)/A\sim\chi^2_K$ at the truth, so $A_U=\bar S/\chi^2_{K,\alpha_2}$ covers
$A$ with probability at least $1-\eta_\gamma-\eta_t-\alpha_2$. Total error
$\alpha_1+\alpha_2+\eta_\gamma+\eta_t$, and $\alpha_1+\alpha_2=\alpha_0$ matches
the proposal exactly. The split was scanned and **the narrowest valid choice
given to the competitor** — it chose $(0.040,0.010)$ at $K=60$ and
$(0.045,0.005)$ at $K=200$.

The two arms therefore differ in exactly one place: $\alpha_0$ buys a conformal
rank, or a normal quantile plus a $\chi^2$ bound on $A$.

### G2 was wrong, and it was written down in advance

| $K$ | $d/A$ | oracle cov. | conformal cov. | **Gaussian cov.** | plug-in cov. | **Gaussian / conformal width** |
|---|---|---|---|---|---|---|
| 60 | 0.5 | 0.947 | 0.957 | 0.983 | 0.943 | **1.285** |
| 60 | 1.0 | 0.953 | 0.976 | 0.996 | 0.925 | **1.284** |
| 200 | 0.5 | 0.947 | 0.957 | 0.983 | 0.943 | **1.162** |
| 200 | 1.0 | 0.952 | 0.970 | 0.988 | 0.944 | **1.162** |

**G1 holds** — every valid arm covers at 0.957 or above against a guaranteed
0.90. **G2 is falsified.** The protocol predicted the Gaussian competitor would
be narrower; instead the ratio Gaussian/conformal is 1.162 to 1.285.

**Stated as a reduction, that is $1-1/r$, i.e. the conformal band is 13.9 to 22.2
percent narrower** — not 16 to 28, which is how much wider the Gaussian one is.
The two are different numbers and only the first is a reduction.

**G3 holds**: the gap falls from 1.28 at $K=60$ to 1.16 at $K=200$. **G4 holds**:
under a misspecified structure the ratio is 1.157 to 1.282, unchanged, since the
two share the scale machinery.

**Nominal levels, since they differ and the table must say so.** The conformal
and Gaussian arms both target $1-\alpha_0-\eta_\gamma-\eta_t=0.90$; the plug-in
Gaussian ignores the scale uncertainty and targets $1-\alpha_0=0.95$. Its
realised 0.925 to 0.948 is therefore short of **its own** 0.95 and above the
0.90 the other two claim — it is a reference, not a competitor, and the earlier
phrasing that read it against 0.90 was not the right comparison.

### Why the conformal arm wins here, stated as a mechanism

The same elasticity as §13. The Gaussian band is proportional to $\sqrt{A_U}$, so
its sensitivity to the scale limit is exactly $1/2$; the conformal band enters
through $\{1+\underline t\,\underline a_c\}^{-1/2}$, whose elasticity is
$\underline t\,\underline a_c/\{2(1+\underline t\,\underline a_c)\}<1/2$. **The
conformal band absorbs the scale uncertainty more gently.** The Gaussian arm
additionally has to spend part of $\alpha_0$ on the $\chi^2$ bound, which the
rank step does not need.

### Three qualifications on the comparison

**One valid Gaussian construction, not a class.** This is one comparator with its
split optimised, not the best possible. A different route to $A_U$, or one
exploiting the same damping, could close the gap. **The result is about this
constructed baseline, not about Gaussian methods in general and not about
small-area inference in general.**

**Part of the width difference is a conservatism difference.** The Gaussian arm
realises 0.982 to 0.996 coverage where the conformal arm realises 0.957 to 0.978,
both against the same 0.90. So it is buying some of its extra width with extra
coverage, and the comparison is not of two constructions calibrated to the same
realised level. Saying so does not weaken the result; it is what the numbers mean.

**The budget split was chosen on the data.** $(\alpha_1,\alpha_2)$ was scanned
and the split minimising the competitor's *mean width in that cell* was used.
That is deliberately generous, but it is a selection, and the per-split guarantee
does not automatically survive selection. **A split fixed in advance at
$(0.025,0.025)$ is therefore reported beside it**: the ratio is then 1.256 to
1.350, so the conformal band is 20.4 to 25.9 percent narrower. The
data-chosen split is the conservative number to quote and the fixed one shows the
selection was not doing the work.

### Computational cost

Per replicate: the shared scale machinery costs 0.27 to 0.80 ms and dominates;
the band step itself is 0.0005 to 0.003 ms for both arms. **Computation does not
distinguish them**, and the criterion is satisfied by saying so.

### What this settles for the manuscript

At the **same target, the same data, the same structure model and uncertainty,
the same centre and the same nominal level**, the proposed interval is **13.9 to
22.2 percent narrower** than the matched valid Gaussian baseline constructed
here, with both covering and with the competitor's budget split chosen to favour
it. That is the efficiency claim. It is a claim about this comparator, it carries
the conservatism qualification above, and it falsified a prediction registered
before the run — which is the strongest form this evidence can take.

---

## 24. ESS: the fixed procedure on real survey data, scalar target

`exp27`, protocol `docs/PROTOCOL_exp27_ess_scalar.md`, written before any
estimate was computed. ESS rounds 9–11, 127,286 respondents, 825 region-rounds,
retrieved through the portal API (`docs/DATA.md`). Target
$F_{cr}(t_0)$ at $t_0=4$, fixed by rule; three items fixed in advance; structure
variable $x_{cr}=$ sampled PSU count, carried over unchanged from `exp24`–`exp25`;
$\alpha_0=0.05$, $\eta_\gamma=\eta_t=0.025$ for every arm; the Gaussian split
fixed at $(0.025,0.025)$ rather than scanned. 45 configurations.

**No latent-target coverage is claimed or computed.** ESS has no latent truth and
a held-out region's direct estimate is not the latent value. Coverage is what the
simulations are for.

### Exclusions, counted

18 of 825 region cells have $\nu_{cr}<2$ and are excluded for every item. Cells
with $\widehat D_{cr}=0$: 13 for `trstprl`, 39 for `stflife`, 55 for `happy`; they
are given $v_L=0$, which applies no shrinkage and is conservative. The
$\underline t=0$ fallback fired in **none** of the 45 configurations.

### 1. The regime ESS actually presents

$\widehat\rho^2$ runs **0.25 to 0.68** across configurations — the regional regime
the manuscript identified and the one `exp25` found the method working in, now
confirmed on the real data for a scalar target. Design degrees of freedom per
region are ample: median 22–29, tenth percentile 8, ninetieth 180–339.

**Normality support differs sharply by item**, and this is an assumption check
ESS can actually deliver:

| item | skewness of standardised deviations | excess kurtosis |
|---|---|---|
| `trstprl` | $-0.47$ to $0.62$ | 0.3 to 4.4 |
| `stflife` | $-0.30$ to $2.30$ | 1.1 to 12.6 |
| `happy` | $-0.44$ to $2.81$ | 2.2 to **17.6** |

The pivot needs normality of the population-level deviations. **It is reasonably
supported for `trstprl` and clearly not for the other two**, and that is reported
with their results rather than after them.

### 2. The structure model on ESS

$\widehat\gamma$ runs 0.28 to 0.69 for `trstprl` — the design variance falls with
PSU count roughly as $x^{-1/2}$, not $x^{-1}$, because the PSU count does not
carry the whole design effect. For `happy` at round 9 and $n\ge150$,
$\widehat\gamma=-0.33$ with $C_\gamma$ excluding zero: the fitted structure says
design variance *rises* with sample size, which is not credible and is a signal
that the family does not fit.

$R^2$ of $\log\widehat D_{cr}$ on $\log x_{cr}$: `trstprl` **0.12–0.65**,
`stflife` 0.001–0.57, `happy` 0.0002–0.47. **The structure model describes ESS
design variances moderately at best and often not at all.**

**This $R^2$ is a fit to $\widehat D$, not to $D$, and therefore understates the
fit to the truth**: $\log\widehat D$ carries noise of variance
$\psi'(\nu/2)\approx0.074$–$0.098$ at these degrees of freedom, a standard
deviation of 0.27–0.31 on the log scale. The direction of the bias is known and
the corrected quantity is not reported here.

### 3. How far the arms differ on the same data

| comparison | range over 45 configurations | reading |
|---|---|---|
| certified / uncorrected | **0.647–0.953** | the correction narrows by 4.7 to 35.3 percent |
| certified / matched Gaussian | **0.686–0.964**, narrower in **45 of 45** | 3.6 to 31.4 percent narrower, median 14.6 |
| certified / structure-free | **0.695–1.125** | **mixed**: sometimes 30 percent narrower, sometimes 12 percent wider |

**The Gaussian comparison reproduces `exp26` on real data.** The certified band
is narrower in every configuration, and the median reduction of 14.6 percent sits
inside the 13.9–22.2 percent the simulation gave.

**The structure-free comparison does not, and the reason is visible.** Correlation
between the structure fit and the payoff is $-0.54$ across the 45 configurations:

| observable structure fit | certified / structure-free |
|---|---|
| $R^2<0.20$ (22 configurations) | median **1.048**, range 0.734–1.125 |
| $R^2\ge0.40$ (15 configurations) | median **0.908**, range 0.695–1.035 |

**Where the structure model fits, using it pays; where it does not, it costs.**
And the quantity that separates the two is computable from the analyst's own
data — it needs $\widehat D_{cr}$ and $x_{cr}$, both of which the procedure
already requires.

**This association was not pre-specified.** It was found in these 45
configurations after the fact and is reported as an observed association, not a
rule. Confirming it needs a survey system these data have not been used to
select — the AmericasBarometer replication that `docs/NEXT.md` has carried since
the start is the obvious candidate.

### 4. Superseded in part by §25

$\widehat D_{cr}$ above is the design variance of $\widehat F_{cr}$, **not of the
deviation $\widehat F_{cr}-\widehat F_c$ that the score actually uses.** §25
computes the right one and the difference is not cosmetic: every number in this
section that depends on $\widehat D$ — $\widehat\gamma$, the structure fit, and
three of the four arms' radii — is replaced there. **What survives unchanged is
the comparison against the matched Gaussian**, because both arms use the same
variance. The design share, the normality diagnostics and the exclusion counts
also stand.

The centre remains the **estimated** country-round share where §17–§20 assume it
known, and §25 shows that gap is not closed by fixing the variance. Nothing in
either section is a coverage statement.

**What it is:** an analyst can see which inputs each construction needs, how far
the intervals differ on their own data, that the structure route's payoff tracks
a diagnostic they can compute, and that the normality the pivot needs is
supported for one of these three items and not the other two.

---

## 25. The centring–variance mismatch, measured — and it changes §24

`exp28`, protocol `docs/PROTOCOL_exp28_centring.md`. Same data, same
configurations, same row sets (verified: $K$ identical, uncorrected radii
identical to machine zero). **No new method.**

§24 scored regions by $Y_{cr}=\widehat F_{cr}-\widehat F_c$ while using the design
variance of $\widehat F_{cr}$ alone. The right quantity comes from the Taylor
linearisation of the deviation,
$$u_i=\frac{w_i\mathbf 1\{i\in r\}(z_i-\widehat F_{cr})}{W_r}
-\frac{w_i(z_i-\widehat F_c)}{W_c},$$
aggregated to PSU totals over the whole country-round and passed through the same
stratified ultimate-cluster estimator. Degrees of freedom are kept at the region
level, which is the conservative choice and is stated rather than optimised.

### The variance itself moves modestly

$\widehat D^{\mathrm{dev}}/\widehat D$ has median 0.952–0.963 with tenth and
ninetieth percentiles 0.80 and 1.16–1.28, and **exceeds 1 in 26 to 33 percent of
cells**. M2 holds cleanly: by quartile of the region's weight share the median
ratio is 0.99, 0.97, 0.94, **0.84** — the more a region contributes to the centre
it is measured against, the more cancels.

### But the structure model changes character completely

| | §24 (wrong variance) | §25 (corrected) |
|---|---|---|
| median $\widehat\gamma$ | 0.531 | **1.140** |
| $C_\gamma$ contains $\gamma=1$ | **0 of 45** | **17 of 45** |
| implausible $\widehat\gamma<0$ | yes (`happy`, round 9) | none |
| $R^2$ of $\log\widehat D$ on $\log x$ | 0.000–0.653 | 0.091–0.225 |

$\gamma=1$ is $D\propto1/n$, the elementary expectation. **With the wrong
variance the structure fit never contained it; with the right one it contains it
in nearly forty percent of configurations and the median estimate sits at 1.14.**
The country-level component that does not scale with a region's own sample size
was inflating $\widehat D$ for small regions and flattening the fitted exponent.
That is a substantive validation that the mismatch had to be fixed, not a
technicality.

The $R^2$ falls and compresses, which is consistent with
$\log\widehat D^{\mathrm{dev}}$ being the noisier quantity — it is a difference of
two estimates — and the noise attenuates the fit.

### The arms, corrected

| comparison | §24 | **§25 (corrected)** |
|---|---|---|
| certified / matched Gaussian | 0.686–0.964, 45/45 narrower, median 0.854 | **0.729–1.014, 44/45 narrower, median 0.821** |
| certified / structure-free | 0.695–1.125, **mixed** | **0.459–1.034, 43/45 narrower, median 0.830** |
| certified / uncorrected | 0.647–0.953 | **0.422–0.867, median 0.730** |
| $\widehat\rho^2$ | 0.250–0.680 | 0.219–0.612 |

**The same-target Gaussian comparison is the one that survives**, median 0.821
against §24's 0.854 and `exp26`'s simulated 13.9–22.2 percent reduction. It is
insensitive to the correction precisely because both arms are built on the same
variance — which is the sense in which it is the robust result here.

The structure-free comparison, by contrast, moves from mixed to favourable. **The
§24 version of it was computed on the wrong variance and is withdrawn.**

### The exploratory diagnostic does not survive well, and is downgraded

§24 reported a correlation of $-0.54$ between the structure fit and the payoff
against the structure-free arm, and suggested it as something an analyst could
compute. Corrected, the correlation is **$-0.30$** and the $R^2$ range compresses
to 0.091–0.225.

**It is therefore an observable exploratory diagnostic, not a criterion for
deciding whether the method may be used.** Two reasons beyond the weakened
correlation: both quantities are built from the same variance estimates, so part
of any association is arithmetic rather than substantive; and a good structure
fit does not imply latent-target coverage, which is not measured here at all. The
earlier phrasing — "a computable criterion" — is withdrawn.

### What fixing the variance does not fix

A centre estimated from the same sample makes the regional scores **dependent**,
and the conformal rank argument assumes they are not. Measured from the same
influence functions, the mean within-country correlation among distinct regions
is

| regions in the country-round | observed | $-1/(n_r-1)$ |
|---|---|---|
| $\le5$ | $-0.232$ | $-0.250$ |
| 6–10 | $-0.116$ | $-0.111$ |
| 11–20 | $-0.046$ | $-0.053$ |
| $>20$ | $-0.029$ | $-0.029$ |

**Almost exactly the $-1/(n_r-1)$ of deviations from a common mean.** It is
negative, so it is the benign direction for a maximum-based rank statistic, and
it shrinks with the number of regions — but it is not zero, and **nothing here
repairs the exchangeability the rank argument needs.**

### The status of the ESS analysis, fixed

> ESS is presented as an application of the procedure **under a stated
> approximation**: the centre is estimated rather than known, and the scores carry
> a measured within-country dependence of about $-1/(n_r-1)$. **The theorem's
> guarantee is not attached to it.** What it shows is which inputs each
> construction needs, how far the intervals differ on real data, that the
> structure model recovers $D\propto1/n$ once the right variance is used, and
> which assumption is supported for which item.
