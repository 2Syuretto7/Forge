import numpy as np


def symmetric_init(sizes, value=0.1):
    p = {}
    for i, (a, b) in enumerate(zip(sizes, sizes[1:]), start=1):
        p[f"W{i}"] = np.full((a, b), float(value))
        p[f"b{i}"] = np.zeros(b)
    return p


def unit_spread(W1):
    return float(np.max(np.max(W1, axis=1) - np.min(W1, axis=1)))


def _loss_grads(p, X, y):
    L = len(p) // 2
    h, cache = X, []
    for i in range(1, L + 1):
        z = h @ p[f"W{i}"] + p[f"b{i}"]
        cache.append((h, z))
        h = np.tanh(z) if i < L else z
    B = X.shape[0]
    Zs = h - h.max(axis=1, keepdims=True)
    logp = Zs - np.log(np.exp(Zs).sum(axis=1, keepdims=True))
    loss = -np.mean(logp[np.arange(B), y])
    G = np.exp(logp)
    G[np.arange(B), y] -= 1
    G /= B
    g = {}
    for i in range(L, 0, -1):
        hin, z = cache[i - 1]
        if i < L:
            G = G * (1 - np.tanh(z) ** 2)
        g[f"W{i}"] = hin.T @ G
        g[f"b{i}"] = G.sum(axis=0)
        G = G @ p[f"W{i}"].T
    return float(loss), g


def train_full_batch(params, X, y, lr=0.5, steps=2000):
    loss = None
    for _ in range(steps):
        loss, g = _loss_grads(params, X, y)
        for k in params:
            params[k] -= lr * g[k]
    return _loss_grads(params, X, y)[0]
