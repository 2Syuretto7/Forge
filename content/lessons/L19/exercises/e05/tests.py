import sub


def test_schedule():
    assert sub.lr_at(1, 1e-3, 100, 1000) == 1e-5
    assert sub.lr_at(100, 1e-3, 100, 1000) == 1e-3
    assert abs(sub.lr_at(1000, 1e-3, 100, 1000) - 1e-4) < 1e-15
    assert abs(sub.lr_at(5000, 1e-3, 100, 1000) - 1e-4) < 1e-15
    mid = sub.lr_at(550, 1e-3, 100, 1000)
    assert abs(mid - 1e-3 * (0.1 + 0.9 * 0.5)) < 1e-15
    assert all(sub.lr_at(t + 1, 1e-3, 100, 1000) <= sub.lr_at(t, 1e-3, 100, 1000) for t in range(100, 1200))
