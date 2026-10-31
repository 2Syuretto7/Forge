import numpy as np
import sub

R = np.array([0.3, 1.2, -0.7, 1.2, 0.9])


def test_naive_overflows():
    assert np.any(np.isnan(sub.naive_gibbs(R, 1e-3)))


def test_limits():
    assert np.allclose(sub.stable_gibbs(R, 1e-4), sub.limit_low(R))
    assert np.allclose(sub.limit_low(R), [0, 0.5, 0, 0.5, 0])
    assert np.allclose(sub.stable_gibbs(R, 1e12), sub.limit_high(R))
    p = sub.stable_gibbs(R, 1.0)
    assert np.allclose(p, sub.naive_gibbs(R, 1.0)) and abs(p.sum() - 1) < 1e-12
