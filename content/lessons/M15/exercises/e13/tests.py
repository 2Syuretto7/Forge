import math
import sub

relu = lambda x: max(0.0, x)  # noqa: E731


def test_abs_and_relu():
    e = sub.estimates_at_zero(abs, 1e-6)
    assert e["central"] == 0.0 and e["forward"] == 1.0 and e["backward"] == -1.0
    assert abs(sub.estimates_at_zero(relu, 1e-6)["central"] - 0.5) < 1e-12


def test_detect():
    assert not sub.looks_differentiable(abs, 0.0)
    assert not sub.looks_differentiable(relu, 0.0)
    assert sub.looks_differentiable(math.sin, 0.0)
    assert sub.looks_differentiable(lambda x: x * abs(x), 0.0)
