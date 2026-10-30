import numpy as np


def poly_eval(c, x):
    """Horner's rule."""
    s = 0.0
    for ck in reversed(c):
        s = s * x + ck
    return s


def poly_deriv(c):
    """Coefficients of the derivative."""
    return [k * c[k] for k in range(1, len(c))] or [0.0]


def critical_points(c):
    """Sorted real roots of the derivative."""
    d = poly_deriv(c)
    if len(d) < 2:
        return []
    r = np.roots(d[::-1])
    return sorted(float(z.real) for z in r if abs(z.imag) < 1e-9)


def classify(c, x):
    """min, max or flat by the second derivative."""
    s = poly_eval(poly_deriv(poly_deriv(c)), x)
    if abs(s) < 1e-9:
        return "flat"
    return "min" if s > 0 else "max"
