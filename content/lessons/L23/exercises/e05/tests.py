import numpy as np
import sub

rng = np.random.default_rng(1)
nw = 60
prop = rng.integers(0, 2, nw)
emb = rng.normal(size=(nw, 16))
emb[:, 0] += 2 * (prop * 2 - 1)
ids = rng.integers(0, nw, 800)
A = emb[ids] + 0.5 * rng.normal(size=(800, 16))
y = prop[ids].astype(float)


def test_control_labels_are_per_type():
    c = sub.control_labels(ids, 0)
    for w in np.unique(ids):
        assert len(set(c[ids == w])) == 1
    assert 0.2 < c.mean() < 0.8


def test_selectivity():
    c = sub.control_labels(ids, 0)
    assert sub.selectivity(A[:600], y[:600], A[600:], y[600:], c[:600], c[600:]) > 0.15
