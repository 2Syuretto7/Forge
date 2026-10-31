import numpy as np


def stationary_eig(P):
    """Left eigenvector of P for eigenvalue 1, normalized."""
    vals, vecs = np.linalg.eig(np.asarray(P, dtype=float).T)
    v = np.real(vecs[:, np.argmin(np.abs(vals - 1))])
    return v / v.sum()


def stationary_power(P, tol=1e-13, max_iter=100000):
    """Stationary distribution by repeated multiplication."""
    P = np.asarray(P, dtype=float)
    pi = np.ones(len(P)) / len(P)
    for _ in range(max_iter):
        new = pi @ P
        if np.max(np.abs(new - pi)) < tol:
            return new
        pi = new
    return pi


def stationary_sim(P, n, rng, x0=0):
    """Fraction of time a simulated path spends in each state."""
    C = np.cumsum(np.asarray(P, dtype=float), axis=1)
    last = C.shape[0] - 1
    u = rng.random(n)
    counts = np.zeros(len(C))
    x = x0
    for i in range(n):
        x = min(int(np.searchsorted(C[x], u[i], side="right")), last)
        counts[x] += 1
    return counts / n


def two_state(a, b):
    """Stationary distribution of the two-state chain."""
    return np.array([b / (a + b), a / (a + b)])
