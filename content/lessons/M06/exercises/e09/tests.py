import sub

XS = [1 + i for i in range(20)]


def test_ticks():
    assert sub.log_ticks(0.05, 2000) == [0.1, 1.0, 10.0, 100.0, 1000.0]
    assert sub.log_ticks(1, 1) == [1.0]


def test_fit_line():
    m, c, r2 = sub.fit_line([0, 1, 2], [1, 3, 5])
    assert abs(m - 2) < 1e-12 and abs(c - 1) < 1e-12 and abs(r2 - 1) < 1e-12


def test_best_axes():
    assert sub.best_axes(XS, [4 * x + 3 for x in XS]) == "linear"
    assert sub.best_axes(XS, [2 * 1.5 ** x for x in XS]) == "semilog"
    assert sub.best_axes(XS, [3 * x ** 2.5 for x in XS]) == "loglog"
