import math


def items_needed(p, half_width, z=1.96):
    """Items needed for a confidence interval of +- half_width around an accuracy near p:
    n = z^2 p (1 - p) / half_width^2, rounded up."""
    return math.ceil(z * z * p * (1 - p) / half_width ** 2)


def detectable_difference(p, n, z=1.96):
    """Roughly the smallest accuracy difference between two independent evaluations of n items
    each that a 95% test can detect: z sqrt(2 p (1 - p) / n)."""
    return z * math.sqrt(2 * p * (1 - p) / n)
