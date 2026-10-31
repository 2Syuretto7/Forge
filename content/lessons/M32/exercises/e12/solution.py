import math
import numpy as np


def sgd_chains(a, s, eta, steps, chains, rng):
    """Final positions of parallel constant-step SGD chains on a x^2 / 2."""
    x = np.zeros(chains)
    for _ in range(steps):
        x = x - eta * (a * x + s * rng.standard_normal(chains))
    return x


def sgd_stationary_var(a, s, eta):
    """Stationary variance of constant-step SGD on a quadratic."""
    if eta * a >= 2:
        return math.inf
    return eta * s * s / (a * (2 - eta * a))


def ula_chains(grad_log_p, x0, h, steps, rng):
    """Parallel unadjusted Langevin chains."""
    x = np.array(x0, dtype=float)
    c = math.sqrt(2 * h)
    for _ in range(steps):
        x = x + h * grad_log_p(x) + c * rng.standard_normal(x.shape)
    return x


def ula_stationary_var(sigma2, h):
    """Stationary variance of ULA on N(0, sigma2)."""
    return sigma2 / (1 - h / (2 * sigma2))
