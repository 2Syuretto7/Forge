import numpy as np
import sub


def test_action_dependent_baselines():
    rng = np.random.default_rng(0)
    z = np.array([0.4, -0.3, 0.1])
    r = np.array([2.0, -1.0, 0.5])
    p = np.exp(z) / np.exp(z).sum()
    exact = p * (r - p @ r)
    assert sub.bias(z, r, lambda a: 0.7, 200000, rng) < 0.02
    half = sub.estimates(z, r, 200000, rng, lambda a: 0.5 * r[a]).mean(axis=0)
    assert np.max(np.abs(half - 0.5 * exact)) < 0.02
    zero = sub.estimates(z, r, 1000, rng, lambda a: r[a])
    assert np.max(np.abs(zero)) == 0.0
    assert abs(sub.bias(z, r, lambda a: r[a], 1000, rng) - np.max(np.abs(exact))) < 1e-12
