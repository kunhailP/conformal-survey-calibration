"""Design-aware conformal prediction for survey-estimated distribution curves.

Two prediction targets are kept apart throughout:

    T1 (observed)  a further *survey estimate*      \\tilde F_{K+1}
    T2 (latent)    its *population distribution*    F_{K+1}

Every construction in :mod:`dac.bands` declares which target it guarantees and
under what assumption.  Nothing in this package infers T2 coverage from T1
coverage without an explicit assumption object.
"""

__version__ = "0.1.0"

from dac import bands, diagnostics, generators  # noqa: F401
