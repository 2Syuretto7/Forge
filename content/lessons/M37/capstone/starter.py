import math
import numpy as np

WEIGHTS = np.array([0.3, 0.3, 0.4])
MEANS = np.array([[-2.0, 0.0], [2.0, 1.0], [0.0, -2.0]])


# provided
def sample_target(n, rng):
    k = rng.choice(3, size=n, p=WEIGHTS)
    return MEANS[k] + 0.35 * rng.standard_normal((n, 2))


# provided
def sliced_w1(X, Y, seed=0, n_proj=50):
    phi = np.random.default_rng(seed).uniform(0, np.pi, n_proj)
    D = np.stack([np.cos(phi), np.sin(phi)], axis=1)
    q = (np.arange(200) + 0.5) / 200
    return float(np.mean(np.abs(np.quantile(X @ D.T, q, axis=0) - np.quantile(Y @ D.T, q, axis=0))))


def kde_score(X, t, centres, h):
    """Score of the noised kernel density estimate."""
    raise NotImplementedError


def dsm_loss(score, x0, seed, T=5.0, n_t=8):
    """Sigma-weighted denoising score-matching loss averaged over times."""
    raise NotImplementedError


def fit(train, valid, hs=(0.0, 0.05, 0.1, 0.2, 0.4)):
    """Bandwidth with the smallest held-out loss."""
    raise NotImplementedError


def sample(train, h, n, seed=0, T=5.0, steps=60):
    """Reverse-time SDE with the kernel score."""
    raise NotImplementedError


def nn_distance(gen, train):
    """Median distance to the nearest training point."""
    raise NotImplementedError


# your answer
REPORT = """
"""
