import math
import sub

HILL = lambda x: math.exp(-x * x)


def test_interp_is_exact_at_corners():
    g = sub.pl_interp(HILL, -3, 3, 6)
    for j in range(7):
        assert abs(g(-3 + j) - HILL(-3 + j)) < 1e-12


def test_max_error():
    assert sub.max_error(lambda x: x, lambda x: 0, 0, 2) == 2


def test_hill_needs_thirty():
    assert sub.pieces_needed(HILL, -3, 3, 0.01) == 30


def test_a_line_needs_one():
    assert sub.pieces_needed(lambda x: 3 * x - 1, -5, 5, 1e-9) == 1
