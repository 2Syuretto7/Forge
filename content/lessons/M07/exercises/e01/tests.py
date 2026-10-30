import math
import random
import sub


def test_conversions():
    assert abs(sub.to_radians(180) - math.pi) < 1e-15
    assert abs(sub.to_degrees(math.pi / 6) - 30) < 1e-12


def test_normalize():
    assert abs(sub.normalize(3 * math.pi) - math.pi) < 1e-12
    assert abs(sub.normalize(-math.pi / 2 - 4 * math.pi) + math.pi / 2) < 1e-12
    assert -math.pi < sub.normalize(-math.pi) <= math.pi
    assert sub.same_direction(0.3, 0.3 + 6 * math.pi) and not sub.same_direction(0.3, 0.3 + math.pi)


def test_invariant_round_trip_and_direction():
    rnd = random.Random(0)
    for _ in range(2000):
        d = rnd.uniform(-1e4, 1e4)
        assert abs(sub.to_degrees(sub.to_radians(d)) - d) < 1e-9
        t = rnd.uniform(-100, 100)
        n = sub.normalize(t)
        assert -math.pi < n <= math.pi
        assert abs(math.cos(n) - math.cos(t)) < 1e-9 and abs(math.sin(n) - math.sin(t)) < 1e-9
