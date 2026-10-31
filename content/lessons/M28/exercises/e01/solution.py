import numpy as np


def chord_violation(f, a, b, ts):
    """Largest amount by which f rises above its chord between a and b."""
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    fa, fb = f(a), f(b)
    return float(max(f(t * a + (1 - t) * b) - (t * fa + (1 - t) * fb) for t in ts))


def search_violation(f, dim, trials, rng, scale=3.0):
    """Largest chord violation over random pairs of points."""
    ts = np.linspace(0, 1, 21)
    worst = -np.inf
    for _ in range(trials):
        a = rng.uniform(-scale, scale, size=dim)
        b = rng.uniform(-scale, scale, size=dim)
        worst = max(worst, chord_violation(f, a, b, ts))
    return float(worst)


def second_difference_min(f, lo, hi, n=2001):
    """Smallest second difference of f on a grid."""
    x = np.linspace(lo, hi, n)
    y = np.array([f(v) for v in x])
    return float(np.min(y[:-2] - 2 * y[1:-1] + y[2:]))
