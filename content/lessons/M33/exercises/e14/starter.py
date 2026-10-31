import numpy as np


# provided
def make_matrix(m, n, decay, rng):
    U = np.linalg.qr(rng.standard_normal((m, n)))[0]
    V = np.linalg.qr(rng.standard_normal((n, n)))[0]
    return (U / np.arange(1, n + 1) ** decay) @ V.T


def _approx(A, k, p, q, rng):
    raise NotImplementedError


def rsvd_error_ratio(A, s, k, p, q, rng):
    """Frobenius error relative to the optimum."""
    raise NotImplementedError


def spectral_error_ratio(A, s, k, p, q, rng):
    """Spectral error relative to sigma_{k+1}."""
    raise NotImplementedError
