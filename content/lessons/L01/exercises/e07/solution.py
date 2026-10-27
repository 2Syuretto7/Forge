import math
import numpy as np


def power_iteration(S, iters, seed=0):
    """S: symmetric (n, n). Return (lam: float, v: (n,) unit vector, largest entry positive)."""
    n = S.shape[0]
    x = np.random.default_rng(seed).normal(size=n)
    x = x / np.linalg.norm(x)
    for _ in range(iters):
        x = S @ x
        x = x / np.linalg.norm(x)
    i = np.argmax(np.abs(x))
    x = x * np.sign(x[i])
    return float(x @ S @ x), x


def gap_ratio(S):
    """Return |lambda_2| / |lambda_1| for the two eigenvalues largest in magnitude."""
    w = np.sort(np.abs(np.linalg.eigvalsh(S)))[::-1]
    return float(w[1] / w[0])


def iterations_needed(ratio, tol):
    """Smallest integer k with ratio**k <= tol (0 < ratio < 1, 0 < tol < 1)."""
    k = math.ceil(math.log(tol) / math.log(ratio) - 1e-12)
    return int(k)
