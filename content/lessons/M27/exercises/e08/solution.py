import numpy as np


def plugin_entropy(samples, K):
    c = np.bincount(np.asarray(samples), minlength=K)
    p = c[c > 0] / c.sum()
    return float(-np.sum(p * np.log(p)))


def miller_madow(samples, K):
    c = np.bincount(np.asarray(samples), minlength=K)
    return plugin_entropy(samples, K) + (np.count_nonzero(c) - 1) / (2 * c.sum())


def average_estimates(p, n, trials, seed=0):
    S = np.random.default_rng(seed).choice(len(p), size=(trials, n), p=p)
    K = len(p)
    a = np.mean([plugin_entropy(s, K) for s in S])
    b = np.mean([miller_madow(s, K) for s in S])
    return float(a), float(b)
