import sub


def test_too_much_momentum_is_slow():
    plain = sub.heavy_ball_errors(1.0, 0.5, 0.0, 200)
    heavy = sub.heavy_ball_errors(1.0, 0.5, 0.99, 200)
    assert plain[-1] < 1e-50
    late, early = max(heavy[180:201]), max(heavy[80:101])
    assert late > 0.1
    assert abs((late / early) ** 0.01 - 0.995) < 0.003


def test_stability_boundary():
    assert sub.stable(1.0, 3.9, 0.99) and not sub.stable(1.0, 4.1, 0.99)
    assert sub.heavy_ball_errors(1.0, 4.1, 0.99, 400)[-1] > 1e3
    assert sub.heavy_ball_errors(1.0, 3.9, 0.99, 2000)[-1] < 1e-2
