import numpy as np


def sample_preferences(r, n, rng):
    """Count matrix of n Bradley-Terry comparisons."""
    r = np.asarray(r)
    K = len(r)
    i = rng.integers(0, K, n)
    j = (i + rng.integers(1, K, n)) % K
    win = rng.random(n) < 1 / (1 + np.exp(-(r[i] - r[j])))
    N = np.zeros((K, K))
    np.add.at(N, (np.where(win, i, j), np.where(win, j, i)), 1)
    return N


def _log_softmax(z):
    m = np.max(z)
    return z - m - np.log(np.sum(np.exp(z - m)))


def train_dpo(ref_logp, N, beta, steps=3000, lr=5.0):
    """Gradient descent on the DPO loss over softmax logits."""
    z = np.zeros(len(ref_logp))
    total = np.sum(N)
    for _ in range(steps):
        d = _log_softmax(z) - ref_logp
        h = beta * (d[:, None] - d[None, :])
        s = N / (1 + np.exp(h))
        z -= lr * (-beta * (s.sum(axis=1) - s.sum(axis=0)) / total)
    return z


def tv(p, q):
    """Total variation distance."""
    return 0.5 * float(np.sum(np.abs(np.asarray(p) - np.asarray(q))))
