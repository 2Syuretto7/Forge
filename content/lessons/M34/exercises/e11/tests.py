import numpy as np
import sub


def test_contrast_vanishes():
    rng = np.random.default_rng(0)
    c2 = sub.relative_contrast(2, 1000, rng)
    c1000 = sub.relative_contrast(1000, 1000, rng)
    assert c2 > 10 and c1000 < 0.5, (c2, c1000)


def test_distance_statistics():
    rng = np.random.default_rng(1)
    for d in (10, 400):
        x, y = rng.random((5000, d)), rng.random((5000, d))
        assert abs(np.mean(np.sum((x - y) ** 2, axis=1)) / sub.expected_sq_distance(d) - 1) < 0.03
    ratio = sub.distance_cv(25, 5000, rng) / sub.distance_cv(400, 5000, rng)
    assert 3.3 < ratio < 4.8, ratio
