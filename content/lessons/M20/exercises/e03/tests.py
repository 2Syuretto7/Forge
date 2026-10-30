import math
import numpy as np
import sub

polar = lambda q: np.array([q[0] * np.cos(q[1]), q[0] * np.sin(q[1])])  # noqa: E731
sph = lambda q: np.array([q[0] * np.sin(q[1]) * np.cos(q[2]), q[0] * np.sin(q[1]) * np.sin(q[2]), q[0] * np.cos(q[1])])  # noqa: E731
bm = lambda q: np.sqrt(-2 * np.log(q[0])) * np.array([np.cos(2 * np.pi * q[1]), np.sin(2 * np.pi * q[1])])  # noqa: E731


def test_grad_polar_and_spherical():
    for r, t in [(0.5, 0.3), (2.0, 4.0)]:
        assert abs(sub.jacobian_det(polar, [r, t]) - sub.det_polar(r, t)) < 1e-8
    for r, p, t in [(1.0, 0.4, 1.0), (2.5, 2.0, 5.0)]:
        assert abs(abs(sub.jacobian_det(sph, [r, p, t])) - sub.det_spherical(r, p, t)) < 1e-7


def test_grad_box_muller():
    for u1, u2 in [(0.3, 0.6), (0.9, 0.1), (0.05, 0.75)]:
        assert abs(abs(sub.jacobian_det(bm, [u1, u2])) - sub.det_box_muller(u1, u2)) < 1e-5 * sub.det_box_muller(u1, u2)
