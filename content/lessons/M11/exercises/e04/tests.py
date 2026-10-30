import numpy as np
import sub

rng = np.random.default_rng(0)


def test_solve_and_det():
    for _ in range(50):
        n = int(rng.integers(1, 9))
        A = rng.normal(size=(n, n))
        b = rng.normal(size=n)
        P, L, U = sub.lu(A)
        assert np.allclose(A @ sub.lu_solve(P, L, U, b), b)
        assert np.isclose(sub.det_from_lu(P, U), np.linalg.det(A))


def test_det_sign_needs_swaps():
    A = np.array([[0.0, 1, 0], [0, 0, 1], [1, 0, 0]])
    P, L, U = sub.lu(A)
    assert sub.det_from_lu(P, U) == np.linalg.det(A).round()


def test_many():
    A, B = rng.normal(size=(6, 6)), rng.normal(size=(6, 4))
    assert np.allclose(A @ sub.solve_many(A, B), B)
