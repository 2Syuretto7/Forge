import numpy as np


def inverse_iteration(A, mu, iters=50, seed=0):
    """Eigenpair of A with eigenvalue nearest mu."""
    n = A.shape[0]
    x = np.random.default_rng(seed).normal(size=n)
    M = A - mu * np.eye(n)
    for _ in range(iters):
        x = np.linalg.solve(M, x)
        x = x / np.linalg.norm(x)
    return float(x @ A @ x), x


def all_by_shifts(A, guesses):
    """Distinct eigenvalues found from the guesses, sorted."""
    return sorted({round(inverse_iteration(A, g)[0], 10) for g in guesses})
