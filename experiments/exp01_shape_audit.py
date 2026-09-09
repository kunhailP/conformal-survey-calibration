"""exp01 - standardised-shape sensitivity of the oracle scale correction.

Protocol: docs/PROTOCOL_exp01_shape_audit.md (written before execution).

Coordinate variances are exactly correct in every cell; only the correlation
shape is manipulated.  Requires no licensed microdata and no network.

    python experiments/exp01_shape_audit.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from dac import bands, generators  # noqa: E402

REPS, ALPHA, BATCH = 4000, 0.10, 200
K_GRID = (30, 100, 250)
RHO_GRID = (0.29, 0.40, 0.52, 0.80)
D_GRID = (8, 24, 48)

# (label, R_G builder, R_S builder).  All keep coordinate variances correct.
#: Mean weighted CDF of the survey item at the four core thresholds, from the
#: European Social Survey rounds 9-11; used to give the partial-sum structure
#: realistic values rather than a stylised one.
CORE_P = np.array([0.177, 0.262, 0.370, 0.463])


def _cdf_grid(d: int) -> np.ndarray:
    """Interpolate the observed core CDF values onto d thresholds."""
    return np.interp(np.linspace(0, 1, d), np.linspace(0, 1, len(CORE_P)), CORE_P)


STRUCTURES = (
    ("matched", lambda d: generators.equicorrelated(d, 0.5),
     lambda d: generators.equicorrelated(d, 0.5)),
    ("survey_realistic", lambda d: generators.ar1(d, 0.3),
     lambda d: generators.cdf_partial_sum(_cdf_grid(d))),
    ("noise_more_correlated", lambda d: generators.equicorrelated(d, 0.0),
     lambda d: generators.equicorrelated(d, 0.8)),
    ("noise_far_more_correlated", lambda d: generators.equicorrelated(d, 0.0),
     lambda d: generators.equicorrelated(d, 0.95)),
    ("noise_equi_latent_ar1", lambda d: generators.ar1(d, 0.3),
     lambda d: generators.equicorrelated(d, 0.9)),
    ("latent_more_correlated", lambda d: generators.equicorrelated(d, 0.9),
     lambda d: generators.ar1(d, 0.3)),
)


def run_cell(k: int, rho: float, d: int, name: str, build_g, build_s) -> list[dict]:
    label = f"exp01|{name}|{k}|{rho}|{d}"
    seed = int.from_bytes(hashlib.sha256(label.encode()).digest()[:8], "little")
    rng = np.random.default_rng(seed)
    sigma = generators.noise_scale(rho)
    total_scale = np.sqrt(1.0 + sigma ** 2)
    Lg = generators.cholesky(build_g(d))
    Ls = generators.cholesky(build_s(d))

    tally = {m: np.zeros(3) for m in bands.TARGETS}  # latent hits, observed hits, radius
    for start in range(0, REPS, BATCH):
        n = min(BATCH, REPS - start)
        g = generators.draw_curves(rng, n, k + 1, Lg)
        s = sigma * generators.draw_curves(rng, n, k + 1, Ls)
        y = g + s
        cal_y, cal_g = y[:, :k], g[:, :k]
        radii = {
            "observed_anchor": bands.observed_anchor(cal_y, ALPHA),
            "noise_enlargement": bands.noise_enlargement(cal_y, ALPHA, sigma, d),
            "oracle_rescaled": bands.oracle_rescaled(cal_y, ALPHA, total_scale),
            "latent_oracle": bands.latent_oracle(cal_g, ALPHA),
        }
        tgt_g = np.max(np.abs(g[:, k]), axis=1)
        tgt_y = np.max(np.abs(y[:, k]), axis=1)
        for m, r in radii.items():
            tally[m] += ((tgt_g <= r).sum(), (tgt_y <= r).sum(), r.sum())

    out = []
    for m, (hits_g, hits_y, radius) in tally.items():
        p = hits_g / REPS
        target, basis = bands.TARGETS[m]
        out.append(dict(
            experiment="exp01", structure=name, K=k, rho=rho, d=d, method=m,
            claims_target=target, basis=basis, reps=REPS, seed=seed,
            latent_hits=int(hits_g), latent_coverage=p,
            latent_mcse=float(np.sqrt(p * (1 - p) / REPS)),
            observed_coverage=hits_y / REPS, mean_radius=radius / REPS))
    return out


def main() -> None:
    rows: list[dict] = []
    for d in D_GRID:
        for name, bg, bs in STRUCTURES:
            for k in K_GRID:
                for rho in RHO_GRID:
                    rows.append(run_cell(k, rho, d, name, bg, bs))
    df = pd.DataFrame([r for cell in rows for r in cell])

    results = ROOT / "results"
    results.mkdir(exist_ok=True)
    df.to_csv(results / "exp01_shape_audit.csv", index=False, float_format="%.9g")
    (results / "exp01_manifest.json").write_text(json.dumps({
        "protocol": "docs/PROTOCOL_exp01_shape_audit.md",
        "status": "post-development sensitivity analysis, exploratory, not preregistered",
        "cells": len(D_GRID) * len(STRUCTURES) * len(K_GRID) * len(RHO_GRID),
        "reps_per_cell": REPS, "alpha": ALPHA,
        "K": list(K_GRID), "rho": list(RHO_GRID), "d": list(D_GRID),
        "structures": [s[0] for s in STRUCTURES],
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "numpy": np.__version__, "pandas": pd.__version__,
    }, indent=2) + "\n")

    orc = df[df.method == "oracle_rescaled"]
    print("Oracle rescaling, latent simultaneous coverage, K=250, nominal 0.90")
    print("rho 0.29 = national maximum in the applications; 0.52 = regional maximum\n")
    print(orc[orc.K == 250].pivot_table(index=["structure", "rho"], columns="d",
                                        values="latent_coverage").round(4).to_string())
    print(f"\ncells: {len(df) // len(bands.TARGETS)}   max MC SE: {df.latent_mcse.max():.5f}")


if __name__ == "__main__":
    main()
