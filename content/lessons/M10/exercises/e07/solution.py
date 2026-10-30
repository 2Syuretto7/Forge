import numpy as np


def polygon_area(P):
    """Signed shoelace area."""
    Q = np.roll(P, -1, axis=0)
    return 0.5 * float(np.sum(P[:, 0] * Q[:, 1] - Q[:, 0] * P[:, 1]))


def area_ratio(M, P):
    """Signed area of the image over the signed area of P."""
    return polygon_area(P @ M.T) / polygon_area(P)
