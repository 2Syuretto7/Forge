import math

import numpy as np


def jump_central(h):
    """Central difference of the step at 0."""
    raise NotImplementedError


def blowup_rate(hs):
    """Slope of log |estimate| against log h."""
    raise NotImplementedError


def smoothed_step(x, w):
    """Sigmoid of width w."""
    raise NotImplementedError
