import numpy as np
import sub


def test_gumbel_max_is_softmax():
    rng = np.random.default_rng(0)
    z = np.array([1.0, 0.0, -0.5, 2.0])
    p = np.exp(z) / np.exp(z).sum()
    a = sub.gumbel_max(z, 100000, rng)
    assert np.max(np.abs(np.bincount(a, minlength=4) / 100000 - p)) < 0.005


def test_temperature():
    rng = np.random.default_rng(1)
    z = np.array([1.0, 0.0, -0.5, 2.0])
    cold = sub.gumbel_softmax(z, 0.1, 5000, rng)
    hot = sub.gumbel_softmax(z, 10.0, 5000, rng)
    assert np.allclose(cold.sum(axis=1), 1) and sub.mean_max_entry(cold) > 0.95
    assert sub.mean_max_entry(hot) < 0.35
