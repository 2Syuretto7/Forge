import numpy as np


def numerical_jacobian(f, x, h=1e-6):
    """Return the (m, n) central-difference Jacobian of f at x (n,)."""
    raise NotImplementedError


def jacobian_of_composition(Jg, Jf):
    """Jacobian of g(f(x)) given Jg (at f(x)) and Jf (at x)."""
    raise NotImplementedError
