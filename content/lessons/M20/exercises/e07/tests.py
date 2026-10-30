import numpy as np
import sub

rng = np.random.default_rng(7)
expo = -np.log(1 - rng.random(200_000))


def test_density_estimate():
    c, d = sub.histogram_density(expo, 50, 0, 5)
    assert np.allclose(d[:10], np.exp(-c[:10]), rtol=0.05)


def test_deviation():
    assert sub.max_relative_deviation(expo, lambda x: np.exp(-x), 40, 0, 6) < 0.1
    assert sub.max_relative_deviation(expo, lambda x: 2 * np.exp(-2 * x), 40, 0, 6) > 0.3
