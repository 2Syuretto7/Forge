def solve_2x2(a, b, c, d, p, q):
    """Solve a x + b y = p, c x + d y = q by elimination; ValueError if ad - bc == 0."""
    det = a * d - b * c
    if det == 0:
        raise ValueError("the equations are not independent")
    return (p * d - b * q) / det, (a * q - c * p) / det


def residual(a, b, c, d, p, q, x, y):
    """Largest absolute error of (x, y) in the two equations."""
    return max(abs(a * x + b * y - p), abs(c * x + d * y - q))
