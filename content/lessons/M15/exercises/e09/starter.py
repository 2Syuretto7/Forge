import sys


def scaled_step(x, kind):
    """Step scaled to the size of x."""
    raise NotImplementedError


def check_derivative(f, df, xs, tol=1e-6):
    """Points where df disagrees with a central difference."""
    raise NotImplementedError
