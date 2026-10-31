import sub

W, c, BW = 14e9, 0.5e9, 2e12


def test_grad_throughput():
    for b in [1, 8, 64]:
        num = (sub.throughput(b + 1e-4, W, c, BW) - sub.throughput(b - 1e-4, W, c, BW)) / 2e-4
        assert abs(sub.marginal_throughput(b, W, c, BW) - num) < 1e-6 * num


def test_saturation_and_latency():
    assert sub.throughput(1, W, c, BW) < sub.throughput(64, W, c, BW) < BW / c
    b = sub.largest_batch_within(0.02, W, c, BW)
    assert (W + b * c) / BW <= 0.02 < (W + (b + 1) * c) / BW
    assert sub.largest_batch_within(0.001, W, c, BW) == 0
