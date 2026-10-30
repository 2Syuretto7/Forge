import math
import sub


def test_disc():
    est, se = sub.disc_area(200_000)
    assert abs(est - math.pi) < 4 * se and se < 0.01


def test_error_shrinks():
    _, se1 = sub.disc_area(10_000)
    _, se2 = sub.disc_area(1_000_000)
    assert 8 < se1 / se2 < 12
