import math
import numpy as np


def coverage(intervals, truth):
    """Fraction of intervals that contain truth."""
    raise NotImplementedError


def hoeffding_intervals(accs, n, delta=0.05):
    """Hoeffding intervals around each accuracy."""
    raise NotImplementedError


def clt_intervals(accs, n, z=1.96):
    """Normal-approximation intervals around each accuracy."""
    raise NotImplementedError


def simulate(p, n, sets, rng):
    """Measured accuracies of independent test sets."""
    raise NotImplementedError
