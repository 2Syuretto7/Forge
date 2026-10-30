import math


class Complex:
    """A complex number re + im i."""

    def __init__(self, re, im=0.0):
        """Store the real and imaginary parts."""
        self.re = re
        self.im = im

    def __add__(self, w):
        """Sum."""
        return Complex(self.re + w.re, self.im + w.im)

    def __sub__(self, w):
        """Difference."""
        return Complex(self.re - w.re, self.im - w.im)

    def __mul__(self, w):
        """Product (ac - bd) + (ad + bc) i."""
        return Complex(self.re * w.re - self.im * w.im, self.re * w.im + self.im * w.re)

    def conj(self):
        """The conjugate re - im i."""
        return Complex(self.re, -self.im)

    def __abs__(self):
        """The modulus."""
        return math.sqrt(self.re ** 2 + self.im ** 2)

    def arg(self):
        """The angle, in (-pi, pi]."""
        return math.atan2(self.im, self.re)

    def close(self, w, tol=1e-9):
        """Both parts within tol."""
        return abs(self.re - w.re) <= tol and abs(self.im - w.im) <= tol


def from_polar(r, theta):
    """r (cos theta + i sin theta)."""
    return Complex(r * math.cos(theta), r * math.sin(theta))
