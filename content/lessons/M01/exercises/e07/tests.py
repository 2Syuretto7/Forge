import math
import random
import sub

I = sub.Interval


def test_construction():
    a = I(2, 8)
    assert (a.lo, a.hi) == (2, 8)
    for lo, hi in [(0, 1), (3, 2), (-1, 1)]:
        try:
            I(lo, hi)
        except ValueError:
            continue
        raise AssertionError(f"Interval({lo}, {hi}) should raise ValueError")


def test_arithmetic():
    p = I(2, 3) * I(10, 20)
    assert (p.lo, p.hi) == (20, 60)
    q = I(10, 20) / I(2, 5)
    assert (q.lo, q.hi) == (2, 10)
    r = I(2, 3) * 4
    assert (r.lo, r.hi) == (8, 12)


def test_mid_and_factor():
    a = I(10, 1000)
    assert abs(a.mid() - 100) < 1e-9
    assert abs(a.factor() - 10) < 1e-9
    assert a.contains(10) and a.contains(1000) and not a.contains(1001)


def test_invariant_points_stay_inside():
    rnd = random.Random(7)
    for _ in range(2000):
        a_lo, b_lo = rnd.uniform(0.1, 10), rnd.uniform(0.1, 10)
        A = I(a_lo, a_lo * rnd.uniform(1, 5))
        B = I(b_lo, b_lo * rnd.uniform(1, 5))
        x, y = rnd.uniform(A.lo, A.hi), rnd.uniform(B.lo, B.hi)
        P, Qt = A * B, A / B
        assert P.lo * (1 - 1e-12) <= x * y <= P.hi * (1 + 1e-12)
        assert Qt.lo * (1 - 1e-12) <= x / y <= Qt.hi * (1 + 1e-12)
        assert math.isclose((A * B).mid(), A.mid() * B.mid(), rel_tol=1e-12)
