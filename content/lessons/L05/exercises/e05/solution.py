import numpy as np


def _sigmoid(a):
    return 0.5 * (1.0 + np.tanh(0.5 * a))


def fit_logistic(X, y, lr=0.5, steps=5000, l2=0.0):
    n, d = X.shape
    w = np.zeros(d)
    b = 0.0
    for _ in range(steps):
        err = _sigmoid(X @ w + b) - y
        w = w - lr * (X.T @ err / n + l2 * w)
        b = b - lr * np.mean(err)
    return w, b


def predict_proba(w, b, X):
    return _sigmoid(X @ w + b)


def accuracy(w, b, X, y):
    return float(np.mean((predict_proba(w, b, X) >= 0.5) == (y == 1)))
