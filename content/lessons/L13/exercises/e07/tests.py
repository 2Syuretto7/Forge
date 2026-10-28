import numpy as np
import sub

rng = np.random.default_rng(7)


def test_position_zero_and_norm():
    X = rng.normal(size=(4, 8))
    assert np.allclose(sub.rope(X, np.zeros(4)), X)
    R = sub.rope(X, np.array([1, 5, 20, 300]))
    assert np.allclose(np.linalg.norm(R, axis=1), np.linalg.norm(X, axis=1))


def test_relative_positions():
    q, k = rng.normal(size=(1, 16)), rng.normal(size=(1, 16))
    def score(m, n):
        return float((sub.rope(q, np.array([m])) @ sub.rope(k, np.array([n])).T)[0, 0])
    assert np.isclose(score(3, 7), score(103, 107))
    assert np.isclose(score(0, 4), score(50, 54))
    assert not np.isclose(score(3, 7), score(3, 8))


def test_single_pair():
    x = np.array([[1.0, 0.0]])
    assert np.allclose(sub.rope(x, np.array([2.0])), [[np.cos(2), np.sin(2)]])
