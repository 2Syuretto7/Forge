import numpy as np


def softmax_ce_forward(Z, y):
    Zs = Z - Z.max(axis=1, keepdims=True)
    logp = Zs - np.log(np.exp(Zs).sum(axis=1, keepdims=True))
    B = Z.shape[0]
    loss = -np.mean(logp[np.arange(B), y])
    return float(loss), (np.exp(logp), y)


def softmax_ce_backward(cache):
    P, y = cache
    B = P.shape[0]
    d = P.copy()
    d[np.arange(B), y] -= 1.0
    return d / B
