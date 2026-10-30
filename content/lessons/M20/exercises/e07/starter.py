import numpy as np


def histogram_density(samples, bins, lo, hi):
    """(bin centers, estimated density)."""
    raise NotImplementedError


def max_relative_deviation(samples, pdf, bins, lo, hi, min_expected=1000):
    """Worst relative deviation over well-filled bins."""
    raise NotImplementedError
