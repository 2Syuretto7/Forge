import math
import numpy as np


def sketch(A, b, s, rng):
    """Gaussian sketch of A and b with s rows."""
    S = rng.standard_normal((s, A.shape[0])) / math.sqrt(s)
    return S @ A, S @ b


def sketched_lstsq(A, b, s, rng):
    """Least squares on the sketched problem."""
    SA, Sb = sketch(A, b, s, rng)
    return np.linalg.lstsq(SA, Sb, rcond=None)[0]


def residual_ratio(A, b, x):
    """Residual of x relative to the optimal residual."""
    best = np.linalg.lstsq(A, b, rcond=None)[0]
    return float(np.linalg.norm(A @ x - b) / np.linalg.norm(A @ best - b))


def predicted_ratio(n, s):
    """Typical residual ratio of a Gaussian sketch."""
    return math.sqrt(1 + n / (s - n - 1))
