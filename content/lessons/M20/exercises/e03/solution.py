import math

import numpy as np


def jacobian_det(T, p, h=1e-6):
    """Determinant of the numerical Jacobian."""
    p = np.asarray(p, dtype=float)
    J = np.zeros((p.size, p.size))
    for j in range(p.size):
        e = np.zeros_like(p)
        e[j] = h
        J[:, j] = (np.asarray(T(p + e)) - np.asarray(T(p - e))) / (2 * h)
    return float(np.linalg.det(J))


def det_polar(r, theta):
    """Polar coordinates."""
    return r


def det_spherical(r, phi, theta):
    """Spherical coordinates."""
    return r * r * math.sin(phi)


def det_box_muller(u1, u2):
    """Absolute Jacobian determinant of Box-Muller."""
    return 2 * math.pi / u1
