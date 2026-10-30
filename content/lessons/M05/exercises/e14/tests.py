import math
import sub


def test_usual_order():
    assert abs(sub.alternating(200000) - math.log(2)) < 1e-5


def test_one_up_two_down_halves_it():
    assert abs(sub.one_up_two_down(200000) - math.log(2) / 2) < 1e-5


def test_steer_anywhere():
    for target in [0.0, 1.5, -0.7, 3.0]:
        assert abs(sub.steer(target, 400000) - target) < 1e-3, target
