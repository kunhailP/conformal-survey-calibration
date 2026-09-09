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
