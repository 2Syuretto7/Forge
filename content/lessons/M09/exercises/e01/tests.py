import random
import sub

V = sub.Vec


def test_basics():
    v = V([1, 2, 2])
    assert v.norm() == 3 and len(v) == 3
    assert (v + V([1, 0, 0])).c == [2, 2, 2]
    assert (2 * v).c == [2, 4, 4] and (v * 2).c == [2, 4, 4]
    assert abs(v.unit().norm() - 1) < 1e-15


def test_errors():
    for f in [lambda: V([1, 2]) + V([1, 2, 3]), lambda: V([0, 0]).unit()]:
        try:
            f()
        except ValueError:
            continue
        raise AssertionError("expected ValueError")


def test_invariant_bilinear_and_scaling():
    rnd = random.Random(0)
    for _ in range(500):
        d = rnd.randint(1, 8)
        u, v, w = (V([rnd.uniform(-3, 3) for _ in range(d)]) for _ in range(3))
        a, b, k = rnd.uniform(-2, 2), rnd.uniform(-2, 2), rnd.uniform(-2, 2)
        assert abs(u.dot(w) - w.dot(u)) < 1e-12
        assert abs((a * u + b * v).dot(w) - (a * u.dot(w) + b * v.dot(w))) < 1e-9
        assert abs((k * v).norm() - abs(k) * v.norm()) < 1e-9
