import math


class Vec:
    """A vector stored as a list of floats."""

    def __init__(self, coords):
        """Store the coordinates."""
        raise NotImplementedError

    def _check(self, w):
        raise NotImplementedError

    def __add__(self, w):
        """Coordinate-wise sum."""
        raise NotImplementedError

    def __sub__(self, w):
        """Coordinate-wise difference."""
        raise NotImplementedError

    def __mul__(self, k):
        """Scale by a number."""
        raise NotImplementedError

    def __rmul__(self, k):
        """Number times vector."""
        raise NotImplementedError

    def __len__(self):
        """Number of coordinates."""
        raise NotImplementedError

    def dot(self, w):
        """Sum of products of coordinates."""
        raise NotImplementedError

    def norm(self):
        """Euclidean length."""
        raise NotImplementedError

    def unit(self):
        """Unit vector in the same direction; ValueError for zero."""
        raise NotImplementedError
