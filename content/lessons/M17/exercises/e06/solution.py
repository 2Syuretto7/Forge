import math


def _simpson(f, a, b, n):
    h = (b - a) / n
    return h / 3 * sum((1 if k in (0, n) else 4 if k % 2 else 2) * f(a + k * h) for k in range(n + 1))


def normalizer(g, a, b, n=2000):
    """Total area of g on [a, b]."""
    return _simpson(g, a, b, n)


def make_pdf(g, a, b):
    """g divided by its total area."""
    Z = normalizer(g, a, b)
    return lambda x: g(x) / Z


def make_cdf(g, a, b, n=2000):
    """Cumulative probability from a to x."""
    Z = normalizer(g, a, b, n)
    return lambda x: _simpson(g, a, x, n) / Z


def beta_normalizer(alpha, beta):
    """B(alpha, beta)."""
    return math.gamma(alpha) * math.gamma(beta) / math.gamma(alpha + beta)
