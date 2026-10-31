import math
import numpy as np


# provided
def simulate_target(n, seed=0):
    rng = np.random.default_rng(seed)
    x = np.zeros(n)
    pos, vel = 0.0, 1.0
    for t in range(n):
        a = 0.02 * rng.standard_normal()
        pos += vel + 0.5 * a
        vel += a
        x[t] = pos
    return x, x + rng.standard_normal(n)


def sample(mu, Sigma, n, rng):
    """n samples of N(mu, Sigma)."""
    raise NotImplementedError


def logpdf(X, mu, Sigma):
    """Log-density at each row of X."""
    raise NotImplementedError


def condition(mu, Sigma, obs, x_obs):
    """Conditional mean and covariance of the unobserved coordinates."""
    raise NotImplementedError


def track(z, accel_sd=0.02, meas_sd=1.0):
    """Kalman filter for position and velocity; returns filtered positions."""
    raise NotImplementedError
