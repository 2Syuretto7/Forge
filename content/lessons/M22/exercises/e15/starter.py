import numpy as np


def plug_in(g, values, probs):
    """g(E[X])."""
    raise NotImplementedError


def expect(g, values, probs):
    """E[g(X)]."""
    raise NotImplementedError


def mc_expect(g, samples):
    """Monte Carlo estimate of E[g(X)]."""
    raise NotImplementedError


def relu_second_moment():
    """E[max(Z, 0)^2] for a standard normal Z."""
    raise NotImplementedError
