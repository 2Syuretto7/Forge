import numpy as np


def ce_from_probs(z, y):
    """Cross-entropy through probabilities."""
    z = np.asarray(z)
    e = np.exp(z - z.max())
    p = e / np.sum(e)
    with np.errstate(divide="ignore"):
        return float(-np.log(p[y]))


def ce_from_logits(z, y):
    """Cross-entropy straight from the logits."""
    z = np.asarray(z)
    m = z.max()
    return float(m + np.log(np.sum(np.exp(z - m))) - z[y])


def first_failure(dtype):
    """Smallest integer logit gap that makes ce_from_probs infinite."""
    g = 1
    while np.isfinite(ce_from_probs(np.array([g, 0], dtype=dtype), 1)):
        g += 1
    return g
