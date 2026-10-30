import numpy as np


def rank_by_dot(q, X):
    """Row indices by raw dot product, best first."""
    return [int(i) for i in np.argsort(-(X @ q), kind="stable")]


def rank_by_cosine(q, X):
    """Row indices by cosine similarity, best first."""
    s = (X @ q) / (np.linalg.norm(X, axis=1) * np.linalg.norm(q))
    return [int(i) for i in np.argsort(-s, kind="stable")]


def length_bias(q, X):
    """corr(lengths, dot scores) - corr(lengths, cosine scores)."""
    L = np.linalg.norm(X, axis=1)
    dots = X @ q
    cos = dots / (L * np.linalg.norm(q))
    return float(np.corrcoef(L, dots)[0, 1] - np.corrcoef(L, cos)[0, 1])


def make_trap(q, scale):
    """Row 0 along q (length 1); row 1 at 60 degrees from q with length scale."""
    qh = q / np.linalg.norm(q)
    r = np.zeros(q.size)
    r[np.argmin(np.abs(qh))] = 1.0
    p = r - (r @ qh) * qh
    p /= np.linalg.norm(p)
    return np.vstack([qh, scale * (0.5 * qh + np.sqrt(3) / 2 * p)])
