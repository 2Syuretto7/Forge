import math
import numpy as np


def normal_interval(values, z=1.96):
    """CLT interval for the mean."""
    raise NotImplementedError


def coverage(draw, true_mean, n, runs, rng):
    """Fraction of runs whose interval contains the true mean."""
    raise NotImplementedError


def n_for_halfwidth(sigma, h, z=1.96):
    """Samples needed for a halfwidth of h."""
    raise NotImplementedError
