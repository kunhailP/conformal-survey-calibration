# Targets and assumptions for conformal prediction on survey-estimated curves

Research repository for a manuscript in preparation for the *Journal of Survey
Statistics and Methodology*.

Repeated probability surveys produce estimated distributions. When those
estimates calibrate a prediction for a further population, the calibration
objects carry sampling error of their own. This repository studies what such a
prediction band guarantees, about which object, under which assumption.

Two targets are kept apart everywhere, in the code as well as the prose:

| target | object | reached by |
|---|---|---|
| **T1** | a further *survey estimate* | exchangeability of observed curves, finite sample |
| **T2** | its *population distribution* | a sampling-error bound, or a distributional shape assumption |

`src/dac/bands.py` labels every construction with the target it may claim and
the basis of that claim. Nothing converts T1 coverage into T2 coverage without
an explicit assumption.

## Layout

```
docs/        scope, claims ledger, experiment protocols, data access, research log
src/dac/     bands, generators, diagnostics
experiments/ numbered, each with a protocol written before execution
results/     generated outputs; results/archived/ holds inherited tables
tests/       contract tests binding each claim to executable behaviour
paper/       manuscript sources
```

## Reproduce

`exp01` needs no microdata and no network.

```
pip install numpy scipy pandas matplotlib pytest
python experiments/exp01_shape_audit.py     # ~2 min, 180 cells
python -m pytest tests/ -q                  # ~3 min, 11 contract tests
```

Cell seeds derive from cell labels by SHA-256, so any cell reproduces on its
own and no cell can be selected after its outcome is known.

## Working rules

1. **A protocol before an experiment.** Written, dated, committed before
   execution, and it records what a disappointing outcome would look like.
2. **A claim needs a row.** Every number intended for the manuscript appears in
   `docs/CLAIMS.md` with the artefact that produces it, marked `verified` or
   `inherited`.
3. **Targets are declared, never inferred.** A construction states the target it
   guarantees; a test enforces it.
4. **Decisions are logged.** `docs/RESEARCH_LOG.md` is append-only, including
   the decisions that weakened a claim.

## Provenance

Archived tables under `results/archived/` come from
`github.com/kunhailP/design-aware-conformal` at `ea592e9`. They were produced
on licensed microdata and have **not** been re-executed here; `docs/CLAIMS.md`
marks them `inherited` and `docs/DATA.md` records the access route and the
outstanding design-file check.
