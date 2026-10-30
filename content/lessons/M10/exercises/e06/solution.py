from functools import reduce

import numpy as np


def apply(M, P):
    """Rows of P mapped by M."""
    return P @ M.T


def compose(*Ms):
    """Matrix of applying Ms[0], then Ms[1], ..."""
    return reduce(lambda acc, M: M @ acc, Ms[1:], Ms[0])


def to_h(P):
    """Append a column of ones."""
    return np.hstack([P, np.ones((len(P), 1))])


def from_h(H):
    """Drop the last column."""
    return H[:, :-1]


def translate(tx, ty):
    """3 by 3 translation."""
    return np.array([[1.0, 0, tx], [0, 1.0, ty], [0, 0, 1.0]])


def lift(M):
    """2 by 2 matrix as a 3 by 3 one."""
    L = np.eye(3)
    L[:2, :2] = M
    return L


def rotate_about(theta, c):
    """Rotation by theta about the point c, as a 3 by 3 matrix."""
    R = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    return translate(c[0], c[1]) @ lift(R) @ translate(-c[0], -c[1])
