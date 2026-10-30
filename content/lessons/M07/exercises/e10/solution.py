import numpy as np


def rotation(theta, dtype):
    """Matrix turning row vectors by theta under points @ R."""
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, s], [-s, c]], dtype=dtype)


def turn_many(points, steps, dtype):
    """Turn the points by 2 pi / steps, steps times, in dtype."""
    X = points.astype(dtype)
    R = rotation(2 * np.pi / steps, dtype)
    for _ in range(steps):
        X = X @ R
    return X


def drift(points, steps, dtype):
    """Largest absolute difference after a full circle in steps steps."""
    return float(np.max(np.abs(turn_many(points, steps, dtype).astype(np.float64) - points)))
