"""Manuscript figures, generated from the result tables.

    python paper/figures.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
R, FIG = ROOT / "results", ROOT / "paper" / "figures"
FIG.mkdir(exist_ok=True)
TAU, RHO0, KFLOOR = 0.147, 0.47, 94

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.spines.top": False,
    "axes.spines.right": False, "axes.labelsize": 9, "legend.frameon": False,
})
INK, MUTED = "#1a1a1a", "#8a8a8a"
OPEN_C, SHUT_C = "#2f6879", "#b53c40"


def boundary(rho, tau=TAU, h=0.0):
    return 1 + 2 / (tau ** 2 * (1 - rho ** 2) ** 2 * (1 - h))


def fig_frontier():
    reg = pd.read_csv(R / "exp03_regional.csv")
    nat = pd.read_csv(R / "exp04_national.csv")
    fig, ax = plt.subplots(figsize=(6.4, 4.3))

    rho = np.linspace(0.001, 0.80, 400)
    ax.plot(rho, boundary(rho), color=INK, lw=1.8, zorder=3,
            label=r"$K \geq 1 + 2/[\tau^2(1-\rho^2)^2]$   (this paper)")
    ax.fill_between(rho, boundary(rho), 1e4, color=OPEN_C, alpha=0.07, zorder=0)
    ax.axhline(KFLOOR, color=MUTED, ls="--", lw=1.2, zorder=2,
               label=r"reported floor $K \geq 94$")
    ax.axvline(RHO0, color=MUTED, ls=":", lw=1.2, zorder=2)
    ax.text(RHO0 + .009, 4.6e3, r"need gate  $\rho_0 = 0.47$", rotation=90,
            va="top", ha="left", fontsize=7.5, color=MUTED)
    ax.text(0.045, 190, "reliability gate can open", fontsize=8,
            color=OPEN_C, style="italic")
    ax.text(0.045, 46, "reliability gate shut", fontsize=8,
            color=SHUT_C, style="italic")

    dom = pd.read_csv(R / "exp08_domains.csv")
    for df, mk, lab in ((reg, "o", "ESS regional"), (nat, "^", "ESS national"),
                        (dom, "D", "ESS domains")):
        for opened, c in ((True, OPEN_C), (False, SHUT_C)):
            s = df[df.gate_B == opened]
            if len(s):
                ax.scatter(s.rho_hat, s.K, marker=mk,
                           s=26 if mk == "D" else 34, zorder=4,
                           facecolor=c if opened else "none", edgecolor=c,
                           linewidths=1.1,
                           label=f"{lab}, gate {'open' if opened else 'shut'}")

    ax.set(xscale="linear", yscale="log", xlim=(0, 0.75), ylim=(3.2, 6e3),
           xlabel=r"design share $\hat\rho$   (fraction of observed dispersion from sampling)",
           ylabel="calibration populations $K$")
    ax.set_yticks([10, 30, 94, 300, 1000, 3000])
    ax.set_yticklabels(["10", "30", "94", "300", "1000", "3000"])
    ax.legend(loc="lower right", fontsize=7.4, ncol=1, handletextpad=.6,
              borderpad=.5)
    fig.tight_layout()
    for ext in ("pdf", "png"):
        fig.savefig(FIG / f"frontier.{ext}", dpi=200, bbox_inches="tight")
    print("frontier.pdf")


def fig_shape():
    df = pd.read_csv(R / "exp01_shape_audit.csv")
    o = df[df.method == "oracle_rescaled"]
    styles = {
        "matched": ("s", MUTED, "correlations match (S holds)"),
        "noise_more_correlated": ("v", "#c98a2b", "noise more correlated"),
        "noise_far_more_correlated": ("v", SHUT_C, "noise far more correlated"),
        "latent_more_correlated": ("^", OPEN_C, "latent more correlated"),
    }
    fig, axes = plt.subplots(1, 3, figsize=(7.6, 2.9), sharey=True)
    for ax, d in zip(axes, (8, 24, 48)):
        for st, (mk, c, lab) in styles.items():
            z = o[(o.d == d) & (o.structure == st) & (o.K == 250)].sort_values("rho")
            ax.errorbar(z.rho, z.latent_coverage, yerr=2 * z.latent_mcse,
                        marker=mk, color=c, lw=1.4, ms=4.5, capsize=2, label=lab)
        ax.axhline(0.90, color=INK, ls="--", lw=.8)
        for x in (0.29, 0.52):
            ax.axvline(x, color=MUTED, ls=":", lw=.8)
        ax.set(title=f"$d = {d}$ coordinates", xlabel=r"design share $\rho$",
               xticks=[0.29, 0.40, 0.52, 0.80], ylim=(0.72, 1.005))
    axes[0].set_ylabel("latent simultaneous coverage")
    axes[0].text(0.30, 0.745, "national\nmax", fontsize=6.5, color=MUTED)
    axes[0].text(0.53, 0.745, "regional\nmax", fontsize=6.5, color=MUTED)
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=4, fontsize=7.4)
    fig.tight_layout(rect=(0, 0.11, 1, 1))
    for ext in ("pdf", "png"):
        fig.savefig(FIG / f"shape.{ext}", dpi=200, bbox_inches="tight")
    print("shape.pdf")


if __name__ == "__main__":
    fig_frontier()
    fig_shape()
