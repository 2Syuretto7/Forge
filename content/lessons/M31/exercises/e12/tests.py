import numpy as np
import sub


def test_constant_sd_and_shrinking_relative_spread():
    rng = np.random.default_rng(12)
    for d in (10, 100, 1000):
        sd = sub.norms(d, 4000, rng).std()
        assert abs(sd - 1 / np.sqrt(2)) < 0.05, (d, sd)
    a = sub.relative_spread(16, 8000, rng)
    b = sub.relative_spread(1024, 8000, rng)
    assert abs(a / b - 8) < 0.8


def test_thin_shell():
    rng = np.random.default_rng(13)
    assert sub.fraction_in_shell(1000, 4000, rng) > 0.999
    assert sub.fraction_in_shell(2, 4000, rng) < 0.2
