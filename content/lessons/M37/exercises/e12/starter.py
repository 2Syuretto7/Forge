import math
import numpy as np


def _sample(score, n, T, steps, rng):
    raise NotImplementedError


def quality_vs_T(score, data, Ts, steps, rng):
    """W1 to the data for each end time T."""
    raise NotImplementedError


def prior_mismatch(w, m, s, T):
    """W1 between the noised mixture at T and the standard normal."""
    raise NotImplementedError
