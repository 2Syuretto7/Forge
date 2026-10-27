import numpy as np


def _log_softmax(z):
    m = np.max(z)
    return z - (m + np.log(np.sum(np.exp(z - m))))


def empirical(data, K):
    return np.bincount(np.asarray(data), minlength=K) / len(data)


def avg_nll(z, data):
    return float(-np.mean(_log_softmax(np.asarray(z, dtype=float))[np.asarray(data)]))


def grad_avg_nll(z, data, K):
    return np.exp(_log_softmax(np.asarray(z, dtype=float))) - empirical(data, K)


def fit(data, K, steps=2000, lr=1.0):
    z = np.zeros(K)
    for _ in range(steps):
        z = z - lr * grad_avg_nll(z, data, K)
    return np.exp(_log_softmax(z))
