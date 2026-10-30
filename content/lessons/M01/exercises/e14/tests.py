import sub


def test_ten_dimes():
    assert sub.sum_floats([0.1] * 10) != 1.0, "0.1 has no exact binary form"
    assert abs(sub.sum_floats([0.1] * 10) - 1.0) < 1e-15
    assert sub.sum_cents([0.1] * 10) == 100


def test_cents_are_exact():
    prices = [19.99, 5.01, 0.10, 0.20, 74.70]
    assert sub.sum_cents(prices) == 10000
    assert isinstance(sub.sum_cents(prices), int)


def test_a_million_cents():
    cents = [0.01] * 1_000_000
    assert sub.sum_cents(cents) == 1_000_000
    assert abs(sub.sum_floats(cents) - 10000) < 1e-5
    drift = sub.drift_cents(cents)
    assert drift > 1000, f"float32 should lose more than 10 dollars here, lost {drift:.0f} cents"
