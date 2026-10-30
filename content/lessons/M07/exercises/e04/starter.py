import math


class Complex:
    """A complex number re + im i."""

    def __init__(self, re, im=0.0):
        """Store the real and imaginary parts."""
        raise NotImplementedError

    def __add__(self, w):
        """Sum."""
        raise NotImplementedError

    def __sub__(self, w):
        """Difference."""
        raise NotImplementedError

    def __mul__(self, w):
        """Product (ac - bd) + (ad + bc) i."""
        raise NotImplementedError

    def conj(self):
        """The conjugate re - im i."""
        raise NotImplementedError

    def __abs__(self):
        """The modulus."""
        raise NotImplementedError

    def arg(self):
        """The angle, in (-pi, pi]."""
        raise NotImplementedError

    def close(self, w, tol=1e-9):
        """Both parts within tol."""
        raise NotImplementedError


def from_polar(r, theta):
    """r (cos theta + i sin theta)."""
    raise NotImplementedError
