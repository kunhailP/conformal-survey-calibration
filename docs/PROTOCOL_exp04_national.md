# Protocol — exp04: national unit, recomputed

Written 2026-09-09, before executing `experiments/exp04_national.py`.
Licensed ESS microdata.

## Why

`docs/CLAIMS.md` carries the national design shares as **inherited**: read from
archived tables, produced under an `m`-of-`m` bootstrap that biases design
variance downward. `exp03` showed that at the regional unit, switching to
Rao-Wu-Yue rescaling with correct joint resampling moved every diagnostic
enough to close a gate that had been open. The national figures were produced
by the same superseded machinery and have not been rechecked.

The national unit carries the first cell of the paper's three-way
characterisation — *the correction is unnecessary here*. That cell currently
rests on a number this project has not computed.

## Estimand

Country `c`'s deviation from the cross-country transport centre, on `trstprl`,
thresholds `t = 0..9`. Two coordinate structures, because `exp01` found the
coordinate count matters and the two applications differ in it:

- **per-round**, `d = 10`, directly comparable to the regional estimand of `exp03`;
- **trajectory**, rounds 9-11 stacked, `d = 30`, which is the object the
  cross-country transport band actually covers.

Design variance from the same `(stratum, psu)` Rao-Wu-Yue resampling as `exp03`,
`B = 400`, computed within each country.

## Checks

1. Recompute `rho_hat` and `rho_LCB` at the national unit, per round and for the
   trajectory, and compare with the inherited maximum of 0.29.
2. Apply the same frozen gates. Report which open.
3. Decompose `D` into its K-floor and design-variance-heterogeneity terms, as in
   `exp03`, and report whether the national unit shows the same structure.
4. Repeat over a minimum-sample-size sweep and an age-band subgroup scan, since
   the inherited maximum came from a subgroup scan rather than the full samples.

## Outcomes, written before running

1. **National shares stay small** (`rho_hat` well below `rho_0 = 0.47`). The
   first cell stands, now verified rather than inherited, and the
   characterisation is unchanged: unnecessary nationally, unlearnable regionally.
2. **National shares rise materially** under correct resampling, perhaps past
   `rho_0`. Then the correction is *needed* at the national unit too, `K <= 33`
   puts it far below any reliability threshold, and the paper's claim becomes
   stronger and simpler: needed at both units, reachable at neither.
3. **Shares rise past `rho_0` and a gate opens somewhere.** Then the national
   cell must be reported as conditionally feasible and the three-way
   characterisation redrawn.

The prediction is outcome 1 or 2. Outcome 2 would require rewriting the
national cell of the characterisation, and would be reported as such rather
than smoothed over. The full sweep is written to disk regardless of outcome.
