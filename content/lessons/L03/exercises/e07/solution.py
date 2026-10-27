import numpy as np


def softmax(z):
    e = np.exp(z - np.max(z))
    return e / e.sum()


def softmax_jacobian(z):
    p = softmax(z)
    return np.diag(p) - np.outer(p, p)


def softmax_vjp(z, u):
    p = softmax(z)
    return p * (u - u @ p)
