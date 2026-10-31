import numpy as np
import sub

rng0 = np.random.default_rng(12)
V = 30
P = rng0.dirichlet(np.full(V, 0.3), size=V)


def test_cold_loops_hot_rambles():
    cold = sub.generate(P, 0, 300, 0.05, np.random.default_rng(1))
    warm = sub.generate(P, 0, 300, 1.0, np.random.default_rng(1))
    hot = sub.generate(P, 0, 300, 5.0, np.random.default_rng(1))
    assert len(cold) == 301
    assert sub.distinct_ratio(cold) < 0.2 < sub.distinct_ratio(warm)
    assert sub.model_nll(cold, P) < sub.model_nll(warm, P) < sub.model_nll(hot, P)


def test_distinct_ratio():
    assert sub.distinct_ratio([1, 2, 1, 2, 1, 2], 2) == 2 / 5
    assert sub.distinct_ratio(list(range(10))) == 1.0
