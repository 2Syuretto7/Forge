import math
import numpy as np


def em_ou(x0, theta, sigma, h, steps, n, rng):
    """Euler-Maruyama for the Ornstein-Uhlenbeck process."""
    x = np.full(n, float(x0))
    with np.errstate(over="ignore", invalid="ignore"):
        for _ in range(steps):
            x = x - theta * x * h + sigma * math.sqrt(h) * rng.standard_normal(n)
    return x


def em_stationary_var(theta, sigma, h):
    """Stationary variance of the Euler-Maruyama recursion."""
    if theta * h >= 2:
        return math.inf
    return sigma**2 / (theta * (2 - theta * h))


def exact_ou(x0, theta, sigma, h, steps, n, rng):
    """Exact transitions for the same process."""
    e = math.exp(-theta * h)
    sd = math.sqrt(sigma**2 / (2 * theta) * (1 - e * e))
    x = np.full(n, float(x0))
    for _ in range(steps):
        x = x * e + sd * rng.standard_normal(n)
    return x
