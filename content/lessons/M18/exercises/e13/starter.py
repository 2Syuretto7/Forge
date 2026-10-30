import numpy as np


def check(f, grad, x, dtype, h, tol):
    """(passed, relative error) of a central-difference check in dtype."""
    raise NotImplementedError


def float32_noise_floor(f, x, h):
    """Relative error of a correct float32 check."""
    raise NotImplementedError
