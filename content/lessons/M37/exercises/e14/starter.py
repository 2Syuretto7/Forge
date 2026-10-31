import math
import numpy as np


def frozen(score, t_star):
    """A score that always answers as if at time t_star."""
    raise NotImplementedError


def reverse(score, n, T, steps, rng):
    """Reverse-time SDE on a geometric grid."""
    raise NotImplementedError


def compare(score, data, t_star, rng):
    """W1 of samples from the true score and from the frozen one."""
    raise NotImplementedError
