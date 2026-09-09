# What remains

Two substantive items, then submission. Both are additions to an otherwise
complete manuscript; neither blocks the others.

---

## 1. Empirical Bayes trade-off table (Discussion, or an appendix)

**Why.** The manuscript establishes when the correction is reachable and, in
Section 6.4, how to reach it. It does not say what to do when it is not
reachable, which is most of the time. As it stands a reader who fails the
boundary is told only to stay with the uncorrected anchor. That leaves the paper
open to the fair objection that it diagnoses without prescribing.

**What to build.** A single table on the ESS configurations already computed in
`exp07`, comparing three radii on the same data:

| construction | guarantee | assumption |
|---|---|---|
| observed anchor | finite-sample, marginal over populations | exchangeability only |
| estimated scale correction | latent target, marginal | (S) plus scale control |
| simultaneous empirical Bayes band | area-conditional, asymptotic | area-level model correct |

Use a Fay--Herriot band with a second-order-correct interval as the third
column; `yoshimori2014second` and `burris2020exact` are already in `refs.bib`.

**Framing, and this matters.** Not a race. The three cover different targets
under different assumptions, and Section 6.5 already argues that a width
comparison across different targets is uninformative. The table is a trade-off
illustration: what model assumptions buy in width, and what distribution-free
exchangeability costs. Presenting it as a contest would contradict the paper's
own argument two sections earlier and a referee would notice.

**Where it lands.** Section 7 becomes prescriptive: above the boundary, correct
and check (S); below it, either accept the model assumptions and use an
area-level estimator, or stay with the anchor and report its target honestly.

---

## 2. AmericasBarometer replication

**Why.** Every empirical claim rests on one survey system, one item and one
outcome. The boundary predicts the gate in 44 of 45 ESS configurations, which is
strong within ESS and says nothing about whether the finding is an ESS artefact.
This is the largest remaining structural weakness and the only one that data can
fix.

**What to build.** Re-run `exp03` and `exp04` on the AmericasBarometer Grand
Merge, which carries design variables. The predecessor archive reports national
design shares at or below 0.22 there, so the boundary should predict the need
gate staying shut at the national unit. A confirmed prediction on a second
system, with roughly twenty countries rather than thirty-three and a different
design tradition, is what turns "characterised on one survey" into
"characterised".

**Data.** Not in this repository and not redistributable. `docs/DATA.md` records
the retrieval route. The file used previously was
`Grand_Merge_2004-2023_LAPOP_AmericasBarometer_v1.0_FREE.dta`.

**Watch for.** The item and threshold grid must be chosen before the diagnostics
are computed and recorded in a protocol, as with every other experiment here.
The design share depends on which item is used, and choosing it after seeing the
gates would invalidate the test.

---

## Then

- Complete the generative-AI disclosure on the title page (author).
- Complete the PRICSSA item checklist for upload (author).
- Draft a cover letter.
- Decide whether `docs/RESEARCH_LOG.md` stays as written if this repository is
  made public: it records the earlier desk rejection by name.
- Rotate the access token used to create this repository.

## Reproducing after a fresh clone

```
pip install numpy scipy pandas matplotlib pytest
make            # the two experiments needing no microdata, tests, numbers, figures
make paper      # rebuild both PDFs (needs a TeX distribution)
make survey     # the seven needing ESS microdata; see docs/DATA.md
```

`results/` is committed, so `make numbers` and `make paper` reproduce every
figure in the manuscript without any licensed data.
