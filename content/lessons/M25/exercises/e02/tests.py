import numpy as np
import sub


def test_estimators():
    x = np.array([0.5, 1.5, 1.0, 1.0])
    assert abs(sub.rate_mle(x) - 1.0) < 1e-12 and abs(sub.rate_unbiased(x) - 0.75) < 1e-12


def test_bias():
    b_mle, b_unb = sub.simulate_rate_bias(5, 2.0, 200000, seed=3)
    se = 2.0 * 5 / 4 / np.sqrt(3) / np.sqrt(200000)
    assert abs(b_mle - 0.5) < 5 * se, b_mle
    assert abs(b_unb) < 5 * se, b_unb


def test_bias_shrinks_like_one_over_n():
    b5, _ = sub.simulate_rate_bias(5, 1.0, 100000, seed=4)
    b50, _ = sub.simulate_rate_bias(50, 1.0, 100000, seed=5)
    assert abs(b5 - 0.25) < 0.02 and abs(b50 - 1 / 49) < 0.005
