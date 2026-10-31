import sub

T4 = sub.T4


def test_ridge():
    assert abs(sub.ridge(T4["fp16"], T4["bw"]) - 203.125) < 1e-9
    assert abs(sub.ridge(T4["fp32"], T4["bw"]) - 25.3125) < 1e-9


def test_time_and_bound():
    n = 1 << 26
    t = sub.roofline_time(n, 6 * n, T4["fp16"], T4["bw"])
    assert abs(t - 6 * n / 320e9) < 1e-15
    assert sub.bound(n, 6 * n, T4["fp16"], T4["bw"]) == "memory"
    f, b = 2 * 4096 ** 3, 3 * 4096 ** 2 * 2
    assert sub.bound(f, b, T4["fp16"], T4["bw"]) == "compute"
    assert abs(sub.roofline_time(f, b, T4["fp16"], T4["bw"]) - f / 65e12) < 1e-15


def test_efficiency():
    f, b = 2 * 4096 ** 3, 3 * 4096 ** 2 * 2
    assert abs(sub.efficiency(f, b, 2 * f / 65e12, T4["fp16"], T4["bw"]) - 0.5) < 1e-12
