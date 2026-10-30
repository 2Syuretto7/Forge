import math
import numpy as np


def chunk_stats(x):
    """(n, mean, M2) of an array."""
    raise NotImplementedError


def merge(a, b):
    """Summary of the union of two chunks."""
    raise NotImplementedError


def streaming_moments(draw, n, chunk=10**6):
    """(mean, variance) of n draws, drawn chunk by chunk."""
    raise NotImplementedError


def mean_se(var, n):
    """Standard error of the sample mean."""
    raise NotImplementedError


def var_se(var, m4, n):
    """Standard error of the sample variance."""
    raise NotImplementedError
