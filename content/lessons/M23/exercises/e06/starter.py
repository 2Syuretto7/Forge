import numpy as np


def _blocks(Sigma, obs):
    raise NotImplementedError


def regression_slope(mu, Sigma, obs):
    """Sigma_ab Sigma_bb^{-1}."""
    raise NotImplementedError


def condition(mu, Sigma, obs, x_obs):
    """Mean and covariance of the unobserved coordinates given the observed ones."""
    raise NotImplementedError
