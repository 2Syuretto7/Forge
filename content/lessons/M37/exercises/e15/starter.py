import math
import numpy as np


def kde_score(X, t, centres, h):
    """Score of the noised kernel density estimate."""
    raise NotImplementedError


def generate(train, h, n, rng, steps=80, tmin=1e-4):
    """Reverse sampling with the kernel score."""
    raise NotImplementedError


def nn_distance(gen, train):
    """Median distance from generated points to the nearest training point."""
    raise NotImplementedError
