import numpy as np


def log_softmax(logits):
    """logits - logsumexp(logits), with the max shift."""
    m = logits.max()
    return logits - (m + np.log(np.exp(logits - m).sum()))


def cross_entropy(logits, target):
    """Minus the log-softmax of the target."""
    return float(-log_softmax(logits)[target])


def uniform_loss(V):
    """ln V."""
    return float(np.log(V))


def random_init_loss(V, scale, seed=0):
    """Mean cross-entropy over 100 random targets with logits scale * N(0, 1)."""
    rng = np.random.default_rng(seed)
    losses = []
    for _ in range(100):
        logits = rng.normal(size=V) * scale
        losses.append(cross_entropy(logits, int(rng.integers(V))))
    return float(np.mean(losses))
