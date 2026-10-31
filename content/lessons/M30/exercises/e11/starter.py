import numpy as np


# provided
def make_rewards(seed=0):
    return np.random.default_rng(seed).standard_normal(10**6)


def entropy(p):
    """Entropy in nats."""
    raise NotImplementedError


def effective_actions(p):
    """exp(entropy)."""
    raise NotImplementedError


def sweep(r, taus):
    """Entropy and expected reward of the Gibbs distribution at each temperature."""
    raise NotImplementedError
