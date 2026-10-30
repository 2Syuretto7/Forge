def complete_square(a, b, c):
    """(h, k) with a x^2 + b x + c == a (x + h)^2 + k."""
    h = b / (2 * a)
    return h, c - b * b / (4 * a)


def vertex(a, b, c):
    """(x, y) of the parabola's turning point."""
    h, k = complete_square(a, b, c)
    return -h, k


def minimum_value(a, b, c):
    """Smallest value of a x^2 + b x + c for a > 0; ValueError otherwise."""
    if a <= 0:
        raise ValueError("no minimum unless a > 0")
    return complete_square(a, b, c)[1]
