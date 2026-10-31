import sub


def test_backoff_and_skip():
    s = sub.DynamicLossScaler(scale=1024.0, interval=3)
    assert s.update(True) is False and s.scale == 512.0
    assert s.update(False) is True and s.scale == 512.0


def test_growth():
    s = sub.DynamicLossScaler(scale=8.0, interval=3)
    results = [s.update(False) for _ in range(3)]
    assert results == [True] * 3 and s.scale == 16.0
    s.update(False)
    s.update(True)
    assert s.scale == 8.0
    for _ in range(2):
        s.update(False)
    assert s.scale == 8.0
    s.update(False)
    assert s.scale == 16.0
