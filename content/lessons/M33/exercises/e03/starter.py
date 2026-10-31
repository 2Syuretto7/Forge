import math
import numpy as np


def blocked_matmul(A, B, b):
    """Tile-by-tile matrix product."""
    raise NotImplementedError


def traffic_naive(n):
    """Words moved by the naive triple loop."""
    raise NotImplementedError


def traffic_blocked(n, b):
    """Words moved by the blocked algorithm with b x b tiles."""
    raise NotImplementedError


def best_tile(cache_words):
    """Largest tile with three tiles in cache."""
    raise NotImplementedError
