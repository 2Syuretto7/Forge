import numpy as np


def kl_gauss(mu1, s1, mu2, s2):
    return float(np.log(s2 / s1) + (s1 ** 2 + (mu1 - mu2) ** 2) / (2 * s2 ** 2) - 0.5)


def _logpdf(x, mu, s):
    return -0.5 * np.log(2 * np.pi * s * s) - (x - mu) ** 2 / (2 * s * s)


def kl_gauss_mc(mu1, s1, mu2, s2, n=200000, seed=0):
    x = np.random.default_rng(seed).normal(mu1, s1, size=n)
    return float(np.mean(_logpdf(x, mu1, s1) - _logpdf(x, mu2, s2)))


def grad_kl_mu1(mu1, s1, mu2, s2):
    return (mu1 - mu2) / s2 ** 2
