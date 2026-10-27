import math
import numpy as np


def beta_logpdf(t, a, b):
    """Log density of Beta(a, b) at points t in (0, 1)."""
    raise NotImplementedError


def prob_a_better_grid(ka, na, kb, nb, m=20000):
    """P(theta_A > theta_B) under uniform priors, by numerical integration."""
    raise NotImplementedError


def prob_a_better_mc(ka, na, kb, nb, draws=200000, seed=0):
    """P(theta_A > theta_B) under uniform priors, by Monte Carlo."""
    raise NotImplementedError
