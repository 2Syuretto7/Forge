import numpy as np


def project_onto_line(b, a):
    """b, a: shape (m,). Return the projection of b onto span{a}, shape (m,)."""
    raise NotImplementedError


def projection_matrix(A):
    """A: shape (m, n), independent columns. Return P, shape (m, m)."""
    raise NotImplementedError


def project(b, A):
    """Return the projection of b (shape (m,)) onto the column space of A."""
    raise NotImplementedError
