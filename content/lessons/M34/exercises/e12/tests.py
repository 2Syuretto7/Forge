import numpy as np
import sub


def test_law_fits_and_improves():
    rng = np.random.default_rng(0)
    d = sub.ks_for_sizes([50, 500], 0.25, rng)
    assert d[1] < 0.03 and d[1] < d[0], d


def test_wrong_law_fails():
    rng = np.random.default_rng(1)
    X = rng.standard_normal((2000, 500)) * np.sqrt(np.linspace(0.5, 1.5, 500))
    assert sub.ks_distance(np.linalg.eigvalsh(X.T @ X / 2000), 0.25) > 0.05
    assert abs(sub.mp_cdf(np.array([1.0]), 0.25)[0] - 0.5) < 0.2
