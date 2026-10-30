import math

import numpy as np


def ball_volume(n):
    """Volume of the unit ball in n dimensions."""
    return math.pi ** (n / 2) / math.gamma(n / 2 + 1)


def cube_fraction(n):
    """V_n / 2^n."""
    return ball_volume(n) / 2 ** n


def mc_fraction(n, samples, seed=0):
    """(fraction inside, standard error) by sampling the cube."""
    X = np.random.default_rng(seed).uniform(-1, 1, size=(samples, n))
    p = float(np.mean(np.sum(X * X, axis=1) <= 1))
    return p, math.sqrt(max(p * (1 - p), 1e-300) / samples)


def peak_dimension(max_n=50):
    """Dimension of largest volume."""
    return max(range(1, max_n + 1), key=ball_volume)
