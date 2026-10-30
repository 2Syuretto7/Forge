import numpy as np


def block_matmul(A, B, bs):
    """AB computed tile by tile."""
    raise NotImplementedError


def tile_count(m, n, p, bs):
    """Number of tile products."""
    raise NotImplementedError
