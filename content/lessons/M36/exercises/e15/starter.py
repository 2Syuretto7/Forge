import numpy as np


def kl_optimal(pi_ref, r_hat, beta):
    """pi_ref exp(r_hat / beta), normalized."""
    raise NotImplementedError


def kl(p, q):
    """KL divergence of p from q."""
    raise NotImplementedError


def true_reward(pi, r):
    """Expected true reward."""
    raise NotImplementedError


def sweep(pi_ref, r_hat, r, betas):
    """(true reward, KL) of the regularized optimum for each beta."""
    raise NotImplementedError
