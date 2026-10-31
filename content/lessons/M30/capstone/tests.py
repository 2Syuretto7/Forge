import numpy as np
import sub

X, Y = sub.make_data()


def test_dual_svm():
    a, w = sub.solve(X, Y, 1.0)
    assert np.allclose(w, X.T @ (a * Y))
    assert sub.kkt_residual(a, X, Y, 1.0) < 1e-4
    assert 0 <= sub.duality_gap(a, X, Y, 1.0) < 1e-5
    m = Y * (X @ w)
    tol = 1e-3
    assert np.all(m[a <= 1e-9] >= 1 - tol) and np.all(np.abs(m[(a > 1e-9) & (a < 1 - 1e-9)] - 1) <= tol) and np.all(m[a >= 1 - 1e-9] <= 1 + tol)
    assert np.mean(np.sign(X @ w) == Y) > 0.85


def test_kl_optimum():
    rng = np.random.default_rng(1)
    pi = rng.dirichlet(np.ones(8))
    r = rng.normal(size=8)
    for beta in (0.1, 1.0, 10.0):
        assert sub.check_kl_optimum(pi, r, beta, 1000, rng) <= 1e-12
        assert abs(sub.log_ratio_slope(pi, r, beta) - 1 / beta) < 1e-9
