def brackets(f, y, lo, hi, m=1000):
    """Cells (a, b) of an m-cell grid where f - y changes sign or is zero at a."""
    g = lambda x: f(x) - y
    xs = [lo + (hi - lo) * i / m for i in range(m + 1)]
    out = []
    for a, b in zip(xs[:-1], xs[1:]):
        if g(a) == 0 or g(a) * g(b) < 0:
            out.append((a, b))
    if g(xs[-1]) == 0:
        out.append((xs[-2], xs[-1]))
    return out


def bisect(f, y, a, b, steps=60):
    """Root of f - y on [a, b] whose ends have opposite signs (or a zero)."""
    g = lambda x: f(x) - y
    if g(a) == 0:
        return a
    if g(b) == 0:
        return b
    for _ in range(steps):
        mid = (a + b) / 2
        if g(a) * g(mid) <= 0:
            b = mid
        else:
            a = mid
    return (a + b) / 2


def all_preimages(f, y, lo, hi):
    """Every solution of f(x) = y in [lo, hi], sorted."""
    return sorted(bisect(f, y, a, b) for a, b in brackets(f, y, lo, hi))
