import numpy as np


def project_onto_line(b, a):
    """Projection of b onto the line through a."""
    raise NotImplementedError


def projection_matrix(A):
    """P = A (A^T A)^-1 A^T."""
    raise NotImplementedError


def project(b, A):
    """Projection of b onto the column space of A."""
    raise NotImplementedError
