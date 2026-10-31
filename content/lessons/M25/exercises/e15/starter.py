import math
import numpy as np


# provided
def ar1(n, rho, rng):
    e = rng.standard_normal(n)
    x = np.empty(n)
    x[0] = e[0]
    s = math.sqrt(1 - rho * rho)
    for t in range(1, n):
        x[t] = rho * x[t - 1] + s * e[t]
    return x


def iid_bootstrap_se(x, B, rng):
    """Bootstrap standard error of the mean, resampling single points."""
    raise NotImplementedError


def block_bootstrap_se(x, block, B, rng):
    """Bootstrap standard error of the mean, resampling blocks."""
    raise NotImplementedError
