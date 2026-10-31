import sub


def test_budget():
    C = sub.compute_budget(65e12, 0.3, 1.0)
    assert abs(C - 7.02e16) < 1e9
    N, D = sub.chinchilla_split(C)
    assert abs(N - 2.4187e7) / 2.4187e7 < 1e-3 and abs(D / N - 20) < 1e-9
    assert abs(6 * N * D - C) / C < 1e-12
    assert abs(sub.epochs(D, 1.1154e6) - 433.7) < 0.5
