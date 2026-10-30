import math
import numpy as np
import sub


def test_moments():
    z = sub.sample_normal(400_001)
    assert z.size == 400_001
    m, v, f = sub.check_moments(z)
    assert abs(m) < 0.01 and abs(v - 1) < 0.01 and abs(f - math.erf(1 / math.sqrt(2))) < 0.005


def test_independence():
    rng = np.random.default_rng(3)
    x, y = sub.box_muller(1 - rng.random(200_000), rng.random(200_000))
    assert abs(np.corrcoef(x, y)[0, 1]) < 0.01
    assert abs(np.mean(x * x * y * y) - 1) < 0.05
