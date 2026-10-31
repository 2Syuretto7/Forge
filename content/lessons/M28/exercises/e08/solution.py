import numpy as np


def objective(A, b, x):
    """(1/2) x^T A x - b^T x."""
    return float(0.5 * x @ A @ x - b @ x)


def solve_equality_qp(A, b, C, d):
    """Minimizer and multipliers of the equality-constrained quadratic."""
    A, C = np.asarray(A, dtype=float), np.atleast_2d(np.asarray(C, dtype=float))
    n, m = A.shape[0], C.shape[0]
    K = np.block([[A, C.T], [C, np.zeros((m, m))]])
    sol = np.linalg.solve(K, np.concatenate([np.asarray(b, dtype=float), np.atleast_1d(d).astype(float)]))
    return sol[:n], sol[n:]


def projected_minimum_check(A, b, C, d, x, trials, rng):
    """Smallest objective increase over random feasible perturbations."""
    C = np.atleast_2d(np.asarray(C, dtype=float))
    m = C.shape[0]
    N = np.linalg.svd(C)[2][m:].T
    f0 = objective(A, b, x)
    return min(objective(A, b, x + N @ rng.normal(size=N.shape[1])) - f0 for _ in range(trials))
