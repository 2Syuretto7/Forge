import math
import numpy as np
import sub


def ref_target(x):
    a, b, c = x
    s = a * b + math.sin(c)
    t = math.exp(-s * s / 4)
    u = math.log(1 + a * a) / (1 + t)
    v = sum(u ** k / k for k in range(1, 4))
    w = math.sqrt(a * a + b * b + 1) if a > 0 else math.cos(b) + 2
    y = v * w + math.tanh(c - a)
    return y / (1 + b * b) + 3 * t


def ref_grad(x):
    # Richardson-extrapolated central differences: error far below 1e-9 here.
    g = np.zeros(3)
    for j in range(3):
        def d(h):
            xp = list(x)
            xm = list(x)
            xp[j] += h
            xm[j] -= h
            return (ref_target(xp) - ref_target(xm)) / (2 * h)
        g[j] = (4 * d(1e-3) - d(2e-3)) / 3
        g[j] = (16 * ((4 * d(5e-4) - d(1e-3)) / 3) - g[j]) / 15
    return g


POINTS = [[0.7, -1.2, 0.4], [1.5, 0.3, -0.8], [-0.6, 0.9, 1.1], [-1.4, -0.5, 0.2]]


def test_target_on_floats():
    for p in POINTS:
        assert abs(sub.target(p) - ref_target(p)) < 1e-12


def test_dual_gradient_matches_reference_on_both_branches():
    for p in POINTS:
        g = sub.grad(sub.target, p)
        r = ref_grad(p)
        assert g.shape == (3,)
        assert np.max(np.abs(g - r)) < 1e-9, (p, g, r)


def test_check_reports_agreement():
    for p in POINTS:
        assert sub.check(sub.target, p) < 1e-8


def test_fd_grad_on_a_simple_function():
    g = sub.fd_grad(lambda v: v[0] ** 2 + 3 * v[1], [2.0, 5.0])
    assert np.allclose(g, [4.0, 3.0], atol=1e-8)
