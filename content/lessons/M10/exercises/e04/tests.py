import numpy as np
import sub

rng = np.random.default_rng(0)


def test_examples():
    assert np.allclose(sub.rotation(np.pi / 2) @ [1, 0], [0, 1])
    assert np.allclose(sub.shear(2) @ [1, 1], [3, 1])
    assert np.allclose(sub.reflection(np.pi / 4) @ [1, 0], [0, 1])
    assert np.allclose(sub.reflection(0) @ [1, 1], [1, -1])
    assert np.isclose(np.linalg.det(sub.scaling(2, 3)), 6)


def test_invariant_rotations_and_reflections():
    for _ in range(200):
        a, b, phi = rng.uniform(-4, 4, size=3)
        x, y = rng.normal(size=2), rng.normal(size=2)
        R = sub.rotation(a)
        assert np.isclose((R @ x) @ (R @ y), x @ y)
        assert np.allclose(sub.rotation(a) @ sub.rotation(b), sub.rotation(a + b))
        F = sub.reflection(phi)
        assert np.allclose(F @ F, np.eye(2))
        assert np.isclose(np.linalg.det(F), -1)
