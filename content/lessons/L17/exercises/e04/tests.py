import numpy as np
import sub

r = np.array([0.0, 0.0, 1.0, 0.0, 2.0])
V = np.array([0.5, 0.4, 0.9, 0.3, 1.0, 0.0])


def test_limits():
    assert np.allclose(sub.gae(r, V, 0.9, 0.0), r + 0.9 * V[1:] - V[:-1])
    assert np.allclose(sub.gae(r, V, 0.9, 1.0), sub.returns(r, 0.9) - V[:-1])


def test_returns():
    assert np.allclose(sub.returns([1, 1, 1], 0.5), [1.75, 1.5, 1.0])
