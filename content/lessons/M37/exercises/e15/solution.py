import math
import numpy as np


def kde_score(X, t, centres, h):
    """Score of the noised kernel density estimate."""
    a = math.exp(-t)
    v = a * a * h * h + 1 - a * a
    d = np.asarray(X)[:, None, :] - a * np.asarray(centres)[None]
    L = -np.sum(d * d, axis=2) / (2 * v)
    R = np.exp(L - L.max(axis=1, keepdims=True))
    R /= R.sum(axis=1, keepdims=True)
    return -np.einsum("nk,nkd->nd", R, d) / v


def generate(train, h, n, rng, steps=80, tmin=1e-4):
    """Reverse sampling with the kernel score."""
    ts = np.geomspace(4.0, tmin, steps + 1)
    x = rng.standard_normal((n, 2))
    for i in range(steps):
        dt = ts[i] - ts[i + 1]
        x = x + dt * (x + 2 * kde_score(x, ts[i], train, h)) + math.sqrt(2 * dt) * rng.standard_normal((n, 2))
    return x


def nn_distance(gen, train):
    """Median distance from generated points to the nearest training point."""
    d = np.linalg.norm(np.asarray(gen)[:, None, :] - np.asarray(train)[None], axis=2)
    return float(np.median(d.min(axis=1)))
