import numpy as np


def _softmax(z):
    e = np.exp(z - np.max(z))
    return e / e.sum()


def gradient_variance(z, r, n, rng, b=0.0):
    """Total variance of single-sample REINFORCE estimates."""
    p = _softmax(z)
    a = rng.choice(len(z), size=n, p=p)
    E = np.zeros((n, len(z)))
    E[np.arange(n), a] = 1
    G = (np.asarray(r)[a] - b)[:, None] * (E - p)
    return float(np.sum(np.var(G, axis=0)))


def train(means, offset, steps, lr, use_baseline, rng):
    """REINFORCE on a deterministic bandit; probability of the best arm at the end."""
    r = np.asarray(means, dtype=float) + offset
    z = np.zeros(len(r))
    b = None
    for _ in range(steps):
        p = _softmax(z)
        a = rng.choice(len(r), p=p)
        if b is None:
            b = r[a]
        g = -p
        g[a] += 1
        z += lr * (r[a] - (b if use_baseline else 0.0)) * g
        if use_baseline:
            b += 0.05 * (r[a] - b)
    return float(_softmax(z)[int(np.argmax(r))])
