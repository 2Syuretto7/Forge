import numpy as np
import sub

f = lambda v: v[0] ** 2 + 3 * v[1] ** 2 + v[0] * v[1]  # noqa: E731
grad = lambda v: np.array([2 * v[0] + v[1], 6 * v[1] + v[0]])  # noqa: E731


def test_segments_on_level():
    segs = sub.contour_segments(f, 1.0, 2.0, 60)
    assert len(segs) > 30
    for p, q in segs:
        assert abs(f(p) - 1) < 0.05 and abs(f(q) - 1) < 0.05


def test_grad_perpendicular():
    segs = sub.contour_segments(f, 1.0, 2.0, 80)
    assert sub.max_cosine(segs, grad) < 0.05
