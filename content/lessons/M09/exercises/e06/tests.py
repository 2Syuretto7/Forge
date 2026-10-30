import numpy as np
import sub

rng = np.random.default_rng(0)


def test_properties():
    X = rng.normal(size=(30, 8))
    C = sub.cosine_matrix(X)
    assert C.shape == (30, 30)
    assert np.allclose(np.diag(C), 1) and np.allclose(C, C.T)
    assert np.all(np.abs(C) <= 1 + 1e-12)
    assert np.allclose(np.linalg.norm(sub.normalize_rows(X), axis=1), 1)


def test_most_similar_pair():
    X = rng.normal(size=(20, 5))
    X[13] = 3.0 * X[4] + 0.01 * rng.normal(size=5)
    assert sub.most_similar_pair(X) == (4, 13)
