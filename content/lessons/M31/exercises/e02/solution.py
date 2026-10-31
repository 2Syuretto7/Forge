import math


def exact_tail(n, p, eps):
    """P(|K/n - p| >= eps) for K ~ Binomial(n, p)."""
    total = 0.0
    for k in range(n + 1):
        if abs(k / n - p) >= eps - 1e-12:
            lc = math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
            total += math.exp(lc + k * math.log(p) + (n - k) * math.log(1 - p))
    return min(1.0, total)


def chebyshev(n, p, eps):
    """Chebyshev's bound."""
    return min(1.0, p * (1 - p) / (n * eps * eps))


def hoeffding(n, eps):
    """Hoeffding's bound."""
    return min(1.0, 2 * math.exp(-2 * n * eps * eps))


def ratio_table(n, p, eps):
    """The exact tail and both bounds."""
    return {"exact": exact_tail(n, p, eps), "chebyshev": chebyshev(n, p, eps), "hoeffding": hoeffding(n, eps)}
