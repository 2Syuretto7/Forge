import numpy as np
import sub


def test_no_oversampling_hurts():
    rng = np.random.default_rng(0)
    A = sub.make_matrix(1000, 200, 0.5, rng)
    s = 1 / np.sqrt(np.arange(1, 201))
    bad = np.mean([sub.spectral_error_ratio(A, s, 10, 0, 0, rng) for _ in range(3)])
    good = np.mean([sub.spectral_error_ratio(A, s, 10, 10, 2, rng) for _ in range(3)])
    assert bad > 1.6 and good < 1.15, (bad, good)
    fro_bad = sub.rsvd_error_ratio(A, s, 10, 0, 0, rng)
    assert 1.0 < fro_bad < 1.35
