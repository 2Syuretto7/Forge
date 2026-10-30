import numpy as np
import sub

rng = np.random.default_rng(11)


def test_iqr():
    assert abs(sub.iqr(np.arange(101)) - 50) < 1e-12


def test_gaussian_means_concentrate():
    a = sub.spread_of_means(rng.normal(size=(4000, 10)))
    b = sub.spread_of_means(rng.normal(size=(4000, 1000)))
    assert 7 < a / b < 13, f"ratio {a / b:.2f}, expected about 10"


def test_cauchy_means_do_not_concentrate():
    a = sub.spread_of_means(rng.standard_cauchy(size=(4000, 10)))
    b = sub.spread_of_means(rng.standard_cauchy(size=(4000, 1000)))
    assert abs(b - 2.0) < 0.3, f"IQR of Cauchy means at n=1000 is {b:.2f}; theory says 2"
    assert b > 0.7 * a


def test_cauchy_medians_still_concentrate():
    a = sub.spread_of_medians(rng.standard_cauchy(size=(4000, 10)))
    b = sub.spread_of_medians(rng.standard_cauchy(size=(4000, 1000)))
    assert a / b > 6
