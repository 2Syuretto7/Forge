def shift(f, h, k):
    """x -> f(x - h) + k."""
    raise NotImplementedError


def stretch(f, a, b):
    """x -> b f(x / a)."""
    raise NotImplementedError


def reflect_y(f):
    """x -> f(-x)."""
    raise NotImplementedError


def reflect_x(f):
    """x -> -f(x)."""
    raise NotImplementedError


def vertex_after_shift(h, k):
    """Lowest point of x^2 shifted right by h and up by k."""
    raise NotImplementedError
