import bisect
import numpy as np


def discounted_return(rewards, gamma):
    """Sum of gamma^t r_t."""
    raise NotImplementedError


def chain_of(P, R, pi):
    """Transition matrix and expected reward of the chain a policy induces."""
    raise NotImplementedError


def policy_evaluation(P, R, pi, gamma):
    """Exact value of a policy."""
    raise NotImplementedError


def mc_value(P, R, pi, gamma, s0, episodes, horizon, rng):
    """Monte Carlo estimate of V(s0)."""
    raise NotImplementedError
