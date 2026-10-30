import sub


def test_values():
    assert abs(sub.correct(0.001, 0.99, 0.99) - 0.0901639344) < 1e-9
    assert 10 < sub.overstatement(0.001, 0.99, 0.99) < 11.5
    assert abs(sub.prosecutor(1e-6, 5_000_001) - 1 / 6) < 1e-6
