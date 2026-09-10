# Protocol — exp29: Proposition S4 as a pre-registered prediction

Written 2026-09-10. Derivation: `docs/THEORY_scale_sensitivity.md`.
**The predicted numbers below were computed before the experiment was run and
are not revised afterwards.** A fresh grid is used: none of these $K$, $\rho^2$
or $\nu$ values appear in `exp26`.

## What is being tested

Proposition S4 says that in the scalar homoscedastic case the width ratio of the
deconvolution band to the matched Gaussian band is
$$\frac{R_{\text{conformal}}}{R_{\text{gaussian}}}\;\approx\;
\frac{z_p}{z_{1-\alpha_1/2}}\sqrt{\frac{\chi^2_{K,\alpha_2}}{K}},\qquad p=\frac{m}{K+1},$$
with the certified scale bound $\underline t$ cancelling, along with $A$, $L$,
$\rho$ and $\nu$. This is a strong claim: it says a quantity that looked like it
should depend on the design share and the variance degrees of freedom depends on
**neither**.

## Pre-registered predictions

Budget throughout: $\alpha_0=0.05$, $\eta_\gamma=\eta_t=0.025$, split
$(\alpha_1,\alpha_2)=(0.025,0.025)$ unless stated.

**P-A. Level.** With that split, the ratio is predicted to be

| $K$ | predicted conformal/Gaussian |
|---|---|
| 40 | **0.6871** |
| 120 | **0.7653** |
| 400 | **0.8143** |

Registered tolerance: **within 5 percent** of the predicted value in every cell.
The formula is asymptotic in $K$ and exact only in the scalar homoscedastic case,
so a systematic 1–4 percent error is expected and larger would refute it.

**P-B. Invariance.** Within each $K$ the ratio must not move with
$\rho^2\in\{0.20,0.45,0.70\}$, with $\nu\in\{6,20\}$, or with structure
misspecification $\sigma_{\mathrm{mis}}\in\{0,0.5\}$. Registered tolerance:
**within-$K$ spread below 0.02** in the absolute ratio. This is the discriminating
test — a quantity that varied with the design share would refute S4 outright.

**P-C. Monotone response to the split.** At $K=120$, varying $(\alpha_1,\alpha_2)$
with $\alpha_1+\alpha_2=0.05$ the ratio is predicted to rise monotonically:

| $\alpha_1$ | 0.005 | 0.010 | 0.020 | 0.025 | 0.035 | 0.045 |
|---|---|---|---|---|---|---|
| predicted | **0.6225** | **0.6758** | **0.7414** | **0.7653** | **0.8015** | **0.8188** |

Registered tolerance: monotone increasing, and every value within 5 percent.
No crossing is predicted in this range — the ratio stays below 1 throughout — so
a crossing would refute the calculus, not merely the constant.

## Design

Model R with an estimated structure exactly as in `exp26`; the certified
procedure and the Gaussian competitor unchanged. Grid: $K\in\{40,120,400\}$,
$\rho^2\in\{0.20,0.45,0.70\}$, $\nu\in\{6,20\}$,
$\sigma_{\mathrm{mis}}\in\{0,0.5\}$ — 36 cells for P-A and P-B — plus 6 cells at
$K=120$, $\rho^2=0.45$, $\nu=20$, $\sigma_{\mathrm{mis}}=0$ for P-C. 10,000
replicates.

$\rho^2$ is converted to $d/A=\rho^2/(1-\rho^2)$: 0.25, 0.818, 2.333.

## Outcomes

1. **P-A, P-B and P-C all hold.** S4 stands as a predictive law and the paper's
   contribution is stated around the calculus, with the procedure as an instance.
2. **P-B fails.** The ratio depends on the design share after all, the
   cancellation is wrong, and S4 is withdrawn — S1 and the elasticity table would
   survive but the sharp form would not.
3. **P-A fails while P-B holds.** The invariance is real and the constant is
   wrong; the derivation of $z_p$ or of $\bar S$ needs correcting and the error is
   located.

Recorded either way, and the predicted numbers above stand as written.
