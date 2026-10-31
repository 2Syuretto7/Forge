import numpy as np


def softmax(z):
    """Numerically stable softmax."""
    e = np.exp(z - np.max(z))
    return e / e.sum()


def softmax_jacobian(z):
    """Jacobian of the softmax."""
    p = softmax(z)
    return np.diag(p) - np.outer(p, p)


def attention_stats(d, n_keys, scaled, trials, rng):
    """(mean largest weight, median Jacobian Frobenius norm) of random attention."""
    top, jn = [], []
    for _ in range(trials):
        q = rng.standard_normal(d)
        K = rng.standard_normal((n_keys, d))
        z = K @ q / (np.sqrt(d) if scaled else 1.0)
        top.append(softmax(z).max())
        jn.append(np.linalg.norm(softmax_jacobian(z)))
    return float(np.mean(top)), float(np.median(jn))
