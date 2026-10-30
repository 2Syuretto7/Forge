import numpy as np
import sub

rng = np.random.default_rng(0)


def test_values():
    x = np.array([3.0, -4.0])
    assert (sub.l1(x), sub.l2(x), sub.linf(x)) == (7.0, 5.0, 4.0)
    assert sub.in_unit_ball(np.array([0.5, 0.5]), 1) and not sub.in_unit_ball(np.array([0.6, 0.6]), 1)
    assert sub.in_unit_ball(np.array([0.6, 0.6]), 2) and sub.in_unit_ball(np.array([0.9, -0.9]), "inf")


def test_clip():
    g = np.array([30.0, 40.0])
    assert np.allclose(sub.clip_by_norm(g, 5), [3, 4])
    assert sub.clip_by_norm(np.array([0.3, 0.4]), 5) is not None
    assert np.allclose(sub.clip_by_norm(np.array([0.3, 0.4]), 5), [0.3, 0.4])


def test_invariant_norm_inequalities():
    for _ in range(500):
        d = int(rng.integers(1, 40))
        x, y = rng.normal(size=d), rng.normal(size=d)
        assert sub.linf(x) <= sub.l2(x) + 1e-12 <= sub.l1(x) + 2e-12
        assert sub.l1(x) <= np.sqrt(d) * sub.l2(x) + 1e-9
        for f in (sub.l1, sub.l2, sub.linf):
            assert f(x + y) <= f(x) + f(y) + 1e-12
