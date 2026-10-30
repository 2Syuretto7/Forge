import numpy as np
import sub

rng = np.random.default_rng(8)


def test_example():
    Q = np.array([[0.6, 0], [0.8, 0], [0, 1.0]])
    b = np.array([1.0, 2, 3])
    assert np.allclose(sub.coefficients(Q, b), [2.2, 3])
    assert np.allclose(sub.project_orthonormal(Q, b), [1.32, 1.76, 3])


def test_invariant_pythagoras():
    for _ in range(100):
        m = int(rng.integers(2, 10))
        n = int(rng.integers(1, m + 1))
        Q, _ = np.linalg.qr(rng.normal(size=(m, n)))
        b = rng.normal(size=m)
        inside, outside = sub.energy_split(Q, b)
        assert np.isclose(inside + outside, b @ b)
        p = sub.project_orthonormal(Q, b)
        assert np.isclose(p @ p, inside)
