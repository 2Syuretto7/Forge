import sub

PLANTED = sorted(["quadratic form", "softmax", "normalize", "layer norm, mean term dropped", "square elementwise"])


def test_suite_size():
    assert len(sub.SUITE) == 25


def test_grad_finds_exactly_the_planted_bugs():
    assert sub.run_suite() == PLANTED


def test_grad_correct_ones_are_tight():
    for e in sub.SUITE:
        if e[0] not in PLANTED:
            assert sub.check(e) < 1e-6, e[0]


def test_relative_error():
    assert sub.relative_error([[1.0, 2.0]], [[1.0, 2.0]]) == 0.0
    assert abs(sub.relative_error([[2.0]], [[1.0]]) - 1 / 3) < 1e-15
