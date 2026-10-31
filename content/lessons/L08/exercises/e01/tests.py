import numpy as np
import sub

rng = np.random.default_rng(1)


def test_matches_softmax():
    x = rng.normal(size=37) * 5
    p, m, l = sub.online_softmax(x, block=4)
    ref = np.exp(x - x.max())
    assert np.allclose(p, ref / ref.sum()) and m == x.max()
    assert np.isclose(l, np.exp(x - x.max()).sum())


def test_two_blocks_from_derivation():
    _, m, l = sub.online_softmax(np.array([1.0, 3.0, 2.0, 5.0]), block=2)
    assert m == 5 and abs(l - 1.203438) < 1e-6


def test_large_values_and_merge():
    x = np.array([1000.0, 1001.0, 999.0, 1002.0, 998.0])
    p, _, _ = sub.online_softmax(x, block=2)
    assert np.all(np.isfinite(p)) and np.isclose(p.sum(), 1)
    a, b = x[:2], x[2:]
    _, ma, la = sub.online_softmax(a)
    _, mb, lb = sub.online_softmax(b)
    m1, l1 = sub.merge(ma, la, mb, lb)
    m2, l2 = sub.merge(mb, lb, ma, la)
    _, m, l = sub.online_softmax(x)
    assert m1 == m2 == m and np.isclose(l1, l) and np.isclose(l2, l)
