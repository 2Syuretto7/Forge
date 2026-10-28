import numpy as np


def log_mse(theta, x, y):
    """theta = (log k, a). The mean squared error between log(k x^-a) and log y, and its gradient
    with respect to theta, as (value, array of 2)."""
    raise NotImplementedError


def fit_power_law(x, y):
    """Least-squares fit of y = k x^-a in log-log coordinates. Return (k, a)."""
    raise NotImplementedError
