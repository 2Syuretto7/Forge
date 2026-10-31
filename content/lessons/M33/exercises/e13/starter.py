import numpy as np


# provided
def make_nonsymmetric(n, rng):
    G = rng.standard_normal((n, n))
    S = G @ G.T / n + np.eye(n)
    return S + 0.4 * np.triu(rng.standard_normal((n, n)), 1)


def cg_residuals(A, b, iters):
    """Relative residuals of plain CG, whatever A is."""
    raise NotImplementedError


def cgnr(A, b, tol=1e-10, max_iter=5000):
    """CG on the normal equations: (x, iterations)."""
    raise NotImplementedError
