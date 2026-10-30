import numpy as np


def box_muller(u1, u2):
    """Two independent standard normals from two uniforms."""
    r = np.sqrt(-2 * np.log(u1))
    return r * np.cos(2 * np.pi * u2), r * np.sin(2 * np.pi * u2)


def sample_normal(n, seed=0):
    """n standard normals."""
    rng = np.random.default_rng(seed)
    m = (n + 1) // 2
    x, y = box_muller(1 - rng.random(m), rng.random(m))
    return np.concatenate([x, y])[:n]


def check_moments(z):
    """(mean, variance, fraction within one standard deviation)."""
    return float(np.mean(z)), float(np.var(z)), float(np.mean(np.abs(z) < 1))
