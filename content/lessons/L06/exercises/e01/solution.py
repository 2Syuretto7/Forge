import numpy as np


def design(x, degree):
    return np.vander(np.asarray(x, dtype=float), degree + 1, increasing=True)


def fit_poly(x, y, degree):
    return np.linalg.lstsq(design(x, degree), y, rcond=None)[0]


def predict(coef, x):
    return design(x, len(coef) - 1) @ coef


def mse(yhat, y):
    return float(np.mean((np.asarray(yhat) - np.asarray(y)) ** 2))
