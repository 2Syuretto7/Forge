import numpy as np


def linear_forward(X, W, b):
    return X @ W + b, (X, W)


def linear_backward(dY, cache):
    X, W = cache
    return dY @ W.T, X.T @ dY, dY.sum(axis=0)
