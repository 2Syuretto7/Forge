import numpy as np


def log_softmax(z):
    """Stable log-softmax."""
    m = np.max(z)
    return z - m - np.log(np.sum(np.exp(z - m)))


def _h(z, ref_logp, beta):
    d = log_softmax(np.asarray(z, dtype=float)) - np.asarray(ref_logp)
    return beta * (d[:, None] - d[None, :])


def dpo_loss(z, ref_logp, N, beta):
    """Mean DPO loss over the comparisons counted in N."""
    return float(np.sum(N * np.logaddexp(0, -_h(z, ref_logp, beta))) / np.sum(N))


def grad_dpo_loss(z, ref_logp, N, beta):
    """Gradient of the DPO loss in the logits."""
    s = N / (1 + np.exp(_h(z, ref_logp, beta)))
    return -beta * (s.sum(axis=1) - s.sum(axis=0)) / np.sum(N)
