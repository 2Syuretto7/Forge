import math


def _phi(x):
    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)


def one_branch(y):
    """Only the positive preimage."""
    return _phi(math.sqrt(y)) / (2 * math.sqrt(y))


def chi_square_1(y):
    """Both preimages."""
    return math.exp(-y / 2) / math.sqrt(2 * math.pi * y)


def total_half_open(density, upper=60.0, n=200_000):
    """Integral over (0, upper] after substituting y = t^2."""
    b = math.sqrt(upper)
    h = b / n
    return sum(density((h * (k + 0.5)) ** 2) * 2 * h * (k + 0.5) for k in range(n)) * h
