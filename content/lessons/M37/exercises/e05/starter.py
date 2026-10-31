import math
import numpy as np


def noise(x0, t, rng):
    """Samples of x_t given samples of x_0."""
    raise NotImplementedError


def noised_params(w, m, s, t):
    """Mixture parameters at time t of the forward process."""
    raise NotImplementedError


def kl_to_standard_normal(m, v):
    """KL divergence of N(m, v) from N(0, 1)."""
    raise NotImplementedError
