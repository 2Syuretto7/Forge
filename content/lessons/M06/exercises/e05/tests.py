import math
import sub


def test_doubling():
    assert abs(sub.doubling_time(1.0) - 1) < 1e-12
    assert abs(sub.continuous_doubling_time(0.07) - 9.902102579427789) < 1e-9
    for pct in [1, 2, 5, 7, 10]:
        assert abs(sub.rule_of_70(pct) / sub.continuous_doubling_time(pct / 100) - 1) < 0.02


def test_decay():
    k = 0.3
    t = sub.half_life(k)
    assert abs(math.exp(-k * t) - 0.5) < 1e-12


def test_growth_factor():
    assert abs(sub.growth_factor(0.05, 10) - 1.6487212707001282) < 1e-12
