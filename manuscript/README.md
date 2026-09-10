# Manuscript — scalar latent-target prediction

New manuscript, scoped to a **scalar** population summary. It is not the
inherited full-CDF paper in `../paper/`, which remains as written; the two are
not placed under one guarantee.

| section | evidence |
|---|---|
| 2 target and information | `exp09`, `exp10`, `exp12`, `exp13` |
| 3 scale sensitivity | `exp29` (registered), plus `exp13`, `exp16`, `exp17`, `exp23`, `exp26` |
| 4 method | `exp20`--`exp23` |
| 5 simulation | `exp18`, `exp19`, `exp25`, `exp26` |
| 6 ESS | `exp27`, `exp28` |

Positioning: `../docs/CONTRIBUTION.md`. Every number traces to a row of
`../docs/CLAIMS.md`.

    cd manuscript && latexmk -pdf main.tex
