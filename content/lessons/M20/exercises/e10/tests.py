import math
import sub


def test_formula():
    assert abs(sub.ball_volume(2) - math.pi) < 1e-12
    assert abs(sub.ball_volume(3) - 4 * math.pi / 3) < 1e-12
    assert sub.peak_dimension() == 5
    assert sub.cube_fraction(20) < 3e-8


def test_sampling():
    for n in (2, 4, 6, 8, 10):
        p, se = sub.mc_fraction(n, 200_000, seed=n)
        assert abs(p - sub.cube_fraction(n)) < 5 * se + 1e-12, n
