import time

import numpy as np


def time_matmul(n, repeats=3, seed=0):
    """Fastest of several timings of an n by n product."""
    raise NotImplementedError


def fit_exponent(ns, times):
    """Slope of log(time) against log(n)."""
    raise NotImplementedError


def predicted_ratio(n1, n2):
    """(n2 / n1) cubed."""
    raise NotImplementedError
