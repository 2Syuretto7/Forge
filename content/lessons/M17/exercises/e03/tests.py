import math
import sub


def test_accuracy():
    v, n = sub.adaptive_simpson(math.sin, 0, math.pi, 1e-10)
    assert abs(v - 2) < 1e-9
    assert n < 500


def test_concentrates_where_needed():
    f = lambda x: 1 / (x + 0.001)  # noqa: E731
    exact = math.log(1001)
    v, n = sub.adaptive_simpson(f, 0, 1, 1e-10)
    assert abs(v - exact) < 1e-9
    assert n < 10000
    N = 8192
    h = 1 / N
    fixed = h / 3 * sum((1 if k in (0, N) else 4 if k % 2 else 2) * f(k * h) for k in range(N + 1))
    assert abs(fixed - exact) > 1e-7, "a fixed grid with more points is still far less accurate"


def test_can_be_fooled():
    f = lambda x: math.exp(-1e4 * (x - 0.3) ** 2)  # noqa: E731
    v, n = sub.adaptive_simpson(f, 0, 1, 1e-10)
    assert n == 5 and abs(v - math.sqrt(math.pi / 1e4)) > 1e-3
