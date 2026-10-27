import numpy as np


def init_mlp(sizes, seed=0):
    rng = np.random.default_rng(seed)
    params = {}
    for i, (a, b) in enumerate(zip(sizes, sizes[1:]), start=1):
        params[f"W{i}"] = rng.normal(size=(a, b)) * np.sqrt(2.0 / a)
        params[f"b{i}"] = np.zeros(b)
    return params


def _forward(params, X, act):
    L = len(params) // 2
    h = X
    cache = []
    for i in range(1, L + 1):
        z = h @ params[f"W{i}"] + params[f"b{i}"]
        cache.append((h, z))
        if i < L:
            h = np.maximum(z, 0) if act == "relu" else np.tanh(z)
        else:
            h = z
    return h, cache


def loss_and_grads(params, X, y, act="relu"):
    Z, cache = _forward(params, X, act)
    L = len(params) // 2
    B = X.shape[0]
    Zs = Z - Z.max(axis=1, keepdims=True)
    logp = Zs - np.log(np.exp(Zs).sum(axis=1, keepdims=True))
    loss = -np.mean(logp[np.arange(B), y])
    G = np.exp(logp)
    G[np.arange(B), y] -= 1.0
    G /= B
    grads = {}
    for i in range(L, 0, -1):
        h, z = cache[i - 1]
        if i < L:
            G = G * (z > 0) if act == "relu" else G * (1 - np.tanh(z) ** 2)
        grads[f"W{i}"] = h.T @ G
        grads[f"b{i}"] = G.sum(axis=0)
        G = G @ params[f"W{i}"].T
    return float(loss), grads


def predict(params, X, act="relu"):
    return _forward(params, X, act)[0].argmax(axis=1)
