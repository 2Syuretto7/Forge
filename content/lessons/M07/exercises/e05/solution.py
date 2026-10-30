import cmath
import math


def rotate_complex(p, theta):
    """Rotate p by multiplying by cos theta + i sin theta."""
    z = complex(*p) * complex(math.cos(theta), math.sin(theta))
    return z.real, z.imag


def rotate_trig(p, theta):
    """Rotate p with the rotation formula."""
    x, y = p
    c, s = math.cos(theta), math.sin(theta)
    return x * c - y * s, x * s + y * c


def compose_angles(thetas):
    """Angle of the product of the unit complex numbers for the angles."""
    z = complex(1, 0)
    for t in thetas:
        z *= complex(math.cos(t), math.sin(t))
    return cmath.phase(z)


def quarter_turns(p, k):
    """p multiplied by i, k times."""
    z = complex(*p)
    for _ in range(k):
        z *= 1j
    return z.real, z.imag
