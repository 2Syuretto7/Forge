import math
import numpy as np


def rw_metropolis(log_p, x0, step, n, rng):
    """Random-walk Metropolis: (samples of shape (n, d), acceptance rate)."""
    raise NotImplementedError


def independence_mh(log_p, sample_q, log_q, x0, n, rng, correct=True):
    """Independence sampler, with or without the Hastings correction."""
    raise NotImplementedError
