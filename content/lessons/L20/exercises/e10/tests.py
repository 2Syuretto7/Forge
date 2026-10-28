import numpy as np
import sub

z = np.array([6.0, 3.0, 2.5, 0.0, -1.0, -3.0])


def test_temperature():
    ents = [sub.entropy(sub.soften(z, T)) for T in [0.5, 1, 2, 4]]
    assert all(a < b for a, b in zip(ents, ents[1:]))
    for T in [0.5, 1, 2, 4]:
        assert np.array_equal(np.argsort(sub.soften(z, T)), np.argsort(z))


def test_topk():
    p = sub.soften(z, 1.0)
    q = sub.topk_teacher(p, 3)
    assert abs(q.sum() - 1) < 1e-12 and np.count_nonzero(q) == 3
    full = sub.topk_teacher(p, 6)
    assert np.allclose(full, p)
