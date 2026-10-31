import sub

P, W = 8.1e12, 320e9


def test_roofline():
    assert abs(sub.ridge_point(P, W) - 25.3125) < 1e-12
    assert sub.attainable(0.5, P, W) == 160e9
    assert sub.attainable(683, P, W) == P
    assert sub.bound(0.5, P, W) == "memory" and sub.bound(683, P, W) == "compute"
    assert sub.bound(25.3125, P, W) == "compute"


def test_times():
    f, b = 2 * 4096**3, 3 * 4096 * 4096 * 4
    assert abs(sub.time_estimate(f, b, P, W) - f / P) < 1e-15
    mv_f, mv_b = 2 * 4096 * 4096, (4096 * 4096 + 2 * 4096) * 4
    assert abs(sub.time_estimate(mv_f, mv_b, P, W) - mv_b / W) < 1e-15
