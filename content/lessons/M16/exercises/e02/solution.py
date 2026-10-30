import math


def bisect(f, a, b, tol=1e-12, max_iter=200):
    """(root, iterations) by halving a sign-changing bracket."""
    fa = f(a)
    if (fa < 0) == (f(b) < 0):
        raise ValueError("f(a) and f(b) must have opposite signs")
    k = 0
    while b - a >= tol and k < max_iter:
        m = (a + b) / 2
        fm = f(m)
        if fm == 0:
            return m, k + 1
        if (fa < 0) != (fm < 0):
            b = m
        else:
            a, fa = m, fm
        k += 1
    return (a + b) / 2, k


def predicted_iterations(a, b, tol):
    """ceil(log2((b - a) / tol))."""
    return math.ceil(math.log2((b - a) / tol))
