import numpy as np


def train_probe(A, y, steps=300, lr=1.0, l2=1e-3):
    """A logistic-regression probe (the solution of exercise 4)."""
    w, b = np.zeros(A.shape[1]), 0.0
    for _ in range(steps):
        p = 1 / (1 + np.exp(-(A @ w + b)))
        g = (p - y) / len(y)
        w -= lr * (A.T @ g + l2 * w)
        b -= lr * g.sum()
    return w, b


def probe_accuracy(w, b, A, y):
    return float(np.mean(((A @ w + b) > 0) == (y == 1)))


def random_feature_probe(n_train, n_test, d, seed=0):
    """Labels that are pure noise and features that are pure noise: train a probe on n_train rows of
    d random features with random labels, and return (train accuracy, test accuracy on n_test new
    rows)."""
    rng = np.random.default_rng(seed)
    A, y = rng.normal(size=(n_train, d)), rng.integers(0, 2, n_train).astype(float)
    At, yt = rng.normal(size=(n_test, d)), rng.integers(0, 2, n_test).astype(float)
    w, b = train_probe(A, y, steps=2000, l2=0.0)
    return probe_accuracy(w, b, A, y), probe_accuracy(w, b, At, yt)
