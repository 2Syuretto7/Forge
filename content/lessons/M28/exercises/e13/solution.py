import numpy as np


def gd_path(A, x0, step, iters):
    """Iterates of gradient descent on (1/2) x^T A x."""
    A = np.asarray(A, dtype=float)
    x = np.array(x0, dtype=float)
    out = [x.copy()]
    for _ in range(iters):
        x = x - step * (A @ x)
        out.append(x.copy())
    return np.array(out)


def growth_factor(A, step):
    """Largest per-step multiplier of the error."""
    return float(np.max(np.abs(1 - step * np.linalg.eigvalsh(np.asarray(A, dtype=float)))))


def largest_stable_step(A):
    """2 / lambda_max."""
    return float(2 / np.linalg.eigvalsh(np.asarray(A, dtype=float))[-1])
