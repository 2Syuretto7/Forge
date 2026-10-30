import numpy as np


def second_diff(f, x, h=1e-4):
    """Central second difference."""
    return (f(x + h) - 2 * f(x) + f(x - h)) / (h * h)


def convex_on_grid(f, a, b, n=200, h=1e-4):
    """Whether the second difference is nonnegative on a grid."""
    return all(second_diff(f, x, h) >= -1e-6 for x in np.linspace(a, b, n))


def chord_check(f, a, b, trials=500, seed=0):
    """Whether random chords lie above the graph."""
    rng = np.random.default_rng(seed)
    for _ in range(trials):
        x, y = rng.uniform(a, b, size=2)
        t = rng.uniform()
        if f(t * x + (1 - t) * y) > t * f(x) + (1 - t) * f(y) + 1e-12:
            return False
    return True
