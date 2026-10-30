import numpy as np


def midpoint_errors(ns):
    """Midpoint-rule errors for x^(-1/2) on [0, 1]."""
    out = []
    for n in ns:
        x = (np.arange(n) + 0.5) / n
        out.append(abs(np.sum(x ** -0.5) / n - 2))
    return np.array(out)


def fitted_order(ns, errs):
    """Least-squares slope of -log(error) against log n."""
    return float(np.polyfit(np.log(ns), -np.log(errs), 1)[0])


def after_substitution(n):
    """Simpson error on the substituted, constant integrand."""
    t = np.linspace(0, 1, n + 1)
    w = np.ones(n + 1)
    w[1:-1:2] = 4
    w[2:-1:2] = 2
    return abs(float(np.sum(w * np.full_like(t, 2.0)) / n / 3) - 2)
