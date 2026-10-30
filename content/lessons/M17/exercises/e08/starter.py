# provided
def simpson(f, a, b, n=2000):
    h = (b - a) / n
    return h / 3 * sum((1 if k in (0, n) else 4 if k % 2 else 2) * f(a + k * h) for k in range(n + 1))


def prob_between(pdf, lo, hi):
    """Probability of [lo, hi]."""
    raise NotImplementedError


def mean(pdf, a, b):
    """Expected value."""
    raise NotImplementedError


def variance(pdf, a, b):
    """Variance."""
    raise NotImplementedError


def quantile(pdf, a, b, q):
    """x with cumulative probability q."""
    raise NotImplementedError
