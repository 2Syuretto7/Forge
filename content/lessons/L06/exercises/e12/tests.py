import numpy as np
import sub

rng = np.random.default_rng(12)
X = rng.normal(size=(40, 8)) * np.array([3, 2, 1, 1, 0.5, 0.3, 0.1, 0.05])


def test_two_formulas_agree():
    for lam in [0.0, 0.1, 1.0, 10.0]:
        assert abs(sub.df_svd(X, lam) - sub.df_trace(X, lam)) < 1e-8


def test_limits_and_monotonicity():
    assert abs(sub.df_svd(X, 0.0) - 8) < 1e-10
    vals = [sub.df_svd(X, lam) for lam in [0.01, 0.1, 1, 10, 100, 1e4]]
    assert all(a > b for a, b in zip(vals, vals[1:]))
    assert vals[-1] < 0.1


def test_grad_df_lambda_matches_finite_differences():
    for lam in [0.05, 1.0, 20.0]:
        h = 1e-6 * max(1.0, lam)
        num = (sub.df_svd(X, lam + h) - sub.df_svd(X, lam - h)) / (2 * h)
        g = sub.ddf_dlam(X, lam)
        assert abs(g - num) / (abs(g) + abs(num)) < 1e-5
