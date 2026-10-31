import math
import numpy as np


def laplace_logpdf(x, b=1.0):
    """Log-density of the Laplace distribution with scale b."""
    raise NotImplementedError


def laplace_sample(b, n, rng):
    """Laplace(0, b) samples by the inverse CDF."""
    raise NotImplementedError


def is_run(proposal, n, rng):
    """(estimate of E_p[X^2], standard error, ESS fraction) for the Laplace target."""
    raise NotImplementedError
