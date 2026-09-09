# Protocol — exp03: regional transport under corrected resampling

Written 2026-09-09, before executing `experiments/exp03_regional.py`.
Licensed ESS microdata, rounds 9-11.

## Why

The regional construction is the only place the variance correction activates
on real survey data. `exp02` showed the resampling structure it assumes is
violated in fifteen country-rounds, that strata do not nest in regions in 63 of
90, and that twelve countries carry degenerate PSU identifiers. **The activation
result therefore cannot be reported as inherited. It must be recomputed under
correct resampling and allowed to fail.**

## Estimand

For region `g` in country `c` at round `r`, the departure from its own national
distribution, on the threshold grid of `trstprl` (0-10, eleven categories, ten
thresholds `F(t) = P(trstprl <= t)` for `t = 0..9`):

    D_g(t) = F_g(t) - F_{nation(c)}(t)

Weighted by the ESS analysis weight. The coordinate count is `d = 10`: this is
a per-round curve over thresholds, not a trajectory over rounds. The
coordinate-count sensitivity in `exp01` therefore bears on the trajectory
transport, not on this estimand, and the manuscript must not transfer it.

## What changes from the inherited analysis

1. **The resampling unit is `(stratum, psu)`, never `(stratum, psu, region)`.**
   A resampled PSU carries all of its respondents, across whatever regions they
   fall in, so a region-splitting PSU is handled jointly by construction. This
   is the correction `exp02` forces.
2. **Rao-Wu-Yue rescaling is the default**, not a robustness rerun. It is the
   defensible choice for a stratified PSU design, and the inherited analysis
   showed the activation set is sensitive to this choice (four cells to one).
3. **Degenerate-PSU countries are reported separately**, since their design
   variance carries no clustering component and the pool otherwise mixes two
   kinds of quantity.
4. Region and national curves are recomputed **inside the same replicate**
   before differencing, so their covariance is propagated rather than assumed.

## Reproduction gate (added 2026-09-09, after this protocol failed to require it)

Before any disagreement with the archive is reported as a finding, the
reimplementation must reproduce the archive's reported diagnostic under the
archive's own settings, to the precision the archive reports. A reimplementation
that has not cleared this gate is not characterising the same statistic and its
disagreements carry no information.

## Procedure

`B = 400` replicates. Within each stratum of `n_h` PSUs draw `m_h = n_h - 1`
with replacement; rescaled weight
`w* = w [1 - lambda + lambda (n_h / m_h) r_hi]`, `lambda = sqrt(m_h / (n_h - 1))`.
Singleton strata contribute no variance and are counted. Design SD `v_g(t)` is
the replicate standard deviation of `D_g(t)`.

Gates, at the frozen constants of the implementation under study
(`rho_0 = 0.47`, `delta_max = 0.02`, `delta_UCB(D) = 0.0061 + 0.0943 D`, hence
`tau_D = 0.147` and `K >= 94`):

- **A, need:** `rho_LCB > rho_0`
- **B, reliability:** `delta_UCB(D) <= delta_max`

Sweep minimum region size in {40, 60, 80, 100, 150} by round in {9, 10, 11},
for the all-countries pool and the common-coding-level pool.

## The three outcomes, written before running

1. **Activation survives** in at least one configuration under RWY rescaling
   with correct joint resampling. The paper gains a verified positive case, and
   reports it with the fifteen affected country-rounds identified.
2. **Activation survives only in the all-countries pool** and not at a common
   coding level, as the inherited archive already suggested. Reported as
   conditional feasibility, with the pooling requirement stated as the price.
3. **Activation disappears entirely.** Then the correction is unreachable on
   this survey at every unit examined, and the manuscript's characterisation
   becomes cleaner, not weaker: unnecessary at the national unit, unlearnable
   at the regional unit under correct resampling.

Outcome 3 is not a failure of the project. All three are reported. No pool,
round, or size threshold is dropped after seeing its result, and the full sweep
is written to disk regardless.
