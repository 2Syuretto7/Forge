import sub


def test_values():
    assert abs(sub.harmonic(4) - 25 / 12) < 1e-15


def test_grouping_bound_holds():
    for k in range(0, 21):
        assert sub.harmonic(2 ** k) >= sub.grouping_bound(k) - 1e-12


def test_log_estimate():
    for n in [10, 1000, 100000]:
        assert abs(sub.harmonic(n) - sub.log_estimate(n)) < 1 / n


def test_slow_growth():
    assert sub.terms_to_exceed(5) == 83
    assert sub.terms_to_exceed(10) == 12367
