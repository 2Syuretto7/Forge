import math
import numpy as np
import sub

W, M, S = np.array([0.4, 0.6]), np.array([-2.0, 1.5]), np.array([0.4, 0.6])


def exact_score(x, t):
    a = math.exp(-t)
    m, v = M * a, S**2 * a * a + 1 - a * a
    L = np.log(W) - 0.5 * np.log(v) - (x[:, None] - m) ** 2 / (2 * v)
    R = np.exp(L - L.max(axis=1, keepdims=True))
    R /= R.sum(axis=1, keepdims=True)
    return np.sum(R * (m - x[:, None]) / v, axis=1)


def test_grad_dsm_loss():
    rng = np.random.default_rng(0)
    X, y = rng.standard_normal(50), rng.standard_normal(50)
    c = rng.standard_normal(7)
    g = sub.grad_dsm_loss(c, X, y)
    h = 1e-6
    for j in range(7):
        e = np.zeros(7)
        e[j] = h
        assert abs((sub.dsm_loss(c + e, X, y) - sub.dsm_loss(c - e, X, y)) / (2 * h) - g[j]) < 1e-6


def test_learns_the_score():
    rng = np.random.default_rng(1)
    k = rng.choice(2, size=60000, p=W)
    x0 = M[k] + S[k] * rng.standard_normal(60000)
    X, y = sub.dsm_data(x0, 0.3, rng)
    c = sub.fit_score(X, y)
    grid = np.concatenate([np.linspace(-2.6, -1.0, 20), np.linspace(0.3, 2.4, 20)])
    err = sub.features(grid) @ c - exact_score(grid, 0.3)
    assert np.sqrt(np.mean(err**2)) < 0.3, np.sqrt(np.mean(err**2))
