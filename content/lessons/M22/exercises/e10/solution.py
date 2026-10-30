import math
import numpy as np


def chunk_stats(x):
    """(n, mean, M2) of an array."""
    x = np.asarray(x, dtype=float)
    m = float(x.mean())
    return len(x), m, float(np.sum((x - m) ** 2))


def merge(a, b):
    """Summary of the union of two chunks."""
    na, ma, sa = a
    nb, mb, sb = b
    n = na + nb
    if n == 0:
        return 0, 0.0, 0.0
    d = mb - ma
    return n, ma + d * nb / n, sa + sb + d * d * na * nb / n


def streaming_moments(draw, n, chunk=10**6):
    """(mean, variance) of n draws, drawn chunk by chunk."""
    acc = (0, 0.0, 0.0)
    done = 0
    while done < n:
        k = min(chunk, n - done)
        acc = merge(acc, chunk_stats(draw(k)))
        done += k
    return acc[1], acc[2] / (acc[0] - 1)


def mean_se(var, n):
    """Standard error of the sample mean."""
    return math.sqrt(var / n)


def var_se(var, m4, n):
    """Standard error of the sample variance."""
    return math.sqrt((m4 - var**2) / n)
