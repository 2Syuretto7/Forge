def signed_density(y):
    """Without the absolute value."""
    return 1.0 * (-1 / (y * y))


def density(y):
    """Density of 1/X."""
    return 1 / (y * y)


def prob_greater(t):
    """P(Y > t)."""
    return 1 / t
