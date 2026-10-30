import math


def cos_sum(a, b):
    """cos(a + b) from cos and sin of a and b."""
    return math.cos(a) * math.cos(b) - math.sin(a) * math.sin(b)


def sin_sum(a, b):
    """sin(a + b) from cos and sin of a and b."""
    return math.sin(a) * math.cos(b) + math.cos(a) * math.sin(b)


def double_angle(a):
    """(cos 2a, sin 2a)."""
    return cos_sum(a, a), sin_sum(a, a)


def half_angle_cos(a):
    """cos(a/2) for a in [0, pi]."""
    return math.sqrt((1 + math.cos(a)) / 2)
