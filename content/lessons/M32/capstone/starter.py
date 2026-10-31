import math
import numpy as np

PRIOR_SD = 5.0


# provided
def make_data(seed=0):
    rng = np.random.default_rng(seed)
    x = rng.standard_normal(100)
    y = (rng.random(100) < 1 / (1 + np.exp(-(0.5 + 1.5 * x)))).astype(float)
    return x, y


X, Y = make_data()


def log_post(theta):
    """Log posterior of (intercept, slope), for one vector or a stack of rows."""
    raise NotImplementedError


def grad_log_post(theta):
    """Gradient of log_post for one vector."""
    raise NotImplementedError


def run_chains(n_chains=4, n=5000, seed=0):
    """Random-walk Metropolis with a Laplace-shaped proposal, all chains at once."""

    raise NotImplementedError


def autocorr(x, max_lag):
    """Autocorrelations at lags 0..max_lag by the FFT."""
    raise NotImplementedError


def ess(x):
    """Effective sample size with pairwise truncation."""
    raise NotImplementedError


def r_hat(chains):
    """Potential scale reduction factor."""
    raise NotImplementedError


def diagnostics(samples):
    """Means, standard deviations, effective sample sizes, errors, R-hat and autocorrelations."""
    raise NotImplementedError


# your answer
REPORT = """
"""
