import numpy as np


def kl_optimal(ref_logp, r, beta):
    """Log-probabilities of the KL-regularized optimum."""
    s = np.asarray(ref_logp) + np.asarray(r) / beta
    m = s.max()
    return s - m - np.log(np.sum(np.exp(s - m)))


def implied_reward(logp, ref_logp, beta):
    """Reward implied by a policy, up to a constant."""
    return beta * (np.asarray(logp) - np.asarray(ref_logp))


def same_up_to_constant(a, b, tol=1e-9):
    """Whether a - b is constant."""
    d = np.asarray(a) - np.asarray(b)
    return bool(np.max(d) - np.min(d) < tol)
