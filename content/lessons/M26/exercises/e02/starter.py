def machine_epsilon(dtype):
    """Gap between 1 and the next float of this type."""
    raise NotImplementedError


def unit_roundoff(dtype):
    """Largest relative rounding error."""
    raise NotImplementedError


def stall_point(dtype):
    """Smallest power of two N with N + 1 == N."""
    raise NotImplementedError
