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
