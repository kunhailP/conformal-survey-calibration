# Research log

Dated decisions, with reasons. Append only.

## 2026-09-09 — repository rebuilt

The predecessor repository carried two papers' worth of material: a
within-country simultaneous claim family with a political reanalysis, and a
cross-population conformal transport layer with a variance correction. A desk
rejection at *Political Analysis* on 2026-09-08, thirteen hours after
submission and without external review, turned on the contribution being hard
to locate. The diagnosis accepted here is that the manuscript's architecture,
not its content, was the obstacle.

This repository is scoped to one paper: targets, assumptions, and operating
conditions for conformal prediction on survey-estimated curves. See
`docs/SCOPE.md`.

**Carried over**, with provenance recorded: the archived result tables from the
licensed-microdata analyses, and the mathematical results they support.

**Rebuilt**: package structure, the target labelling of every construction, the
experiment protocol discipline, the claims ledger, and the test layer.

**Deferred**: the claim family and its closed-testing prevalence bound. It is a
survey-inference result — attaching uncertainty to a trajectory rather than a
wave pair moved a certified count from twenty countries to six — and a decision
is open on whether a compressed version returns as a second application. It is
not abandoned.

## 2026-09-09 — exp01 supersedes the inherited shape audit

The inherited audit fixed eight coordinates and reported its headline at design
share 0.80. Two problems: the applications report at most 0.29 nationally and
0.52 regionally, so the demonstrated failure sat outside the presented
operating range; and simultaneity runs over rounds by thresholds, so eight
coordinates understates the real count.

`exp01` adds a coordinate axis and evaluates at the observed operating points.
Outcome, in `docs/CLAIMS.md`:

- The mismatch cost grows with the coordinate count and does not shrink in K.
- The direction is predictable, and the survey-realistic direction is the
  anti-conservative one. This was written into the protocol as a falsifiable
  prediction before execution, and it held.
- At the operating points the cost is about one to two percentage points, not
  the headline figure. The manuscript must say so.

The last point weakens a claim the predecessor draft would have made and is
recorded here so it is not quietly reinstated.

## 2026-09-09 — licensed data obtained; the design-file condition is closed

ESS rounds 1-11, the WVS trend file and the LAPOP Grand Merge were supplied
directly. Rounds 9-11 carry complete design metadata for all 33 countries.

`exp02` settled the condition that `docs/DATA.md` had carried as unverified and
that the predecessor manuscript relied on without checking: whether primary
sampling units nest inside regions. They mostly do — 99.48% of respondents sit
in a PSU confined to one region — but fifteen country-rounds violate it, with
France round 11 at 15% and Belgium round 10 at 9%, and strata fail to nest in
regions in 63 of 90 country-rounds. Twelve countries carry degenerate PSU
identifiers, correctly so for register-based individual samples, which means
the regional pool mixes design variances that do and do not contain a
clustering component.

This does not overturn the inherited regional result. It does mean the result
cannot be reported until it is shown to survive correct joint resampling of the
offending regions, which is the next experiment. Recorded now so that the
obligation is not lost.

## 2026-09-09 — exp03 returns outcome 3, and reframes the paper

The protocol wrote down three possible outcomes. The answer is the third:
under Rao-Wu-Yue rescaling with the resampling unit set to `(stratum, psu)`,
the correction activates in **none** of thirty configurations. The inherited
single activation does not survive.

The mechanism matters more than the count. The need gate opens in 27 of 30
configurations — design noise at the regional unit is real, with shares of 0.49
to 0.66 against a national maximum of 0.29 — and the reliability gate opens in
none. Decomposing the diagnostic shows why. At round 10 with a minimum region
size of 40 there are 290 regions, more than three times the reported floor of
94, and the K-floor term is 0.083 against a threshold of 0.147. It passes
comfortably. The realised diagnostic is 0.244, and 60% of its square comes from
the *dispersion* of design variances across regions, whose largest-to-smallest
ratio reaches four figures.

**The `K >= 94` floor, which the predecessor manuscript carried as its negative
headline, is cleared in 27 of 30 configurations and blocks nothing.** The
binding constraint is heterogeneity of design variances, which more units do
not fix, because the refinement that raises the unit count is the same
refinement that raises the dispersion.

This is a better result than the one it replaces. It is structural rather than
arithmetic, it explains the inherited activation as an artefact of a downward-
biased bootstrap, and it holds at population counts where the stated floor has
no purchase. The manuscript's negative characterisation should be rebuilt on
it, and the K-floor demoted to what it is: a property of one diagnostic that
turns out not to be the operative obstacle.

## 2026-09-09 — exp03 was wrong, and exp03b is why we know

The exp03 entry above reported no activation in thirty configurations and
concluded that the `K >= 94` floor is displaced by design-variance
heterogeneity. **Both claims were artefacts of a reimplementation that did not
match the statistic it was characterising.** The verification run found it.

Four differences from `pcb.inference.design_aware`: the threshold grid was all
ten thresholds rather than the preregistered low-trust core `t in {1,2,3,4}`,
and `D` is a maximum over coordinates, so the grid is not cosmetic; the plug-in
scale lacked the floored modulation; standard deviations used `ddof=1` where the
archive uses `ddof=0`; and the rho lower bound carried a spurious `1/sqrt(d)`.

With the formulas aligned the archive reproduces to four decimal places, and
the result changes: four activations of thirty under Rao-Wu-Yue, not none.

Two further corrections to what was reported.

- The claim that the bootstrap choice and the resampling-unit correction "push
  the diagnostic the same way" was half wrong. The bootstrap is decisive: gate B
  opens in eight of eight m-of-m arms and two of eight Rao-Wu-Yue arms. The
  resampling unit moves `D` by under one percent and never flips a gate, which
  follows directly from `exp02` finding only 0.52% of respondents in a
  region-splitting PSU. That should have been anticipated from `exp02` itself.
- The heterogeneity account was overstated. Its median share of `D^2` is 7.3%,
  not 30%.

What replaces them is better than either. The ratio of the realised diagnostic
to its K-floor is predicted by scale shrinkage times a heterogeneity factor at
correlation 0.984, `corr(rho_hat, D / K-floor)` is 0.964, and scale shrinkage is
the dominant term. **The need gate and the reliability gate read the same
quantity in opposite directions**: design noise large enough to be worth
removing is, by that very magnitude, large enough to make the remainder poorly
determined. The frontier is a diagonal, not two independent dimensions.

The lesson for this repository is procedural. A reimplementation must reproduce
the statistic it characterises before its disagreements mean anything, and that
reproduction check belongs in the protocol, not in a verification run afterwards.
`docs/PROTOCOL_exp03_regional.md` did not require it. Future protocols will.

## 2026-09-09 — the coupling result, and the draft

Following the exp03 correction, the mechanism was pinned down in closed form.
At the coordinate attaining the maximum in the reliability diagnostic,

    D = sqrt(2/(K-1)) / [kappa sqrt(1-h)]

with `kappa` the scale shrinkage and `h` the share of the squared standard
error contributed by dispersion of design variances. Under the shape assumption
`kappa` is approximately `1 - rho^2`, so the reliability gate becomes

    K >= 1 + 2 / [tau^2 (1-rho^2)^2 (1-h)].

The identity reproduces the realised diagnostic to 3.2% mean and 7.1% maximum
relative error over the thirty regional configurations, and the boundary
predicts the gate correctly in **30 of 30**, against 27 that the fixed `K >= 94`
rule would admit while only 6 open.

The reading: the reported floor of 94 is this boundary at a design share of
zero, the regime where nothing needs removing. At the need gate's own cutoff of
0.47 the requirement is 153, at 0.60 it is 227, and at 0.66 it is 292. The two
gates read the same quantity in opposite directions, because the diagnostic is
evaluated on the scale the correction shrinks.

This is the manuscript's centrepiece and it exists only because the exp03
correction forced the diagnostic to be reproduced exactly. The wrong version of
exp03 would have supported a vaguer and weaker claim about heterogeneity.

Draft written to `paper/`: 3,581 words of body prose, abstract, statement of
significance. Every reported number is a macro emitted by
`paper/build_numbers.py` from the result tables, so a figure cannot drift from
its artefact. Macro, cross-reference and citation resolution verified
programmatically; the document has not been compiled, since no TeX distribution
is available in this environment.

## 2026-09-09 — novelty contingency for the coupling result

A literature check is running. Independently of it, the identity should be
assessed honestly, because it is short.

Strip the conformal setting away and it reads: let `T` estimate a total
variance and let a noise component `N` be subtracted to leave `S = T - N`.
With `N` known exactly, `SE(S_hat) = SE(T_hat)`, so

    RSE(S_hat) = SE(T_hat) / S = RSE(T_hat) x (T / S) = RSE(T_hat) / (1 - rho^2).

Subtracting a component does not reduce the standard error but does reduce what
that error is divided by, so relative precision degrades by exactly the
shrinkage factor. Under normality `RSE(T_hat) = sqrt(2/(K-1))`, and requiring
`RSE <= tau` gives `K >= 1 + 2/[tau^2 (1-rho^2)^2]`; the square is algebra from
squaring both sides, not a second mechanism.

**This is one line, and the phenomenon is adjacent to well-trodden ground:**
negative variance-component estimates in random-effects models, the precision
of estimated intraclass correlation and heritability when the between-group
component is small, and attenuation by a reliability ratio in measurement-error
models. It would be surprising if no one had written the relative-precision
version down. The manuscript should not be built on the assumption that nobody
has.

**What survives if it has been.** The identity becomes a stated elementary fact
with a citation, and the contribution is its consequence, which is specific and
was in fact overlooked: a published feasibility criterion for this correction is
a fixed population floor of 94, and that floor is the boundary evaluated at zero
design share — the regime where the correction is unnecessary. The empirical
demonstration stands on its own: the boundary predicts the gate in 30 of 30
survey configurations while the floor admits 27 of which 6 open. So do the
design-file audit, the variance-estimator sensitivity (the gate opens in 8 of 8
m-of-m arms and 2 of 8 Rao-Wu-Yue arms), and the directional argument about
correlated sampling error in cumulative distribution functions.

**What would have to change.** Section 4 would lead with the consequence rather
than the proposition, the proposition would be demoted to a lemma with prior
attribution, and the introduction would not describe the coupling as unexpected.
The paper would be a characterisation paper, which is what JSSAM publishes, and
a smaller claim honestly placed is worth more at review than a large one a
referee can puncture.

Prepared before the literature result arrives so that the framing is not chosen
to protect a conclusion.

## 2026-09-09 — exp05: the coupling is a property of the problem

The generalisation asked for after the tier question. The Fisher information
for the model variance of a Fay-Herriot model with known sampling variances is
`I(A) = (1/2) sum_c (A + D_c)^-2`, so any unbiased estimator has relative
standard error at least `sqrt(2/K)/(1-rho^2)` at equal sampling variances.
Protocol outcome 1: REML attains it, median ratio 1.002 over conditions with
`K >= 100`, and the closed form reproduces the exact bound to 3e-16.

Three consequences.

The result is no longer about one implementation's diagnostic. It is about any
workflow that subtracts sampling variance from between-population dispersion,
which includes the standard small-area model. That is the difference between a
paper about an uncited selector and a paper about survey practice.

It closes the scope gap the predecessor left open. Its floor was proved for
unbiased estimation and explicitly excluded shrinkage estimators, which is what
small-area practice is built on. The information version covers the estimator
practitioners use, and that estimator sits on the bound.

It connects to a symptom practitioners already know. REML returns a zero
estimate on a quarter of replicates at `rho = 0.9, K = 30` and never at design
shares up to 0.5, so zero and negative between-area variance estimates arise in
exactly the regime the boundary calls infeasible.

**Novelty is not claimed for the bound itself.** It is the standard asymptotic
variance in this model, and the contingency entry above anticipated that the
identity would prove to be known. The manuscript says so in the text rather
than waiting to be told. The claim is the consequence: a published feasibility
criterion for this correction is a fixed count of 94 populations, and that count
is the boundary at zero design share, the regime where the correction is
unnecessary.

## 2026-09-09 — exp06: the reproduction gate earns its place

The claim family was restored to give the manuscript a companion to its scope
results. The reproduction gate added after the exp03 failure caught a second
implementation divergence immediately, before anything was claimed.

The first attempt returned 15 / 7 / 4 / 1 against the archive's 20 / 12 / 6 / 1.
Three candidate explanations were tested and rejected: the bootstrap scheme, the
scope of the band over ordered pairs, and the definition of the marginal
comparator. Reading the archive's certification code settled it. Its critical
value is **one-sided** and the reimplementation used a two-sided supremum; and
its "plug-in" column is not a bootstrap at all but the sign of the point
estimate. With both corrected the archive reproduces exactly, counts and named
set.

That second finding matters for presentation. The predecessor's headline
compared the point-estimate column with the simultaneous column and described
the former as a "marginal reading". It is not a statistical reading. Reported
honestly the sequence is 20 by sign, 15 pointwise with design-based uncertainty,
11 simultaneous, and the effect is still large. The manuscript states the
correction rather than quietly using the better decomposition.

Both of this project's disagreements with the inherited archive have now turned
out to be the reimplementation's fault, caught by the gate the first failure
prompted. That is the gate working, and it is worth keeping.

## 2026-09-09 — the literature check returns; the contingency applies

The adversarial search found prior art, as the contingency entry anticipated.

**The coupling algebra is classical.** It is the familiar imprecision of a
variance component estimated by subtraction, in small-area models and in
random-effects meta-analysis. \citet{partlett2017random}, *Statistics in
Medicine* 36(2), document the coupled condition empirically in the
meta-analytic setting: intervals behave only when the number of studies is
large and the heterogeneity is not small relative to within-study error, which
is the trade-off the boundary describes. The manuscript now says so in the
abstract, the introduction and Section 4.1, and locates what is added: the
transfer to a calibration criterion that decides whether a procedure may be used
at all, the closed form as a planning quantity, and the reinterpretation of the
fixed floor.

**The floor being reinterpreted is our own.** The manuscript says that too. It
is self-correction, not a criticism of a third party, and presenting it
otherwise would be dishonest.

**Venue positioning is better than expected.** *Survey Methodology* contains one
conformal paper, this journal two, both from 2024. There is no *Survey
Methodology* paper constructing simultaneous bands for an estimated
distribution function; the only design-based simultaneous-band paper there is
for a functional mean. The gap is real and now stated with evidence.

**Three papers that had to be found and were not in hand.**
`michal2024model`, in the same issue as Bersson-Hoff, proposes a scaled split
conformal procedure relaxing exchangeability for complex designs. Its title
does not name the method, and a referee who knows it would have asked why it
was absent. `burris2020exact` is the in-venue precedent for exact area-level
coverage and predates Bersson-Hoff by four years. `koffman2025function` uses a
Rao-Wu-Yue-Beaumont bootstrap for joint bands under a complex design, the
closest existing machinery.

**An objection to the estimator choice, now answered in the text.**
`saigo2007mean` recommends an unrescaled scheme *because* no rescaling is
performed, on the grounds that rescaling sits awkwardly with estimating
distribution functions and quantiles. Our estimands are distribution functions,
so it applies. Section 2.1 answers it empirically: every diagnostic is reported
under both schemes, the difference is consequential and is reported rather than
absorbed.

**Unresolved.** The `K >= 94` figure has no source outside our own working
paper. That is consistent with it being ours, and the manuscript now attributes
it there explicitly.

## 2026-09-09 — exp07 closes the comparison gap, and improves the message

The literature check named Yoshimori-Lahiri as the benchmark a referee would ask
for. Running it would have been a mistake: it covers a scalar parameter of an
observed area, asymptotically, while this construction covers a curve for a
held-out population in finite samples. Racing them invites the objection that
incommensurable things were compared. The manuscript argues the point instead
and runs the two comparisons that are commensurable.

**The correction buys more than expected.** Against the anchor, at the same
level on the same calibration set, its realised radius is 0.805 of it at the
median and 0.805 to 0.849 where the gates open: a 15 to 20 percent reduction,
inside the oracle ceiling of 17 to 22 percent for those cells. The predecessor's
comparator, the conservative envelope, is 1.63 times the anchor, so beating it
was easy and the reported gain against it was not the informative number.

This changes the message. The correction is worth having where it is reachable,
so the boundary is a search instruction, not a discouragement, and the paper
should not read as a negative result. Section 6.2 now says so.

**The anchor holds.** Michal et al. document plain split conformal undercovering
under complex designs. Leave-one-country-out marginal coverage of the observed
target is 0.896 at the median across fifteen configurations, 0.891 to 0.906,
against a nominal 0.90, within one standard error at the smallest evaluation
count. The finite-sample guarantee survives a real complex design. Conditional
coverage on the worst held-out country runs 0.10 to 0.60 and is not claimed.

## 2026-09-09 — format compliance and a full read-through

**Format.** JSSAM allows 6,500 words of body text; ours is 5,929. The abstract
limit is 300 and it was 315, now 271. Statement of Significance is 123 against a
limit of 200, with no acronyms as required. Set in twelve-point Times on US
letter, double-spaced, ragged right, fonts embedded. Figure alt text sits
beneath each legend as the guidelines ask.

**The one requirement that forced a rewrite.** JSSAM instructs authors not to
cite unpublished manuscripts, and three citations pointed at the working paper
whose implementation this characterises. The implementation is now stated in
full in Section 4 and the manuscript is self-contained; the title page carries
the relationship. This is a better paper for it, since a reader no longer needs
a document they cannot obtain.

**PRICSSA.** Added a survey-reporting paragraph: target population, field
periods by round, the exact question wording, exclusions, weight composition,
and why no pooled response rate is quoted. The checklist itself is an external
form for the author to complete at submission.

**Read-through, four substantive corrections.**

Section 7 still listed a version of the boundary for shrinkage estimators as an
open problem. `exp05` closed that: REML attains the information bound, and
shrinkage is not what carries the result. The open problem is now structured
covariance across populations, which the equal-variance closed form genuinely
does not address.

Section 7 also said no improvement over any method had been demonstrated, which
`exp07` had already made false in the internal comparison. It now distinguishes:
no matched comparison against external methods is possible without agreeing a
common target, and the improvement against the uncorrected band on the same
target is measured.

Four references to "the archive" and "the predecessor manuscript" survived the
removal of the citation and pointed at nothing a reader could reach. All now
name an earlier implementation of the same procedure, identified on the title
page.

The introduction and Section 7 ended on the negative result, written before the
width comparison existed. Both now carry the 15 to 19 percent gain, so the paper
reads as what it is: a boundary that says where to look, not a discouragement.

The section heading "needed, and mostly unreachable" was likewise reversed to
"reachable only in a narrow band".

## 2026-09-09 — exp08 supplies the consequence the paper was missing

The paper could characterise when the correction is reachable but had nothing a
practitioner would do differently. A boundary that says "you need 300
populations and you have 30" is precise and inert. `exp08` asks the question a
practitioner would actually ask: can the unit be refined until the requirement
is met?

Refinement raises supply and requirement together, and the dimension decides
which wins. Cutting the survey by sex yields 60 populations against a
requirement of 2,006; cutting the same survey by region yields 236 against 256.
The domain counts differ only fourfold, so the count is not the operative
quantity. Sex halves each sample without adding between-domain dispersion,
because men and women have nearly the same trust distribution, and the design
share reaches 0.85. Regions differ, dispersion grows with the noise, and the
share stays at 0.60.

That is a design instruction, and it is the first thing in this project that
tells someone what to do rather than what not to do: **refine along a dimension
on which the domains actually differ.**

It also strengthens the boundary's evidence considerably. It now predicts the
gate correctly across five domain definitions rather than one, and six
configurations open, so the manuscript has positive cases and Section 6.5's
15 to 19 percent applies to something reachable.

**A level was dropped after the first run,** and it is recorded rather than
quietly removed. The country level was in the original sweep and is degenerate
for this estimand: a domain that is the country has zero departure from its own
national curve. Its points sat at a design share of exactly zero and were
visible as an artefact in the frontier figure. The level was removed, the sweep
re-run, and the national reference is `exp04`.

**A lapse worth recording.** The first version of this section hard-coded the
ledger figures into `build_numbers.py` rather than computing them from the
result table, which is precisely what the claims-ledger discipline exists to
prevent. They are now derived.

## 2026-09-10 — exp09: estimating the sampling variance is a bias problem, not an information problem

Section 4.2 states the information bound for the model variance with the design
variances known. They are not known in any application in this paper. The
obvious extension is to redo the bound with $\widehat D_i$ in place of $D_i$,
and `docs/THEORY_estimated_variance.md` does it: profiling the per-population
nuisance $D_i$ out of the joint Gaussian-$\chi^2$ likelihood gives
$I_{\mathrm{eff}}(A)=\tfrac12\sum_i[(A+D_i)^2+D_i^2/\nu_i]^{-1}$, so the
manuscript's boundary picks up a factor $1+\rho^4/\nu$.

**That extension is not worth a section, and the experiment says so plainly.**
The factor is fourth order in the design share. At the largest share in the
applications, $\rho=0.66$, the effective information falls below the known-$D$
value by under 4 percent even at five degrees of freedom. A paper whose
contribution was "we account for estimated sampling variances in the
information bound" would be a paper about a two-percent correction. This is
recorded because the negative result was the reason to look further, not a
disappointment to be buried.

**What is worth a section is what the information calculation cannot see.**
Standard practice does not use an unbiased estimator; it substitutes
$\widehat D_i$ into a known-$D$ likelihood. The substitution correlates the
weight with the residual, and the resulting estimating function is positively
biased at the truth, by $4\rho^4/[\nu(1-\rho^2)]$ relative to $A$ to first
order. The bias is $O(1/\nu)$ and the noise is $O(m^{-1/2})$, so **it does not
average away as populations accumulate**: over $m$ from 30 to 1,000 the
realised relative bias at $\rho=0.66,\nu=10$ is flat at 0.10 to 0.11.

Three consequences, in increasing order of how much they matter here.

1. The bias is upward, so the deconvolved scale is overstated and the
   reliability diagnostic understated. At $\rho=0.66$ and $m=250$ — the regional
   operating point of Section 6 — the plug-in opens the reliability gate on 59
   percent of replicates where the correct scale opens it on 18. The one gate
   this manuscript characterises is anti-conservative under estimated design
   variances.
2. **It reverses `exp05`.** `exp05` found REML attains the information bound
   with $D_i$ known and concluded the inflation cannot be evaded by a better
   estimator. True, and narrower than it reads. With $D_i$ estimated the
   likelihood-weighted estimator sits at 1.22 times the bound at the regional
   operating point and 2.27 times at $\rho=0.9$, while the unweighted
   Prasad-Rao moment estimator — dominated when $D_i$ is known — sits on the
   bound. The choice among variance-component estimators stops being an
   efficiency question and becomes a bias question.
3. It gives a sharper reason for smoothing design variances than the usual one.
   Weights built from a smoothed $\widetilde D_i$ are nearly independent of the
   residual, which removes the leading bias term. That is a stronger argument
   than "the estimates are noisy".

**A prediction that came out qualified, and it is recorded as such.** The
protocol predicted the plug-in would open the gate more often, full stop. It
does not. At low design shares and small $m$ it opens the gate *less* often,
because the sampling variability of $\widehat A$ acts through
$E[1/\widehat A]>1/A$ in the opposite direction to the bias. Bias wins where
$\rho^4/\nu$ is large, variance wins near the threshold. The claim that
survives is regime-specific and the memo now says so.

**Also settled, and it closes a question `exp03b` raised.** Degrees of freedom
are a property of the design, not of the computation: with
$\nu^{\mathrm{des}}=20$, raising the replicate count from 100 to 10,000 buys
3.6 effective degrees of freedom and no more. `exp03b` found the gate opening
in different numbers of arms under $m$-of-$m$ and Rao-Wu-Yue resampling; the
framework above says the difference should run through $\nu^{\mathrm{eff}}$ and
bias, which is a prediction that experiment can be re-read against.

**What this does not touch.** The model assumes populations are independent and
$Y_i \perp \widehat D_i$. The second is false for a CDF ordinate, whose design
variance is approximately $p(1-p)/n^{\mathrm{eff}}$ and so is a function of the
estimand itself — that is the extension specific to this paper's setting rather
than inherited from small-area estimation, and it is next. The first is plan
item (3), the country-region block structure, and nothing here bears on it.

## 2026-09-10 — exp10: the gate certifies the wrong quantity

The development plan asked for a confidence-interval certification with a
stated error budget, targeting the latent scale $s=\sqrt A$, and for the two
checks that decide whether it is worth building: does it reduce false
certification, and does it abstain so often as to be useless.

Both checks came out well, and on the way the experiment found something
larger. **The band does not depend on $\widehat s_G$. It depends on
$\widehat\kappa=\widehat s_G/\widehat s_Y$**, because the calibration scores
divide by $\widehat s_Y$ and the placement multiplies by $\widehat s_G$, so the
half-width is $|Y|_{(m)}\widehat\kappa$ and nothing else. Both quantities are
built from the same $S_Y^2$, so the errors partly cancel, and
$\mathrm{RSE}(\widehat\kappa)/\mathrm{RSE}(\widehat s_G)\to\rho^2$.

The population requirement therefore falls by $\rho^4$. At $\rho=0.66$, the
largest regional design share, that is 291 populations against about 55. **Every
regional configuration in Section 6 has $K$ between 100 and 290.** If this
survives heteroscedastic designs, the manuscript's central finding — that the
correction is reachable only in a narrow diagonal band — is an artefact of
certifying $\widehat A$ instead of the width factor. That is not established
yet and `docs/THEORY_certification.md` §6 says exactly what would establish it.

The boundary also gains a second axis. Populations and design degrees of
freedom enter harmonically,
$K_{\mathrm{eff}}^{-1}=(K-1)^{-1}+\nu_{\mathrm{tot}}^{-1}$, so $\nu$ imposes a
floor no number of populations clears. `exp09` showed replicates cannot buy
$\nu$; this says what not having it costs.

**On the plan's proposed interval.** Separate $\chi^2$ intervals for $T$ and
$D$ combined by a union bound is valid and it certifies essentially never — at
most 6.5 percent of replicates in any cell, against 100 percent for the exact
interval at the same truth. Two causes, and the experiment separates them: the
union bound costs about a factor of seven against the standard Graybill-Wang
interval for a difference of variance components, and the wrong target costs
the rest. For $\kappa$ no bound is needed at all, because
$(\widehat D/S_Y^2)/\rho^2\sim F_{\nu,K-1}$ is an exact pivot. The pivot exists
because $\kappa$ is a *ratio* of the two components; certifying the difference
forfeits it.

**On the frozen gate.** It is not an error-controlled rule and should stop being
described as one. At $K=300$, $\rho=0.707$ it certifies on 53 percent of
replicates and is wrong on 47 of those 53. The stated population floor of 94
certifies always and is wrong on up to 94 percent. The exact rule never exceeds
its budget of 0.05 in any of 54 cells.

**A detail that is part of the theorem, not a refinement.** The guarantee holds
for the minimax point estimate $\widehat\kappa_\star=2LU/(L+U)$ and not for the
plug-in: false certification is 0.003 for the former and 0.045 for the latter.
Reporting a certified interval while shipping the plug-in point estimate breaks
the result.

**The reframing this forces, and it is the reason to rewrite rather than
patch.** The safe band $B_U$ — the union over the confidence interval, which by
monotonicity is just the band at the upper limit, with no grid — is valid at
$\alpha_0+\eta$ at *every* $(K,\nu,\rho)$. Realised coverage never fell below
0.951 against a 0.90 target, while the plug-in band undercovered by up to 25
percentage points. Its width penalty over the infeasible oracle is 2 to 61
percent and shrinks in $K$, and even at its worst it is 28 percent narrower than
the uncorrected anchor. **So certification is not a gate. It is a report.** The
manuscript currently tells a practitioner who fails the gate to fall back to the
anchor; that discards a valid and much narrower band. The prescription should be
to widen to the confidence limit always, and to report the widening as the price
of not knowing the scale.

**What is not established.** Propositions A and C are exact only under equal
design variances, and the ESS configurations are not. Proposition C is the
cleanest result here and the one least likely to survive a real design;
replacing it is now the main theoretical task. $Y_i\perp\widehat D_i$ remains
false for a CDF ordinate (`exp09` §7.1), and the country-region block structure
remains untouched — though the centring bound is available now and is small:
country-centred deviations cost one contrast per country, so 236 regions in 30
countries give 206 effective, not 235.

## 2026-09-10 — correction: the requirement claim mixed two criteria

The `exp10` entry above reported the population requirement at $\rho=0.66$
falling from 291 to about 55. **That is wrong and the error is recorded rather
than quietly fixed.**

291 is a *relative standard error* criterion. The certification of
`docs/THEORY_certification.md` §2 is a *high probability* criterion, and for a
log-symmetric interval it demands $\sigma\lesssim\varepsilon/z_{1-\eta/2}$ where
an RSE criterion demands $\sigma\le\varepsilon$. The requirement is therefore
about $z^2\approx3.84$ times larger. Recomputed on matched criteria at
$\tau=0.147$, $\eta=0.05$:

| $\rho$ | RSE on $s_G$ | RSE on $\kappa$ | certify on $\kappa$, median |
|---|---|---|---|
| 0.47 | 153 | 9--10 | 33--41 |
| 0.60 | 226 | 31--37 | 122--149 |
| 0.66 | 291 | 58--70 | 226--276 |

The $\rho^{-4}$ mechanism is confirmed — the RSE column matches
$\rho^{-4}=20.5,\ 7.7,\ 5.3$. **What does not survive is the claim that this
makes the regional configurations reachable.** At $\rho=0.66$ a certified
guarantee needs 226 to 276 populations for a coin-flip chance, against the
manuscript's own 291 and against regional counts of 100 to 290. The gain is
material only near the need cutoff $\rho=0.47$, where it is a factor of four.

**This changes which result the paper leads with, not whether it has one.** The
safe band $B_U$ is valid whether or not certification succeeds, so a high
certification requirement is a statement about how often a small widening can be
*announced*, not about whether the band works. The comparison that settles it is
against a valid alternative on the same target, which the repository already
contains: `noise_enlargement`, the shape-free tail-bound widening. At
$\alpha_0=\eta=0.05$, 40,000 replicates, the safe band is **30 to 68 percent
narrower** than the enlargement band while covering at 0.955 or better against a
0.90 target; the enlargement band covers at 0.999 or above and wastes nearly its
whole budget. That is the lead result, and it needs no certification.

**Two further corrections from the same review.**

"The band does not depend on $\widehat s_G$" was wrong as written. It depends on
$\widehat s_G$ only through the ratio $\kappa$, which is a weaker requirement,
not no requirement.

The observed 0.955 coverage is not a proven 0.95. The declared budget was
$\alpha_0=\eta=0.05$ and the guarantee is 0.90. The gap decomposes into
conformal granularity (0.014 at $K=30$, 0.001 at $K\ge100$ — only $K+1$ levels
exist, and at $K=30$ the radius is finite only for $\alpha_0\ge0.032$, so the
budget split is constrained) and the union step (0.004 to 0.035 of its 0.05).
The union argument is loose by at most about three percentage points, which is
less than assumed.

**Verified against the repository's own code, not only against a reduction.**
`src/dac/bands.py::oracle_rescaled` returns
`latent_scale * quantile(max|Y| / total_scale)`, which is exactly
$|Y|_{(m)}\kappa$. Proposition A is the implementation, not an idealisation of
it. Note also that the function takes *scalar* scales, so the coordinate-varying
case the review asks about is not implemented anywhere yet.

## 2026-09-10 — two corrections to the previous entry

**The column label was wrong even though the number was right.** The
manuscript's diagnostic (eq. 14) is $\mathrm{SE}(\widehat s_G^2)/\widehat s_G^2$,
a relative standard error of the **variance**, not of $s_G$. The matched-criterion
table's first column is therefore "RSE on $A$ at $\tau$", and the $\kappa$ column
is computed at $\varepsilon=\tau/2$ to put them on the same footing. That is what
the computation did; the label named the wrong quantity.

**"Coordinate-varying scales are implemented nowhere" is false.** It was read off
`src/dac/bands.py`, whose `oracle_rescaled` does take scalars, and generalised
without checking the experiments. `experiments/exp07_widths.py` already uses
per-coordinate scales throughout: `s_plug = maximum(dep.std(0), ...)` is a
vector, `sT` is a vector, the scores are `max(abs(dep) / s_plug, axis=1)`, and
the reported radius is `q * sT.mean()`.

The last of those matters more than the correction itself. `q * sT.mean()` is the
**mean half-width over coordinates**, not one radius applied to every coordinate.
The band the code actually forms is $q\,sT(j)$, coordinate by coordinate. So the
accurate description of the project is: the closed-model results use a scalar
scale; the ESS analysis uses per-coordinate standardisation and a per-coordinate
correction; **no theory yet connects them.**

Two specific consequences for the safe band. At $d>1$ the union argument of
Proposition E needs $\kappa_U(j)\ge\kappa(j)$ *simultaneously* across
coordinates, which is a simultaneous band on $\kappa(\cdot)$ and pays a
multiplicity cost the scalar result does not. And the scalar closed form
$q\kappa_U$ is not what the ESS code would compute even if $\kappa$ were known.
Both are unmeasured and neither should be asserted until they are.

## 2026-09-10 — exp11: unequal design variances do not break the upper limit, and they relocate the bottleneck

The work order was: keep the equal-variance results, move the central claim to
the safe T2 band and the width it costs, and take the next experiment to
**scalar** targets with unequal $D_i$ before touching coordinates. Done.

**The one-sided upper limit keeps its budget everywhere.** Over 45 cells,
$\Pr(\kappa>\kappa_U)$ reaches 0.0514 with oracle degrees of freedom and 0.0481
with feasible ones, against $\eta=0.05$ at a Monte Carlo standard error of
0.0015. At zero dispersion it returns 0.047 to 0.051, reproducing `exp10`. This
is outcome 1 of the protocol: the scalar heteroscedastic case is closed and the
next obstacle is coordinates, not populations.

Also switched to a **one-sided** limit. `exp10` spent a two-sided interval on a
band that only needs an upper bound; the one-sided version is the correct
construction and strictly narrower. Certification keeps both ends.

**The interesting finding is where heteroscedasticity costs information.** Not
in the variance estimator. The Satterthwaite degrees of freedom of the
*numerator* $\overline{\widehat D}$ never fall below 75 and are usually in the
hundreds. The *denominator* $S_Y^2$ is a quadratic form in non-identically
distributed normals, and its effective degrees of freedom
$\nu_{\mathrm{den}}/(K-1)$ fall to **0.144** at $K=100$, $\bar D/A=4$,
$\sigma_{\log}=1.5$. **A hundred populations then carry the information of
fourteen.**

That quantity, $(K-1)^2(s_1/K)^2/[s_2(1-2/K)+s_1^2/K^2]$, is the effective
population count this project has been circling since the $K_{\mathrm{eff}}$
discussion began, and it is not an assumption imposed on the problem — it comes
out of the quadratic form and is computable from the data. It composes with the
other two losses already on the table: the $\rho^4$ factor from certifying the
right functional, and the one-contrast-per-country cost of centring. None of the
three is the raw count.

**A second appearance of the plug-in mechanism from `exp09`.** With oracle
degrees of freedom the failure rate stays near 0.05 at every dispersion. With
feasible ones it collapses to 0.001 to 0.004 at high dispersion — heavily
conservative, and the conservatism shows up as width. So it is not the $F$
approximation that degrades; it is substituting $\widehat D_i$ into the
Satterthwaite formula. The same substitution that biased the variance component
in `exp09` §4 now distorts the degrees of freedom.

**The comparator was given every advantage and still loses.** The review asked
for a fair budget allocation for `noise_enlargement` and a model-based
competitor. The enlargement's anchor/tail split was scanned and the narrowest
valid choice used per cell — the optimum puts 0.5 to 0.8 on the anchor, so the
even split used earlier was handicapping it. The safe band is still **18 to 71
percent narrower in every cell**, at coverage never below 0.950 against a
guaranteed 0.90. The Gaussian plug-in prediction interval is narrower still and
**never reaches its nominal 0.90 anywhere**, falling to 0.547: narrow and
invalid, which is the contrast worth printing.

**And the comparison is of assumptions, not only of widths.** The enlargement
reaches T2 by a Gaussian tail bound on the target's sampling error; the safe
correction reaches it by (S) plus a bound on the correction factor. These data
are generated under (S). The claim is therefore conditional: *where the
common-shape assumption holds*, the correction is substantially narrower at the
same guaranteed level. What happens when (S) fails is `exp01`, on a different
axis, and the two must not be merged into a single ranking.

**What remains, unchanged by this.** Numerator and denominator are independent
by construction here and are not for a CDF ordinate. Populations are
independent. And everything above is scalar: `exp07_widths.py` standardises
coordinate by coordinate and reports a mean half-width, so the closed form
$q\kappa_U$ is not yet what the application computes.

## 2026-09-10 — exp12: two retractions, and the question turns around

Three objections to `exp11`, all answered without touching coordinates.

**Retraction 1. $\nu_{\mathrm{den}}$ is not $K_{\mathrm{eff}}$.** The previous
entry said unequal design variances reduce 100 populations to 14. That is the
effective degrees of freedom of the *unweighted sample variance*, and it moves
in the opposite direction to the information. At $K=100$, $A=1$, mean $D=4$:
equal $D_i$ gives $\nu_{\mathrm{den}}=99.0$ and $K_I=4.00$; splitting into 50 at
0.1 and 50 at 7.9 gives $\nu_{\mathrm{den}}=61.8$ and $K_I=\mathbf{41.95}$.
Dispersion multiplies the Fisher information tenfold — the manuscript's own
Jensen argument in §4.2 already says so — while making $S_Y^2$ less precise.
Reporting the two as one quantity was wrong.

**Retraction 2. The scalar case was not closed.** `exp11` used the
common-denominator construction $|Y|_{(m)}\widehat\kappa$. Under (S) with
unequal $v_c$ the manuscript's Section 3 licenses per-population
standardisation instead, $M_c=|Y_c|/\sqrt{s_G^2+v_c^2}$ with the band at $s_G$.
The two coincide only under equal design variances, and `exp07_widths.py` uses
the former. So **the manuscript's theory and its own ESS implementation are
already two different constructions**, which this experiment surfaced rather
than created.

Measured: the licensed construction covers at exactly $m/(K+1)$ at every
dispersion (largest deviation 0.003 against Monte Carlo error 0.0015). The
common-denominator one departs by up to $+0.021$ at a width 12 percent higher,
and by $-0.003$ the other way elsewhere — neither exact nor uniformly
conservative. And the scalar $\kappa_U$ band contains the licensed oracle band
on as few as **83.5 percent** of replicates. `exp11`'s band is not the object
Proposition E covers.

A correct heteroscedastic safe band is built and works: the half-width is the
$m$-th order statistic of $h_c(s)=|Y_c|/\sqrt{1+v_c^2/s^2}$, each $h_c$
increasing in $s$, so the union over an interval is the band at its upper
endpoint — an upper limit on $s_G$, not on $\kappa$. Coverage 0.964 to 0.996
against a guaranteed 0.90. **Its containment of the oracle band is 0.944 to
0.997, marginally short of $1-\eta$**, because $h_c$ decreases in $v_c$ so
substituting $\widehat v_c$ is not conservative. Small, real, and not closed.

**The finding that matters is the answer to the review's own question.** Is
information destroyed by heteroscedasticity, or discarded by summarising it
with an unweighted variance? **Discarded.** Efficiency against the information
bound at $K=300$, $\bar D/A=4$: at equal variances the unweighted estimator
reaches 0.996; at $\sigma_{\log}=1.5$ it reaches **0.232**, while the optimally
weighted estimator of `exp09` Proposition 2 reaches 0.999. The information is
there; the standard construction — observed spread minus a mean design variance
— is the step that discards it.

**With a sting.** Plug-in weights built from $\widehat D_i$ reach 0.341 where
the unweighted estimator reaches 0.996, and never exceed 0.69 anywhere. Naive
weighting is worse than none. That is `exp09` §4 for the third time: the
correlation between $\widehat D_i$ in the weight and in the residual. A usable
weighted construction needs weights independent of the residual — smoothed
design variances, or sample splitting — and that is a task, not a corollary.

**The model-based comparator, and a wrong prediction.** Built properly this
time, $\pm z_{1-\alpha_0/2}\sqrt{A_U}$ with a one-sided Graybill-Wang limit at
the same total budget. The protocol predicted it would beat the conformal band
under Gaussian truth. **It does not** — it is 3 to 14 percent wider in every
cell. The mechanism is worth printing because it is not about conformal
prediction: both use the same $A_U$, but the model-based band is proportional to
$\sqrt{A_U}$ while the conformal band has
$\partial\log h_c/\partial\log s=\rho_c^2$. The advantage is the $\rho^2$
damping of §1, and a parametric interval exploiting the same damping would match
it. The paper should say that rather than claim a win for the rank argument.

**Claim downgraded, as asked.** "Unequal design variances do not break the upper
limit" becomes: across the 45 conditions of `exp11` and the 27 of `exp12`, no
evidence was found of the nominal level being exceeded. Satterthwaite
approximates a heteroscedastic quadratic form by one chi-square; oracle degrees
of freedom do not make the ratio exactly $F$, and nothing here proves
finite-sample control.

**One point of fact.** The oracle-versus-feasible comparison in `exp11` already
varies only the degrees of freedom — both limits come from the same
$R=\overline{\widehat D}/S_Y^2$ on the same replicates through the same
function. So the collapse of the feasible failure rate to 0.001-0.004 is
attributable to the substitution, and it is excess conservatism, not loss of
control.

## 2026-09-10 — exp13: the independence hypothesis was wrong, and smoothing is why

The work order was: run the weighting experiment but keep the known-$D$ ideal and
the estimated-$D$ bound apart; treat independent weights as **one candidate**
rather than the answer; price the sample split; and do not read an estimation
improvement as a band result. Part A and Part B are separate blocks of `exp13`
for that reason.

**First, a scoped restatement.** The three-way decomposition asked for:
estimating the design variances costs **0.5 to 1.9 percent**, and the unweighted
procedure costs **28 to 202 percent**. So essentially none of the gap comes from
$D_i$ being unknown. The previous entry's "three quarters of the information is
discarded" is the third gap only, in the closed Gaussian-$\chi^2$ model, and it
is a statement about an estimator rather than about survey data. (For the record:
`exp12` already measured efficiency against $\sqrt{2/K_{I,\mathrm{eff}}}$, the
estimated-$D$ bound, using RMSE, so bias was inside it. What was missing was the
decomposition, not the benchmark.)

**The prediction that failed is the one that taught something.** The protocol
predicted a GVF fitted on all populations — own $\widehat D_i$ included — would
inherit the plug-in failure. It does not. Efficiency: `plugin` 0.49-0.91 with
bias up to **+0.58**; `gvf_all` **0.71-1.00** with bias at most +0.075;
`unweighted` 0.33-0.78. `gvf_all` beats `unweighted` 12 of 12 and beats
two-fold cross-fitting 12 of 12.

The mechanism is dilution, not independence. A GVF averages $\widehat D_i$ over
all $K$ populations, so a population's own estimate enters its own weight with
coefficient $O(1/K)$; the residual bias falls from +0.075 at $K=60$ to +0.030 at
$K=200$. **So "a valid method must use weights independent of the residual" was
too strong and is withdrawn.** What the evidence supports is narrower: weights
built from one population's own estimate fail badly, weights built from a smooth
over many do not, and the residual $O(1/K)$ bias has to be quantified rather than
assumed away.

**Sample splitting is priced and mostly not worth it.** `gvf_split` beats its
matched half-sample baseline 12 of 12 — the weighting itself works — but beats
the *full-sample* unweighted estimator in only 6 of 12, exactly the
$\bar D/A=4$ cells. At $\bar D/A=1$ the half of the data given up exceeds what
the weighting recovers. Cross-fitting, which was meant to buy the split cost
back, is worse than `gvf_all` everywhere. The independence machinery is not what
pays; the smoothing is.

**And the gain is conditional on the design variable predicting $D_i$.**
`gvf_all` efficiency at $K=200$, $\bar D/A=4$ runs 0.963, 0.893, 0.707 as GVF
misfit $\sigma_e$ goes 0, 0.3, 0.6. A generalised variance function that does not
fit gives back most of the improvement. That is the transfer condition and it
belongs in any claim about survey data.

**An unplanned side effect.** The share of replicates with $\widehat A\le0$ falls
from 0.198-0.237 (unweighted, $K=60$, $\bar D/A=4$) to 0.017-0.057 under
`gvf_all`. Section 4.2 of the manuscript reads zero estimates as the symptom of an
infeasible regime; part of that symptom is the estimator, not the regime. Largest
single weight share stays at 0.012-0.081 across all arms, so none of this is
extreme weights.

**Part B, kept separate, and it works.** Because $h_c(s,v_c)$ increases in $s$
and *decreases* in $v_c$, bounding only $s_G$ is not enough — which is the
diagnosis behind `exp12`'s 0.944 containment. Bounding both, with $s_U$ at
$\eta_1$ and simultaneous Bonferroni lower limits $v_{L,c}$ at $\eta_2$, gives
containment of **0.9998 to 1.0000** against the $1-\eta$ requirement. Its price
is 1.28 to 1.89 times the oracle width against 1.10 to 1.53 for the band that
does not contain — **17 to 36 percentage points for the guarantee.** Having that
measured is what allows a narrower approximation to be judged instead of
asserted.

The `exp12` shortfall also decomposes, and only half of it was diagnosed before.
$\Pr(v_c\ge v_{L,c}\ \forall c)$ is 0.974-0.977 against a nominal 0.975, so
Bonferroni is essentially exact. But $\Pr(s_G\le s_U)$ is **0.963-0.969** against
0.975 at $\bar D/A=1$: the normal-approximation upper limit for $A$ is itself
mildly anti-conservative. One cause is the $\widehat v_c$ substitution, the other
is the scale limit, and the second is fixable with an exact or Graybill-Wang
limit.

**What none of this shows.** That an estimation improvement improves a band. The
two blocks were run on the same replicates and reported apart on purpose. And
nothing here has been through a finite-population complex-sample experiment,
which is the step that decides transfer.

## 2026-09-10 — exp14: the estimation improvement does not reach the band

**Retraction first.** The `exp13` entry said a band whose containment is
guaranteed by construction had been obtained. It had not. The argument needs
$\Pr(A>A_U)\le\eta_1$, and the $s_U$ used was a normal approximation with an
estimated variance covering at **0.963--0.969** against a nominal 0.975. What
`exp13` showed is that the construction behaved conservatively in the conditions
examined, two conservatisms compensating — not that the stated guarantee holds.

**A limit for which the argument does go through.** With $\mu_i$ known,
$\sum_cY_c^2/(A+D_c)\sim\chi^2_K$ exactly, and replacing $D_c$ by the
simultaneous lower limits already needed for the band can only raise the sum. So
with $A_U$ the root of $\sum_cY_c^2/(A+v_{L,c}^2)=\chi^2_{K,\eta_1}$,
$\Pr(E_D\cap\{A>A_U\})\le\eta_1$ and the total is $\eta_1+\eta_2$ — the same
lower limits doing both jobs. Realised coverage 0.9998 to 1.0000 against 0.975.

**And it is built from a pivot, not from the point estimator.** That is what
makes the review's connection question answerable rather than automatic, and the
answer is negative.

| arm | scale-limit coverage (nominal 0.975) | band width over oracle |
|---|---|---|
| `chi2_pivot` | **0.9998--1.0000** | 1.31--2.03 |
| `normal_unw` | 0.962--0.992 | 1.28--1.89 |
| **`normal_gvf`** | **0.900--0.956** | 1.26--1.74 |
| `gw` | 0.940--0.967 | 1.27--1.87 |
| `boot_gvf` (full procedure refitted, B=200) | **0.901, 0.920** | 1.68--1.72 |

**The arm built on the best point estimator has the worst coverage.** `gvf_all`
has the lowest RMSE of any feasible estimator and the interval formed from it
covers at 0.900 in the worst cell. Its variance is smaller and its bias positive,
and the smaller variance wins — a tighter interval around a displaced centre.
**An improvement in point estimation does not propagate to an interval; here it
hurts.** The project has two results, not one, and the write-up must say so.

The bootstrap that refits GVF, weights and subtraction inside the resampling
covers at 0.901 and 0.920. Redoing the whole procedure does not confer validity,
exactly as the review cautioned.

**Where the containment problem actually was.** Containment of the oracle
half-width is 0.989--1.000 for *every* arm here, including those whose scale
limit undercovers, because all of them substitute the simultaneous lower limits
$v_{L,c}$ in the band. In `exp13`, substituting $\widehat v_c$ gave 0.940. So the
containment failure was the design-variance substitution, not the scale limit.
Fixing the scale limit is what makes the guarantee derivable; it is not what was
breaking containment. Two separate problems that had been running together.

**The price of validity is small.** The valid arm is 4 to 20 percent wider than
the narrowest invalid one, and every arm covers the latent target at 0.985 or
above against a guaranteed 0.90.

**The $O(1/K)$ rate is now tested rather than asserted.** $|$bias$|$ of
`gvf_all` runs 0.0874, 0.0518, 0.0227, 0.0123 at $K=60,120,240,480$; the slope of
$\log|$bias$|$ on $\log K$ is $-0.966$. Consistent with $O(1/K)$. The theoretical
justification is still owed.

**The leverage stress failed, and the test was wrong rather than the concern.**
Heavy-tailed $n_i$ raised the largest leverage from 10.8 to 95.0 times the median
and the bias *fell*, 0.033 to 0.018. With $D_i=c\,e_i/n_i$ and the ratio smoother
$\widehat c=\overline{\widehat D_jn_j}$, the product $\widehat D_jn_j$ is free of
$n_j$, so leverage is uniform in $n$ by construction however dispersed $n$ is.
The cell stressed the design variable, not the smoother. The review's concern
about uneven smoother influence is still open.

**Also corrected in the memo.** The 0.5--1.9 percent cost of estimating the
design variances now carries $\nu=10$ beside it and the bound
$\sqrt{1+\rho^4/\nu_{\min}}$: 3.15 percent at $\nu=10$, 7.7 at $\nu=4$, 14.9 at
$\nu=2$. It does not transfer to a small area with four PSUs. And "cross-fitting
is not what pays" is narrowed to this model and grid.

## 2026-09-10 — exp15: the diagnosis reverses the previous entry

**The explanation in the `exp14` entry was wrong in direction.** It attributed
the GVF upper limit's undercoverage to "positive bias and smaller variance, a
tighter interval around a displaced centre". For a **one-sided** upper limit
failure is $(\widehat A-A)/\widehat{se}<-z$, a left-tail event, and with
$\widehat A=A+b+\sigma Z$ at known $\sigma$ coverage is
$\Phi(z+b/\sigma)$ — a positive bias *raises* it. The cause was unidentified,
and asserting a negative result on top of a wrong mechanism was the error.

**The actual cause is a random denominator correlated with the numerator.** The
standardised error has 2.5 percent quantile $-2.37$ to $-3.25$ against $-1.96$.
With the variance evaluated at the *true* $D_i$ — a denominator that does not
move with the data — the tail is *lighter* than normal ($-1.54$ to $-1.72$) and
coverage is 0.989 to 0.996. $\widehat{se}$ and $\widehat A$ are built from the
same $\widehat D_i$, so the interval contracts exactly on the replicates where
$\widehat A$ is low. A studentisation problem, not a bias problem.

Two contributing defects, both real and both smaller. The variance was evaluated
at the smoothed $\widetilde D_i$: mean $\widehat{se}$ over realised standard
deviation is 0.891--1.004 there against **1.007--1.040** at $\widehat D_i$, and
correcting the argument alone lifts coverage from 0.911 to 0.952. A
delete-one-population jackknife over the whole procedure gets the magnitude right
(0.972--1.038) and does not fix the tail, so it reaches only 0.919--0.959.

**And most of the defect was the resampling form.** `exp14` used a *basic* upper
limit at $B=200$, where the 2.5 percent tail rests on about five replicates.
Percentile at $B=2{,}000$: **0.953, 0.960, 0.973, 0.988** against a nominal
0.975, Monte Carlo error 0.0078. At $K=200$ it is at nominal.

**The corrected limit is also far tighter than the pivot.** Mean $A_U$ on
identical replicates at true $A=1$: pivot 4.39--5.66, percentile bootstrap
1.79--2.73, a ratio of 0.38--0.47. The pivot covers at 1.000 and spends almost
none of its budget.

**So the previous entry's conclusions are withdrawn.** "An improvement in point
estimation does not propagate to an interval" and "one procedure cannot do both"
were both built on a mis-specified comparison: a badly chosen resampling limit
against a very conservative pivot, with a wrong mechanism attached. What stands
is narrower — the constructions tried in `exp14` were poor, and a correctly
formed one is valid to within Monte Carlo error at $K=200$ and 2.5 times tighter.

**Not measured yet, and it is the next thing.** The *band* built on the
percentile-bootstrap limit. `exp14` reported band widths for the pivot only.

**Three labelling corrections adopted from the same review.** The pivot's
derivable unconditional guarantee is $1-\eta_1-\eta_2=0.95$, not the 0.975 each
arm targets. The pivot needs **normality**, not assumption (S) — standardised
curves sharing a law does not give $\sum_cW_c^2\sim\chi^2_K$. And the claim that
the containment failure was the design-variance substitution *and not* the scale
limit is weakened to what the evidence supports: a conservative $v_L$ compensated
for an undercovering $s_U$ in the conditions examined, and a conservative lower
limit can mask a failing upper one.

**The unknown-mean extension is verified.** With
$Q(a,\mathbf D)=\min_\beta\sum_c(Y_c-x_c^\top\beta)^2/(a+D_c)$ refitted at each
candidate $a$: mean and variance of $Q(A,\mathbf D)$ match $\chi^2_{K-p}$ to
Monte Carlo error, Kolmogorov--Smirnov $p$ 0.10 to 0.55, and the resulting limit
covers. It bounds the variance component only — not the error from centring the
band on an estimated mean, nor exchangeability of the scores under an estimated
centre.

**And the normal-model comparison the pivot now obliges.** Given the same $A_U$,
$\eta_1,\eta_2$ and $\alpha_0$, the conformal band is 7 to 14 percent narrower
than the normal-model interval — the $\rho^2$ damping again. Both are grossly
conservative on the pivot limit, so this comparison should be repeated on the
corrected limit before being used for anything.

## 2026-09-10 — exp16: the tighter limit is worth 3 to 14 percent, and the pivot should be the method

The work order was: put the percentile limit into the final band, compare it
against the pivot band and against a normal-model interval on the *same* limit,
report the four quantities linked, keep the small-$K$ cells that failed, and
separate the two things `exp15` changed at once. All done, 2,000 outer
replicates at $B=2{,}000$.

**W1 — the review's warning was the decisive one.** A scale limit 1.5 to 2.5
times tighter buys **3 to 14 percent** of band width. The realised gain is
smaller even than the $\sqrt{\cdot}$ bound, because the elasticity
$L_c/\{2(A+L_c)\}$ runs 0.20 to 0.36 rather than its maximum of $1/2$. Reading
the width ratio off the mean-limit ratio would have overstated the gain twofold.
The gain tracks the design share, not $K$: 12 to 14 percent at $\bar D/A=4$ and
3.3 percent at $\bar D/A=1$.

**W2 holds, W3 falsified.** Latent-target coverage is 0.983 to 0.999 for the
percentile band and 0.986 to 1.000 for the pivot band, against a guaranteed 0.90.
Containment of the oracle half-width is 0.9965 to 1.0000 against a 0.95
requirement, so it does not degrade under the tighter limit. The margins are so
wide in every arm that **the scale limit is not what governs coverage here** —
the oracle band already covers at 0.939 to 0.958 and the $v_{L,c}$ inflation
supplies the rest.

**W4 — and this withdraws an attribution from the previous entry.** From one set
of draws, with the $B=200$ arms reading the first 200 of the 2,000: the
**form** is worth 3 to 8 percentage points, the **count** 0.1 to 0.9. The
previous entry credited part of the improvement to the 2.5 percent tail resting
on about five replicates. Raising $B$ tenfold moves coverage by less than one
point. It was basic-versus-percentile, essentially alone.

**And the percentile limit's coverage does not survive better precision.** At
2,000 outer replicates rather than 400 it covers at **0.939 to 0.968** against a
nominal 0.975 — below nominal in every cell including $K=200$, where `exp15`
reported 0.973 and 0.988 on 400 replicates. So "valid to within Monte Carlo
error at $K=200$" is withdrawn. It is a promising approximation that undercovers
by 0.7 to 3.6 points.

**W5 falsified, and the reversal is instructive.** On the *same* percentile
limit the normal-model interval is **narrower** than the conformal band, ratio
0.776 to 0.981. `exp15` reported the opposite, but measured it on the pivot
limit and flagged that it needed repeating. The normal band has elasticity
exactly $1/2$ in $A_U$; the conformal band's is $L_c/\{2(A+L_c)\}\le1/2$, here
0.20 to 0.36. **The conformal band is less sensitive to the scale limit, so it
wins on a loose limit and loses on a tight one.** Neither dominates, and any
width claim must name the limit it was measured on. Both earlier statements of
this comparison were made without naming it.

**The decision.** The pivot's guarantee costs 3 to 14 percent of band width
against an approximation that undercovers its own nominal level. **The $\chi^2$
pivot should be the method and the bootstrap a reported alternative** — the
opposite of where the previous entry was heading, and the difference came from
measuring the band instead of the limit.

**What keeps this provisional.** Independent normal population model, scalar
target. The coverage margins are wide enough that they may not discriminate
between constructions in a harder setting. Nothing has been through a
finite-population complex-sample experiment, and that is now the next thing:
there is a procedure to take there.

## 2026-09-10 — three corrections to the exp16 write-up, before moving on

**The square root was labelled without a direction.** For $A_1\le A_2$,
$\sqrt{A_1/A_2}\le h_c(A_1)/h_c(A_2)\le1$, and an order statistic preserves a
common positive factor, so $R(A_1)/R(A_2)\ge\sqrt{A_1/A_2}$ **per replicate**.
The square root is a *lower* bound on the width ratio — an upper bound on the
achievable narrowing — not an upper bound on the ratio. And the column applied
it to the *mean* limit ratio, which is a reference point, not a bound on the
mean width ratio. Both now stated correctly, with the per-replicate version
marked as the proved one.

**"3 to 14 percent" was quoted without fixing a denominator.** At $r=0.861$ the
percentile band is 13.9 percent narrower and the pivot band is 16.1 percent
wider. All ratios are now stated as percentile over pivot and only the narrowing
is quoted.

**The elasticity argument was overstated.** That the conformal band has a lower
elasticity in $A_U$ is consistent with the observed reversal but does not force
one at any particular limit — the ranking also carries the conformal quantile,
the standardisation and the data distribution. Restricted to the range measured.
Coverage is now printed beside every width comparison, because equal nominal
budgets did not give equal coverage: 0.972--0.991 for the normal interval
against 0.983--0.999 for the conformal band.

**And the framing of the next experiment is corrected.** It does not test
whether the pivot's guarantee holds under a complex design. The guarantee's
conditions — normality of the population-level deviations and a $\chi^2$ law for
the design-variance estimator — are not satisfied there, and a simulation cannot
extend a theorem's scope. The experiment measures how stably the procedure
behaves when its conditions are not met, and which violation moves which
quantity. The earlier prediction that the coverage margin would shrink is
withdrawn as a prediction: it may shrink, grow, or distort in another direction,
and writing the design around an expected direction would be designing toward a
result.

What is fixed is the **baseline procedure to carry forward**, not the paper's
method. The percentile alternative is recorded as an approximation with
0.7--3.1 points of undercoverage and no further variants of it will be tried.

## 2026-09-10 — exp17: the procedure survives a complex design, at a design share that does not test it hard

Framed as instructed: this does **not** test whether the pivot's guarantee holds
under a complex sample. Its conditions fail there and a simulation cannot extend
a theorem's scope. What was measured is stability, and which violation moves
which quantity. No direction was predicted for the coverage margin.

Design: 4 strata $\times$ 20 PSUs $\times$ 10 units, SRSWOR of 5 PSUs per
stratum, $\nu=16$. Estimand one pre-specified CDF point of a finite population;
target a **newly generated** population, not design-based coverage for a fixed
one.

**Three violations, all measured rather than assumed.** Normality of the
standardised deviations fails decisively at the 0.15 quantile — skewness 0.92 to
1.10, excess kurtosis 0.93 to 1.40, KS $p=0$ — and holds to a mild platykurtosis
at the median. The $\chi^2$ law for $\widehat D_c$ is rejected everywhere but in
the **conservative** direction: mean 15.98 to 16.00 against 16, variance 20.5 to
23.1 against 32, so the estimator is 28 to 36 percent less dispersed than
$\chi^2_{16}$ and the Bonferroni lower limits sit too low rather than too high.
And $\mathrm{corr}(\widehat D_c,Y_c)$ is **0.80 to 0.84** at the tail quantile
against 0.00 at the median — the violation `exp09` §7.1 named as specific to a
CDF ordinate, now realised, because the design variance of a proportion is a
function of the proportion and that function is flat at the median and steep in
the tail.

A degeneracy worth recording: at the tail quantile the exact design variance is
sometimes **zero** ($\Pr=2\times10^{-5}$, and $\Pr(\widehat D_c=0)=0.13$ to
0.21 percent). Ten-unit clusters in the tail of a small finite population
genuinely have no within-stratum spread sometimes, and no variance model covers
that.

**X3 holds and it is the important one.** The oracle band — true $A$, true
$D_c$, per-population standardisation — covers at 0.942 to 0.959 against a
nominal 0.950 at a Monte Carlo error of 0.0067. So assumption (S) survives this
design to about $\pm0.008$ and the downstream machinery is not being asked to
repair a broken target. Had this failed, the variance work would have been
beside the point.

**X4 holds for the pivot and fails for the alternative, with a clean
attribution.** The pivot limit covers at 0.953 to 0.998 against its 0.95
guarantee in every cell, including those where normality is decisively rejected.
Fitting the mean — $\chi^2_{K-1}$, refitting the weighted mean at each candidate
$A$ — costs 0.001 to 0.007 and leaves the band unchanged to three decimals. The
percentile bootstrap limit covers at 0.952 to 0.984 at the median and **0.852 to
0.908 at the tail quantile**, which is exactly where the correlation is 0.8 and
where its GVF weights are built from $\widehat F_c(1-\widehat F_c)$, a function
of the estimate itself. Every band still covers at 0.947 or above against the
guaranteed 0.90.

**The width ordering reverses for the third time, and now both ends have been
seen.** Conformal bands are 1.0 to 1.08 times the oracle here and the normal
interval on the same limit is 1.11 to 1.20, so conformal wins — the reverse of
`exp16`. The operating point explains it: $\bar D/A$ is 0.038 to 0.126 here so
the elasticity is 0.02 to 0.06, against 0.20 to 0.36 in `exp16`. **Which
construction is narrower is decided by the design share and neither dominates.**

**And that is also the limitation that matters most.** This design sits at
$\rho^2=0.037$ to $0.112$ — the manuscript's *national* ESS regime, not its
regional one at $\rho^2$ between 0.25 and 0.44. Where the correction is nearly
inactive, adding 1 to 8 percent over the oracle is not a demanding test.
Reaching a regional-like design share needs the between-population spread
reduced or the sample cut, and has not been run. That is the next cell, and the
alternative construction carries a located failure into it.

## 2026-09-10 — exp18: at the design share where the correction matters, the valid procedure recovers a quarter of it

The work order: move to the regional design share by **two separate routes**,
keep the procedures and budget fixed, carry an uncorrected band as a reference,
and compute the lower-limit coverage directly instead of inferring it.

**The design shares reached are the manuscript's regional range**, $\rho=0.41$ to
$0.66$, where the oracle correction is worth 8.8 to 24.5 percent of width. So
this is a real test, unlike `exp17` at $\rho\approx0.1$.

**Y1 holds: the two routes are not the same problem at the same $\bar D/A$.**
Fewer PSUs and smaller clusters give $\nu=4$ or 8 against 16, tail skewness 0.7
to 0.9 against 0.2 to 0.5, and **a fifth of all variance estimates exactly zero**
against none. Reducing the between-population signal changes only $A$.

**The diagnostic `exp17` got wrong, now computed directly.**
$\Pr\{v_{L,c}^2\le D_c\ \forall c\}$ against the 0.975 the containment argument
needs: 0.999 to 1.000 at the median, but **0.834, 0.721, 0.718 and 0.445** at
the tail quantile on the small-sample route. The previous entry inferred these
limits were conservative from a variance smaller than $\chi^2$'s; that inference
was wrong in exactly the cells that matter. The mechanism shows in the $K$
dependence — Bonferroni sets each limit at $\eta_2/K$, so larger $K$ reaches
further into a $\chi^2$ tail that does not describe the estimator, and coverage
**falls** with $K$.

The correlation decomposes as the review said. The pooled 0.8 of `exp17` is a
**between-population** relation of 0.78 to 0.95 between true $D_c$ and true
$F_c$, plus a **within-population** sampling dependence of 0.52 to 0.67.
Different objects, both present.

**Y2 holds.** Pivot band coverage 0.9615 to 0.9860 against a guaranteed 0.90 on
both routes, including cells where the containment premise fails on half the
replicates. Stability, not validity.

**Y4 nearly holds, and the exception is the important one.** The oracle band
covers at 0.9315 to 0.9605 against a nominal 0.950; the worst cell —
small-sample, tail quantile, $K=200$ — is **0.9315, 2.8 Monte Carlo standard
errors low**. The oracle uses the true $A$ and the true $D_c$, so **no variance
work can address this.** It is the first sign in the project of the target itself
failing, and it belongs with `exp01`.

**Y3 fails, and that is the result.** The valid corrected band is **0.9 to 6.6
percent narrower than not correcting at all**, capturing **6 to 31 percent** of
the narrowing the oracle achieves. The mechanism is the guarantee: the band
factor is $\{1+v_{L,c}^2/A_U\}^{-1/2}$, the argument needs $A$ bounded above and
each $v_c$ bounded below, and **both push that factor toward 1, which is no
correction.** The two conservatisms compound rather than offset.

**This lands on the manuscript directly.** Section 6.5 reports the correction
narrowing the band by 15 to 19 percent where it activates. In the cell whose
oracle narrowing is 19.5 percent — the same figure — the feasible, honestly
bounded band achieves **4.9 percent**. The manuscript's number is an oracle-like
quantity computed from plug-in scales, and the price of turning it into a
statement with an error budget is most of the gain.

Protocol outcome 2, reported as prominently as a success would have been: **at
the design share where the correction is needed, the valid procedure is valid
and worth little.** Whether a construction exists that keeps the guarantee and
recovers more of that 6 to 31 percent is now the open question. It is a sharper
question than the one this project started with, and it is the one a paper
should be built on.

**Four interpretations from the previous entry corrected in the memo.** "The
guarantee held although the assumptions broke" becomes an empirical statement
about coverage near the target with its Monte Carlo error attached. "Assumption
(S) survives to $\pm0.008$" is withdrawn — coverage at one nominal level does not
verify a common standardised shape. The inference from a small variance to
conservative lower limits is replaced by the direct computation above. And the
cause of the percentile bootstrap's tail failure is downgraded from established
to a plausible path, since the tail cells change several things at once.

## 2026-09-10 — step 1 of the fixed plan, and a headroom check that redirects step 2

**Step 1 delivered: `docs/CLAIMS_ALIGNMENT.md`.** It separates what stands, what
is now a confirmed limit, what is owed, and what may not be claimed, and lists
five theory/implementation mismatches with the manuscript edit each requires.

The one that matters most for the review's §4: **§6.5's 15–19 percent is a
plug-in ratio of the correction's radius to the anchor's, with no error budget
for the scale.** The number may be right as that comparison. What is not
supported is the sentence built on it — "the correction is therefore worth
having where it is reachable" — because in a matched simulated cell whose oracle
narrowing is 19.5 percent, an honestly-bounded band achieves 4.9 percent. And
"reachable" rests on the frozen gate, which `exp10` showed is not an
error-controlled rule. Both sentences need rewriting; the number does not.

**Before designing the joint-inference candidate, `exp19` measured whether there
is headroom and where.** No method was added: the same band function was
evaluated at mixed arguments.

- Bounding the design variances costs more than bounding $A$ (0.136–0.332
  against 0.074–0.204) in every cell.
- **The multiplicity is only 6 to 22 percent of the current loss**, growing with
  $K$ as expected but minor.
- Removing the simultaneity correction entirely raises the captured share of the
  oracle narrowing from **6–27 percent only to 12–42 percent.**

**So a candidate that only replaces the simultaneity treatment should not be
built** — that was the point of running this before designing. Bounding $A$
alone, with the *true* $D_c$ supplied, already costs 7 to 20 percent. The version
worth designing bounds the band factor $v_c^2/A$ as a single object, which is the
structure the scalar $\kappa$ pivot had and which separate upper/lower bounding
destroys.

**And one observation reframes the target.** The band covers at 0.974 to 0.986
against a guaranteed 0.90 **even when the lower limits cover on 0.05 percent of
replicates**. The sufficient-condition chain is slack enough that breaking a link
barely moves the coverage. The width is not being spent on the coverage achieved;
it is being spent on the argument. **The next construction should be calibrated
to the coverage it claims rather than reaching it through separately conservative
bounds** — a different problem from tightening any one link.

Recorded as the answer to the planned step 3, obtained before step 2 rather than
after, which is what the plan asked for.

## 2026-09-10 — a design error corrected, and the ratio construction works in the exact case

**The error.** The previous report's design sketch said that under
heteroscedasticity the ratios $r_c=D_c/A$ are determined by $A$ together with the
observed $\widehat D_c$, so the confidence set could live on one axis. **False.**
$\widehat D_c/A$ is a plug-in, not the parameter: $\widehat D\approx(1,1)$ leaves
$\mathbf D=(1,1)$ and $(0.5,2)$ both compatible. Holding $\widehat D_c$ fixed and
moving only $A$ excludes most admissible ratio vectors and reintroduces exactly
the fault the construction exists to avoid. `docs/THEORY_ratio_pivot.md` §0
records it and keeps three things apart from here on: a genuinely low-dimensional
model, profiling the nuisance, and substituting the estimate.

**The exact reference case.** With $D_c=d\,a_c$ and $a_c$ a **known** design
quantity, $t=d/A$ is the only unknown ratio parameter, and
$$T(t)=\frac{K\widehat d}{t\,S(t)}\sim F_{\nu,K},\qquad
\widehat d=\frac1\nu\sum_c\frac{\nu_c\widehat D_c}{a_c},\quad
S(t)=\sum_c\frac{Y_c^2}{1+t a_c},$$
exactly, with $t S(t)$ strictly increasing so $T$ is strictly decreasing and
inverts to an exact one-sided lower bound $t_L$. One parameter, one budget, one
bound — against the incumbent's $\eta_1$ for an upper limit on $A$ plus $\eta_2$
for $K$ simultaneous lower limits on the $D_c$, both of which push the correction
toward zero.

**Read in the order the plan fixed — level, containment, then width.**

*Level.* $\Pr\{t\ge t_L\}$ has mean **0.9498**, range 0.9465–0.9538, against a
nominal 0.95 at Monte Carlo error 0.0015. The incumbent's $A$-limit covers at
0.998–1.000 against 0.975 — spending almost none of its budget — while its
Bonferroni limits sit at 0.973–0.978.

*Containment.* $\Pr\{R(t_L)\ge R(t)\}$ equals the level to **machine zero** in
every cell. For this construction containment and level are the same event, and
nothing is lost between them.

*Width.* The ratio band is **9 to 20 percent narrower** than the incumbent, and
sits 2.6–11.6 percent over the infeasible oracle where the incumbent sits
15.0–34.8 percent over it. Every arm covers at 0.955 or above against a
guaranteed 0.90.

**In the units that matter: the incumbent captures 18–38 percent of the available
narrowing; the ratio bound captures 73–89 percent.** `exp18` found the incumbent
valid and worth little at the regional design share. In the exact case, bounding
the ratio directly recovers most of what was being lost, under correct error
control.

**Where the gain comes from, and one prediction wrong.** Mean width ratio by
factor: $K=60$ 0.870 against $K=200$ 0.850; $d/A=0.5$ 0.894 against $d/A=1$
0.826; dispersion of $a_c$ 0.859 against 0.861. The gain grows with $K$ and much
more with the **design share**, and is **flat in the dispersion of $a_c$** —
prediction V4 had that wrong. The Bonferroni step charges for the existence of
$K$ separate limits, not for heterogeneity among them.

**What this is not.** $a_c$ is known, and that is the entire reduction. This is an
exact reference case and a verification, not a survey-ready method and not by
itself a contribution. The question that decides the line is whether the gain
survives when the relative structure must be estimated — specification §3 route
(b), with `exp13`'s finding that GVF misfit returns most of the gain as the
standing warning. $\mathbf D$ was never profiled here.

**Two framing corrections adopted.** `exp19` is a diagnostic that orders the
design options, **not** an upper bound on what any valid joint inference could
achieve — components interact and an invalid multiplicity-free procedure need not
be narrower than every valid joint one. And "calibrate to the claimed coverage"
now distinguishes reducing theoretical conservatism, which is a validity
argument, from tuning width down on a generative model, which is not.
Over-coverage in some conditions is acceptable; the aim is removing unnecessary
width while keeping validity.

## 2026-09-10 — exp21: the gain is pooling, and the structure assumption is the condition

The work order was to run the matched-information comparison **before**
extending to an estimated structure, so that the `exp20` gain could be split into
pooling and direct ratio inference. Doing it in that order changed the answer.

**A bug found and fixed before reading anything.** A dictionary key collision
overwrote the confidence-set coverage of $C_\gamma$ with the latent-target
coverage of the band built from it, so the first run's "0.956--0.972" was not that
quantity. The interval was then verified in isolation at 200,000 draws (0.9746
against 0.975) and the whole experiment rerun.

**$C_\gamma$ is exact.** $W(\gamma)$ is linear increasing in $\gamma$, so the set
is the closed-form interval $\widehat\gamma\pm w\sigma_\epsilon/\sqrt{S_{xx}}$
with $w$ from a null law free of both $d$ and $\gamma$. Realised coverage
0.9716--0.9777, mean **0.9752** against 0.975 at Monte Carlo error 0.0016. The
supremum over $C_\gamma$ was grid-insensitive (31 against 61 points differed by
0.0000) and the corrected $t_L=0$ fallback was never needed.

**U2 holds decisively, U3 largely fails, and that relocates the contribution.**
Share of the available narrowing captured:

| construction | captured |
|---|---|
| incumbent, per-population limits with Bonferroni | 0.20--0.31 |
| **same, but given the known $a_c$** (one exact limit for $d$) | **0.63--0.80** |
| ratio bound, same known $a_c$ | 0.74--0.86 |
| $C_\gamma$ construction, structure estimated | 0.63--0.80 |

Giving the incumbent the same structure information moves it from 0.20--0.31 to
0.63--0.80. Bounding the ratio directly then adds 0.06--0.11 — a width ratio of
0.958--0.987, **between 1.3 and 4.2 percent**. So `exp20`'s 9--20 percent was
almost entirely **pooling**, not the ratio idea. The review asked for exactly
this separation before the contribution was named.

**And paying for the structure costs back the ratio step.** $C_\gamma$'s
containment is 0.983--0.986 against its 0.95 requirement, and its captured share
lands back at 0.63--0.80 — where `sep_struct` already was. Against the incumbent
the band is 0.817--0.926, i.e. **7 to 18 percent narrower**.

**The condition, measured rather than assumed.** Under correct specification the
plug-in $a_c(\widehat\gamma)$ is fine (containment 0.944--0.949), so the
prediction that it undercovers generally was wrong. Under misspecification it
falls to **0.821--0.898**, and $C_\gamma$ degrades more gracefully but still
fails, **0.899--0.964**, below its requirement in half the cells — while the
incumbent, which assumes no structure, stays at 1.000.

**So the claim is now:** using a relative variance structure, with its estimation
uncertainty paid for by a confidence set rather than removed by substitution,
takes the captured share from 0.20--0.31 to 0.63--0.80 and the band to 7--18
percent narrower than the incumbent — **conditional on the structure being
correctly specified**, with a measured failure mode when it is not. That is a
smaller and different claim than the previous entry pointed toward, and it is the
one the evidence supports.

Not yet touched: any of this under a complex design, where neither the $\chi^2$
law for $\widehat D_c$ nor the normality of $Y_c$ holds and where `exp18` found
the incumbent's own lower limits covering at 0.445.

## 2026-09-10 — exp22: the algorithm closes, and the main method is fixed

Route (b) kept; route (a) not opened. Two closing jobs, no new candidates.

**Job 1 — the supremum becomes two evaluations, and half of it is a theorem.**
$\partial_\gamma\log a_c(\gamma)=\bar\ell(\gamma)-\log x_c$ with
$\bar\ell'(\gamma)=-\mathrm{Var}_w(\log x)\le0$, so $\log a_c$ is **concave** in
$\gamma$ and its minimum over an interval is attained **at an endpoint,
exactly**. With $R$ decreasing coordinatewise in $t\,a_c$ that yields a certified
envelope dominating $R(t_L(\gamma),\gamma)$ for every $\gamma\in C_\gamma$, not
just the grid points — verified at 100 percent of replicates — for a width cost
of **0.5 to 1.9 percent**.

The step still owed is $\inf_\gamma t_L(\gamma)$: its grid minimiser is at an
endpoint on **0.9999 to 1.0000** of replicates, so the computation needs only
$\gamma_L$ and $\gamma_U$, but that is evidence and not a theorem. It is the one
remaining item on this construction and is recorded as such.

**Job 2 — the matched comparison the review required.** With both sides
estimating the structure and the same total budget, the ratio envelope is
**0.7 to 2.3 percent** narrower than the component-wise construction. Captured
share: envelope 0.53--0.78, component-wise 0.53--0.75, structure-free incumbent
0.20--0.31.

**So the matched comparison settles the attribution.** The substance is using a
variance structure and paying for its estimation; the ratio formulation is a
refinement worth one or two percent. That is the claim the paper can make, and it
is smaller than the ratio idea looked when it was compared only against the
Bonferroni incumbent.

**Main method fixed: the ratio envelope**, chosen on provability rather than
width — two budget pieces against three, a shorter chain, and the one unproved
step shared by both. **The component-wise version is retained and reported**
because it degrades more gracefully under misspecification (containment
0.958--0.992 against the envelope's 0.930--0.981), which the width comparison
does not show and which is a real reason to prefer it.

**Misspecification is written as model error, not estimation error.** $C_\gamma$
answers how precisely $\gamma$ was estimated; when no $\gamma$ describes the
truth there is nothing for it to cover. Containment falls below 0.95 in three of
eight cells for the envelope while the structure-free incumbent stays at 1.000.
Latent-target coverage nonetheless holds at 0.960--0.977 against a guaranteed
0.90, so the failure is absorbed by downstream slack — not something to rely on.

**Three corrections to the previous entry, adopted.** "The plug-in is fine when
correct" is too strong: 0.944--0.949 is below the 0.95 requirement by more than
Monte Carlo error, so it becomes "the departure was small under a correct
structure". The three probabilities — structure-set coverage, oracle containment,
latent-target coverage — are now printed side by side in every table, after the
key collision that made that necessary. And `exp21`'s last row is read both ways:
the method that must estimate the structure lands where the method given it
already sat, verified here paired on the same replicates rather than by comparing
ranges.

**Next, as instructed:** the fixed method goes to the two complex-survey routes
of `exp18`, which differ at matched $D/A$ in degrees of freedom, zero-variance
rate and estimate--variance dependence, to ask whether the structure model
describes real design-variance patterns and whether the gain survives in coverage
and width.

## 2026-09-10 — exp23: the endpoint claim is retracted and the computation is certified

**Retraction.** The previous entry evaluated $\inf_{\gamma\in C_\gamma}t_L(\gamma)$
at the two endpoints because the grid minimiser landed there on 0.9999--1.0000 of
replicates. **A counterexample supplied in review reproduces exactly.** With
$K=6$, $\nu_c=8$, $C_\gamma=[-0.59651,0.34495]$ and the tabulated data,
$t_L(\gamma_L)=0.10974$ and $t_L(\gamma_U)=0.12106$ but the interior minimum is
$t_L(-0.18321)=\mathbf{0.09121}$ — the smaller endpoint is **20.3 percent above**
it. The endpoint property is proved for $a_c(\gamma)$ and **does not transfer** to
$t_L(\gamma)$, which is the solution of an $F$ inversion with both the variance
estimates and the observations in it. A rate of 0.9999 was never a theorem and the
remaining $10^{-4}$ is what a universal claim needs.

**The fix is a bound, not a better search.** $\Phi(t;\gamma)=\sum_c
tY_c^2/\{1+ta_c(\gamma)\}$ is increasing in $t$ and decreasing in each $a_c$.
Replacing $a_c(\gamma)$ by the exact endpoint minimum $\underline a_c$ gives
$\bar\Phi\ge\Phi$ for every $\gamma$; and $1/a_c(\gamma)=K^{-1}\sum_j
(x_c/x_j)^\gamma$ is a positive sum of exponentials, so $\widehat d(\gamma)$ is
**convex** and a one-dimensional convex minimisation *certifies*
$\underline d$. Then
$\bar\Phi(t_L(\gamma))\ge K\widehat d(\gamma)/q\ge K\underline d/q$ gives
$t_L(\gamma)\ge\bar\Phi^{-1}(K\underline d/q)=\underline t_{\mathrm{cert}}$ for
every $\gamma$ in the set — no branch-and-bound, and **cheaper** than the grid it
replaces (two structure evaluations, one convex minimisation, one inversion,
against 31 $F$ inversions).

Verified before use: 0.08924 against the counterexample's true infimum of
0.09121; **zero violations** over 300 random configurations with a 401-point
reference grid at relative tolerance $10^{-9}$; tightness median 0.941, 5th--95th
0.796--0.990. A coarser first pass at 3,000 cases showed one apparent violation
that did not survive a finer reference and is recorded as an artefact of the
reference.

**The numbers, restated.** The certified envelope dominates the retracted grid
computation on 100 percent of replicates and costs **0.7 to 2.9 percent** of width
against it — more than the 0.5--1.9 percent claimed before, as it must, since
$\underline t_{\mathrm{cert}}$ sits below the true infimum. The $\underline t=0$
fallback was never used.

Correctly specified: structure-set coverage 0.972--0.978 against a nominal 0.975,
containment 0.995--0.999 against 0.95, latent-target coverage 0.961--0.977 against
a guaranteed 0.90. **Levels were derived in the restricted model and the
simulated values agree within Monte Carlo uncertainty** — which is the way to
write it, rather than "all requirements met".

Width: the certified construction captures **0.574 to 0.768** of the available
narrowing where the structure-free incumbent captures **0.205 to 0.306**, and its
band is **6.5 to 16.5 percent narrower** than that incumbent. It stays 0.4 to 1.5
percent narrower than the component-wise construction.

**And the main-method choice now rests on something stronger than width.** The
component-wise arm's supremum is still computed on a grid and is **not
certified**: its band depends on $\gamma$ through $d_L(\gamma)$, $a_c(\gamma)$ and
$A_U(\gamma)$ at once, and admits no analogous bound. The ratio form is the one
whose supremum can be computed with a guarantee. That, not the one to two percent,
is why it is the main method.

**Unchanged:** containment under a misspecified structure family is 0.941--0.989
for the certified arm, below requirement in one of eight cells, against 1.000 for
the incumbent that assumes no structure. A confidence set for $\gamma$ is not
protection against the family being wrong.

Nothing further is owed on the computation. Next is the complex-survey step, for
which `exp18`'s two routes are already built.

## 2026-09-10 — exp24: the structure route does not pay under a complex design

Certified numerics finished first, as instructed. **A value returned by an
optimiser is not a lower bound**, so the implementation no longer uses one:
$\widehat d'$ is increasing by convexity, its sign at the endpoints decides the
exact endpoint cases, and otherwise a bisection on $\widehat d'$ brackets the
minimiser with the supporting line at the bracket's left end giving the bound.
Every returned quantity is shrunk by a relative $10^{-9}$ and the monotone
inversion returns its lower bracket end. Zero violations over 400 stress
configurations; tightness median 0.941, 5th--95th 0.797--0.990 — the same as the
uncertified ternary version, so rigour cost nothing here. The "only form that
admits a certified computation" claim is narrowed to: among the constructions
implemented here, the one for which such a bound has been obtained.

**Then the fixed method went to the two complex-survey routes.** Populations were
given different numbers of sampled PSUs so an exogenous structure variable
exists, $x_c=m_c$, fixed before running. A sign error in one diagnostic —
comparing $[\gamma_L,\gamma_U]$ against the regression slope instead of
$\gamma_{\mathrm{ls}}=-\text{slope}$ — was found and fixed before anything was
read.

**Structure explanatory power.** $R^2$ of $\log D_c$ on $\log x_c$ is
**0.63--0.79 at the median** and **0.17--0.26 at a tail quantile**, where the
design variance of a proportion is dominated by $p_c(1-p_c)$ and the cluster
structure that $d\,x_c^{-\gamma}$ does not carry. The best-fitting exponent is
1.14--1.56 and its replicate-to-replicate standard deviation reaches 5.5 at the
tail.

**The inference stage fails, and the contrast locates why.** Certified
containment runs **0.366--0.989** against a 0.95 requirement, and is worst — 0.37
at $K=200$ — in exactly the cells where $C_\gamma$ contains the best-fitting
exponent on 99 percent of replicates. So the failure is **not** that $\gamma$ was
estimated badly; it is that even the best-fitting $\gamma$ leaves a third of
$\log D_c$ unexplained. **Whether the structure confidence set covers the
best-fitting exponent does not diagnose whether the structure model is
adequate.** The $\underline t=0$ fallback never fired, so it is not a
computational failure either.

**Final performance.** Latent-target coverage holds — certified 0.943--0.963
against a guaranteed 0.90 — but that is **empirical conservatism, not the
restricted-model guarantee transferring**: the intermediate containment event
fails on up to 63 percent of replicates while the final coverage does not,
because the chain has slack downstream. And the width advantage over the
structure-free incumbent falls from **6.5--16.5 percent in the closed model to
0.2--4.1 percent here.**

Two of sixteen cells report a captured share above 1. That is the band falling
*below* the oracle where containment is 0.37, and it is kept in the record
because it marks where the capture statistic stops meaning anything.

**So: protocol outcome 2, reported as prominently as a gain would have been —
on this design, using a variance structure does not pay.** The binding cause is
the structure family's explanatory power, not the estimation of its parameter.

One limitation bounds the reading the other way: the design shares reached here
are 0.05--0.26, so the available narrowing is 1.2--15.5 percent to begin with.
A regional-share version of this design has not been built, and whether the
conclusion changes there is not known.

## 2026-09-10 — exp25: the range completes, and it corrects the previous entry

The method, structure variable and budget were fixed and unchanged. **Realised
$\bar D/A=0.541$ to $0.752$, $\rho^2=0.351$ to $0.429$** — the agreed targets and
`exp18`'s regional range. The $\underline t=0$ fallback fired on no replicate.

**The applicable range splits by route, and that is the result.**

On `low_signal` ($\nu_c$ 12--28, no zero variance estimates, structure $R^2$
0.59--0.85): containment **0.955--0.992** against its 0.95 requirement, coverage
0.958--0.971 against a guaranteed 0.90, band **0.883--0.937** of the
structure-free construction — 6.3 to 11.7 percent narrower — capturing 0.56--0.74
of the available narrowing where that construction captures 0.23--0.30.

On `small_sample` ($\nu_c$ 4--8, up to 17 percent of variance estimates exactly
zero, structure $R^2$ 0.05--0.71): containment falls to **0.681--0.780** at the
tail quantile. The width figures there are not usable, because the band is not
containing what it is meant to contain.

**This corrects the previous entry.** `exp24` reported the width advantage
collapsing to 0.2--4.1 percent; here it is 6.3--16.4 percent. The difference is
the design share — `exp24` sat at 0.053--0.262, where the *whole* available
narrowing was 1.2--15.5 percent. **`exp24` was measuring a regime with little to
win, not a method that does not work**, and stopping there would have produced
the wrong conclusion. The instruction to finish the high-share range was the
right call and the record should say so.

**The true-structure diagnostic separates the two explanations, and the answer is
both.** Supplying $a_c^{\mathrm{true}}=D_c/\overline D$ as known — infeasible on
real data, diagnostic only — raises containment on the harsh route from 0.682 to
0.815 and from 0.770 to 0.888, **and does not reach 0.95**. So approximating the
variance structure is a major part of the failure and not all of it: normality of
$Y_c$, the $\chi^2$ law for $\widehat D_c$ and their independence also fail
there, and better structure modelling alone would not close the gap. On the
well-behaved route the true-structure arm sits at 0.937--0.952, slightly *below*
the certified arm, which pays for $C_\gamma$ and is more conservative — the
expected ordering, confirming the structure step is not what binds there.

**Zero-variance populations recorded, not repaired.** $\Pr(D_c=0)$ up to 0.0033
and $\Pr(\widehat D_c=0)$ up to 0.171 on the small-sample route. The diagnostic
arm is undefined when any $D_c=0$, so replicates containing one are excluded from
**that arm only**, at 0.000 on `low_signal` and up to 0.483 at `small_sample`,
tail, $K=200$. Nothing substituted, no other arm affected.

**Two reporting corrections adopted.** Coverage and realised width are printed
first and the capture share is secondary, since its denominator is small wherever
the uncorrected and oracle widths are close. And a band narrower than the oracle
is not by itself invalid — the oracle uses the true scale as a reference and has
not been shown to be the narrowest valid band; what forbids reading `exp24`'s
capture above 1 as an improvement is the containment of 0.37 in the same cells.

**And one causal claim narrowed.** "The binding cause is the structure family's
explanatory power" is withdrawn: containing the best-fitting exponent did not
restore containment, which rules out estimation error in $\gamma$, but the same
designs break normality, the $\chi^2$ law and independence at once. `exp25`'s
diagnostic then showed the structure is a major but not sole cause.

**The applicable range is now fixed and no further conditions will be searched
with this method:** $\rho^2\approx0.35$--0.43, roughly 12 or more design degrees
of freedom per population, no zero variance estimates, and a structure model
explaining about 0.6 of $\log D_c$ or better — there, 6 to 12 percent narrower
than a structure-free construction with containment and coverage intact.

## 2026-09-10 — manuscript reconstruction begins; positioning fixed

Experiments stop here. Three corrections applied to the `exp25` write-up first.

**"The applicable range, fixed" becomes "the verified scenario range".** Writing
"degrees of freedom of 12 or more and a structure $R^2$ above 0.6" as an
operating rule would be wrong three times over: those numbers co-occurred in
these scenarios rather than being derived or tested as thresholds; the structure
$R^2$ is computed from the *true* $D_c$ and is not available in real data; and
nothing proves normality or the $\chi^2$ law under any complex design. The two
routes also move degrees of freedom, sampling distributions and structure fit
together, so their separate contributions are not identified. Reporting the
simulation accurately does not require inventing a usage threshold.

**The true-structure diagnostic is not a full causal separation.** It supports
exactly two statements — the structure step affects the outcome, and improving it
alone would not repair the procedure — and the residue is **not** apportioned
among normality, the $\chi^2$ law and independence. The low-signal ordering, where
the true-structure arm sits slightly below the certified arm, is reported as
consistent with conservatism from carrying estimation uncertainty masking other
approximation error, and not as an established cause.

**And the comparison was rerun with every arm scored on the subset the diagnostic
can use.** On that subset the certified arm's containment is 0.676--0.992 against
0.682--0.992 on all replicates, and the contrast is unchanged: 0.676 against
0.815, 0.771 against 0.908. The exclusion does not carry the finding.

**Positioning fixed — `docs/CONTRIBUTION.md`.** The nearest prior work is
[arXiv:2608.02766](https://arxiv.org/abs/2608.02766) (August 2026), conformal
confidence intervals for small area estimation. The contrast is sharp and
favourable: it targets an **in-sample** area's latent parameter and reaches
validity *precisely by not estimating the sampling variances* — "no need at all
to estimate the sampling variances" — absorbing both components into a shrinkage
score with no deconvolution. That is a good answer to its question and
unavailable for ours: **an unobserved population has no direct estimate to
shrink**, so the latent scale must be recovered from the observed populations,
and recovering it *is* the deconvolution. The two papers are complementary and
the manuscript will say so.

Out-of-sample area prediction is otherwise handled by synthetic estimation
(Rao & Molina 2015), which drops the random effect and is described in that
literature as risky. **What is missing is an interval for that target that
accounts for the uncertainty in the latent scale it must use.**

Novelty is explicitly **not** claimed for the Fisher information of a variance
component, the $\chi^2$/$F$ theory, the conformal rank argument, variance
smoothing, or taking a supremum over a confidence set. The contribution is the
chain: an information analysis identifying *which* quantity must be precise, a
construction carrying that quantity's uncertainty to the band with a computable
bound, and measured operating conditions.

Two items remain and neither is a new method: a comparison against a construction
that shares the target, and a real-data analysis on the scalar target.

## 2026-09-10 — exp26: the same-target comparison, and a prediction of mine that was wrong

**Two corrections to the positioning first.** The Zhang & Tuoto abstract was read
directly and confirms the target difference in their own words — "confidence
intervals of the unknown expectations of the **in-sample** outcomes ...
conditional on the realised sample". The further claim that their method needs no
estimate of the sampling variances came from a full-text summary that **has not
been independently checked**, and `docs/CONTRIBUTION.md` now carries a
verification note saying the sentence, its location and its premises must be
confirmed before it enters the manuscript.

**And the gap claim is narrowed.** "The literature offers no interval for an
out-of-sample latent target" is false and has been removed: the linear
mixed-model literature does treat prediction intervals for a target containing a
new random effect, with the parametric-bootstrap EBLUP interval of Chatterjee,
Lahiri & Li as the reference point. What is not offered is an interval carrying
the uncertainty of an **estimated relative design-variance structure**, and that
is now the claim — tested here rather than asserted. Also narrowed: an unobserved
population forces a deconvolution *for a correction that rescales by the latent
scale*, not for every possible latent-target interval. And "conformal, therefore
robust" is explicitly disclaimed, since the exact ratio inference rests on a
normal--$\chi^2$ model.

**The comparison.** Both arms predict $\theta_{\mathrm{new}}=\mu+u_{\mathrm{new}}$
— the latent value of a population with no direct estimate — from the same data,
the same structure model and its uncertainty, and the identical budget
$\alpha_0+\eta_\gamma+\eta_t=0.10$. The Gaussian competitor uses the same
certified $\underline t_{\mathrm{cert}}$ and $\underline a_c$, then
$A_U=\bar S/\chi^2_{K,\alpha_2}$ and $\pm z_{1-\alpha_1/2}\sqrt{A_U}$, with the
split scanned and the narrowest valid choice given to it. The arms differ in
exactly one place: $\alpha_0$ buys a conformal rank, or a normal quantile plus a
$\chi^2$ bound.

**G2 was written down before the run and is falsified.** It predicted the
Gaussian arm would be narrower because it exploits a shape the rank step does
not. It is **16 to 28 percent wider**, paired on the same replicates, with both
covering — conformal 0.957--0.978, Gaussian 0.982--0.996, against a guaranteed
0.90. The gap falls from 1.28 at $K=60$ to 1.16 at $K=200$ (G3) and is unchanged
under a misspecified structure (G4).

**The mechanism is the elasticity of §13 again.** The Gaussian band is
proportional to $\sqrt{A_U}$, sensitivity exactly $1/2$; the conformal band
enters through $\{1+\underline t\,\underline a_c\}^{-1/2}$, whose elasticity is
strictly below $1/2$. It absorbs scale uncertainty more gently, and it does not
have to spend part of $\alpha_0$ on a $\chi^2$ bound.

**One qualification that is not small:** this is *one* valid Gaussian
construction with an optimised split, not the best possible. A different route to
$A_U$, or one exploiting the same damping, could close the gap. The claim is
about this comparator.

**Computation does not separate them** — the shared scale machinery costs
0.27--0.80 ms per replicate and the band step 0.0005--0.003 ms for both.

So completion criterion 3 is met in the restricted model: at the same target,
information, centre and nominal level, the proposal is 16--28 percent narrower
than a matched valid comparator that shares the target. **Only the real-data
analysis on the scalar target remains.**

## 2026-09-10 — exp26 corrected, ESS data obtained through the portal API

**Three corrections to `exp26`, all adopted.**

*The reduction is $1-1/r$, not $r-1$.* A ratio of 1.162--1.285 means the Gaussian
comparator is 16--28 percent wider and the conformal band **13.9--22.2 percent
narrower**. Only the second is a reduction and only it is quoted.

*The scope is one constructed baseline.* Not Gaussian methods in general, not
small-area inference in general. And part of the width difference is a
**conservatism difference** — the Gaussian arm realises 0.982--0.996 coverage
against the conformal arm's 0.957--0.978, both nominally 0.90 — so the two are
not calibrated to the same realised level. Nominal levels are now printed for
every arm: 0.90 for the two valid ones, 0.95 for the plug-in, whose realised
0.925--0.948 is short of **its own** level rather than of 0.90.

*The budget split was chosen on the data.* $(\alpha_1,\alpha_2)$ was scanned and
the split minimising the competitor's mean width in each cell was used, which is
generous but is a selection. **A split fixed in advance at $(0.025,0.025)$ is now
reported beside it**: the ratio is then 1.256--1.350, so the conformal band is
20.4--25.9 percent narrower. The data-chosen split is the conservative figure and
the fixed one shows the selection was not doing the work.

**ESS microdata obtained.** The portal at `ess.sikt.no` exposes a beta REST API
with a single endpoint, `GET /v1/data/dataFile/{doiPrefix}/{doiSuffix}`. The
`userId` parameter is **not** authentication — the API's own documentation says
it is for usage statistics — so the End User Licence still applies and each user
supplies their own id. **No id is stored in this repository.**

Rounds 9, 10 and 11 integrated files (`ess9e03_2`, `ess10e03_2`, `ess11e02_0`,
prefix `10.21338`): 127,286 respondents, 75 country-rounds, 31 countries, 825
region-rounds, median 10 regions per country-round. `region`, `stratum`, `psu`,
`prob`, `domain`, `anweight`, `pspwght`, `dweight`, `pweight` all present with
**zero missingness**, so the design-file condition `exp02` verified holds for the
API files too. `experiments/fetch_ess.py` scripts the retrieval and caches a
column subset **outside the repository**; nothing licensed is committed.

This makes the ESS half of the analysis reproducible from source for anyone with
an ESS registration, which the inherited analyses were not.

**`docs/PROTOCOL_exp27_ess_scalar.md` is written and fixes everything before any
estimate is computed**: the scalar target $F_{cr}(t_0)$ at $t_0=4$ by rule rather
than inspection, three items chosen in advance for differing heterogeneity, the
structure variable $x_{cr}=$ sampled PSU count carried over unchanged from
`exp24`/`exp25`, the ultimate-cluster variance estimator with
$\nu_{cr}=\#\text{PSU}-\#\text{strata}$, the four comparators, and a Gaussian
budget split **fixed** rather than scanned since on real data there is nothing to
scan against but the outcome.

**And the standing limit is written into the protocol.** ESS has no latent truth,
so **no latent-target coverage is claimed or computed**; a held-out region's
direct estimate carries its own sampling error and is not the latent value.
Coverage is the simulations' job. The real data show what inputs each arm needs,
how far the intervals differ on the same data, and which assumptions the data
support. Also recorded there: the centre is **estimated** in ESS where the theory
assumes it known, and that gap is stated with every number.

## 2026-09-10 — exp27: the fixed procedure on ESS

Everything was fixed in the protocol before any estimate touched the microdata,
and nothing was changed afterwards: target $F_{cr}(4)$ with the threshold set by
rule, three items chosen in advance, structure variable carried over unchanged
from the simulations, one budget for every arm, the Gaussian split fixed rather
than scanned.

**No latent-target coverage is claimed or computed.** ESS has no latent truth.

**Exclusions counted, not hidden.** 18 of 825 region cells have $\nu<2$;
$\widehat D=0$ in 13, 39 and 55 cells for `trstprl`, `stflife` and `happy`,
handled by $v_L=0$, which applies no shrinkage. The $\underline t=0$ fallback
fired in none of the 45 configurations.

**ESS presents the regime the correction is for.** $\widehat\rho^2$ runs 0.25 to
0.68 with ample design degrees of freedom — median 22--29 per region. So this is
`exp25`'s working regime rather than `exp24`'s.

**The normality the pivot needs is supported for one item of three.** Standardised
regional deviations: `trstprl` skew $-0.47$ to $0.62$ and excess kurtosis 0.3 to
4.4; `stflife` and `happy` reach skew 2.30 and 2.81 and kurtosis 12.6 and 17.6.
Reported with their results, not after.

**The structure model describes ESS design variances moderately at best.** $R^2$
of $\log\widehat D$ on $\log x$: `trstprl` 0.12--0.65, `stflife` 0.001--0.57,
`happy` 0.0002--0.47. $\widehat\gamma\approx0.3$--0.7 rather than 1, since PSU
count does not carry the whole design effect. At `happy`, round 9, $n\ge150$ the
fit gives $\widehat\gamma=-0.33$ with $C_\gamma$ excluding zero — design variance
rising with sample size, which is not credible and is a signal the family fails.
**The $R^2$ is a fit to $\widehat D$ and understates the fit to $D$**, since
$\log\widehat D$ carries noise of variance $\psi'(\nu/2)\approx0.074$--0.098.

**Two results on how far the arms differ.**

*The Gaussian comparison reproduces the simulation on real data.* The certified
band is narrower in **45 of 45** configurations, by 3.6 to 31.4 percent with
median 14.6 — inside `exp26`'s 13.9--22.2 percent.

*Against the structure-free construction the answer is mixed, and the split is
predicted by something the analyst can compute.* The ratio runs 0.695 to 1.125.
Correlation between the structure fit and the payoff is $-0.54$: where $R^2<0.20$
(22 configurations) the median ratio is **1.048** — using the structure **costs**
width — and where $R^2\ge0.40$ (15 configurations) it is **0.908**. The quantity
that separates them needs only $\widehat D_{cr}$ and $x_{cr}$, which the
procedure already requires.

**That association was not pre-specified** and is reported as an observed
association in these 45 configurations, not as a rule. Confirming it needs a
survey system not used to find it — the AmericasBarometer replication that
`docs/NEXT.md` has carried from the start.

**Standing qualifications, attached to every number.** The centre is the
estimated country-round share where the theory assumes it known.
$\widehat D_{cr}$ is the design variance of $\widehat F_{cr}$, not of the
deviation from the country estimate, following the manuscript's own construction.
Neither is closed here.

**Completion criterion 4 is now met in the form the data can support**: an
analyst can see which inputs each construction needs, how far the intervals
differ on their own data, that the structure route's payoff tracks a computable
diagnostic, and which assumption holds for which item.

## 2026-09-10 — exp28: the centring mismatch was not a technicality

Recording a limitation is not connecting the theory to the application, so the
mismatch `exp27` noted was computed instead. The design variance of the score
$Y_{cr}=\widehat F_{cr}-\widehat F_c$ comes from the Taylor linearisation of the
deviation, aggregated to PSU totals over the whole country-round and passed
through the same stratified ultimate-cluster estimator. Row sets are identical to
`exp27` — $K$ matches and the uncorrected radii match to machine zero — so the
comparison is like for like. Degrees of freedom stay at the region level, the
conservative choice, stated rather than optimised.

**The variance moves modestly.** $\widehat D^{\mathrm{dev}}/\widehat D$ has median
0.95--0.96 and exceeds 1 in 26--33 percent of cells. By quartile of the region's
weight share the median is 0.99, 0.97, 0.94, **0.84** — the more a region
contributes to the centre it is measured against, the more cancels.

**But the structure model changes character, and this is the finding.** Median
$\widehat\gamma$ goes from 0.531 to **1.140**, and $C_\gamma$ contains
$\gamma=1$ — the elementary $D\propto1/n$ — in **17 of 45** configurations where
before it did so in **none**. The implausible negative estimate at `happy`,
round 9 disappears. The country-level component that does not scale with a
region's own sample size had been inflating $\widehat D$ for small regions and
flattening the fitted exponent. **The mismatch had to be fixed.**

**M4 is falsified: the correction moves the conclusions.**

| comparison | exp27 | corrected |
|---|---|---|
| certified / matched Gaussian | 0.686--0.964, 45/45, median 0.854 | **0.729--1.014, 44/45, median 0.821** |
| certified / structure-free | 0.695--1.125, mixed | **0.459--1.034, 43/45, median 0.830** |
| certified / uncorrected | 0.647--0.953 | **0.422--0.867, median 0.730** |

**The same-target Gaussian comparison is the robust one** — it barely moves,
because both arms are built on the same variance, and its median 0.821 sits with
`exp26`'s simulated 13.9--22.2 percent. The structure-free comparison moves from
mixed to favourable, and **the `exp27` version of it is withdrawn as computed on
the wrong variance.**

**The exploratory diagnostic is downgraded, as instructed.** The correlation
between the structure fit and the payoff falls from $-0.54$ to $-0.30$ and the
$R^2$ range compresses to 0.091--0.225. Beyond that: both quantities are built
from the same variance estimates so part of any association is arithmetic, and a
good structure fit does not imply latent-target coverage, which is not measured.
"A computable criterion for whether to use the method" is withdrawn; it is an
**observable exploratory diagnostic**.

**And what fixing the variance does not fix.** A common estimated centre makes
the scores dependent. Measured from the same influence functions, the mean
within-country correlation among distinct regions is $-0.232$, $-0.116$,
$-0.046$, $-0.029$ for country-rounds with $\le5$, 6--10, 11--20 and $>20$
regions — **almost exactly $-1/(n_r-1)$**, the classical dependence of deviations
from a common mean. Negative, hence the benign direction for a maximum-based rank
statistic, shrinking with the region count, and **not zero**. The conformal rank
argument assumes independence and nothing here supplies it.

**So the ESS analysis's status is fixed:** an application under a stated
approximation — estimated centre, measured dependence of about $-1/(n_r-1)$ —
**with the theorem's guarantee not attached to it.** That is what goes in the
manuscript.

Two further wording corrections adopted: `exp26`'s **fixed** budget split
(0.025, 0.025) is the primary comparison and the data-chosen split is reported
as exploratory; and the four completion criteria are "ready to write", not
"complete", since the manuscript still has to make the connection legible.

## 2026-09-10 — the original result was already in the failures: a scale-sensitivity calculus

The standing objection is that variance smoothing, confidence sets, pivots and
conformal ranks are each standard, and that against a component-wise construction
given the same structure the assembled gain is one to two percent. If the claim
is the assembly, that objection lands. **So the claim is not the assembly.**

**What was sitting unnoticed in the record.** Six results were reported as
separate surprises: §13 (a tighter scale limit buys only 3--14 percent of band
width), §13 again (the normal interval wins on a tight limit), §14 (the conformal
band wins on a loose one), §17 (it wins by 10--12 percent at a low design share),
§23 and §26 (it wins at a matched budget, falsifying a registered prediction that
it would lose). **These are one identity.**

Define the scale elasticity $e=\partial\log R/\partial\log\theta$. For a
deconvolution band $R=q\sqrt{A/(A+L)}$ it is $\rho^2/2$, **damped by the design
share**; for any band proportional to $\sqrt A$ it is exactly $1/2$; for the
uncorrected anchor it is 0. And for that pair, evaluated at a common bound
$A_U$,
$$\frac{R_c(A_U)/R_g(A_U)}{R_c(A)/R_g(A)}=\sqrt{\frac{A+L}{A_U+L}}$$
**exactly** — zero violations in 200,000 random cases. Every reversal is that
factor at a different design share and a different looseness of bound. The
requirement being $\rho^{-4}$ smaller than a variance-component criterion (§13)
is the same statement squared.

**And a sharper consequence.** When the Gaussian arm's bound is built from the
conformal arm's own statistic, as in `exp26`, the bound cancels and the ratio
should depend only on $K$ and the budget split — not on the design share, not on
the variance degrees of freedom. That predicted the invariance `exp26` showed and
could not explain: 0.778--0.784 across all $\rho$, $\nu$ and misspecification at
$K=60$.

**Tested as a pre-registered prediction, and one of three registered claims was
refuted.** `exp29`, fresh grid, predictions written into the protocol before
running.

*P-C passes decisively and is the sharpest test.* Across six budget splits
spanning a factor of 1.32 in the predicted ratio, the error is **identical to six
decimal places** (1.2774 percent). The functional dependence is exact.

*P-A fails.* Registered tolerance 5 percent, worst cell **7.07 percent**. The
failure is one multiplicative constant per $K$: fitting $(c-1)$ on $1/K$ gives
$c\approx1+1.92/K$, and the refined law errs by at most **2.17 percent**. The
source is identified — S4 replaces an order statistic's expectation by the
corresponding quantile, a gap of order $1/K$. The constant is fitted, not
derived; the order-statistic expansion would supply it and that is owed.

*P-B holds asymptotically, not exactly.* Within-$K$ spread 0.0200, 0.0110, 0.0089
against a registered 0.02, but the residual is **systematic in $\rho^2$** — mean
ratio 0.7171, 0.7194, 0.7270 at $\rho^2=0.20,0.45,0.70$ for $K=40$. **The strong
claim that the ratio does not depend on the design share at all is refuted**;
what stands is a dependence an order of magnitude smaller than the quantity's
construction would suggest, vanishing in $K$.

**Why this is the contribution rather than the procedure.** It is a statement
about the problem: which construction is narrowest for a given survey
configuration is decided by the design share and by how loose the achievable
scale bound is, both known before any interval is computed. It gives a reason to
choose a construction that does not rest on trusting a simulation, and it
explains why the same two constructions change places between settings. The
procedure of §17--§20 becomes an instance built to exploit the damping.

**What it is not.** Not an optimality theorem — it says how two named forms trade
off, not that either is best. Not a property of conformal prediction — the rank
step contributes only $z_p$, and a parametric band built on $\sqrt{A/(A+L)}$ would
inherit the same elasticity. `docs/CONTRIBUTION.md` is rewritten around this and
says both.

**A law stated in advance, tested on a fresh grid and refuted in one of its three
registered predictions is a stronger object than one fitted to the data that
produced it.** The refined form is now itself an untested prediction.
