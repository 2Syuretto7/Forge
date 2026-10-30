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
    x = np.linspace(a, b, n + 1)
    y = f(x)
    return (b - a) / n * (y.sum() - (y[0] + y[-1]) / 2)


def _simp(f, a, b, n):
    x = np.linspace(a, b, n + 1)
    w = np.ones(n + 1)
    w[1:-1:2] = 4
    w[2:-1:2] = 2
    return (b - a) / n / 3 * np.sum(w * f(x))


def exact(a, b):
    """Integral of exp(-a x) cos(b x) over [0, 1]."""
    return (a - math.exp(-a) * (a * math.cos(b) - b * math.sin(b))) / (a * a + b * b)


def evals_doubling(rule, f, tol, exact_value):
    """Evaluations used by the first doubled grid that meets tol."""
    n = 2
    while abs(rule(f, 0.0, 1.0, n) - exact_value) >= tol:
        n *= 2
    return n + 1


def survey(n_funcs=1000, seed=0):
    """Average evaluations: trapezoid, Simpson, adaptive Simpson."""
    rng = np.random.default_rng(seed)
    t = s = ad = 0
    for _ in range(n_funcs):
        a, b = rng.uniform(0, 5), rng.uniform(0, 30)
        f = lambda x, a=a, b=b: np.exp(-a * x) * np.cos(b * x)  # noqa: E731
        ex = exact(a, b)
        t += evals_doubling(_trap, f, 1e-8, ex)
        s += evals_doubling(_simp, f, 1e-8, ex)
        g = lambda x, a=a, b=b: math.exp(-a * x) * math.cos(b * x)  # noqa: E731
        v, n = adaptive_simpson(g, 0.0, 1.0, 1e-9)
        assert abs(v - ex) < 1e-8
        ad += n
    return t / n_funcs, s / n_funcs, ad / n_funcs
