def pipeline(steps):
    """Apply steps left to right."""
    def machine(x):
        for f in steps:
            x = f(x)
        return x
    return machine


def standardize(xs):
    """(x - mean) / std with the population standard deviation."""
    n = len(xs)
    m = sum(xs) / n
    s = (sum((x - m) ** 2 for x in xs) / n) ** 0.5
    return [(x - m) / s for x in xs]


def clip(xs, lo, hi):
    """Each value limited to [lo, hi]."""
    return [min(max(x, lo), hi) for x in xs]


def order_matters(xs, lo, hi):
    """Whether clip-then-standardize differs from standardize-then-clip."""
    a = pipeline([lambda v: clip(v, lo, hi), standardize])(xs)
    b = pipeline([standardize, lambda v: clip(v, lo, hi)])(xs)
    return any(abs(p - q) > 1e-12 for p, q in zip(a, b))
