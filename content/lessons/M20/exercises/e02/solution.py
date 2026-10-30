import numpy as np


def mc_integral(f, box, n, seed=0):
    """(estimate, standard error) of the integral of f over the box."""
    ax, bx, ay, by = box
    rng = np.random.default_rng(seed)
    v = f(rng.uniform(ax, bx, n), rng.uniform(ay, by, n))
    area = (bx - ax) * (by - ay)
    return float(area * np.mean(v)), float(area * np.std(v, ddof=1) / np.sqrt(n))


def disc_area(n, seed=0):
    """Area of the unit disc by Monte Carlo."""
    return mc_integral(lambda x, y: (x * x + y * y <= 1).astype(float), (-1, 1, -1, 1), n, seed)
