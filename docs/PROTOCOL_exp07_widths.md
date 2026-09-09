# Protocol — exp07: what the correction buys, and does the anchor hold?

Written 2026-09-09, before executing `experiments/exp07_widths.py`.

## Why no external head-to-head is run

The obvious benchmarks cover different objects. \citet{yoshimori2014second} give
a second-order-correct interval for a **scalar** area mean in an **observed**
area, asymptotically; \citet{burris2020exact} give exact area-level coverage for
the same kind of parameter. The construction here is a **simultaneous band over
a curve** for a **held-out** population, finite-sample for the observed target
and assumption-dependent for the latent one. A width comparison across different
estimands, populations and guarantee types would not be informative, and
presenting one would invite the objection that incommensurable things were
raced. The positioning is argued in prose instead.

Two comparisons are commensurable and are run here.

## (a) Internal: three constructions, one target, realised radii

In every regional configuration, compute the realised radius of the observed
anchor, the noise enlargement, and the scale correction, all at the same level
on the same calibration set. Report ratios to the anchor.

The archive reported a gain against the **conservative envelope**, and reported
a **scale ratio** rather than a realised width. Neither answers the question a
reader asks, which is what the correction buys over the band a sensible analyst
would otherwise use. That band is the anchor.

Prediction: the gain over the anchor is second order in the design share,
`1 - sqrt(1 - rho^2)`, so at the regional shares of 0.49 to 0.66 the ceiling is
roughly 13 to 25 percent, and the realised gain will be smaller because the
conformal quantiles also differ. If it is small, that is the finding.

## (b) External and commensurable: does the anchor hold under a complex design?

\citet{michal2024model} document that plain split conformal undercovers under
complex survey designs. Our anchor claims finite-sample coverage for the
observed target under exchangeability of the observed curves, which is a
different construction, but the concern transfers and should be tested rather
than argued away.

Leave-one-country-out: calibrate the anchor on the regions of all other
countries, and record the coverage of held-out regions' observed departures,
marginally and conditionally on the held-out country. Report both. Marginal
coverage at or above nominal supports the T1 claim on real data; conditional
coverage is not claimed and is reported so the gap is visible.

## Outcomes

1. **Anchor holds marginally, correction buys little.** The recommendation to
   use the anchor is supported from both sides, and the paper says so.
2. **Anchor holds, correction buys materially where it activates.** Then the
   narrow feasible band identified in Section 4 is worth reaching for, and the
   boundary becomes a planning tool rather than a discouragement.
3. **Anchor undercovers marginally.** Then exchangeability of observed curves
   fails on these data, which would undercut the T1 guarantee the whole paper
   rests on. It would be reported, and it would be the most important result in
   the manuscript.

All outcomes reported. No configuration dropped after execution.
