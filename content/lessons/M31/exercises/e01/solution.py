import math


def hoeffding_bound(n, eps, a=0.0, b=1.0):
    """Hoeffding's bound on P(|mean - mu| >= eps)."""
    return min(1.0, 2 * math.exp(-2 * n * eps * eps / (b - a) ** 2))


def hoeffding_epsilon(n, delta, a=0.0, b=1.0):
    """Half-width guaranteed with probability 1 - delta."""
    return (b - a) * math.sqrt(math.log(2 / delta) / (2 * n))


def hoeffding_n(eps, delta, a=0.0, b=1.0):
    """Samples guaranteeing half-width eps with probability 1 - delta."""
    return math.ceil(round((b - a) ** 2 * math.log(2 / delta) / (2 * eps * eps), 9))
