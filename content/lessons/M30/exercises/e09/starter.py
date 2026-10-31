import numpy as np


def kl_optimum(pi, r, beta):
    """The maximizer of expected reward minus beta KL(p || pi)."""
    raise NotImplementedError


def kl_objective(p, pi, r, beta):
    """Expected reward minus beta KL(p || pi)."""
    raise NotImplementedError


def implied_reward(p, pi, beta):
    """beta log(p / pi)."""
    raise NotImplementedError
