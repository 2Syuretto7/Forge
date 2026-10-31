import math
import numpy as np


def _log_resp(X, w, M, s):
    raise NotImplementedError


def mixture2d_logpdf(X, w, M, s):
    """Log density of an isotropic two-dimensional Gaussian mixture."""
    raise NotImplementedError


def mixture2d_score(X, w, M, s):
    """Gradient of the log density."""
    raise NotImplementedError


def noised_score(X, t, w, M, s):
    """Exact score of the noised mixture at time t."""
    raise NotImplementedError


def reverse_sample_2d(score, n, T, steps, rng, tmin=1e-3):
    """Reverse-time SDE in two dimensions."""
    raise NotImplementedError


def sliced_w1(X, Y, rng, n_proj=50):
    """Sliced Wasserstein-1 distance from matching quantiles."""
    raise NotImplementedError
