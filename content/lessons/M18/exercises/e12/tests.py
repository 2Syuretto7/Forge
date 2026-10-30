import sub


def test_costs():
    assert sub.fd_evaluations(10 ** 4) == 20000
    assert abs(sub.fd_seconds(10 ** 8, 1e-3) / 86400 - 2.3148) < 1e-3
    assert sub.directional_evaluations(5) == 10
    assert sub.analytic_ratio(3.0, 1.5) == 2.0
