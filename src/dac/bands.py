"""Prediction bands, each labelled by the target it guarantees.

Constructions
-------------
``observed_anchor``
    Conformal band on the observed scores.  Guarantees **T1** in finite samples
    under exchangeability of the observed curves.  Makes no T2 claim.

``noise_enlargement``
    ``observed_anchor`` widened by a bound on the target's maximum sampling
    error.  Guarantees **T2** at ``1 - alpha0 - beta`` with no shape assumption.
    Operational only when such a bound is available.

``oracle_rescaled``
    Scores studentised by the known total scale, band placed on the latent
    scale.  Guarantees **T2** *only* under the common standardised-shape
    assumption (S).  Correct coordinate variances are not sufficient.

``latent_oracle``
    Conformal band calibrated on the unobserved latent curves.  Infeasible;
    included as the reference the other constructions are measured against.
"""
from __future__ import annotations

import numpy as np

__all__ = ["conformal_rank", "conformal_quantile", "observed_anchor",
           "noise_enlargement", "oracle_rescaled", "latent_oracle", "TARGETS"]

#: Which target each construction is entitled to claim, and on what basis.
TARGETS = {
    "observed_anchor": ("T1", "exchangeability of observed curves"),
    "noise_enlargement": ("T2", "observed anchor + sampling-error tail bound"),
    "oracle_rescaled": ("T2", "common standardised-shape assumption (S) + known scales"),
    "latent_oracle": ("T2", "infeasible reference: calibrated on latent curves"),
}


def conformal_rank(k: int, alpha: float) -> int:
    """The order statistic index ``ceil((1 - alpha) (k + 1))`` used throughout."""
    return int(np.ceil((1.0 - alpha) * (k + 1)))


def conformal_quantile(scores: np.ndarray, alpha: float) -> np.ndarray:
    """Rank-based conformal quantile along axis 1.

    Returns ``inf`` where the requested rank exceeds the calibration count, which
    is the honest answer: the band is uninformative rather than merely wide.
    """
    k = scores.shape[1]
    rank = conformal_rank(k, alpha)
    if rank > k:
        return np.full(scores.shape[0], np.inf)
    return np.partition(scores, rank - 1, axis=1)[:, rank - 1]


def observed_anchor(observed: np.ndarray, alpha: float) -> np.ndarray:
    """Radius of the T1 anchor.  ``observed`` has shape ``(n, k, d)``."""
    return conformal_quantile(np.max(np.abs(observed), axis=2), alpha)


def noise_enlargement(observed: np.ndarray, alpha: float, sigma: float, d: int,
                      *, anchor_share: float = 0.5) -> np.ndarray:
    """T2 band: anchor at ``alpha0`` widened by a Gaussian union-bound tail.

    The error budget is split between the anchor (``anchor_share``) and the
    sampling-error tail.  With Gaussian coordinate errors of scale ``sigma`` the
    union bound over ``d`` coordinates and two tails gives the enlargement
    ``sigma * z_{1 - beta / (2 d)}``.
    """
    from scipy.stats import norm

    alpha0 = alpha * anchor_share
    beta = alpha - alpha0
    radius = observed_anchor(observed, alpha0)
    return radius + sigma * norm.ppf(1.0 - beta / (2.0 * d))


def oracle_rescaled(observed: np.ndarray, alpha: float, total_scale: float,
                    latent_scale: float = 1.0) -> np.ndarray:
    """T2 band under assumption (S), with the scales supplied rather than estimated.

    Dividing the observed scores by ``total_scale`` makes them copies of the
    shape process's sup-norm *iff* (S) holds; the band is then placed on the
    latent scale.  When (S) fails the division is still well defined and the
    resulting coverage is what :mod:`experiments.exp01_shape_audit` measures.
    """
    return latent_scale * conformal_quantile(
        np.max(np.abs(observed), axis=2) / total_scale, alpha)


def latent_oracle(latent: np.ndarray, alpha: float) -> np.ndarray:
    """Infeasible reference: conformal radius calibrated on the latent curves."""
    return conformal_quantile(np.max(np.abs(latent), axis=2), alpha)
