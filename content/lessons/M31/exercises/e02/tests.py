import sub


def test_bounds_hold():
    for n in (20, 200, 2000):
        for p in (0.05, 0.5, 0.9):
            for eps in (0.02, 0.05, 0.1):
                t = sub.ratio_table(n, p, eps)
                assert t["exact"] <= t["chebyshev"] + 1e-12 and t["exact"] <= t["hoeffding"] + 1e-12


def test_which_bound_wins():
    big = sub.ratio_table(2000, 0.5, 0.05)
    assert big["hoeffding"] < big["chebyshev"] / 100
    small = sub.ratio_table(50, 0.02, 0.1)
    assert small["chebyshev"] < small["hoeffding"]
    assert abs(sub.exact_tail(10, 0.5, 0.0) - 1) < 1e-12
