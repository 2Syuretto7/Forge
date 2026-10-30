import numpy as np
import sub

rng = np.random.default_rng(0)


def test_bounds():
    for _ in range(300):
        z = rng.normal(size=rng.integers(1, 50)) * rng.uniform(0.1, 100)
        assert sub.bounds_hold(z)
    z = np.full(7, 3.0)
    assert abs(sub.lse(z) - (3 + np.log(7))) < 1e-12


def test_shifts():
    for _ in range(100):
        z = rng.normal(size=10) * 20
        assert sub.shift_is_exact(z, [-2000, -500, -50, 0, 13.7, z.max(), 500, 2000])


def test_unusable_shift_is_skipped():
    z = np.array([0.0, 1.0])
    assert sub.shift_is_exact(z, [-1000.0])
