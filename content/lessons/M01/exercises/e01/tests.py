import sub


def test_seconds():
    assert sub.seconds_in_days(1) == 86400
    assert sub.seconds_in_days(365) == 31536000
    assert abs(sub.seconds_in_days(0.5) - 43200) < 1e-9


def test_average():
    assert abs(sub.average([3, 1, 4, 1, 5]) - 2.8) < 1e-12
    assert sub.average([7]) == 7


def test_percent_change():
    assert abs(sub.percent_change(50, 60) - 20) < 1e-12
    assert abs(sub.percent_change(80, 60) - (-25)) < 1e-12


def test_compound():
    assert abs(sub.compound(100, 0.1, 2) - 121) < 1e-9
    assert abs(sub.compound(1000, 0.05, 0) - 1000) < 1e-12
    # Doubling every year for ten years is the 2 ** 10 = 1024 of the recall bridge.
    assert abs(sub.compound(1, 1.0, 10) - 1024) < 1e-9
