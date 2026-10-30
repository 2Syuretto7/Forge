import math
import random
import sub

C = sub.Complex


def test_arithmetic():
    z = C(3, 4) * C(0, 1)
    assert (z.re, z.im) == (-4, 3)
    w = C(0, 1) * C(0, 1)
    assert (w.re, w.im) == (-1, 0)
    assert abs(C(3, 4)) == 5
    assert (C(1, 2) + C(3, -1)).close(C(4, 1))
    assert (C(1, 2) - C(3, -1)).close(C(-2, 3))


def test_polar():
    assert sub.from_polar(2, math.pi / 2).close(C(0, 2), 1e-12)
    assert abs(C(-1, 0).arg() - math.pi) < 1e-15


def test_invariant_lengths_multiply_angles_add():
    rnd = random.Random(0)
    for _ in range(2000):
        z = C(rnd.uniform(-5, 5), rnd.uniform(-5, 5))
        w = C(rnd.uniform(-5, 5), rnd.uniform(-5, 5))
        p = z * w
        assert math.isclose(abs(p), abs(z) * abs(w), rel_tol=1e-12)
        d = p.arg() - z.arg() - w.arg()
        assert abs(math.cos(d) - 1) < 1e-9 and abs(math.sin(d)) < 1e-9
        zz = z * z.conj()
        assert abs(zz.re - abs(z) ** 2) < 1e-9 and abs(zz.im) < 1e-12
