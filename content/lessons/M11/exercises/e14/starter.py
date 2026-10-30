import numpy as np


# provided
def rank(A, tol=None):
    U = np.array(A, dtype=float)
    m, n = U.shape
    big = np.max(np.abs(U)) if U.size else 0.0
    if big == 0:
        return 0
    if tol is None:
        tol = max(m, n) * 1e-12 * big
    r = 0
    for k in range(min(m, n)):
        block = np.abs(U[k:, k:])
        i, j = np.unravel_index(np.argmax(block), block.shape)
        if block[i, j] <= tol:
            break
        i, j = i + k, j + k
        U[[k, i]] = U[[i, k]]
        U[:, [k, j]] = U[:, [j, k]]
        U[k + 1:, k:] -= np.outer(U[k + 1:, k] / U[k, k], U[k, k:])
        r += 1
    return r


# provided
def make_noisy(seed=0):
    rng = np.random.default_rng(seed)
    return rng.normal(size=(50, 5)) @ rng.normal(size=(5, 30)) + 1e-6 * rng.normal(size=(50, 30))


def rank_sweep(A, tols):
    """Rank for each tolerance."""
    raise NotImplementedError


def pivots(A):
    """Absolute pivots of complete-pivoting elimination, no tolerance."""
    raise NotImplementedError


def gap_rank(p):
    """Number of pivots before the largest drop."""
    raise NotImplementedError


def honest_tol(noise, shape):
    """A tolerance just above the noise."""
    raise NotImplementedError
