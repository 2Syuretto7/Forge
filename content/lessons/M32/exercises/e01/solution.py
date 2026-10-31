import numpy as np


def check_stochastic(P):
    """True for a square matrix with nonnegative entries and unit row sums."""
    P = np.asarray(P, dtype=float)
    if P.ndim != 2 or P.shape[0] != P.shape[1]:
        return False
    return bool(np.all(P >= 0) and np.all(np.abs(P.sum(axis=1) - 1) < 1e-12))


def distribution_after(pi0, P, n):
    """pi0 P^n."""
    pi = np.asarray(pi0, dtype=float)
    for _ in range(n):
        pi = pi @ P
    return pi


def simulate(P, x0, n, rng):
    """A path of n + 1 states of the chain P starting at x0."""
    C = np.cumsum(np.asarray(P, dtype=float), axis=1)
    last = C.shape[0] - 1
    u = rng.random(n)
    path = [x0]
    x = x0
    for i in range(n):
        x = min(int(np.searchsorted(C[x], u[i], side="right")), last)
        path.append(x)
    return np.array(path)
