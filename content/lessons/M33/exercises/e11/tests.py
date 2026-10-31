import numpy as np
import sub


def data():
    rng = np.random.default_rng(0)
    X = rng.standard_normal((5000, 150)) * np.linspace(0.2, 3, 150)
    return X, X @ rng.standard_normal(150) + rng.standard_normal(5000)


def test_grad_ridge_loss():
    rng = np.random.default_rng(1)
    X, y = rng.standard_normal((30, 5)), rng.standard_normal(30)
    w = rng.standard_normal(5)
    g = sub.grad_ridge_loss(w, X, y, 0.7)
    h = 1e-6
    for i in range(5):
        e = np.zeros(5)
        e[i] = h
        assert abs((sub.ridge_loss(w + e, X, y, 0.7) - sub.ridge_loss(w - e, X, y, 0.7)) / (2 * h) - g[i]) < 1e-6


def test_cg_matches_direct():
    X, y = data()
    counts = []
    for lam in (1.0, 1e4):
        w, k = sub.ridge_cg(X, y, lam)
        assert np.max(np.abs(w - sub.ridge_direct(X, y, lam))) < 1e-7 * (1 + np.max(np.abs(w)))
        assert np.max(np.abs(sub.grad_ridge_loss(w, X, y, lam))) < 1e-6 * np.linalg.norm(X.T @ y)
        counts.append(k)
    assert counts[1] < counts[0] <= 150, counts
