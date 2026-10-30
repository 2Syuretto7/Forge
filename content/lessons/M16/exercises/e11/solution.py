import math


def first_guess(a):
    """Cheap estimate of sqrt(a) from the floating-point exponent."""
    m, e = math.frexp(a)
    g = (0.41 + 0.59 * m) * 2.0 ** (e // 2)
    return g * math.sqrt(2) if e % 2 else g


def iterations_to_full_precision(a, x0, tol=4e-16):
    """Newton steps until the relative error of sqrt(a) is below tol."""
    r = math.sqrt(a)
    x, k = x0, 0
    while abs(x - r) > tol * r and k < 2000:
        x = 0.5 * (x + a / x)
        k += 1
    return k
