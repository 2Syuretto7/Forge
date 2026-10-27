import numpy as np


def jacobian_forward(jvp, n):
    """Return (J, number of jvp calls)."""
    raise NotImplementedError


def jacobian_reverse(vjp, m):
    """Return (J, number of vjp calls)."""
    raise NotImplementedError


def cheaper_mode(n, m):
    raise NotImplementedError
