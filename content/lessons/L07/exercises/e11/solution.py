import numpy as np


def dead_fraction(W1, b1, X):
    active = (X @ W1 + b1) > 0
    return float(np.mean(~active.any(axis=0)))


def first_layer_grads(params, X, y):
    z1 = X @ params["W1"] + params["b1"]
    h1 = np.maximum(z1, 0)
    Z = h1 @ params["W2"] + params["b2"]
    B = X.shape[0]
    Zs = Z - Z.max(axis=1, keepdims=True)
    P = np.exp(Zs)
    P /= P.sum(axis=1, keepdims=True)
    G = P
    G[np.arange(B), y] -= 1
    G /= B
    G1 = (G @ params["W2"].T) * (z1 > 0)
    return X.T @ G1, G1.sum(axis=0)
