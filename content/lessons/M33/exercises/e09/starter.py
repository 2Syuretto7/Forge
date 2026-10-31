import math
import numpy as np


def sketch(A, b, s, rng):
    """Gaussian sketch of A and b with s rows."""
    raise NotImplementedError


def sketched_lstsq(A, b, s, rng):
    """Least squares on the sketched problem."""
    raise NotImplementedError


def residual_ratio(A, b, x):
    """Residual of x relative to the optimal residual."""
    raise NotImplementedError


def predicted_ratio(n, s):
    """Typical residual ratio of a Gaussian sketch."""
    raise NotImplementedError
