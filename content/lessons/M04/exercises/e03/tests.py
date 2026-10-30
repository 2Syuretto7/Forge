import math
import sub


def raises(f, x):
    try:
        f(x)
    except ValueError as e:
        return str(e)
    return None


def test_inside_the_domain():
    assert sub.safe_sqrt(9) == 3
    assert abs(sub.safe_log(math.e) - 1) < 1e-15
    assert sub.safe_reciprocal(4) == 0.25


def test_outside_the_domain():
    assert "sqrt" in (raises(sub.safe_sqrt, -1) or "")
    assert raises(sub.safe_log, 0) is not None
    assert raises(sub.safe_reciprocal, 0) is not None


def test_composite_domain():
    # sqrt(1 - x^2) is defined for -1 <= x <= 1.
    g = lambda x: 1 - x * x
    inside = [x / 10 for x in range(-20, 21) if sub.in_composite_domain(lambda y: y >= 0, g, lambda x: True, x / 10)]
    assert min(inside) == -1 and max(inside) == 1
    # log(1/x): x must be non-zero and 1/x positive.
    assert sub.in_composite_domain(lambda y: y > 0, lambda x: 1 / x, lambda x: x != 0, 2)
    assert not sub.in_composite_domain(lambda y: y > 0, lambda x: 1 / x, lambda x: x != 0, -2)
    assert not sub.in_composite_domain(lambda y: y > 0, lambda x: 1 / x, lambda x: x != 0, 0)
