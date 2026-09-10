# Submission checklist — JSSAM

Checked against the journal's General Instructions on 2026-09-10. Anything the
instructions require that this repository cannot supply is listed under *What a
human must supply*, and nothing on that list is optional.

## Files

| file | role |
|---|---|
| `main.tex` | **blinded** manuscript: abstract, statement of significance, body, references |
| `titlepage.tex` | separate title page: authors, funding, conflict, preregistration, acknowledgments, AI disclosure. **Compile separately; never `\input` it into `main.tex`.** |
| `sections/99_references.tex` | references, written out in ASA style so the output does not depend on which `.bst` is installed |
| `figures.py` | rebuilds both figures from `../results/`; run before compiling |

## Requirements met

| requirement | state |
|---|---|
| Double-blind: no identifying material in the manuscript | met — no author block, no repository URL, no author-archived data link |
| Body text under 6,500 words | 5,250 words (abstract, significance and references excluded) |
| Abstract, max 300 words, non-technical | 298 words, rewritten without notation |
| Statement of Significance, max 200 words | 199 words |
| Double-spaced, 12 pt Times, 1-inch margins, ragged right | `mathptmx`, `setspace`, `ragged2e`, `geometry` |
| Figures embedded near first reference | yes, `[t]` floats in §3 and §6 |
| Alt text under each figure legend | yes, prefixed `Alt text:` |
| ASA reference style | yes, written out |
| Data availability statement | yes |
| Exact question wording for the survey items | yes, §6, quoted from the ESS source questionnaire |
| Preregistration statement | on the title page; protocols are in `docs/` |

## What a human must supply

1. **Author names, affiliations, corresponding author, funding, conflict of
   interest.** Placeholders in `titlepage.tex` say so.
2. **A statement on the use of generative artificial intelligence**, per the
   journal's and publisher's policy at the time of submission. Placeholder in
   `titlepage.tex`.
3. **Fieldwork dates and response rates by country and round**, with the response
   rate definition and how it was calculated. The journal's survey-documentation
   requirement is explicit about this and the data files do not carry it; ESS
   publishes it per round. §6 currently says it must be tabulated in an appendix
   and does not report it. **This is a blocking item.**
4. **PRICSSA checklist.** Required for studies using complex sample designs, which
   this is. Not drafted here.
5. **AAPOR Code of Professional Ethics compliance**, mandatory for survey-based
   submissions.
6. **Confirmation of the question wording against the round 9--11 source
   questionnaires.** The wording in §6 is verbatim from the round 1 instrument;
   the items are core and stable, but the round used should be the round cited.
7. **A cover letter.**
8. **A compile.** No TeX installation was available here, so the manuscript has
   been checked structurally — balanced environments, every `\ref` resolving,
   every citation having a `\bibitem` — but never compiled. Build it before
   trusting any of the formatting claims above.

## What a referee will attack, and where the paper answers

1. **Originality.** §3 is the contribution: the scale elasticity and the exchange
   identity. The necessary condition in §2 is explicitly *not* claimed as new —
   with equal design variances the model is the balanced one-way random-effects
   model and the group-versus-replicate design trade-off for the intraclass
   correlation is an existing literature, which §2 cites.
2. **The theory–application gap.** The guarantee is proved under Assumption R;
   the ESS analysis runs under approximations Assumption R does not cover. §6
   states this in a boxed note and §7 calls it the paper's main weakness. *The
   most likely ground for a major revision.*
3. **Comparator strength.** Against a component-wise bound given the same
   structure the gain is 0.7–2.3%. §7 concedes it and argues the preference on
   other grounds. §7 also states that no comparison has been run against Zhang
   and Tuoto's split conformal construction, because the targets differ.

## Declared debts, all in §7

- The *O*(1/*K*) generalised-variance-function bias has no derivation.
- The 1.9/*K* constant in the refined scale law is fitted, not derived.
- Exchangeability under an estimated centre is measured (about −1/(*n_r*−1)) and
  not repaired. Repairing it is the single change that would most improve the
  paper, and it is a new result rather than an edit.

## Building

    cd manuscript
    python3 figures.py
    latexmk -pdf main.tex
    latexmk -pdf titlepage.tex
