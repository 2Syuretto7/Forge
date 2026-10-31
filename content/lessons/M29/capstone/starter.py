import math
import numpy as np


def _run(lam, x0, iters, alpha, beta, look_ahead):
    raise NotImplementedError


def gd(lam, x0, iters):
    """Gradient descent with the best fixed step."""
    raise NotImplementedError


def heavy_ball(lam, x0, iters):
    """Heavy ball with optimal constants."""
    raise NotImplementedError


def nesterov(lam, x0, iters):
    """Nesterov with step 1/L and constant momentum."""
    raise NotImplementedError


def proved_rate(method, kappa):
    """Per-step rate guaranteed on a quadratic."""
    raise NotImplementedError


def measured_rate(errors, start, stop):
    """Rate from a log-linear fit over range(start, stop)."""
    raise NotImplementedError


def sgd_inverse_time(mu, sigma, eta0, k0, iters, chains, rng):
    """Mean squared error of SGD with an inverse-time step, after every step."""
    raise NotImplementedError


def bias_correction(b1, b2, t):
    """Correction factors of Adam's moments at step t."""
    raise NotImplementedError


def uncorrected_mean(b1, t):
    """E[m_t] / E[g] for a stationary gradient."""
    raise NotImplementedError
