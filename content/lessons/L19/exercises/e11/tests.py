import sub


def test_correct_resume():
    full = sub.stream(1, 0, 0, 40, 8, 12)
    assert sub.stream(1, 0, 3, 40, 8, 9) == full[3:]
    assert sub.first_divergence(full[3:], sub.stream(1, 0, 3, 40, 8, 9)) is None


def test_buggy_resume_diverges_at_once():
    full = sub.stream(1, 0, 0, 40, 8, 12)
    bad = sub.buggy_resume(1, 0, 3, 40, 8, 9)
    assert sub.first_divergence(full[3:], bad) == 0
    assert sub.first_divergence([(1,), (2,)], [(1,), (3,)]) == 1
