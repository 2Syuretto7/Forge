import numpy as np
import sub

rng = np.random.default_rng(3)


def test_tv_values():
    assert abs(sub.total_variation([0.5, 0.5], [0.9, 0.1]) - 0.4) < 1e-12
    assert sub.total_variation([0.2, 0.8], [0.2, 0.8]) == 0.0


def test_pinsker_holds_on_random_pairs():
    for _ in range(300):
        k = rng.integers(2, 8)
        p, q = rng.dirichlet(np.ones(k)), rng.dirichlet(np.ones(k))
        assert sub.total_variation(p, q) <= sub.pinsker_bound(p, q) + 1e-12


def test_worst_event_attains_tv():
    p, q = rng.dirichlet(np.ones(6)), rng.dirichlet(np.ones(6))
    A = sub.worst_event(p, q)
    assert abs((p[A].sum() - q[A].sum()) - sub.total_variation(p, q)) < 1e-12
