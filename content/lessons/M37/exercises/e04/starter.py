import numpy as np


def _logcomp(x, w, m, s):
    raise NotImplementedError


def mixture_logpdf(x, w, m, s):
    """Log density of a one-dimensional Gaussian mixture."""
    raise NotImplementedError


def responsibilities(x, w, m, s):
    """Posterior probability of each component."""
    raise NotImplementedError


def mixture_score(x, w, m, s):
    """Derivative of the log density."""
    raise NotImplementedError
