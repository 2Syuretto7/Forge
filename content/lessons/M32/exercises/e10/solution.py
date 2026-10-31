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
    r = y - X @ w
    return -0.5 * (r @ r) / sigma**2 - 0.5 * (w @ w) / tau**2


def grad_log_posterior(w, X, y, sigma=1.0, tau=1.0):
    """Gradient of log_posterior in w."""
    return X.T @ (y - X @ w) / sigma**2 - w / tau**2


def exact_posterior(X, y, sigma=1.0, tau=1.0):
    """Posterior mean and covariance."""
    cov = np.linalg.inv(X.T @ X / sigma**2 + np.eye(X.shape[1]) / tau**2)
    return cov @ X.T @ y / sigma**2, cov


def rw_chain(log_p, x0, step, n, rng):
    """Random-walk Metropolis: (samples, acceptance)."""
    x = np.asarray(x0, dtype=float)
    lx = log_p(x)
    out = np.empty((n, len(x)))
    z = rng.standard_normal((n, len(x)))
    logu = np.log(rng.random(n))
    acc = 0
    for i in range(n):
        y = x + step * z[i]
        ly = log_p(y)
        if logu[i] < ly - lx:
            x, lx = y, ly
            acc += 1
        out[i] = x
    return out, acc / n


def tune_rw(log_p, x0, rng, step=0.1, target=0.234, rounds=30, per_round=200):
    """Adapt the step toward a target acceptance rate."""
    x = np.asarray(x0, dtype=float)
    for _ in range(rounds):
        s, a = rw_chain(log_p, x, step, per_round, rng)
        x = s[-1]
        step *= math.exp(2 * (a - target))
    return step, x
