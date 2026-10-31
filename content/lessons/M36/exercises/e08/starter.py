import numpy as np


def policy(theta):
    """Row-wise softmax of the logits."""
    raise NotImplementedError


def _values(P, R, theta, gamma):
    raise NotImplementedError


def objective(P, R, theta, rho0, gamma):
    """Expected discounted return from the start distribution."""
    raise NotImplementedError


def policy_gradient(P, R, theta, rho0, gamma):
    """Exact policy gradient for a tabular softmax policy."""
    raise NotImplementedError
