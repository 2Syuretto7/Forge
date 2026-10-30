def sum_first(n):
    """1 + 2 + ... + n."""
    return n * (n + 1) // 2


def sum_odds(n):
    """1 + 3 + ... + (2n - 1)."""
    return n * n


def sum_squares(n):
    """1^2 + ... + n^2."""
    return n * (n + 1) * (2 * n + 1) // 6


def sum_cubes(n):
    """1^3 + ... + n^3."""
    return sum_first(n) ** 2
