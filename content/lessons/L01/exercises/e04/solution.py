import numpy as np


def sigmoid(a):
    a = np.asarray(a, dtype=float)
    out = np.empty_like(a)
    pos = a >= 0
    out[pos] = 1.0 / (1.0 + np.exp(-a[pos]))
    e = np.exp(a[~pos])
    out[~pos] = e / (1.0 + e)
    return out


def logistic_loss(w, b, X, y):
    a = X @ w + b
    return float(np.mean(np.maximum(a, 0) - a * y + np.log1p(np.exp(-np.abs(a)))))


def logistic_grad(w, b, X, y):
    err = sigmoid(X @ w + b) - y
    return X.T @ err / X.shape[0], float(np.mean(err))
