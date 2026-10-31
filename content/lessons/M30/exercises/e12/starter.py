import numpy as np


# provided
def make_noise(seed=0):
    return np.random.default_rng(seed).uniform(0.1, 3.0, size=10**5)


def allocation(noise, nu):
    """Water-filling allocation at level nu."""
    raise NotImplementedError


def water_level(noise, P):
    """The level at which the allocation uses the whole budget."""
    raise NotImplementedError


def kkt_check(noise, x, nu):
    """Largest violation of dual feasibility and complementary slackness."""
    raise NotImplementedError
