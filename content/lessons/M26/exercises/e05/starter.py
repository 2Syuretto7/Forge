import numpy as np


def forward_diff(f, x, h):
    """(f(x + h) - f(x)) / h."""
    raise NotImplementedError


def central_diff(f, x, h):
    """(f(x + h) - f(x - h)) / (2h)."""
    raise NotImplementedError


def complex_step(f, x, h=1e-20):
    """Im f(x + ih) / h."""
    raise NotImplementedError


def error_curve(f, df, x, hs, method):
    """Absolute errors of method(f, x, h) for each h."""
    raise NotImplementedError
