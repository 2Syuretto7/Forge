import numpy as np


def xavier(n_in, n_out, rng):
    """Normal weights with variance 2 / (n_in + n_out)."""
    raise NotImplementedError


def he(n_in, n_out, rng):
    """Normal weights with variance 2 / n_in."""
    raise NotImplementedError


def depth_rms(init, act, depth=30, width=256, batch=128, seed=0):
    """Push unit-normal inputs through `depth` layers h <- act(h W) with W from `init`
    ("xavier", "he" or "unit" for standard normal). Return the RMS of h after each layer."""
    raise NotImplementedError
