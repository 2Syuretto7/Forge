import numpy as np


def relative_contrast(d, n, rng, queries=20):
    """Average (max - min) / min distance from random queries to n uniform points."""
    P = rng.random((n, d))
    vals = []
    for _ in range(queries):
        dist = np.linalg.norm(P - rng.random(d), axis=1)
        vals.append((dist.max() - dist.min()) / dist.min())
    return float(np.mean(vals))


def expected_sq_distance(d):
    """Mean squared distance between independent uniform points in the unit cube."""
    return d / 6


def distance_cv(d, n, rng):
    """Coefficient of variation of distances between independent uniform pairs."""
    dist = np.linalg.norm(rng.random((n, d)) - rng.random((n, d)), axis=1)
    return float(dist.std() / dist.mean())
