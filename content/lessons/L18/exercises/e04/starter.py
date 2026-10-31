import numpy as np

rng = np.random.default_rng(3)
VOCAB, D = 12, 8
E = rng.normal(size=(VOCAB, D)) * 0.7
P = rng.normal(size=(32, D)) * 1.5
Wq, Wk, Wv, Wo = (rng.normal(size=(D, D)) / np.sqrt(D) for _ in range(4))


def softmax(z):
    e = np.exp(z - z.max(axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


def logits_full(ids):
    """A one-layer attention model: next-token logits at every position, recomputed from scratch."""
    x = E[ids] + P[: len(ids)]
    Q, K, V = x @ Wq, x @ Wk, x @ Wv
    T = len(ids)
    s = np.where(np.triu(np.ones((T, T), dtype=bool), 1), -np.inf, Q @ K.T / np.sqrt(D))
    h = x + softmax(s) @ V @ Wo
    return h @ E.T


def generate_uncached(prompt, n):
    """Greedy generation that recomputes the whole sequence at every step."""
    raise NotImplementedError


def generate_cached(prompt, n):
    """Greedy generation with a KV cache: process the prompt once, then each step computes q, k, v
    for the newest token only, appends k and v, and attends over the cache. Must return exactly
    what generate_uncached returns."""
    raise NotImplementedError
