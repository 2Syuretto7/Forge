import numpy as np


def _simp(f, a, b, n):
    x = np.linspace(a, b, n + 1)
    w = np.ones(n + 1)
    w[1:-1:2] = 4
    w[2:-1:2] = 2
    return float((b - a) / n / 3 * np.sum(w * f(x)))


def simpson_step_errors(ns):
    """Simpson errors for the step at 1/3."""
    H = lambda x: (x > 1 / 3).astype(float)  # noqa: E731
    return np.array([abs(_simp(H, 0.0, 1.0, n) - 2 / 3) for n in ns])


def fitted_order(ns, errs):
    """Least-squares slope of -log(error) against log n."""
    return float(np.polyfit(np.log(ns), -np.log(errs), 1)[0])


def split_at_jump(n):
    """Error after splitting at the jump."""
    a = _simp(lambda x: np.zeros_like(x), 0.0, 1 / 3, n)
    b = _simp(lambda x: np.ones_like(x), 1 / 3, 1.0, n)
    return abs(a + b - 2 / 3)
