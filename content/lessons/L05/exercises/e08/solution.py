import numpy as np


def accuracy(P, y):
    return float(np.mean(P.argmax(axis=1) == y))


def log_loss(P, y):
    p = np.clip(P[np.arange(len(y)), y], 1e-15, 1.0)
    return float(-np.mean(np.log(p)))


def confusion_matrix(P, y, K):
    C = np.zeros((K, K), dtype=int)
    np.add.at(C, (y, P.argmax(axis=1)), 1)
    return C
