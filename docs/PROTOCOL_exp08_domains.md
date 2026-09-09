# Protocol — exp08: can the boundary be outrun by refining the unit?

Written 2026-09-09, before executing `experiments/exp08_domains.py`.
Licensed ESS microdata, rounds 9-11.

## The question

The boundary requires `K >= 2 / [tau^2 (1 - rho^2)^2]`. A practitioner facing it
has one obvious move: **refine the unit.** Splitting countries into regions, or
into demographic domains, multiplies the number of calibration populations. If
`K` can be raised past the requirement, the correction becomes usable and the
paper acquires the positive case it currently lacks.

But refinement is not free. Smaller domains carry smaller samples, so the design
variance `v^2` rises, so the design share `rho` rises, so the requirement rises
too. The two move together. **Which wins is an empirical question with a
predictable shape, and it decides whether the boundary is an obstacle that can
be engineered around or one that cannot.**

## The prediction, written before running

Let `D` be the number of domains. Then `K = D`, and domain sample size falls as
`n ~ N / D`, so `v^2 ~ D / N`. If between-domain dispersion `s_G^2` is roughly
stable under refinement, then

    1 - rho^2 = s_G^2 / (s_G^2 + v^2)  ~  1 / (1 + cD),

so the requirement `2 / [tau^2 (1-rho^2)^2]` grows like `D^2` while the supply
`K` grows like `D`. **Refinement should therefore lose, and lose at an
increasing rate.** If that holds, the correction cannot be reached by
subdividing the unit, and the reason is structural rather than a property of
this survey.

The prediction fails if between-domain dispersion grows fast enough under
refinement to hold `rho` down. That is possible: finer domains may be more
heterogeneous, not less.

## Design

Domains of increasing fineness, all nested in country, estimand held fixed as
the domain's departure from its own national distribution, `trstprl`, low-trust
core, Rao-Wu-Yue resampling at `(stratum, psu)`, `B = 400`:

1. country (the national unit, for reference)
2. country x sex
3. country x age band (4)
4. country x age band x sex
5. country x region
6. country x region x sex

Minimum domain size swept over {40, 60, 100}. For each, record `K`, `rho_hat`,
`D`, the requirement implied by the boundary, and whether the gates open.

## What each outcome means

1. **Requirement outruns supply at every refinement.** The boundary cannot be
   engineered around by subdividing, and the paper states that as its main
   practical finding. The correction is unreachable in this survey system for a
   structural reason, not an incidental one.
2. **Supply outruns requirement somewhere.** That configuration is the positive
   case the manuscript lacks, and the boundary becomes a design instruction:
   refine to here and no further.
3. **Neither, because dispersion behaves irregularly across domain types.** Then
   the relationship is reported as observed and no general claim is made.

Every domain definition and size threshold is fixed here. None is dropped after
its result is seen, and the full sweep is written to disk.
