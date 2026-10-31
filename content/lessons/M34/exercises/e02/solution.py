import numpy as np


def cosines(d, pairs, rng):
    """Cosines between independent random vectors."""
    X = rng.standard_normal((pairs, d))
    Y = rng.standard_normal((pairs, d))
    return np.einsum("ij,ij->i", X, Y) / (np.linalg.norm(X, axis=1) * np.linalg.norm(Y, axis=1))


def angles_degrees(d, pairs, rng):
    """Angles between independent random vectors, in degrees."""
    return np.degrees(np.arccos(cosines(d, pairs, rng)))


def predicted_angle_sd(d):
    """Standard deviation of the angle, in degrees, for large d."""
    return 180 / (np.pi * np.sqrt(d))
