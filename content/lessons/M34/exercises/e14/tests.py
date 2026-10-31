import numpy as np
import sub


def test_compounding():
    rng = np.random.default_rng(0)
    he = sub.forward_second_moments(50, 128, 1.0, rng)
    assert 0.2 < he[-1] / he[0] < 5
    for c in (0.5, 2.0):
        m = sub.forward_second_moments(50, 128, c, rng)
        ratio = m[-1] / m[0] * c
        assert abs(np.log10(ratio) - np.log10(sub.predicted_ratio(c, 50))) < 1.5, (c, ratio)
    assert sub.predicted_ratio(0.5, 50) < 1e-14
