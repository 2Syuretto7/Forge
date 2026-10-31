import math
import numpy as np


def log_gauss(x, scales):
    """Log density of independent normals with the given scales, up to a constant."""
    raise NotImplementedError


def grad_log_gauss(x, scales):
    """Gradient of log_gauss."""
    raise NotImplementedError


def mala_chain(log_p, grad_log_p, x0, h, n, rng):
    """Metropolis-adjusted Langevin: (samples, acceptance)."""
    raise NotImplementedError


def tune_mala(log_p, grad_log_p, x0, rng, h=0.01, target=0.574, rounds=30, per_round=200):
    """Adapt the Langevin step toward a target acceptance rate."""
    raise NotImplementedError
