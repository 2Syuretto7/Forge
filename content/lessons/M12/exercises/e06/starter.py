import numpy as np


def loss(x, A, b):
    """||Ax - b||^2."""
    raise NotImplementedError


def slope_vector(x, A, b):
    """s = 2 A^T (Ax - b)."""
    raise NotImplementedError


def step_down(A, b, steps):
    """Repeated steps against s with eta = 1 / (2 ||A||_F^2)."""
    raise NotImplementedError
