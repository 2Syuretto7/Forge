import math


def softmax_naive(z):
    """e**z_i / sum e**z_j, as written."""
    es = [math.exp(v) for v in z]
    s = sum(es)
    return [e / s for e in es]


def softmax(z):
    """Softmax after subtracting the maximum score."""
    m = max(z)
    es = [math.exp(v - m) for v in z]
    s = sum(es)
    return [e / s for e in es]


def argmax(z):
    """Index of the largest score."""
    return z.index(max(z))
