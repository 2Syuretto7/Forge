import math
import numpy as np


def em_ou(x0, theta, sigma, h, steps, n, rng):
    """Euler-Maruyama for the Ornstein-Uhlenbeck process."""
    raise NotImplementedError


def em_stationary_var(theta, sigma, h):
    """Stationary variance of the Euler-Maruyama recursion."""
    raise NotImplementedError


def exact_ou(x0, theta, sigma, h, steps, n, rng):
    """Exact transitions for the same process."""
    raise NotImplementedError
