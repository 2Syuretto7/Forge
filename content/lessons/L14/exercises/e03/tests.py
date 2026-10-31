import sub


def test_collectives():
    assert sub.collective_time("all_reduce", 1e9, 1, 1e-5, 1e11) == 0
    rs = sub.collective_time("reduce_scatter", 1e9, 8, 1e-5, 1e11)
    ag = sub.collective_time("all_gather", 1e9, 8, 1e-5, 1e11)
    ar = sub.collective_time("all_reduce", 1e9, 8, 1e-5, 1e11)
    assert abs(ar - (rs + ag)) < 1e-15 and abs(rs - (7e-5 + 7 / 8 * 1e-2)) < 1e-15


def test_large_rings_cost_latency_not_bandwidth():
    big = sub.collective_time("all_reduce", 1e9, 1024, 0, 1e11)
    assert abs(big - 2e-2) < 1e-4
    lat = sub.collective_time("all_reduce", 1e3, 1024, 1e-5, 1e11)
    assert lat > 100 * sub.collective_time("all_reduce", 1e3, 1024, 0, 1e11)


def test_overlap():
    a = sub.dp_step_time(1e9, 8, 1e-5, 1e11, 0.05, overlap=False)
    b = sub.dp_step_time(1e9, 8, 1e-5, 1e11, 0.05, overlap=True)
    assert b == 0.05 and abs(a - 0.05 - sub.collective_time("all_reduce", 2e9, 8, 1e-5, 1e11)) < 1e-15
