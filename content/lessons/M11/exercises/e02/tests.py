import numpy as np
import sub

A = np.array([[2.0, 1, -1], [-3, -1, 2], [-2, 1, 2]])
b = np.array([8.0, -11, -3])


def test_elimination():
    U, c = sub.eliminate(A, b)
    assert np.allclose(U, [[2, 1, -1], [0, 0.5, 0.5], [0, 0, -1]])
    assert np.allclose(c, [8, 1, 1])
    assert A[1, 0] == -3, "eliminate must not modify its input"


def test_solve():
    assert np.allclose(sub.solve_naive(A, b), [2, 3, -1])


def test_zero_pivot():
    try:
        sub.solve_naive(np.array([[0.0, 1], [1, 1]]), np.array([1.0, 2]))
    except ValueError:
        pass
    else:
        raise AssertionError("a zero pivot without swapping should raise ValueError")
