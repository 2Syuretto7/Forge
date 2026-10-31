import numpy as np


def softmax_t(logits, T=1.0):
    z = logits / T
    z = z - z.max()
    e = np.exp(z)
    return e / e.sum()


def top_k_filter(logits, k):
    """Keep the k largest logits; set the rest to -inf."""
    if k >= len(logits):
        return logits.copy()
    cut = np.sort(logits)[-k]
    return np.where(logits >= cut, logits, -np.inf)


def top_p_filter(logits, p):
    """Keep the smallest set of tokens, taken in order of probability, whose total probability is at
    least p; set the rest to -inf."""
    probs = softmax_t(logits)
    order = np.argsort(-probs)
    keep = np.searchsorted(np.cumsum(probs[order]), p) + 1
    out = np.full_like(logits, -np.inf)
    out[order[:keep]] = logits[order[:keep]]
    return out


def sample(logits, rng, T=1.0, k=None, p=None):
    """Temperature first, then the filters, then draw one token."""
    z = logits / T
    if k is not None:
        z = top_k_filter(z, k)
    if p is not None:
        z = top_p_filter(z, p)
    return int(rng.choice(len(z), p=softmax_t(z)))
