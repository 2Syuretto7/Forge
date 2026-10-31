import numpy as np
import sub

A = np.array([[1e-20, 1.0], [1.0, 1.0]])
B = np.array([1.0, 2.0])


def test_tiny_pivot():
    x = sub.solve_no_pivot(A, B)
    assert x[0] == 0.0 and abs(x[1] - 1) < 1e-15
    y = sub.solve_partial_pivot(A, B)
    assert np.allclose(y, [1, 1], atol=1e-15)


def test_growth():
    assert sub.growth_factor(A, False) > 1e19
    assert sub.growth_factor(A, True) <= 2


def test_random_systems_agree_with_numpy():
    rng = np.random.default_rng(15)
    M = rng.normal(size=(6, 6))
    v = rng.normal(size=6)
    assert np.allclose(sub.solve_partial_pivot(M, v), np.linalg.solve(M, v))
