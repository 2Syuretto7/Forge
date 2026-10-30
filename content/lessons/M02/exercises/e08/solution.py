import math


def discriminant(a, b, c):
    """b^2 - 4ac."""
    return b * b - 4 * a * c


def solve_quadratic(a, b, c):
    """Sorted distinct real roots of a x^2 + b x + c = 0; ValueError when a == 0."""
    if a == 0:
        raise ValueError("not a quadratic")
    D = discriminant(a, b, c)
    if D < 0:
        return []
    if D == 0:
        return [-b / (2 * a)]
    s = math.sqrt(D)
    return sorted([(-b - s) / (2 * a), (-b + s) / (2 * a)])
