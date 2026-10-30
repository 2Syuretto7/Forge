import math
import sub


def test_corners():
    assert sub.has_corner(abs, 0.0)
    assert sub.has_corner(lambda x: max(0.0, x), 0.0)
    assert not sub.has_corner(lambda x: x * abs(x), 0.0)
    l, r = sub.one_sided(lambda x: max(0.0, x), 0.0)
    assert abs(l) < 1e-12 and abs(r - 1) < 1e-9


def test_grad_smooth_functions_agree():
    for f, df in [(math.sin, math.cos), (math.exp, math.exp), (lambda x: x ** 3, lambda x: 3 * x * x)]:
        for a in (-1.0, 0.3, 2.0):
            l, r = sub.one_sided(f, a)
            assert abs(l - df(a)) < 1e-5 * max(1, abs(df(a))) and abs(r - df(a)) < 1e-5 * max(1, abs(df(a)))
            assert not sub.has_corner(f, a)


def test_conventions():
    assert sub.relu_grad(0.0) == 0.0 and sub.relu_grad(2.0) == 1.0 and sub.relu_grad(-1.0) == 0.0
    assert sub.abs_subgradients(0.0) == (-1.0, 1.0)
    assert sub.abs_subgradients(-3.0) == (-1.0, -1.0)
