import time

import numpy as np


def f(x):
    """Softplus sum plus a smoothness penalty."""
    raise NotImplementedError


def grad(x):
    """Analytic gradient in O(n)."""
    raise NotImplementedError


def fd_grad(x, h=1e-6):
    """Central differences, 2n evaluations."""
    raise NotImplementedError


def speedup(n):
    """Time of fd_grad over time of grad."""
    raise NotImplementedError
