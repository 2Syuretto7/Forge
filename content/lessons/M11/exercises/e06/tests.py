import numpy as np
import sub


def test_sensor_matrix():
    R, piv = sub.rref(np.array([[1.0, 2, 1], [2, 4, 2], [1, 0, 1]]))
    assert piv == [0, 1]
    assert np.allclose(R, [[1, 0, 1], [0, 1, 0], [0, 0, 0]])


def test_wide():
    A = np.array([[1.0, 2, 0, 3], [2, 4, 1, 7]])
    R, piv = sub.rref(A)
    assert piv == [0, 2]
    assert np.allclose(R, [[1, 2, 0, 3], [0, 0, 1, 1]])


def test_identity_and_zero():
    assert sub.rref(np.eye(3))[1] == [0, 1, 2]
    assert sub.rref(np.zeros((2, 2)))[1] == []
