import math
import numpy as np


def features(x):
    """Basis functions for a one-dimensional score model."""
    x = np.asarray(x, dtype=float)
    return np.stack([np.ones_like(x), x, x**3, np.tanh(x - 1.5), np.tanh(x + 2), np.tanh(2 * (x - 1.5)), np.tanh(2 * (x + 2))], axis=1)


def dsm_data(x0, t, rng):
    """Noised samples and their denoising score-matching targets."""
    a = math.exp(-t)
    sigma = math.sqrt(1 - a * a)
    eps = rng.standard_normal(np.shape(x0))
    return a * np.asarray(x0) + sigma * eps, -eps / sigma


def dsm_loss(c, X, target):
    """Mean squared error of the linear score model."""
    r = features(X) @ c - target
    return float(np.mean(r * r))


def grad_dsm_loss(c, X, target):
    """Gradient of dsm_loss in the coefficients."""
    F = features(X)
    return 2 * F.T @ (F @ c - target) / len(target)


def fit_score(X, target):
    """Least-squares coefficients."""
    return np.linalg.lstsq(features(X), target, rcond=None)[0]
