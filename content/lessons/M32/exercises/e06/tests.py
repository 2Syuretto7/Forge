import math
import numpy as np
import sub


def test_correlated_gaussian():
    C = np.array([[1.0, 0.8], [0.8, 1.0]])
    Pr = np.linalg.inv(C)
    s, acc = sub.rw_metropolis(lambda x: -0.5 * x @ Pr @ x, [3.0, -3.0], 1.0, 40000, np.random.default_rng(0))
    s = s[2000:]
    assert s.shape == (38000, 2) and 0.2 < acc < 0.7
    assert np.max(np.abs(s.mean(axis=0))) < 0.1
    assert np.max(np.abs(np.cov(s.T) - C)) < 0.1


def gamma3(x):
    return 2 * math.log(x) - x if x > 0 else -math.inf


def test_hastings_correction_matters():
    q = (lambda r: r.exponential(3.0), lambda x: -x / 3 - math.log(3))
    good, _ = sub.independence_mh(gamma3, q[0], q[1], 1.0, 40000, np.random.default_rng(1))
    bad, _ = sub.independence_mh(gamma3, q[0], q[1], 1.0, 40000, np.random.default_rng(1), correct=False)
    assert abs(good.mean() - 3) < 0.1 and abs(good.var() - 3) < 0.3
    assert abs(bad.mean() - 2.25) < 0.1
