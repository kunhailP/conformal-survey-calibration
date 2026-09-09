# Scope

## The question

When distributions estimated from several probability samples are used to
predict a distribution in a further population, what is guaranteed, about which
object, under which assumption?

## Targets

- **T1, observed.** A further *survey estimate*. Reached by exchangeability of
  observed curves alone, in finite samples.
- **T2, latent.** The *population distribution* behind it. Requires either a
  sampling-error bound (shape-free, wide) or a distributional shape assumption
  (efficient, fragile).

The two are not interchangeable and the manuscript never converts one into the
other without naming the assumption that does it.

## In scope

1. Target-specific statements for each construction.
2. The operating conditions of one deployed adaptive implementation, including
   the deterministic floor of its reliability diagnostic.
3. A sensitivity analysis isolating the shape assumption from scale estimation.
4. Survey applications characterising when the correction is inactive, when it
   activates, and what activation does and does not certify.

## Out of scope for this manuscript

- Adjudicating any substantive theory of political change. The applications
  characterise operating conditions; they are not a reanalysis of a debate.
- The within-country simultaneous claim family and its closed-testing
  prevalence bound. Held for separate treatment; see `docs/RESEARCH_LOG.md`.
- Design-based guarantees conditional on a named country or region. The
  guarantee is marginal over populations.
- Any claim of superiority over existing noisy-calibration or small-area
  methods. No matched comparison has been run.

## Standing constraint

Licensed microdata are not redistributable. Any result depending on them is
marked `inherited` in `docs/CLAIMS.md` until re-executed by a holder of the
data, and the manuscript says which results those are.
