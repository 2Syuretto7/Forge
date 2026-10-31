import numpy as np


def softmax(z):
    """Stable softmax."""
    e = np.exp(z - np.max(z))
    return e / e.sum()


def log_softmax(z):
    """Stable log-softmax."""
    m = np.max(z)
    return z - m - np.log(np.sum(np.exp(z - m)))


def score(a, z):
    """Gradient of log pi_a in the logits."""
    g = -softmax(z)
    g[a] += 1
    return g


def exact_grad(z, r):
    """Gradient of the expected reward in the logits."""
    p = softmax(z)
    return p * (r - p @ r)


def reinforce(z, r, n, rng):
    """Average of n REINFORCE estimates."""
    p = softmax(z)
    a = rng.choice(len(z), size=n, p=p)
    E = np.zeros((n, len(z)))
    E[np.arange(n), a] = 1
    return np.mean(np.asarray(r)[a][:, None] * (E - p), axis=0)
