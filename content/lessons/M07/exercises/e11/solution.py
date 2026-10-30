import numpy as np


def _R(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, s], [-s, c]])


def turn_direct(points, k, delta):
    """One rotation by k * delta."""
    return points @ _R(k * delta)


def turn_repeated(points, k, delta):
    """k rotations by delta."""
    X, R = points.copy(), _R(delta)
    for _ in range(k):
        X = X @ R
    return X


def gap(points, k, delta):
    """Largest difference between the direct and the repeated turn."""
    return float(np.max(np.abs(turn_direct(points, k, delta) - turn_repeated(points, k, delta))))


def gap_growth(points, ks, delta):
    """Gaps for each k."""
    return [gap(points, k, delta) for k in ks]
