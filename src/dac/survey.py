"""Stratified primary-sampling-unit resampling for complex survey designs.

The resampling unit is ``(stratum, psu)``.  A PSU carries every one of its
respondents into a replicate, whichever regions or domains they fall in, so
estimands defined on sub-populations that a PSU straddles keep their dependence
structure.  Grouping by ``(stratum, psu, sub-population)`` instead would split
such a PSU and destroy exactly the dependence the resample exists to represent.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

__all__ = ["replicate_weights", "weighted_cdf", "RESAMPLE_UNIT"]

RESAMPLE_UNIT = ("stratum", "psu")


def replicate_weights(stratum: np.ndarray, psu: np.ndarray, weight: np.ndarray,
                      n_rep: int, rng: np.random.Generator,
                      rescaled: bool = True) -> tuple[np.ndarray, int]:
    """Rao-Wu-Yue rescaled bootstrap replicate weights.

    Within each stratum of ``n_h`` PSUs, ``m_h = n_h - 1`` PSUs are drawn with
    replacement and the weight of PSU ``i`` becomes

        w* = w [1 - lambda + lambda (n_h / m_h) r_hi],
        lambda = sqrt(m_h / (n_h - 1)),

    which is ``lambda = 1`` at ``m_h = n_h - 1``.  With ``rescaled=False`` the
    plain ``m``-of-``m`` scheme is used instead, for comparison with analyses
    built on it.

    Singleton strata cannot be resampled; their weights are carried through
    unchanged, contributing no variance, and their count is returned.

    Returns ``(W, n_singleton)`` with ``W`` of shape ``(n_obs, n_rep)``.
    """
    key = pd.MultiIndex.from_arrays([stratum, psu])
    unit = pd.factorize(key)[0]
    strat = pd.factorize(stratum)[0]

    n_units = unit.max() + 1
    unit_stratum = np.zeros(n_units, dtype=np.int64)
    unit_stratum[unit] = strat

    W = np.repeat(weight[:, None], n_rep, axis=1).astype(np.float64)
    counts = np.zeros((n_units, n_rep))
    n_singleton = 0

    for h in range(strat.max() + 1):
        members = np.flatnonzero(unit_stratum == h)
        n_h = members.size
        if n_h < 2:
            n_singleton += 1
            counts[members] = 1.0
            continue
        m_h = n_h - 1 if rescaled else n_h
        draws = rng.integers(0, n_h, size=(m_h, n_rep))
        r = np.zeros((n_h, n_rep))
        np.add.at(r, (draws, np.arange(n_rep)[None, :].repeat(m_h, axis=0)), 1.0)
        if rescaled:
            lam = np.sqrt(m_h / (n_h - 1))
            counts[members] = 1.0 - lam + lam * (n_h / m_h) * r
        else:
            counts[members] = (n_h / m_h) * r

    return W * counts[unit], n_singleton


def weighted_cdf(indicator: np.ndarray, weight: np.ndarray,
                 group: np.ndarray, n_group: int) -> np.ndarray:
    """Weighted CDF per group.

    ``indicator`` is ``(n_obs, n_threshold)`` with ``1{y <= t}``; ``weight`` is
    ``(n_obs,)`` or ``(n_obs, n_rep)``.  Returns ``(n_group, n_threshold)`` or
    ``(n_group, n_threshold, n_rep)``.  Groups with no weight yield ``nan``.
    """
    w = weight[:, None] if weight.ndim == 1 else weight
    num = np.zeros((n_group, indicator.shape[1], w.shape[1]))
    den = np.zeros((n_group, w.shape[1]))
    np.add.at(num, group, indicator[:, :, None] * w[:, None, :])
    np.add.at(den, group, w)
    with np.errstate(invalid="ignore", divide="ignore"):
        out = num / den[:, None, :]
    out[den[:, None, :].repeat(indicator.shape[1], axis=1) == 0] = np.nan
    return out[:, :, 0] if weight.ndim == 1 else out
