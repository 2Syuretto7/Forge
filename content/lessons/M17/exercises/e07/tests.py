import math
import sub


def test_tails():
    assert abs(sub.to_infinity(lambda x: math.exp(-x), 0) - 1) < 1e-9
    assert abs(sub.to_infinity(lambda x: x * math.exp(-x * x), 0) - 0.5) < 1e-9
    assert abs(sub.to_infinity(lambda x: 1 / (x * x), 1) - 1) < 1e-8


def test_singular():
    assert abs(sub.square_root_singular(lambda x: x ** -0.5, 1.0) - 2) < 1e-10
    exact = math.sqrt(math.pi) * math.erf(1)
    assert abs(sub.square_root_singular(lambda x: x ** -0.5 * math.exp(-x), 1.0) - exact) < 1e-10
