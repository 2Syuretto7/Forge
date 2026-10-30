# provided
def simpson(f, a, b, n=2000):
    h = (b - a) / n
    return h / 3 * sum((1 if k in (0, n) else 4 if k % 2 else 2) * f(a + k * h) for k in range(n + 1))


def prob_between(pdf, lo, hi):
    """Probability of [lo, hi]."""
    return simpson(pdf, lo, hi)


def mean(pdf, a, b):
    """Expected value."""
    return simpson(lambda x: x * pdf(x), a, b)


def variance(pdf, a, b):
    """Variance."""
    mu = mean(pdf, a, b)
    return simpson(lambda x: (x - mu) ** 2 * pdf(x), a, b)


def quantile(pdf, a, b, q):
    """x with cumulative probability q."""
    lo, hi = a, b
    while hi - lo > 1e-10:
        m = (lo + hi) / 2
        if simpson(pdf, a, m, 200) < q:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2
