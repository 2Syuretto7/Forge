import sub

sq = lambda x: x * x  # noqa: E731


def test_vanishes():
    assert sub.vanishing_step(1e8, 1e-9)
    assert sub.forward_at(sq, 1e8, 1e-9) == 0.0
    assert sub.smallest_visible_step(1e8) == 1e-8
    assert sub.smallest_visible_step(1.0) == 1e-15


def test_digits():
    assert sub.digits_correct(sub.forward_at(sq, 1.0, 1e-15), 2.0) < 2
    assert sub.digits_correct(sub.forward_at(sq, 1.0, 1e-8), 2.0) > 7
