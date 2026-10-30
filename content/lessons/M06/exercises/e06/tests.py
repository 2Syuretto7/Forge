import random
import sub


def test_values():
    assert sub.sigmoid(0) == 0.5
    assert sub.sigmoid(1000) == 1.0 and sub.sigmoid(-1000) == 0.0
    assert abs(sub.sigmoid_derivative(0) - 0.25) < 1e-15


def test_invariant_symmetry_and_inverse():
    rnd = random.Random(0)
    for _ in range(1000):
        x = rnd.uniform(-30, 30)
        assert abs(sub.sigmoid(-x) - (1 - sub.sigmoid(x))) < 1e-15
        if abs(x) < 15:
            assert abs(sub.logit(sub.sigmoid(x)) - x) < 1e-9


def test_derivative_matches_slope():
    for x in [-3.0, -0.5, 0.0, 2.0]:
        h = 1e-6
        slope = (sub.sigmoid(x + h) - sub.sigmoid(x - h)) / (2 * h)
        assert abs(slope - sub.sigmoid_derivative(x)) < 1e-9
