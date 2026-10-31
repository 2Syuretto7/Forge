import numpy as np


def softmax(z):
    e = np.exp(z - np.max(z, axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


def kl_optimum(ref, reward, beta):
    """The maximizer of E[r] - beta KL(pi || ref): pi proportional to ref exp(r / beta)."""
    return softmax(np.log(np.asarray(ref, dtype=float)) + np.asarray(reward, dtype=float) / beta)


def tradeoff(ref, proxy, truth, betas):
    """For each beta, optimize the proxy reward and report (KL to ref, expected proxy, expected true
    reward) of the optimum."""
    out = []
    for b in betas:
        pi = kl_optimum(ref, proxy, b)
        kl = float(np.sum(pi * np.log(pi / np.asarray(ref))))
        out.append((kl, float(pi @ np.asarray(proxy)), float(pi @ np.asarray(truth))))
    return out
