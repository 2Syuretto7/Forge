import math
import numpy as np


def iterations_bound(kappa, eps, step="best"):
    """Iterations the rate bound guarantees for relative error eps."""
    raise NotImplementedError


def iterations_needed(A, b, x0, step, eps, max_iter=10**6):
    """Gradient-descent steps until the error falls below eps times the initial error."""
    raise NotImplementedError
