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
