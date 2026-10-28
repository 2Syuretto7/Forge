import sub


def test_peak():
    assert abs(sub.peak_flops(40, 64, 1.59e9) - 8.1408e12) < 1e6


def test_occupancy_limits():
    assert sub.blocks_per_sm(256, 32, 0) == 4 and sub.occupancy(256, 32, 0) == 1.0
    assert sub.occupancy(256, 128, 0) == 0.5
    assert sub.occupancy(128, 32, 32 * 1024) == 0.25
    assert sub.blocks_per_sm(32, 16, 0) == 16 and sub.occupancy(32, 16, 0) == 0.5
    assert sub.blocks_per_sm(100, 32, 0) == 8
