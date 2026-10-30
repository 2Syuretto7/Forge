import numpy as np


def nll(z, y, T):
    """Mean negative log-likelihood at temperature T."""
    u = z / T
    return float(np.mean(y * np.logaddexp(0, -u) + (1 - y) * np.logaddexp(0, u)))


def dnll_dT(z, y, T):
    """Derivative of the NLL in T."""
    u = z / T
    s = 1 / (1 + np.exp(-np.clip(u, -700, 700)))
    return float(np.mean((s - y) * (-z / T ** 2)))


def fit_temperature(z, y):
    """Bisection on the derivative over [0.25, 10]."""
    lo, hi = 0.25, 10.0
    for _ in range(60):
        m = (lo + hi) / 2
        if dnll_dT(z, y, m) < 0:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2
