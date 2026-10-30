import numpy as np


def numerical_jacobian(f, x, h=1e-6):
    """Central-difference Jacobian, shape (m, n)."""
    raise NotImplementedError


def jacobian_of_composition(Jg, Jf):
    """Jacobian of g(f(x))."""
    raise NotImplementedError
