import numpy as np
import sub

rng = np.random.default_rng(2)


def test_running_mean():
    assert np.allclose(sub.running_mean([2, 4, 6, 0]), [2, 3, 4, 3])
    x = rng.exponential(size=100000)
    assert abs(sub.running_mean(x)[-1] - 1) < 0.01


def test_far_averages_become_rare():
    fr = []
    for n in (100, 1000, 10000):
        flips = (rng.random((2000, n)) < 0.5).astype(float)
        f = sub.fraction_far(flips, 0.5, 0.02)
        assert f <= min(1.0, 0.25 / (n * 0.02**2))
        fr.append(f)
    assert fr[0] > 0.5 and fr[2] < 0.001 and fr[0] > fr[1] > fr[2]


def test_chebyshev_n():
    assert sub.chebyshev_n(0.25, 0.01, 0.05) == 50000
    assert sub.chebyshev_n(1.0, 0.1, 0.5) == 200
