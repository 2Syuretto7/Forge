import numpy as np
import sub

rng = np.random.default_rng(1)
X = np.column_stack([np.ones(50), rng.normal(size=(50, 2))])
w_true = np.array([1.0, -2.0, 0.5])
y = X @ w_true + 0.3 * rng.normal(size=50)


def test_ols_matches_normal_equations():
    assert np.allclose(sub.ols(X, y), np.linalg.solve(X.T @ X, X.T @ y))


def test_ols_minimizes_the_gaussian_nll():
    w = sub.ols(X, y)
    for sigma in [0.1, 0.3, 2.0]:
        base = sub.gaussian_nll(w, sigma, X, y)
        for _ in range(20):
            assert sub.gaussian_nll(w + 0.01 * rng.normal(size=3), sigma, X, y) > base


def test_noise_mle_maximizes_likelihood():
    w = sub.ols(X, y)
    s2 = sub.noise_mle(X, y, w)
    best = sub.gaussian_nll(w, np.sqrt(s2), X, y)
    for f in [0.8, 0.95, 1.05, 1.2]:
        assert sub.gaussian_nll(w, np.sqrt(s2 * f), X, y) > best
    assert abs(np.sqrt(s2) - 0.3) < 0.1
