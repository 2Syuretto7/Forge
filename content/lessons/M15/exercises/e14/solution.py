import math

import numpy as np


def jump_central(h):
    """Central difference of the step at 0."""
    H = lambda x: 1.0 if x > 0 else 0.0  # noqa: E731
    return (H(h) - H(-h)) / (2 * h)


def blowup_rate(hs):
    """Slope of log |estimate| against log h."""
    vals = np.array([jump_central(h) for h in hs])
    return float(np.polyfit(np.log(hs), np.log(np.abs(vals)), 1)[0])


def smoothed_step(x, w):
    """Sigmoid of width w."""
    return 1 / (1 + math.exp(-x / w))
