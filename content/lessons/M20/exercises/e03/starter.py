import math

import numpy as np


def jacobian_det(T, p, h=1e-6):
    """Determinant of the numerical Jacobian."""
    raise NotImplementedError


def det_polar(r, theta):
    """Polar coordinates."""
    raise NotImplementedError


def det_spherical(r, phi, theta):
    """Spherical coordinates."""
    raise NotImplementedError


def det_box_muller(u1, u2):
    """Absolute Jacobian determinant of Box-Muller."""
    raise NotImplementedError
