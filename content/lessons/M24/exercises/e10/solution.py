import math


def upper_tail(x):
    """P(Z > x) for a standard normal Z."""
    return 0.5 * math.erfc(x / math.sqrt(2))


def second_moment(theta, a):
    """Second moment of the importance-sampling estimator with proposal N(theta, 1)."""
    return math.exp(theta * theta) * upper_tail(a + theta)


def d_second_moment(theta, a):
    """Derivative of second_moment with respect to theta."""
    phi = math.exp(-0.5 * (a + theta) ** 2) / math.sqrt(2 * math.pi)
    return 2 * theta * second_moment(theta, a) - math.exp(theta * theta) * phi


def best_shift(a):
    """Shift minimizing the second moment, by bisection on the derivative."""
    lo, hi = 0.0, 2.0 * a
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if d_second_moment(mid, a) < 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def relative_error(theta, a, n):
    """Relative standard error with n samples from N(theta, 1)."""
    p = upper_tail(a)
    return math.sqrt((second_moment(theta, a) / p**2 - 1) / n)
