import numpy as np


def sae_loss(params, X, l1):
    """The loss and gradients of exercise 7."""
    We, be, Wd, bd = params
    n = len(X)
    U = X - bd
    pre = U @ We.T + be
    z = np.maximum(pre, 0)
    E = z @ Wd + bd - X
    dXh = 2 * E / n
    dz = dXh @ Wd.T + l1 / n
    dpre = dz * (pre > 0)
    grads = (dpre.T @ U, dpre.sum(axis=0), z.T @ dXh, dXh.sum(axis=0) - (dpre @ We).sum(axis=0))
    return float(np.sum(E ** 2) / n + l1 * np.sum(z) / n), grads


def make_activations(features, n, p, seed=0):
    """n samples, each a sum of feature rows active independently with probability p, with
    magnitudes uniform in [0, 1]."""
    rng = np.random.default_rng(seed)
    mask = rng.random((n, len(features))) < p
    return (mask * rng.random((n, len(features)))) @ features


def recovered(features, decoder, threshold=0.9):
    """How many true features have a decoder row with cosine above threshold."""
    F = features / np.linalg.norm(features, axis=1, keepdims=True)
    D = decoder / np.linalg.norm(decoder, axis=1, keepdims=True)
    return int(np.sum((F @ D.T).max(axis=1) > threshold))


def train_sae(X, m, l1, steps=1000, lr=0.01, seed=0, batch=256):
    """Adam on sae_loss over minibatches of `batch` rows. Initialize the decoder rows as random
    unit vectors (np.random.default_rng(seed)), the encoder as a copy of them, b_e at zero and b_d
    at the data mean; after every step rescale the decoder rows to unit length. Return the
    parameters (W_e, b_e, W_d, b_d)."""
    rng = np.random.default_rng(seed)
    d = X.shape[1]
    Wd = rng.normal(size=(m, d))
    Wd /= np.linalg.norm(Wd, axis=1, keepdims=True)
    params = [Wd.copy(), np.zeros(m), Wd.copy(), X.mean(axis=0)]
    M = [np.zeros_like(p) for p in params]
    V = [np.zeros_like(p) for p in params]
    for t in range(1, steps + 1):
        _, grads = sae_loss(params, X[rng.integers(0, len(X), batch)], l1)
        for i, g in enumerate(grads):
            M[i] = 0.9 * M[i] + 0.1 * g
            V[i] = 0.999 * V[i] + 0.001 * g * g
            params[i] = params[i] - lr * (M[i] / (1 - 0.9 ** t)) / (np.sqrt(V[i] / (1 - 0.999 ** t)) + 1e-8)
        params[2] = params[2] / np.linalg.norm(params[2], axis=1, keepdims=True)
    return tuple(params)
