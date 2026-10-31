import numpy as np
import sub


def test_sign_pair():
    x, y = sub.sign_pair(200000, np.random.default_rng(15))
    assert abs(sub.correlation(x, y)) < 0.01
    assert abs(y.std() - 1) < 0.01
    assert sub.square_correlation(x, y) > 0.999
    assert abs(sub.zero_sum_fraction(x, y) - 0.5) < 0.005


def test_jointly_gaussian_uncorrelated_pair_is_independent():
    rng = np.random.default_rng(16)
    x, y = rng.standard_normal(200000), rng.standard_normal(200000)
    assert abs(sub.square_correlation(x, y)) < 0.01
    assert sub.zero_sum_fraction(x, y) == 0.0
