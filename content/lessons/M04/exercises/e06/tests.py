import sub


def test_polynomial():
    p = sub.polynomial([5, 6, 1])  # x^2 + 6x + 5
    assert p(-1) == 0 and p(-5) == 0 and p(0) == 5
    assert sub.polynomial([1, 0, 0, 2])(2) == 17
    assert sub.polynomial([])(3) == 0


def test_rational():
    r = sub.rational([1], [0, 1])  # 1/x
    assert r(4) == 0.25
    try:
        r(0)
    except ValueError:
        pass
    else:
        raise AssertionError("1/x at 0 should raise ValueError")


def test_piecewise():
    absval = sub.piecewise([(float("-inf"), 0, lambda x: -x), (0, float("inf"), lambda x: x)])
    assert absval(-3) == 3 and absval(2) == 2 and absval(0) == 0
    step = sub.piecewise([(0, 1, lambda x: 0), (1, 2, lambda x: 1)])
    try:
        step(5)
    except ValueError:
        return
    raise AssertionError("5 is in no piece")
