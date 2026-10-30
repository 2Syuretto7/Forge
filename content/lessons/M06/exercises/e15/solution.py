import numpy as np


def lse(z):
    """Log-sum-exp with the max shift."""
    m = z.max()
    return float(m + np.log(np.exp(z - m).sum()))


def lse_shifted(z, c):
    """c + ln sum exp(z - c)."""
    with np.errstate(all="ignore"):
        return float(c + np.log(np.exp(z - c).sum()))


def bounds_hold(z):
    """max z <= LSE(z) <= max z + ln n."""
    v = lse(z)
    return z.max() - 1e-12 <= v <= z.max() + np.log(z.size) + 1e-12


def shift_is_exact(z, cs):
    """lse_shifted agrees with lse for every usable shift in cs."""
    target = lse(z)
    for c in cs:
        with np.errstate(all="ignore"):
            s = np.exp(z - c).sum()
        if not (0 < s < np.inf):
            continue
        if abs(lse_shifted(z, c) - target) > 1e-9 * max(1, abs(target)):
            return False
    return True
