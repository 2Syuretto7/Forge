import math

import numpy as np

# provided
PROBLEMS = [
    ("quartic plus quadratic", lambda x: x ** 4 + x * x - x, lambda x: 4 * x ** 3 + 2 * x - 1, lambda x: 12 * x * x + 2, 1.0, 0.385458498529624),
    ("exp minus linear", lambda x: math.exp(x) - 2 * x, lambda x: math.exp(x) - 2, math.exp, 2.0, math.log(2)),
    ("log cosh plus cubic", lambda x: math.log(math.cosh(x - 0.5)) + 0.1 * (x - 0.5) ** 3, lambda x: math.tanh(x - 0.5) + 0.3 * (x - 0.5) ** 2, lambda x: 1 - math.tanh(x - 0.5) ** 2 + 0.6 * (x - 0.5), 1.2, 0.5),
    ("cos plus polynomial", lambda x: math.cos(x) + 0.75 * x * x + 0.1 * x ** 3, lambda x: -math.sin(x) + 1.5 * x + 0.3 * x * x, lambda x: -math.cos(x) + 1.5 + 0.6 * x, 1.0, 0.0),
    ("softplus plus quadratic", lambda x: math.log1p(math.exp(x)) + 0.5 * x * x, lambda x: 1 / (1 + math.exp(-x)) + x, lambda x: 1 / (1 + math.exp(-x)) * (1 - 1 / (1 + math.exp(-x))) + 1, 2.0, -0.40105813754154707),
]


def _done(a, b):
    return abs(b - a) < 1e-15 * max(1.0, abs(b))


def gd_min(df, x0, eta, steps=300):
    """Gradient descent iterates."""
    xs = [float(x0)]
    for _ in range(steps):
        xs.append(xs[-1] - eta * df(xs[-1]))
        if _done(xs[-2], xs[-1]):
            break
    return xs


def secant_min(df, x0, x1, steps=60):
    """Secant method on f'."""
    xs = [float(x0), float(x1)]
    for _ in range(steps):
        a, b = xs[-2], xs[-1]
        ga, gb = df(a), df(b)
        if gb == ga:
            break
        xs.append(b - gb * (b - a) / (gb - ga))
        if _done(xs[-2], xs[-1]):
            break
    return xs


def newton_min(df, d2f, x0, steps=30):
    """Newton's method on f'."""
    xs = [float(x0)]
    for _ in range(steps):
        x = xs[-1]
        xs.append(x - df(x) / d2f(x))
        if _done(xs[-2], xs[-1]):
            break
    return xs


def _usable(errs):
    return [e for e in errs if 1e-13 < e < 0.3]


def measured_order(errs):
    """Median order estimate."""
    e = _usable(errs)
    p = [math.log(e[k + 1] / e[k]) / math.log(e[k] / e[k - 1]) for k in range(1, len(e) - 1)]
    return float(np.median(p))


def measured_rate(errs):
    """Median ratio of consecutive errors."""
    e = _usable(errs)
    return float(np.median([e[k + 1] / e[k] for k in range(len(e) - 1)]))


def report():
    """Measured orders and rates per problem."""
    out = []
    for name, f, df, d2f, x0, xs in PROBLEMS:
        eta = 0.5 / d2f(xs)
        err = lambda it: [abs(x - xs) for x in it]  # noqa: E731
        g = err(gd_min(df, x0, eta))
        out.append(
            {
                "name": name,
                "gd_order": measured_order(g),
                "gd_rate": measured_rate(g),
                "gd_predicted_rate": abs(1 - eta * d2f(xs)),
                "secant_order": measured_order(err(secant_min(df, x0, x0 + 0.1))),
                "newton_order": measured_order(err(newton_min(df, d2f, x0))),
            }
        )
    return out
