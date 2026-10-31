import numpy as np


# provided
def make_noise(seed=0):
    return np.random.default_rng(seed).uniform(0.1, 3.0, size=10**5)


def allocation(noise, nu):
    """Water-filling allocation at level nu."""
    return np.maximum(0.0, nu - np.asarray(noise, dtype=float))


def water_level(noise, P):
    """The level at which the allocation uses the whole budget."""
    noise = np.asarray(noise, dtype=float)
    lo, hi = noise.min(), noise.min() + P
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if allocation(noise, mid).sum() < P:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def kkt_check(noise, x, nu):
    """Largest violation of dual feasibility and complementary slackness."""
    noise, x = np.asarray(noise, dtype=float), np.asarray(x, dtype=float)
    mu = 1 / nu - 1 / (noise + x)
    return float(max(np.max(np.maximum(-mu, 0)), np.max(np.abs(mu * x))))
