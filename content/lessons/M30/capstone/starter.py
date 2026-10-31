import numpy as np


# provided
def make_data(n=400, seed=0):
    rng = np.random.default_rng(seed)
    Z = rng.normal(size=(n, 4))
    y = np.sign(Z @ np.array([1.0, -1.0, 0.5, 2.0]) + 0.7 + 0.5 * rng.normal(size=n))
    return np.hstack([Z, np.ones((n, 1))]), y


def _G(alpha, X, y):
    raise NotImplementedError


def kkt_residual(alpha, X, y, C):
    """Largest projected-gradient violation of the dual."""
    raise NotImplementedError


def duality_gap(alpha, X, y, C):
    """Relative duality gap."""
    raise NotImplementedError


def solve(X, y, C, tol=1e-5, max_epochs=500, seed=0):
    """Dual coordinate ascent until the KKT residual is at most tol."""
    raise NotImplementedError


def kl_optimum(pi, r, beta):
    """pi exp(r / beta), normalized."""
    raise NotImplementedError


def _objective(p, pi, r, beta):
    raise NotImplementedError


def check_kl_optimum(pi, r, beta, trials, rng):
    """Largest improvement any random distribution makes over kl_optimum."""
    raise NotImplementedError


def log_ratio_slope(pi, r, beta):
    """Slope of log(p / pi) against r."""
    raise NotImplementedError
