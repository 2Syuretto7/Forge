import math
import numpy as np


def hoeffding_interval(correct, delta=0.05):
    """(accuracy, low, high) from Hoeffding's inequality."""
    raise NotImplementedError


def bootstrap_interval(correct, B=2000, seed=0, level=0.95):
    """(accuracy, low, high) from the percentile bootstrap."""
    raise NotImplementedError


def width_ratio(correct):
    """Width of the Hoeffding interval over the bootstrap's."""
    raise NotImplementedError
