import numpy as np


def lse(z):
    """Log-sum-exp with the max shift."""
    raise NotImplementedError


def lse_shifted(z, c):
    """c + ln sum exp(z - c)."""
    raise NotImplementedError


def bounds_hold(z):
    """max z <= LSE(z) <= max z + ln n."""
    raise NotImplementedError


def shift_is_exact(z, cs):
    """lse_shifted agrees with lse for every usable shift in cs."""
    raise NotImplementedError
