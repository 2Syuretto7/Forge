import math
import numpy as np


def iterations_bound(kappa, eps, step="best"):
    """Iterations the rate bound guarantees for relative error eps."""
    rho = (kappa - 1) / (kappa + 1) if step == "best" else 1 - 1 / kappa
    return math.ceil(math.log(eps) / math.log(rho))


def iterations_needed(A, b, x0, step, eps, max_iter=10**6):
    """Gradient-descent steps until the error falls below eps times the initial error."""
    xs = np.linalg.solve(A, b)
    x = np.array(x0, dtype=float)
    e0 = np.linalg.norm(x - xs)
    for k in range(max_iter + 1):
        if np.linalg.norm(x - xs) <= eps * e0:
            return k
        x = x - step * (A @ x - b)
    return max_iter
