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


def dsm_loss(score, x0, rng, T=5.0, n_t=8):
    """Sigma-weighted denoising score-matching loss averaged over times."""
    total = 0.0
    for t in np.geomspace(0.01, T, n_t):
        a = math.exp(-t)
        s = math.sqrt(1 - a * a)
        eps = rng.standard_normal(np.shape(x0))
        xt = a * np.asarray(x0) + s * eps
        total += float(np.mean(np.sum((s * score(xt, t) + eps) ** 2, axis=1)))
    return total / n_t


def choose_bandwidth(train, valid, hs, rng):
    """Bandwidth with the smallest held-out score-matching loss."""
    seed = int(rng.integers(1 << 30))
    losses = [dsm_loss(lambda x, t: kde_score(x, t, train, h), valid, np.random.default_rng(seed)) for h in hs]
    return hs[int(np.argmin(losses))], losses
