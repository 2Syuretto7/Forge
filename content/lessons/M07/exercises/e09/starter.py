import math


def frequencies(d, base=10000):
    """The d/2 rotation speeds base**(-2j/d)."""
    raise NotImplementedError


def rope(x, m, base=10000):
    """x with each pair (x[2j], x[2j+1]) turned by m * omega_j."""
    raise NotImplementedError


def dot(u, v):
    """Sum of u_i v_i."""
    raise NotImplementedError


def score(q, k, m, n):
    """Dot product of q encoded at m and k encoded at n."""
    raise NotImplementedError
