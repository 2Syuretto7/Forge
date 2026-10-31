import numpy as np
import sub

W = np.array([0.3, 0.3, 0.4])
M = np.array([[-2.0, 0.0], [2.0, 1.0], [0.0, -2.0]])


def sample(n, rng):
    k = rng.choice(3, size=n, p=W)
    return M[k] + 0.35 * rng.standard_normal((n, 2))


def test_held_out_bandwidth():
    rng = np.random.default_rng(0)
    train, valid = sample(300, rng), sample(300, rng)
    h, losses = sub.choose_bandwidth(train, valid, [0.0, 0.05, 0.1, 0.2, 0.4], rng)
    assert 0.05 <= h <= 0.2 and losses[0] > min(losses)
    s = sub.kde_score(np.zeros((1, 2)), 3.0, train, 0.1)
    assert s.shape == (1, 2) and np.all(np.isfinite(s))
