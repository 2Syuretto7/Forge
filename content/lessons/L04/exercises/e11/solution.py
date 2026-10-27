import numpy as np


def naive_softmax(z):
    e = np.exp(z)
    return e / np.sum(e)


def naive_logprob(z, y):
    return np.log(naive_softmax(z)[y])


def stable_logprob(z, y):
    m = np.max(z)
    return z[y] - (m + np.log(np.sum(np.exp(z - m))))
