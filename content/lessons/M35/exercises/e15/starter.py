import math
import numpy as np


def line_fit(u, v):
    """(intercept, slope, s) of a least-squares line."""
    raise NotImplementedError


def prediction_half_width(u, s, u0, q):
    """Half-width of the prediction interval for a new observation at u0."""
    raise NotImplementedError


def coverage(n, q, u0, trials, rng, sigma=0.05):
    """Fraction of prediction intervals that contain a fresh observation."""
    raise NotImplementedError
