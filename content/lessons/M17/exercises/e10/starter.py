import math

import numpy as np


# provided
def adaptive_simpson(f, a, b, tol=1e-10, max_depth=50):
    count = [0]

    def F(x):
        count[0] += 1
        return f(x)

    def rec(a, b, fa, fm, fb, whole, tol, depth):
        m = (a + b) / 2
        lm, rm = (a + m) / 2, (m + b) / 2
        flm, frm = F(lm), F(rm)
        left = (m - a) / 6 * (fa + 4 * flm + fm)
        right = (b - m) / 6 * (fm + 4 * frm + fb)
        if depth >= max_depth or abs(left + right - whole) <= 15 * tol:
            return left + right + (left + right - whole) / 15
        return rec(a, m, fa, flm, fm, left, tol / 2, depth + 1) + rec(m, b, fm, frm, fb, right, tol / 2, depth + 1)

    fa, fm, fb = F(a), F((a + b) / 2), F(b)
    whole = (b - a) / 6 * (fa + 4 * fm + fb)
    return rec(a, b, fa, fm, fb, whole, tol, 0), count[0]


def _trap(f, a, b, n):
    raise NotImplementedError


def _simp(f, a, b, n):
    raise NotImplementedError


def exact(a, b):
    """Integral of exp(-a x) cos(b x) over [0, 1]."""
    raise NotImplementedError


def evals_doubling(rule, f, tol, exact_value):
    """Evaluations used by the first doubled grid that meets tol."""
    raise NotImplementedError


def survey(n_funcs=1000, seed=0):
    """Average evaluations: trapezoid, Simpson, adaptive Simpson."""
    raise NotImplementedError
