import math


# provided
def taylor_cos(x, terms):
    s, t = 0.0, 1.0
    for k in range(terms):
        s += t
        t *= -x * x / ((2 * k + 1) * (2 * k + 2))
    return s


def taylor_sin(x, terms):
    """First `terms` nonzero terms of the sine series."""
    raise NotImplementedError


def taylor_exp(x, terms):
    """Sum of x^k / k! for k < terms."""
    raise NotImplementedError


def sin_bound(x, terms):
    """Size of the first omitted term."""
    raise NotImplementedError


def terms_for(x, tol):
    """Fewest terms with sin_bound below tol."""
    raise NotImplementedError
