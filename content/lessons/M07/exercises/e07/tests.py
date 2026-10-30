import math
import sub


def test_round_trip():
    r, t = sub.to_polar(-3, 4)
    x, y = sub.to_cartesian(r, t)
    assert abs(x + 3) < 1e-12 and abs(y - 4) < 1e-12 and r == 5


def test_square():
    sq = sub.regular_polygon(4)
    assert abs(sub.perimeter(sq) - 4 * math.sqrt(2)) < 1e-12


def test_archimedes():
    assert 3 + 10 / 71 < sub.pi_estimate(96) < 3 + 1 / 7
    assert abs(sub.pi_estimate(10000) - math.pi) < 1e-6
    assert sub.pi_estimate(6) == 3.0 or abs(sub.pi_estimate(6) - 3) < 1e-12
