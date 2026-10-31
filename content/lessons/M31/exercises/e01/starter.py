import math


def hoeffding_bound(n, eps, a=0.0, b=1.0):
    """Hoeffding's bound on P(|mean - mu| >= eps)."""
    raise NotImplementedError


def hoeffding_epsilon(n, delta, a=0.0, b=1.0):
    """Half-width guaranteed with probability 1 - delta."""
    raise NotImplementedError


def hoeffding_n(eps, delta, a=0.0, b=1.0):
    """Samples guaranteeing half-width eps with probability 1 - delta."""
    raise NotImplementedError
