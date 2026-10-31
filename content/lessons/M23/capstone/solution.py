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
    L = np.linalg.cholesky(np.asarray(Sigma, dtype=float))
    return np.asarray(mu, dtype=float) + rng.standard_normal((n, len(mu))) @ L.T


def logpdf(X, mu, Sigma):
    """Log-density at each row of X."""
    X = np.atleast_2d(np.asarray(X, dtype=float))
    L = np.linalg.cholesky(np.asarray(Sigma, dtype=float))
    Z = np.linalg.solve(L, (X - mu).T)
    return -0.5 * np.sum(Z * Z, axis=0) - np.sum(np.log(np.diag(L))) - 0.5 * X.shape[1] * math.log(2 * math.pi)


def condition(mu, Sigma, obs, x_obs):
    """Conditional mean and covariance of the unobserved coordinates."""
    mu, Sigma = np.asarray(mu, dtype=float), np.asarray(Sigma, dtype=float)
    rest = [i for i in range(len(mu)) if i not in obs]
    Sab = Sigma[np.ix_(rest, obs)]
    B = np.linalg.solve(Sigma[np.ix_(obs, obs)], Sab.T).T
    return mu[rest] + B @ (np.asarray(x_obs, dtype=float) - mu[obs]), Sigma[np.ix_(rest, rest)] - B @ Sab.T


def track(z, accel_sd=0.02, meas_sd=1.0):
    """Kalman filter for position and velocity; returns filtered positions."""
    F = np.array([[1.0, 1.0], [0.0, 1.0]])
    g = np.array([0.5, 1.0])
    Q = accel_sd**2 * np.outer(g, g)
    R = meas_sd**2
    m = np.array([z[0], 0.0])
    P = np.diag([R, 100.0])
    out = np.zeros(len(z))
    for t, zt in enumerate(z):
        if t > 0:
            m = F @ m
            P = F @ P @ F.T + Q
        K = P[:, 0] / (P[0, 0] + R)
        m = m + K * (zt - m[0])
        P = P - np.outer(K, P[0, :])
        out[t] = m[0]
    return out
