import numpy as np


def soften(logits, T):
    """softmax(logits / T)."""
    z = np.asarray(logits, dtype=float) / T
    e = np.exp(z - z.max())
    return e / e.sum()


def entropy(p):
    p = np.asarray(p)
    return float(-np.sum(p[p > 0] * np.log(p[p > 0])))


def topk_teacher(p, k):
    """Keep the teacher's k largest probabilities and renormalize them (storing the teacher's full
    distribution for every token of a corpus costs vocabulary-size numbers per token)."""
    p = np.asarray(p, dtype=float)
    keep = np.argsort(p)[-k:]
    q = np.zeros_like(p)
    q[keep] = p[keep]
    return q / q.sum()
