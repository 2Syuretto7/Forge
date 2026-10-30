import numpy as np
import sub

rng = np.random.default_rng(6)
A = rng.normal(size=(20, 5))
b = rng.normal(size=20)


def test_invariant_expansion_is_exact():
    for _ in range(100):
        x, u = rng.normal(size=5), rng.normal(size=5)
        t = rng.uniform(-2, 2)
        lhs = sub.loss(x + t * u, A, b)
        rhs = sub.loss(x, A, b) + t * (sub.slope_vector(x, A, b) @ u) + t * t * np.sum((A @ u) ** 2)
        assert abs(lhs - rhs) < 1e-9 * max(1, abs(lhs))


def test_slope_vanishes_at_solution():
    x, *_ = np.linalg.lstsq(A, b, rcond=None)
    assert np.linalg.norm(sub.slope_vector(x, A, b)) < 1e-9


def test_steps_reach_solution():
    ref, *_ = np.linalg.lstsq(A, b, rcond=None)
    x = sub.step_down(A, b, 5000)
    assert np.allclose(x, ref, atol=1e-6)
