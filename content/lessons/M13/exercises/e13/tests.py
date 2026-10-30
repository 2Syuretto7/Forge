import numpy as np
import sub

SWAP = np.array([[0.0, 1], [1, 0]])


def test_swap_never_settles():
    h = sub.power_history(SWAP, [1.0, 0.0], 50)
    assert len(h) == 51
    assert not sub.settled(h)
    assert np.allclose(h[50], [1, 0])


def test_negative_dominant_settles():
    h = sub.power_history(np.diag([-3.0, 1.0]), [1.0, 1.0], 60)
    assert sub.settled(h)


def test_shift_fixes_it():
    assert np.isclose(sub.shifted_top(SWAP, 1.0, 40, [1.0, 0.3]), 1.0)
    assert np.isclose(sub.shifted_top(SWAP, -1.0, 40, [1.0, 0.3]), -1.0)
