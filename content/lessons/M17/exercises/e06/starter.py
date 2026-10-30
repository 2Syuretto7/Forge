import math


def _simpson(f, a, b, n):
    raise NotImplementedError


def normalizer(g, a, b, n=2000):
    """Total area of g on [a, b]."""
    raise NotImplementedError


def make_pdf(g, a, b):
    """g divided by its total area."""
    raise NotImplementedError


def make_cdf(g, a, b, n=2000):
    """Cumulative probability from a to x."""
    raise NotImplementedError


def beta_normalizer(alpha, beta):
    """B(alpha, beta)."""
    raise NotImplementedError
