import math
import numpy as np


def brownian_paths(n_paths, T, steps, rng):
    """Brownian motion sampled at steps + 1 equally spaced times."""
    raise NotImplementedError


def euler_maruyama(a, b, x0, T, steps, n_paths, rng):
    """Final values of Euler-Maruyama paths of dX = a dt + b dW."""
    raise NotImplementedError
