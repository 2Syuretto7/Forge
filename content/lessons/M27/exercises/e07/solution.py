import numpy as np


def logsumexp(Z):
    Z = np.asarray(Z, dtype=float)
    m = Z.max(axis=1, keepdims=True)
    return m[:, 0] + np.log(np.sum(np.exp(Z - m), axis=1))


def cross_entropy(Z, y):
    Z = np.asarray(Z, dtype=float)
    B = Z.shape[0]
    return float(np.mean(logsumexp(Z) - Z[np.arange(B), y]))


def cross_entropy_grad(Z, y):
    Z = np.asarray(Z, dtype=float)
    B = Z.shape[0]
    P = np.exp(Z - logsumexp(Z)[:, None])
    P[np.arange(B), y] -= 1.0
    return P / B
