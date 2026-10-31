import numpy as np
import sub

rng = np.random.default_rng(9)


def test_resample_means_shape_and_center():
    x = rng.normal(5, 2, size=50)
    m = sub.bootstrap_means(x, 2000, seed=1)
    assert m.shape == (2000,)
    assert abs(m.mean() - x.mean()) < 0.05


def test_interval_width_matches_standard_error():
    x = rng.normal(0, 3, size=100)
    lo, hi = sub.percentile_ci(sub.bootstrap_means(x, 4000, seed=2), 0.95)
    expected = 2 * 1.96 * x.std() / np.sqrt(100)
    assert abs((hi - lo) / expected - 1) < 0.12
    assert lo < x.mean() < hi


def test_coverage_is_near_nominal():
    data = rng.exponential(1.0, size=(300, 40))
    c = sub.coverage(1.0, data, B=400, level=0.95, seed=0)
    assert 0.88 <= c <= 0.98, f"coverage {c:.3f}"
