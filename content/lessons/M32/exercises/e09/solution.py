import math
import numpy as np


def scaled_walk(n, T, paths, rng):
    """Random walks with n steps per unit time, scaled by 1/sqrt(n)."""
    steps = rng.choice([-1.0, 1.0], size=(paths, n * T))
    W = np.concatenate([np.zeros((paths, 1)), np.cumsum(steps, axis=1)], axis=1) / math.sqrt(n)
    return np.arange(n * T + 1) / n, W


def heat_kernel(x, t):
    """The N(0, t) density."""
    return np.exp(-np.asarray(x) ** 2 / (2 * t)) / math.sqrt(2 * math.pi * t)


def d_heat_dx(x, t):
    """d/dx of the heat kernel."""
    return -np.asarray(x) / t * heat_kernel(x, t)


def d2_heat_dx2(x, t):
    """d^2/dx^2 of the heat kernel."""
    x = np.asarray(x)
    return (x * x / t**2 - 1 / t) * heat_kernel(x, t)


def d_heat_dt(x, t):
    """d/dt of the heat kernel."""
    x = np.asarray(x)
    return (x * x / (2 * t * t) - 1 / (2 * t)) * heat_kernel(x, t)
