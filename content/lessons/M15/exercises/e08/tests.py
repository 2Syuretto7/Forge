import math
import sub


def test_tangent():
    t = sub.tangent(lambda x: x * x, lambda x: 2 * x, 1.0)
    assert t(1.0) == 1.0 and t(3.0) == 5.0


def test_grad_quadratic_error_for_smooth():
    for f, df, a in [(math.exp, math.exp, 0.5), (math.sin, math.cos, 1.0), (math.log, lambda x: 1 / x, 2.0)]:
        r = sub.error_order(f, df, a, 1e-2)
        assert 3.8 < r < 4.2, (f, r)


def test_corner_is_only_linear():
    for slope in (-0.5, 0.0, 0.3, 0.8):
        r = sub.error_order(abs, lambda x: slope, 0.0, 1e-2)
        assert abs(r - 2) < 1e-9
