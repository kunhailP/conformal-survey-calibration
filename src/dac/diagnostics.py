"""Diagnostics of the deployed adaptive implementation.

These reproduce the *frozen* quantities of the implementation under study so
that its operating conditions can be characterised.  They are properties of
that implementation, not universal limits on inference.
"""
from __future__ import annotations

import numpy as np

__all__ = ["design_share", "reliability_floor", "min_populations", "guarded_scale"]

#: Frozen constants of the implementation under study.
RHO_CUTOFF = 0.47
TAU_D = 0.147


def design_share(mean_design_var: np.ndarray, total_var: np.ndarray) -> np.ndarray:
    """``rho(j) ** 2 = mean design variance / total observed variance``."""
    return np.sqrt(np.clip(mean_design_var / total_var, 0.0, 1.0))


def guarded_scale(total_var: np.ndarray, mean_design_var: np.ndarray,
                  se_design_var: np.ndarray, floor: np.ndarray,
                  z: float = 1.645) -> np.ndarray:
    """Finite-K guarded latent scale: subtract less variance when unsure of it."""
    subtract = np.maximum(mean_design_var - z * se_design_var, 0.0)
    return np.maximum(total_var - subtract, floor)


def reliability_floor(k: int) -> float:
    """Deterministic floor ``sqrt(2 / (K - 1))`` of the chosen diagnostic ``D``.

    Holds on every realisation because the guarded scale never exceeds the
    observed scale.  It bounds *this* diagnostic; it is not a lower bound over
    biased, shrinkage, or structured-covariance estimators.
    """
    if k < 2:
        raise ValueError("the diagnostic is undefined below two populations")
    return float(np.sqrt(2.0 / (k - 1)))


def min_populations(tau: float = TAU_D) -> int:
    """Smallest ``K`` at which ``D <= tau`` is attainable, i.e. ``1 + 2 / tau ** 2``."""
    return int(np.ceil(1.0 + 2.0 / tau ** 2))
