import math
import numpy as np


def sgd_chains(a, s, eta, steps, chains, rng):
    """Final positions of parallel constant-step SGD chains on a x^2 / 2."""
    raise NotImplementedError


def sgd_stationary_var(a, s, eta):
    """Stationary variance of constant-step SGD on a quadratic."""
    raise NotImplementedError


def ula_chains(grad_log_p, x0, h, steps, rng):
    """Parallel unadjusted Langevin chains."""
    raise NotImplementedError


def ula_stationary_var(sigma2, h):
    """Stationary variance of ULA on N(0, sigma2)."""
    raise NotImplementedError
