import numpy as np
import sub


def test_product():
    rng = np.random.default_rng(0)
    A, B = rng.normal(size=(7, 7)), rng.normal(size=(7, 7))
    C, count = sub.matmul(A.tolist(), B.tolist())
    assert np.allclose(C, A @ B)
    assert count == 343 == sub.predicted_multiply_adds(7)


def test_ratio():
    a = sub.matmul([[1.0] * 16] * 16, [[1.0] * 16] * 16)[1]
    b = sub.matmul([[1.0] * 32] * 32, [[1.0] * 32] * 32)[1]
    assert b / a == sub.predicted_ratio(16) == 8
