import numpy as np


def power_history(A, x0, k):
    """Unit vectors of power iteration, start included."""
    x = np.asarray(x0, dtype=float)
    out = [x / np.linalg.norm(x)]
    for _ in range(k):
        y = A @ out[-1]
        out.append(y / np.linalg.norm(y))
    return out


def settled(history, tol=1e-8):
    """Whether the last two vectors lie along the same line."""
    return bool(abs(history[-2] @ history[-1]) >= 1 - tol)


def shifted_top(A, shift, k, x0):
    """Eigenvalue of A found by power iteration on A + shift I."""
    v = power_history(A + shift * np.eye(A.shape[0]), x0, k)[-1]
    return float(v @ A @ v)
