import math
import numpy as np


# provided
def make_data(seed=0, n=300, d=50):
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n, d))
    w = rng.standard_normal(d)
    return X, X @ w + rng.standard_normal(n)


def log_posterior(w, X, y, sigma=1.0, tau=1.0):
    """Log posterior of Bayesian linear regression, up to a constant."""
    raise NotImplementedError


def grad_log_posterior(w, X, y, sigma=1.0, tau=1.0):
    """Gradient of log_posterior in w."""
    raise NotImplementedError


def exact_posterior(X, y, sigma=1.0, tau=1.0):
    """Posterior mean and covariance."""
    raise NotImplementedError


def rw_chain(log_p, x0, step, n, rng):
    """Random-walk Metropolis: (samples, acceptance)."""
    raise NotImplementedError


def tune_rw(log_p, x0, rng, step=0.1, target=0.234, rounds=30, per_round=200):
    """Adapt the step toward a target acceptance rate."""
    raise NotImplementedError
