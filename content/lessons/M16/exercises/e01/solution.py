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
    s, t = 0.0, x
    for k in range(1, terms + 1):
        s += t
        t *= -x * x / ((2 * k) * (2 * k + 1))
    return s


def taylor_exp(x, terms):
    """Sum of x^k / k! for k < terms."""
    s, t = 0.0, 1.0
    for k in range(terms):
        s += t
        t *= x / (k + 1)
    return s


def sin_bound(x, terms):
    """Size of the first omitted term."""
    n = 2 * terms + 1
    return abs(x) ** n / math.factorial(n)


def terms_for(x, tol):
    """Fewest terms with sin_bound below tol."""
    n = 1
    while sin_bound(x, n) >= tol:
        n += 1
    return n
