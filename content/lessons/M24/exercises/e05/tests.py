import math
import numpy as np
import sub

rng = np.random.default_rng(8)


def test_normal_cdf_values():
    assert np.allclose(sub.normal_cdf(np.array([0.0, 1.96, -1.0])), [0.5, 0.9750021, 0.1586553], atol=1e-6)


def test_standardization():
    s = np.array([[1.0, 3.0], [2.0, 2.0]])
    assert np.allclose(sub.standardized_means(s, 2.0, 1.0), [0.0, 0.0])
    s2 = np.array([[3.0, 3.0, 3.0, 3.0]])
    assert np.allclose(sub.standardized_means(s2, 2.0, 2.0), [1.0])


def test_ks_of_exact_normal_quantiles_is_small():
    m = 1000
    # midpoints of the probability grid mapped through an accurate inverse CDF approximation
    p = (np.arange(m) + 0.5) / m
    z = np.sqrt(2) * np.array([_erfinv(2 * q - 1) for q in p])
    assert sub.ks_distance(z) < 0.002


def _erfinv(y):
    lo, hi = -6.0, 6.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if math.erf(mid) < y:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def test_clt_for_uniform_means():
    u = rng.uniform(size=(20000, 30))
    z = sub.standardized_means(u, 0.5, 1 / math.sqrt(12))
    assert sub.ks_distance(z) < 0.02


def test_skewed_single_draws_are_far_from_normal():
    e = rng.exponential(size=(20000, 1))
    z = sub.standardized_means(e, 1.0, 1.0)
    assert sub.ks_distance(z) > 0.1
    z30 = sub.standardized_means(rng.exponential(size=(20000, 30)), 1.0, 1.0)
    assert sub.ks_distance(z30) < sub.ks_distance(z) / 3
