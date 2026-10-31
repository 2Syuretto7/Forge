import math
import numpy as np


def line_fit(u, v):
    """(intercept, slope, s) of a least-squares line."""
    u, v = np.asarray(u, dtype=float), np.asarray(v, dtype=float)
    ub, vb = u.mean(), v.mean()
    slope = np.sum((u - ub) * (v - vb)) / np.sum((u - ub) ** 2)
    intercept = vb - slope * ub
    r = v - (intercept + slope * u)
    return intercept, slope, math.sqrt(r @ r / (len(u) - 2))


def prediction_half_width(u, s, u0, q):
    """Half-width of the prediction interval for a new observation at u0."""
    u = np.asarray(u, dtype=float)
    return q * s * math.sqrt(1 + 1 / len(u) + (u0 - u.mean()) ** 2 / np.sum((u - u.mean()) ** 2))


def coverage(n, q, u0, trials, rng, sigma=0.05):
    """Fraction of prediction intervals that contain a fresh observation."""
    u = np.linspace(0, math.log(100), n)
    hits = 0
    for _ in range(trials):
        v = 1.0 - 0.3 * u + sigma * rng.standard_normal(n)
        a, b, s = line_fit(u, v)
        new = 1.0 - 0.3 * u0 + sigma * rng.standard_normal()
        hits += abs(new - (a + b * u0)) <= prediction_half_width(u, s, u0, q)
    return hits / trials
