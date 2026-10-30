import numpy as np
import sub

Z = np.array([1000.0, 999.0, 998.0])


def test_naive_fails_stable_does_not():
    assert sub.fails(Z)
    p = sub.stable_softmax(Z)
    assert np.allclose(p, [0.66524096, 0.24472847, 0.09003057])
    assert np.allclose(sub.stable_softmax(Z - 1000), p)


def test_threshold():
    c = sub.smallest_failing_shift(np.array([0.0, -1.0, -2.0]))
    assert c == 710, c
    assert not sub.fails(np.array([0.0, -1.0, -2.0]) + c - 1)
