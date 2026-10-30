import numpy as np
import sub

rng = np.random.default_rng(2)
f = lambda v: np.sin(v[0]) * np.exp(v[1]) + v[2] ** 2  # noqa: E731
grad = lambda v: np.array([np.cos(v[0]) * np.exp(v[1]), np.sin(v[0]) * np.exp(v[1]), 2 * v[2]])  # noqa: E731


def test_grad_directional_matches():
    for _ in range(20):
        x, u = rng.normal(size=3), rng.normal(size=3)
        d = sub.directional(grad, x, u)
        assert abs(d - sub.numerical_directional(f, x, u)) < 1e-7 * max(1, abs(d))
        assert abs(d) <= np.linalg.norm(grad(x)) + 1e-12


def test_steepest():
    x = rng.normal(size=3)
    u = sub.steepest(grad, x)
    assert np.isclose(np.linalg.norm(u), 1)
    assert np.isclose(sub.directional(grad, x, u), np.linalg.norm(grad(x)))
    assert sub.directional(lambda v: np.array([3.0, 4.0]), None, [1, 0]) == 3.0
