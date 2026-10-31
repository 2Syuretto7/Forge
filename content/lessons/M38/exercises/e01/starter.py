import numpy as np


def kl_optimal(ref_logp, r, beta):
    """Log-probabilities of the KL-regularized optimum."""
    raise NotImplementedError


def implied_reward(logp, ref_logp, beta):
    """Reward implied by a policy, up to a constant."""
    raise NotImplementedError


def same_up_to_constant(a, b, tol=1e-9):
    """Whether a - b is constant."""
    raise NotImplementedError
