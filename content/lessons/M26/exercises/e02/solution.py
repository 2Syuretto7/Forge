def machine_epsilon(dtype):
    """Gap between 1 and the next float of this type."""
    one, two = dtype(1), dtype(2)
    eps = dtype(1)
    while one + eps / two != one:
        eps = eps / two
    return float(eps)


def unit_roundoff(dtype):
    """Largest relative rounding error."""
    return machine_epsilon(dtype) / 2


def stall_point(dtype):
    """Smallest power of two N with N + 1 == N."""
    n = dtype(1)
    while n + dtype(1) != n:
        n = n * dtype(2)
    return float(n)
