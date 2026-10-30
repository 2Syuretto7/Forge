import math


class Vec:
    """A vector stored as a list of floats."""

    def __init__(self, coords):
        """Store the coordinates."""
        self.c = [float(x) for x in coords]

    def _check(self, w):
        if len(self.c) != len(w.c):
            raise ValueError("vectors of different lengths")

    def __add__(self, w):
        """Coordinate-wise sum."""
        self._check(w)
        return Vec([a + b for a, b in zip(self.c, w.c)])

    def __sub__(self, w):
        """Coordinate-wise difference."""
        self._check(w)
        return Vec([a - b for a, b in zip(self.c, w.c)])

    def __mul__(self, k):
        """Scale by a number."""
        return Vec([k * a for a in self.c])

    def __rmul__(self, k):
        """Number times vector."""
        return self * k

    def __len__(self):
        """Number of coordinates."""
        return len(self.c)

    def dot(self, w):
        """Sum of products of coordinates."""
        self._check(w)
        return sum(a * b for a, b in zip(self.c, w.c))

    def norm(self):
        """Euclidean length."""
        return math.sqrt(self.dot(self))

    def unit(self):
        """Unit vector in the same direction; ValueError for zero."""
        n = self.norm()
        if n == 0:
            raise ValueError("the zero vector has no direction")
        return self * (1 / n)
