import sub


def test_time_is_positive_and_small():
    t = sub.time_matmul(64)
    assert 0 < t < 1


def test_rate_is_plausible():
    r = sub.flops_per_second(128)
    assert 1e6 < r < 1e13, f"{r:.3g} FLOP/s is not a plausible CPU rate"


def test_prediction_from_a_smaller_size():
    rate = sub.flops_per_second(128)
    predicted = sub.predict_seconds(192, rate)
    measured = sub.time_matmul(192)
    ratio = max(predicted / measured, measured / predicted)
    assert ratio < 10, f"prediction {predicted:.3g} s vs measured {measured:.3g} s"


def test_predict_formula():
    assert sub.predict_seconds(1000, 2e9) == 1.0
