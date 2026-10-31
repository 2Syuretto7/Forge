import sub

A = 4.7534


def test_grad_second_moment():
    h = 1e-6
    for t in (0.0, 1.0, 4.0, 5.5):
        num = (sub.second_moment(t + h, A) - sub.second_moment(t - h, A)) / (2 * h)
        assert abs(num - sub.d_second_moment(t, A)) < 1e-6 * abs(num) + 1e-18


def test_best_shift():
    t = sub.best_shift(A)
    assert A < t < A + 0.3, t
    assert abs(sub.d_second_moment(t, A)) < 1e-12 * sub.second_moment(0.0, A)


def test_samples_needed():
    assert abs(sub.upper_tail(A) - 1e-6) < 1e-8
    naive = sub.relative_error(0.0, A, 10**8)
    assert 0.09 < naive < 0.11
    best = sub.relative_error(sub.best_shift(A), A, 1000)
    assert best < 0.08, best
