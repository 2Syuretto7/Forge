import numpy as np


def marginal(P, axes):
    """Sum out the variables not in axes."""
    other = tuple(k for k in range(P.ndim) if k not in axes)
    return P.sum(axis=other)


def independent(P, i, j, tol=1e-12):
    """Independence of variables i and j."""
    M = marginal(P, (i, j)) if i < j else marginal(P, (j, i)).T
    return bool(np.allclose(M, np.outer(M.sum(axis=1), M.sum(axis=0)), atol=tol))


def cond_independent(P, tol=1e-12):
    """Independence of variables 0 and 1 given variable 2."""
    for c in range(P.shape[2]):
        pc = P[:, :, c].sum()
        if pc == 0:
            continue
        M = P[:, :, c] / pc
        if not np.allclose(M, np.outer(M.sum(axis=1), M.sum(axis=0)), atol=tol):
            return False
    return True


def two_tests(prev, sens, spec):
    """Joint table of (test 1, test 2, disease)."""
    P = np.zeros((2, 2, 2))
    for d, pd in ((1, prev), (0, 1 - prev)):
        p_pos = sens if d else 1 - spec
        for t1 in (0, 1):
            for t2 in (0, 1):
                P[t1, t2, d] = pd * (p_pos if t1 else 1 - p_pos) * (p_pos if t2 else 1 - p_pos)
    return P
