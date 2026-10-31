import numpy as np


def _log_softmax(z):
    m = np.max(z)
    return z - m - np.log(np.sum(np.exp(z - m)))


def train_dpo(ref_logp, N, beta, steps, lr=5.0):
    """Gradient descent on the DPO loss over softmax logits."""
    z = np.zeros(len(ref_logp))
    total = np.sum(N)
    for _ in range(steps):
        d = _log_softmax(z) - ref_logp
        h = beta * (d[:, None] - d[None, :])
        s = N / (1 + np.exp(h))
        z -= lr * (-beta * (s.sum(axis=1) - s.sum(axis=0)) / total)
    return z


def prob_gap(z):
    """Largest minus second largest probability."""
    p = np.sort(np.exp(_log_softmax(np.asarray(z))))[::-1]
    return float(p[0] - p[1])


def loss_at(z, ref_logp, N, beta):
    """DPO loss."""
    d = _log_softmax(np.asarray(z)) - ref_logp
    h = beta * (d[:, None] - d[None, :])
    return float(np.sum(N * np.logaddexp(0, -h)) / np.sum(N))
