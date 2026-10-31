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


def generate_cached_buggy(prompt, n):
    """A cached generator with an off-by-one: new tokens get the position of the previous one."""
    ids = list(prompt)
    Ks, Vs = [], []
    for t, tok in enumerate(ids):
        x = E[tok] + P[t]
        Ks.append(x @ Wk)
        Vs.append(x @ Wv)
        h = x + (softmax(np.array(Ks) @ (x @ Wq) / np.sqrt(D)) @ np.array(Vs)) @ Wo
    for _ in range(n):
        ids.append(int((h @ E.T).argmax()))
        x = E[ids[-1]] + P[len(ids) - 2]
        Ks.append(x @ Wk)
        Vs.append(x @ Wv)
        h = x + (softmax(np.array(Ks) @ (x @ Wq) / np.sqrt(D)) @ np.array(Vs)) @ Wo
    return ids


def first_divergence(prompt, n, generator):
    """Compare `generator`'s greedy continuation with full recomputation, step by step: return the
    index (within the n new tokens) of the first token where they differ, or None. The reference
    for each step is logits_full on the generator's own sequence so far."""
    ids = generator(prompt, n)
    for i in range(n):
        prefix = ids[: len(prompt) + i]
        if int(logits_full(prefix)[-1].argmax()) != ids[len(prompt) + i]:
            return i
    return None
