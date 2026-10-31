import numpy as np
import sub

K = 10


def test_mean_and_uniform():
    p = sub.max_entropy(2.5, K)
    assert abs(sub.mean_of(p) - 2.5) < 1e-9 and abs(p.sum() - 1) < 1e-12
    assert np.all(np.diff(p) < 0)
    assert np.allclose(sub.max_entropy(5.0, K), np.full(K + 1, 1 / (K + 1)), atol=1e-9)


def test_beats_every_rival():
    rng = np.random.default_rng(9)
    p = sub.max_entropy(2.5, K)
    H = sub.entropy(p)
    k = np.arange(K + 1)
    for _ in range(200):
        d = rng.normal(size=K + 1)
        d -= d.mean()
        d -= (d @ (k - k.mean())) / ((k - k.mean()) @ (k - k.mean())) * (k - k.mean())
        t = 0.9 * np.min(np.where(d < 0, p / -np.where(d < 0, d, -1), np.inf))
        q = p + t * d
        assert abs(sub.mean_of(q) - 2.5) < 1e-9 and q.min() >= 0
        assert sub.entropy(q) <= H + 1e-12
