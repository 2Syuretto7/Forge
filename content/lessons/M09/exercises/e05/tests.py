import numpy as np
import sub

rng = np.random.default_rng(0)


def test_example():
    p = sub.project(np.array([3.0, 4.0]), np.array([1.0, 0.0]))
    assert np.allclose(p, [3, 0])
    assert sub.component(np.array([3.0, 4.0]), np.array([0.0, 2.0])) == 4


def test_invariant_geometry():
    for _ in range(300):
        d = int(rng.integers(2, 20))
        a, b = rng.normal(size=d), rng.normal(size=d)
        p, r = sub.project(b, a), sub.residual(b, a)
        assert abs(r @ a) < 1e-9 * np.linalg.norm(a) * np.linalg.norm(b)
        assert np.allclose(sub.project(p, a), p)
        assert abs(b @ b - (p @ p + r @ r)) < 1e-9 * (b @ b)
