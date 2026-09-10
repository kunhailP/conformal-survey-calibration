# Protocol — exp19: is there headroom, and where?

Written 2026-09-10, before executing `experiments/exp19_headroom.py`.
**No method is proposed or added.** This is the precondition check for designing
a joint-inference candidate: if the loss is not where a joint set could help,
the candidate should not be built.

## Why

`exp18` found the valid band 0.9 to 6.6 percent narrower than not correcting,
capturing 6 to 31 percent of the oracle's narrowing. The suspected cause is that
the argument bounds $A$ **above** and every $v_c$ **below**, and both drive the
band factor $\{1+v_{L,c}^2/A_U\}^{-1/2}$ toward 1.

That is a hypothesis about where the width goes. It is testable by evaluating
the *same* band function at mixed arguments, which requires no new construction:

| evaluation | meaning |
|---|---|
| $R(A,\mathbf D)$ | oracle |
| $R(A_U,\mathbf D)$ | cost of bounding $A$ alone |
| $R(A,\mathbf v_L)$ | cost of bounding $\mathbf D$ alone |
| $R(A_U,\mathbf v_L)$ | the current procedure |
| $R(A_U^{[\eta_2]},\mathbf v_L^{[\eta_2]})$ | the same with each $v_c$ at $\eta_2$ rather than $\eta_2/K$ |

The last row is **not a valid procedure** and is not offered as one. It measures
the multiplicity cost: the most any improvement to the simultaneity treatment
alone could return.

## What the answer decides

- If most of the loss is the **multiplicity** row, a joint set that avoids
  bounding all $K$ variances simultaneously has room to work, and the candidate
  is worth designing.
- If most of the loss is **bounding $A$**, a joint set does not address it and
  the candidate should not be built.
- If the two are comparable, both must be handled at once, which is the harder
  design and should be known before starting rather than after.

Additivity is not assumed: the mixed evaluations are reported directly and the
individual costs need not sum to the total.

## Grid

The `exp18` configurations where the design share is largest, since that is where
the correction has something to lose: `low_signal` and `small_sample` at level
S2, $t_0\in\{$median$,0.15\}$, $K\in\{60,200\}$ — 8 cells, 2,000 replicates,
same seeds and same generation as `exp18`. No bootstrap arm.

## Predictions

| # | prediction | falsified by |
|---|---|---|
| Z1 | bounding $\mathbf D$ costs more than bounding $A$ | the reverse |
| Z2 | the multiplicity is a large share of the $\mathbf D$ cost, and grows with $K$ | multiplicity being a minor part |
| Z3 | even with the multiplicity removed entirely, most of the oracle narrowing is still not recovered | full recovery, which would make the candidate straightforward |

## Outcomes

1. **Z2 holds and Z3 fails** — the multiplicity is the binding cost. Design the
   joint candidate around it.
2. **Z2 holds and Z3 holds** — removing multiplicity helps but leaves most of the
   gap. Report the ceiling on what a joint set can buy before building one.
3. **Z1 fails** — bounding $A$ dominates. A joint set over $\mathbf D$ is the
   wrong target and the candidate is not built.

Recorded either way; a negative answer here saves the development step.
