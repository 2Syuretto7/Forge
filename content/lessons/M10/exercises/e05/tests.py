import numpy as np
import sub

rng = np.random.default_rng(0)


def test_values():
    assert sub.det2([[3, 1], [1, 2]]) == 5
    assert np.isclose(sub.det3([[2, 0, 1], [1, 3, 2], [1, 1, 1]]), np.linalg.det(np.array([[2, 0, 1], [1, 3, 2], [1, 1, 1]])))
    assert np.allclose(sub.inverse2([[2, 1], [1, 1]]), [[1, -1], [-1, 2]])
    try:
        sub.inverse2([[1, 2], [2, 4]])
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")


def test_invariant_product_rule():
    for _ in range(200):
        A, B = rng.normal(size=(3, 3)), rng.normal(size=(3, 3))
        assert np.isclose(sub.det3(A @ B), sub.det3(A) * sub.det3(B))
        M = rng.normal(size=(2, 2))
        assert np.allclose(sub.inverse2(M) @ M, np.eye(2))
