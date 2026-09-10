"""Figures for the manuscript. Reads only result tables written by the experiments.

    python3 manuscript/figures.py

Writes manuscript/figures/fig1_elasticity.pdf and fig2_ess_widths.pdf.
Every plotted point traces to a row of docs/CLAIMS.md.

Note on what is NOT plotted. exp15 and exp16 disagree on which of the two
constructions is narrower, and the elasticity calculus explains that as a
crossing. We do not plot it as a measured crossing: docs/CLAIMS.md records that
exp16 supersedes exp15's normal comparison, so the two differ in more than the
tightness of the scale limit.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
OUT = Path(__file__).resolve().parent / "figures"
OUT.mkdir(exist_ok=True)

plt.rcParams.update({
    "font.size": 9,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 150,
    "savefig.bbox": "tight",
})


def fig1_elasticity():
    """The damping: what the identity says, and what the simulation measured."""
    a = pd.read_csv(RES / "exp16_band_comparison.csv")
    a = a.assign(rho2=a["Dbar_over_A"] / (1 + a["Dbar_over_A"]))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 2.9))

    # --- left: the exchange identity, exact, no fitted constant ---------------
    lam = np.logspace(0, np.log10(50), 300)
    for r2, style in ((0.2, ":"), (0.5, "--"), (0.8, "-")):
        ax1.plot(lam, lam ** (r2 / 2 - 0.5), style, color="k", lw=1.3,
                 label=rf"$\rho^2={r2}$")
    ax1.set_xscale("log")
    ax1.set_xlabel(r"looseness of the scale bound, $\lambda=A_U/A$")
    ax1.set_ylabel(r"$\Lambda=\lambda^{\rho^2/2-1/2}$")
    ax1.set_title("What a loose bound costs, relatively", fontsize=9, loc="left")
    ax1.legend(frameon=False, fontsize=8, loc="lower left")
    ax1.annotate("the deconvolution form\ngains as the bound loosens,\nand gains "
                 "faster the larger\nthe design share",
                 xy=(1.15, 0.33), fontsize=7, color="0.35", va="bottom")

    # --- right: predicted vs measured elasticity ------------------------------
    pred = a["rho2"] / 2
    meas = a["elasticity"]
    lo, hi = 0.15, 0.45
    ax2.plot([lo, hi], [lo, hi], "-", color="0.6", lw=0.9)
    for K, mk in ((60, "o"), (200, "s")):
        sel = a["K"] == K
        ax2.plot(pred[sel], meas[sel], mk, ms=5, color="k", mfc="w", mew=1.0,
                 label=f"$K={K}$")
    ax2.set_xlim(lo, hi)
    ax2.set_ylim(lo, hi)
    ax2.set_xlabel(r"predicted elasticity $\rho^2/2$")
    ax2.set_ylabel("measured elasticity")
    ax2.set_title("Predicted against measured", fontsize=9, loc="left")
    ax2.legend(frameon=False, fontsize=8, loc="upper left")
    ratio = float((meas / pred).mean())
    ax2.annotate(f"measured / predicted\nmean {ratio:.2f}, always below 1",
                 xy=(0.30, 0.19), fontsize=7, color="0.35")

    fig.savefig(OUT / "fig1_elasticity.pdf")
    plt.close(fig)
    return dict(cells=int(len(a)), mean_measured_over_predicted=ratio,
                max_measured_over_predicted=float((meas / pred).max()))


def fig2_ess():
    """What the arms do on the same real data: 45 ESS configurations.

    The dev_* columns are the ones computed with the variance of the centred
    score; the unprefixed columns use the wrong variance (Section 6.3).
    """
    d = pd.read_csv(RES / "exp28_centring.csv")
    cols = [("dev_cert_over_gauss", "vs. normal-theory comparator\n(same target, structure, budget)"),
            ("dev_cert_over_sep", "vs. component-wise bound"),
            ("dev_cert_over_unc", "vs. no correction")]
    cols = [(c, t) for c, t in cols if c in d.columns]

    fig, ax = plt.subplots(figsize=(7.4, 3.1))
    items = sorted(d["item"].unique())
    marks = dict(zip(items, ["o", "s", "^", "D"]))

    for j, (col, _) in enumerate(cols):
        v = d[col].to_numpy(dtype=float)
        for it in items:
            sel = (d["item"] == it).to_numpy()
            y = np.full(sel.sum(), j) + np.linspace(-.17, .17, sel.sum())
            ax.plot(d.loc[sel, col], y, marks[it], ms=3.6, color="k",
                    mfc="w", mew=0.8, label=it if j == 0 else None)
        ax.plot([np.median(v)] * 2, [j - .30, j + .30], "-", color="k", lw=2)
        ax.text(np.median(v), j - .40, f"median {np.median(v):.3f}",
                fontsize=7.5, ha="center", color="0.25")
        ax.text(1.03, j, f"narrower in {(v < 1).sum()} of {v.size}",
                fontsize=7.5, va="center", color="0.25")

    ax.axvline(1.0, color="0.6", lw=0.8)
    ax.set_yticks(range(len(cols)))
    ax.set_yticklabels([t for _, t in cols], fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("width of the proposed interval, relative to the comparator")
    ax.set_xlim(0.38, 1.22)
    ax.legend(frameon=False, fontsize=7.5, loc="lower left", title="item",
              title_fontsize=7.5, ncol=len(items))
    fig.savefig(OUT / "fig2_ess_widths.pdf")
    plt.close(fig)
    return {c: dict(median=round(float(d[c].median()), 3),
                    lo=round(float(d[c].min()), 3), hi=round(float(d[c].max()), 3),
                    narrower=int((d[c] < 1).sum()), n=int(d[c].size))
            for c, _ in cols}


if __name__ == "__main__":
    import json
    print(json.dumps({"fig1": fig1_elasticity(), "fig2": fig2_ess()}, indent=2))
    print("wrote", *(p.name for p in sorted(OUT.glob("*.pdf"))))
