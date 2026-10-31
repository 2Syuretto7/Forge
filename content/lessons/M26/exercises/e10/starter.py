import math
import numpy as np


def _seq(carry, x, dtype):
    raise NotImplementedError


def stream_sums(n_chunks=100, chunk=10**6, seed=0):
    """Running totals of 10^8 uniform float32 numbers by six methods."""
    raise NotImplementedError


def errors(sums):
    """Absolute error of each method against the exact sum."""
    raise NotImplementedError
