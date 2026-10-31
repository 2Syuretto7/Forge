import numpy as np


def tv(p, q):
    """Total variation distance."""
    return 0.5 * float(np.sum(np.abs(np.asarray(p) - np.asarray(q))))


def lazy_cycle(n):
    """Lazy random walk on a ring."""
    P = 0.5 * np.eye(n)
    for i in range(n):
        P[i, (i + 1) % n] += 0.25
        P[i, (i - 1) % n] += 0.25
    return P


def spectral_gap(P):
    """1 minus the second largest eigenvalue modulus."""
    mods = np.sort(np.abs(np.linalg.eigvals(P)))[::-1]
    return float(1 - mods[1])


def mixing_time(P, eps=0.25):
    """Worst-start steps until total variation at most eps."""
    P = np.asarray(P, dtype=float)
    vals, vecs = np.linalg.eig(P.T)
    pi = np.real(vecs[:, np.argmin(np.abs(vals - 1))])
    pi = pi / pi.sum()
    M = np.eye(len(P))
    t = 0
    while max(tv(row, pi) for row in M) > eps:
        M = M @ P
        t += 1
    return t
