import numpy as np


def norms(d, samples, rng):
    """Norms of random standard normal vectors."""
    raise NotImplementedError


def relative_spread(d, samples, rng):
    """Standard deviation of the norm over sqrt(d)."""
    raise NotImplementedError


def fraction_in_shell(d, samples, rng, width=0.1):
    """Fraction of norms within width sqrt(d) of sqrt(d)."""
    raise NotImplementedError
