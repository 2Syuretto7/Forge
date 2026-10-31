import numpy as np


def softmax(z):
    """Stable softmax of a 1-D array."""
    z = np.asarray(z, dtype=float)
    e = np.exp(z - z.max())
    return e / e.sum()


def nll(z, counts):
    """-sum_j counts_j * log softmax(z)_j as a float."""
    z = np.asarray(z, dtype=float)
    m = z.max()
    logp = z - (m + np.log(np.sum(np.exp(z - m))))
    return float(-np.sum(np.asarray(counts) * logp))


def grad_nll(z, counts):
    """Gradient of nll with respect to z, shape (K,)."""
    counts = np.asarray(counts, dtype=float)
    return counts.sum() * softmax(z) - counts


def mle_probs(counts):
    """Closed-form MLE of the category probabilities."""
    counts = np.asarray(counts, dtype=float)
    return counts / counts.sum()
