"""Contract tests: each band must deliver the guarantee it advertises.

These are not smoke tests.  Each one fails if a stated property of the
construction stops holding, so a claim in the manuscript cannot silently drift
away from the code that supports it.
"""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from dac import bands, diagnostics, generators  # noqa: E402

ALPHA = 0.10


def _sample(rng, n, k, d, rho, cg=0.0, cs=0.0):
    sigma = generators.noise_scale(rho)
    Lg = generators.cholesky(generators.equicorrelated(d, cg))
    Ls = generators.cholesky(generators.equicorrelated(d, cs))
    g = generators.draw_curves(rng, n, k + 1, Lg)
    s = sigma * generators.draw_curves(rng, n, k + 1, Ls)
    return g, g + s, sigma


def test_anchor_attains_its_finite_sample_floor_on_T1():
    """The anchor's observed-target coverage must reach ceil((1-a)(K+1))/(K+1)."""
    rng = np.random.default_rng(20260909)
    k, d, n = 60, 8, 40000
    g, y, _ = _sample(rng, n, k, d, rho=0.5, cg=0.0, cs=0.8)
    r = bands.observed_anchor(y[:, :k], ALPHA)
    hit = (np.max(np.abs(y[:, k]), axis=1) <= r).mean()
    floor = bands.conformal_rank(k, ALPHA) / (k + 1)
    assert hit >= floor - 4 * np.sqrt(floor * (1 - floor) / n)


def test_anchor_T1_guarantee_survives_shape_violation():
    """T1 needs exchangeability only, so mismatched correlations cannot break it."""
    rng = np.random.default_rng(7)
    k, d, n = 100, 24, 20000
    _, y, _ = _sample(rng, n, k, d, rho=0.8, cg=0.0, cs=0.95)
    r = bands.observed_anchor(y[:, :k], ALPHA)
    hit = (np.max(np.abs(y[:, k]), axis=1) <= r).mean()
    assert hit > 1 - ALPHA - 0.01


def test_oracle_rescaling_loses_T2_coverage_when_shape_fails():
    """The manuscript's central negative claim, as an executable assertion."""
    rng = np.random.default_rng(11)
    k, d, n = 250, 48, 20000
    g, y, sigma = _sample(rng, n, k, d, rho=0.8, cg=0.0, cs=0.95)
    r = bands.oracle_rescaled(y[:, :k], ALPHA, np.sqrt(1 + sigma ** 2))
    hit = (np.max(np.abs(g[:, k]), axis=1) <= r).mean()
    assert hit < 1 - ALPHA - 0.05, "shape violation no longer costs coverage"


def test_oracle_rescaling_is_valid_when_shape_holds():
    """The same construction must be sound when its assumption is satisfied."""
    rng = np.random.default_rng(13)
    k, d, n = 250, 48, 20000
    g, y, sigma = _sample(rng, n, k, d, rho=0.8, cg=0.5, cs=0.5)
    r = bands.oracle_rescaled(y[:, :k], ALPHA, np.sqrt(1 + sigma ** 2))
    hit = (np.max(np.abs(g[:, k]), axis=1) <= r).mean()
    assert abs(hit - (1 - ALPHA)) < 0.015


def test_noise_enlargement_contains_the_anchor_it_widens():
    rng = np.random.default_rng(17)
    _, y, sigma = _sample(rng, 500, 80, 8, rho=0.5)
    wide = bands.noise_enlargement(y[:, :80], ALPHA, sigma, 8)
    assert np.all(wide >= bands.observed_anchor(y[:, :80], ALPHA))


def test_quantile_is_infinite_when_the_rank_does_not_exist():
    """An uninformative band must say so rather than silently returning the max."""
    rng = np.random.default_rng(3)
    _, y, _ = _sample(rng, 5, 6, 8, rho=0.5)
    assert np.all(np.isinf(bands.observed_anchor(y[:, :6], 0.05)))


@pytest.mark.parametrize("k", [30, 94, 250])
def test_reliability_floor_matches_the_reported_threshold(k):
    assert diagnostics.reliability_floor(k) == pytest.approx(np.sqrt(2 / (k - 1)))


def test_reported_population_floor_is_ninety_four():
    """94 is the intercept of this diagnostic at its frozen tuning constant."""
    assert diagnostics.min_populations(diagnostics.TAU_D) == 94
    assert diagnostics.reliability_floor(94) <= diagnostics.TAU_D
    assert diagnostics.reliability_floor(93) > diagnostics.TAU_D


def test_design_share_inverts_the_noise_scale():
    for rho in (0.29, 0.52, 0.8):
        sigma = generators.noise_scale(rho)
        assert diagnostics.design_share(np.array([sigma ** 2]),
                                        np.array([1 + sigma ** 2])) == pytest.approx(rho)


def test_rwy_bootstrap_preserves_the_weighted_total():
    """Rao-Wu-Yue at m = n - 1 reproduces the population total on every replicate."""
    from dac.survey import replicate_weights
    rng = np.random.default_rng(41)
    stratum = np.repeat(np.arange(5), 8 * 4)
    psu = np.repeat(np.arange(40), 4)
    w = rng.uniform(0.5, 2.0, size=len(stratum))
    W, n_single = replicate_weights(stratum, psu, w, 200, rng)
    assert n_single == 0
    assert np.allclose(W.sum(axis=0), w.sum())


def test_rwy_bootstrap_recovers_a_clustered_standard_error():
    """The replicate SD must match the analytic clustered SE of a mean."""
    from dac.survey import replicate_weights
    rng = np.random.default_rng(5)
    n_psu, per = 60, 6
    stratum = np.zeros(n_psu * per, dtype=int)
    psu = np.repeat(np.arange(n_psu), per)
    w = np.ones(n_psu * per)
    y = (rng.normal(size=(n_psu, 1)) + 0.4 * rng.normal(size=(n_psu, per))).ravel()
    W, _ = replicate_weights(stratum, psu, w, 4000, rng)
    boot = ((W * y[:, None]).sum(0) / W.sum(0)).std()
    analytic = y.reshape(-1, per).mean(1).std(ddof=1) / np.sqrt(n_psu)
    assert abs(boot - analytic) / analytic < 0.10
