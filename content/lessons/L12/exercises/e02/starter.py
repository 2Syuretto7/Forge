import numpy as np


def tiled_matmul(A, B, T):
    """C = A B computed in T x T output tiles, looping over K in steps of T, with sizes that need not be
    multiples of T. Return (C, loads), where loads counts the elements read from A and B."""
    raise NotImplementedError
