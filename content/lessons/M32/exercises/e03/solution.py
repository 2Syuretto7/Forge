import numpy as np


def is_reversible(P, pi, tol=1e-12):
    """Detailed balance pi_i P_ij = pi_j P_ji for all pairs."""
    F = np.asarray(pi, dtype=float)[:, None] * np.asarray(P, dtype=float)
    return bool(np.max(np.abs(F - F.T)) < tol)


def metropolis_matrix(pi, Q):
    """Metropolis-Hastings transition matrix for target pi and proposal Q."""
    pi = np.asarray(pi, dtype=float)
    Q = np.asarray(Q, dtype=float)
    n = len(pi)
    P = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j and Q[i, j] > 0:
                P[i, j] = Q[i, j] * min(1.0, pi[j] * Q[j, i] / (pi[i] * Q[i, j]))
        P[i, i] = 1 - P[i].sum()
    return P


def cycle_chain(n, p):
    """Clockwise step with probability p, otherwise stay."""
    P = (1 - p) * np.eye(n)
    for i in range(n):
        P[i, (i + 1) % n] += p
    return P
