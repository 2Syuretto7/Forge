import numpy as np


def softmax(z):
    e = np.exp(z - np.max(z, axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


def kl_optimum(ref, reward, beta):
    """The maximizer of E[r] - beta KL(pi || ref): pi proportional to ref exp(r / beta)."""
    raise NotImplementedError


def tradeoff(ref, proxy, truth, betas):
    """For each beta, optimize the proxy reward and report (KL to ref, expected proxy, expected true
    reward) of the optimum."""
    raise NotImplementedError
