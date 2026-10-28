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


def control_labels(word_ids, seed=0):
    """A control task (Hewitt and Liang, 2019): give every word type a random binary label, so the
    labels carry no linguistic property but are consistent per word."""
    rng = np.random.default_rng(seed)
    types = np.unique(word_ids)
    table = dict(zip(types.tolist(), rng.integers(0, 2, len(types)).tolist()))
    return np.array([table[int(w)] for w in word_ids], dtype=float)


def selectivity(A_tr, y_tr, A_te, y_te, c_tr, c_te):
    """Held-out probe accuracy on the real labels minus held-out accuracy on the control labels."""
    w, b = train_probe(A_tr, y_tr)
    wc, bc = train_probe(A_tr, c_tr)
    return probe_accuracy(w, b, A_te, y_te) - probe_accuracy(wc, bc, A_te, c_te)
