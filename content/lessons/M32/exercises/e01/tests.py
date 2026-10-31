import numpy as np
import sub

W = np.array([[0.9, 0.1], [0.5, 0.5]])


def test_check():
    assert sub.check_stochastic(W)
    assert not sub.check_stochastic([[0.9, 0.2], [0.5, 0.5]])
    assert not sub.check_stochastic([[1.1, -0.1], [0.5, 0.5]])
    assert not sub.check_stochastic([[0.5, 0.5]])


def test_distributions():
    assert np.allclose(sub.distribution_after([1, 0], W, 1), [0.9, 0.1])
    assert np.allclose(sub.distribution_after([1, 0], W, 2), [0.86, 0.14])
    assert np.allclose(sub.distribution_after([0, 1], W, 200), [5 / 6, 1 / 6])


def test_simulate():
    path = sub.simulate(W, 1, 50000, np.random.default_rng(0))
    assert len(path) == 50001 and path[0] == 1 and set(np.unique(path)) <= {0, 1}
    assert abs(np.mean(path == 0) - 5 / 6) < 0.015
