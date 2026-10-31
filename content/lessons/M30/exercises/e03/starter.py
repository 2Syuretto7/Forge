import numpy as np


def project_box(y, lo, hi):
    """Closest point of the box [lo, hi]^n."""
    raise NotImplementedError


def project_ball(y, r):
    """Closest point of the ball of radius r."""
    raise NotImplementedError


def project_simplex(y):
    """Closest point of the probability simplex."""
    raise NotImplementedError


def projected_gd(grad, proj, x0, step, iters):
    """Projected gradient descent; returns the last iterate."""
    raise NotImplementedError
