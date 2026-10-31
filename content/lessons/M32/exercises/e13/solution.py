import math
from functools import reduce
import numpy as np


def communicating_classes(P):
    """Classes of mutually reachable states."""
    A = (np.asarray(P) > 0).astype(int)
    n = len(A)
    R = np.eye(n, dtype=int)
    while True:
        new = ((R + R @ A) > 0).astype(int)
        if np.array_equal(new, R):
            break
        R = new
    classes = {tuple(j for j in range(n) if R[i, j] and R[j, i]) for i in range(n)}
    return sorted(list(c) for c in classes)


def n_stationary(P, tol=1e-9):
    """Number of eigenvalues equal to 1."""
    return int(np.sum(np.abs(np.linalg.eigvals(np.asarray(P, dtype=float)) - 1) < tol))


def period(P, i):
    """gcd of return times to state i, up to 3n steps."""
    A = (np.asarray(P) > 0).astype(int)
    n = len(A)
    M = np.eye(n, dtype=int)
    times = []
    for t in range(1, 3 * n + 1):
        M = ((M @ A) > 0).astype(int)
        if M[i, i]:
            times.append(t)
    return reduce(math.gcd, times) if times else 0


def long_run(P, x0, steps=2000):
    """Distribution after many steps from x0."""
    d = np.zeros(len(P))
    d[x0] = 1.0
    for _ in range(steps):
        d = d @ P
    return d
