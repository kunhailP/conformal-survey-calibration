# Protocol — exp06: the claim family

Written 2026-09-09, before executing `experiments/exp06_claims.py`.
Licensed ESS microdata.

## Why

The manuscript characterises when a correction is reachable and finds it mostly
is not. That is a scope result, and a scope result needs a companion showing
what the framework delivers when applied. The available one is a survey-
inference finding, not a political one: **attaching uncertainty to a country's
whole trajectory rather than to one wave pair changes what a repeated survey
certifies, and by a large factor.**

## Construction

For country `c` with observed rounds, the object is the contrast surface
`theta_{a,b}(t) = F_b(t) - F_a(t)` over every ordered round pair `a < b` and
every threshold in the preregistered low-trust core `t in {1,2,3,4}`. Rounds are
independent cross-sections, so each round's primary sampling units are resampled
within its own strata and the contrasts are formed from the resampled curves.

One simultaneous sup-`t` band covers the whole surface: the critical value is
the `1 - alpha` quantile of `max_{a,b,t} |theta*(t) - theta_hat(t)| / s_hat(t)`
over replicates. A claim is certified when the band lies entirely inside it, so
every claim, every sub-span and the reverse direction are read off **one**
coverage event and no further multiplicity correction is spent.

Claims, ordered by strength: **pairwise** (one adjacent pair declines across the
core), **any-pair** (some adjacent pair does), **net** (first-to-last does),
**persistent** (every adjacent pair does). Persistent implies net and any-pair;
net and any-pair are incomparable.

The comparator is a **marginal reading**: the same contrasts certified pointwise
at the same nominal level with no simultaneity over pairs or thresholds. This is
the reading a wave-pair analysis produces.

## Reproduction gate

Required by `docs/PROTOCOL_exp03_regional.md` after that experiment's failure.
The archive reports, for `trstprl` over rounds 9-11 at `alpha = 0.10`: 20 of 30
countries under the marginal reading, 12 any-pair, 6 net, 1 persistent, with the
net six being Austria, Belgium, Estonia, the United Kingdom, Greece and the
Netherlands. **This implementation must reproduce those counts, and that named
set, before any disagreement with it is reported as a finding.** If it does not,
the discrepancy is diagnosed before anything else is claimed.

## What is being demonstrated, and what is not

Demonstrated: the size of the gap between a wave-pair reading and a
trajectory-simultaneous one, on real repeated-survey data, at a fixed level.

Not demonstrated: any substantive claim about political change. The window
contains a pandemic round and a mode transition in several countries, either of
which can produce the shifts the bands certify, and measurement comparability is
assumed rather than established. The certification is a statement about
response distributions under those assumptions, and the manuscript will say so.

## Outcomes

1. **The counts reproduce and the gap is large.** Reported as the framework's
   payoff, with the caveats above.
2. **The counts reproduce and the gap is small.** Then simultaneity costs little
   here and the demonstration is weak; report it and do not build on it.
3. **The counts do not reproduce.** Diagnose before proceeding. No disagreement
   is reported as a finding until the gate is cleared.
