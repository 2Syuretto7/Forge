import sub


def test_small_network():
    s = [4, 3, 2]
    assert sub.forward_flops(s, 10) == 2 * 10 * (12 + 6)
    assert sub.backward_flops(s, 10) == 4 * 10 * 18 - 2 * 10 * 12
    assert sub.params(s) == 12 + 3 + 6 + 2


def test_ratio_approaches_six():
    r = sub.flops_per_param_per_example([4096] * 9, 32)
    assert 5.3 < r < 6.0, r
    assert sub.backward_flops([4096] * 9, 32) > 1.8 * sub.forward_flops([4096] * 9, 32)
