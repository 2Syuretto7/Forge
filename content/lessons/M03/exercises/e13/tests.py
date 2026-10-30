import sub


def test_lines_hold_until_the_division():
    for a in [1, 2.5, -3]:
        assert sub.first_false_line(sub.LINES, a, a) == 4
        assert sub.divisor_at_step(a, a) == 0


def test_holds():
    assert sub.holds(sub.LINES[3], 1, 1)
    assert not sub.holds(sub.LINES[4], 1, 1)
    assert sub.first_false_line(sub.LINES[:4], 2, 2) is None
