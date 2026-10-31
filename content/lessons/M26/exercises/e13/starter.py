import numpy as np


def one_pass_var(x):
    """Mean of squares minus square of the mean, in the array's dtype."""
    raise NotImplementedError


def two_pass_var(x):
    """Mean squared deviation from the mean, computed in two passes."""
    raise NotImplementedError


def welford_var(x):
    """Welford's streaming variance."""
    raise NotImplementedError
