import numpy as np
import sub

V = np.array([1.0, 2.0, 3.0])
P = np.full(3, 1 / 3)


def test_reciprocal():
    assert abs(sub.plug_in(lambda x: 1 / x, V, P) - 0.5) < 1e-12
    assert abs(sub.expect(lambda x: 1 / x, V, P) - 11 / 18) < 1e-12


def test_square_gap_is_the_variance():
    gap = sub.expect(np.square, V, P) - sub.plug_in(np.square, V, P)
    assert abs(gap - 2 / 3) < 1e-12


def test_convex_gap_is_nonnegative():
    rng = np.random.default_rng(15)
    for _ in range(50):
        v = rng.normal(size=6)
        p = rng.dirichlet(np.ones(6))
        assert sub.expect(np.exp, v, p) >= sub.plug_in(np.exp, v, p) - 1e-12
        assert sub.expect(np.sqrt, v * v, p) <= sub.plug_in(np.sqrt, v * v, p) + 1e-12


def test_relu_factor():
    z = np.random.default_rng(16).standard_normal(1_000_000)
    est = sub.mc_expect(lambda x: np.maximum(x, 0) ** 2, z)
    assert abs(est - sub.relu_second_moment()) < 0.005
    assert sub.relu_second_moment() == 0.5
    assert abs(sub.plug_in(lambda x: np.maximum(x, 0) ** 2, z, np.full(z.size, 1 / z.size))) < 1e-5
