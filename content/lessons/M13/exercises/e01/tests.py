import numpy as np
import sub

rng = np.random.default_rng(1)


def test_examples():
    A = np.array([[2.0, 1], [1, 2]])
    assert sub.char_poly2(A) == (1.0, -4.0, 3.0)
    assert sub.eig2_real(A) == (3.0, 1.0)
    assert sub.is_eigenpair(A, 3.0, np.array([1.0, 1.0]))
    assert not sub.is_eigenpair(A, 3.0, np.array([1.0, 0.0]))
    assert not sub.is_eigenpair(A, 3.0, np.zeros(2))
    try:
        sub.eig2_real(np.array([[0.0, -1], [1, 0]]))
    except ValueError:
        pass
    else:
        raise AssertionError("rotation has complex eigenvalues")


def test_invariant_trace_det_and_pairs():
    for _ in range(200):
        a, b, d = rng.normal(size=3)
        A = np.array([[a, b], [b, d]])
        l1, l2 = sub.eig2_real(A)
        assert np.isclose(l1 + l2, a + d) and np.isclose(l1 * l2, a * d - b * b)
        w, V = np.linalg.eigh(A)
        assert sub.is_eigenpair(A, l1, V[:, 1]) and sub.is_eigenpair(A, l2, V[:, 0])
