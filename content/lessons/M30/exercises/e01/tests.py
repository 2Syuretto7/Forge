import numpy as np
import sub

rng = np.random.default_rng(1)
A = rng.normal(size=(3, 6))
B = rng.normal(size=3)


def test_pinv_and_stationarity():
    x, lam = sub.min_norm(A, B)
    assert np.allclose(x, np.linalg.pinv(A) @ B)
    assert np.allclose(A @ x, B)
    assert sub.check_stationarity(A, x, lam) < 1e-12


def test_null_space_makes_it_longer():
    x, _ = sub.min_norm(A, B)
    for _ in range(10):
        v = rng.normal(size=6)
        z = v - A.T @ np.linalg.solve(A @ A.T, A @ v)
        assert np.allclose(A @ (x + z), B)
        assert np.linalg.norm(x + z) > np.linalg.norm(x)


def test_multiplier_is_a_sensitivity():
    _, lam = sub.min_norm(A, B)
    h = 1e-6
    for i in range(3):
        e = np.zeros(3)
        e[i] = h
        fp = 0.5 * np.sum(sub.min_norm(A, B + e)[0] ** 2)
        fm = 0.5 * np.sum(sub.min_norm(A, B - e)[0] ** 2)
        assert abs((fp - fm) / (2 * h) + lam[i]) < 1e-6
