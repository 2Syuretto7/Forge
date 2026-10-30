def shift(f, h, k):
    """x -> f(x - h) + k."""
    return lambda x: f(x - h) + k


def stretch(f, a, b):
    """x -> b f(x / a)."""
    return lambda x: b * f(x / a)


def reflect_y(f):
    """x -> f(-x)."""
    return lambda x: f(-x)


def reflect_x(f):
    """x -> -f(x)."""
    return lambda x: -f(x)


def vertex_after_shift(h, k):
    """Lowest point of x^2 shifted right by h and up by k."""
    return h, k
