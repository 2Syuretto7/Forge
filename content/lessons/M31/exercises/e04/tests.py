import math
import numpy as np
import sub


def test_best_of_1000():
    rng = np.random.default_rng(4)
    best = [sub.best_of_random(1000, 1000, rng) for _ in range(5)]
    assert all(0.53 < b < 0.5 + sub.union_epsilon(1000, 1000, 0.05) for b in best), best
    assert abs(sub.union_epsilon(1000, 1, 0.05) - 0.04295) < 1e-4


def test_grows_with_log_k():
    rng = np.random.default_rng(5)
    e10 = sub.expected_excess(10, 1000, 40, rng)
    e1000 = sub.expected_excess(1000, 1000, 10, rng)
    ratio = e1000 / e10
    assert 1.5 < ratio < 2.6, ratio
    assert abs(math.sqrt(math.log(1000) / math.log(10)) - math.sqrt(3)) < 1e-12
