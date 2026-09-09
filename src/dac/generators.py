"""Correlation structures and deviation-curve generators.

The generators produce *standardised deviation curves*, not cumulative
distribution functions and not finite-population sampling designs.  They exist
to isolate distributional assumptions, and any experiment built on them must
say so.
"""
from __future__ import annotations

import numpy as np

__all__ = ["equicorrelated", "ar1", "banded", "cdf_partial_sum", "cholesky",
           "draw_curves", "noise_scale"]


def equicorrelated(d: int, r: float) -> np.ndarray:
    """Exchangeable correlation: every off-diagonal entry equals ``r``."""
    if not -1.0 / (d - 1) < r < 1.0:
        raise ValueError(f"equicorrelated({d}, {r}) is not positive definite")
    R = np.full((d, d), float(r))
    np.fill_diagonal(R, 1.0)
    return R


def ar1(d: int, r: float) -> np.ndarray:
    """First-order autoregressive correlation, ``R[i, j] = r ** |i - j|``."""
    if not -1.0 < r < 1.0:
        raise ValueError(f"ar1 requires |r| < 1, got {r}")
    i = np.arange(d)
    return np.asarray(float(r)) ** np.abs(i[:, None] - i[None, :])


def banded(d: int, r: float, bandwidth: int = 1) -> np.ndarray:
    """Correlation ``r`` within ``bandwidth`` coordinates, zero beyond."""
    i = np.arange(d)
    lag = np.abs(i[:, None] - i[None, :])
    R = np.where(lag <= bandwidth, float(r), 0.0)
    np.fill_diagonal(R, 1.0)
    return R


def cdf_partial_sum(p: np.ndarray) -> np.ndarray:
    """Correlation of sampling error in a cumulative distribution function.

    For a multinomial sample the estimated CDF values at thresholds are partial
    sums over one sample, so for ``j <= k`` the errors correlate as

        R(j, k) = sqrt( p_j (1 - p_k) / ( p_k (1 - p_j) ) ),

    the standardised Brownian-bridge covariance.  Correlation is high and decays
    only with the distance between the CDF values, which is the mechanism that
    makes sampling error more correlated across thresholds than differences
    between populations are.  ``p`` must be strictly increasing in (0, 1).
    """
    p = np.asarray(p, dtype=float)
    if not (np.all(np.diff(p) > 0) and p[0] > 0 and p[-1] < 1):
        raise ValueError("p must be strictly increasing inside (0, 1)")
    lo, hi = np.minimum.outer(p, p), np.maximum.outer(p, p)
    return np.sqrt(lo * (1 - hi) / (hi * (1 - lo)))


def cholesky(R: np.ndarray) -> np.ndarray:
    """Lower Cholesky factor, with a clear error when ``R`` is not admissible."""
    try:
        return np.linalg.cholesky(R)
    except np.linalg.LinAlgError as exc:  # pragma: no cover - guard
        raise ValueError("correlation matrix is not positive definite") from exc


def draw_curves(rng: np.random.Generator, n: int, k: int, L: np.ndarray) -> np.ndarray:
    """Draw ``n`` replicates of ``k`` independent Gaussian curves with factor ``L``.

    Returns an array of shape ``(n, k, d)`` with unit coordinate variances when
    ``L`` is the Cholesky factor of a correlation matrix.
    """
    d = L.shape[0]
    return rng.normal(size=(n, k, d)) @ L.T


def noise_scale(rho: float) -> float:
    """Noise standard deviation giving design share ``rho`` at unit latent scale.

    With latent variance 1 and noise variance ``sigma ** 2``, the design share is
    ``rho ** 2 = sigma ** 2 / (1 + sigma ** 2)``, so ``sigma = rho / sqrt(1 - rho ** 2)``.
    """
    if not 0.0 <= rho < 1.0:
        raise ValueError(f"design share must lie in [0, 1), got {rho}")
    return float(rho) / np.sqrt(1.0 - float(rho) ** 2)
