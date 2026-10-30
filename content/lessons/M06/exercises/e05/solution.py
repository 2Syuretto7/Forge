import math


def doubling_time(rate):
    """Years to double at a yearly growth fraction rate."""
    return math.log(2) / math.log(1 + rate)


def continuous_doubling_time(r):
    """Years to double under continuous growth e**(r t)."""
    return math.log(2) / r


def rule_of_70(percent):
    """70 / percent."""
    return 70 / percent


def half_life(k):
    """Time for e**(-k t) to halve."""
    return math.log(2) / k


def growth_factor(r, years):
    """e**(r * years)."""
    return math.exp(r * years)
