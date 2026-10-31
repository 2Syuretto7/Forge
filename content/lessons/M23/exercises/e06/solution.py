import numpy as np


def _blocks(Sigma, obs):
    Sigma = np.asarray(Sigma, dtype=float)
    rest = [i for i in range(Sigma.shape[0]) if i not in obs]
    return rest, Sigma[np.ix_(rest, rest)], Sigma[np.ix_(rest, obs)], Sigma[np.ix_(obs, obs)]


def regression_slope(mu, Sigma, obs):
    """Sigma_ab Sigma_bb^{-1}."""
    rest, Saa, Sab, Sbb = _blocks(Sigma, obs)
    return np.linalg.solve(Sbb, Sab.T).T


def condition(mu, Sigma, obs, x_obs):
    """Mean and covariance of the unobserved coordinates given the observed ones."""
    mu = np.asarray(mu, dtype=float)
    rest, Saa, Sab, Sbb = _blocks(Sigma, obs)
    B = regression_slope(mu, Sigma, obs)
    mean = mu[rest] + B @ (np.asarray(x_obs, dtype=float) - mu[obs])
    return mean, Saa - B @ Sab.T
