import math


def upper_tail(x):
    """P(Z > x) for a standard normal Z."""
    raise NotImplementedError


def second_moment(theta, a):
    """Second moment of the importance-sampling estimator with proposal N(theta, 1)."""
    raise NotImplementedError


def d_second_moment(theta, a):
    """Derivative of second_moment with respect to theta."""
    raise NotImplementedError


def best_shift(a):
    """Shift minimizing the second moment, by bisection on the derivative."""
    raise NotImplementedError


def relative_error(theta, a, n):
    """Relative standard error with n samples from N(theta, 1)."""
    raise NotImplementedError
