import math

TARGETS = {
    "hill": (lambda x: math.exp(-x * x), -3.0, 3.0, 0.01),
    "sine": (math.sin, 0.0, 2 * math.pi, 0.005),
    "cubic": (lambda x: x ** 3 / 9, -3.0, 3.0, 0.01),
    "kink": (lambda x: abs(x) - 0.5, -2.0, 2.0, 1e-9),
    "root": (math.sqrt, 0.0, 4.0, 0.02),
}


def max_gap(f, a, b, m=60):
    """Largest gap between f and its chord on [a, b], at m points."""
    fa, fb = f(a), f(b)
    gap = 0.0
    for i in range(m):
        x = a + (b - a) * i / (m - 1)
        gap = max(gap, abs(f(x) - (fa + (fb - fa) * (x - a) / (b - a))))
    return gap


def adaptive_knots(f, a, b, tol):
    """Corners from splitting the worst piece at its midpoint until every gap is within tol."""
    pieces = [(a, b)]
    gaps = [max_gap(f, a, b)]
    while max(gaps) > tol:
        i = gaps.index(max(gaps))
        lo, hi = pieces.pop(i)
        gaps.pop(i)
        mid = (lo + hi) / 2
        pieces += [(lo, mid), (mid, hi)]
        gaps += [max_gap(f, lo, mid), max_gap(f, mid, hi)]
    return sorted({p[0] for p in pieces} | {p[1] for p in pieces})


def to_relus(f, knots):
    """(intercept, slope, inner_knots, weights) through (t, f(t)) for the corners."""
    y = [f(t) for t in knots]
    s = [(y[j + 1] - y[j]) / (knots[j + 1] - knots[j]) for j in range(len(knots) - 1)]
    weights = [s[j] - s[j - 1] for j in range(1, len(s))]
    return y[0] - s[0] * knots[0], s[0], knots[1:-1], weights


def evaluate(desc, x):
    """Value of a ReLU description at x."""
    c, s, knots, weights = desc
    return c + s * x + sum(w * max(0.0, x - t) for t, w in zip(knots, weights))


def build_all(targets):
    """Name -> corners for each target."""
    return {name: adaptive_knots(f, a, b, tol) for name, (f, a, b, tol) in targets.items()}


# your answer
REPORT = """
hill: 20 pieces, crowded near the top and the two shoulders where the hill bends most, sparse on the flat tails.
sine: 28 pieces, spread fairly evenly, a little denser near the peaks where the sine bends hardest.
cubic: 28 pieces, crowded at both ends where x^3/9 bends most and sparse near 0 where it is almost straight.
kink: 2 pieces, because the first split lands exactly on the corner at 0 and each side is already a straight line.
root: 12 pieces, crowded right next to 0 where the square root bends without limit, with long pieces further out.
"""
