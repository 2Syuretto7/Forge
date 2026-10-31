import numpy as np


def ols(X, y):
    return np.linalg.lstsq(X, y, rcond=None)[0]


def gaussian_nll(w, sigma, X, y):
    r = y - X @ w
    return float(0.5 * np.log(2 * np.pi * sigma ** 2) + np.mean(r ** 2) / (2 * sigma ** 2))


def noise_mle(X, y, w):
    r = y - X @ w
    return float(np.mean(r ** 2))
