import math


def vanishing_step(x, h):
    """Whether x + h rounds back to x."""
    raise NotImplementedError


def forward_at(f, x, h):
    """Forward difference."""
    raise NotImplementedError


def smallest_visible_step(x):
    """Smallest 10^-k with x + 10^-k != x."""
    raise NotImplementedError


def digits_correct(est, exact):
    """-log10 of the relative error, capped at 16."""
    raise NotImplementedError
