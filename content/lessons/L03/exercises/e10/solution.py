import numpy as np


def jacobian_forward(jvp, n):
    """Return (J, number of jvp calls)."""
    cols = [np.asarray(jvp(np.eye(n)[j])) for j in range(n)]
    return np.stack(cols, axis=1), n


def jacobian_reverse(vjp, m):
    """Return (J, number of vjp calls)."""
    rows = [np.asarray(vjp(np.eye(m)[i])) for i in range(m)]
    return np.stack(rows, axis=0), m


def cheaper_mode(n, m):
    if n < m:
        return "forward"
    if m < n:
        return "reverse"
    return "either"
