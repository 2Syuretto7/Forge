import numpy as np
import sub

A = sub.make_noisy()
TOLS = np.logspace(-14, 2, 33)


def test_sweep():
    r = sub.rank_sweep(A, TOLS)
    assert r[0] == 30 and r[-1] == 0
    assert all(a >= b for a, b in zip(r, r[1:])), "rank cannot grow with the tolerance"
    assert r.count(5) >= 8


def test_pivots_and_gap():
    p = sub.pivots(A)
    assert len(p) == 30 and np.all(p[:5] > 1) and np.all(p[5:] < 1e-4)
    assert p[4] / p[5] > 1e4
    assert sub.gap_rank(p) == 5
    assert sub.gap_rank([4.0, 2.0, 1.0, 0.0]) == 3


def test_honest():
    t = sub.honest_tol(1e-6, A.shape)
    assert sub.rank(A, t) == 5
    assert sub.rank(A, t / 1000) > 5
