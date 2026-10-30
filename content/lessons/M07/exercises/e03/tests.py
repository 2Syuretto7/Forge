import math
import random
import sub


def close(p, q, tol=1e-12):
    return abs(p[0] - q[0]) < tol and abs(p[1] - q[1]) < tol


def test_quarter_turns():
    assert close(sub.rotate((1, 0), math.pi / 2), (0, 1))
    assert close(sub.rotate((0, 1), math.pi / 2), (-1, 0))
    assert close(sub.rotate_about((2, 1), (1, 1), math.pi), (0, 1))


def test_angles_add():
    rnd = random.Random(0)
    for _ in range(500):
        p = (rnd.uniform(-5, 5), rnd.uniform(-5, 5))
        a, b = rnd.uniform(-3, 3), rnd.uniform(-3, 3)
        assert close(sub.rotate(sub.rotate(p, a), b), sub.rotate(p, a + b), 1e-9)


def test_matrix_agrees():
    for t in [0.3, -2.0, 4.0]:
        p = (1.5, -0.25)
        assert close(sub.apply(sub.rotation_matrix(t), p), sub.rotate(p, t))
