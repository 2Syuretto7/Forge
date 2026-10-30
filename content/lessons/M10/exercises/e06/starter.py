from functools import reduce

import numpy as np


def apply(M, P):
    """Rows of P mapped by M."""
    raise NotImplementedError


def compose(*Ms):
    """Matrix of applying Ms[0], then Ms[1], ..."""
    raise NotImplementedError


def to_h(P):
    """Append a column of ones."""
    raise NotImplementedError


def from_h(H):
    """Drop the last column."""
    raise NotImplementedError


def translate(tx, ty):
    """3 by 3 translation."""
    raise NotImplementedError


def lift(M):
    """2 by 2 matrix as a 3 by 3 one."""
    raise NotImplementedError


def rotate_about(theta, c):
    """Rotation by theta about the point c, as a 3 by 3 matrix."""
    raise NotImplementedError
