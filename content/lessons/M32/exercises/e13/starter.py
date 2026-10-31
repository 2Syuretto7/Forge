import math
from functools import reduce
import numpy as np


def communicating_classes(P):
    """Classes of mutually reachable states."""
    raise NotImplementedError


def n_stationary(P, tol=1e-9):
    """Number of eigenvalues equal to 1."""
    raise NotImplementedError


def period(P, i):
    """gcd of return times to state i, up to 3n steps."""
    raise NotImplementedError


def long_run(P, x0, steps=2000):
    """Distribution after many steps from x0."""
    raise NotImplementedError
