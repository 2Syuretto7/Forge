import numpy as np
import sub

rng = np.random.default_rng(1)
EXP = rng.exponential(size=200000)
UNI = rng.random(200000)


def test_markov():
    for a in (1, 2, 5):
        assert sub.tail_prob(EXP, a) <= sub.markov_bound(1.0, a)
    assert sub.markov_bound(1.0, 0.5) == 1.0
    assert abs(sub.tail_prob(EXP, 5) - np.exp(-5)) < 0.001


def test_chebyshev():
    for k in (1.5, 2, 3):
        assert sub.two_sided_prob(EXP, 1.0, k) <= sub.chebyshev_bound(1.0, k)
        assert sub.two_sided_prob(UNI, 0.5, k * np.sqrt(1 / 12)) <= sub.chebyshev_bound(1 / 12, k * np.sqrt(1 / 12))


def test_chebyshev_is_tight():
    k = 2.0
    vals = rng.choice([-k, 0.0, k], size=400000, p=[1 / (2 * k * k), 1 - 1 / (k * k), 1 / (2 * k * k)])
    assert abs(sub.chebyshev_bound(1.0, k) - 0.25) < 1e-15
    assert abs(sub.two_sided_prob(vals, 0.0, k) - 0.25) < 0.003
