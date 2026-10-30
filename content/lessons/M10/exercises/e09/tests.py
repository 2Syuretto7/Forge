import numpy as np
import sub

H = np.random.default_rng(5).normal(size=(3, 4))


def test_recover_matrix():
    f = lambda x: H @ x
    assert sub.is_linear(f, 4)
    assert np.allclose(sub.matrix_of(f, 4), H)
    rot = lambda x: np.array([x[0] * 0.6 - x[1] * 0.8, x[0] * 0.8 + x[1] * 0.6])
    assert np.allclose(sub.matrix_of(rot, 2), [[0.6, -0.8], [0.8, 0.6]])


def test_not_linear():
    assert not sub.is_linear(lambda x: H @ x + 1, 4)
    assert not sub.is_linear(lambda x: np.maximum(H @ x, 0), 4)
    assert not sub.is_linear(lambda x: x * np.linalg.norm(x), 4)
    assert sub.is_linear(lambda x: np.cumsum(x), 5)
