import numpy as np


def nll(z, y, T):
    """Mean negative log-likelihood at temperature T."""
    raise NotImplementedError


def dnll_dT(z, y, T):
    """Derivative of the NLL in T."""
    raise NotImplementedError


def fit_temperature(z, y):
    """Bisection on the derivative over [0.25, 10]."""
    raise NotImplementedError
