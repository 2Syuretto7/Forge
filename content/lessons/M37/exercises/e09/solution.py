import math
import numpy as np


def _log_resp(X, w, M, s):
    d = np.asarray(X)[:, None, :] - np.asarray(M)[None]
    L = np.log(w)[None] - np.sum(d * d, axis=2) / (2 * s * s) - np.log(2 * np.pi * s * s)
    return L, d


def mixture2d_logpdf(X, w, M, s):
    """Log density of an isotropic two-dimensional Gaussian mixture."""
    L, _ = _log_resp(X, w, M, s)
    mx = L.max(axis=1, keepdims=True)
    return (mx + np.log(np.sum(np.exp(L - mx), axis=1, keepdims=True)))[:, 0]


def mixture2d_score(X, w, M, s):
    """Gradient of the log density."""
    L, d = _log_resp(X, w, M, s)
    R = np.exp(L - L.max(axis=1, keepdims=True))
    R /= R.sum(axis=1, keepdims=True)
    return -np.einsum("nk,nkd->nd", R, d) / (s * s)


def noised_score(X, t, w, M, s):
    """Exact score of the noised mixture at time t."""
    a = math.exp(-t)
    return mixture2d_score(X, w, np.asarray(M) * a, math.sqrt(s * s * a * a + 1 - a * a))


def reverse_sample_2d(score, n, T, steps, rng, tmin=1e-3):
    """Reverse-time SDE in two dimensions."""
    ts = np.geomspace(T, tmin, steps + 1)
    x = rng.standard_normal((n, 2))
    for i in range(steps):
        h = ts[i] - ts[i + 1]
        x = x + h * (x + 2 * score(x, ts[i])) + math.sqrt(2 * h) * rng.standard_normal((n, 2))
    return x


def sliced_w1(X, Y, rng, n_proj=50):
    """Sliced Wasserstein-1 distance from matching quantiles."""
    phi = rng.uniform(0, np.pi, n_proj)
    D = np.stack([np.cos(phi), np.sin(phi)], axis=1)
    q = (np.arange(200) + 0.5) / 200
    return float(np.mean(np.abs(np.quantile(X @ D.T, q, axis=0) - np.quantile(Y @ D.T, q, axis=0))))
