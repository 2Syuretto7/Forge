import math


def exact_tail(n, p, eps):
    """P(|K/n - p| >= eps) for K ~ Binomial(n, p)."""
    raise NotImplementedError


def chebyshev(n, p, eps):
    """Chebyshev's bound."""
    raise NotImplementedError


def hoeffding(n, eps):
    """Hoeffding's bound."""
    raise NotImplementedError


def ratio_table(n, p, eps):
    """The exact tail and both bounds."""
    raise NotImplementedError
