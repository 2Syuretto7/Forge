import numpy as np


def forward_diff(f, x, h):
    """(f(x + h) - f(x)) / h."""
    return (f(x + h) - f(x)) / h


def central_diff(f, x, h):
    """(f(x + h) - f(x - h)) / (2h)."""
    return (f(x + h) - f(x - h)) / (2 * h)


def complex_step(f, x, h=1e-20):
    """Im f(x + ih) / h."""
    return float(np.imag(f(x + 1j * h)) / h)


def error_curve(f, df, x, hs, method):
    """Absolute errors of method(f, x, h) for each h."""
    return [abs(float(np.real(method(f, x, h))) - df(x)) for h in hs]
