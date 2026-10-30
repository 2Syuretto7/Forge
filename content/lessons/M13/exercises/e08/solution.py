import numpy as np


def google_matrix(links, n, d=0.85):
    """Dense random-surfer matrix."""
    S = np.zeros((n, n))
    out = np.zeros(n)
    for s, _ in links:
        out[s] += 1
    for s, t in links:
        S[t, s] += 1 / out[s]
    S[:, out == 0] = 1 / n
    return d * S + (1 - d) / n


def pagerank(links, n, d=0.85, tol=1e-12):
    """Stationary distribution by power iteration."""
    G = google_matrix(links, n, d)
    p = np.full(n, 1 / n)
    while True:
        q = G @ p
        if np.abs(q - p).sum() < tol:
            return q
        p = q
