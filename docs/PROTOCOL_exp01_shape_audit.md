# Protocol — exp01: standardised-shape sensitivity

Written 2026-09-09, before executing `experiments/exp01_shape_audit.py`.
Status: **post-development sensitivity analysis, exploratory.** The method was
developed first; this experiment interrogates one of its assumptions. It is not
a preregistered confirmatory test and it does not evaluate the deployed
adaptive selector.

## Question

Assumption (S) requires the standardised observed and latent curves to follow a
common law. Correct coordinate variances do not imply it. **Under what
conditions does violating (S) cost simultaneous latent coverage, and is the
damaging regime one that repeated cross-national surveys actually occupy?**

## Why the predecessor experiment is not sufficient

The inherited audit fixes eight coordinates and reports its headline at design
share `rho = 0.8`. Two gaps follow.

1. The applications in this paper report `rho_hat <= 0.29` at the national unit
   and `<= 0.52` at the regional unit. A failure demonstrated only at `0.8` is
   outside the operating range of the evidence presented alongside it.
2. Simultaneity is taken over rounds x thresholds, so the real coordinate count
   is not eight. If the cost of shape mismatch grows with the coordinate count,
   fixing `d = 8` understates it.

## Design

Latent curves `G ~ N(0, R_G)`, sampling error `S ~ N(0, sigma^2 R_S)`,
independent, `sigma = rho / sqrt(1 - rho^2)`. All coordinate variances are
exactly correct by construction; only the correlation *shape* is manipulated.

- Coordinates `d` in {8, 24, 48}. **New axis.**
- Design share `rho` in {0.29, 0.40, 0.52, 0.80}. The first and third are the
  maxima observed at the national and regional units; `0.80` retains
  comparability with the inherited grid.
- Calibration populations `K` in {30, 100, 250}.
- Correlation pairs `(R_G, R_S)`, all with correct variances:
  - `matched` — equicorrelated 0.5 in both. Assumption (S) holds. Control.
  - `noise_more_correlated` — latent independent, noise equicorrelated 0.8.
  - `noise_far_more_correlated` — latent independent, noise equicorrelated 0.95.
  - `noise_equi_latent_ar1` — latent AR(1) 0.3, noise equicorrelated 0.9.
  - `latent_more_correlated` — latent equicorrelated 0.9, noise AR(1) 0.3.
- 4,000 replicates per cell, nominal level 0.90, fixed zero centre.
- Four constructions per replicate, all scored against the same latent target.

Seeds are derived deterministically from the cell label by SHA-256, so any cell
reproduces independently and no cell is selected after seeing its outcome.

## The directional claim to be tested

For a cumulative distribution function, sampling errors at adjacent thresholds
are partial sums over one sample and are therefore strongly positively
correlated. Differences between populations across thresholds carry no such
mechanism. **The survey-realistic configuration is therefore
`noise_more_correlated`, and the prediction is that this is the
anti-conservative direction.** If instead the conservative direction dominated
at realistic `rho`, the practical warning in the manuscript would be unfounded
and would have to be withdrawn.

## What this experiment cannot establish

It uses Gaussian deviation vectors, not cumulative distribution functions and
not a finite-population sampling design. It supplies exact scales, so it
isolates (S) from scale-estimation error. It therefore cannot bound the
deployed selector's realised coverage on survey data, and no such claim will be
made from it.

## Acceptance

All cells are reported. No cell is dropped after execution. If the realistic
range shows no meaningful cost, that outcome is reported as the finding.
