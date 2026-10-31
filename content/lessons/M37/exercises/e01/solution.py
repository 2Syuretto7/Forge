import math
import numpy as np


def brownian_paths(n_paths, T, steps, rng):
    """Brownian motion sampled at steps + 1 equally spaced times."""
    dW = rng.standard_normal((n_paths, steps)) * math.sqrt(T / steps)
    return np.concatenate([np.zeros((n_paths, 1)), np.cumsum(dW, axis=1)], axis=1)


def euler_maruyama(a, b, x0, T, steps, n_paths, rng):
    """Final values of Euler-Maruyama paths of dX = a dt + b dW."""
    h = T / steps
    x = np.full(n_paths, float(x0))
    for k in range(steps):
        t = k * h
        x = x + a(x, t) * h + b(x, t) * math.sqrt(h) * rng.standard_normal(n_paths)
    return x
