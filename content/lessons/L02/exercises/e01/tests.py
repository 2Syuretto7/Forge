import numpy as np
import sub


def test_design():
    D = sub.design(np.array([2.0, 3.0]), 2)
    assert np.allclose(D, [[1, 2, 4], [1, 3, 9]])


def test_exact_recovery_of_a_polynomial():
    x = np.linspace(-1, 1, 12)
    y = 1 - 2 * x + 0.5 * x ** 3
    c = sub.fit_poly(x, y, 3)
    assert np.allclose(c, [1, -2, 0, 0.5], atol=1e-10)
    assert sub.mse(sub.predict(c, x), y) < 1e-20


def test_interpolation_at_degree_n_minus_1():
    rng = np.random.default_rng(1)
    x = np.sort(rng.uniform(-1, 1, 8))
    y = rng.normal(size=8)
    c = sub.fit_poly(x, y, 7)
    assert sub.mse(sub.predict(c, x), y) < 1e-12
