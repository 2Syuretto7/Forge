import math
import numpy as np

N0, D0 = 1e9, 1e10
TRUE = (1.69, 406.4, 0.34, 410.7, 0.28)


# provided
def make_runs(seed=1):
    rng = np.random.default_rng(seed)
    N, D = [a.ravel() for a in np.meshgrid(np.logspace(7, 9, 8), np.logspace(8.5, 10.5, 6))]
    E, A, alpha, B, beta = TRUE
    return N, D, E + A / N**alpha + B / D**beta + 0.004 * rng.standard_normal(N.size)


# provided
def held_out(seed=1):
    rng = np.random.default_rng(seed + 100)
    N, D = 6e9, 2e11
    E, A, alpha, B, beta = TRUE
    return N, D, E + A / N**alpha + B / D**beta + 0.004 * rng.standard_normal()


def _surface(theta, u, v):
    raise NotImplementedError


def fit(N, D, L, iters=200):
    """Levenberg-Marquardt fit of the Chinchilla form."""
    raise NotImplementedError


def predict(chin, N, D):
    """Loss predicted by a fit."""
    raise NotImplementedError


def bootstrap(N, D, L, B=100, seed=0):
    """Residual-bootstrap refits."""
    raise NotImplementedError


def predict_interval(samples, N, D, level=0.95):
    """Bootstrap interval for a new run's loss, including run-to-run noise."""
    raise NotImplementedError


# your answer
REPORT = """
"""
