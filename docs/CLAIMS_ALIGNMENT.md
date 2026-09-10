# Claims alignment — what stands, what is limited, what must be proved

Written 2026-09-10. Step 1 of the fixed research plan: separate the existing
contribution, the confirmed limits, and the work still owed, and record every
place where the manuscript's theory, its implementation and its claims disagree.

This document is the reference for the rewrite. It makes no new claim.

---

## 1. What stands, unchanged

| claim | source | status |
|---|---|---|
| T1/T2 separation and the target table | §2 | stands; it is the paper's spine |
| The anchor's finite-sample T1 guarantee | §2 | stands, and `exp07` checks it on ESS (leave-one-country-out) |
| Non-identification of the latent law from the convolution | §2 | stands, correctly attributed |
| The gate-coupling identity, eq. (13) | §4 | stands as algebra; verified to 0.4% on ESS |
| Information bound for $A$ with known $D_c$ | §4.2 | stands, and the manuscript already says it is classical |
| Shape mismatch costs simultaneous coverage, and the direction is predictable | §5, `exp01` | stands |

---

## 2. Confirmed limits — established here, not previously stated

| finding | experiment | consequence for the manuscript |
|---|---|---|
| The frozen reliability gate is not an error-controlled rule: it certifies on 53% of replicates and is wrong on 47% of those | `exp10` | "reachable" must stop being described as a decision with a guarantee |
| The $K\ge94$ floor certifies always and is wrong up to 94% of the time | `exp10` | keep as motivation only |
| Plug-in ML for $A$ is biased **upward** by $\approx4\rho^4/[\nu(1-\rho^2)]$, and the bias does not shrink in $K$ | `exp09` | the gate is anti-conservative in the regime it is used |
| Estimating $D_i$ costs $\le\sqrt{1+\rho^4/\nu}$ of information — 3% at $\nu=10$, 15% at $\nu=2$ | `exp09`, `exp13` | the estimated-variance worry is second order; the procedure loss is not |
| The unweighted deconvolution reaches 23% of the information bound under realistic dispersion; oracle weighting reaches 99% | `exp12` | information is discarded, not absent |
| A GVF fitted on all populations recovers most of it; plug-in weights do not | `exp13` | actionable, conditional on the GVF fitting |
| Better point estimation does **not** transfer to a valid interval | `exp14`, `exp15` | two results, not one |
| A tighter scale limit buys 3–14% of band width, not the limit's own ratio | `exp16` | width claims must be measured, not inferred |
| At the regional design share the **valid** band is 0.9–6.6% narrower than not correcting, capturing 6–31% of the oracle narrowing | `exp18` | this is the finding that most changes the paper |
| Simultaneous lower limits on $D_c$ fail (0.445–0.834 against 0.975) at a tail quantile with few PSUs, and worsen as $K$ grows | `exp18` | the containment premise is not safe |
| The oracle band itself undercovers (0.9315 against 0.950) in the harshest cell | `exp18` | not a variance problem; belongs with `exp01` |
| Removing the multiplicity entirely raises the captured share only from 6–27% to 12–42% | `exp19` | a joint set over $\mathbf D$ alone cannot fix this |

---

## 3. Theory–implementation mismatches to fix in the manuscript

**(a) §3's oracle is not §6's implementation.** §3 standardises **per
population**, $M_c=|Y_c|/\sqrt{s_G^2+v_c^2}$. `exp07_widths.py` uses a
**common** denominator: `s_plug = dep.std(axis=0)` is a per-coordinate vector
shared across populations. The two coincide only under equal design variances.
`exp12` measured the difference: the licensed construction is exact at every
dispersion, the common-denominator one departs by up to $+0.021$ at 12% more
width. **Either the theory is restated for the implemented construction or the
implementation is changed. It cannot stay as it is.**

**(b) The reported radius is a mean half-width, not a radius.** `exp07` reports
`q * sT.mean()`, the average of the per-coordinate half-widths $q\,sT(j)$, not
one radius applied to every coordinate. The prose reads as the latter.

**(c) The 15–19% is a plug-in ratio with no error budget.** §6.5 compares the
correction's realised radius to the anchor's, both computed from plug-in scales.
The number may well be right *as that comparison*. What is not established is
that a band carrying an explicit budget for the scale uncertainty narrows by
that much: in a matched simulated cell whose oracle narrowing is 19.5%, the
honestly-bounded band achieves **4.9%** (`exp18`). The sentence "the correction
is therefore worth having where it is reachable" is not supported at the
strength it is written, and §6.5 must say which quantity the 15–19% is.

**(d) "Reachable" rests on the gate.** The gate is a plug-in RSE criterion with
no error control (`exp10`). Wherever the manuscript uses reachability as a
decision, it is reporting a diagnostic, not a certification.

**(e) The width comparison's direction and denominator.** Ratios must name their
denominator ($r=0.861$ is 13.9% narrower one way and 16.1% wider the other) and
must be reported beside realised coverage, since equal nominal budgets did not
produce equal coverage in any experiment here.

---

## 4. What must be proved, and what may not be claimed

**Owed.**

1. A coverage argument for the **implemented** procedure, in the form
   $\Pr\{\theta_{\text{new}}\in B\}\ge1-\alpha-\varepsilon_{K,n}$, with
   $\varepsilon_{K,n}$ resolved into its drivers — $K$, within-area survey
   information, variance-estimation accuracy, and the standardised-shape
   condition — rather than called small.
2. A result on the gain: either the new construction's half-width approaching
   the oracle's under stated conditions, or a quantification of what separate
   upper/lower bounding adds, or a lower bound on certifiable gain given stated
   survey information.
3. A theoretical account of the $O(1/K)$ GVF bias, whose rate is measured
   ($-0.966$ in $\log K$) and not derived.

**May not be claimed.**

- That the $\chi^2$ pivot's guarantee holds under a complex design. Its
  conditions fail measurably and a simulation cannot extend a theorem's scope.
- That assumption (S) is verified by coverage at one nominal level.
- That the percentile bootstrap limit is valid: it undercovers by 0.7–3.1 points
  in the closed model and by 7–16 at a tail quantile under a complex design.
- Any lower bound derived from the Cramér–Rao statement for $A$ as an
  impossibility result for bands. The target and the admissible procedures must
  be named first.
- Superiority over the enlargement route without stating that the comparison is
  of assumptions as well as widths, and that the simulations were generated
  under (S).

---

## 5. Scope decision, fixed

**The paper is completed for a scalar population summary.** The full-CDF
simultaneous band is not carried as a core contribution: it needs the
coordinate-dependence and simultaneity work that `exp12` §4 identified and that
nothing here has done. Scalar results are not transported to a whole-curve
guarantee.

The ESS analysis's role is correspondingly fixed: it cannot demonstrate T2
coverage, because the latent truth is unobserved. It can show where the
applicability judgement changes, how it differs across pre-specified outcomes,
and how far the plug-in and budgeted answers diverge.
