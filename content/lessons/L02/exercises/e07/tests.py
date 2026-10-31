import numpy as np
import sub

rng = np.random.default_rng(7)
X = rng.normal(size=(10, 30))
y = rng.normal(size=10)


def test_grad_mse_matches_finite_differences():
    w = rng.normal(size=30)
    g = sub.mse_grad(w, X, y)
    num = np.zeros(30)
    for j in range(30):
        e = np.zeros(30)
        e[j] = 1e-6
        num[j] = (sub.mse(w + e, X, y) - sub.mse(w - e, X, y)) / 2e-6
    assert np.linalg.norm(g - num) / (np.linalg.norm(g) + np.linalg.norm(num)) < 1e-5


def test_min_norm_interpolates_and_is_smallest():
    w = sub.min_norm(X, y)
    assert np.allclose(X @ w, y)
    v = rng.normal(size=30)
    v -= X.T @ np.linalg.solve(X @ X.T, X @ v)  # null-space component
    assert np.allclose(X @ (w + v), y)
    assert np.linalg.norm(w + v) > np.linalg.norm(w)


def test_gd_from_zero_finds_min_norm():
    lam = np.linalg.eigvalsh(2.0 / 10 * X @ X.T).max()
    w = sub.gd_from_zero(X, y, 0.9 / lam, 20000)
    assert np.allclose(w, sub.min_norm(X, y), atol=1e-6)
