import math
import numpy as np


# provided
def ar1_chains(runs, n, rho, rng):
    x = np.empty((runs, n))
    x[:, 0] = rng.standard_normal(runs)
    s = math.sqrt(1 - rho * rho)
    for t in range(1, n):
        x[:, t] = rho * x[:, t - 1] + s * rng.standard_normal(runs)
    return x


def naive_se(x):
    """Standard error assuming independent samples."""
    raise NotImplementedError


def batch_means_se(x, batches=50):
    """Standard error from the spread of block averages."""
    raise NotImplementedError


def inflation(rho):
    """True over naive standard error for an AR(1) chain."""
    raise NotImplementedError
