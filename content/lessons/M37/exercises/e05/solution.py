import math
import numpy as np


def noise(x0, t, rng):
    """Samples of x_t given samples of x_0."""
    a = math.exp(-t)
    x0 = np.asarray(x0, dtype=float)
    return a * x0 + math.sqrt(1 - a * a) * rng.standard_normal(x0.shape)


def noised_params(w, m, s, t):
    """Mixture parameters at time t of the forward process."""
    a = math.exp(-t)
    return np.asarray(w), np.asarray(m) * a, np.sqrt(np.asarray(s) ** 2 * a * a + 1 - a * a)


def kl_to_standard_normal(m, v):
    """KL divergence of N(m, v) from N(0, 1)."""
    return 0.5 * (v + m * m - 1 - math.log(v))
