import sub

P, BW = 65e12, 320e9


def test_one_big_kernel_is_not_launch_bound():
    n = 1 << 24
    t = sub.step_time([(n, 6 * n)], P, BW)
    assert abs(t - 6 * n / BW) < 1e-12
    assert sub.launch_bound_fraction([(n, 6 * n)], P, BW) == 0.0


def test_many_small_kernels_are():
    small = [(4096, 6 * 4096)] * 4096
    t = sub.step_time(small, P, BW)
    assert abs(t - 4096 * 10e-6) < 1e-12
    assert sub.launch_bound_fraction(small, P, BW) == 1.0
    assert t > 100 * sub.step_time([(1 << 24, 6 << 24)], P, BW)
