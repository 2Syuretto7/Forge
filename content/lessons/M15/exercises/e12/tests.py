import sub


def test_counts():
    assert sub.evaluations(10, "forward") == 11 and sub.evaluations(10, "central") == 20


def test_model():
    assert abs(sub.days_for_model(10 ** 8, 0.1) - 2e7 / 86400) < 1e-6
    assert 230 < sub.days_for_model(10 ** 8, 0.1) < 232
