import math
import sub


def test_both_square_roots():
    r = sub.all_preimages(lambda x: x * x, 4, -3, 3)
    assert len(r) == 2 and abs(r[0] + 2) < 1e-9 and abs(r[1] - 2) < 1e-9


def test_sine():
    r = sub.all_preimages(math.sin, 0.5, 0, 10)
    expected = [math.pi / 6, 5 * math.pi / 6, math.pi / 6 + 2 * math.pi, 5 * math.pi / 6 + 2 * math.pi]
    assert len(r) == 4
    assert all(abs(a - b) < 1e-9 for a, b in zip(r, expected))


def test_no_solution():
    assert sub.all_preimages(lambda x: x * x, -1, -3, 3) == []
