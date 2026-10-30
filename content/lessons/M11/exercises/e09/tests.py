import numpy as np
import sub

a, b = np.array([1.0, 0, 1]), np.array([0.0, 1, 1])


def test_independent():
    assert sub.independent([a, b])
    assert not sub.independent([a, b, a + 2 * b])
    assert not sub.independent([a, b, np.ones(3), np.array([1.0, 2, 3])])
    assert not sub.independent([np.zeros(3)])


def test_basis_and_coordinates():
    vs = [a, 2 * a, b, a - b, np.array([0.0, 0, 1])]
    assert sub.pick_basis(vs) == [0, 2, 4]
    c = sub.coordinates([a, b], 3 * a - 2 * b)
    assert np.allclose(c, [3, -2])
