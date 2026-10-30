import numpy as np
import sub


def test_broadcast_matches_numpy():
    for s1, s2 in [((100,), (100, 1)), ((3, 1), (1, 4)), ((5, 4), (4,)), ((2, 1, 3), (4, 1)), ((), (3,)), ((0,), (1,))]:
        assert sub.broadcast_shape(s1, s2) == np.broadcast(np.empty(s1), np.empty(s2)).shape, (s1, s2)
    try:
        sub.broadcast_shape((3,), (4,))
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")


def test_silent_bug_caught():
    pred = np.linspace(0, 1, 100)
    target = pred.reshape(100, 1)
    assert (pred - target).shape == (100, 100)
    try:
        sub.mse(pred, target)
    except ValueError:
        pass
    else:
        raise AssertionError("mse should refuse (100,) against (100, 1)")
    assert abs(sub.mse(pred, pred + 0.1) - 0.01) < 1e-12
