import math
import numpy as np


def features(x):
    """Basis functions for a one-dimensional score model."""
    raise NotImplementedError


def dsm_data(x0, t, rng):
    """Noised samples and their denoising score-matching targets."""
    raise NotImplementedError


def dsm_loss(c, X, target):
    """Mean squared error of the linear score model."""
    raise NotImplementedError


def grad_dsm_loss(c, X, target):
    """Gradient of dsm_loss in the coefficients."""
    raise NotImplementedError


def fit_score(X, target):
    """Least-squares coefficients."""
    raise NotImplementedError
