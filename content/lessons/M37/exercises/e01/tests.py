import math
import numpy as np
import sub


def test_brownian():
    W = sub.brownian_paths(20000, 2.0, 100, np.random.default_rng(0))
    assert W.shape == (20000, 101) and np.all(W[:, 0] == 0)
    assert abs(W[:, -1].var() / 2.0 - 1) < 0.04
    assert abs(np.corrcoef(W[:, 50], W[:, 100] - W[:, 50])[0, 1]) < 0.03


def test_geometric_brownian_motion():
    x = sub.euler_maruyama(lambda x, t: 0.3 * x, lambda x, t: 0.4 * x, 1.0, 1.0, 200, 40000, np.random.default_rng(1))
    assert abs(x.mean() / math.exp(0.3) - 1) < 0.02
