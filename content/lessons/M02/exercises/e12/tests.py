import numpy as np
import sub

rng = np.random.default_rng(5)
X = rng.uniform(0, 10, size=50)
Y = 2.0 * X + 1.0 + rng.normal(scale=1.0, size=50)
PTS = list(zip(X.tolist(), Y.tolist()))


def test_line_through():
    m, c = sub.line_through((1, 3), (3, 7))
    assert abs(m - 2) < 1e-12 and abs(c - 1) < 1e-12


def test_misfit():
    assert sub.misfit([(0, 1), (1, 3)], 2, 1) == 0
    assert sub.misfit([(0, 2), (1, 3)], 2, 1) == 1


def test_best_pair_is_close_to_the_truth():
    m, c = sub.best_pair_line(PTS)
    assert abs(m - 2) < 0.5 and abs(c - 1) < 3
    for i in range(0, 50, 7):
        for j in range(i + 1, 50, 5):
            mm, cc = sub.line_through(PTS[i], PTS[j])
            assert sub.misfit(PTS, m, c) <= sub.misfit(PTS, mm, cc) + 1e-9
    # The line through the best pair still misses more than the best line through all points (M12).
    ls_m, ls_c = np.polyfit(X, Y, 1)
    assert sub.misfit(PTS, ls_m, ls_c) < sub.misfit(PTS, m, c)
