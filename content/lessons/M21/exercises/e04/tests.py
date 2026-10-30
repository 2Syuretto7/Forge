import numpy as np
import sub


def test_two_tests():
    P = sub.two_tests(0.1, 0.9, 0.8)
    assert abs(P.sum() - 1) < 1e-12
    assert sub.cond_independent(P)
    assert not sub.independent(P, 0, 1)
    assert np.allclose(sub.marginal(P, (2,)), [0.9, 0.1])


def test_independent_table():
    a, b, c = np.array([0.3, 0.7]), np.array([0.6, 0.4]), np.array([0.5, 0.5])
    P = np.einsum("i,j,k->ijk", a, b, c)
    assert sub.independent(P, 0, 1) and sub.cond_independent(P) and sub.independent(P, 0, 2)
