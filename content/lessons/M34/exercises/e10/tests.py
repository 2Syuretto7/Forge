import numpy as np
import sub


def test_spread_tracks_theory():
    rng = np.random.default_rng(0)
    X = rng.standard_normal((20000, 128))
    t = sub.distortion_table(X, [8, 16, 32, 64], 5000, rng)
    for k, (sd, q99) in t.items():
        assert abs(sd / np.sqrt(2 / k) - 1) < 0.12, (k, sd)
        assert 2.4 * sd < q99 < 3.6 * sd
    i, j = sub.sample_pairs(10, 1000, rng)
    assert np.all(i != j) and i.max() < 10 and j.max() < 10
