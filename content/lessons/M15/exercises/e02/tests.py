import math
import sub


def test_values():
    assert abs(sub.forward_diff(lambda x: x * x, 3.0, 0.5) - 6.5) < 1e-12
    assert abs(sub.central_diff(lambda x: x * x, 3.0, 0.5) - 6.0) < 1e-12, "central differences are exact for quadratics"


def test_grad_forward_is_first_order():
    r = sub.error_ratio(math.exp, math.exp, 1.0, 1e-2, "forward")
    assert 1.9 < r < 2.1, f"ratio {r:.3f}"


def test_grad_central_is_second_order():
    r = sub.error_ratio(math.sin, math.cos, 0.7, 1e-2, "central")
    assert 3.9 < r < 4.1, f"ratio {r:.3f}"
    e_f = abs(sub.forward_diff(math.exp, 1.0, 1e-4) - math.e)
    e_c = abs(sub.central_diff(math.exp, 1.0, 1e-4) - math.e)
    assert e_c < e_f / 1000
