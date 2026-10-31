import numpy as np
import sub

rng = np.random.default_rng(5)
s = rng.normal(size=(4, 6))
t = rng.normal(size=(4, 6)) * 2
y = np.array([0, 3, 5, 1])


def test_grad_distill():
    for T, a in [(1.0, 0.5), (3.0, 0.9), (2.0, 0.0)]:
        _, g = sub.distill_loss(s, t, y, T, a)
        num = np.zeros_like(s)
        for idx in np.ndindex(s.shape):
            P = s.copy()
            P[idx] += 1e-6
            up = sub.distill_loss(P, t, y, T, a)[0]
            P[idx] -= 2e-6
            num[idx] = (up - sub.distill_loss(P, t, y, T, a)[0]) / 2e-6
        assert np.allclose(g, num, atol=1e-7)


def test_matching_the_teacher():
    loss, g = sub.distill_loss(t, t, y, 2.0, 1.0)
    assert abs(loss) < 1e-12 and np.allclose(g, 0)
