import numpy as np
import sub

rng = np.random.default_rng(0)


def test_gram():
    X = np.array([[1.0, 2.0], [3.0, 4.0]])
    assert np.allclose(sub.gram(X), [[5, 11], [11, 25]])


def test_invariant_nonnegative_quadratic_form():
    for _ in range(300):
        n, d = int(rng.integers(1, 10)), int(rng.integers(1, 10))
        X = rng.normal(size=(n, d))
        z = rng.normal(size=n)
        G = sub.gram(X)
        q = sub.quadratic_form(G, z)
        assert abs(q - sub.as_squared_length(X, z)) < 1e-9 * max(1, q)
        assert q >= -1e-9
