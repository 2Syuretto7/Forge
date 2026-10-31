import numpy as np
import sub

K = 20
P = 1 / np.arange(1, K + 1)
P /= P.sum()
rng = np.random.default_rng(15)
TRAIN = rng.choice(K, size=30, p=P)
TEST = rng.choice(K, size=5000, p=P)


def test_zero_makes_kl_infinite():
    q = sub.fit(TRAIN, K)
    assert np.any(q == 0) and abs(q.sum() - 1) < 1e-12
    assert sub.kl(P, q) == float("inf")
    assert np.isfinite(sub.kl(q, P))
    assert sub.heldout_ce(q, TEST) == float("inf")


def test_smoothing_repairs_it():
    q = sub.fit(TRAIN, K, 1.0)
    assert np.isfinite(sub.kl(P, q)) and np.isfinite(sub.heldout_ce(q, TEST))
    a = sub.best_alpha(TRAIN, TEST, K, [0.0, 0.1, 0.3, 1.0, 3.0])
    assert a > 0
    assert sub.heldout_ce(sub.fit(TRAIN, K, a), TEST) >= sub.kl(P, sub.fit(TRAIN, K, a)) - 1e-9


def test_kl_basics():
    assert sub.kl([0.5, 0.5], [0.5, 0.5]) == 0.0
    assert abs(sub.kl([0.5, 0.5], [0.9, 0.1]) - 0.5108256237659907) < 1e-12
    assert sub.kl([1.0, 0.0], [0.5, 0.5]) == np.log(2)
