import time
import numpy as np


# provided
def make_data(n=10**6, d=8, seed=0):
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n, d))
    w = np.linspace(-1, 1, d)
    y = (rng.random(n) < 1 / (1 + np.exp(-X @ w))).astype(float)
    return X, y


# provided
TRUE_W = np.linspace(-1, 1, 8)


def _sig(z):
    e = np.exp(-np.abs(z))
    return np.where(z >= 0, 1 / (1 + e), e / (1 + e))


def minibatch_grad(w, Xb, yb):
    """Logistic gradient on a batch."""
    return Xb.T @ (_sig(Xb @ w) - yb) / len(yb)


def full_loss(w, X, y, chunk=100000):
    """Average logistic loss, chunk by chunk."""
    total = 0.0
    for i in range(0, len(y), chunk):
        z = X[i:i + chunk] @ w
        total += float(np.sum(np.maximum(z, 0) + np.log1p(np.exp(-np.abs(z))) - y[i:i + chunk] * z))
    return total / len(y)


def train(X, y, method, epochs=2, batch=1000, lr=0.1, seed=0):
    """(weights, seconds) after training with the given optimizer."""
    rng = np.random.default_rng(seed)
    n, d = X.shape
    w = np.zeros(d)
    vel = np.zeros(d)
    m, v = np.zeros(d), np.zeros(d)
    t = 0
    start = time.perf_counter()
    for _ in range(epochs):
        order = rng.permutation(n)
        for i in range(0, n, batch):
            idx = order[i:i + batch]
            g = minibatch_grad(w, X[idx], y[idx])
            t += 1
            if method == "sgd":
                w = w - lr * g
            elif method == "momentum":
                vel = 0.9 * vel - lr * 0.1 * g
                w = w + vel
            else:
                m = 0.9 * m + 0.1 * g
                v = 0.999 * v + 0.001 * g * g
                w = w - (lr / 10) * (m / (1 - 0.9**t)) / (np.sqrt(v / (1 - 0.999**t)) + 1e-8)
    return w, time.perf_counter() - start
