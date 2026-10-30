import random
import sub

CUBIC = [0.0, -3.0, 0.0, 1.0]  # x^3 - 3x


def test_cubic():
    pts = sub.critical_points(CUBIC)
    assert [round(p, 12) for p in pts] == [-1.0, 1.0]
    assert sub.classify(CUBIC, 1.0) == "min" and sub.classify(CUBIC, -1.0) == "max"
    assert sub.poly_eval(CUBIC, 1.0) == -2.0
    assert sub.classify([0, 0, 0, 0, 1], 0.0) == "flat"


def test_grad_derivative_matches_central_differences():
    rnd = random.Random(0)
    for _ in range(20):
        c = [rnd.uniform(-2, 2) for _ in range(rnd.randint(2, 6))]
        d = sub.poly_deriv(c)
        for x in (-1.3, 0.2, 0.9):
            h = 1e-6
            num = (sub.poly_eval(c, x + h) - sub.poly_eval(c, x - h)) / (2 * h)
            assert abs(sub.poly_eval(d, x) - num) < 1e-7
