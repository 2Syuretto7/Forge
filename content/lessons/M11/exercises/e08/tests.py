import numpy as np
import sub

S = np.array([[1.0, 2, 1], [2, 4, 2], [1, 0, 1]])


def test_puzzle():
    kind, x = sub.classify(S, np.array([4.0, 8, 2]))
    assert kind == "infinite"
    assert np.allclose(S @ x, [4, 8, 2])
    assert sub.classify(S, np.array([4.0, 8.1, 2])) == ("none", None)


def test_unique_and_rectangular():
    A = np.array([[2.0, 1, -1], [-3, -1, 2], [-2, 1, 2]])
    kind, x = sub.classify(A, np.array([8.0, -11, -3]))
    assert kind == "unique" and np.allclose(x, [2, 3, -1])
    T = np.array([[1.0, 0], [0, 1], [1, 1]])
    assert sub.classify(T, np.array([1.0, 2, 3]))[0] == "unique"
    assert sub.classify(T, np.array([1.0, 2, 4]))[0] == "none"
    kind, x = sub.classify(np.array([[1.0, 1, 1]]), np.array([3.0]))
    assert kind == "infinite" and np.isclose(x.sum(), 3)
