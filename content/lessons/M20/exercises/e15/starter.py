import math


def _phi(x):
    raise NotImplementedError


def one_branch(y):
    """Only the positive preimage."""
    raise NotImplementedError


def chi_square_1(y):
    """Both preimages."""
    raise NotImplementedError


def total_half_open(density, upper=60.0, n=200_000):
    """Integral over (0, upper] after substituting y = t^2."""
    raise NotImplementedError
