import numpy as np
import sub


def test_shapes_and_labels():
    X, y = sub.make_spiral(50, 3, seed=1)
    assert X.shape == (150, 2) and y.shape == (150,)
    assert list(np.bincount(y)) == [50, 50, 50]
    assert np.all(np.linalg.norm(X, axis=1) <= 1 + 1e-12)


def test_deterministic():
    a, _ = sub.make_spiral(20, 3, seed=5)
    b, _ = sub.make_spiral(20, 3, seed=5)
    assert np.array_equal(a, b)


def test_linear_model_fails():
    X, y = sub.make_spiral(100, 3, seed=0)
    acc = sub.linear_baseline(X, y)
    assert 0.35 < acc < 0.65, acc
