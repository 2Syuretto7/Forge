import numpy as np
import sub


def test_interval():
    lo, hi = sub.normal_interval([1.0, 2.0, 3.0, 4.0])
    h = 1.96 * np.std([1, 2, 3, 4], ddof=1) / 2
    assert abs(lo - (2.5 - h)) < 1e-12 and abs(hi - (2.5 + h)) < 1e-12


def test_coverage_near_95():
    c = sub.coverage(lambda r, s: r.exponential(size=s), 1.0, 200, 4000, np.random.default_rng(7))
    assert 0.93 < c < 0.965, c
    g = sub.coverage(lambda r, s: r.normal(size=s), 0.0, 50, 4000, np.random.default_rng(8))
    assert 0.935 < g < 0.965, g


def test_sample_size():
    assert sub.n_for_halfwidth(1.0, 0.01) == 38416
    assert sub.n_for_halfwidth(2.0, 0.5, z=2.0) == 64
