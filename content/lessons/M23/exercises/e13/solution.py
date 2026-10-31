import numpy as np


# provided
def try_cholesky(S):
    """The Cholesky factor of S, or None if S is not positive definite."""
    try:
        L = np.linalg.cholesky(S)
    except np.linalg.LinAlgError:
        return None
    return L if np.all(np.isfinite(L)) and np.all(np.diag(L) > 0) else None


def sample_cov_rank(n, d, seed, tol=1e-10):
    """Numerical rank of the sample covariance of n samples in d dimensions."""
    X = np.random.default_rng(seed).standard_normal((n, d))
    e = np.linalg.eigvalsh(np.cov(X, rowvar=False))
    return int(np.sum(e > tol * e[-1]))


def cholesky_with_jitter(S, start=1e-10, factor=10, max_tries=20):
    """Cholesky factor of S + j I for the smallest jitter j that works."""
    S = np.asarray(S, dtype=float)
    I = np.eye(S.shape[0])
    j = 0.0
    for k in range(max_tries + 1):
        L = try_cholesky(S + j * I)
        if L is not None:
            return L, j
        j = start * factor**k
    raise np.linalg.LinAlgError("no jitter made the matrix positive definite")
