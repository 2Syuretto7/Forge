import numpy as np
import sub

rng = np.random.default_rng(6)
X = rng.normal(size=(2000, 5))
Y = X @ np.array([1.0, 2.0, -1.0, 0.5, 0.0]) + rng.normal(size=2000)


def test_floor_scales_with_step():
    a = sub.excess_floor(X, Y, 0.02, 1, np.random.default_rng(1))
    b = sub.excess_floor(X, Y, 0.01, 1, np.random.default_rng(2))
    assert 1.5 < a / b < 2.6, (a, b)


def test_floor_scales_with_batch():
    a = sub.excess_floor(X, Y, 0.02, 1, np.random.default_rng(3))
    b = sub.excess_floor(X, Y, 0.02, 10, np.random.default_rng(4))
    assert a / b > 5, (a, b)


def test_converges_from_far():
    w, losses = sub.sgd(X, Y, np.full(5, 5.0), 0.01, 3000, 8, np.random.default_rng(5))
    assert losses[-1] < 0.6 and losses[0] > 10
