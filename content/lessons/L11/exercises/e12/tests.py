import sub


def test_times():
    assert abs(sub.pipelined_time(100, 2e-3, 6e-3) - (8e-3 + 99 * 6e-3)) < 1e-12
    assert abs(sub.synced_time(100, 2e-3, 6e-3) - 0.8) < 1e-12


def test_slowdown():
    assert abs(sub.sync_slowdown(1, 2e-3, 6e-3) - 1.0) < 1e-12
    assert 1.32 < sub.sync_slowdown(1000, 2e-3, 6e-3) < 1.34
    assert sub.sync_slowdown(10000, 5e-3, 5e-3) > 1.99
