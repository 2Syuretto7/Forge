import itertools
import numpy as np


def brute_force(W):
    """Minimum of x^T W x over sign vectors."""
    raise NotImplementedError


def eigen_bound(W):
    """n times the smallest eigenvalue: a Lagrangian lower bound."""
    raise NotImplementedError


def gap(W):
    """Duality gap p* - d."""
    raise NotImplementedError
