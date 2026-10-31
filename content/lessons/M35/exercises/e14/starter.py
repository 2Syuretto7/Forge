import numpy as np


def broken_law(x, E=1.7, A=2.0, a1=0.5, a2=0.2, xb=1e3):
    """A power law whose exponent changes at xb."""
    raise NotImplementedError


def _model(theta, x):
    raise NotImplementedError


def _jac(theta, x):
    raise NotImplementedError


def fit_and_band(x, y, x0, z=1.96, iters=100):
    """Prediction and delta-method half-width at x0."""
    raise NotImplementedError


def inside(pred, half, truth):
    """Whether the truth lies in the band."""
    raise NotImplementedError
