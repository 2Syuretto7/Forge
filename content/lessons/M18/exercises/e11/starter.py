import numpy as np


def directional_check(f, grad, x, k=5, h=1e-4, seed=0):
    """Worst relative difference over k random directions."""
    raise NotImplementedError


def buggy_grad(grad, i):
    """grad with entry i doubled."""
    raise NotImplementedError
