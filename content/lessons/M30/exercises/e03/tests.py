import numpy as np
import sub

rng = np.random.default_rng(3)


def test_simplex_projection():
    for _ in range(50):
        y = rng.normal(size=7) * 2
        p = sub.project_simplex(y)
        assert abs(p.sum() - 1) < 1e-12 and p.min() >= 0
        assert np.allclose(sub.project_simplex(p), p)
        for _ in range(5):
            z = rng.dirichlet(np.ones(7))
            assert (y - p) @ (z - p) <= 1e-12


def test_ball_and_box():
    assert np.allclose(sub.project_ball([3.0, 4.0], 1.0), [0.6, 0.8])
    assert np.allclose(sub.project_ball([0.3, 0.4], 1.0), [0.3, 0.4])
    assert np.allclose(sub.project_box([-2.0, 0.5, 9.0], 0.0, 1.0), [0.0, 0.5, 1.0])


def test_quadratic_over_the_simplex():
    c = np.array([0.8, 0.5, -0.4, 0.1])
    x = sub.projected_gd(lambda v: v - c, sub.project_simplex, np.full(4, 0.25), 0.5, 200)
    assert np.allclose(x, sub.project_simplex(c), atol=1e-9)
    assert np.allclose(x, [0.65, 0.35, 0.0, 0.0], atol=1e-9)
